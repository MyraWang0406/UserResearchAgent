# 部署说明（Railway 后端 + Cloudflare Pages 前端）

本仓库**不再使用 ECS**。线上架构：

- **后端：** Railway（通过 GitHub 连接，push main 自动构建部署）
- **前端：** GitHub → Cloudflare Pages（连接本仓库，静态站点根目录为 `frontend` 或根目录）
- **记忆服务：** 后端调用 **EverMemOS Cloud**（通过环境变量 `EVERMEM_URL` 配置）

---

## 1. 后端部署（Railway）

1. 登录 [Railway](https://railway.app)，用 GitHub 登录。
2. **New Project** → **Deploy from GitHub repo** → 选择 `MyraWang0406/UserResearchAgent`。
3. 根目录已有 `railway.json`，启动命令为：  
   `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`  
   Railway 会自动注入 `PORT`，无需改代码。
4. **环境变量（必配）：**
   - `EVERMEM_URL`：EverMemOS Cloud 的 API 根地址（例如 `https://your-evermem-cloud.example.com`）。不设则后端以 **Mock 模式** 运行（记忆不持久化）。
   - 若 EverMem Cloud 需要 API Key，请按 EverMem 文档在请求头或 URL 中配置；本仓库当前通过 `EVERMEM_URL` 区分 Mock/Real。
5. 部署完成后，在 Railway 项目 **Settings → Domains** 中查看 **Public URL**（当前为 `https://userinsightagent-production.up.railway.app`）。
6. 前端已默认使用该 URL；若你部署的 Railway 域名不同，用户需在页面点击「设置API地址」填写实际 URL。

---

## 2. 前端部署（Cloudflare Pages）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**。
2. 选择 GitHub 账号下的 **MyraWang0406/UserResearchAgent**，分支 **main**。
3. **Build 配置：**
   - **Build command：** 留空或 `echo "static"`（本前端无构建步骤）。
   - **Build output directory / Root：**
     - 若选 **Root**：站点根目录为仓库根，首页为根目录的 `index.html`（已与 `frontend/index.html` 同步）。
     - 若选 **frontend**：站点根目录为 `frontend/`，首页为 `frontend/index.html`。
4. 保存并部署。之后每次 push 到 main 会自动重新部署。
5. 部署完成后会得到 `*.pages.dev` 域名；可绑定自定义域名。

---

## 3. 前后端联调

- 前端（Cloudflare Pages）默认请求的后端地址为 **`https://userinsightagent-production.up.railway.app`**（见 `frontend/index.html` 与根目录 `index.html` 中的 `getDefaultApiBase()`）。
- 若你的 Railway 应用 URL 不同，用户打开前端后点击「设置API地址」，填入 Railway 的 **Public URL** 即可（不要带端口，不要填 `:8000`）。
- 后端已开启 CORS（`allow_origins=["*"]`），Pages 域名可正常跨域请求 Railway。

---

## 4. 仓库内可查的部署相关文件

| 文件 | 说明 |
|------|------|
| `railway.json` | Railway 构建与启动命令（Nixpacks + uvicorn） |
| `frontend/index.html` | 前端单页；内嵌默认 API 与「设置API地址」逻辑 |
| `index.html` | 根目录副本，供「以根目录为站点根」的 Pages 使用 |
| `backend/app.py` | FastAPI 应用；已加 CORS，供 Pages 调用 |
| `backend/core/evermem_client.py` | 记忆客户端；通过 `EVERMEM_URL` 接 EverMemOS Cloud |

---

## 5. 验收（Railway + Pages）

- **后端：** 打开 `https://userinsightagent-production.up.railway.app/docs` 应返回 200，Swagger 可访问。
- **前端：** 打开 Cloudflare Pages 站点，不设置 API 时默认请求上述 Railway URL；Run A / Run B 不应出现 Failed to fetch。
- **EverMem：** 配置好 `EVERMEM_URL` 后，后端日志应出现 `[EverMemOS] Running in REAL mode: ...`，否则为 Mock 模式。
