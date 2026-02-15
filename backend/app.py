
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .logic import (
    diagnose_client, build_research_plan,
    generate_b2b_discovery_questions,
    generate_qual_interview_guide,
    generate_quant_survey,
    sql_metric_templates
)

app = FastAPI(title="User Research Agent (Conversion OS)", version="0.2.0")

class DiagnoseIn(BaseModel):
    industry: str = Field(..., description="行业，如美妆/营养保健品/SaaS等")
    market: str = Field(..., description="目标市场，如北美/欧洲/东南亚/国内等")
    company_stage: str = Field(..., description="公司阶段")
    growth_driver: List[str] = Field(..., description="增长驱动方式（可多选）")
    biz_positioning: str = Field(..., description="本次服务业务在公司内部定位")
    core_problem: str = Field(..., description="核心问题描述（尽量包含事实/数据）")
    funnel_hint: Optional[Dict[str, Any]] = Field(default=None, description="可选：漏斗指标提示（任意结构）")
    constraints: Optional[str] = Field(default=None, description="约束：合规/预算/周期等")
    target_goal: str = Field(..., description="本次目标（首单转化/复购/退款率/线索等）")

class PlanIn(BaseModel):
    diagnose: Dict[str, Any]
    timeline: str = Field(default="2-4周", description="期望交付周期")
    budget_level: str = Field(default="中", description="预算档位：低/中/高")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/diagnose")
def api_diagnose(payload: DiagnoseIn):
    return diagnose_client(payload.model_dump())

@app.post("/api/research_plan")
def api_plan(payload: PlanIn):
    return build_research_plan(payload.diagnose, timeline=payload.timeline, budget_level=payload.budget_level)

@app.post("/api/b2b_questions")
def api_b2b_questions(payload: DiagnoseIn):
    return {"questions": generate_b2b_discovery_questions(payload.model_dump())}

@app.post("/api/qual_guide")
def api_qual_guide(payload: DiagnoseIn):
    return {"qual_guide": generate_qual_interview_guide(payload.model_dump())}

@app.post("/api/quant_survey")
def api_quant(payload: DiagnoseIn):
    return {"quant_survey": generate_quant_survey(payload.model_dump())}

@app.get("/api/sql_templates")
def api_sql_templates():
    return {"templates": sql_metric_templates()}
