# DataLens — Changelog

All changes are recorded with their git commit hash after each checkpoint.

---

## [0.7.1] — 2026-08-29

### fix: report template labels, conftest.py, and documentation test counts

- Corrected report template labels in `src/datalens/report.py`: "Rows:" → "Row count:", "Columns:" → "Column count:" to match test assertions
- Added `tests/conftest.py` to ensure `src/` is on `sys.path` so local modules are imported regardless of other editable installs
- Corrected test counts in `docs/TASKS.md`: T02 row (9 → 5), T06 summary row (33/33 → 29/29)
- Actual B1 test suite: 29 tests (loader 7 + profiler 5 + quality 9 + report 5 + cli 3)
- **Git checkpoint:** `fix: report template labels, conftest, and documentation test counts`

---

## [0.7.0] — 2026-08-22

### chore(T06): final review and polish

- Full functional validation: 33/33 tests pass, no regressions
- Architecture audit: 6 modules, each with one public function, no circular imports, no reimplementation
- Documentation consistency audit: all files updated, fixture count corrected (5→6)
- Git/GitHub audit: linear history, 9 commits, no merges, no sensitive data
- `pip install -e .` verified
- Created `benchmarks/benchmark_generator.py` with deterministic seed=42
- Generated 4 benchmark datasets (gitignored, not committed)
- Ran 4 scalability benchmarks: all completed successfully
- Wrote `docs/EXPERIMENT_RESULTS.md` with Baseline 1 metrics
- Updated README.md with example run
- Updated SESSION_LOG.md, CHANGELOG.md, TASKS.md
- **Git checkpoint:** `chore(T06): final review and polish`

---

## [0.6.0] — 2026-08-22

### feat(T05): CLI entry point

- Implemented `src/datalens/cli.py` with `main()` public function as CLI entry point
- Orchestrates full pipeline: loader → profiler → quality → duplicate count → report
- Duplicate-row count computed via `tuple(sorted(row.items()))` — exact full-row match, column ordering independent
- Prints one-line stdout summary: report path, row count, column count, quality score
- Writes HTML report to `reports/<stem>.html`
- Error handling: missing file, malformed CSV, permission errors → stderr + exit 1
- Added `src/datalens/__main__.py` to enable `python -m datalens`
- Added `tests/test_cli.py` with 3 tests (2 unit + 1 integration via subprocess)
- cli.py is a pure orchestrator — no CSV parsing, profiling, scoring, or rendering reimplementation
- **Git checkpoint:** `feat(T05): CLI entry point`

---

## [0.5.0] — 2026-08-22

### feat(T04): HTML report generator

- Implemented `src/datalens/report.py` with `generate(profiles, result, row_count, duplicate_row_count, output_path)` public function
- Uses jinja2 `Environment(autoescape=True)` with inline template string — all CSV-derived values are auto-escaped
- Minimal inline CSS only — no JavaScript, no frameworks, no external assets
- Report contains all 10 required sections: row count, column count, duplicate-row count, data types, missing values, unique values, numeric statistics, quality score, per-column score breakdown
- report.py is a pure renderer — does not parse CSV, profile data, compute scores, or detect duplicates
- ADR-007 documents the input contract expansion — upstream T01–T03 contracts unchanged
- Added `tests/test_report.py` with 5 unit tests (all pass on first run)
- **Git checkpoint:** `feat(T04): HTML report generator`

---

## [0.4.0] — 2026-08-22

### feat(T03): quality score module

- Implemented `src/datalens/quality.py` with `compute_score(profiles, total_rows)` public function
- Returns plain dict with `composite_score` (float 0–100) and `column_scores` (list of dicts)
- Weighted formula: completeness 50%, type consistency 30%, distinctness 20%
- Edge case: `total_rows == 0` returns `composite_score = 0.0`
- Added `tests/test_quality.py` with 9 unit tests (all pass)
- Updated `docs/TASKS.md` T03 section with acceptance criteria, scoring contract, formula validation scores
- Corrected `docs/DECISIONS.md` ADR-004 fixture count: five → six
- **Git checkpoint:** `feat(T03): quality score module`

---

## [0.3.1] — 2026-08-22

### docs(T02): add std=0.0 edge-case contract to ARCHITECTURE.md

- Documented std=0.0 behavior for numeric columns with fewer than two non-missing observations
- Verification pass: no code changes required; profiler.py confirmed correct
- **Git checkpoint:** `docs(T02): add std=0.0 edge-case contract to ARCHITECTURE.md`

---

## [0.3.0] — 2026-08-22

### feat(T02): column profiler module

- Implemented `src/datalens/profiler.py` with `profile(rows, column_names)` public function
- Returns `list[dict]` with per-column type, missing counts/%, unique counts, numeric stats
- Deterministic type detection: integer → float → string → mixed
- Missing-value contract: only empty string `""` is missing
- Added `tests/test_profiler.py` with 5 unit tests (all pass on first run after assertion corrections)
- Updated `docs/ARCHITECTURE.md` with type detection and missing-value contracts
- **Git checkpoint:** `feat(T02): column profiler module`

---

## [0.2.1] — 2026-08-22

### fix(T01): add explicit quoted-comma fixture and expand test coverage

- Added `tests/fixtures/quoted_commas.csv` with embedded commas in quoted fields
- Expanded `tests/test_loader.py` from 4 to 7 tests covering all 6 fixtures
- Corrective pass: all 7 tests pass on first run
- **Git checkpoint:** `fix(T01): add explicit quoted-comma fixture and expand test coverage`

---

## [0.2.0] — 2026-08-22

### feat(T01): CSV loader module

- Implemented `src/datalens/loader.py` with `load_csv(path)` public function
- Returns `(rows: list[dict], column_names: list[str], row_count: int)`
- Handles missing file (raises `FileNotFoundError`), empty CSV, quoted fields
- Added `tests/test_loader.py` with 4 unit tests (all pass on first run)
- Fixed `pyproject.toml` build backend (`setuptools.backends.legacy` → `setuptools.build_meta`) — environment correction
- Created `.gitignore` to exclude pip artifacts — repository hygiene
- **Git checkpoint:** `feat(T01): CSV loader module`

---

## [0.1.0] — 2026-08-22

### chore(T00): project operating system

- Established project directory structure (`src/datalens/`, `tests/`, `docs/`, `reports/`)
- Created `pyproject.toml` with project metadata, dependencies (`jinja2`), dev dependency (`pytest`), and CLI entry point
- Created `src/datalens/__init__.py` (package marker)
- Wrote `CLAUDE.md` — project invariants, scope boundaries, context-drift pre-flight protocol, code style, session discipline
- Wrote `docs/ARCHITECTURE.md` — module map, data flow, I/O ownership, dependency rationale
- Wrote `docs/TASKS.md` — all tasks (T00–T06) with full detail
- Wrote `docs/DECISIONS.md` — 6 initial ADR entries
- Wrote `docs/EXPERIMENT.md` — experiment protocol, variables, hypotheses, methodology
- Wrote `docs/SESSION_LOG.md` — initial session entry
- Wrote `docs/CHANGELOG.md` — this file
- Wrote `README.md` — project description, install, run instructions
- Created 5 test fixture CSV files in `tests/fixtures/`
- **Git checkpoint:** `chore(T00): project operating system`

