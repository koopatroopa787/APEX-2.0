import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Any, Tuple

class MetaQoSEnv(gym.Env):
    """
    High-level Meta Orchestrator environment for Quality of Service (QoS) 
    and budget management across the APEX platform.
    """
    def __init__(self, daily_budget: float = 1000.0):
        super().__init__()
        self.daily_budget = daily_budget
        
        # State: [total_cost_spent, throughput_qps, avg_latency_ms, system_health, current_hour]
        # Health is 0 to 1, hour is 0 to 24
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
            high=np.array([daily_budget * 2, 5000.0, 10000.0, 1.0, 24.0]),
            dtype=np.float32
        )
        
        # Action: [budget_allocation_ratio, throttling_factor, priority_boost]
        # All between 0 and 1
        self.action_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0]),
            high=np.array([1.0, 1.0, 1.0]),
            dtype=np.float32
        )
        
        self.current_step = 0
        self.max_steps = 24  # Simulating a day in hourly steps
        self.reset()

    def reset(self, seed: int = None, options: Dict = None) -> Tuple[np.ndarray, Dict]:
        super().reset(seed=seed)
        self.current_step = 0
        self.total_cost = 0.0
        # Initial state: low cost, moderate throughput, low latency, perfect health, start of day
        self._state = np.array([0.0, 100.0, 200.0, 1.0, 0.0], dtype=np.float32)
        return self._state, {}

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        self.current_step += 1
        
        budget_ratio, throttling, p_boost = action
        cost_spent, qps, latency, health, hour = self._state
        
        # Simulate environment dynamics
        # Demand fluctuates based on hour (peak at mid-day)
        demand_factor = np.sin(np.pi * hour / 24.0) + 0.5
        new_qps = demand_factor * 1000.0 * (1.0 - throttling)
        
        # Cost increases with QPS and priority boost
        step_cost = (new_qps * 0.01) + (p_boost * 10.0)
        self.total_cost += step_cost
        
        # Latency increases with QPS but decreases with budget/throttling
        new_latency = (new_qps / 10.0) * (2.0 - budget_ratio) + 100.0
        
        # Health degrades if latency is too high or budget is too low
        new_health = health
        if new_latency > 2000.0:
            new_health -= 0.1
        if budget_ratio < 0.2:
            new_health -= 0.05
        new_health = max(0.0, min(1.0, new_health + 0.05)) # self-healing
        
        self._state = np.array([
            self.total_cost, new_qps, new_latency, new_health, float(self.current_step)
        ], dtype=np.float32)
        
        # REWARD FUNCTION
        # Reward for high throughput and high health
        reward = (new_qps / 100.0) * new_health
        
        # Penalty for exceeding budget
        if self.total_cost > self.daily_budget:
            reward -= 100.0
            
        # Penalty for high latency
        if new_latency > 1000.0:
            reward -= (new_latency / 500.0)
            
        terminated = self.current_step >= self.max_steps
        truncated = False
        
        return self._state, float(reward), terminated, truncated, {"total_cost": self.total_cost}
