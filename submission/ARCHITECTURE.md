# Decision Memory Architecture

## Core Idea

**Memory must affect future decisions.** If recall does not constrain new decisions, it is storage, not memory.

## Memory Cell Types

| Type | Role |
|------|------|
| Context | Domain/stage/growth context (optional) |
| Evidence | Interview summary, metric snapshot |
| Decision | rationale + decision_type; **must have citations** |
| Requirement | scope_summary + version; must derive_from Decision |
| Outcome | metrics_delta + verdict (SUPPORT/FALSIFY) |

## Mandatory Citation Rule

- Decision with empty `citations` → API returns **400**
- Requirement with empty `derived_from` → API returns **400**

## Recall-Driven Evolution

Round 3 depends on Round 2 falsification:

1. `recall_by_tags({type: "decision", domain, stage, growth})` fetches historical Decisions
2. Filter `falsified_decisions = [c for c in history if "FALSIFIED:true" in c.tags]`
3. If new interview conflicts with falsified rationale → reject revert, rationale states "due to previous falsification"

Without this recall step, Round 3 would adopt the new interview and revert the requirement—wrong.

## Causal Graph

```
Evidence ──cites──> Decision ──cites──> Requirement
Outcome   ──cites──> Decision
```

## Why This Is Not Logging

Logging records events; it does not constrain future actions. Here, recall **feeds into** the decision logic: Round 3's rationale is explicitly shaped by Round 2's falsified Decision. That prevents organizational decision revert and repeated mistakes.
