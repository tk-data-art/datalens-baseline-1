# DataLens — Experiment Results

## 1. Baseline 1 Summary

### 1.1 Implementation

| Metric | Value |
|---|---|
| Total modules | 6 (loader, profiler, quality, report, cli, __main__) |
| Total application LOC | ~200 |
| Total test LOC | ~350 |
| Total tests | 29 |
| Dependencies | jinja2 (production), pytest (dev) |
| Python version | 3.13.14 |

**Module list with public functions:**

| Module | Public Function | Responsibility |
|---|---|---|
| `loader.py` | `load_csv(path)` | Read and parse CSV files |
| `profiler.py` | `profile(rows, column_names)` | Per-column statistics |
| `quality.py` | `compute_score(profiles, total_rows)` | Composite quality score |
| `report.py` | `generate(profiles, result, row_count, duplicate_row_count, output_path)` | HTML report rendering |
| `cli.py` | `main()` | CLI entry point, pipeline orchestration |
| `__main__.py` | (entry-point wrapper) | Enables `python -m datalens` |

---

### 1.2 Test Results

| Test File | Tests | Pass | Fail |
|---|---|---|---|
| `test_loader.py` | 7 | 7 | 0 |
| `test_profiler.py` | 5 | 5 | 0 |
| `test_quality.py` | 9 | 9 | 0 |
| `test_report.py` | 5 | 5 | 0 |
| `test_cli.py` | 3 | 3 | 0 |
| **Total** | **29** | **29** | **0** |

**All tests pass on first run.** No assertion corrections needed for T02–T05.

---

### 1.3 Development Process

| Task | Description | Est. | Actual | Tests | Drift | Corrective Passes |
|---|---|---|---|---|---|---|
| T00 | Project operating system | 110 min | ~15 min | N/A | NONE | 0 |
| T01 | loader.py — CSV reading | 35 min | ~25 min | 7/7 | NONE | 1 (added quoted-comma fixture) |
| T02 | profiler.py — per-column profiling | 40 min | ~15 min | 5/5 | NONE | 0 |
| T03 | quality.py — composite quality score | 30 min | ~20 min | 9/9 | NONE | 0 |
| T04 | report.py — HTML report generation | 40 min | ~25 min | 5/5 | NONE | 0 |
| T05 | cli.py — CLI entry point | 30 min | ~20 min | 3/3 | NONE | 0 |
| T06 | Final review and polish | 130 min | ~90 min | 29/29 | NONE | 0 |

**Total time (T00–T05):** ~120 minutes

---

### 1.4 Context Drift

| Session | Drift Type | Description | Severity | Resolution |
|---|---|---|---|---|
| T00 | Documentation enhancement | Added task completion reporting protocol, live progress tracker, audit template | NONE | Within documentation scope |
| T01 | Repository/environment | Fixed pyproject.toml build backend, created .gitignore | NONE | Environment hygiene |
| T03 | API contract expansion | Expanded `compute_score(profiles)` → `compute_score(profiles, total_rows)` | NONE | Pre-flight approved |
| T04 | Input contract expansion | report.py receives 4 explicit parameters instead of 1 | NONE | Pre-flight approved, ADR-007 written |
| T05 | Entry point addition | Added `__main__.py` for `python -m datalens` | NONE | Required for subprocess integration test |

**No application scope drift in any session.**

---

### 1.5 Pre-Flight Decisions

| Session | Decisions Made | Count |
|---|---|---|
| T01 | None (implementation straightforward) | 0 |
| T02 | None (edge case documented in ARCHITECTURE.md) | 0 |
| T03 | Scoring formula (0.50/0.30/0.20), API expansion, terminology (distinctness) | 3 |
| T04 | Template format, quality score display, long-value handling, edge case rendering, input contract | 5 |
| T05 | Duplicate semantics, integration test approach, stdout format | 3 |
| **Total** | | **11** |

---

### 1.6 Corrective Passes

| Task | Issue | Resolution |
|---|---|---|
| T01 | Initial test count was 4, expanded to 7 after adding quoted-comma fixture | Added explicit fixture and 3 additional tests |
| T06 (T00 fix) | T00 acceptance criteria said "5 fixtures" — corrected to "6 fixtures" | Updated docs/TASKS.md |

**Total corrective passes: 2**

---

### 1.7 Scalability Benchmark Results

| Benchmark | Rows | Cols | File Size | Time (s) | Peak RSS (MB) | Result |
|---|---|---|---|---|---|---|
| 10k × 20 | 10,000 | 20 | 1.0 MB | 0.16 | 56.8 | Success |
| 100k × 20 | 100,000 | 20 | 10.1 MB | 1.23 | 322.2 | Success |
| 1M × 20 | 1,000,000 | 20 | 106.1 MB | 14.86 | 3250.5 | Success |
| 100k × 100 | 100,000 | 100 | 40.6 MB | 6.59 | 1581.1 | Success |

**All benchmarks completed successfully.** No OOM failures, no timeouts.

**Scaling observations:**
- Time scales roughly linearly with row count (10k → 100k → 1M: ~10× increase in rows → ~10× increase in time)
- Memory scales with data size + report output
- 100k × 100 completes in 6.59s despite 5× more columns than 100k × 20 (1.23s) — profiling cost is modest per column
- 1M × 20 uses ~3.2 GB peak memory — viable on modern hardware but approaching limits on memory-constrained systems

---

### 1.8 Limitations Observed

- **In-memory processing:** All CSV data is loaded into memory as `list[dict]`. For files approaching available RAM, performance degrades and may cause OOM.
- **No streaming:** Cannot process files larger than available memory.
- **Duplicate detection complexity:** `tuple(sorted(row.items()))` is O(c log c) per row where c = column count. For wide datasets (100+ columns) with many rows, this becomes noticeable.
- **Single-threaded:** No parallel processing of columns or rows.
- **No incremental processing:** Full reprofile required for every run.

---

## 2. Baseline 2 Summary

*Reserved for Baseline 2 (plugin-enhanced Claude Code) results. To be populated after Baseline 2 completion.*

---

## 3. Comparative Analysis

*Reserved for post-experiment comparative analysis. To be populated after both baselines complete.*

---

## 4. Environment Metadata

| Field | Value |
|---|---|
| Machine | MacBook Pro (Apple Silicon) |
| CPU Architecture | arm64 |
| macOS Version | 26.5.2 |
| Python Version | 3.13.14 (Clang 21.0.0) |
| Git Commit | `0fae8ce` — `chore(T06): final review and polish` |
| Benchmark Date | 2026-08-22 |
| Benchmark Seed | 42 (deterministic) |
| Measurement Tool | `/usr/bin/time -l` (macOS) |

---

## 5. Reproducibility

To reproduce these benchmarks:

1. Clone the repository at commit `0fae8ce`
2. Run `python3 -m pip install -e .`
3. Run `python3 benchmarks/benchmark_generator.py <rows> <cols> benchmarks/data/benchmark_<rows>k_<cols>.csv`
4. Run `PYTHONPATH=src /usr/bin/time -l python3 -m datalens benchmarks/data/benchmark_<rows>k_<cols>.csv`
5. Parse peak RSS from `/usr/bin/time -l` stderr output

---

*This report was generated as part of the DataLens experimental protocol. See `docs/EXPERIMENT.md` for details.*
