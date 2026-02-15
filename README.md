Decision Memory is an organizational infrastructure where historical evidence and falsification actively constrain future decisions.

# Decision Memory / 组织决策记忆

**Memory Genesis Track 1 参赛项目** · 强制「无援引不决策」，实现决策可追溯、需求演化一致性、组织记忆沉淀。

> This is not a static UI demo.  
> The system enforces decision consistency through memory recall, citation, and falsification.  
> Decisions without historical citation are explicitly rejected (400).

## Proof: Memory Influences Decisions

本区块目的：**证明 recall 实际影响了新决策，而非仅存储**。以下三条硬证据来自 `demo_outputs/demo.log`，可交叉验证。

1. **RecallHits Found: 2 cells**（其中至少一条为 `FALSIFIED:true` 的 Decision）
   ```
   RecallHits Found: 2 cells
     - [Hit] ID: decision_1771119630.400876 | Tags: [..., 'FALSIFIED:true', 'type:decision'] | Summary: Metrics FALSIFY previous speed hypothesis....
     - [Hit] ID: decision_1771119630.39957 | Tags: [..., 'type:decision'] | Summary: Initial requirement generation based on interview....
   ```

2. **Conflict Reason**（明确指出来自 Round 2）
   ```
   Conflict Reason: Detected contradiction with Round 2 Falsification (Decision ID: decision_1771119630.400876)
   ```

3. **Final Decision Rationale**（明确拒绝需求回退）
   ```
   Final Decision Rationale: Conflict Detected: Rejected reverting to speed-focus; maintained quality-focus due to previous falsification.
   ```

## 为什么需要

- **决策可追溯**：每个决策必须援引证据，形成完整溯源链
- **需求演化一致性**：证伪后的假设不会被新访谈轻易推翻，Recall 影响决策
- **组织记忆**：证据、决策、需求、结果统一存储，支持回溯与冲突检测

## Demo 说明（3 轮）

| 轮次 | 类型 | 说明 |
|------|------|------|
| **Round 1** | Intake | 访谈输入 → Evidence → Decision → Requirement v1 |
| **Round 2** | Falsify | 指标 CVR&lt;2% → Outcome → Decision(证伪) → Requirement v2 |
| **Round 3** | Conflict Recall | 新访谈再次提「速度」→ Recall 历史决策 → 检测到与 Round 2 证伪冲突 → 拒绝回退，维持质量优先 |

**核心**：第 3 轮 Recall 到第 2 轮证伪决策，影响最终 rationale，体现「组织记忆」约束新决策。

**Live Demo:** https://userinsightagent.myrawzm0406.online/

## How to judge it's memory-driven (not storage)

**目标：让评委知道如果没有这一层 memory，这个系统会做错什么。**

1. **Round 3 的 Decision 是否显式引用 Round 2 的 falsification Decision ID**  
   本 Demo 中，`demo.log` 的 Conflict Reason 明确写出 `Decision ID: decision_1771119630.400876`（即 Round 2 证伪决策），rationale 写明「due to previous falsification」。若未通过 recall 命中该 cell，则无法产生此引用。

2. **若未 recall 到 Round 2 的证伪结论，系统可能直接采纳新访谈并回退需求**  
   新访谈再次提「速度」时，若系统未执行 `recall_by_tags` 或未筛选 `FALSIFIED:true`，则可能直接采纳新访谈、回退到速度优先，此时决策不依赖组织记忆，仅为 storage 而非 memory-driven。

3. **本 Demo 的实现**  
   通过 `recall_by_tags({type: "decision", ...})` 获取历史决策，筛选 `FALSIFIED:true` 的 cell，检测到与新访谈冲突时拒绝回退，rationale 明确说明「Rejected reverting to speed-focus; maintained quality-focus due to previous falsification」。

## 一键运行

### Windows (PowerShell)

```powershell
cd user_research_agent
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_demo.py
pytest -q
```

### Mac / Linux

```bash
cd user_research_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_demo.py
pytest -q
```

## demo_outputs 文件说明

| 文件 | 说明 |
|------|------|
| `demo.log` | 3 轮 Demo 执行日志 |
| `graph.json` | 溯源图谱（nodes + edges） |
| `decisions.json` | 所有决策 cell |
| `snapshots.json` | 需求快照（requirement 类型 cell） |

## GitHub Actions

CI 工作流会执行 `pytest -q` 并产出 `demo_outputs` artifact（含 demo.log、graph.json、decisions.json、snapshots.json）。

## 参赛材料（submission/）

| 文件 | 说明 |
|------|------|
| `submission/DEMO_SCRIPT.md` | 90 秒 / 3 分钟口播稿（中英） |
| `submission/ARCHITECTURE.md` | 1 页架构说明 |
| `submission/demo_outputs/` | demo 产出副本；亦可从 Actions artifact 下载 |
