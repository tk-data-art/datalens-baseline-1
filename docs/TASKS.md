# DataLens — Tasks

> **Completion reports:** After every completed task (T01–T06), a Task Completion Report must be produced using the template in `docs/TASK_COMPLETION.md`. Claude must STOP after producing the report and wait for human approval before starting the next task.

---

## Live Progress Tracker

| ID | Title | Status | Est. | Actual | Tests | Context Drift | Git Commit |
|---|---|---|---|---|---|---|---|
| T00 | Project Operating System | Complete | 110 min | ~15 min | N/A | NONE | `77ad371` |
| T01 | loader.py — CSV reading and parsing | Complete | 35 min | ~15 min | 4/4 pass | NONE | `{pending}` |
| T02 | profiler.py — per-column profiling | Pending | 40 min | — | — | — | — |
| T03 | quality.py — composite quality score | Pending | 30 min | — | — | — | — |
| T04 | report.py — HTML report generation | Pending | 40 min | — | — | — | — |
| T05 | cli.py — CLI entry point | Pending | 30 min | — | — | — | — |
| T06 | Final review and polish | Pending | 25 min | — | — | — | — |

**Overall completion:** 2/7 tasks complete (28%) | Implementation started

**Completed tasks:** T00, T01

**Current task:** None (awaiting human approval to begin T02)

**Remaining tasks:** T01, T02, T03, T04, T05, T06

**Estimated remaining time:** 200 minutes

---

## Task Index

| ID | Title | Est. | Status |
|---|---|---|---|
| T00 | Project Operating System | 110 min | Complete |
| T01 | loader.py — CSV reading and parsing | 35 min | Pending |
| T02 | profiler.py — per-column profiling | 40 min | Pending |
| T03 | quality.py — composite quality score | 30 min | Pending |
| T04 | report.py — HTML report generation | 40 min | Pending |
| T05 | cli.py — CLI entry point | 30 min | Pending |
| T06 | Final review and polish | 25 min | Pending |

---

## T00 — Project Operating System

**Objective:** Establish the project's operating system: documentation, scaffolding, fixtures, and experiment protocol. No application implementation code.

**Dependencies:** None

**Acceptance criteria:**
- [x] All project directories exist (`src/datalens/`, `tests/`, `tests/fixtures/`, `docs/`, `reports/`)
- [x] `pyproject.toml` defines project metadata, `pytest` as dev dependency, and `[project.scripts]` entry
- [x] `src/datalens/__init__.py` exists (empty)
- [x] `CLAUDE.md` contains: scope boundaries, context-drift pre-flight protocol, code style, session discipline rules
- [x] `docs/ARCHITECTURE.md` contains: module map, data flow, I/O ownership, dependency rationale
- [x] `docs/TASKS.md` contains: all tasks (T00–T06) with objective, dependencies, acceptance criteria, estimated time, DoD
- [x] `docs/DECISIONS.md` contains: initial ADR entries for all architecture choices
- [x] `docs/EXPERIMENT.md` contains: experiment objective, baseline definitions, controlled variables, measured variables, hypotheses, comparison methodology
- [x] `docs/SESSION_LOG.md` contains: header structure and initial entry
- [x] `docs/CHANGELOG.md` contains: header and initial entry
- [x] `README.md` contains: project description, install instructions, run instructions
- [x] 5 fixture CSV files exist in `tests/fixtures/` and are valid CSV

**Estimated time:** 110 minutes

**Definition of Done:**
1. All files listed above exist and are non-empty
2. `pyproject.toml` is valid TOML
3. Fixture CSVs are valid and parseable
4. All documentation files are internally consistent
5. SESSION_LOG.md initial entry written
6. CHANGELOG.md initial entry written
7. Git checkpoint created: `chore(T00): project operating system`

---

## T01 — loader.py: CSV Reading and Parsing

**Objective:** Implement `loader.py` to read CSV files from disk, parse them with the stdlib `csv` module, and return structured data.

**Dependencies:** T00 complete

**Acceptance criteria:**
- [ ] `loader.py` has a public function `load_csv(path: str)` that returns `(rows, column_names, row_count)`
- [ ] Returns `rows` as `list[dict]`, `column_names` as `list[str]`, `row_count` as `int`
- [ ] Correctly parses all 5 fixture files without error
- [ ] Handles quoted fields with embedded commas
- [ ] Handles empty CSV (header only, 0 data rows) without crashing
- [ ] Raises a clear error for a file that does not exist
- [ ] All 4 `test_loader.py` tests pass

