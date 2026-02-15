import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
API_KEY = "admin123"
HEADERS = {"X-API-Key": API_KEY}

def test_decision_requires_citations():
    """citations 为空时 POST /api/v1/decision 返回 400"""
    payload = {
        "decision_type": "Feature_Pivot",
        "rationale": "test",
        "citations": [],
        "tradeoffs": "",
        "timestamp": "2026-02-15T00:00:00Z"
    }
    r = client.post("/api/v1/decision", json=payload, headers=HEADERS)
    assert r.status_code == 400
    assert "cite" in r.json().get("detail", "").lower() or "evidence" in r.json().get("detail", "").lower()

def test_trace_graph_returns_nodes_edges():
    """trace_graph 返回 nodes/edges 结构"""
    r = client.get("/api/v1/trace_graph", headers=HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)
