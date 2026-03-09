import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import logging
from torch.utils.data import DataLoader, TensorDataset
from agents.workload_vision.vision_models import DashboardAutoencoder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_dashboard_images(num_samples: int = 1000):
    """
    Generates dummy grayscale images resembling normalized graphs.
    """
    logger.info(f"Generating {num_samples} synthetic dashboard charts for CV training.")
    # Real graphs are lines on mostly solid background
    data = np.random.uniform(0, 0.2, (num_samples, 1, 64, 64)).astype(np.float32)
    # Add a synthetic "line"
    for i in range(num_samples):
        y, x = np.random.randint(10, 50, 2)
        data[i, 0, y:y+5, x:x+5] += 0.5
    return torch.tensor(data)

def train_autoencoder(epochs: int = 5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Training CV Autoencoder on device: {device}")
    
    model = DashboardAutoencoder().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    
    # Generate Training data
    train_data = generate_synthetic_dashboard_images(5000)
    train_loader = DataLoader(TensorDataset(train_data, train_data), batch_size=32, shuffle=True)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch_features, _ in train_loader:
            batch_features = batch_features.to(device)
            optimizer.zero_grad()
            outputs = model(batch_features)
            loss = criterion(outputs, batch_features)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        logger.info(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")

    os.makedirs('models/cv_checkpoints', exist_ok=True)
    torch.save(model.state_dict(), 'models/cv_checkpoints/autoencoder.pth')
    logger.info("CV Anomaly Detection model saved.")

if __name__ == "__main__":
    train_autoencoder(10)
