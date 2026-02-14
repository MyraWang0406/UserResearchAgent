import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class EverMemClient:
    """
    EverMemOS 适配器：将业务数据映射为具有生命周期的 Memory Cells
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("EVERMEM_URL", "http://localhost:8080")
        # 模拟内存存储，用于演示环境，实际应调用 API
        self._mock_storage = []

    def commit_memory(self, content: Dict[str, Any], tags: List[str], importance: float = 1.0) -> str:
        """
        提交一段记忆单元 (Memory Cell)
        """
        cell_id = f"cell_{datetime.now().timestamp()}"
        cell = {
            "id": cell_id,
            "content": json.dumps(content),
            "tags": tags,
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }
        self._mock_storage.append(cell)
        print(f"[EverMemOS] Committed Memory Cell: {cell_id} with tags {tags}")
        return cell_id

    def recall_memory(self, query_tags: List[str]) -> List[Dict[str, Any]]:
        """
        通过标签回溯记忆 (Recall)
        """
        results = []
        for cell in self._mock_storage:
            if all(tag in cell['tags'] for tag in query_tags):
                results.append({
                    "id": cell['id'],
                    "content": json.loads(cell['content']),
                    "tags": cell['tags'],
                    "timestamp": cell['timestamp']
                })
        # 按时间倒序排列
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return results

# 全局单例
memory_os = EverMemClient()
