# DataLens — Changelog

All changes are recorded with their git commit hash after each checkpoint.

---

## [0.2.0] — 2026-08-22

### feat(T01): CSV loader module

- Implemented `src/datalens/loader.py` with `load_csv(path)` public function
- Returns `(rows: list[dict], column_names: list[str], row_count: int)`
- Handles missing file (raises `FileNotFoundError`), empty CSV, quoted fields
- Added `tests/test_loader.py` with 4 unit tests (all pass on first run)
- Fixed `pyproject.toml` build backend (`setuptools.backends.legacy` → `setuptools.build_meta`)
- Created `.gitignore` to exclude pip artifacts
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
