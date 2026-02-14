import uuid
from typing import Dict, Any, List

def process_interview_to_initial_prd(interview_text: str) -> Dict[str, Any]:
    """
    MVP 功能 1 & 2: 输入访谈文本，生成画像、假设和初始 PRD
    """
    # 模拟 Agent 提取逻辑
    version_id = f"v1_{str(uuid.uuid4())[:6]}"
    
    persona = {
        "name": "小微企业主",
        "pain_points": ["获客成本高", "缺乏专业营销知识"],
        "goals": ["低成本获取精准线索"]
    }
    
    hypotheses = [
        {"id": "H1", "statement": "如果提供 AI 自动生成素材功能，那么转化率会提升 20%，因为解决了素材生产门槛。", "status": "PENDING"},
        {"id": "H2", "statement": "如果集成一键投放功能，那么留存会提升，因为简化了操作链路。", "status": "PENDING"}
    ]
    
    prd_md = f"""# PRD v1.0 - AI 营销助手
## 核心功能
1. **AI 素材生成**: 支持文字转图片。
2. **一键投放**: 对接主流广告平台。
## 优先级
- P0: 素材生成
- P1: 一键投放
"""
    
    return {
        "version_id": version_id,
        "persona": persona,
        "hypotheses": hypotheses,
        "prd_markdown": prd_md,
        "iteration_count": 1
    }

def evolve_requirements_by_metrics(current_snapshot: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    MVP 功能 4 & 5: 输入指标数据，自动判断假设证伪并调整需求
    """
    parent_version = current_snapshot['version_id']
    new_version_id = f"v2_{str(uuid.uuid4())[:6]}"
    
    # 模拟 Agent 分析逻辑
    # 假设指标显示 CVR 极低
    cvr = metrics.get("cvr", 0)
    evolution_logs = []
    new_hypotheses = [h.copy() for h in current_snapshot['hypotheses']]
    
    if cvr < 0.02: # 证伪 H1
        for h in new_hypotheses:
            if h['id'] == "H1":
                h['status'] = "FALSIFIED"
                evolution_logs.append({
                    "version_id": new_version_id,
                    "change_type": "FALSIFIED",
                    "target_requirement": "AI 素材生成",
                    "reasoning": f"指标 CVR={cvr*100}% 低于预期，证伪了‘AI素材能直接提升转化’的假设。",
                    "evidence_metric": metrics
                })
    
    # 调整 PRD
    new_prd_md = current_snapshot['prd_markdown'].replace(
        "1. **AI 素材生成**: 支持文字转图片。",
        "1. **AI 素材生成 (已调整)**: 增加人工审核环节，确保素材质量。"
    )
    
    new_snapshot = {
        "version_id": new_version_id,
        "parent_version_id": parent_version,
        "persona": current_snapshot['persona'],
        "hypotheses": new_hypotheses,
        "prd_markdown": new_prd_md,
        "iteration_count": current_snapshot['iteration_count'] + 1
    }
    
    return {
        "new_snapshot": new_snapshot,
        "evolution_logs": evolution_logs
    }
