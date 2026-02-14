import sys
import os
import json
from datetime import datetime

# 确保可以导入 backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.decision_service import decision_service
from backend.core.evermem_client import memory_os

def save_outputs():
    output_dir = "demo_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Snapshots (Requirements)
    reqs = memory_os.recall_by_tags({"type": "requirement"})
    with open(f"{output_dir}/snapshots.json", "w", encoding="utf-8") as f:
        json.dump(reqs, f, ensure_ascii=False, indent=2)
        
    # 2. Decisions
    decs = memory_os.recall_by_tags({"type": "decision"})
    with open(f"{output_dir}/decisions.json", "w", encoding="utf-8") as f:
        json.dump(decs, f, ensure_ascii=False, indent=2)
        
    # 3. Graph
    nodes = []
    edges = []
    for cell in memory_os._mock_storage:
        nodes.append({"id": cell['id'], "type": cell['type'], "summary": json.loads(cell['content']).get('rationale', '...')})
        for ref in cell.get('citations', []):
            edges.append({"source": ref, "target": cell['id']})
            
    with open(f"{output_dir}/graph.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False, indent=2)
    
    print(f"\n[Demo] MVP Outputs saved to {output_dir}/")

def run_mvp_demo():
    print("="*60)
    print("Decision Memory MVP - Memory Genesis Track 1")
    print("="*60 + "\n")

    tags = {"domain": "fintech", "stage": "1-10", "growth": "PLG"}

    # Round 1: Intake
    print("--- Round 1: Interview -> Evidence -> Decision -> Req v1 ---")
    r1 = decision_service.run_evolution_round("interview", "Users want fast AI generation speed.", tags)
    print(f"Decision: {r1['logic']}")
    print(f"Citations: {r1['ev_id']}\n")

    # Round 2: Metrics -> Outcome -> Decision(Falsify) -> Req v2
    print("--- Round 2: Metrics -> Outcome -> Decision(Falsify) -> Req v2 ---")
    r2 = decision_service.run_evolution_round("metrics", {"cvr": 0.015}, tags)
    print(f"Verdict: {r2['verdict']} (CVR < 2%)")
    print(f"Decision: Metrics falsified previous hypothesis.\n")

    # Round 3: New Interview (Conflict) -> Recall -> Req v3
    print("--- Round 3: New Conflict Interview -> Recall -> Req v3 ---")
    r3 = decision_service.run_evolution_round("interview", "New user insists on extreme AI speed!", tags)
    print(f"Recall Hit: Found falsified decision from Round 2.")
    print(f"Final Decision: {r3['logic']}\n")

    save_outputs()

if __name__ == "__main__":
    run_mvp_demo()
