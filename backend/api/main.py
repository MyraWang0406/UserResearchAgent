import uuid
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import os

from ..core.engine import engine
from ..core.database import init_db, save_trace, get_all_traces, create_approval, update_approval, get_pending_approvals
from ..services.research_service import diagnose_with_growth_logic, generate_survey_v2
from ..services.bc_growth_service import run_bc_growth_research

app = FastAPI(title="Research OS API", version="1.1.0")

# 环境变量配置
API_KEY = os.getenv("API_KEY", "admin123")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

# 简单鉴权中间件
async def verify_token(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return x_api_key

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.1.0"}

@app.get("/ping")
async def ping(token: str = Depends(verify_token)):
    return {"message": "pong", "status": "authenticated"}

# --- 核心业务接口 ---
@app.post("/api/v1/bc_growth_research")
async def bc_growth_research(payload: Dict[str, Any], token: str = Depends(verify_token)):
    result = engine.execute_step("bc_growth_research", run_bc_growth_research, payload)
    save_trace(result)
    return result

@app.post("/api/v1/diagnose")
async def diagnose(payload: Dict[str, Any], token: str = Depends(verify_token)):
    result = engine.execute_step("diagnose", diagnose_with_growth_logic, payload)
    save_trace(result)
    return result

# --- Trace & HITL 接口 ---
@app.get("/api/v1/traces")
async def list_traces(token: str = Depends(verify_token)):
    return get_all_traces()

@app.get("/api/v1/approvals/pending")
async def list_pending_approvals(token: str = Depends(verify_token)):
    return get_pending_approvals()

@app.post("/api/v1/approve")
async def approve_action(approval_id: str, decision: str, comment: str = "", token: str = Depends(verify_token)):
    update_approval(approval_id, decision, "admin", comment)
    return {"status": "success", "approval_id": approval_id, "decision": decision}

# --- MCP HTTP 网关 ---
@app.get("/mcp/tools")
async def list_mcp_tools():
    return {
        "tools": [
            {"name": "bc_growth_research", "description": "执行 BC 双端有限规模增长研究", "input_schema": {"type": "object"}},
            {"name": "diagnose", "description": "执行 AI 业务诊断", "input_schema": {"type": "object"}}
        ]
    }

@app.post("/mcp/call")
async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any], token: str = Depends(verify_token)):
    if tool_name == "bc_growth_research":
        return await bc_growth_research(arguments, token)
    elif tool_name == "diagnose":
        return await diagnose(arguments, token)
    else:
        raise HTTPException(status_code=404, detail="Tool not found")
