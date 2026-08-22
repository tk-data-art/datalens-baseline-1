"""CLI entry point for DataLens.

Orchestrates the full pipeline: load → profile → score → duplicate count → report.
"""

import sys
from pathlib import Path

from datalens.loader import load_csv
from datalens.profiler import profile
from datalens.quality import compute_score
from datalens.report import generate


def _count_duplicates(rows: list[dict]) -> int:
    seen = set()
    for row in rows:
        seen.add(tuple(sorted(row.items())))
    return len(rows) - len(seen)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: datalens <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]

    try:
        rows, column_names, row_count = load_csv(csv_path)
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    profiles = profile(rows, column_names)
    result = compute_score(profiles, row_count)
    duplicate_row_count = _count_duplicates(rows)

    stem = Path(csv_path).stem
    output_path = f"reports/{stem}.html"
    generate(profiles, result, row_count, duplicate_row_count, output_path)

    print(
        f"Report written to: {output_path} | Rows: {row_count} | "
        f"Columns: {len(column_names)} | Quality Score: {result['composite_score']} / 100"
    )
