"""CSV file loader module.

Reads a CSV file from disk and returns structured data as a list of dicts,
column names, and a row count.
"""

import csv
from pathlib import Path


def load_csv(path: str) -> tuple[list[dict], list[str], int]:
    """Load a CSV file and return rows, column names, and row count.

    Args:
        path: File system path to a CSV file.

    Returns:
        A tuple of (rows, column_names, row_count) where rows is a list
        of dicts keyed by column name.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        column_names = list(reader.fieldnames or [])
        rows = list(reader)

    return rows, column_names, len(rows)
