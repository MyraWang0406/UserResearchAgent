from typing import Dict, Any, List
import uuid

def run_bc_growth_research(inp: Dict[str, Any]) -> Dict[str, Any]:
    """
    BC 双端「有限规模增长」主工作流
    """
    # 1. Solution Intake 字段解析
    company_stage = inp.get("company_stage", "小微创新")
    biz_stage = inp.get("biz_stage", "0-1")
    growth_modes = inp.get("growth_modes", ["产品驱动"])
    north_star = inp.get("north_star", "用户规模增长")
    core_bottleneck = inp.get("core_bottleneck", "转化率低")
    
    # 2. 有限规模增长逻辑分流
    research_strategy = ""
    if biz_stage == "0-1":
        research_strategy = "强痛点定性：挖掘核心不买理由"
    elif biz_stage == "1-10":
        research_strategy = "成交 vs 流失：对比关键行为差异"
    elif biz_stage == "10-100":
        research_strategy = "分层抽样：验证不同渠道转化效率"
    else:
        research_strategy = "成熟效率优化：漏斗微调与心智巩固"

    # 3. 生成 5 件套产物 (Mock 逻辑，绑定 Evidence)
    evidence_id = f"ev_{str(uuid.uuid4())[:6]}"
    
    products = {
        "growth_problem_tree": {
            "problem": core_bottleneck,
            "hypothesis": f"由于{core_bottleneck}，导致{north_star}受阻",
            "evidence": f"[{evidence_id}] 漏斗数据显示关键节点折损率 > 60%",
            "suggestion": "优化落地页价值主张，增加社交证明"
        },
        "research_kit": {
            "survey_q": ["您最担心的风险是？", "如果不解决此问题，您的代价是？"],
            "interview_guide": "追问：最后一秒犹豫的真实原因",
            "quota": "有效样本 n=50"
        },
        "insight_cards": [
            {
                "title": "信任度是核心卡点",
                "content": "用户对新品牌存在天然防御心理",
                "evidence": f"[{evidence_id}] 访谈中 80% 用户提到‘没听过这个牌子’",
                "score": {"trust": 3, "motivation": 7}
            }
        ],
        "growth_roadmap": [
            {"phase": "P0", "action": "增加客户案例与背书", "metric_threshold": "CVR > 2.5%"},
            {"phase": "P1", "action": "优化价格锚点", "metric_threshold": "ARPU > $15"}
        ],
        "management_report": {
            "summary": f"当前处于{biz_stage}阶段，应优先解决{core_bottleneck}以实现有限规模增长。",
            "status": "DRAFT_PENDING_APPROVAL"
        }
    }
    
    return {
        "strategy": research_strategy,
        "products": products,
        "trace_status": "COMPLETED",
        "can_publish": False # 必须经过审批
    }
