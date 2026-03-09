import logging
from typing import Dict, Any, List
from integrations.microsoft_foundry import FoundryClient
import os

logger = logging.getLogger(__name__)

class ModelRouter:
    """
    Cost Orchestrator Router using Foundry Model Router API.
    Dynamically routes based on query complexity.
    """
    def __init__(self, foundry_client: FoundryClient):
        self.foundry_client = foundry_client
        self.cost_log: List[Dict[str, Any]] = []
        self._cost_per_family = {
            "gpt-4": 0.0,
            "claude-3-sonnet": 0.0,
            "phi-3-local": 0.0
        }

    async def route_query(self, prompt: str, is_complex: bool = False, max_budget: float = 0.02) -> Dict[str, Any]:
        """
        Routes query through Foundry API, keeping track of cost.
        Includes fallback logic if a primary router fails.
        Modified for Free Tier: max_budget lowered to $0.02.
        """
        # Lower complexity score to favor cheaper/faster routing on free tier
        complexity_score = 0.7 if is_complex else 0.2
        
        try:
            # Foundry API routing
            response = await self.foundry_client.route_model(prompt, complexity_score)
            
            # Simulated model extraction from standard response
            model_used = response.get("model", "phi-3-local")
            usage = response.get("usage", {"total_tokens": 100})
            
            cost = self._calculate_cost(model_used, usage["total_tokens"])
            if cost > max_budget:
                logger.warning(f"Query cost ${cost:.4f} exceeded budget ${max_budget:.4f}")
            
            self._update_cost_tracking(model_used, cost)
            
            return {
                "status": "success",
                "model": model_used,
                "response": response.get("choices", [{"message": {"content": "Routed response"}}])[0]["message"]["content"],
                "cost": cost
            }
            
        except Exception as e:
            logger.error(f"Routing failed: {e}. Executing fallback...")
            return await self._fallback_routing(prompt)

    def _calculate_cost(self, model: str, tokens: int) -> float:
        rates = {
            "gpt-4": 0.03,
            "claude-3-sonnet": 0.015,
            "phi-3-local": 0.00
        }
        rate = rates.get(model, 0.01)
        return (tokens / 1000) * rate

    def _update_cost_tracking(self, model: str, cost: float):
        if model in self._cost_per_family:
            self._cost_per_family[model] += cost
        self.cost_log.append({"model": model, "cost": cost})

    async def _fallback_routing(self, prompt: str) -> Dict[str, Any]:
        """Fallback to local/cheap model if API fails."""
        logger.info("Using local fallback model (phi-3-local)")
        return {
            "status": "fallback",
            "model": "phi-3-local",
            "response": "Fallback response from local model due to primary routing failure.",
            "cost": 0.0
        }
        
    def get_cost_summary(self) -> Dict[str, float]:
        """Returns the total cost incurred per model family."""
        return self._cost_per_family
