# DataLens — Task Completion Audit Template

This document defines the standard completion report that must be produced after every implementation task (T01–T06) before the next task begins.

---

## Task Completion Report — T0X: {Title}

**Generated:** {YYYY-MM-DD HH:MM}
**Baseline:** Baseline 1 (vanilla Claude Code)

---

### 1. Task Summary

| Field | Value |
|---|---|
| Task ID | T0X |
| Title | {task title} |
| Status | Complete / Blocked / Partial |
| Estimated Time | {minutes} |
| Actual Wall-Clock Time | {minutes} |
| Time Variance | {+X min / -X min / on target} |

---

### 2. Objective

{One-sentence restatement of the task objective from TASKS.md}

---

### 3. What Changed

**Before this task:** {Description of the system state before this task — what capabilities existed, what was missing}

**After this task:** {Description of the system state now — what new capabilities exist, what can be done that couldn't be done before}

*This section describes the system capability change, not the filenames changed.*

---

### 4. Files Changed

**Files created:**
- `path/to/file.py` — {purpose}

**Files modified:**
- `path/to/file.py` — {what changed and why}

**Files deleted:**
- (none)

**Unexpected files modified:**
- (none, or list with explanation)

---

### 5. Lines Changed

| Metric | Value |
|---|---|
| Lines added | {count} |
| Lines removed | {count} |
| Net change | {+X / -X} |

---

### 6. Dependencies

**Added:**
- (none, or list new dependencies with version)

**Removed:**
- (none)

**Dependency changes in `pyproject.toml`:**
- (none, or describe changes)

---

### 7. Acceptance Criteria

| Criterion | Result |
|---|---|
| {criterion 1 from TASKS.md} | Pass / Fail |
| {criterion 2} | Pass / Fail |
| {criterion 3} | Pass / Fail |
| ... | ... |

**Overall:** {All pass / N/M pass}

---

### 8. Tests

| Test | Result |
|---|---|
| {test name 1} | Pass / Fail |
| {test name 2} | Pass / Fail |
| ... | ... |

**First-run test result:** {All pass on first run / N/M passed, Y failed, Z required fixes}

**Test commands run:**
```bash
pytest tests/test_{module}.py -v
```

---

### 9. Architecture Impact

{Did this task change any module boundaries, data flow, or I/O ownership? If yes, describe. If no, state "No architecture changes."}

If architecture changed, reference the ADR entry in `docs/DECISIONS.md`.

---

### 10. Decisions Made

| Decision | ADR Reference |
|---|---|
| {decision description} | ADR-00X (if new) |
| (none new) | — |

---

### 11. Context Drift

**Classification:** NONE / MINOR / MAJOR

| Incident | Description | Severity | Resolution |
|---|---|---|---|
| {description of drift} | {what happened} | MINOR/MAJOR | {how it was resolved} |
| (none) | — | — | — |

**Total drift incidents:** {count}

---

### 12. Git Diff Summary

```
{git diff --stat output}
```

| Metric | Value |
|---|---|
| Files added | {count} |
| Files modified | {count} |
| Files deleted | {count} |
| Lines added | {count} |
| Lines removed | {count} |
| Unexpected changes | {count} (describe if any) |

---

### 13. Git Checkpoint

**Commit message:** `feat(T0X): {task title}`
**Commit hash:** `{hash}`
**Branch:** main

---

### 14. Human Review Required

**Before proceeding to the next task, please review:**

1. Do the acceptance criteria match the original intent?
2. Are there any scope additions that should be moved to `docs/TASKS.md` as future tasks?
3. Is the implementation consistent with `docs/ARCHITECTURE.md`?
4. Are the test results acceptable?
5. Any feedback or direction changes before T0Y?

**Approval to proceed:** [Pending human approval]

---

### 15. Learning Notes

{What should the learner understand from completing this task? Key patterns, pitfalls, insights about the codebase or the development process.}

---

*This report was generated as part of the DataLens experimental protocol. See `docs/EXPERIMENT.md` for details.*
