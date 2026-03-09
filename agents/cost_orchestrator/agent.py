import os
import logging
import numpy as np
from stable_baselines3 import A2C
from agents.cost_orchestrator.models import CostRoutingEnv

logger = logging.getLogger(__name__)

class CostOrchestratorAgent:
    """
    RL Agent (A2C) that learns optimal model routing for cost efficiency.
    Learns to balance GPT-4 vs Sonnet vs local models based on query complexity.
    """
    def __init__(self, model_path: str = "models/rl_checkpoints/a2c_cost_orchestrator.zip"):
        self.env = CostRoutingEnv()
        self.model_path = model_path
        self.model = None

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = A2C.load(self.model_path)
            logger.info("Loaded pre-trained A2C Cost Orchestrator model.")
        else:
            logger.warning(f"No existing model at {self.model_path}. Agent needs training.")
            self.model = A2C("MlpPolicy", self.env, verbose=0)
            
    def select_model(self, complexity: float, elapsed_cost: float, target_latency_ms: float) -> str:
        """
        Takes real-time inputs:[query_complexity, historical_cost, target_latency_ms]
        Returns the specific model family to use.
        """
        if not self.model:
            self.load_model()
            
        state = np.array([complexity, elapsed_cost, target_latency_ms], dtype=np.float32)
        action, _states = self.model.predict(state, deterministic=True)
        
        mapping = {0: "phi-3-mini (free)", 1: "phi-3-mini (balanced)", 2: "phi-3-mini (premium-mapped)"}
        return mapping.get(int(action), "phi-3-mini (free)")
