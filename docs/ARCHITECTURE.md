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
- **Output:** list of ColumnProfile objects/dicts
- **Per-column output fields:**
  - `name` — column name
  - `type` — detected type: `integer`, `float`, `string`, or `mixed`
  - `missing_count` — number of missing/empty values
  - `missing_pct` — percentage of missing values (0–100)
  - `unique_count` — number of distinct non-missing values
  - For numeric columns: `min`, `max`, `mean`, `median`, `std`
- **Responsibility:** type inference, missing-value detection, unique counting, numeric statistics

### quality.py
- **Input:** list of ColumnProfile dicts
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
