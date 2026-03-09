import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from integrations.agent_framework import AgentFrameworkIntegration
from agents.meta_orchestrator.coordinator import MetaOrchestrator
from agents.base_agent import BaseAgent
from shared.agent_interfaces import AgentMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("APEX-Demo")

class MockSpecializedAgent(BaseAgent):
    """
    A mock implementation of a specialized agent for demonstration.
    """
    async def execute_task(self, task: dict) -> dict:
        # Simulate processing time
        await asyncio.sleep(0.5)
        payload = task.get("payload", "")
        return {
            "status": "success",
            "response": f"Processed '{payload}' using specialized logic.",
            "timestamp": datetime.now().isoformat()
        }

async def run_apex_demo():
    logger.info("Starting APEX Platform Architecture Demo...")
    
    # 1. Initialize Microsoft Agent Framework Integration
    # This loads SK and AutoGen configs from .env
    framework = AgentFrameworkIntegration()
    
    # 2. Initialize MetaOrchestrator
    # This also initializes the RL Intelligence Engines (Query, Cost, Meta)
    orchestrator = MetaOrchestrator(framework)
    
    # 3. Register specialized agents
    vision_agent = MockSpecializedAgent("vision", "Workload Vision", "Analyzer")
    readiness_agent = MockSpecializedAgent("readiness", "Production Readiness", "Validator")
    user_proxy_mock = MockSpecializedAgent("user_proxy", "User Proxy", "Human Interface")
    
    orchestrator.register_agent("vision", vision_agent)
    orchestrator.register_agent("readiness", readiness_agent)
    orchestrator.register_agent("user_proxy", user_proxy_mock)
    
    # 4. Start the Coordinator in the background
    coordinator_task = asyncio.create_task(orchestrator.run_coordinator())
    
    # 5. Simulate Agentic Workload
    logger.info("Simulating incoming agentic workload...")
    
    test_messages = [
        AgentMessage(content="Analyze query burst in region west-us", sender_id="user_proxy", recipient_id="vision"),
        AgentMessage(content="Validate deployment safety for v2.1.0", sender_id="user_proxy", recipient_id="readiness"),
        AgentMessage(content="Correlate latency spikes with batch size", sender_id="vision", recipient_id="readiness"),
    ]
    
    for msg in test_messages:
        logger.info(f"Injecting message: {msg.sender_id} -> {msg.recipient_id}")
        await orchestrator.message_queue.put(msg)
        # Simulate time spacing between requests
        await asyncio.sleep(1)

    # 6. Allow time for RL agents to process and coordinate
    logger.info("Waiting for RL coordination to finalize...")
    await asyncio.sleep(5)
    
    # 7. Cleanup
    orchestrator.stop_coordinator()
    await coordinator_task
    
    logger.info("Demo completed successfully. Check logs for RL routing decisions.")

if __name__ == "__main__":
    # Ensure logs directory exists for RL models
    os.makedirs("logs", exist_ok=True)
    
    try:
        asyncio.run(run_apex_demo())
    except KeyboardInterrupt:
        pass