**Estimated time:** 35 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_loader.py` passes (4 tests)
3. `docs/TASKS.md` updated (T01 marked complete)
4. `docs/SESSION_LOG.md` updated if session boundary crossed
5. `docs/CHANGELOG.md` entry written
6. Git checkpoint: `feat(T01): CSV loader module`

---

## T02 — profiler.py: Per-Column Profiling

**Objective:** Implement `profiler.py` to compute per-column statistics from loaded CSV data.

**Dependencies:** T01 complete

**Acceptance criteria:**
- [ ] `profiler.py` has a public function `profile(rows, column_names)` returning `list[ColumnProfile]`
- [ ] Per-column output includes: `name`, `type` (integer/float/string/mixed), `missing_count`, `missing_pct`, `unique_count`
- [ ] Numeric columns include: `min`, `max`, `mean`, `median`, `std`
- [ ] Correctly profiles all 5 fixture files
- [ ] Handles empty columns (all missing) without crashing
- [ ] All 5 `test_profiler.py` tests pass

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_profiler.py` passes (5 tests)
3. `docs/TASKS.md` updated (T02 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T02): column profiler module`

---

## T03 — quality.py: Composite Quality Score

**Objective:** Implement `quality.py` to aggregate profiler output into a composite 0–100 quality score.

**Dependencies:** T02 complete

**Acceptance criteria:**
- [ ] `quality.py` has a public function `compute_score(profiles)` returning `QualityResult`
- [ ] Composite score is a float in range [0, 100]
- [ ] A completely clean dataset (clean_simple.csv) scores >= 90
- [ ] A dataset with significant missing values scores lower than a clean dataset
- [ ] Score computation is deterministic (same input → same output)
- [ ] All 3 `test_quality.py` tests pass

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_quality.py` passes (3 tests)
3. `docs/TASKS.md` updated (T03 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T03): quality score module`

---

## T04 — report.py: HTML Report Generation

**Objective:** Implement `report.py` to generate a self-contained HTML report from quality results.

**Dependencies:** T03 complete

**Acceptance criteria:**
- [ ] `report.py` has a public function `generate(result, output_path)` that writes an HTML file
- [ ] Output file exists at the specified path after the function returns
- [ ] HTML contains all 9 required sections: row count, column count, data types table, missing-value table with percentages, duplicate-row count, unique-value counts, numeric statistics table, quality score display
- [ ] HTML is readable in a browser (valid HTML structure)
- [ ] All 3 `test_report.py` tests pass

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_report.py` passes (3 tests)
3. `docs/TASKS.md` updated (T04 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T04): HTML report generator`

---

## T05 — cli.py: CLI Entry Point

**Objective:** Implement `cli.py` as the command-line entry point that orchestrates the full pipeline.

**Dependencies:** T04 complete

**Acceptance criteria:**
- [ ] `cli.py` provides `main()` callable via `python -m datalens <path>` or the `pyproject.toml` scripts entry
- [ ] Accepts a single positional argument: path to a CSV file
- [ ] Runs the full pipeline: load → profile → score → report
- [ ] Prints a one-line summary to stdout (file path, rows, columns, quality score)
- [ ] Writes the HTML report to the `reports/` directory
- [ ] Exits with code 0 on success, non-zero on failure (missing file, parse error)
- [ ] All 3 `test_cli.py` tests pass (2 unit + 1 integration)

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_cli.py` passes (3 tests)
3. `docs/TASKS.md` updated (T05 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T05): CLI entry point`

---

## T06 — Final Review and Polish

**Objective:** Verify the complete project meets all requirements and is ready for experiment comparison.

**Dependencies:** T05 complete

**Acceptance criteria:**
- [ ] Full `pytest` suite passes (all tests across all modules)
- [ ] `README.md` contains realistic example run with fixture output
- [ ] `docs/CHANGELOG.md` has entries for all completed tasks (T00–T05)
- [ ] `docs/SESSION_LOG.md` reflects the final state
- [ ] No unused imports or dead code visible on review
- [ ] `pyproject.toml` installs cleanly (`pip install -e .`)

**Estimated time:** 25 minutes

**Definition of Done:**
1. All acceptance criteria met
2. Full test suite green
3. `docs/TASKS.md` updated (T06 marked complete)
4. `docs/SESSION_LOG.md` final entry written
5. `docs/CHANGELOG.md` entry written
6. Git checkpoint: `chore(T06): final review and polish`
7. Final commit tagged
