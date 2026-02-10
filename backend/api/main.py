from fastapi import FastAPI, HTTPException, Depends
from ..schemas.models import UserRole, HITLRequest
from ..core.engine import engine
from ..services.research_service import diagnose_with_growth_logic, generate_survey_v2
from typing import Dict, Any

app = FastAPI(title="Research OS", version="1.0.0")

# 模拟权限检查
def check_permission(role: UserRole):
    if role == UserRole.READONLY:
        raise HTTPException(status_code=403, detail="Permission denied")

@app.post("/api/v1/diagnose")
async def diagnose(payload: Dict[str, Any]):
    return engine.execute_step("diagnose", diagnose_with_growth_logic, payload)

@app.post("/api/v1/survey/generate")
async def create_survey(payload: Dict[str, Any], role: UserRole = UserRole.PUBLISHER):
    # HITL 门禁示例
    if payload.get("require_approval"):
        return {"status": "PENDING_APPROVAL", "request_id": "hitl_123"}
    
    return engine.execute_step("generate_survey", generate_survey_v2, payload)

@app.get("/api/v1/traces")
async def get_traces():
    return engine.traces
