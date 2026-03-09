from mcp_servers.base_server import BaseMCPServer
import asyncio
from typing import Dict, Any, List

class AzureMonitorServer(BaseMCPServer):
    """
    MCP server exposing underlying Azure Monitor metrics to the agents.
    """
    def __init__(self):
        super().__init__("azure_monitor", "1.0")

    def _register_tools(self):
        self.add_tool("get_metrics", "Fetch real-time metric streams for a resource.", self.get_metrics)
        self.add_tool("query_logs", "Run a KQL query against Log Analytics.", self.query_logs)
        self.add_tool("get_alerts", "Retrieve actively firing Azure Monitor alerts.", self.get_alerts)

    async def get_metrics(self, resource_uri: str, metric_names: List[str], timespan: str = "PT1H") -> Dict[str, Any]:
        # Emulating Azure Monitor call...
        await asyncio.sleep(0.1)
        return {"resource": resource_uri, "metrics": {k: [42.0, 45.1, 44.8] for k in metric_names}}

    async def query_logs(self, query: str, timespan: str = "PT1H") -> Dict[str, Any]:
        # Emulating Log Analytics query...
        await asyncio.sleep(0.2)
        return {"rows_returned": 5, "data": [{"timestamp": "2026-02-20T12:00:00Z", "message": "High CPU utilization detected."}]}

    async def get_alerts(self, severity: int = 2) -> Dict[str, Any]:
        return {"active_alerts": [{"id": "alt_123", "name": "DB CPU Spike", "severity": 1}]}
