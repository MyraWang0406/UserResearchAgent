import uuid
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import os

from ..core.engine import engine
from ..core.database import (
    init_db, save_trace, get_all_traces, 
    save_snapshot, save_evolution_log, get_latest_snapshot
)
from ..services.evolution_service import process_interview_to_initial_prd, evolve_requirements_by_metrics

app = FastAPI(title="MRE MVP API", version="1.2.0")

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

async def verify_token(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

@app.get("/health")
def health():
    return {"status": "healthy", "mre_version": "1.2.0"}

# --- MRE MVP 核心接口 ---

@app.post("/api/v1/mre/intake")
async def mre_intake(payload: Dict[str, Any], token: str = Depends(verify_token)):
    """
    输入访谈文本，生成初始 Snapshot
    """
    interview_text = payload.get("interview_text", "")
    result = engine.execute_step("mre_intake", process_interview_to_initial_prd, interview_text)
    
    # 持久化 Snapshot
    save_snapshot(result['data'])
    save_trace(result)
    return result

@app.post("/api/v1/mre/evolve")
async def mre_evolve(payload: Dict[str, Any], token: str = Depends(verify_token)):
    """
    输入指标数据，演化需求
    """
    metrics = payload.get("metrics", {})
    current_snapshot = get_latest_snapshot()
    if not current_snapshot:
        raise HTTPException(status_code=400, detail="No existing snapshot found. Run intake first.")
    
    result = engine.execute_step("mre_evolve", evolve_requirements_by_metrics, current_snapshot, metrics)
    
    # 持久化新的 Snapshot 和演化日志
    data = result['data']
    save_snapshot(data['new_snapshot'])
    for log in data['evolution_logs']:
        save_evolution_log(log)
    
    save_trace(result)
    return result

@app.get("/api/v1/mre/latest")
async def get_latest(token: str = Depends(verify_token)):
    return get_latest_snapshot()

@app.get("/api/v1/traces")
async def list_traces(token: str = Depends(verify_token)):
    return get_all_traces()
