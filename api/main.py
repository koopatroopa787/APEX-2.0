import os
import json
import asyncio
import random
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI(title="APEX 2.0 Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fetch LLM keys
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not api_key or api_key == "your_azure_openai_api_key_here":
    api_key = os.getenv("FOUNDRY_API_KEY")
    endpoint = os.getenv("FOUNDRY_ENDPOINT")

if api_key and endpoint:
    print(f"Loaded LLM Endpoint for live telemetry: {endpoint[:40]}...")

# Global state
active_websockets = []
agents = [
    {"id": '1', "name": 'ORCHESTRATOR', "status": 'IDLE', "task": 'AWAITING_ORCHESTRATION', "uptime": '12h 45m', "latency": '4ms', "thoughts": [{"time": int(time.time()*1000), "text": 'AWAITING INSTRUCTION...'}]},
    {"id": '2', "name": 'COST_ROUTER', "status": 'IDLE', "task": 'AWAITING_ORCHESTRATION', "uptime": '02h 12m', "latency": '2ms', "thoughts": [{"time": int(time.time()*1000), "text": 'MONITORING COST ALLOCATION'}]},
    {"id": '3', "name": 'QUERY_INTEL', "status": 'IDLE', "task": 'AWAITING_ORCHESTRATION', "uptime": '45h 11m', "latency": '3ms', "thoughts": [{"time": int(time.time()*1000), "text": 'AWAITING QUERIES'}]},
    {"id": '4', "name": 'WORKLOAD_VIS', "status": 'IDLE', "task": 'AWAITING_ORCHESTRATION', "uptime": '11h 05m', "latency": '5ms', "thoughts": [{"time": int(time.time()*1000), "text": 'SCANNING SYSTEM RESOURCES'}]},
]
alerts = [
    {"id": str(int(time.time())), "msg": 'BACKEND TELEMETRY SECURE AND ONLINE', "type": 'info'},
]
tick_counter = 0

async def broadcast_telemetry():
    global tick_counter, agents, alerts
    while True:
        await asyncio.sleep(2.0)
        
        if not active_websockets:
            continue
            
        tick_counter += 1

        # Occasionally run a "real" LLM call to simulate a heavy workload cycle
        azure_latency_ms = "N/A"
        if api_key and endpoint and random.random() > 0.7:
            agents[2]["status"] = "EXEC"
            agents[2]["task"] = "EVALUATING_LLM_LATENCY"
            agents[2]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": "DISPATCHING LIVE REQUEST TO AZURE OPENAI..."})
            
            start_time = time.time()
            try:
                model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "grok-4-1-fast-reasoning")
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        endpoint,
                        headers={
                            "api-key": api_key,
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model_name,
                            "messages": [{"role": "user", "content": "Return the single word 'OK'."}],
                            "max_tokens": 2
                        },
                        timeout=5.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    
                duration = int((time.time() - start_time) * 1000)
                azure_latency_ms = f"{duration}ms"
                agents[2]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": f"MODELS-AS-A-SERVICE RESPONDED '{content}' IN {duration}ms"})
            except Exception as e:
                agents[2]["status"] = "ERR_NODE"
                agents[2]["task"] = "API_CONNECTION_FAILED"
                agents[2]["latency"] = "ERR"
                error_msg = str(e)
                if hasattr(e, 'response') and e.response:
                    error_msg += f" {e.response.text[:50]}"
                agents[2]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": f"CRITICAL: {error_msg[:60]}..."})
                alerts.append({"id": str(int(time.time())), "msg": f'AZURE CONNECTION FAILED', "type": 'error'})
        else:
            # Revert query intel to idle
            agents[2]["status"] = "IDLE"
            agents[2]["task"] = "AWAITING_QUERIES"
            agents[2]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": "AWAITING QUERIES"})

        # Randomize the other agents slightly
        for i in [0, 1, 3]:
            if random.random() > 0.8:
                states = ['IDLE', 'EXEC']
                status = random.choice(states)
                agents[i]["status"] = status
                agents[i]["latency"] = f"{int(random.gauss(6, 2))}ms"
                if status == 'EXEC':
                    agents[i]["task"] = "PROCESSING_TELEMETRY"
                    agents[i]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": f"PROCESSING SYSTEM CYCLE {tick_counter}"})
                else:
                    agents[i]["task"] = "AWAITING_ORCHESTRATION"
                    agents[i]["thoughts"].insert(0, {"time": int(time.time()*1000), "text": "AWAITING ORCHESTRATION"})
                    
            # Keep thoughts bounded
            agents[i]["thoughts"] = agents[i]["thoughts"][:15]

        agents[2]["thoughts"] = agents[2]["thoughts"][:15]
        
        # Add random alerts
        if random.random() > 0.85:
            alerts.append({"id": str(int(time.time())), "msg": f'ROUTING OPTIMIZED [NODE_0{random.randint(1,9)}]', "type": 'info'})
        if len(alerts) > 10:
            alerts.pop(0)

        # Build chart data based on pseudo-random distribution around actual latency (to make the chart move)
        queries_data = []
        for i in range(6):
            base_gpt4 = 80 + int(random.gauss(0, 5))
            queries_data.append({
                "time": f"{tick_counter + i}s",
                "gpt4": base_gpt4 if azure_latency_ms == "N/A" else int(azure_latency_ms.replace('ms',''))/10, # Scale it down
                "sonnet": base_gpt4 - 20,
                "phi3_local": base_gpt4 - 40,
            })

        payload = {
            "tick": tick_counter,
            "agents": agents,
            "alerts": alerts,
            "queries": queries_data
        }
        
        # Broadcast to all connected clients
        disconnected = []
        for ws in active_websockets:
            try:
                await ws.send_json(payload)
            except Exception:
                disconnected.append(ws)
        
        for ws in disconnected:
            active_websockets.remove(ws)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_telemetry())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_websockets.remove(websocket)

@app.get("/")
async def root():
    return {"message": "APEX 2.0 API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
