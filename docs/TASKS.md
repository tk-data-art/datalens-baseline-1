# DataLens — Tasks

> **Completion reports:** After every completed task (T01–T06), a Task Completion Report must be produced using the template in `docs/TASK_COMPLETION.md`. Claude must STOP after producing the report and wait for human approval before starting the next task.

---

## Live Progress Tracker

| ID | Title | Status | Est. | Actual | Tests | Context Drift | Git Commit |
|---|---|---|---|---|---|---|---|
| T00 | Project Operating System | Complete | 110 min | ~15 min | N/A | NONE | `77ad371` |
| T01 | loader.py — CSV reading and parsing | Complete (corrective) | 35 min | ~25 min | 7/7 pass | NONE | `f28a620` + corrective |
| T02 | profiler.py — per-column profiling | Complete | 40 min | ~15 min | 5/5 pass | NONE | `d7915a4`, `2fc77f2` |
| T03 | quality.py — composite quality score | Complete | 30 min | ~20 min | 9/9 pass | NONE | `b23442c` |
| T04 | report.py — HTML report generation | Complete | 40 min | ~25 min | 5/5 pass | NONE | `3149a9e` |
| T05 | cli.py — CLI entry point | Complete | 30 min | ~20 min | 3/3 pass | NONE | `{pending}` |
| T06 | Final review and polish | Complete | 130 min | ~90 min | 29/29 pass | NONE | — |

**Overall completion:** 7/7 tasks complete (100%) | T06 complete

**Completed tasks:** T00, T01, T02, T03, T04, T05, T06

**Current task:** None (awaiting human approval to create final Git tag)

**Remaining tasks:** None

**Estimated remaining time:** 0 minutes

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
- [x] 6 fixture CSV files exist in `tests/fixtures/` and are valid CSV

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
2. `test_loader.py` passes (7 tests after corrective pass)
3. `docs/TASKS.md` updated (T01 marked complete)
4. `docs/SESSION_LOG.md` updated
5. `docs/CHANGELOG.md` entry written
6. Git checkpoint: `feat(T01): CSV loader module` (original) + `fix(T01): add explicit quoted-comma fixture and expand test coverage` (corrective)

---

## T02 — profiler.py: Per-Column Profiling

**Objective:** Implement `profiler.py` to compute per-column statistics from loaded CSV data.

**Dependencies:** T01 complete

**Unassigned product requirement:** "duplicate-row count" is one of the 9 product outputs but is not assigned to any task. This must be resolved before the task that owns it (likely T05 cli.py or T04 report.py). Do not implement duplicate counting in T02.

**Acceptance criteria:**
- [ ] `profiler.py` has a public function `profile(rows, column_names)` returning `list[dict]`
- [ ] Per-column output includes: `name`, `type` (integer/float/string/mixed), `missing_count`, `missing_pct`, `unique_count`
- [ ] Numeric columns include: `min`, `max`, `mean`, `median`, `std`
- [ ] Correctly profiles all 6 fixture files
- [ ] Handles empty columns (all missing) without crashing
- [ ] All 5 `test_profiler.py` tests pass

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_profiler.py` passes (5 tests)
3. `docs/TASKS.md` updated (T02 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T02): column profiler module`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T03

---

## T03 — quality.py: Composite Quality Score

**Objective:** Implement `quality.py` to aggregate profiler output into a composite 0–100 quality score.

**Dependencies:** T02 complete

**Scoring contract:**

```
completeness = 1 - (missing_pct / 100)

type_consistency:
    integer, float, string → 1.0
    mixed → 0.5

distinctness:
    min(unique_count / total_rows, 1.0)
    when total_rows > 0
    (educational baseline metric — not a universal quality measure)

column_score =
    0.50 × completeness
  + 0.30 × type_consistency
  + 0.20 × distinctness

composite_score =
    mean(column_scores) × 100
```

**Boundary conditions:**
- If `total_rows == 0`: `composite_score = 0.0`, `column_scores = []`
- All scores are floats in range [0, 100]

**Result structure (plain dict, no class):**
```python
{
    "composite_score": float,
    "column_scores": [
        {"name": str, "score": float}
    ]
}
```

**Formula validation (pre-computed expected scores):**
- clean_simple.csv (5 rows): composite_score = 96.0
- missing_values.csv (6 rows): composite_score = 81.6667
- mixed_types.csv (6 rows): composite_score = 89.0
- edge_empty.csv (0 rows): composite_score = 0.0

**API:** `compute_score(profiles: list[dict], total_rows: int) -> dict`

