import os
from typing import Optional, Dict, Any
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

from agents.base_agent import BaseAgent
from agents.meta_orchestrator.environment import MetaQoSEnv

class MetaRLAgent(BaseAgent):
    """
    PPO-based Agent responsible for system-wide QoS, budget allocation, 
    and throttling across the APEX platform.
    """
    def __init__(self, config: Dict[str, Any], model_path: Optional[str] = None):
        super().__init__("meta_rl_agent", "Meta Orchestrator", "Orchestrator")
        self.log_dir = config.get("log_dir", "logs/ppo_meta")
        self.env = make_vec_env(MetaQoSEnv, n_envs=1) # High-level decisions usually don't need massive parallelism
        
        if model_path and os.path.exists(model_path):
            self.model = PPO.load(model_path, env=self.env)
        else:
            self.model = PPO(
                "MlpPolicy",
                self.env,
                verbose=1,
                tensorboard_log=self.log_dir,
                learning_rate=0.0003,
                n_steps=512,
                batch_size=32,
                n_epochs=10,
                gamma=0.95, # Meta decisions have shorter horizons than query batching
            )

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines platform-wide throttling and budget allocation based on current metrics.
        """
        state = task.get("state")
        if state is None:
            # For demo fallback: generate a random valid state if none provided
            state = self.env.observation_space.sample()
            
        action, _ = self.model.predict(state, deterministic=True)
        
        result = {
            "status": "success",
            "budget_allocation_ratio": float(action[0]),
            "throttling_factor": float(action[1]),
            "priority_boost": float(action[2]),
            "response": "Platform QoS adjusted based on RL policy."
        }
        return result

    def train(self, total_timesteps: int = 50000, save_path: str = "models/rl_checkpoints/meta_agent"):
        """
        Train the Meta agent on the QoS environment.
        """
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        checkpoint_callback = CheckpointCallback(
            save_freq=5000,
            save_path=os.path.dirname(save_path),
            name_prefix="meta_agent_checkpoint"
        )
        
        self.model.learn(
            total_timesteps=total_timesteps,
            callback=checkpoint_callback,
            tb_log_name="PPO_meta",
            progress_bar=True
        )
        self.model.save(save_path)
        return {"status": "success", "save_path": save_path}
