from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class CellType(str, Enum):
    CONTEXT = "Context"
    EVIDENCE = "Evidence"
    DECISION = "Decision"
    REQUIREMENT = "Requirement"
    OUTCOME = "Outcome"

class EvidenceCell(BaseModel):
    source_type: str
    summary: str
    atomic_claims: List[str] = Field(default_factory=list)
    snippets: List[str] = Field(default_factory=list)
    confidence: float = 1.0

class DecisionCell(BaseModel):
    decision_type: str
    rationale: str
    citations: List[str] = Field(default_factory=list, description="必须援引至少一个证据 ID")
    tradeoffs: Optional[str] = None
    timestamp: Optional[str] = None

class RequirementCell(BaseModel):
    req_type: str
    version: str
    scope_summary: str
    derived_from: List[str] = Field(default_factory=list, description="必须绑定决策或证据 ID")
    cost_summary: str = ""
    priority_score: float = 1.0
