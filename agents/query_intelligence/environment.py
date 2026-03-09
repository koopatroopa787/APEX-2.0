import logging
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class QueryOptimizationEnv(gym.Env):
    """
    Custom Gym environment for query optimization.
    Simulates reality of DB overload and query backlogs.
    """
    metadata = {"render_modes": ["console"]}

    def __init__(self):
        super(QueryOptimizationEnv, self).__init__()
        # State: [db_load_percent, queue_size, active_agents, avg_query_complexity]
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0, 0, 0.0], dtype=np.float32), 
            high=np.array([100.0, 1000, 50, 1.0], dtype=np.float32),
            dtype=np.float32
        )
        
        # Action: [batch_size (1-50), delay_ms (0-1000)]
        self.action_space = spaces.Box(
            low=np.array([1, 0], dtype=np.float32),
            high=np.array([50, 1000], dtype=np.float32),
            dtype=np.float32
        )
        self.reset()

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None):
        super().reset(seed=seed)
        self.state = np.array([10.0, 5, 2, 0.3], dtype=np.float32)
        self.step_count = 0
        return self.state, {}

    def step(self, action):
        self.step_count += 1
        batch_size, delay_ms = action
        
        db_load, queue_size, agents, complexity = self.state
        
        # Compute dynamics
        processed_queries = min(queue_size, batch_size)
        queue_size -= processed_queries
        
        # New queries arrival based on active agents
        new_queries = max(0, int(np.random.normal(agents * 2, agents * 0.5)))
        queue_size = min(1000, queue_size + new_queries)
        
        # Load recalculation
        db_load = min(100.0, max(0.0, db_load + (processed_queries * complexity * 0.5) - (delay_ms / 100.0)))
        
        # Random walk for agents and complexity
        agents = max(0, min(50, agents + np.random.randint(-1, 2)))
        complexity = max(0.1, min(1.0, complexity + np.random.uniform(-0.05, 0.05)))
        
        self.state = np.array([db_load, queue_size, agents, complexity], dtype=np.float32)
        
        # Reward Function: Penalize high DB load and large queues
        reward = -0.5 * (db_load / 100.0) - 0.5 * (queue_size / 1000.0)
        
        # Severe penalty if DB crashes
        if db_load >= 99.0:
            reward -= 10.0
            done = True
        else:
            done = self.step_count >= 100
            
        return self.state, float(reward), done, False, {}
