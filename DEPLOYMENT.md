# 线上部署证据与结论

## 0. 仓库证据（可验证）

```bash
git checkout main && git pull
git remote -v
git log -1 --oneline
```

- **Remote:** `origin` → `https://github.com/MyraWang0406/UserResearchAgent.git`
- **当前 main 最新 commit:** 见 `git log -1 --oneline` 输出（本次 push 后更新）

## 1. 关键字命中与“线上实际入口”结论

在仓库内全局搜索下列关键字，命中文件如下：

| 关键字 | 命中文件路径 |
|--------|--------------|
| B端售前诊断 | `frontend/index.html`, `index.html`（根目录副本） |
| 增长驱动方式 | `frontend/index.html`, `index.html`, `backend/app.py`, `VERIFICATION.md` |
| growth_driver | `frontend/index.html`, `index.html`, `backend/logic.py`, `backend/app.py` |
| 联系作者 | `frontend/index.html`, `index.html`, `VERIFICATION.md` |
| myrawzm0406@163.com | `frontend/index.html`, `index.html` |

**结论：** 本仓库中**唯一前端页面**即上述包含这些内容的文件：**`frontend/index.html`**。根目录 **`index.html`** 已作为其副本加入，供“以仓库根目录为站点根”的部署使用。

## 2. 部署配置（本仓库内可查）

- **Cloudflare Pages：** 仓库内**无** `wrangler.toml` 或其它 Cloudflare 配置；无法从代码推断线上项目设置。
- **GitHub Pages：** 仅存在 `.github/workflows/ci.yml`，为 **CI 测试**（pytest、run_demo），**无** `deploy` / `pages` 等部署步骤。

因此：**线上 https://userinsightagent.myrawzm0406.online/ 的部署源与分支/目录，必须到实际托管平台查看。**

### 你需要在托管侧确认的项（必做）

- **Cloudflare Pages：**  
  Dashboard → 该项目 → Settings → Builds & deployments  
  - **Connected Repository**：是否为 `MyraWang0406/UserResearchAgent`  
  - **Production branch**：是否为 `main`  
  - **Build command**：若为静态，可为空或 `echo`  
  - **Build output directory / Root directory：**  
    - 若为 **根目录**：应使用 **`/`**（根目录），此时站点会使用仓库根目录的 **`index.html`**（已与 frontend 一致）。  
    - 若为 **frontend 目录**：应设为 **`frontend`**，此时站点根即 `frontend/`，会使用 **`frontend/index.html`**。

- **GitHub Pages：**  
  Repo → Settings → Pages  
  - **Source**：Branch = `main`  
  - **Folder**：选 **`/frontend`** 或 **`/ (root)`**。若选 root，则使用根目录的 **`index.html`**（已与 frontend 一致）。

### 结论（写清楚）

- **线上拉取的 Repo：** 应为 **MyraWang0406/UserResearchAgent**（若为其它 repo，则需改为本 repo 或把本 repo 的 frontend 代码迁入被部署的 repo）。  
- **分支：** 应为 **main**。  
- **目录：** 二选一——  
  - **Root 部署**：输出/根目录 = 仓库根目录，则首页即 **根目录 `index.html`**（已与 `frontend/index.html` 内容一致）；  
  - **Frontend 部署**：输出/根目录 = **`frontend`**，则首页即 **`frontend/index.html`**。  
- 部署后请**重新部署一次**并**强刷/无痕**访问，避免 CDN 或浏览器缓存旧版。
