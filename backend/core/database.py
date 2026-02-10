import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = "research_os.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Trace 表
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
        # HITL 审批表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approvals (
                id TEXT PRIMARY KEY,
                action_type TEXT,
                payload TEXT,
                status TEXT,
                requester_id TEXT,
                approver_id TEXT,
                comment TEXT,
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

def get_all_traces():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM traces ORDER BY timestamp DESC')
        return [dict(row) for row in cursor.fetchall()]

def create_approval(approval: Dict[str, Any]):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO approvals (id, action_type, payload, status, requester_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            approval['id'], approval['action_type'], json.dumps(approval['payload']),
            'PENDING', approval['requester_id'], datetime.now().isoformat()
        ))
        conn.commit()

def update_approval(approval_id: str, status: str, approver_id: str, comment: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE approvals SET status = ?, approver_id = ?, comment = ? WHERE id = ?
        ''', (status, approver_id, comment, approval_id))
        conn.commit()

def get_pending_approvals():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM approvals WHERE status = 'PENDING'")
        return [dict(row) for row in cursor.fetchall()]
