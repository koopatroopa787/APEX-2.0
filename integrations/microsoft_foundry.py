import os
import json
import httpx
import logging
from typing import Dict, Any, Optional
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import asyncio

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class FoundryClient:
    """
    Microsoft Foundry Integration for APEX Platform.
    Provides methods for Model Routing, Foundry IQ, and Control Plane API.
    """
    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None, 
                 client_secret: Optional[str] = None, api_base: str = "https://foundry.microsoft.com/api/v1",
                 api_key: Optional[str] = None):
        self.api_base = api_base
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.access_token: Optional[str] = None
        self._async_client = httpx.AsyncClient()

    async def _authenticate(self):
        """Authenticates with Azure Entra ID to get a token."""
        if not self.tenant_id or not self.client_id or not self.client_secret:
            logger.error("Entra ID credentials missing for OAuth flow.")
            return
        # Standard OAuth2 flow omitted here. Using placeholder for hackathon.
        self.access_token = "mock_entra_token_2026"
    
    async def _ensure_auth(self):
        # If API key is provided, we use it directly in the header instead of Entra token
        if self.api_key:
            return
            
        if not self.access_token:
            await self._authenticate()

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Makes an HTTP request with retry logic and OpenTelemetry tracing."""
        await self._ensure_auth()
        url = f"{self.api_base}{endpoint}"
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["api-key"] = self.api_key
        else:
            headers["Authorization"] = f"Bearer {self.access_token}"

        with tracer.start_as_current_span(f"Foundry {method} {endpoint}") as span:
            max_retries = 3
            backoff_factor = 1.5
            
            for attempt in range(max_retries):
                try:
                    span.set_attribute("http.method", method)
                    span.set_attribute("http.url", url)
                    
                    if method.upper() == "POST":
                        response = await self._async_client.post(url, headers=headers, json=data)
                    else:
                        response = await self._async_client.get(url, headers=headers)
                    
                    response.raise_for_status()
                    result = response.json()
                    span.set_status(Status(StatusCode.OK))
                    return result
                
                except httpx.HTTPStatusError as e:
                    span.record_exception(e)
                    if e.response.status_code in [429, 500, 502, 503, 504]:
                        logger.warning(f"Rate limited or server error, retrying attempt {attempt+1}/{max_retries}")
                        await asyncio.sleep(backoff_factor ** attempt)
                        continue
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise e
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise e
            raise Exception("Max retries exceeded")

    async def route_model(self, prompt: str, complexity: float) -> Dict[str, Any]:
        """Routes query to optimal model using Foundry Model Router."""
        payload = {
            "prompt": prompt,
            "complexity_score": complexity
        }
        response = await self._make_request("POST", "/router/completions", payload)
        
        # Log cost tracking based on routing logic
        if "model" in response and "usage" in response:
            self._log_cost(response["model"], response["usage"])
            
        return response

    async def query_knowledge_base(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Queries the Foundry IQ knowledge base for RAG patterns."""
        payload = {
            "query": query,
            "top_k": top_k
        }
        return await self._make_request("POST", "/knowledge/query", payload)

    async def check_governance(self, request_payload: Dict[str, Any]) -> bool:
        """Validates requests against governance policies in Foundry Control Plane."""
        try:
            response = await self._make_request("POST", "/control/governance/check", request_payload)
            return response.get("approved", False)
        except Exception as e:
            logger.error(f"Governance check failed: {e}")
            return False

    def _log_cost(self, model: str, usage: Dict[str, int]):
        """Logs the API call with model, tokens, and approximate cost for cost tracking."""
        # Simple lookup for demonstration. In a real system, use cost_orchestrator for accurate billing
        cost_per_1k_tokens = {
            "gpt-4": 0.03,
            "claude-3-sonnet": 0.015,
            "phi-3-local": 0.00
        }
        
        tokens = usage.get("total_tokens", 0)
        rate = cost_per_1k_tokens.get(model, 0.01)
        cost = (tokens / 1000) * rate
        logger.info(f"COST_TRACKING: Model={model}, Tokens={tokens}, Cost=${cost:.4f}")

    async def close(self):
        await self._async_client.aclose()
