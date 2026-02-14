from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class CellType(str, Enum):
    CONTEXT = "Context"
    EVIDENCE = "Evidence"
    DECISION = "Decision"
    REQUIREMENT = "Requirement"
    OUTCOME = "Outcome"

class ContextCell(BaseModel):
    biz_type: str
    stage: str
    growth_mode: str
    org_game_flags: List[str]
    resourcing_summary: str

class EvidenceCell(BaseModel):
    source_type: str
    summary: str
    atomic_claims: List[str]
    snippets: List[str]
    confidence: float = 1.0

class DecisionCell(BaseModel):
    decision_type: str
    rationale: str
    citations: List[str] = Field(..., min_items=1) # 强制援引
    tradeoffs: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: "")

class RequirementCell(BaseModel):
    req_type: str
    version: str
    scope_summary: str
    derived_from: List[str] = Field(..., min_items=1) # 必须绑定决策/证据
    cost_summary: str
    priority_score: float

class OutcomeCell(BaseModel):
    metrics_delta: Dict[str, Any]
    verdict: str # SUPPORT / FALSIFY
    links: List[str] # Requirement IDs
    timestamp: str
