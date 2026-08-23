# DataLens

A small CSV data-quality analyzer. Reads a CSV file, profiles its contents, computes quality metrics, and produces a self-contained HTML report.

## What it does

- Row count and column count
- Detected data types per column
- Missing-value counts and percentages
- Duplicate-row count
- Unique-value counts per column
- Basic numeric statistics (min, max, mean, median, std)
- Composite data-quality score (0–100)
- HTML report with all findings

## Requirements

- Python 3.11 or higher

## Installation

```bash
pip install -e .
```

## Usage

```bash
datalens path/to/your_file.csv
```

Or equivalently:

```bash
python -m datalens path/to/your_file.csv
```

The HTML report is written to the `reports/` directory.

## Project status

This project is a Claude Code learning experiment (Baseline 1 — vanilla Claude Code, no plugins). All application source code and tests are complete.

See `docs/EXPERIMENT.md` for experiment details.

## Example

```bash
datalens tests/fixtures/clean_simple.csv
```

Output:

```
Report written to: reports/clean_simple.html | Rows: 5 | Columns: 5 | Quality Score: 96.0 / 100
```

The HTML report is written to the `reports/` directory.
