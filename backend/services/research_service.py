from typing import Dict, Any, List
from ..schemas.models import GrowthMode

def diagnose_with_growth_logic(inp: Dict[str, Any]) -> Dict[str, Any]:
    drivers = inp.get("growth_driver", [])
    industry = inp.get("industry", "")
    
    # 核心逻辑：区分 B 端采购者与 C 端使用者
    is_b2b = any(mode in drivers for mode in [GrowthMode.SLG, GrowthMode.PLG])
    
    analysis = {
        "focus": "B端首单转化" if "首单" in inp.get("target_goal", "") else "全链路优化",
        "segments": []
    }
    
    if is_b2b:
        analysis["segments"] = [
            {"role": "Economic Buyer", "focus": "ROI, 合规性, 案例证明"},
            {"role": "End User", "focus": "易用性, 效率提升, 爽感"}
        ]
    else:
        analysis["segments"] = [{"role": "Consumer", "focus": "情绪价值, 价格锚点, 社交证明"}]
        
    # 适配增长模式
    if GrowthMode.PLG in drivers:
        analysis["strategy"] = "侧重产品内激活与 Aha Moment 挖掘"
    elif GrowthMode.SLG in drivers:
        analysis["strategy"] = "侧重销售异议处理与证据包构建"
        
    return analysis

def generate_survey_v2(inp: Dict[str, Any]) -> Dict[str, Any]:
    # 模拟更高级的问卷生成逻辑
    return {
        "questions": [
            {"q": "在决定购买前，您最担心的三个风险是？", "type": "rank"},
            {"q": "如果您现在不解决这个问题，三个月后的代价是？", "type": "text"}
        ],
        "quality_score": 0.95
    }
