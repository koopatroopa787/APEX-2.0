from mcp_servers.base_server import BaseMCPServer
from integrations.microsoft_foundry import FoundryClient
from typing import Dict, Any, List

class FoundryServer(BaseMCPServer):
    """
    MCP server for Microsoft Foundry Capabilities.
    Bridges agent tools and Foundry intelligence.
    """
    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        super().__init__("foundry", "1.0")
        import os
        api_key = os.getenv("FOUNDRY_API_KEY")
        api_base = os.getenv("FOUNDRY_ENDPOINT", "https://foundry.microsoft.com/api/v1")
        self.client = FoundryClient(tenant_id, client_id, client_secret, api_base=api_base, api_key=api_key)

    def _register_tools(self):
        self.add_tool("list_models", "List deployed models available for routing.", self.list_models)
        self.add_tool("route_query", "Evaluate and route query to safest/cheapest model.", self.route_query)
        self.add_tool("get_deployment_info", "Retrieve region metrics for deployed endpoints.", self.get_deployment_info)

    async def list_models(self) -> Dict[str, Any]:
        return {"models": ["gpt-4", "claude-3-sonnet", "phi-3-local"]}

    async def route_query(self, prompt: str, complexity_score: float) -> Dict[str, Any]:
        return await self.client.route_model(prompt, complexity_score)

    async def get_deployment_info(self, model_family: str) -> Dict[str, Any]:
        return {
            "model_family": model_family,
            "region": "eastus2",
            "capacity_remaining": "High"
        }
