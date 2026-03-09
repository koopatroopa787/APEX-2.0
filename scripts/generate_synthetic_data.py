import numpy as np
import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_workload(num_samples: int = 1000000, output_dir: str = "data/synthetic") -> None:
    """
    Generates realistic agentic workload patterns.
    Uses log-normal distributions for query rates and introduces bursty failure patterns.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    logger.info(f"Generating {num_samples} synthetic workload events...")
    
    # Simulating Spiky/Bursty Agent behavior (Log-Normal Distribution)
    query_rates = np.random.lognormal(mean=2.0, sigma=1.0, size=num_samples)
    
    # Queries possess a general complexity (0.0 to 1.0)
    complexities = np.random.beta(a=2, b=5, size=num_samples)
    
    # Introduce cascading failure scenarios (simulating agent loops)
    for i in range(100, num_samples, 50000):
        burst_size = np.random.randint(500, 2000)
        end_idx = min(i + burst_size, num_samples)
        query_rates[i:end_idx] = np.random.uniform(50, 150, end_idx - i) # Massive spike
        complexities[i:end_idx] = np.random.uniform(0.8, 1.0, end_idx - i) # High complexity tail recursion
        
    df = pd.DataFrame({
        "timestamp_ms": np.cumsum(np.random.exponential(scale=1000 / np.maximum(1, query_rates))),
        "queries_per_sec": query_rates,
        "avg_complexity": complexities,
        "agents_active": np.maximum(1, (query_rates / 5).astype(int)),
        "target_latency_ms": np.random.choice([200, 500, 1500], size=num_samples, p=[0.5, 0.4, 0.1])
    })
    
    filepath = os.path.join(output_dir, "agent_workload_1M.csv")
    df.to_csv(filepath, index=False)
    logger.info(f"Successfully generated 1M+ synthetic records at {filepath}")

if __name__ == "__main__":
    import os
    generate_synthetic_workload()
