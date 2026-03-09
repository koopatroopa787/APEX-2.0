import os
import logging
from typing import Dict, Any, List, Callable, Optional
import autogen
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from opentelemetry import trace
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class AgentFrameworkIntegration:
    """
    Microsoft Agent Framework Integration for APEX Platform.
    Combines Semantic Kernel for planning and AutoGen for multi-agent conversations.
    Uses A2A (Agent-to-Agent) protocol and Activity Protocol.
    """
    def __init__(self):
        # Configuration retrieved from environment variables
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        self.foundry_api_key = os.getenv("FOUNDRY_API_KEY")
        
        self.kernel = sk.Kernel()
        self._setup_kernel()
        
        self.llm_config = {
            "config_list": [{
                "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "gpt-4"),
                "api_key": self.api_key,
                "base_url": self.endpoint,
                "api_type": "azure",
                "api_version": "2023-12-01-preview"
            }],
            "temperature": 0.2,
        }

    def _setup_kernel(self):
        """Initializes Semantic Kernel with Azure integration."""
        if not self.endpoint or not self.api_key:
            logger.warning("Azure OpenAI credentials missing. Semantic Kernel might not function correctly.")
            return

        azure_chat_service = AzureChatCompletion(
            service_id="default",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "phi-3-mini"),
            endpoint=self.endpoint,
            api_key=self.api_key
        )
        self.kernel.add_service(azure_chat_service)
        logger.info("Semantic Kernel initialized with Azure Chat Completion.")

    def create_autogen_agent(self, name: str, system_message: str, is_user_proxy: bool = False) -> autogen.ConversableAgent:
        """Creates an AutoGen agent for A2A communication."""
        if is_user_proxy:
            return autogen.UserProxyAgent(
                name=name,
                system_message=system_message,
                human_input_mode="NEVER",
                max_consecutive_auto_reply=10,
                code_execution_config={"work_dir": "workspace"},
            )
        else:
            return autogen.AssistantAgent(
                name=name,
                system_message=system_message,
                llm_config=self.llm_config,
            )

    async def execute_plan(self, goal: str, planner_agent: autogen.ConversableAgent, executor_agents: List[autogen.ConversableAgent]) -> str:
        """
        Executes a plan using the Plan-and-Execute pattern.
        """
        with tracer.start_as_current_span("AgentFramework.ExecutePlan") as span:
            span.set_attribute("goal", goal)
            
            all_agents = [planner_agent] + executor_agents
            groupchat = autogen.GroupChat(agents=all_agents, messages=[], max_round=20)
            manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)
            
            try:
                logger.info(f"Initiating agent correlation for goal: {goal}")
                planner_agent.initiate_chat(manager, message=goal)
                return "Plan executed successfully based on group consensus."
            except Exception as e:
                span.record_exception(e)
                logger.error(f"Execution failed: {e}")
                raise e

    def get_semantic_function(self, plugin_name: str, function_name: str) -> Optional[Callable]:
        """Retrieves a semantic function for specialized agent execution."""
        try:
            return self.kernel.get_function(plugin_name, function_name)
        except Exception:
            logger.warning(f"Plugin {plugin_name} or function {function_name} not found.")
            return None
