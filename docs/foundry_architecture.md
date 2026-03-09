# Microsoft Foundry Integration Architecture

## Overview
The APEX Platform deeply integrates with **Microsoft Foundry (2026)** to leverage state-of-the-art Model Routing, Foundry IQ for knowledge bases, and Control Plane governance. This integration serves as the intelligence backbone for the entire agentic system.

## Components

### 1. Foundry Client (`integrations/microsoft_foundry.py`)
- **Authentication**: Managed via Azure Entra ID.
- **Model Router**: Intelligently routes incoming queries to optimal models (`gpt-4`, `claude-3-sonnet`, `phi-3-local`) based on specified complexity.
- **Foundry IQ**: Retrieves patterns and best practices from APEX's knowledge base using RAG.
- **Control Plane**: Validates requests against organizational governance policies before execution.
- **Observability**: Fully instrumented with OpenTelemetry for distributed tracing and error tracking.

### 2. Cost Orchestrator Router (`agents/cost_orchestrator/router.py`)
- Acts as a wrapper over the Foundry Client's routing.
- Validates model cost against a predefined budget line.
- Implements resilient **fallback logic** (e.g., routing to `phi-3-local` if the API is unreachable, ensuring zero downtime for critical agents).
- Summarizes cost per model family to feed into the global Cost Management systems.

### 3. Knowledge Base (`data/foundry_knowledge_base/`)
- Uses structured JSON schemas for optimization patterns.
- Facilitates the "Plan-and-Execute" models by providing agents with historical APEX context.

## Telemetry & Metrics
Every call to Microsoft Foundry is tracked. We record:
- HTTP status and latency.
- Model selected.
- Token usage and computed cost in USD.
