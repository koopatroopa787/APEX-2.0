import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from integrations.microsoft_foundry import FoundryClient
from agents.cost_orchestrator.router import ModelRouter

@pytest.fixture
def foundry_client():
    return FoundryClient(
        tenant_id="mock_tenant",
        client_id="mock_client",
        client_secret="mock_secret"
    )

@pytest.fixture
def model_router(foundry_client):
    return ModelRouter(foundry_client)

@pytest.mark.asyncio
async def test_foundry_client_auth(foundry_client):
    with patch.object(foundry_client, "_authenticate", new_callable=AsyncMock) as mock_auth:
        await foundry_client._ensure_auth()
        mock_auth.assert_called_once()

@pytest.mark.asyncio
async def test_route_model_success(foundry_client):
    mock_response = {
        "model": "gpt-4",
        "usage": {"total_tokens": 150},
        "choices": [{"message": {"content": "Test response"}}]
    }
    
    with patch.object(foundry_client, "_make_request", new_callable=AsyncMock) as mock_req:
        mock_req.return_value = mock_response
        result = await foundry_client.route_model("Test prompt", 0.9)
        
        assert result["model"] == "gpt-4"
        mock_req.assert_called_with("POST", "/router/completions", {
            "prompt": "Test prompt",
            "complexity_score": 0.9
        })

@pytest.mark.asyncio
async def test_model_router_fallback(model_router):
    with patch.object(model_router.foundry_client, "route_model", new_callable=AsyncMock) as mock_route:
        mock_route.side_effect = Exception("API Error")
        
        result = await model_router.route_query("Test prompt", True)
        
        assert result["status"] == "fallback"
        assert result["model"] == "phi-3-local"
