
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import re

# ---------- helpers ----------
def _norm(s: str) -> str:
    return (s or "").strip()

def _contains_any(s: str, keywords: List[str]) -> bool:
    s=_norm(s)
    return any(k in s for k in keywords)

# ---------- diagnosis ----------
def diagnose_client(inp: Dict[str, Any]) -> Dict[str, Any]:
    """
    规则化诊断：阶段/增长驱动/业务定位/问题类型/紧急度/建议研究策略。
    注意：这里先用可解释规则，便于你后续替换成模型或更复杂的打分器。
    """
    stage = _norm(inp.get("company_stage",""))
    drivers = inp.get("growth_driver",[]) or []
    positioning = _norm(inp.get("biz_positioning",""))
    problem = _norm(inp.get("core_problem",""))
    goal = _norm(inp.get("target_goal",""))
    constraints = _norm(inp.get("constraints",""))

    # 问题类型粗分
    problem_types = []
    if _contains_any(problem, ["转化", "CVR", "加购", "弃购", "漏斗", "下单", "支付"]):
        problem_types.append("漏斗转化折损")
    if _contains_any(problem, ["品牌", "信任", "公信", "口碑", "声誉", "安全", "合规"]):
        problem_types.append("信任与风险")
    if _contains_any(problem, ["价格", "贵", "不值", "促销", "折扣", "性价比"]):
        problem_types.append("价格与价值锚点")
    if _contains_any(problem, ["复购", "留存", "退款", "退货", "满意度", "售后"]):
        problem_types.append("复购与履约体验")
    if _contains_any(problem, ["内容", "素材", "文案", "卖点", "表达", "种草"]):
        problem_types.append("表达与说服力")
    if not problem_types:
        problem_types = ["问题类型待澄清（建议补充漏斗数据或典型案例）"]

    # 紧急度粗估（可解释）
    urgent = "中"
    if _contains_any(problem, ["暴跌", "大幅", "腰斩", "连续", "极低", "投放烧钱"]):
        urgent = "高"
    if _contains_any(constraints, ["尽快", "两周", "本月", "马上"]):
        urgent = "高"
    if _contains_any(goal, ["首单", "获客", "线索", "转化"]):
        urgent = "中-高"

    # 可控性（能否通过研究+表达/产品改动影响）
    controllable = "中"
    if _contains_any(problem, ["供应链", "缺货", "交付", "物流", "监管"]):
        controllable = "低-中"
    if _contains_any(problem, ["落地页", "详情页", "素材", "文案", "卖点"]):
        controllable = "高"

    # 推荐研究组合（先快后深 / 先漏斗再研究）
    research_route = []
    if "漏斗转化折损" in problem_types:
        research_route.append("先做漏斗诊断（用企业现有数据定位折损段）")
    research_route.append("定性深访：优先访谈“差点买但没买/弃购/退货/未复购”人群，获取‘最后一秒犹豫’证据")
    if stage.startswith("0-1") or stage.startswith("1-10"):
        research_route.append("定量快测：小样本验证卖点/阻力排序（用于快速迭代表达与定价锚点）")
    else:
        research_route.append("定量分层：按渠道/国家/新老用户分层验证差异（用于规模化转化提升）")

    # 交付物偏向（按增长驱动）
    deliver_focus = []
    d = " ".join(drivers)
    if "Marketing" in d or "MLG" in d or "营销" in d:
        deliver_focus += ["卖点与证据排序（用于素材/落地页）","落地页信息结构建议","素材脚本与FAQ"]
    if "Product" in d or "PLG" in d or "产品" in d:
        deliver_focus += ["激活/试用关键路径阻力","核心价值达成的最短路径建议"]
    if "Sales" in d or "SLG" in d or "销售" in d:
        deliver_focus += ["异议库与证据包（按角色：经济买方/使用者/IT/采购）","Demo/POC话术与材料清单"]
    if not deliver_focus:
        deliver_focus = ["卖点与阻力地图","可验证的实验清单"]

    # 去重保序
    deliver_focus = list(dict.fromkeys(deliver_focus))

    return {
        "stage": stage,
        "growth_driver": drivers,
        "biz_positioning": positioning,
        "goal": goal,
        "problem_types": problem_types,
        "urgency": urgent,
        "controllability": controllable,
        "recommended_route": research_route,
        "deliverable_focus": deliver_focus,
        "notes": "本诊断使用可解释规则生成，后续可在不改变接口的情况下替换为更复杂的打分/模型。"
    }

