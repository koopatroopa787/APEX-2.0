# APEX Platform - Environment & API Setup Guide

This document details every required API key, endpoint, and environment variable needed to run the APEX platform locally and in production.

To get started locally, copy `.env.example` to `.env` in the root directory:
```bash
cp .env.example .env
```

## 1. Microsoft Foundry Credentials (Agent 1)
Foundry serves as the AI gateway for compliance, PII-scrubbing, and enterprise routing.

- **`FOUNDRY_ENDPOINT`**: The base URL for the Foundry APIs (e.g., `https://api.foundry.microsoft.com/v1`).
- **`FOUNDRY_API_KEY`**: Your unique authentication token.
  - **How to get it**: Log into your Microsoft Foundry Developer Portal, navigate to your workspace, and generate a new API token under the Security/Credentials tab.

## 2. LLM Provider Credentials (Agent 2 & 4)
The platform uses the Microsoft AutoGen framework heavily wrapped around Azure OpenAI for enterprise-grade data privacy.

- **`AZURE_OPENAI_ENDPOINT`**: Your specific Azure OpenAI resource URL.
- **`AZURE_OPENAI_API_KEY`**: The key for your Azure OpenAI resource.
- **`AZURE_OPENAI_DEPLOYMENT_GPT4`**: The name you gave your GPT-4 model deployment within the Azure portal (usually `gpt-4` or `gpt-4-turbo`).
  - **How to get it**: In the Azure Portal, create an "Azure OpenAI" resource. Once deployed, find "Keys and Endpoint" under the Resource Management sidebar. Create your model deployments in Azure AI Studio.

## 3. Azure Infrastructure Credentials (Agent 6)
APEX relies on Azure Cosmos DB for persistent memory and Application Insights for telemetry.

### Cosmos DB (Persistent Agent State)
*Note: In production Container Apps, APEX uses zero-trust Managed Identities.*
- **`COSMOS_DB_ENDPOINT`**: Your Cosmos NoSQL endpoint URI.
- **`COSMOS_DB_KEY`**: Your read-write primary key (for local dev only).
  - **How to get it**: Create an Azure Cosmos DB (Core/NoSQL) resource in the Azure Portal. Go to "Keys" under Settings. Copy the URI and PRIMARY KEY. Make sure to create a Database named `apex-memory-db` and a Container named `agents` with partition key `/agent_id`.

### OpenTelemetry / Application Insights
- **`APPLICATIONINSIGHTS_CONNECTION_STRING`**: For tracing Agent-to-Agent (A2A) calls.
  - **How to get it**: Create an Application Insights resource in Azure. The Connection String is immediately visible on the Overview page.

## 4. MCP Servers & External Integrations (Agent 3)

### Alert Server Webhooks
- **`SLACK_WEBHOOK_URL`**: Used by the MCP Alert server to notify human operators of critical Agent 5 (Computer Vision) or Agent 7 (Production Readiness) anomalies.
  - **How to get it**: Go to your Slack Workspace settings -> Custom Integrations -> Incoming Webhooks. Create a new webhook for your desired alerting channel.

## 5. Running the Application with Environment Variables

### Python Backend / Agents
The Python scripts utilize the `python-dotenv` package. Make sure it is installed (`pip install python-dotenv`). At the top of our main orchestration scripts, it automatically loads `.env`.

### React Frontend
If running the frontend independently, be aware that Create React App requires variables to be prefixed with `REACT_APP_`.
- `REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws`
