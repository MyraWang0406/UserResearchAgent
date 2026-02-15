import json
import os
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional

class EverMemClient:
    """
    统一 Memory 接口：支持 HTTP 真实模式与 Mock 模式
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("EVERMEM_URL")
        self._mock_storage = []
        self.is_mock = self.base_url is None
        if self.is_mock:
            print("[EverMemOS] Running in MOCK mode.")
        else:
            print(f"[EverMemOS] Running in REAL mode: {self.base_url}")

    def commit_cell(self, cell_type: str, data: Dict[str, Any], tags: Dict[str, str], citations: List[str] = None) -> str:
        citations = citations or []
        cell_id = f"{cell_type.lower()}_{datetime.now().timestamp()}"
        flat_tags = [f"{k}:{v}" for k, v in tags.items()]
        flat_tags.append(f"type:{cell_type.lower()}")

        cell_payload = {
            "id": cell_id,
            "type": cell_type,
            "content": json.dumps(data),
            "tags": flat_tags,
            "citations": citations,
            "timestamp": datetime.now().isoformat()
        }

        if self.is_mock:
            self._mock_storage.append(cell_payload)
        else:
            try:
                with httpx.Client() as client:
                    client.post(f"{self.base_url}/commit", json=cell_payload, timeout=5.0)
            except Exception as e:
                print(f"[EverMemOS] HTTP Commit Error: {e}. Falling back to mock.")
                self._mock_storage.append(cell_payload)

        print(f"[EverMemOS] Committed {cell_type} Cell: {cell_id}")
        return cell_id

    def recall_by_tags(self, query_tags: Dict[str, str]) -> List[Dict[str, Any]]:
        flat_query = [f"{k}:{v}" for k, v in query_tags.items()]

        if not self.is_mock:
            try:
                with httpx.Client() as client:
                    resp = client.get(f"{self.base_url}/recall", params={"tags": ",".join(flat_query)}, timeout=5.0)
                    if resp.status_code == 200:
                        return resp.json()
            except Exception as e:
                print(f"[EverMemOS] HTTP Recall Error: {e}. Falling back to mock.")

        results = []
        for cell in self._mock_storage:
            if all(tag in cell['tags'] for tag in flat_query):
                results.append({
                    "id": cell['id'],
                    "type": cell['type'],
                    "data": json.loads(cell['content']),
                    "tags": cell['tags'],
                    "citations": cell.get('citations', []),
                    "timestamp": cell['timestamp']
                })
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return results

memory_os = EverMemClient()
