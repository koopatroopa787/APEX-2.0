# Enterprise Azure Architecture

## Overview
APEX complies with Azure enterprise architecture standards to guarantee zero-trust security and scalable operation without "Pilot Purgatory."

## Services Integrated
1. **Azure Container Apps**: Hosts our isolated Multi-Agent microservices and MCP Servers. Dynamically scales to zero based on KEDA triggers. 
2. **Azure Cosmos DB**: Serverless persistent memory configured with the Free Tier to limit burn. Partitioned per `agent_id`.
3. **Application Insights & OpenTelemetry**: Instruments Python apps out-of-the-box tracking cross-agent A2A correlations.
4. **Log Analytics Workspace**: The central SIEM metric sink.
5. **Azure Key Vault**: Stores `AZURE_OPENAI_API_KEY` and other credentials.
6. **Azure Managed Identities**: Facilitates secretless connections between Container Apps and Key Vault/CosmosDB.
7. **Azure Cost Management**: Polled by our MCP Server.
8. **Azure Monitor**: Dashboards and Action Group triggers.

## Deployment Strategy
All Azure resources are entirely tracked via Infrastructure as Code (IaC) using **Azure Bicep**.
- `deployment/azure/resource-group.bicep`: Stamps the global required dependencies.
- `deployment/azure/container-apps.bicep`: Sets up the agent clusters.

Execute `./scripts/setup_azure.sh` to replicate the infrastructure.
