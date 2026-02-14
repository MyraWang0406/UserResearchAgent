# Research OS v1.2: Memory-driven Requirement Evolution (MRE)

这是一个基于 **EverMemOS** 记忆单元构建的需求演化系统，支持从访谈到决策、从指标到证伪的全链路记忆回溯。

---

## 🚀 快速开始 (Quickstart)

### 1. 环境配置
系统支持 **EverMemOS 远程连接** 与 **本地 Mock 降级模式**。

- **远程模式**: 设置环境变量 `EVERMEM_URL` 指向您的 EverMemOS 实例。
  ```bash
  export EVERMEM_URL="http://your-evermemos-ip:8080"
  ```
- **降级模式**: 若未设置环境变量，系统将自动启用内置的 `Mock Memory Storage`，无需安装额外依赖即可运行 Demo。

### 2. 运行可复现 Demo
我们提供了一个三轮演化脚本，演示系统如何处理“指标证伪”与“需求冲突”：
```bash
python3 scripts/run_demo.py
```

### 3. 查看 Demo 产物
运行结束后，系统会在 `demo_outputs/` 目录下生成以下文件：
- `snapshots.json`: 记录了从 v1 到 v3 的所有需求快照。
- `decisions.json`: 记录了每一轮演化的决策逻辑。
- `graph.json`: 完整的 **Evidence -> Decision -> Requirement** 引用图谱数据。

---

## 🧠 核心架构：组织决策记忆 (ODM)

系统将数据映射为四类 **Memory Cells**:
1. **Context**: 业务背景（PLG/SLG, 阶段, 领导风格）。
2. **Evidence**: 原始事实（访谈文本, 指标数据）。
3. **Decision**: 决策推导（必须援引 Evidence）。
4. **Requirement**: 最终 PRD（溯源至 Decision）。

### 演化闭环示例
- **Round 1**: 初始访谈 -> 生成 PRD v1.0。
- **Round 2**: 指标反馈 (CVR < 2%) -> **证伪** v1.0 假设 -> 演化出 PRD v2.0。
- **Round 3**: 新访谈冲突 -> **回溯 (Recall)** 历史决策 -> 识别冲突并保持演化方向 -> 生成 PRD v3.0。

---

## 🛠️ 开发与部署
- **后端**: FastAPI + SQLite (索引) + EverMemOS (记忆)。
- **前端**: 动态配置面板，支持实时查看 Trace 监控与溯源图谱。
- **部署**: 支持 Docker 一键部署及 Cloudflare Pages 托管。
