# DataLens — Project Operating System

This file is the session contract. It governs scope, behavior, and context discipline for every Claude Code session working on this repository.

---

## Project Identity

**DataLens** is a command-line CSV data-quality analyzer. It reads a CSV file, profiles its contents, computes quality metrics, and produces an HTML report.

**This is a Claude Code learning experiment (Baseline 1).** The goal is to measure development process, not product ambition.

---

## Scope Boundaries

DataLens produces exactly these outputs:

1. Row count
2. Column count
3. Detected data types per column
4. Missing-value counts and percentages per column
5. Duplicate-row count
6. Unique-value counts per column
7. Basic numeric statistics (min, max, mean, median, std) for numeric columns
8. Composite data-quality score (0–100)
9. Self-contained HTML report with all findings

**Nothing beyond these 9 outputs is in scope.** Any request to add features, change outputs, or modify behavior must first be recorded in `docs/TASKS.md` as a future task and explicitly approved before implementation.

---

## Explicit Non-Goals

- No database
- No web server
- No REST API
- No authentication
- No Docker
- No cloud services
- No frontend framework
- No GUI
- No async I/O
- No configuration files beyond `pyproject.toml`
- No plugin system
- No multi-file output

---

## Module I/O Ownership

- **loader.py** — reads CSV file from disk, parses it, returns structured data
- **profiler.py** — receives structured data, returns per-column profile dicts
- **quality.py** — receives profiler output, returns composite score
- **report.py** — receives quality data, writes HTML report to disk
- **cli.py** — parses CLI arguments, orchestrates pipeline, prints summary to stdout

---

## Code Style

- Python 3.11+ syntax only
- No unnecessary abstractions, design patterns, or indirection
- Each module exposes one public function
- Plain Python data structures (lists, dicts, dataclasses) for inter-module communication
- No global state
- Docstrings on public functions only — one short line describing what, not how
- Type hints on public function signatures

---

## Context-Drift Pre-Flight Protocol

Before writing any code for any task, Claude must state the following in the response:

```
Pre-flight for T0X:
- Current task: <task name>
- Objective: <one sentence>
- Acceptance criteria: <list from docs/TASKS.md>
- Files expected to change: <list of file paths>
- Files that should not change: <all other project files>
- Relevant architectural constraints: <any from this document or ARCHITECTURE.md>
```

**Drift response rules:**
1. If implementation drifts outside stated acceptance criteria → stop, state the drift, ask for clarification
2. If a new feature idea emerges → write it to `docs/TASKS.md` as a future task, do not implement it
3. If an architecture change seems necessary → write an ADR entry to `docs/DECISIONS.md` first, wait for approval
4. Do not modify files outside the task's declared scope
5. Do not pre-implement future tasks
6. If the user asks for something outside scope, respond: "That's outside the current scope. I'll add it to `docs/TASKS.md` as a future task."

---

## Task Completion Reporting Protocol

After completing every implementation task (T01–T06), Claude must produce a structured **Task Completion Report** using the template in `docs/TASK_COMPLETION.md`.

**The report must include:**
1. Task summary (ID, title, status, estimated time, actual time, time variance)
2. Objective (restated from TASKS.md)
3. What Changed (system capability before and after, not filenames)
4. Files Changed (created, modified, deleted, unexpected)
5. Lines Changed (added, removed, net)
6. Dependencies (added, removed, changes in pyproject.toml)
7. Acceptance Criteria (pass/fail per criterion from TASKS.md)
8. Tests (test names, results, first-run result, commands run)
9. Architecture Impact (did module boundaries or data flow change?)
10. Decisions Made (new ADRs if any)
11. Context Drift (classification: NONE / MINOR / MAJOR, with incident descriptions)
12. Git Diff Summary (files added/modified/deleted, lines added/removed, unexpected changes)
13. Git Checkpoint (commit message and hash)
14. Human Review Required (explicit prompt for human approval before next task)
15. Learning Notes (what the learner should understand from this task)

**Context Drift classification:**
- **NONE** — implementation stayed within acceptance criteria, no scope additions
- **MINOR** — small scope additions or file edits outside task scope that were corrected
- **MAJOR** — significant scope additions or architecture changes attempted without approval

**After producing the report, Claude must STOP and wait for human approval before starting the next task.** Claude must NOT automatically proceed to the next task.

---

## Session Discipline

- Every session begins by reading `docs/SESSION_LOG.md` to understand current state
- Every session ends by writing a new SESSION_LOG.md entry
- One task at a time. Complete current task fully before starting the next.
- Every completed task gets a git checkpoint before moving on.
- No unrelated file edits within a task.

---

## Git Workflow

- Single branch `main`
- One commit per completed task
- Commit message: `feat(T0X): <title>` for implementation, `chore(T0X): <title>` for setup
- No force-push, no history rewrite

---

## Experiment Context

This repository is Baseline 1 (vanilla Claude Code). A separate, independent repository will run Baseline 2 (Claude Code with optimization plugins). Both start from equivalent T00 states. See `docs/EXPERIMENT.md` for full protocol.
