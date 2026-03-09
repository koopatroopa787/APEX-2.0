# Microsoft Agent Framework Architecture

## Overview
The APEX platform leverages the **Microsoft Agent Framework** to power its intelligent multi-agent system. This framework combines the orchestration capabilities of Semantic Kernel and the conversational flows of AutoGen.

## Core Components
### 1. Extensibility & Orchestration (`integrations/agent_framework.py`)
- Deep integration with **Semantic Kernel (≥0.9.0)** for plan inference.
- **AutoGen** is used for agent-to-agent (A2A) conversational patterns, specifically implementing the "Supervisor" pattern.
- Azure OpenTelemetry captures insights directly into Application Insights.

### 2. Base Agent Architecture (`agents/base_agent.py`)
- Extends the core interfaces.
- Implements `_pre_process` and `_post_process` hooks to automatically inject persistent memory retrievals and telemetry generation without polluting domain logic.

### 3. Meta Orchestrator (`agents/meta_orchestrator/coordinator.py`)
- Implements a central supervisor that coordinates up to 5 specialized agents.
- Uses `asyncio.Queue` for asynchronous A2A message dispatching and fallback resilience.
- Manages shared global state accessible across all agents avoiding duplicate LLM calls.

### 4. Persistent Memory (`agents/meta_orchestrator/memory.py`)
- Backed by **Azure Cosmos DB**.
- Records every agent decision and extracted optimization pattern.
- Provides robust context retrieval to ensure long-term learning patterns apply dynamically.

## Communication Protocol
- We adhere to the **Activity Protocol**.
- Messages encapsulate `content`, `sender_id`, `recipient_id`, and extensive JSON `metadata` for precise routing and tracing headers. 