**Acceptance criteria:**
- [x] `quality.py` has a public function `compute_score(profiles, total_rows)` returning `dict`
- [x] Returned dict has keys `composite_score` (float 0–100) and `column_scores` (list of dicts with `name` and `score`)
- [x] Composite score is a float in range [0, 100]
- [x] A completely clean dataset (clean_simple.csv) scores >= 90
- [x] A dataset containing missing values scores lower than an otherwise equivalent complete dataset
- [x] Score computation is deterministic (same input → same output)
- [x] Edge case: empty dataset (total_rows=0) returns composite_score=0.0
- [x] All 9 `test_quality.py` tests pass

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_quality.py` passes (9 tests)
3. `docs/TASKS.md` updated (T03 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T03): quality score module`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T04

---

## T04 — report.py: HTML Report Generation

**Objective:** Implement `report.py` to generate a self-contained HTML report from profiling and scoring data.

**Dependencies:** T03 complete

**API contract:**
```python
def generate(
    profiles: list[dict],
    result: dict,
    row_count: int,
    duplicate_row_count: int,
    output_path: str,
) -> None
```

**Data ownership:** report.py is a renderer only. It does not parse CSV, profile data, compute quality scores, or detect duplicates. `row_count` comes from loader, `duplicate_row_count` will be computed by cli.py.

**Templating:** jinja2 `Environment(autoescape=True)` with an inline template string. No separate template file. All CSV-derived values are auto-escaped.

**Styling:** Minimal inline CSS — readable typography, section headings, table borders, padding, readable score display. No JavaScript, no responsive frameworks, no themes, no progress bars, no animations, no external CSS, no external assets.

**Quality score display:** "Quality Score: X / 100" with a compact per-column score breakdown within the same section.

**Required report sections/content:**
1. Row count
2. Column count
3. Duplicate-row count
4. Detected type per column (data types table)
5. Missing count and percentage per column (missing-value table)
6. Unique/distinct count per column
7. Numeric statistics (min, max, mean, median, std) — numeric columns only
8. Composite quality score (0–100)
9. Compact per-column score breakdown
10. Self-contained valid HTML

**Edge cases:**
- `edge_empty.csv` has 0 data rows + header columns — report should show row_count=0, column_count=N (number of headers), empty data tables, score=0.0
- Direct 0-row/0-column input (if passed in tests): report with zeros across all metrics
- CSV-derived values with HTML-special characters (`<`, `>`, `&`, `"`) must be escaped

**Long values:** No custom truncation. Normal browser/CSS text wrapping.

**Acceptance criteria:**
- [x] `report.py` has a public function `generate(profiles, result, row_count, duplicate_row_count, output_path)` that writes an HTML file
- [x] Output file exists at the specified path after the function returns
- [x] HTML contains all required sections: row count, column count, duplicate-row count, data types table, missing-value table with percentages, unique-value counts, numeric statistics, quality score display, per-column score breakdown
- [x] HTML is valid and readable in a browser (DOCTYPE, proper HTML structure, inline CSS)
- [x] HTML-escapes CSV-derived values (test with `<`, `>`, `&`, `"` characters)
- [x] All 5 `test_report.py` tests pass

**Estimated time:** 40 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_report.py` passes (5 tests)
3. `docs/TASKS.md` updated (T04 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T04): HTML report generator`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T05

---

## T05 — cli.py: CLI Entry Point

**Objective:** Implement `cli.py` as the command-line entry point that orchestrates the full pipeline. cli.py is an orchestrator only — it calls existing modules in sequence and does not duplicate their logic.

**Dependencies:** T04 complete

**Architecture:** cli.py must only orchestrate: loader → profiler → quality → duplicate counting → report. It must not reimplement CSV parsing, profiling, quality scoring, or HTML rendering.

**Command syntax:**
```
datalens <csv_path>
```

**Arguments:**
- `csv_path` (positional, required) — path to the CSV file to analyze

No options, no flags, no subcommands.

**Output path:** `reports/<input filename stem>.html` (e.g., `datalens data/clean.csv` → `reports/clean.html`)

**CLI stdout summary (one line):**
```
Report written to: reports/<stem>.html | Rows: N | Columns: N | Quality Score: X / 100
```

**Duplicate-row detection:**
- Two rows are duplicates when they have exactly the same column/value pairs
- Implementation: `tuple(sorted(row.items()))` — column dictionary ordering does not affect detection
- Not supported: subset/key-based duplicates, fuzzy matching, semantic matching
- Computed in cli.py from raw rows returned by `load_csv()`

