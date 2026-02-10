import uuid
from typing import Any, Dict, List, Callable
from ..schemas.models import TraceLog, TraceStatus

class ResearchOS:
    def __init__(self):
        self.traces: List[TraceLog] = []

    def execute_step(self, step_name: str, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        trace_id = str(uuid.uuid4())
        input_data = {"args": args, "kwargs": kwargs}
        
        try:
            # 模拟工具调用记录
            result = func(*args, **kwargs)
            
            trace = TraceLog(
                trace_id=trace_id,
                step_name=step_name,
                input_data=input_data,
                output_data=result,
                status=TraceStatus.SUCCESS
            )
            self.traces.append(trace)
            return {"trace_id": trace_id, "data": result}
            
        except Exception as e:
            # 自动降级策略
            fallback_result = self._fallback_strategy(step_name, e)
            trace = TraceLog(
                trace_id=trace_id,
                step_name=step_name,
                input_data=input_data,
                output_data=fallback_result,
                status=TraceStatus.DEGRADED,
                error_msg=str(e)
            )
            self.traces.append(trace)
            return {"trace_id": trace_id, "data": fallback_result, "degraded": True}

    def _fallback_strategy(self, step_name: str, error: Exception) -> Dict[str, Any]:
        # 针对不同步骤的降级逻辑
        fallbacks = {
            "diagnose": {"recommended_route": ["基础诊断：请补充更多漏斗数据"], "notes": "由于模型/工具异常，已切换至保守规则模式"},
            "generate_survey": {"questions": [{"q": "请描述您的核心痛点", "type": "text"}], "notes": "生成失败，已回退至通用模板"}
        }
        return fallbacks.get(step_name, {"error": "Critical failure", "msg": str(error)})

# 全局单例
engine = ResearchOS()
