import pytest
import asyncio
from typing import Dict, Any

from mcp_servers.registry import MCPServerRegistry
from mcp_servers.base_server import BaseMCPServer
from mcp_servers.azure_monitor_server import AzureMonitorServer
from mcp_servers.alert_server import AlertServer

class MockServer(BaseMCPServer):
    def __init__(self):
        super().__init__("mock_server", "1.0")

    def _register_tools(self):
        self.add_tool("echo", "Echos back.", self.echo)

    async def echo(self, text: str) -> str:
        return text

@pytest.fixture
def mock_server():
    return MockServer()

@pytest.mark.asyncio
async def test_base_server_list_tools(mock_server):
    req = {"type": "list_tools"}
    res = await mock_server.handle_request(req)
    assert res["status"] == "success"
    assert "echo" in res["tools"]

@pytest.mark.asyncio
async def test_base_server_call_tool(mock_server):
    req = {"type": "call_tool", "tool": "echo", "params": {"text": "hello mcp"}}
    res = await mock_server.handle_request(req)
    assert res["status"] == "success"
    assert res["result"] == "hello mcp"

@pytest.mark.asyncio
async def test_base_server_invalid_tool(mock_server):
    req = {"type": "call_tool", "tool": "missing_tool", "params": {}}
    res = await mock_server.handle_request(req)
    assert res["status"] == "error"
    assert res["error_code"] == "ToolNotFound"

@pytest.mark.asyncio
async def test_alert_server():
    server = AlertServer()
    req = {"type": "call_tool", "tool": "create_incident", "params": {"title": "Test", "description": "Desc"}}
    res = await server.handle_request(req)
    assert res["status"] == "success"
    assert "INC-" in res["result"]["incident_id"]

def test_registry():
    r = MCPServerRegistry()
    r.register(MockServer())
    assert r.get_server("mock_server") is not None
    assert "echo" in r.list_endpoints()["mock_server"]
