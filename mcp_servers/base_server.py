from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable
import logging

logger = logging.getLogger(__name__)

class BaseMCPServer(ABC):
    """
    Base implementation for a Model Context Protocol (MCP) Server.
    Complies with MCP 2026 standardized request/response schema.
    """
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Callable] = {}
        self._register_tools()

    @abstractmethod
    def _register_tools(self):
        """Register the specific tools exposed by this server."""
        pass

    def add_tool(self, name: str, description: str, handler: Callable):
        """Registers a tool with the MCP server."""
        self.tools[name] = {"description": description, "handler": handler}
        logger.info(f"[{self.name}] Registered tool: '{name}'")

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Entry point for executing an MCP request payload."""
        req_type = request.get("type", "unknown")
        
        if req_type == "list_tools":
            return {"status": "success", "tools": {k: v["description"] for k, v in self.tools.items()}}
            
        elif req_type == "call_tool":
            tool_name = request.get("tool")
            params = request.get("params", {})
            if tool_name not in self.tools:
                return self._error_response("ToolNotFound", f"Tool '{tool_name}' not discovered in {self.name}.")
            try:
                result = await self.tools[tool_name]["handler"](**params)
                return {"status": "success", "result": result}
            except Exception as e:
                logger.error(f"[{self.name}] Execution error for '{tool_name}': {e}")
                return self._error_response("ExecutionFailed", str(e))
        else:
            return self._error_response("InvalidRequest", f"Unsupported request type: {req_type}")

    def _error_response(self, code: str, message: str) -> Dict[str, Any]:
        """Standardized MCP error envelope."""
        return {
            "status": "error",
            "error_code": code,
            "message": message
        }
