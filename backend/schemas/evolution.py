from __future__ import annotations
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
    business_type: str
    growth_mode: List[str]
    company_stage: str
    leadership_style: str
    employee_needs: List[str]
    north_star_metric: str

class EvidenceCell(BaseModel):
    source_type: str # Interview, Metrics, Market_Research
    content: str
    raw_data: Optional[Dict[str, Any]] = None
    reliability_score: float = 1.0

class DecisionCell(BaseModel):
    topic: str
    logic: str
    trade_off: Optional[str] = None
    citations: List[str] = [] # List of Evidence Cell IDs
    status: str = "APPROVED"

class RequirementCell(BaseModel):
    req_type: str # Functional, UX, Technical
    prd_format: str # User Story, Gherkin, Markdown
    content: str
    value_score: float
    cost_estimate: str
    derived_from: List[str] = [] # List of Decision/Evidence Cell IDs

class OutcomeCell(BaseModel):
    metrics_feedback: Dict[str, Any]
    impact_score: float
    falsified_hypotheses: List[str] = []
    linked_requirement: str # Requirement Cell ID

class MemoryCell(BaseModel):
    id: str
    type: CellType
    data: Dict[str, Any]
    tags: List[str]
    timestamp: str
