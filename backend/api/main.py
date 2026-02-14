import uuid
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime

from ..core.database import init_db, save_trace, get_all_traces
from ..core.evermem_client import memory_os
from ..schemas.memory_cells import EvidenceCell, DecisionCell, RequirementCell, CellType

app = FastAPI(title="Decision Memory MVP", version="1.3.0")

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
    return {"status": "healthy", "track": "Memory Genesis Track 1"}

# --- Decision Memory MVP API ---

@app.post("/api/v1/evidence")
async def create_evidence(payload: EvidenceCell, token: str = Depends(verify_token)):
    """创建证据卡片"""
    evidence_id = memory_os.commit_cell("Evidence", payload.dict(), tags={"type": "evidence"})
    return {"evidence_id": evidence_id}

@app.get("/api/v1/evidence/search")
async def search_evidence(q: str = "", tags: str = "", token: str = Depends(verify_token)):
    """搜索证据"""
    query_tags = {"type": "evidence"}
    if tags:
        for t in tags.split(","):
            k, v = t.split(":")
            query_tags[k] = v
    return memory_os.recall_by_tags(query_tags)

@app.post("/api/v1/decision")
async def create_decision(payload: DecisionCell, token: str = Depends(verify_token)):
    """创建决策：强制援引校验"""
    if not payload.citations:
        raise HTTPException(status_code=400, detail="Decision must cite at least one evidence.")
    
    decision_id = memory_os.commit_cell("Decision", payload.dict(), tags={"type": "decision"}, citations=payload.citations)
    save_trace({
        "trace_id": f"tr_{decision_id}",
        "step_name": "decision_making",
        "input_data": payload.dict(),
        "output_data": {"decision_id": decision_id},
        "status": "SUCCESS"
    })
    return {"decision_id": decision_id}

@app.post("/api/v1/requirement/version")
async def create_requirement(payload: RequirementCell, token: str = Depends(verify_token)):
    """创建需求版本：必须绑定决策/证据"""
    if not payload.derived_from:
        raise HTTPException(status_code=400, detail="Requirement must be derived from a decision or evidence.")
    
    req_id = memory_os.commit_cell("Requirement", payload.dict(), tags={"type": "requirement"}, citations=payload.derived_from)
    save_trace({
        "trace_id": f"tr_{req_id}",
        "step_name": "requirement_generation",
        "input_data": payload.dict(),
        "output_data": {"requirement_id": req_id},
        "status": "SUCCESS"
    })
    return {"requirement_id": req_id}

@app.get("/api/v1/trace_graph")
async def get_trace_graph(topic: str = "", stage: str = "", token: str = Depends(verify_token)):
    """
    返回溯源图谱 (Nodes/Edges)
    """
    cells = memory_os._mock_storage
    nodes = []
    edges = []
    for cell in cells:
        # 简单的过滤逻辑
        if topic and topic not in cell['tags']: continue
        
        nodes.append({
            "id": cell['id'], 
            "label": cell['type'], 
            "summary": json.loads(cell['content']).get('summary', cell['type']),
            "timestamp": cell['timestamp']
        })
        # 建立引用边
        for ref in cell.get('citations', []):
            edges.append({"source": ref, "target": cell['id'], "type": "cites"})
            
    return {"nodes": nodes, "edges": edges}

@app.get("/api/v1/traces")
async def list_traces(token: str = Depends(verify_token)):
    return get_all_traces()
