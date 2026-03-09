from agents.query_intelligence.agent import QueryIntelligenceAgent

def run_training_loop(episodes: int = 100):
    """
    Runner for the Query Intelligence training loop.
    """
    config = {
        "agent_id": "query_optimizer_v1",
        "verbose": 1,
        "model_path": "models/rl_checkpoints/query_agent"
    }
    
    agent = QueryIntelligenceAgent(config)
    results = agent.train(episodes=episodes)
    return results

if __name__ == "__main__":
    print("Initializing training for Query Intelligence Agent")
    results = run_training_loop(episodes=50) # Smaller default for testing
    print(f"Training completed: {results}")
