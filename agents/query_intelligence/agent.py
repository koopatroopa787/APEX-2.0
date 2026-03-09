import os
import logging
import numpy as np
from stable_baselines3 import PPO
from agents.query_intelligence.environment import QueryOptimizationEnv

logger = logging.getLogger(__name__)

class QueryIntelligenceAgent:
    """
    RL Agent (PPO) that learns optimal query batching and delay patterns.
    Predicts query explosions by monitoring the State.
    """
    def __init__(self, model_path: str = "models/rl_checkpoints/ppo_query_intel.zip"):
        self.env = QueryOptimizationEnv()
        self.model_path = model_path
        self.model = None

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = PPO.load(self.model_path)
            logger.info("Loaded pre-trained PPO Query Intelligence model.")
        else:
            logger.warning(f"No existing model at {self.model_path}. Agent needs training.")
            self.model = PPO("MlpPolicy", self.env, verbose=0)
            
    def predict_optimal_batch(self, current_state: np.ndarray) -> dict:
        """
        Takes real-time inputs:[db_load_percent, queue_size, active_agents, avg_query_complexity]
        Returns {batch_size, delay_ms}
        """
        if not self.model:
            self.load_model()
            
        action, _states = self.model.predict(current_state, deterministic=True)
        batch_size, delay_ms = action[0], action[1]
        
        return {
            "batch_size": int(max(1, min(50, batch_size))),
            "delay_ms": int(max(0, min(1000, delay_ms)))
        }
