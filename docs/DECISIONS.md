# DataLens — Decisions (ADR Log)

## ADR-001: Python as implementation language

**Date:** 2026-08-22
**Status:** Accepted

**Context:** DataLens is a CLI data-quality analyzer. Language choice affects dependencies, test tooling, and deployment.

**Decision:** Python 3.11+.

**Consequences:**
- Stdlib `csv` and `statistics` modules eliminate two external dependencies
- `pytest` is the standard test framework with minimal configuration
- `jinja2` is the only production dependency (HTML templating)
- Target audience (developers) likely has Python installed
- No compilation step, no runtime complexity

**Alternatives considered:** JavaScript (Node.js) — rejected because Chart.js/Papa Parse are frontend-oriented and the product is a CLI tool, not a web app.

---

## ADR-002: Single-file module layout with one public function per module

**Date:** 2026-08-22
**Status:** Accepted

**Context:** Need module boundaries that are independently testable and easy to understand in a learning experiment.

**Decision:** Each module (`loader.py`, `profiler.py`, `quality.py`, `report.py`, `cli.py`) is a single file exposing one public function. Communication is through plain Python data structures.

**Consequences:**
- Easy to test each module in isolation
- Clear I/O ownership per module
- No circular dependencies
- Simple enough for a small project, modular enough for meaningful evaluation

**Alternatives considered:** Class-based design — rejected as unnecessary abstraction for this scope.

---

## ADR-003: jinja2 for HTML report generation

**Date:** 2026-08-22
**Status:** Accepted

**Context:** Report must be a self-contained HTML file with multiple sections. Need a templating approach.

**Decision:** `jinja2` for HTML templating with an inline template string.

**Consequences:**
- Clean separation of template logic from data
- Single production dependency beyond stdlib
- Template can be tested for content without rendering
- No need for a separate template file — inline template keeps the project small

**Alternatives considered:** String concatenation — rejected because report has enough structure that concatenation becomes hard to maintain and verify.

---

## ADR-004: Five fixture CSV files for test coverage

**Date:** 2026-08-22
**Status:** Accepted

**Context:** Need deterministic test inputs that cover the full feature surface without dynamic generation.

**Decision:** Six static fixture files: `clean_simple.csv`, `missing_values.csv`, `mixed_types.csv`, `duplicates.csv`, `edge_empty.csv`, `quoted_commas.csv`.

**Consequences:**
- Tests are reproducible and version-controlled
- Both baselines use identical fixtures
- No test flakiness from random data
- Covers: baseline metrics, null handling, type edge cases, dedup, empty input, quoted-comma edge case

**Alternatives considered:** Dynamic fixture generation — rejected because static files are simpler, version-controlled, and both baselines can share them exactly.

---

## ADR-005: Independent repositories for Baseline 1 and Baseline 2

**Date:** 2026-08-22
**Status:** Accepted

**Context:** Experiment requires fair comparison between vanilla Claude Code and plugin-enhanced Claude Code.

**Decision:** Baseline 1 and Baseline 2 are separate git repositories with no shared history. Both receive equivalent T00 setup independently.

**Consequences:**
- Clean diff comparison at each task checkpoint
- No risk of cross-contamination between baselines
- Each baseline's git history is self-contained
- Requires manual setup effort for Baseline 2, but this is acceptable for experimental integrity

**Alternatives considered:** Branching Baseline 2 from Baseline 1 — rejected because branch history would conflate the two baselines' work.

---

## ADR-007: report.py receives profiles, result, row_count, and duplicate_row_count as explicit parameters

**Date:** 2026-08-22
**Status:** Accepted

**Context:** report.py needs to display row count, column count, duplicate-row count, and per-column profiling data (types, missing values, unique counts, numeric statistics) — none of which are present in the QualityResult dict from T03. The original T04 spec used `generate(result, output_path)` which cannot populate all required report sections.

**Decision:** report.py receives four explicit parameters: `profiles` (list[dict] from profiler), `result` (dict from quality), `row_count` (int from loader), and `duplicate_row_count` (int, computed by cli.py).

**Consequences:**
- report.py is a pure renderer — it does not parse CSV, profile data, compute scores, or detect duplicates
- Upstream T01–T03 contracts remain unchanged — loader.py, profiler.py, and quality.py output formats are not modified
- row_count remains an explicit parameter rather than embedded in QualityResult — T03 contract stays clean
- duplicate_row_count is computed by cli.py (which has access to raw rows) and passed as input — no duplicate detection logic in report.py
- report.py API: `generate(profiles, result, row_count, duplicate_row_count, output_path) -> None`
- jinja2 Environment(autoescape=True) is used for security against CSV-derived HTML injection

**Alternatives considered:**
- Expanding QualityResult to include row_count and duplicate_row_count — rejected because it would modify the T03-approved output contract
- Computing all metrics in cli.py and embedding them in a flat dict — rejected because profiles already contain the data in structured form; wrapping it adds unnecessary indirection
- Computing duplicate rows in profiler.py — rejected because it would change the T02 module contract and profiler's responsibility is per-column statistics, not row-level comparison

---

## ADR-006: Testing integrated per task, not batched at end

**Date:** 2026-08-22
**Status:** Accepted

**Context:** Need to evaluate development process, including testing behavior.

**Decision:** Each implementation task (T01–T05) includes writing and verifying its own tests within the same session. T06 is a full-suite verification pass only.

**Consequences:**
- Tests validate each module as it's built
- Failures are caught immediately, not at the end
- Measures whether Claude Code writes tests alongside implementation or defers them
- Aligns with the experiment's goal of evaluating development process

**Alternatives considered:** Batch all tests in T06 — rejected because it wouldn't reveal testing behavior differences between baselines.
