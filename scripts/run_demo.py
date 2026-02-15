import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.decision_service import decision_service
from backend.core.evermem_client import memory_os

class DemoLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(f"=== Decision Memory MVP Demo Log - {datetime.now().isoformat()} ===\n\n")

    def log(self, message):
        print(message)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

def save_demo_outputs(logger):
    output_dir = "demo_outputs"
    os.makedirs(output_dir, exist_ok=True)

    snapshots = memory_os.recall_by_tags({"type": "requirement"})
    with open(f"{output_dir}/snapshots.json", "w", encoding="utf-8") as f:
        json.dump(snapshots, f, ensure_ascii=False, indent=2)

    decisions = memory_os.recall_by_tags({"type": "decision"})
    with open(f"{output_dir}/decisions.json", "w", encoding="utf-8") as f:
        json.dump(decisions, f, ensure_ascii=False, indent=2)

    nodes = []
    edges = []
    all_types = ["evidence", "decision", "requirement", "outcome"]
    for t in all_types:
        cells = memory_os.recall_by_tags({"type": t})
        for cell in cells:
            nodes.append({
                "id": cell['id'],
                "type": cell['type'],
                "summary": cell['data'].get('rationale', cell['data'].get('summary', '...'))
            })
            for ref in cell.get('citations', []):
                edges.append({"source": ref, "target": cell['id']})

    with open(f"{output_dir}/graph.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False, indent=2)

    logger.log(f"\n[Demo] MVP Outputs saved to {output_dir}/ (Nodes: {len(nodes)}, Edges: {len(edges)})")

def run_mvp_demo():
    logger = DemoLogger("demo_outputs/demo.log")
    logger.log("=" * 60)
    logger.log("Decision Memory MVP - Memory Genesis Track 1 (Standardized)")
    logger.log("=" * 60 + "\n")

    tags = {"domain": "fintech", "stage": "1-10", "growth": "PLG"}

    logger.log("--- Round 1: Interview -> Evidence -> Decision -> Req v1 ---")
    r1 = decision_service.run_evolution_round("interview", "Users want fast AI generation speed.", tags)
    logger.log(f"Decision Rationale: {r1['logic']}")
    logger.log(f"Citations: {r1['ev_id']}\n")

    logger.log("--- Round 2: Metrics -> Outcome -> Decision(Falsify) -> Req v2 ---")
    r2 = decision_service.run_evolution_round("metrics", {"cvr": 0.015}, tags)
    logger.log(f"Verdict: {r2['verdict']} (CVR < 2%)")
    logger.log(f"Decision: Metrics falsified previous hypothesis. Decision ID: {r2['dec_id']}\n")

    logger.log("--- Round 3: New Conflict Interview -> Recall -> Req v3 ---")
    logger.log("[EverMemOS] Recalling historical decisions to check for conflicts...")
    history = memory_os.recall_by_tags({**tags, "type": "decision"})
    logger.log(f"RecallHits Found: {len(history)} cells")
    for cell in history:
        summary = (cell['data'].get('rationale', 'No rationale') or '')[:60] + "..."
        logger.log(f"  - [Hit] ID: {cell['id']} | Tags: {cell.get('tags', [])} | Summary: {summary}")

    r3 = decision_service.run_evolution_round("interview", "New user insists on extreme AI speed!", tags)
    if "Conflict Detected" in r3['logic']:
        logger.log(f"Conflict Reason: Detected contradiction with Round 2 Falsification (Decision ID: {r2['dec_id']})")
    logger.log(f"Final Decision Rationale: {r3['logic']}\n")

    save_demo_outputs(logger)

if __name__ == "__main__":
    run_mvp_demo()
