# Research OS v1.1: AI 产品操作系统

这是一个可演进的 AI 产品研究与决策系统，实现了 **Traceable（可追溯）** 的决策链路与 **Human-in-the-loop（人类在环审批）** 门禁。

---

## ☁️ 云端部署 (Cloudflare Pages + 阿里云 ECS)

### 第一步：后端部署 (阿里云 ECS / Docker)
**照抄以下命令（需已安装 Docker）：**
1. **克隆并进入目录**
   ```bash
   git clone https://github.com/MyraWang0406/UserResearchAgent.git
   cd UserResearchAgent
   ```
2. **启动后端容器**
   ```bash
   docker-compose up -d
   ```
   *后端将运行在 `http://localhost:8000`，数据持久化在 `research_os.db`。*

3. **安全内网穿透 (Cloudflare Tunnel)**
   如果你不想开放 ECS 端口，请执行：
   ```bash
   # 安装 cloudflared
   curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && dpkg -i cloudflared.deb
   
   # 创建隧道
   cloudflared tunnel login
   cloudflared tunnel create research-os-tunnel
   
   # 配置 DNS (将 api.yourdomain.com 指向隧道)
   cloudflared tunnel route dns research-os-tunnel api.yourdomain.com
   
   # 运行隧道 (将流量转发到本地 8000)
   cloudflared tunnel run --url http://localhost:8000 research-os-tunnel
   ```

### 第二步：前端部署 (Cloudflare Pages)
1. 登录 Cloudflare 控制台 -> **Workers & Pages** -> **Create application** -> **Pages**。
2. 连接本仓库，设置如下：
   - **Build command**: (留空)
   - **Build output directory**: `frontend`
3. 部署完成后，在 Pages 设置中绑定自定义域名（如 `app.yourdomain.com`）。

---

## 💻 本地运行 (可选)
1. **安装依赖**: `pip install -r requirements.txt`
2. **启动**: 直接运行 `start.bat` (Windows) 或 `uvicorn backend.api.main:app --reload`。

---

## 🧠 架构说明

### 1. 决策链路 (Decision Link)
系统不直接输出结论，而是遵循：
**Plan（规划）** → **Tool Usage（工具调用）** → **Evidence（证据收集）** → **Decision（决策）** → **Action（行动）**。

### 2. 核心组件
- **Pipeline（流水线）**: 负责数据的串行加工（如：原始问题 -> 结构化诊断）。
- **Workflow（工作流）**: 负责多分支编排与 **Human-in-the-loop（人类在环审批）**。
- **Skills（技能）**: 后端内部封装的原子工具（问卷生成、指标拆解、降级模板）。
- **MCP（模型上下文协议）**: 通过 `GET /mcp/tools` 和 `POST /mcp/call` 暴露的 HTTP 工具网关，方便任何 AI 客户端接入。

### 3. 容错与追溯
- **失败回退**: 当 AI 工具调用失败或置信度低时，系统自动降级到预设的规则模板，并在 Trace 中记录 `DEGRADED` 状态。
- **Trace 存储**: 所有决策步骤均持久化至 SQLite，可通过前端“Trace 监控”实时查阅。

### 4. 权限模型 (RBAC)
- **管理员 (ADMIN)**: 拥有全量 API 访问与审批权。
- **发布者 (PUBLISHER)**: 可发起诊断与生成，但关键动作需审批。
- **只读 (READONLY)**: 仅能查看 Trace 列表。
