import cv2
import torch
import torch.nn as nn
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DashboardAutoencoder(nn.Module):
    """
    PyTorch Autoencoder for detecting anomalies in grafana/dashboard screenshots.
    Learns the "normal" manifold of charts, throwing high reconstruction error on spikes.
    """
    def __init__(self):
        super(DashboardAutoencoder, self).__init__()
        # Simplified ConvNet for image compression
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
        
class VisionModels:
    """Manages the lifecycle and inference of PyTorch models."""
    def __init__(self, model_path: str = "models/cv_checkpoints/autoencoder.pth"):
        self.model = DashboardAutoencoder()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model_path = model_path
        
    def load_weights(self):
        import os
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.eval()
            logger.info("Loaded CV Anomaly Weights successfully.")
            return True
        return False

    def predict_anomaly(self, image_np: np.ndarray, threshold: float = 0.05) -> Dict[str, Any]:
        """
        Calculates MSE Reconstruction Error. If error > threshold, it's a visual anomaly.
        """
        if not self.load_weights():
            return {"status": "untrained", "anomaly_detected": False}

        # Convert to tensor: [B, C, H, W]
        img_tensor = torch.tensor(image_np, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            reconstructed = self.model(img_tensor)
            
        mse_loss = torch.nn.functional.mse_loss(reconstructed, img_tensor).item()
        
        is_anomaly = mse_loss > threshold
        return {
            "status": "success",
            "anomaly_detected": is_anomaly,
            "reconstruction_error": mse_loss,
            "heat_map": np.abs(img_tensor.cpu().numpy() - reconstructed.cpu().numpy())[0][0]
        }
