import logging
from typing import Dict, Any, Optional
from shared.agent_interfaces import BaseAgentInterface, AgentMessage
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class BaseAgent(BaseAgentInterface):
    """
    Base Agent extending Semantic Kernel / AutoGen concepts.
    Implements common interfaces, memory hooks, telemetry, and error handling.
    """
    def __init__(self, agent_id: str, name: str, role: str):
        super().__init__(agent_id)
        self.name = name
        self.role = role
        self.memory_store = None
        self.state = "idle"

    def register_memory(self, memory_system: Any):
        """Attaches a persistent memory system (e.g., Cosmos DB wrapper)."""
        self.memory_store = memory_system
        logger.info(f"Memory system registered for Agent {self.agent_id}")

    async def _pre_process(self, message: AgentMessage) -> None:
        """Hook for telemetry and memory retrieval before processing."""
        self.state = "processing"
        
        # Optionally retrieve context from memory
        if self.memory_store:
            context = await self.memory_store.retrieve_context(self.agent_id, message.content[:50])
            logger.debug(f"[{self.name}] Context retrieved: {context}")
            
    async def _post_process(self, outcome: Dict[str, Any]) -> None:
        """Hook for telemetry and memory storage after processing."""
        self.state = "idle"
        
        # Store outcome into memory
        if self.memory_store:
            await self.memory_store.store_memory(self.agent_id, outcome)

    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """
        Process an incoming message from the Activity Protocol.
        Wraps domain logic with pre/post hooks.
        """
        with tracer.start_as_current_span(f"Agent-{self.name}.process_message") as span:
            span.set_attribute("agent.id", self.agent_id)
            span.set_attribute("message.sender", message.sender_id)
            
            try:
                await self._pre_process(message)
                
                # Execute domain logic (overridden by sub-classes)
                logger.info(f"[{self.name}] Processing message from {message.sender_id}")
                task_def = {"task_type": "message_response", "payload": message.content}
                
                result = await self.execute_task(task_def)
                await self._post_process(result)

                response_message = AgentMessage(
                    content=result.get("response", "Message processed."),
                    sender_id=self.agent_id,
                    recipient_id=message.sender_id,
                    metadata={"status": "success"}
                )
                return response_message
                
            except Exception as e:
                span.record_exception(e)
                logger.error(f"[{self.name}] Error processing message: {e}")
                self.state = "error"
                return AgentMessage(
                    content=f"Error: {str(e)}",
                    sender_id=self.agent_id,
                    recipient_id=message.sender_id,
                    metadata={"status": "error"}
                )

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific assigned task. Override in subclasses."""
        logger.warning(f"[{self.name}] Base execute_task called. Subclasses should override this.")
        return {"status": "success", "response": f"Task '{task.get('task_type')}' executed by {self.name}"}

    def get_status(self) -> Dict[str, Any]:
        """Return the current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "state": self.state
        }
