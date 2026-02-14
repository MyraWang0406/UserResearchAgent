import uuid
from datetime import datetime
from typing import Dict, Any, List
from ..core.evermem_client import memory_os

class DecisionService:
    """
    核心业务逻辑：处理援引、演化与冲突检测
    """
    @staticmethod
    def run_evolution_round(input_type: str, content: Any, context_tags: Dict[str, str]) -> Dict[str, Any]:
        print(f"\n[DecisionService] Starting Round: {input_type}")
        
        # 1. 记忆回溯 (Recall)
        history = memory_os.recall_by_tags(context_tags)
        print(f"[EverMemOS] Recalled {len(history)} historical cells.")

        # 2. 冲突检测 (Conflict Detection)
        falsified_decisions = [c for c in history if c['type'] == 'Decision' and 'FALSIFIED' in c['tags']]
        
        # 3. 执行逻辑 (模拟 Agent 判断)
        if input_type == "interview":
            # 检查新访谈是否与已证伪的决策冲突
            is_conflict = any("speed" in content.lower() and "speed" in str(d['data']).lower() for d in falsified_decisions)
            
            if is_conflict:
                print("[Agent] Conflict Detected! New request contradicts a previously falsified decision.")
                decision_logic = "Rejected reverting to speed-focus; maintained quality-focus due to previous falsification."
                tags = {**context_tags, "type": "decision", "status": "conflict_resolved"}
            else:
                decision_logic = "Initial requirement generation based on interview."
                tags = {**context_tags, "type": "decision"}
                
            # 提交证据
            ev_id = memory_os.commit_cell("Evidence", {"summary": content, "source_type": "Interview"}, context_tags)
            # 提交决策 (强制援引)
            dec_id = memory_os.commit_cell("Decision", {"rationale": decision_logic, "decision_type": "Requirement_Gen"}, context_tags, citations=[ev_id])
            # 提交需求
            req_id = memory_os.commit_cell("Requirement", {"scope_summary": "PRD Content", "version": "v1.0"}, context_tags, citations=[dec_id])
            
            return {"req_id": req_id, "dec_id": dec_id, "ev_id": ev_id, "logic": decision_logic}

        elif input_type == "metrics":
            # 指标反馈逻辑
            cvr = content.get("cvr", 0)
            verdict = "FALSIFY" if cvr < 0.02 else "SUPPORT"
            
            # 提交结果
            out_id = memory_os.commit_cell("Outcome", {"metrics_delta": content, "verdict": verdict}, context_tags)
            # 提交演化决策
            dec_tags = {**context_tags}
            if verdict == "FALSIFY": dec_tags["FALSIFIED"] = "true"
            
            dec_id = memory_os.commit_cell("Decision", {"rationale": f"Metrics {verdict} previous hypothesis.", "decision_type": "Evolution"}, dec_tags, citations=[out_id])
            
            return {"dec_id": dec_id, "out_id": out_id, "verdict": verdict}

decision_service = DecisionService()
