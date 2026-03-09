import asyncio
import logging
import sys
from integrations.agent_framework import AgentFrameworkIntegration

# Setup basic logging to see the output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

async def run_collaboration_demo():
    """
    Demonstrates the plan-and-execute pattern with Supervisor MetaOrchestrator
    using Semantic Kernel and AutoGen.
    """
    logger.info("Starting APEX Platform Agent Collaboration Demo...")

    # Initialize the Framework Integration
    framework = AgentFrameworkIntegration(
        tenant_id="demo_tenant",
        client_id="demo_client",
        client_secret="demo_secret",
        endpoint="https://demo-endpoint.openai.azure.com/"
    )

    # Note: In a real scenario, API keys and endpoints need to be correctly configured.
    # The current execution will demonstrate the setup of agents via AutoGen.

    # 1. Create Planner (Supervisor) Agent
    planner = framework.create_autogen_agent(
        name="MetaPlanner",
        system_message="You are the Meta Planner. Your job is to break down the goal provided by the user into sub-tasks for the specialists.",
        is_user_proxy=False
    )

    # 2. Create Executor (Specialist) Agents
    cost_agent = framework.create_autogen_agent(
        name="CostOrchestrator",
        system_message="You are the Cost Orchestrator. You calculate and minimize model inference costs for given tasks.",
        is_user_proxy=False
    )

    vision_agent = framework.create_autogen_agent(
        name="WorkloadVision",
        system_message="You are the Computer Vision Monitor. You analyze screenshots to find anomalies in workloads.",
        is_user_proxy=False
    )

    # Define a complex goal for the agents to collaborate on
    goal = "Optimize the platform: Review the recent dashboard screenshot for high latency queries, and compute a cost routing strategy to mitigate the spike."

    # 3. Form GroupChat and run the Plan-and-Execute Pattern
    logger.info(f"Target Goal: {goal}")
    try:
        # In a fully-credentialed environment, this will trigger a multi-turn conversation
        result = await framework.execute_plan(goal, planner, [cost_agent, vision_agent])
        logger.info(f"Demo completed. Strategy outcome: {result}")
    except Exception as e:
        logger.error(f"Demo failed (Expected if LLM credentials are mock): {e}")

if __name__ == "__main__":
    asyncio.run(run_collaboration_demo())
