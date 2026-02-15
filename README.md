Decision Memory is an organizational infrastructure where historical evidence and falsification actively constrain future decisions.

决策记忆是一种组织级基础设施，历史证据与被证伪结论会主动约束未来决策。

# Decision Memory / 组织决策记忆

**Memory Genesis Track 1** · No citation, no decision. Traceable decisions, evolution consistency, organizational memory.

**Memory Genesis Track 1 参赛项目** · 强制「无援引不决策」，实现决策可追溯、需求演化一致性、组织记忆沉淀。

> This is not a static UI demo.
> The system enforces decision consistency through memory recall, citation, and falsification.
> Decisions without historical citation are explicitly rejected (400).

> 这不是一个静态页面演示。
> 系统通过记忆回溯、证据援引与证伪机制，强制保证决策一致性。
> 任何没有历史证据援引的决策都会被系统显式拒绝（400）。

## Proof: Memory Influences Decisions

**Purpose:** Prove that recall actually affects new decisions—not just storage. Three hard evidences from `demo_outputs/demo.log`, cross-verifiable.

**本区块目的：** 证明 recall 实际影响了新决策，而非仅存储。以下三条硬证据来自 `demo_outputs/demo.log`，可交叉验证。

1. **RecallHits Found: 2 cells** (at least one Decision tagged `FALSIFIED:true`)
   **RecallHits Found: 2 cells**（其中至少一条为 `FALSIFIED:true` 的 Decision）
   ```
   RecallHits Found: 2 cells
     - [Hit] ID: decision_1771119630.400876 | Tags: [..., 'FALSIFIED:true', 'type:decision'] | Summary: Metrics FALSIFY previous speed hypothesis....
     - [Hit] ID: decision_1771119630.39957 | Tags: [..., 'type:decision'] | Summary: Initial requirement generation based on interview....
   ```

2. **Conflict Reason** (explicitly from Round 2)
   **Conflict Reason**（明确指出来自 Round 2）
   ```
   Conflict Reason: Detected contradiction with Round 2 Falsification (Decision ID: decision_1771119630.400876)
   ```

3. **Final Decision Rationale** (explicitly rejects requirement rollback)
   **Final Decision Rationale**（明确拒绝需求回退）
   ```
   Final Decision Rationale: Conflict Detected: Rejected reverting to speed-focus; maintained quality-focus due to previous falsification.
   ```

## Why This Matters / 为什么需要

- **Traceable decisions:** Every decision must cite evidence, forming a complete chain.
  **决策可追溯：** 每个决策必须援引证据，形成完整溯源链。
- **Evolution consistency:** Falsified hypotheses are not easily overturned by new interviews; recall affects decisions.
  **需求演化一致性：** 证伪后的假设不会被新访谈轻易推翻，Recall 影响决策。
- **Organizational memory:** Evidence, decisions, requirements, outcomes stored uniformly; supports recall and conflict detection.
  **组织记忆：** 证据、决策、需求、结果统一存储，支持回溯与冲突检测。

## Demo (3 Rounds) / Demo 说明（3 轮）

| Round | Type | Description |
|------|------|--------------|
| **Round 1** | Intake | Interview → Evidence → Decision → Requirement v1 |
| **Round 2** | Falsify | CVR&lt;2% → Outcome → Decision(falsified) → Requirement v2 |
| **Round 3** | Conflict Recall | New interview mentions "speed" again → Recall historical decisions → Detect conflict with Round 2 falsification → Reject rollback, maintain quality-first |

**Core:** Round 3 recalls Round 2's falsified decision and constrains the final rationale. Organizational memory constrains new decisions.

**核心：** 第 3 轮 Recall 到第 2 轮证伪决策，影响最终 rationale，体现「组织记忆」约束新决策。

**Live Demo:** https://userinsightagent.myrawzm0406.online/

## How to judge it's memory-driven (not storage)

**Goal:** Let judges know what would go wrong without this memory layer.

**目标：** 让评委知道如果没有这一层 memory，这个系统会做错什么。

1. **Does Round 3's Decision explicitly reference Round 2's falsification Decision ID?**
   In this demo, `demo.log`'s Conflict Reason explicitly states `Decision ID: decision_1771119630.400876` (Round 2 falsified decision), rationale states "due to previous falsification." Without recall hitting that cell, this reference cannot be produced.
   **Round 3 的 Decision 是否显式引用 Round 2 的 falsification Decision ID？** 本 Demo 中，`demo.log` 的 Conflict Reason 明确写出 `Decision ID: decision_1771119630.400876`（即 Round 2 证伪决策），rationale 写明「due to previous falsification」。若未通过 recall 命中该 cell，则无法产生此引用。

2. **Without recall of Round 2's falsification, the system may adopt the new interview and roll back requirements.**
   When the new interview mentions "speed" again, if the system does not run `recall_by_tags` or filter `FALSIFIED:true`, it may directly adopt the new interview and roll back to speed-first. In that case, decisions do not depend on organizational memory—it is storage, not memory-driven.
   **若未 recall 到 Round 2 的证伪结论，系统可能直接采纳新访谈并回退需求。** 新访谈再次提「速度」时，若系统未执行 `recall_by_tags` 或未筛选 `FALSIFIED:true`，则可能直接采纳新访谈、回退到速度优先，此时决策不依赖组织记忆，仅为 storage 而非 memory-driven。

3. **This demo's implementation:**
   Uses `recall_by_tags({type: "decision", ...})` to fetch historical decisions, filters `FALSIFIED:true` cells, rejects rollback on conflict, rationale explicitly states "Rejected reverting to speed-focus; maintained quality-focus due to previous falsification."
   **本 Demo 的实现：** 通过 `recall_by_tags({type: "decision", ...})` 获取历史决策，筛选 `FALSIFIED:true` 的 cell，检测到与新访谈冲突时拒绝回退，rationale 明确说明「Rejected reverting to speed-focus; maintained quality-focus due to previous falsification」。

## Quick Start / 一键运行

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

## demo_outputs / 文件说明

| File | Description |
|------|-------------|
| `demo.log` | 3-round demo execution log |
| `graph.json` | Trace graph (nodes + edges) |
| `decisions.json` | All decision cells |
| `snapshots.json` | Requirement snapshots |

## GitHub Actions

CI runs `pytest -q` and produces `demo_outputs` artifact (demo.log, graph.json, decisions.json, snapshots.json).

CI 工作流会执行 `pytest -q` 并产出 `demo_outputs` artifact（含 demo.log、graph.json、decisions.json、snapshots.json）。

## Submission Materials / 参赛材料（submission/）

| File | Description |
|------|-------------|
| `submission/DEMO_SCRIPT.md` | 90s / 3min voiceover (EN/ZH) |
| `submission/ARCHITECTURE.md` | 1-page architecture |
| `submission/demo_outputs/` | Demo output copy; also downloadable from Actions artifact |
