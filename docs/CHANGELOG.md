# DataLens — Changelog

All changes are recorded with their git commit hash after each checkpoint.

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
