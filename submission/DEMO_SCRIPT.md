> Tip for reviewers: This demo is not about correctness of decisions, but about consistency enforced by memory recall.

# Demo 口播稿

**定位**：Decision Infrastructure / Organizational Memory

---

## 90 秒版

### 中文

Decision Memory，组织决策记忆，核心原则是 No Citation No Decision——无援引不决策。Round 1：访谈输入，生成 Evidence 和 Requirement。Round 2：CVR 低于 2%，证伪速度假设，Decision 打 FALSIFIED 标签，需求转向质量。Round 3：新访谈又提速度，系统通过 recall 命中 Round 2 的 FALSIFIED 决策，检测冲突，拒绝需求回退，维持演化一致性。Recall 影响决策，才是 memory-driven，而非单纯 storage。

### English

Decision Memory, organizational decision memory. Core principle: No Citation, No Decision. Round 1: interview input, Evidence and Requirement. Round 2: CVR below 2%, falsifies speed hypothesis, Decision tagged FALSIFIED, pivots to quality. Round 3: new interview asks for speed again; system recalls, hits Round 2's FALSIFIED decision, detects conflict, rejects requirement revert, maintains evolution consistency. Recall drives the decision—that's memory-driven, not just storage.

---

## 3 分钟版

### 中文

Decision Memory 是 Decision Infrastructure，组织决策记忆系统。核心原则是 No Citation No Decision：每个 Decision 必须援引至少一个 Evidence 或 Outcome，否则 API 返回 400。

Demo 分三轮。Round 1 Intake：访谈说「要快」，系统生成 Evidence、Decision、Requirement v1。Round 2 Falsify：CVR 低于 2% 阈值，系统判定证伪速度假设，生成 Outcome 和带 FALSIFIED:true 标签的 Decision，需求转向质量优先。Round 3 Conflict Recall：新访谈再次强调「极速」，系统先 recall_by_tags 历史 Decision，命中 Round 2 的 FALSIFIED cell，检测到与新访谈冲突，拒绝需求回退到速度优先，Final Decision Rationale 写明「Rejected reverting to speed-focus; maintained quality-focus due to previous falsification」。因此拒绝回退，保持演化一致性。这是 Recall 影响决策，组织记忆约束新决策，而非仅存储后不参与决策。

### English

Decision Memory is Decision Infrastructure—organizational decision memory. Core principle: No Citation, No Decision. Every Decision must cite at least one Evidence or Outcome; otherwise the API returns 400.

The demo has three rounds. Round 1 Intake: interview says "we want speed." System creates Evidence, Decision, Requirement v1. Round 2 Falsify: CVR below 2% threshold, system falsifies speed hypothesis, creates Outcome and Decision tagged FALSIFIED:true, pivots requirement to quality-first. Round 3 Conflict Recall: new interview insists on "extreme speed." System recalls historical Decisions via recall_by_tags, hits Round 2's FALSIFIED cell, detects conflict with new input, rejects requirement revert to speed. Final Decision Rationale: "Rejected reverting to speed-focus; maintained quality-focus due to previous falsification." Thus rejects revert, maintains evolution consistency. Recall drives the decision—organizational memory constrains new decisions, not just storage that does not participate in decisions.
