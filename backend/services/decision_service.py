from datetime import datetime
from typing import Dict, Any, List
from ..core.evermem_client import memory_os

class DecisionService:
    @staticmethod
    def run_evolution_round(input_type: str, content: Any, context_tags: Dict[str, str]) -> Dict[str, Any]:
        history = memory_os.recall_by_tags({**context_tags, "type": "decision"})
        falsified_decisions = [c for c in history if "FALSIFIED:true" in (c.get('tags') or [])]

        if input_type == "interview":
            is_conflict = False
            if "speed" in str(content).lower():
                for d in falsified_decisions:
                    rationale = str(d.get('data', {}).get('rationale', ''))
                    if "speed" in rationale.lower() or "hypothesis" in rationale.lower():
                        is_conflict = True
                        break

            if is_conflict:
                decision_logic = "Conflict Detected: Rejected reverting to speed-focus; maintained quality-focus due to previous falsification."
            else:
                decision_logic = "Initial requirement generation based on interview."

            ev_id = memory_os.commit_cell("Evidence", {"summary": content, "source_type": "Interview"}, context_tags)
            dec_id = memory_os.commit_cell("Decision", {"rationale": decision_logic, "decision_type": "Requirement_Gen"}, context_tags, citations=[ev_id])
            req_id = memory_os.commit_cell("Requirement", {"scope_summary": "PRD Content", "version": "v1.0"}, context_tags, citations=[dec_id])

            return {"req_id": req_id, "dec_id": dec_id, "ev_id": ev_id, "logic": decision_logic}

        elif input_type == "metrics":
            cvr = content.get("cvr", 0) if isinstance(content, dict) else 0
            verdict = "FALSIFY" if cvr < 0.02 else "SUPPORT"

            out_id = memory_os.commit_cell("Outcome", {"metrics_delta": content, "verdict": verdict}, context_tags)
            dec_tags = {**context_tags}
            if verdict == "FALSIFY":
                dec_tags["FALSIFIED"] = "true"

            dec_id = memory_os.commit_cell("Decision", {"rationale": f"Metrics {verdict} previous speed hypothesis.", "decision_type": "Evolution"}, dec_tags, citations=[out_id])

            return {"dec_id": dec_id, "out_id": out_id, "verdict": verdict}

decision_service = DecisionService()