**Scalability:** DataLens processes CSV data in memory and is intended for small-to-medium CSV files that comfortably fit in memory. No artificial row/column limit is imposed.

**Error handling:**
- Missing file → print error to stderr, exit 1
- Malformed CSV → print error to stderr, exit 1
- Permission errors → print error to stderr, exit 1

**Exit codes:**
- `0` — success, report generated
- `1` — failure (any error)

**Acceptance criteria:**
- [x] `cli.py` provides `main()` callable via `python -m datalens <path>` or the `pyproject.toml` scripts entry
- [x] Accepts a single positional argument: path to a CSV file
- [x] Runs the full pipeline: load → profile → score → duplicate count → report
- [x] Prints a one-line summary to stdout: report path, row count, column count, quality score
- [x] Writes the HTML report to `reports/<stem>.html`
- [x] Exits with code 0 on success, non-zero on failure
- [x] All 3 `test_cli.py` tests pass (2 unit + 1 integration)

**Testing strategy:**
- 2 unit tests call `main()` directly with controlled inputs, capturing stdout/stderr and exit codes
- 1 integration test invokes the actual CLI entry point through `python -m datalens <csv_path>` (subprocess) to verify the real user-facing path
- Integration test runs the full pipeline on a fixture file, asserts the report exists, stdout contains expected summary, exit code is 0

**Estimated time:** 30 minutes

**Definition of Done:**
1. All acceptance criteria met
2. `test_cli.py` passes (3 tests: 2 unit + 1 integration)
3. `docs/TASKS.md` updated (T05 marked complete)
4. `docs/CHANGELOG.md` entry written
5. Git checkpoint: `feat(T05): CLI entry point`
6. Task Completion Report produced via `docs/TASK_COMPLETION.md` template
7. Human approval received before proceeding to T06

---

## T06 — Final Review and Polish

**Objective:** Verify the complete project meets all requirements and is ready for experiment comparison. Run scalability benchmarks, produce experiment results, and finalize Baseline 1.

**Dependencies:** T05 complete

**Benchmark methodology:**
- Benchmark data generated by `benchmarks/benchmark_generator.py` with `random.seed(42)`
- Generated CSVs stored in `benchmarks/data/` (gitignored — not committed)
- Reproducibility: deterministic generator + seed + dimensions + environment metadata + Git commit
- Each benchmark runs once; results are observational, not statistical estimates
- Peak memory measured via `/usr/bin/time -l` (macOS), normalized to MB
- Environment metadata recorded: machine, CPU architecture, macOS version, Python version, Git commit
- Timeouts: 10k×20: 60s, 100k×20: 120s, 1M×20: 300s, 100k×100: 300s
- Failed benchmarks recorded as experimental findings — application code not modified

**Benchmark datasets (not committed):**
- `benchmarks/data/benchmark_10k_20.csv` — 10,000 rows × 20 columns
- `benchmarks/data/benchmark_100k_20.csv` — 100,000 rows × 20 columns
- `benchmarks/data/benchmark_1m_20.csv` — 1,000,000 rows × 20 columns
- `benchmarks/data/benchmark_100k_100.csv` — 100,000 rows × 100 columns

**Experiment results document:**
- `docs/EXPERIMENT_RESULTS.md` — Baseline 1 implementation summary, test results, development process, context drift, corrective passes, pre-flight decisions, scalability benchmark table, limitations, environment metadata, Git commit used for benchmarking
- Sections for Baseline 2 and comparative analysis reserved but not populated

**Acceptance criteria:**
- [x] Full `pytest` suite passes (29/29)
- [x] README.md contains realistic example run with fixture output
- [x] docs/CHANGELOG.md has entries for all completed tasks (T00–T05)
- [x] docs/SESSION_LOG.md has final entry
- [x] No unused imports or dead code visible on review
- [x] pyproject.toml installs cleanly (`pip install -e .`)
- [x] benchmarks/benchmark_generator.py exists and is functional
- [x] benchmarks/data/ is gitignored
- [x] All 4 benchmarks run and results recorded
- [x] docs/EXPERIMENT_RESULTS.md written with Baseline 1 metrics

**Estimated time:** 130 minutes

**Definition of Done:**
1. All acceptance criteria met
2. Full test suite green
3. Benchmark data generated and results recorded
4. docs/EXPERIMENT_RESULTS.md written
5. docs/TASKS.md updated (T06 marked complete)
6. docs/SESSION_LOG.md final entry written
7. docs/CHANGELOG.md entry written
8. Git checkpoint: `chore(T06): final review and polish`
9. Human approval received before push/tag
