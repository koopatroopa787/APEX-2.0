import os
import logging
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.env_util import make_vec_env

from agents.query_intelligence.environment import QueryOptimizationEnv
from agents.cost_orchestrator.models import CostRoutingEnv
from agents.meta_orchestrator.environment import MetaQoSEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_query_intelligence(timesteps: int = 100000):
    """
    Trains the PPO agent for Query Batching and DB Load Prediction.
    """
    logger.info("Initializing PPO Training for Query Intelligence...")
    env = make_vec_env(QueryOptimizationEnv, n_envs=4)
    
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, 
        save_path='models/rl_checkpoints/query/',
        name_prefix='query_agent'
    )
    
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="logs/ppo_query")
    model.learn(total_timesteps=timesteps, callback=checkpoint_callback)
    
    os.makedirs('models/rl_checkpoints', exist_ok=True)
    model.save("models/rl_checkpoints/query_agent_final.zip")
    logger.info("Query Intelligence model saved.")

def train_cost_orchestrator(timesteps: int = 100000):
    """
    Trains the A2C engine mapping context to Model Routing.
    """
    logger.info("Initializing A2C Training for Cost Routing...")
    env = make_vec_env(CostRoutingEnv, n_envs=4)
    
    model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="logs/a2c_cost")
    model.learn(total_timesteps=timesteps)
    
    os.makedirs('models/rl_checkpoints', exist_ok=True)
    model.save("models/rl_checkpoints/cost_agent_final.zip")
    logger.info("Cost Orchestrator model saved.")

def train_meta_orchestrator(timesteps: int = 50000):
    """
    Trains the PPO agent for Meta QoS and Budget Orchestration.
    """
    logger.info("Initializing PPO Training for Meta Orchestrator...")
    env = make_vec_env(MetaQoSEnv, n_envs=1)
    
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="logs/ppo_meta")
    model.learn(total_timesteps=timesteps)
    
    os.makedirs('models/rl_checkpoints', exist_ok=True)
    model.save("models/rl_checkpoints/meta_agent_final.zip")
    logger.info("Meta Orchestrator model saved.")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("models/rl_checkpoints", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Train all 3 innovation agents
    train_query_intelligence(50000)
    train_cost_orchestrator(50000)
    train_meta_orchestrator(30000)
    
    logger.info("Innovation Engine: All RL agents trained and evaluation metrics logged.")
