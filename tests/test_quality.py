"""Unit tests for quality.py."""

import pytest
from pathlib import Path

from datalens.loader import load_csv
from datalens.profiler import profile
from datalens.quality import compute_score


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_profile(path: str) -> tuple[list[dict], int]:
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / path))
    profiles = profile(rows, columns)
    return profiles, row_count


def test_clean_simple_scores_ninety_or_higher():
    profiles, row_count = _load_profile("clean_simple.csv")
    result = compute_score(profiles, row_count)
    assert result["composite_score"] == pytest.approx(96.0, abs=0.01)
    assert result["composite_score"] >= 90


def test_missing_values_scores_lower_than_clean():
    clean_profiles, clean_rows = _load_profile("clean_simple.csv")
    missing_profiles, missing_rows = _load_profile("missing_values.csv")
    clean_score = compute_score(clean_profiles, clean_rows)["composite_score"]
    missing_score = compute_score(missing_profiles, missing_rows)["composite_score"]
    assert missing_score == pytest.approx(81.6667, abs=0.01)
    assert missing_score < clean_score


def test_mixed_types_scores_lower_than_clean():
    clean_profiles, clean_rows = _load_profile("clean_simple.csv")
    mixed_profiles, mixed_rows = _load_profile("mixed_types.csv")
    clean_score = compute_score(clean_profiles, clean_rows)["composite_score"]
    mixed_score = compute_score(mixed_profiles, mixed_rows)["composite_score"]
    assert mixed_score == pytest.approx(89.0, abs=0.01)
    assert mixed_score < clean_score


def test_edge_empty_returns_zero():
    profiles, row_count = _load_profile("edge_empty.csv")
    result = compute_score(profiles, row_count)
    assert result["composite_score"] == 0.0
    assert result["column_scores"] == []


def test_type_consistency_weights():
    profiles = [
        {"name": "col_a", "type": "integer", "missing_pct": 0.0, "unique_count": 5},
        {"name": "col_b", "type": "float", "missing_pct": 0.0, "unique_count": 5},
        {"name": "col_c", "type": "string", "missing_pct": 0.0, "unique_count": 5},
        {"name": "col_d", "type": "mixed", "missing_pct": 0.0, "unique_count": 5},
    ]
    result = compute_score(profiles, 5)
    scores = {cs["name"]: cs["score"] for cs in result["column_scores"]}

    assert scores["col_a"] == pytest.approx(1.0, abs=0.001)
    assert scores["col_b"] == pytest.approx(1.0, abs=0.001)
    assert scores["col_c"] == pytest.approx(1.0, abs=0.001)
    assert scores["col_d"] == pytest.approx(0.85, abs=0.001)


def test_distinctness_calculation():
    profiles = [
        {"name": "col_a", "type": "string", "missing_pct": 0.0, "unique_count": 5},
        {"name": "col_b", "type": "string", "missing_pct": 0.0, "unique_count": 2},
    ]
    result = compute_score(profiles, 5)
    scores = {cs["name"]: cs["score"] for cs in result["column_scores"]}

    assert scores["col_a"] == pytest.approx(1.0, abs=0.001)
    assert scores["col_b"] == pytest.approx(0.88, abs=0.001)


def test_empty_total_rows_returns_zero():
    profiles = [
        {"name": "x", "type": "string", "missing_pct": 0.0, "unique_count": 0},
    ]
    result = compute_score(profiles, 0)
    assert result["composite_score"] == 0.0
    assert result["column_scores"] == []


def test_deterministic_results():
    profiles, row_count = _load_profile("missing_values.csv")
    result_1 = compute_score(profiles, row_count)
    result_2 = compute_score(profiles, row_count)
    assert result_1 == result_2


def test_composite_score_in_bounds():
    profiles, row_count = _load_profile("clean_simple.csv")
    result = compute_score(profiles, row_count)
    assert 0.0 <= result["composite_score"] <= 100.0
