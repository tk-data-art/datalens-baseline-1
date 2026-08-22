"""Unit tests for loader.py."""

import pytest
from pathlib import Path

from datalens.loader import load_csv


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_load_clean_simple():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "clean_simple.csv"))
    assert row_count == 5
    assert columns == ["name", "age", "salary", "department", "active"]
    assert len(rows) == 5
    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == "30"
    assert rows[4]["active"] == "false"


def test_load_missing_values():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "missing_values.csv"))
    assert row_count == 6
    assert columns == ["name", "age", "salary", "department", "active"]
    assert rows[0]["salary"] == ""  # empty field


def test_load_mixed_types():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "mixed_types.csv"))
    assert row_count == 6
    assert columns == ["name", "age", "salary", "rating", "active"]
    assert rows[4]["age"] == "thirty-two"  # string where numeric expected


def test_load_duplicates():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "duplicates.csv"))
    assert row_count == 6
    assert columns == ["name", "age", "city"]
    assert rows[0] == rows[2]  # Alice appears twice


def test_quoted_fields_with_embedded_commas():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "quoted_commas.csv"))
    assert row_count == 4
    assert columns == ["name", "description", "location"]
    assert rows[0]["description"] == "Software Engineer, Senior"
    assert rows[2]["description"] == "Product Manager"
    assert rows[2]["location"] == "San Francisco, CA"


def test_empty_csv():
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / "edge_empty.csv"))
    assert row_count == 0
    assert columns == ["name", "age", "salary"]
    assert rows == []


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_csv(str(FIXTURES_DIR / "nonexistent_file.csv"))
