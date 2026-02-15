from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import os

from ..core.database import init_db, get_all_traces
from ..core.evermem_client import memory_os
from ..schemas.memory_cells import EvidenceCell, DecisionCell, RequirementCell

app = FastAPI(title="Decision Memory MVP", version="1.3.1")

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
    return {"status": "healthy", "track": "Memory Genesis Track 1", "mode": "MOCK" if memory_os.is_mock else "REAL"}

@app.post("/api/v1/evidence")
async def create_evidence(payload: EvidenceCell, token: str = Depends(verify_token)):
    data = payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict()
    evidence_id = memory_os.commit_cell("Evidence", data, tags={"type": "evidence", "domain": "enterprise"})
    return {"evidence_id": evidence_id}

@app.get("/api/v1/evidence/search")
async def search_evidence(tags: str = "", token: str = Depends(verify_token)):
    query_tags = {"type": "evidence"}
    if tags:
        for t in tags.split(","):
            if ":" in t:
                k, v = t.split(":", 1)
                query_tags[k] = v
    return memory_os.recall_by_tags(query_tags)

@app.post("/api/v1/decision")
async def create_decision(payload: DecisionCell, token: str = Depends(verify_token)):
    if not payload.citations or len(payload.citations) == 0:
        raise HTTPException(status_code=400, detail="Decision must cite at least one evidence.")
    data = payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict()
    decision_id = memory_os.commit_cell("Decision", data, tags={"type": "decision"}, citations=payload.citations)
    return {"decision_id": decision_id}

@app.post("/api/v1/requirement/version")
async def create_requirement(payload: RequirementCell, token: str = Depends(verify_token)):
    if not payload.derived_from or len(payload.derived_from) == 0:
        raise HTTPException(status_code=400, detail="Requirement must be derived from a decision or evidence.")
    data = payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict()
    req_id = memory_os.commit_cell("Requirement", data, tags={"type": "requirement"}, citations=payload.derived_from)
    return {"requirement_id": req_id}

@app.get("/api/v1/trace_graph")
async def get_trace_graph(token: str = Depends(verify_token)):
    all_types = ["evidence", "decision", "requirement", "outcome"]
    nodes = []
    edges = []
    for t in all_types:
        cells = memory_os.recall_by_tags({"type": t})
        for cell in cells:
            nodes.append({
                "id": cell['id'],
                "label": cell['type'],
                "summary": cell['data'].get('summary', cell['data'].get('rationale', cell['type'])),
                "timestamp": cell['timestamp']
            })
            for ref in cell.get('citations', []):
                edges.append({"source": ref, "target": cell['id'], "type": "cites"})
    return {"nodes": nodes, "edges": edges}

@app.get("/api/v1/traces")
async def list_traces(token: str = Depends(verify_token)):
    return get_all_traces()
