"""Unit tests for profiler.py."""

import pytest
from pathlib import Path

from datalens.loader import load_csv
from datalens.profiler import profile


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_and_profile(filename: str) -> list[dict]:
    rows, columns, _ = load_csv(str(FIXTURES_DIR / filename))
    return profile(rows, columns)


def _col(profiles: list[dict], name: str) -> dict:
    for p in profiles:
        if p["name"] == name:
            return p
    raise KeyError(f"Column '{name}' not found in profiles")


def test_profile_clean_simple():
    profiles = _load_and_profile("clean_simple.csv")

    name_col = _col(profiles, "name")
    assert name_col["type"] == "string"
    assert name_col["missing_count"] == 0
    assert name_col["missing_pct"] == 0.0
    assert name_col["unique_count"] == 5

    age_col = _col(profiles, "age")
    assert age_col["type"] == "integer"
    assert age_col["missing_count"] == 0
    assert age_col["missing_pct"] == 0.0
    assert age_col["unique_count"] == 5
    assert age_col["min"] == 25.0
    assert age_col["max"] == 35.0
    assert age_col["mean"] == 30.0
    assert age_col["median"] == 30.0
    assert age_col["std"] == pytest.approx(3.808, abs=0.001)

    salary_col = _col(profiles, "salary")
    assert salary_col["type"] == "integer"
    assert salary_col["min"] == 45000.0
    assert salary_col["max"] == 60000.0
    assert salary_col["mean"] == 52400.0

    active_col = _col(profiles, "active")
    assert active_col["type"] == "string"
    assert active_col["unique_count"] == 2


def test_profile_missing_values():
    profiles = _load_and_profile("missing_values.csv")

    name_col = _col(profiles, "name")
    assert name_col["missing_count"] == 0
    assert name_col["unique_count"] == 6

    age_col = _col(profiles, "age")
    assert age_col["missing_count"] == 1
    assert age_col["missing_pct"] == pytest.approx(16.67, abs=0.01)

    salary_col = _col(profiles, "salary")
    assert salary_col["missing_count"] == 2
    assert salary_col["missing_pct"] == pytest.approx(33.33, abs=0.01)

    dept_col = _col(profiles, "department")
    assert dept_col["missing_count"] == 2
    assert dept_col["missing_pct"] == pytest.approx(33.33, abs=0.01)


def test_profile_mixed_types():
    profiles = _load_and_profile("mixed_types.csv")

    name_col = _col(profiles, "name")
    assert name_col["type"] == "string"
    assert name_col["unique_count"] == 6

    age_col = _col(profiles, "age")
    assert age_col["type"] == "mixed"
    assert "min" not in age_col

    salary_col = _col(profiles, "salary")
    assert salary_col["type"] == "integer"
    assert salary_col["missing_count"] == 0

    rating_col = _col(profiles, "rating")
    assert rating_col["type"] == "mixed"

    active_col = _col(profiles, "active")
    assert active_col["type"] == "string"


def test_profile_duplicates():
    profiles = _load_and_profile("duplicates.csv")

    name_col = _col(profiles, "name")
    assert name_col["unique_count"] == 4

    age_col = _col(profiles, "age")
    assert age_col["unique_count"] == 4

    city_col = _col(profiles, "city")
    assert city_col["unique_count"] == 3


def test_profile_edge_empty():
    profiles = _load_and_profile("edge_empty.csv")

    assert len(profiles) == 3

    for col in profiles:
        assert col["missing_count"] == 0
        assert col["missing_pct"] == 0.0
        assert col["unique_count"] == 0
        assert col["type"] == "string"
        assert "min" not in col
