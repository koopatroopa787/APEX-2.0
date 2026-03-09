import logging
import numpy as np
import gymnasium as gym
from gymnasium import spaces

logger = logging.getLogger(__name__)

class CostRoutingEnv(gym.Env):
    """
    Custom Gym environment representing Cost-Performance tradeoffs for A2C Model Selection.
    State: [query_complexity, historical_cost, target_latency_ms]
    Action: {0: phi-3-local (free), 1: claude-3-sonnet (balanced), 2: gpt-4 (expensive)}
    """
    def __init__(self):
        super(CostRoutingEnv, self).__init__()
        # Ensure we define the correct spaces
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 10.0]),
            high=np.array([1.0, 1000.0, 5000.0]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(3)
        self.reset()
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array([np.random.rand(), 0.0, np.random.uniform(50, 1000)], dtype=np.float32)
        self.step_count = 0
        return self.state, {}

    def step(self, action):
        complexity, hist_cost, target_lat = self.state
        self.step_count += 1
        
        # Action Cost and Latency Mapping
        model_stats = {
            0: {"cost": 0.00, "lat": 50, "qual": 0.4},   # Phi-3
            1: {"cost": 0.015, "lat": 200, "qual": 0.8}, # Sonnet
            2: {"cost": 0.03, "lat": 400, "qual": 0.98}  # GPT-4
        }
        
        stats = model_stats[action]
        latency = stats["lat"]
        cost = stats["cost"]
        quality = stats["qual"]
        
        # Quality must meet complexity
        quality_penalty = 0.0
        if quality < complexity:
            quality_penalty = (complexity - quality) * 10
            
        # Latency must meet target
        latency_penalty = 0.0
        if latency > target_lat:
            latency_penalty = (latency - target_lat) / 100.0
            
        # Update state
        hist_cost += cost
        new_complexity = np.random.rand()
        self.state = np.array([new_complexity, hist_cost, target_lat], dtype=np.float32)
        
        # Reward: Maximize (quality / cost) but harshly penalize missing SLA
        reward = quality - (cost * 10) - quality_penalty - latency_penalty
        done = self.step_count >= 100
        
        return self.state, float(reward), done, False, {}
