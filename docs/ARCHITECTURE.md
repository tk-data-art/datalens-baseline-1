# DataLens — Architecture

## System Overview

DataLens is a single-process command-line tool. It reads a CSV from disk, profiles its contents, computes a quality score, and writes an HTML report. No network, no server, no concurrency.

## Module Map

```
src/datalens/
├── __init__.py        Package marker (empty)
├── loader.py          CSV I/O and parsing
├── profiler.py        Per-column statistics computation
├── quality.py         Composite quality score calculation
├── report.py          HTML report generation and file output
└── cli.py             CLI entry point and pipeline orchestration
```

## Data Flow

```
CSV file on disk
    │
    ▼ loader.load_csv(path)
    │  returns: list[dict], column_names: list[str], row_count: int
    ▼
profiler.profile(data, column_names)
    │  returns: list[ColumnProfile] (one per column)
    ▼
quality.compute_score(profiles)
    │  returns: QualityResult (composite score + per-column breakdown)
    ▼
report.generate(result, output_path)
    │  writes: HTML file to disk
    ▼
cli.main()
    │  orchestrates the above sequence
    │  prints summary to stdout
    │  returns exit code
```

## Module Contracts

### loader.py
- **Input:** file path (str)
- **Output:** tuple of (rows: list[dict], column_names: list[str], row_count: int)
- **Errors:** raises clear exception for missing file, empty file, malformed CSV
- **Responsibility:** file I/O, CSV parsing, initial row count

### profiler.py
- **Input:** rows (list[dict]), column_names (list[str])
- **Output:** list[dict] — each dict is a ColumnProfile with fields: `name`, `type`, `missing_count`, `missing_pct`, `unique_count`, and for numeric columns: `min`, `max`, `mean`, `median`, `std`
- **Responsibility:** type inference, missing-value detection, unique counting, numeric statistics

**Type detection contract (deterministic rules):**
For each column, ignore values classified as missing (empty string `""`).
- If all non-missing values parse as integers → type is `"integer"`
- Otherwise, if all non-missing values are numeric → type is `"float"`
- If all non-missing values are non-numeric → type is `"string"`
- If the column contains both numeric and non-numeric non-missing values → type is `"mixed"`
- Boolean-looking strings ("true", "false") are classified as `"string"` — no boolean type is defined in the architecture.

**Missing-value contract:**
Only the empty string `""` is considered missing for T02. Whitespace-only values, "NA", "N/A", "null", and similar are NOT missing. Configurable missing-value semantics are not implemented in T02.

**ColumnProfile output dict fields:**
- `name` (str) — column header name
- `type` (str) — one of: `"integer"`, `"float"`, `"string"`, `"mixed"`
- `missing_count` (int) — count of empty-string values
- `missing_pct` (float) — percentage of missing values (0.0–100.0)
- `unique_count` (int) — count of distinct non-missing values
- `min`, `max`, `mean`, `median`, `std` (float) — present only for numeric columns (`integer` or `float` type)

**Standard deviation edge case:**
For numeric columns with fewer than two non-missing observations, `std` is `0.0`. The `statistics.stdev()` function requires at least 2 data points; with fewer, the profiler returns `0.0` rather than raising an exception.

### quality.py
- **Input:** list[dict] — each dict is a ColumnProfile from profiler.py
- **Output:** QualityResult (composite_score: float 0–100, column_scores: list)
- **Scoring logic:** weighted aggregation of per-column metrics (missing values, type consistency, completeness). Exact weighting defined in implementation.
- **Responsibility:** score computation, score aggregation

### report.py
- **Input:** QualityResult, output_path (str)
- **Output:** writes HTML file to output_path
- **HTML sections:** row count, column count, data types table, missing-value table with percentages, duplicate-row count, unique-value counts, numeric statistics, quality score display
- **Responsibility:** HTML generation, file I/O for report

### cli.py
- **Input:** CLI arguments (positional: CSV file path)
- **Output:** stdout summary, HTML report file, exit code
- **Responsibility:** argument parsing, pipeline orchestration, user-facing output

## Dependency Graph

```
cli.py → loader.py → (stdlib csv)
cli.py → profiler.py → (stdlib statistics)
cli.py → quality.py → (no deps beyond profiler output)
cli.py → report.py → jinja2
```

Modules communicate only through plain Python data structures. No module imports another module's internals.

## Dependency Choices

| Dependency | Purpose | Rationale |
|---|---|---|
| `csv` (stdlib) | CSV parsing | Built-in, handles quoted fields, no external dependency |
| `statistics` (stdlib) | Numeric stats (mean, median, stdev) | Built-in, no external dependency |
| `jinja2` | HTML templating | Single-purpose, widely used, enables clean report templates |
| `pytest` (dev) | Testing | Minimal config, standard choice |
| `argparse` (stdlib) | CLI argument parsing | Built-in, sufficient for single-argument CLI |
