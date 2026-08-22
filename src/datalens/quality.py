"""Composite data-quality score computation.

Aggregates profiler output into a 0–100 quality score using a
weighted formula: completeness (50%), type consistency (30%),
distinctness (20%).
"""

from typing import Any


_TYPE_CONSISTENCY = {
    "integer": 1.0,
    "float": 1.0,
    "string": 1.0,
    "mixed": 0.5,
}

_W_COMPLETENESS = 0.50
_W_TYPE = 0.30
_W_DISTINCTNESS = 0.20


def compute_score(profiles: list[dict[str, Any]], total_rows: int) -> dict[str, Any]:
    """Compute a composite quality score from profiler output.

    Args:
        profiles: ColumnProfile dicts from profiler.profile().
        total_rows: Row count from loader.load_csv().

    Returns:
        Dict with composite_score (float 0–100) and column_scores (list).
    """
    if total_rows == 0:
        return {"composite_score": 0.0, "column_scores": []}

    column_scores = []
    for p in profiles:
        completeness = 1.0 - (p["missing_pct"] / 100.0)
        type_cons = _TYPE_CONSISTENCY[p["type"]]
        distinctness = min(p["unique_count"] / total_rows, 1.0)

        col_score = (
            _W_COMPLETENESS * completeness
            + _W_TYPE * type_cons
            + _W_DISTINCTNESS * distinctness
        )
        column_scores.append({"name": p["name"], "score": col_score})

    composite = (sum(c["score"] for c in column_scores) / len(column_scores)) * 100
    return {"composite_score": composite, "column_scores": column_scores}
