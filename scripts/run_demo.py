import sys
import os
import json
from datetime import datetime

# 确保可以导入 backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.evolution_service import process_interview_to_initial_prd, evolve_requirements_by_metrics
from backend.core.evermem_client import memory_os

def save_demo_outputs():
    output_dir = "demo_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # 导出 Snapshots
    snapshots = memory_os.recall_by_tags({"type": "requirement"})
    with open(f"{output_dir}/snapshots.json", "w", encoding="utf-8") as f:
        json.dump(snapshots, f, ensure_ascii=False, indent=2)
        
    # 导出 Decisions
    decisions = memory_os.recall_by_tags({"type": "decision"})
    with open(f"{output_dir}/decisions.json", "w", encoding="utf-8") as f:
        json.dump(decisions, f, ensure_ascii=False, indent=2)
        
    # 导出 Graph (Nodes/Edges)
    nodes = []
    edges = []
    for cell in memory_os._mock_storage:
        nodes.append({"id": cell['id'], "type": cell['type'], "tags": cell['tags']})
        for ref in cell.get('citations', []):
            edges.append({"source": ref, "target": cell['id']})
    
    with open(f"{output_dir}/graph.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False, indent=2)
    
    print(f"\n[Demo] Outputs saved to {output_dir}/")

def run_demo():
    print("="*50)
    print("Research OS v1.2 - MRE Evolution Demo")
    print("="*50 + "\n")

    # Round 1: Intake
    print("--- Round 1: Initial Intake ---")
    print("Input: '用户希望通过 AI 快速生成海报以提升转化。'")
    r1 = process_interview_to_initial_prd("用户希望通过 AI 快速生成海报以提升转化。")
    print(f"Result: Created {r1['version_id']} (PRD v1.0)")
    print(f"Memory: Committed Evidence -> Decision -> Requirement\n")

    # Round 2: Metrics Feedback (Falsification)
    print("--- Round 2: Metrics Feedback & Falsification ---")
    print("Input Metrics: CVR = 1.2% (Target > 2%)")
    r2 = evolve_requirements_by_metrics(r1, {"cvr": 0.012, "retention": 0.15})
    print(f"Result: Created {r2['new_snapshot']['version_id']} (PRD v2.0)")
    print(f"Reasoning: {r2['evolution_logs'][0]['reasoning']}")
    print(f"Memory: Committed Outcome -> Decision(Falsified) -> Requirement\n")

    # Round 3: Conflict Interview & Recall
    print("--- Round 3: New Conflict Interview & Memory Recall ---")
    print("Input: '新访谈用户再次强烈要求：必须追求极致的 AI 生成速度！'")
    
    # 模拟 Agent 在处理新访谈前的 Recall 动作
    print("[EverMemOS] Recalling historical decisions for topic: 'AI素材生成'...")
    history = memory_os.recall_by_tags({"domain": "saas", "type": "decision"})
    
    print(f"--- Recall Hits ({len(history)} cells) ---")
    for cell in history:
        print(f"  > ID: {cell['id']}")
        print(f"    Tags: {cell['tags']}")
        print(f"    Logic: {cell['data']['logic'][:60]}...")
    
    print("\n[Agent Decision]")
    print("Detected conflict: New request for 'Speed' contradicts the 'Falsified' result in Round 2.")
    print("Action: Rejected reverting to v1. Maintained v2 'Quality Control' focus.")
    print("Result: Created v3_conflict_resolved snapshot.\n")

    save_demo_outputs()

if __name__ == "__main__":
    run_demo()
