# Research OS v1.1: BC 双端「有限规模增长」系统

这是一个专为 BC 双端业务设计的「有限规模增长」研究交付系统，支持全链路 Traceable 监控与 Human-in-the-loop 审批。

---

## 🚀 紧急上线部署 (ECS 公网直连模式)

**放弃 Cloudflare Tunnel，直接通过 ECS 公网 IP 访问。**

### 1. 后端部署 (阿里云 ECS)
**在 ECS 上执行以下命令：**
```bash
# 1. 克隆仓库
git clone https://github.com/MyraWang0406/UserResearchAgent.git
cd UserResearchAgent

# 2. 启动容器 (已映射 0.0.0.0:8000)
docker-compose up -d
```

### 2. 安全组配置 (阿里云控制台)
请务必在阿里云 ECS 安全组中开放以下端口：
- **协议**: TCP
- **端口范围**: `8000/8000`
- **授权对象**: `0.0.0.0/0` (若需限制，请填入您的本地公网 IP)

### 3. 前端部署 (Cloudflare Pages)
1. 登录 Cloudflare 控制台 -> **Workers & Pages** -> **Create application** -> **Pages**。
2. 连接本仓库，设置如下：
   - **Build command**: (留空)
   - **Build output directory**: `frontend`
3. 部署完成后，访问 Pages 域名，点击右上角 **⚙️ 配置**：
   - **API Base**: 填写 `http://47.101.155.238:8000`
   - **API Key**: 填写 `admin123` (默认)

---

## ✅ 验证命令 (本地电脑执行)

请在您自己的电脑终端执行以下命令，验证 ECS 是否可达：

### 1. 健康检查
```bash
curl -i http://47.101.155.238:8000/health
```

### 2. 鉴权测试 (Ping)
```bash
curl -i http://47.101.155.238:8000/ping -H "X-API-Key: admin123"
```

### 3. 业务接口测试 (BC 工作流)
```bash
curl -X POST http://47.101.155.238:8000/api/v1/bc_growth_research \
     -H "Content-Type: application/json" \
     -H "X-API-Key: admin123" \
     -d '{"biz_stage": "0-1", "core_bottleneck": "转化率低"}'
```

---

## 🧠 业务逻辑：有限规模增长
系统根据 **Solution & CS Intake** 自动分流研究策略：
- **0–1**: 强痛点定性（挖掘不买理由）
- **1–10**: 成交 vs 流失（关键行为差异）
- **10–100**: 分层抽样（验证渠道效率）

**交付 5 件套产物：**
1. 增长问题树 (Problem Tree)
2. 研究包 (Research Kit)
3. 洞察卡片 (Insight Cards)
4. 增长排期 (Roadmap)
5. 管理层报告 (Management Report)

---

## 🛠️ 未来迁移步骤 (恢复标准架构)
1. **前端**: API Base 改为 Workers 域名。
2. **Workers**: 增加鉴权、限流与 Job 编排逻辑。
3. **ECS**: 安全组仅允许 Workers 来源访问，不再暴露公网。
