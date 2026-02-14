import sqlite3
import json
import sys
import os

# 确保可以导入 backend 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.database import DB_PATH
from backend.core.evermem_client import memory_os

def migrate():
    print("Starting migration from SQLite to EverMemOS...")
    
    if not os.path.exists(DB_PATH):
        print(f"No database found at {DB_PATH}. Skipping migration.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. 迁移 Snapshots
        cursor.execute('SELECT * FROM requirement_snapshots')
        snapshots = cursor.fetchall()
        for row in snapshots:
            snapshot = dict(row)
            snapshot['persona'] = json.loads(snapshot['persona_json'])
            snapshot['hypotheses'] = json.loads(snapshot['hypotheses_json'])
            
            memory_os.commit_memory(
                content=snapshot,
                tags=["type:snapshot", f"ver:{snapshot['version_id']}", "domain:mre"],
                importance=0.9
            )
            print(f"Migrated Snapshot: {snapshot['version_id']}")

        # 2. 迁移 Evolution Logs
        cursor.execute('SELECT * FROM evolution_logs')
        logs = cursor.fetchall()
        for row in logs:
            log = dict(row)
            log['evidence_metric'] = json.loads(log['evidence_metric'])
            
            memory_os.commit_memory(
                content=log,
                tags=["type:evolution", f"ref:{log['version_id']}", "domain:mre"],
                importance=0.8
            )
            print(f"Migrated Evolution Log for version: {log['version_id']}")

    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
