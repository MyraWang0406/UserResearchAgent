import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class EverMemClient:
    """
    EverMemOS 适配器：支持组织决策记忆模型 (Context/Evidence/Decision/Requirement)
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("EVERMEM_URL", "http://localhost:8080")
        self._mock_storage = []

    def commit_cell(self, cell_type: str, data: Dict[str, Any], tags: Dict[str, str], citations: List[str] = []) -> str:
        """
        提交一个组织决策记忆单元
        tags: {"domain": "saas", "stage": "1-10", ...}
        """
        cell_id = f"{cell_type.lower()}_{datetime.now().timestamp()}"
        
        # 将字典形式的 tags 展平为 EverMemOS 格式
        flat_tags = [f"{k}:{v}" for k, v in tags.items()]
        flat_tags.append(f"type:{cell_type.lower()}")
        
        cell = {
            "id": cell_id,
            "type": cell_type,
            "content": json.dumps(data),
            "tags": flat_tags,
            "citations": citations,
            "timestamp": datetime.now().isoformat()
        }
        self._mock_storage.append(cell)
        print(f"[EverMemOS] Committed {cell_type} Cell: {cell_id} | Tags: {flat_tags} | Citations: {citations}")
        return cell_id

    def recall_by_tags(self, query_tags: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        通过多维标签回溯记忆
        """
        flat_query = [f"{k}:{v}" for k, v in query_tags.items()]
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

# 全局单例
memory_os = EverMemClient()
