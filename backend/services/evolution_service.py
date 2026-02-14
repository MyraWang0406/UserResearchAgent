import uuid
from typing import Dict, Any, List
from ..core.evermem_client import memory_os

def process_interview_to_initial_prd(interview_text: str) -> Dict[str, Any]:
    """
    组织决策记忆链路：Evidence -> Decision -> Requirement
    """
    # 1. 提交 Context Cell (假设当前上下文)
    context_data = {
        "business_type": "B2B SaaS",
        "growth_mode": ["PLG"],
        "company_stage": "1-10",
        "leadership_style": "Data-Driven",
        "employee_needs": ["Efficiency"],
        "north_star_metric": "CVR"
    }
    tags = {"domain": "saas", "stage": "1-10", "growth": "PLG"}
    context_id = memory_os.commit_cell("Context", context_data, tags)

    # 2. 提交 Evidence Cell
    evidence_data = {
        "source_type": "Interview",
        "content": interview_text,
        "reliability_score": 0.9
    }
    evidence_id = memory_os.commit_cell("Evidence", evidence_data, tags)

    # 3. 提交 Decision Cell
    decision_data = {
        "topic": "Initial Feature Set",
        "logic": "基于访谈证据，确定核心功能为 AI 素材生成以提升转化。",
        "citations": [evidence_id]
    }
    decision_id = memory_os.commit_cell("Decision", decision_data, tags, citations=[evidence_id])

    # 4. 提交 Requirement Cell
    requirement_data = {
        "req_type": "Functional",
        "prd_format": "Markdown",
        "content": "# PRD v1.0\n1. AI 素材生成\n2. 一键投放",
        "value_score": 8.5,
        "cost_estimate": "2 weeks",
        "derived_from": [decision_id]
    }
    requirement_id = memory_os.commit_cell("Requirement", requirement_data, tags, citations=[decision_id])

    return {
        "version_id": requirement_id,
        "context_id": context_id,
        "evidence_id": evidence_id,
        "decision_id": decision_id,
        "prd_markdown": requirement_data['content'],
        "persona": {"name": "小微企业主"}, # 保持兼容
        "hypotheses": [{"id": "H1", "statement": "AI素材提升转化", "status": "PENDING"}]
    }

def evolve_requirements_by_metrics(current_snapshot: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    演化链路：Outcome -> Decision -> New Requirement
    """
    tags = {"domain": "saas", "stage": "1-10", "growth": "PLG"}
    
    # 1. 提交 Outcome Cell
    outcome_data = {
        "metrics_feedback": metrics,
        "impact_score": 0.4,
        "falsified_hypotheses": ["H1"] if metrics.get("cvr", 0) < 0.02 else [],
        "linked_requirement": current_snapshot['version_id']
    }
    outcome_id = memory_os.commit_cell("Outcome", outcome_data, tags)

    # 2. 提交演化 Decision Cell
    evo_decision_data = {
        "topic": "Requirement Pivot",
        "logic": f"由于指标未达标 ({metrics}), 决定调整 AI 素材生成逻辑。",
        "citations": [outcome_id]
    }
    evo_decision_id = memory_os.commit_cell("Decision", evo_decision_data, tags, citations=[outcome_id])

    # 3. 提交新 Requirement Cell
    new_requirement_data = {
        "req_type": "Functional",
        "prd_format": "Markdown",
        "content": "# PRD v2.0\n1. AI 素材生成 (增加人工审核)",
        "value_score": 9.0,
        "cost_estimate": "1 week",
        "derived_from": [evo_decision_id]
    }
    new_requirement_id = memory_os.commit_cell("Requirement", new_requirement_data, tags, citations=[evo_decision_id])

    return {
        "new_snapshot": {
            "version_id": new_requirement_id,
            "prd_markdown": new_requirement_data['content'],
            "persona": current_snapshot['persona'],
            "hypotheses": [{"id": "H1", "statement": "AI素材提升转化", "status": "FALSIFIED"}]
        },
        "evolution_logs": [{
            "version_id": new_requirement_id,
            "change_type": "EVOLVED",
            "reasoning": evo_decision_data['logic'],
            "evidence_metric": metrics
        }]
    }
