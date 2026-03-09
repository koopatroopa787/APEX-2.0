import logging
from typing import Dict, Any
from agents.workload_vision.vision_models import VisionModels
from agents.workload_vision.metric_analyzer import MetricAnalyzer

logger = logging.getLogger(__name__)

class WorkloadVisionAgent:
    """
    Agent 5: Parses visually rendered charts looking for degradation patterns
    like Query Explosions spanning multiple agents.
    """
    def __init__(self):
        self.vision_models = VisionModels()
        self.analyzer = MetricAnalyzer()
        
    async def analyze_dashboard(self, image_path: str) -> Dict[str, Any]:
        """
        Full pipeline: Capture -> Preprocess -> Isolate Graphs -> Run CV -> Generate Alerts.
        """
        try:
            logger.info(f"Vision Agent analyzing dashboard: {image_path}")
            
            # 1. Image Preprocessing
            img_normalized = self.analyzer.preprocess_image(image_path)
            
            # 2. Graph Isolation
            graph_region = self.analyzer.extract_graph_regions(img_normalized)
            
            # 3. Model Prediction
            result = self.vision_models.predict_anomaly(graph_region)
            
            # 4. Synthesize with OCR
            text_metrics = self.analyzer.parse_text_metrics(image_path)

            alert = False
            if result.get("anomaly_detected"):
                logger.warning("VISUAL ANOMALY DETECTED IN DASHBOARD PIPELINE.")
                alert = True

            return {
                "alert": alert,
                "reconstruction_error": result.get("reconstruction_error", 0.0),
                "ocr_metrics": text_metrics
            }
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            return {"alert": False, "error": str(e)}
