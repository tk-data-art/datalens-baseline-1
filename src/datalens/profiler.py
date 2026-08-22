"""Per-column CSV data profiler.

Computes type inference, missing-value statistics, unique-value counts,
and numeric statistics for each column in loaded CSV data.
"""

import statistics
from typing import Any


def _try_int(value: str) -> bool:
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def _try_float(value: str) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def _infer_type(non_missing: list[str]) -> str:
    if not non_missing:
        return "string"

    all_int = all(_try_int(v) for v in non_missing)
    if all_int:
        return "integer"

    all_numeric = all(_try_float(v) for v in non_missing)
    if all_numeric:
        return "float"

    any_numeric = any(_try_float(v) for v in non_missing)
    if any_numeric:
        return "mixed"

    return "string"


def _numeric_stats(values: list[float]) -> dict[str, float]:
    return {
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.mean(values), 10),
        "median": round(statistics.median(values), 10),
        "std": round(statistics.stdev(values), 10) if len(values) > 1 else 0.0,
    }


def profile(rows: list[dict], column_names: list[str]) -> list[dict]:
    """Profile each column in loaded CSV data.

    Args:
        rows: List of row dicts from loader.load_csv().
        column_names: List of column header strings.

    Returns:
        A list of dicts, one per column. Each dict contains:
        - name (str): column header name
        - type (str): "integer", "float", "string", or "mixed"
        - missing_count (int): count of empty-string values
        - missing_pct (float): percentage of missing values (0.0–100.0)
        - unique_count (int): count of distinct non-missing values
        - min, max, mean, median, std (float): present for numeric columns
    """
    total_rows = len(rows)
    profiles = []

    for col in column_names:
        values = [row.get(col, "") for row in rows]
        missing = [v for v in values if v == ""]
        non_missing = [v for v in values if v != ""]

        missing_count = len(missing)
        missing_pct = round((missing_count / total_rows) * 100, 10) if total_rows > 0 else 0.0
        unique_count = len(set(non_missing))

        col_type = _infer_type(non_missing)

        profile_dict: dict[str, Any] = {
            "name": col,
            "type": col_type,
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_count,
        }

        if col_type in ("integer", "float"):
            numeric_values = [float(v) for v in non_missing]
            profile_dict.update(_numeric_stats(numeric_values))

        profiles.append(profile_dict)

    return profiles
