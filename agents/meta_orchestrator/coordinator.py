import logging
import asyncio
import os
from typing import Dict, Any, List, Optional
from shared.agent_interfaces import AgentMessage
from opentelemetry import trace
import numpy as np

from agents.query_intelligence.agent import QueryIntelligenceAgent
from agents.cost_orchestrator.agent import CostOrchestratorAgent
from agents.meta_orchestrator.agent import MetaRLAgent

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class MetaOrchestrator:
    """
    Coordinates specialized agents with RL-driven intelligence.
    Implements A2A message passing, failure handling, and shared state management.
    Uses RL agents for Query Intelligence, Cost Orchestration, and Meta QoS.
    """
    def __init__(self, agent_framework):
        self.framework = agent_framework
        self.agents: Dict[str, Any] = {}
        self.shared_state: Dict[str, Any] = {
            "total_cost": 0.0,
            "qps": 0.0,
            "latency": 0.0,
            "system_health": 1.0
        }
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self._is_running = False
        
        # Initialize RL Intelligence Engines
        # In production, these would point to saved .zip model paths
        self.query_intel = QueryIntelligenceAgent()
        self.cost_router = CostOrchestratorAgent()
        self.meta_governor = MetaRLAgent(config={"log_dir": "logs/ppo_meta"})

    def register_agent(self, agent_id: str, agent_instance: Any):
        """Registers a specialized agent with the orchestrator."""
        self.agents[agent_id] = agent_instance
        logger.info(f"Agent '{agent_id}' registered under MetaOrchestrator.")

    async def _get_meta_guidance(self):
        """Retrieves high-level QoS guidance from the Meta RL Agent."""
        state = [
            self.shared_state["total_cost"],
            self.shared_state["qps"],
            self.shared_state["latency"],
            self.shared_state["system_health"],
            0.0 # hour placeholder
        ]
        return await self.meta_governor.execute_task({"state": np.array(state, dtype=np.float32)})

    async def dispatch_message(self, message: AgentMessage) -> None:
        """Route message to recipient agent using RL-optimized logic."""
        target_id = message.recipient_id
        if target_id not in self.agents:
            logger.error(f"Recipient {target_id} not found. Dropping message.")
            return

        with tracer.start_as_current_span(f"A2A_Dispatch: {message.sender_id} -> {target_id}") as span:
            # 1. Query Intelligence: Decide on batching/delay
            query_state = [
                self.shared_state["latency"] / 100.0, # db_load proxy
                self.message_queue.qsize(),
                len(self.agents),
                0.3 # default complexity placeholder
            ]
            q_ai = self.query_intel.predict_optimal_batch(np.array(query_state, dtype=np.float32))
            delay_ms = q_ai.get("delay_ms", 0)
            if delay_ms > 500:
                # Artificial delay to prevent DB overload (RL-optimized)
                await asyncio.sleep(delay_ms / 1000.0)

            # 2. Cost Orchestration: Decide on Model Routing
            cost_state = [0.5, self.shared_state["total_cost"], self.shared_state["latency"]/1000.0]
            model_selection = self.cost_router.select_model(*cost_state)
            logger.info(f"RL Cost Router selected {model_selection} for agent {target_id}")
            
            # 3. Meta Guidance: Throttling
            guidance = await self._get_meta_guidance()
            if guidance.get("throttling_factor", 0) > 0.8:
                logger.warning("Meta Governor initiated extreme throttling. Message delayed.")
                await asyncio.sleep(1.0)

            target_agent = self.agents[target_id]
            
            # Simple retry mechanism for agent robustness
            for attempt in range(3):
                try:
                    # Injecting RL metadata into the agent call
                    message.metadata = message.metadata or {}
                    message.metadata["model_preference"] = model_selection
                    
                    response = await target_agent.process_message(message)
                    if response:
                        await self.message_queue.put(response)
                    return
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1} failed for {target_id}: {e}")
                    await asyncio.sleep(1)
            
            logger.error(f"Agent {target_id} failed to process message after 3 attempts.")

    async def run_coordinator(self):
        """Main loop for the MetaOrchestrator."""
        self._is_running = True
        logger.info("MetaOrchestrator loop started with RL Intelligence enabled.")
        while self._is_running:
            try:
                message = await self.message_queue.get()
                await self.dispatch_message(message)
                self.message_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Coordinator error: {e}")

    def stop_coordinator(self):
        """Signals the loop to stop."""
        self._is_running = False
        logger.info("MetaOrchestrator loop stopped.")

    def update_shared_state(self, key: str, value: Any):
        """Updates global state accessible to all agents."""
        self.shared_state[key] = value
        logger.debug(f"Shared state updated: {key} -> {value}")

    def get_shared_state(self, key: str) -> Any:
        return self.shared_state.get(key)
