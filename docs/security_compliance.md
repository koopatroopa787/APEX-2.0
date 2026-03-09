# APEX Security & Governance

## Core Compliance Strategy
Enterprises fail pilot stages without embedded governance. APEX enforces the following:

- **Secret-less Operations**: APEX utilizes Azure Managed Identities. There are exactly **zero** hardcoded connection strings or passwords required in the configuration layer to access Cosmos DB or Application Insights.
- **RBAC**: Agent applications only request the minimal built-in scopes (`Cosmos DB Data Contributor`, `Key Vault Secrets User`).
- **Foundry Control Plane**: Every incoming prompt and outgoing action passes through the Microsoft Foundry Control Plane (simulated via API call) to enforce explicit PII and compliance boundary evaluations.

## Data Retention & Isolation
- Cosmos DB Memory Collections rely on explicit document TTLs (e.g. 30 Days) enforcing the "right to be forgotten."
- Container Apps strictly run in individual micro-environments without root privileges (`activeRevisionsMode: Single`).
- Communication strictly isolates via standard MCP payloads. 
