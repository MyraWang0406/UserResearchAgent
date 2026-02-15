import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .evermem_client import memory_os

DB_PATH = "research_os.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traces (
                trace_id TEXT PRIMARY KEY,
                step_name TEXT,
                input_data TEXT,
                output_data TEXT,
                status TEXT,
                error_msg TEXT,
                score REAL,
                timestamp DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requirement_snapshots (
                version_id TEXT PRIMARY KEY,
                parent_version_id TEXT,
                persona_json TEXT,
                hypotheses_json TEXT,
                prd_markdown TEXT,
                iteration_count INTEGER,
                timestamp DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_id TEXT,
                change_type TEXT,
                target_requirement TEXT,
                reasoning TEXT,
                evidence_metric TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()

def save_trace(trace: Dict[str, Any]):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO traces (trace_id, step_name, input_data, output_data, status, error_msg, score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trace['trace_id'], trace['step_name'],
            json.dumps(trace['input_data']), json.dumps(trace['output_data']),
            trace['status'], trace.get('error_msg'), trace.get('score', 1.0),
            datetime.now().isoformat()
        ))
        conn.commit()
    memory_os.commit_cell(
        cell_type="Trace",
        data=trace,
        tags={"type": "trace", "step": trace['step_name'], "domain": "mre"}
    )

def save_snapshot(snapshot: Dict[str, Any]):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO requirement_snapshots (version_id, parent_version_id, persona_json, hypotheses_json, prd_markdown, iteration_count, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            snapshot['version_id'], snapshot.get('parent_version_id'),
            json.dumps(snapshot['persona']), json.dumps(snapshot['hypotheses']),
            snapshot['prd_markdown'], snapshot.get('iteration_count', 0),
            datetime.now().isoformat()
        ))
        conn.commit()
    memory_os.commit_cell(
        cell_type="Requirement",
        data=snapshot,
        tags={"type": "requirement", "ver": snapshot['version_id'], "domain": "mre"}
    )

def save_evolution_log(log: Dict[str, Any]):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evolution_logs (version_id, change_type, target_requirement, reasoning, evidence_metric, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            log['version_id'], log['change_type'], log.get('target_requirement'),
            log['reasoning'], json.dumps(log.get('evidence_metric')),
            datetime.now().isoformat()
        ))
        conn.commit()
    memory_os.commit_cell(
        cell_type="Evolution",
        data=log,
        tags={"type": "evolution", "ref": log['version_id'], "domain": "mre"}
    )

def get_latest_snapshot():
    memories = memory_os.recall_by_tags({"type": "requirement", "domain": "mre"})
    if memories:
        return memories[0]['data']
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM requirement_snapshots ORDER BY timestamp DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            res = dict(row)
            res['persona'] = json.loads(res['persona_json'])
            res['hypotheses'] = json.loads(res['hypotheses_json'])
            return res
        return None

def get_all_traces():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM traces ORDER BY timestamp DESC')
        return [dict(row) for row in cursor.fetchall()]
