# APEX Platform: Reinforcement Learning Intelligence Engine

## Overview
The "Agentic Design & Innovation" criteria emphasize robust and self-optimizing architectures. APEX Platform leverages a tri-agent Reinforcement Learning optimization engine to ensure minimal database overhead, high throughput, and maximum cost-efficiency across all sub-agents.

---

## 1. Query Intelligence Agent (PPO)
*Goal: Batching queries in realtime and mitigating database explosions.*
- **File**: `agents/query_intelligence/agent.py` & `environment.py`
- **Algorithm**: PPO (Proximal Policy Optimization).
- **Reasoning**: PPO excels at continuous control spaces. We must continuously dictate cache decisions and batch sizes to prevent DB throttling.
- **State**: DB load metrics, queue size, active sub-agent count, and query categorizations (high/low priority).
- **Action**: Continuous vectors determining `batch_size`, `timing_delay`, and `cache_decision`.
- **Reward**: Severely penalizes Database saturation (>80% load) and high request latency.

---

## 2. Cost Orchestrator Agent (A2C + MAB)
*Goal: Dynamically routing tasks to local SLMs, Claude 3.5 Sonnet, or GPT-4o.*
- **File**: `agents/cost_orchestrator/agent.py` & `models.py`
- **Algorithm**: A2C (Advantage Actor-Critic) hybridized with a Contextual Multi-Armed Bandit.
- **Reasoning**: Operates perfectly over categorical discrete action spaces (Choose Model A, B, or C) with high sample efficiency.
- **State**: Task complexity estimation, prior cost history, latency requirements.
- **Action**: Discrete choice between `Local_LLM`, `Claude_3.5_Sonnet`, or `GPT-4o`.
- **Reward**: Quality-to-Cost Ratio (QCR). Penalizes SLA breaches or using expensive models for low-complexity tasks.

---

## 3. Meta Orchestrating Agent (PPO)
*Goal: High-level supervisor assigning budgets and dynamically throttling the entire platform.*
- **File**: `agents/meta_orchestrator/agent.py` & `environment.py`
- **Algorithm**: PPO (Proximal Policy Optimization).
- **State**: Total platform cost, throughput (QPS), average latency, overall system health, and time of day.
- **Action**: `budget_allocation_ratio`, `throttling_factor`, and `priority_boost`.
- **Reward**: Balanced optimization of QoS metrics within hard budget constraints.

---

## Training & Data Pipeline
- **Synthesis**: `scripts/generate_synthetic_data.py` seeds 1M+ simulated agent records mimicking Log-Normal ("spiky") behavior typical of autonomous agents.
- **Pipeline**: `scripts/train_agents.py` handles sequential training of all three agents with TensorBoard logging and model checkpointing.
- **Environment**: All agents use custom OpenAI Gym environments (0.26.2) for realistic workload simulation.
