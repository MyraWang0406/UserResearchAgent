from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class GrowthMode(str, Enum):
    PLG = "PLG"  # Product-Led
    SLG = "SLG"  # Sales-Led
    MLG = "MLG"  # Marketing-Led
    OLG = "OLG"  # Operations-Led
    TLG = "TLG"  # Tech-Led

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    PUBLISHER = "PUBLISHER"
    SUGGESTER = "SUGGESTER"
    READONLY = "READONLY"

class TraceStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    UNCERTAIN = "UNCERTAIN"
    DEGRADED = "DEGRADED"

class ResearchProject(BaseModel):
    id: str
    title: str
    industry: str
    market: str
    growth_mode: List[GrowthMode]
    target_goal: str
    created_at: datetime = Field(default_factory=datetime.now)

class Persona(BaseModel):
    id: str
    project_id: str
    name: str
    role_type: str  # e.g., "Economic Buyer", "End User", "IT Decision Maker"
    pain_points: List[str]
    motivation_bucket: str

class Hypothesis(BaseModel):
    id: str
    project_id: str
    statement: str
    evidence_ids: List[str] = []
    confidence: float = 0.0
    status: str = "PENDING"  # PENDING, VALIDATED, REJECTED

class TraceLog(BaseModel):
    trace_id: str
    step_name: str
    input_data: Dict[str, Any]
    tool_calls: List[Dict[str, Any]] = []
    output_data: Dict[str, Any]
    score: float = 1.0
    status: TraceStatus = TraceStatus.SUCCESS
    error_msg: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class HITLRequest(BaseModel):
    id: str
    action_type: str  # e.g., "PUBLISH_SURVEY", "OVERRIDE_CONCLUSION"
    payload: Dict[str, Any]
    requester_id: str
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    approver_id: Optional[str] = None
    comment: Optional[str] = None
