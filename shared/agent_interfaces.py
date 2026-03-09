from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class AgentMessage:
    content: str
    sender_id: str
    recipient_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseAgentInterface(ABC):
    """
    Common interface for all APEX platform agents.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process an incoming message from the Activity Protocol."""
        pass

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific assigned task."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return the current agent status."""
        pass