# ---------- plan builder ----------
def build_research_plan(diagnose: Dict[str, Any], timeline: str="2-4周", budget_level: str="中") -> Dict[str, Any]:
    stage = diagnose.get("stage","")
    problem_types = diagnose.get("problem_types",[])
    goal = diagnose.get("goal","")

    # 样本建议（旗舰版默认）
    if str(stage).startswith("0-1") or str(stage).startswith("1-10"):
        qual_n = "12-18（2-3个分层，每层约6人）"
        quant_n = "80-200（快测验证）" if budget_level != "低" else "50-120（快测验证）"
    elif str(stage).startswith("10-100"):
        qual_n = "15-24（按漏斗节点抽样：弃购/支付失败/退款/复购）"
        quant_n = "200-800（按渠道/国家/新老用户分层）"
    else:
        qual_n = "18-30（分层更细：高价值/流失/竞品迁移）"
        quant_n = "500+（代表性/分层验证，预算高时）" if budget_level == "高" else "300-600（分层验证）"

    metrics = suggest_metrics(goal, problem_types)

    return {
        "timeline": timeline,
        "qualitative": {
            "recommended_n": qual_n,
            "format": "40-45分钟半结构化深访（可真人主持+AI辅助，或AI主持）",
            "who_first": [
                "差点买但没买（弃购/未转化）",
                "首购后未复购",
                "退款/退货用户（如适用）",
                "高价值复购用户（用于对照）"
            ],
            "quality_bar": [
                "每条洞察必须绑定具体情境与证据片段（可回放）",
                "必须覆盖：触发事件→替代方案→评估路径→最后一秒犹豫→买单条件"
            ]
        },
        "quantitative": {
            "recommended_n": quant_n,
            "format": "在线问卷（支持跳题/配额/多语言）",
            "question_modules": [
                "价值点排序（建议迫选：MaxDiff 或同等迫选设计）",
                "阻力与风险排序（价格/信任/履约/替代/选择困难）",
                "证据偏好（你信什么：评价/成分/案例/保障）",
                "价格敏感（愿付费区间）",
                "人群分层变量（渠道/国家/是否新客/是否复购）"
            ],
            "data_quality": [
                "耗时异常、直线作答、矛盾检测、开放题空洞→自动剔除或降权",
                "关键题同义复核（减少迎合噪声）"
            ]
        },
        "deliverables": diagnose.get("deliverable_focus",[]) + [
            "转化阻力地图（可控/不可控拆解）",
            "可直接上线的转化资产：落地页结构+素材脚本+FAQ/异议处理",
            "验证口径与A/B实验清单（指标、分组、周期）"
        ],
        "validation_metrics": metrics,
        "risk_controls": [
            "所有结论必须有证据链（定性引用/定量分布/数据口径）",
            "输出必须可行动+可验证（否则不输出）",
            "Text2SQL/数据查询只允许白名单指标与只读SQL（SELECT）"
        ]
    }

def suggest_metrics(goal: str, problem_types: List[str]) -> List[Dict[str,str]]:
    goal=_norm(goal)
    mets=[]
    if "首单" in goal or "转化" in goal or "获客" in goal:
        mets += [
            {"metric":"购买转化率（CVR）","definition":"购买/访问（或订单/会话）","note":"统一分母口径"},
            {"metric":"加购率（ATC rate）","definition":"加购/访问","note":""},
            {"metric":"发起结账率（Checkout rate）","definition":"发起结账/加购","note":""}
        ]
    if "复购" in goal or "留存" in goal:
        mets += [
            {"metric":"30/60/90天复购率","definition":"窗口期复购用户/首购用户","note":"按首购cohort分组"},
            {"metric":"复购间隔","definition":"复购日期-首购日期","note":""}
        ]
    if "退款" in goal or "退货" in goal or "履约" in " ".join(problem_types):
        mets += [{"metric":"退款率/退货率","definition":"退款（退货）订单/支付订单","note":"需区分原因"}]
    if not mets:
        mets = [{"metric":"关键业务指标","definition":"由客户定义","note":"建议绑定漏斗节点"}]
    # 去重
    seen=set()
    out=[]
    for m in mets:
        k=m["metric"]
        if k not in seen:
            out.append(m); seen.add(k)
    return out

