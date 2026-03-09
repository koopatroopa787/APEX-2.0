# Model Context Protocol (MCP) Network Architecture

## Overview
The APEX Platform employs the **Model Context Protocol (MCP)**, conforming to the 2026 standardized specs, to expose external enterprise services—such as Azure Monitor, Cost Management, and Cosmos DB—as standardized tools. This creates an isolated and uniform communication channel between external APIs and the internal "Agent Framework".

## Server Network
APEX hosts 5 bespoke MCP Servers:
1. **Azure Monitor Server**: Streams metric dashboards and executes KQL queries.
2. **Cost Management Server**: Tracks live amortized costs and predicts standard resource breaches.
3. **Foundry Server**: Bridges the intelligent Foundry client into the unified agent pool.
4. **Database Server**: Extracts RU/s loads and query inefficiency for optimization scoring.
5. **Alerts Server**: Re-broadcasts agentic events directly to Slack/Teams/PagerDuty.

## Extensibility Design
- **BaseMCPServer**: Every server inherits from `mcp_servers/base_server.py`. It guarantees JSON-RPC compliant tool registration, request validation, payload mapping, and structured error responses.
- **Registry & Discovery**: The `mcp_servers/registry.py` enforces a discoverable endpoint catalog, allowing Meta Orchestrators to dynamically poll available tool capabilities.

## Infrastructure Standard
All MCP servers run isolated behind an async `FastAPI` instance using SSE streams under heavy production loads, orchestrated by the unified `docker-compose.yml`.
