# Research OS: AI 产品操作系统

这是一个可演进的 AI 产品研究与决策系统，旨在通过 Traceable（可追溯）的决策链路，帮助 B 端业务提升首单转化率。

## 🚀 快速开始 (Windows)

**照抄以下命令即可跑起来：**

1. **克隆仓库**
   ```bash
   git clone https://github.com/MyraWang0406/UserResearchAgent.git
   cd UserResearchAgent
   ```

2. **一键启动**
   直接双击运行 `start.bat`。
   *脚本会自动检查 Python 3.12 环境、创建虚拟环境、安装依赖并同时启动前后端。*

3. **访问界面**
   打开浏览器访问：`http://localhost:5173`

---

## ☁️ Cloudflare 部署方案

### 1. 前端部署 (Cloudflare Pages)
1. 进入 Cloudflare 控制台 -> Workers & Pages。
2. 点击 "Create application" -> "Pages" -> "Connect to Git"。
3. 选择本仓库，构建设置如下：
   - **Framework preset**: None
   - **Build command**: (留空)
   - **Build output directory**: `frontend`

### 2. 后端部署 (Cloudflare Workers + D1)
由于 Python 在 Workers 上的限制，建议使用以下命令部署适配层：
```bash
# 安装 Wrangler
npm install -g wrangler

# 初始化 D1 数据库
wrangler d1 create research-db

# 部署 Worker (需根据 mcp/worker.js 适配)
wrangler deploy
```

---

## 🛠️ 架构特性

- **决策链路 OS**: Plan → Tool Usage → Evidence → Decision → Action。
- **Trace 系统**: 每个步骤生成唯一 `trace_id`，记录输入输出与评分。
- **HITL 门禁**: 关键动作（如发布问卷）需通过 `POST /api/v1/approve` 审批。
- **自动降级**: 工具调用失败时自动切换至保守的规则引擎模式。

---

## 🔌 MCP (Model Context Protocol) 接入

本系统支持通过 MCP 将研究工具暴露给客户端（如 Claude Desktop）：

1. **配置说明**:
   在 `mcp/config.json` 中定义工具映射。
2. **启动 MCP Server**:
   ```bash
   python -m mcp.server
   ```

---

## ⚖️ 权限模型
- `ADMIN`: 全权限。
- `PUBLISHER`: 可发布研究任务，需 HITL 审批。
- `READONLY`: 仅查看 Trace 与报告。
