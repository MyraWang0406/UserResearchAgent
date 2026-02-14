import uuid
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import os
import json

from ..core.engine import engine
from ..core.database import (
    init_db, save_trace, get_all_traces, 
    save_snapshot, save_evolution_log, get_latest_snapshot
)
from ..core.evermem_client import memory_os
from ..services.evolution_service import process_interview_to_initial_prd, evolve_requirements_by_metrics
from ..schemas.evolution import EvidenceCell, DecisionCell, RequirementCell

app = FastAPI(title="Research OS v1.2 - Decision Loop", version="1.2.1")

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
    return {"status": "healthy", "version": "1.2.1"}

# --- 企业决策援引闭环 API ---

@app.post("/api/v1/evidence")
async def create_evidence(payload: EvidenceCell, token: str = Depends(verify_token)):
    """创建证据卡片"""
    evidence_id = memory_os.commit_cell("Evidence", payload.dict(), tags={"type": "evidence", "domain": "enterprise"})
    save_trace({
        "trace_id": f"tr_{evidence_id}",
        "step_name": "create_evidence",
        "input_data": payload.dict(),
        "output_data": {"evidence_id": evidence_id},
        "status": "SUCCESS"
    })
    return {"evidence_id": evidence_id}

@app.get("/api/v1/evidence/search")
async def search_evidence(token: str = Depends(verify_token)):
    """搜索所有证据"""
    return memory_os.recall_by_tags({"type": "evidence"})

@app.get("/api/v1/trace_graph")
async def get_trace_graph(token: str = Depends(verify_token)):
    """
    返回溯源图谱 (Nodes/Edges)
    """
    cells = memory_os._mock_storage
    nodes = []
    edges = []
    for cell in cells:
        nodes.append({
            "id": cell['id'], 
            "label": cell['type'], 
            "content": json.loads(cell['content']).get('content', cell['type']),
            "timestamp": cell['timestamp']
        })
        for ref in cell.get('citations', []):
            edges.append({"source": ref, "target": cell['id']})
    return {"nodes": nodes, "edges": edges}

# --- 兼容旧有 MRE 流程 ---

@app.post("/api/v1/mre/intake")
async def mre_intake(payload: Dict[str, Any], token: str = Depends(verify_token)):
    interview_text = payload.get("interview_text", "")
    result = engine.execute_step("mre_intake", process_interview_to_initial_prd, interview_text)
    save_snapshot(result['data'])
    save_trace(result)
    return result

@app.post("/api/v1/mre/evolve")
async def mre_evolve(payload: Dict[str, Any], token: str = Depends(verify_token)):
    metrics = payload.get("metrics", {})
    current_snapshot = get_latest_snapshot()
    if not current_snapshot:
        raise HTTPException(status_code=400, detail="No existing snapshot found.")
    
    result = engine.execute_step("mre_evolve", evolve_requirements_by_metrics, current_snapshot, metrics)
    data = result['data']
    save_snapshot(data['new_snapshot'])
    for log in data['evolution_logs']:
        save_evolution_log(log)
    save_trace(result)
    return result

@app.get("/api/v1/traces")
async def list_traces(token: str = Depends(verify_token)):
    return get_all_traces()
