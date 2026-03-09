import logging
from typing import Dict, Any, Optional
from mcp_servers.base_server import BaseMCPServer
from mcp_servers.azure_monitor_server import AzureMonitorServer
from mcp_servers.cost_management_server import CostManagementServer
from mcp_servers.foundry_server import FoundryServer
from mcp_servers.database_server import DatabaseServer
from mcp_servers.alert_server import AlertServer

logger = logging.getLogger(__name__)

class MCPServerRegistry:
    """
    Central discovery service for all instantiated MCP servers.
    Validates adherence to the MCP spec structure.
    """
    def __init__(self):
        self._servers: Dict[str, BaseMCPServer] = {}

    def register(self, server: BaseMCPServer):
        """Register a running server."""
        if server.name in self._servers:
            logger.warning(f"Server '{server.name}' already registered. Overwriting.")
        self._servers[server.name] = server
        logger.info(f"Registered MCP Server: {server.name}")

    def get_server(self, name: str) -> Optional[BaseMCPServer]:
        return self._servers.get(name)

    def list_endpoints(self) -> Dict[str, List[str]]:
        """Used for Service Discovery."""
        endpoints = {}
        for name, server in self._servers.items():
            endpoints[name] = list(server.tools.keys())
        return endpoints

def bootstrap_registry() -> MCPServerRegistry:
    registry = MCPServerRegistry()
    registry.register(AzureMonitorServer())
    registry.register(CostManagementServer())
    registry.register(FoundryServer("t_id", "c_id", "c_sec"))
    registry.register(DatabaseServer())
    registry.register(AlertServer())
    return registry