# ---------- generators ----------
def generate_b2b_discovery_questions(inp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成售前“问什么”的问题清单（给销售/售前）。
    """
    stage=_norm(inp.get("company_stage",""))
    drivers=inp.get("growth_driver",[]) or []
    goal=_norm(inp.get("target_goal",""))
    industry=_norm(inp.get("industry",""))
    questions=[
        {"section":"公司阶段与目标","q":"公司当前阶段是什么？（0-1/1-10/10-100/成熟/探索创新）","type":"single"},
        {"section":"公司阶段与目标","q":f"本次项目要提升的核心指标是什么？（例如：{goal}）","type":"text"},
        {"section":"增长驱动","q":"当前主导的增长方式是什么？请按主次排序。","type":"multi","options":drivers or [
            "产品驱动增长（Product-Led Growth, PLG）",
            "销售驱动增长（Sales-Led Growth, SLG）",
            "营销驱动增长（Marketing-Led Growth, MLG）",
            "运营驱动增长（Operations-Led Growth, OLG）",
            "技术驱动增长（Tech-Led Growth, TLG）"
        ]},
        {"section":"业务定位","q":"本次服务对应哪条业务线？在公司内部属于新孵化/规模化/成熟优化/探索创新？","type":"text"},
        {"section":"问题定义","q":"用数据或事实描述当前最痛的问题（含典型案例）。","type":"text"},
        {"section":"漏斗与证据","q":"漏斗各环节目前大概水平/趋势？最大折损发生在哪一段？","type":"text"},
        {"section":"约束","q":"合规/隐私/品牌调性/时间/预算有哪些硬约束？","type":"text"},
        {"section":"成功标准","q":"如果两周/一个月后要证明有效，你希望看到什么变化？","type":"text"}
    ]
    if industry:
        questions.append({"section":"行业特性","q":f"{industry}行业里，用户做决策最看重哪些证据？（评价/专家/成分/案例/保障/售后）","type":"text"})
    return questions

def generate_qual_interview_guide(inp: Dict[str, Any]) -> Dict[str, Any]:
    goal=_norm(inp.get("target_goal",""))
    problem=_norm(inp.get("core_problem",""))
    return {
        "duration_minutes": 45,
        "principles": [
            "追到具体事件：时间、场景、对比对象、代价",
            "用‘为什么/为什么现在/如果不…会怎样’穿透套话",
            "所有洞察必须落到：可行动的改动点 + 可验证指标"
        ],
        "sections":[
            {"t":"0-5min 破冰与背景","prompts":[
                "你简单介绍下自己/使用场景？",
                "最近一次产生相关需求/想购买的触发事件是什么？"
            ]},
            {"t":"5-15min 现有替代方案","prompts":[
                "现在你是怎么解决的？（替代/竞品/人工/拖着不做）",
                "这样做的成本是什么？（时间/钱/风险/麻烦）"
            ]},
            {"t":"15-30min 评估路径（证据链）","prompts":[
                "你评估时看了哪些信息？先看什么后看什么？",
                "哪些证据最让你信？哪些让你不信？为什么？",
                "在这个过程中你什么时候开始犹豫？"
            ]},
            {"t":"30-40min 最后一秒犹豫探针（核心）","prompts":[
                "如果你‘差点’就买了，最后没买的那一刻发生了什么？",
                "表面原因之外，最真实的顾虑是什么？（价格/信任/麻烦/风险/不确定）",
                "如果给你一个条件/承诺/证据，你会当场买单吗？是什么？"
            ]},
            {"t":"40-45min 购买条件与改动建议","prompts":[
                f"站在{goal}目标上，你觉得我们最应该先改哪一件事？为什么？",
                "如果只允许改3点（页面/文案/证据/流程/售后），你会选什么？"
            ]}
        ],
        "context": {
            "goal": goal,
            "problem_hint": problem
        }
    }

def generate_quant_survey(inp: Dict[str, Any]) -> Dict[str, Any]:
    goal=_norm(inp.get("target_goal",""))
    return {
        "intro": "本问卷用于理解购买/不购买的关键驱动因素，预计2-4分钟完成。",
        "modules":[
            {"name":"筛选题","questions":[
                {"id":"S1","type":"single","q":"你是否属于目标用户？","options":["是","否"]},
                {"id":"S2","type":"single","q":"你最近3个月是否购买过同类产品/服务？","options":["买过","没买过"]},
            ]},
            {"name":"价值点迫选（建议MaxDiff）","note":"迫选用于减少‘都重要’噪声。",
             "questions":[
                {"id":"V1","type":"maxdiff_seed","q":"以下卖点中，最能驱动你购买的是哪些？最不能驱动的是哪些？",
                 "items":["效果/收益明确","省时省钱","更安全/更可信","更方便易用","售后保障强","口碑/评价好","性价比高"]}
             ]},
            {"name":"阻力与风险排序","questions":[
                {"id":"R1","type":"rank","q":"以下因素会让你不买/犹豫，请按影响从大到小排序",
                 "items":["价格不值","不信任（夸大/虚假）","看不懂/信息不清","担心售后/退换","麻烦（流程/学习成本）","替代方案够用","不确定是否适合我"]}
            ]},
            {"name":"证据偏好","questions":[
                {"id":"E1","type":"multi","q":"你更愿意相信哪些证据？（可多选）",
                 "options":["真实用户评价/口碑","权威背书/专家","对比测评","成分/原理说明","无理由退换/保障承诺","朋友推荐","品牌历史与资质"]}
            ]},
            {"name":"价格敏感","questions":[
                {"id":"P1","type":"single","q":"在满足需求前提下，你觉得合理价格区间是？",
                 "options":["低于$10","$10-$30","$30-$60","$60-$100","$100以上","不确定"]}
            ]},
            {"name":"开放题（少量）","questions":[
                {"id":"O1","type":"text","q":f"如果要实现{goal}提升，你认为最需要先解决的一个问题是什么？（一句话）"}
            ]}
        ],
        "data_quality": {
            "attention_checks": ["设置1-2道注意力题（如选项指令题）"],
            "speeding_rule": "完成时长过短（如<30秒）标记为低质量",
            "straightlining_rule": "连续同选项或无差异作答标记",
            "contradiction_rule": "同义题前后矛盾标记"
        }
    }

# ---------- Text2SQL templates (white-list) ----------
def sql_metric_templates() -> List[Dict[str, Any]]:
    """
    给工程同学/你后续对接数据库用：可控模板，而非自由生成。
    """
    return [
        {
            "name":"首单购买转化率（CVR）",
            "description":"购买用户/访问用户（或订单/会话），按日期、渠道、国家分组",
            "safe_sql_template": """SELECT date(event_time) AS ds,
       channel,
       country,
       COUNT(DISTINCT CASE WHEN event='purchase' THEN user_id END) * 1.0
       / NULLIF(COUNT(DISTINCT CASE WHEN event='visit' THEN user_id END),0) AS cvr
FROM events
WHERE event IN ('visit','purchase')
  AND event_time BETWEEN :start AND :end
GROUP BY 1,2,3
ORDER BY 1 DESC
LIMIT 200;"""
        },
        {
            "name":"加购率（ATC rate）",
            "description":"加购用户/访问用户",
            "safe_sql_template": """SELECT date(event_time) AS ds,
       channel,
       country,
       COUNT(DISTINCT CASE WHEN event='add_to_cart' THEN user_id END) * 1.0
       / NULLIF(COUNT(DISTINCT CASE WHEN event='visit' THEN user_id END),0) AS atc_rate
FROM events
WHERE event IN ('visit','add_to_cart')
  AND event_time BETWEEN :start AND :end
GROUP BY 1,2,3
ORDER BY 1 DESC
LIMIT 200;"""
        }
    ]
