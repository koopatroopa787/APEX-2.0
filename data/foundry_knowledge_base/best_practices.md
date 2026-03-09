# Best Practices for Agentic Workloads on Microsoft Foundry (2026)

## 1. Intelligent Model Routing

To maximize ROI and efficiency on the APEX platform, all agentic queries MUST utilize the **Foundry Model Router**.

*   **Complexity-Based Routing**: Assign a `complexity` score (0.0 to 1.0) to every task.
    *   `> 0.8`: Route to `gpt-4` for high-reasoning tasks (code generation, complex data analysis).
    *   `0.4 - 0.8`: Route to `gpt-35-turbo` or `claude-3-sonnet` for standard NLP tasks.
    *   `< 0.4`: Route to `local-phi-3` or equivalent SLMs for simple extraction and formatting.
*   **Cost Constraints**: Always supply `max_cost` constraints to the router to prevent unexpected billing spikes during autonomous loops.

## 2. Knowledge Base Integration (Foundry IQ)

*   **Schema Enforcement**: All uploaded optimization patterns must strictly adhere to the `schema.json` defined in this repository.
*   **Chunking Strategy**: When ingesting large architecture documents into Foundry IQ, use semantic chunking to keep context windows optimal for retrieval.
*   **Vector Search**: Leverage hybrid search (keyword + vector) configured in the Foundry IQ indexes for highest accuracy on APEX queries.

## 3. Governance and Control Plane

*   **Synchronous Auditing**: Use the `FoundryClient.log_governance_event` method for all state-changing actions taken by agents.
*   **Policy Checks**: Before an agent modifies infrastructure or commits a costly optimization plan, it MUST call `FoundryClient.check_policy_compliance` to ensure cross-tenant safety rules are respected.

## 4. Observability

*   **Tracing**: Maintain the OpenTelemetry spans initialized in `FoundryClient`. Ensure new agent modules hook into `tracer.start_as_current_span`.
*   **Cost Tracking**: Rely on the APEX `CostOrchestrator` to aggregate token usage across model families real-time, preventing autonomous budget overruns.
