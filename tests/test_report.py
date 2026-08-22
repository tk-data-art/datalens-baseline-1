"""Unit tests for report.py."""

import re
from pathlib import Path

from datalens.loader import load_csv
from datalens.profiler import profile
from datalens.quality import compute_score
from datalens.report import generate


FIXTURES_DIR = Path(__file__).parent / "fixtures"
OUTPUT_DIR = Path(__file__).parent / "tmp_output"


def _run_pipeline(filename: str, duplicate_row_count: int = 0):
    rows, columns, row_count = load_csv(str(FIXTURES_DIR / filename))
    profiles = profile(rows, columns)
    result = compute_score(profiles, row_count)
    output_path = str(OUTPUT_DIR / f"{Path(filename).stem}.html")
    generate(profiles, result, row_count, duplicate_row_count, output_path)
    return Path(output_path), profiles, result, row_count


def setup_function():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def teardown_function():
    for f in OUTPUT_DIR.glob("*.html"):
        f.unlink()


def test_generate_creates_file():
    path, _, _, _ = _run_pipeline("clean_simple.csv", 0)
    assert path.exists()
    assert path.stat().st_size > 0


def test_generate_contains_all_sections():
    path, profiles, result, row_count = _run_pipeline("clean_simple.csv", 0)
    html = path.read_text(encoding="utf-8")

    assert "<!DOCTYPE html>" in html
    assert "Row count" in html
    assert str(row_count) in html
    assert "Column count" in html
    assert str(len(profiles)) in html
    assert "Duplicate rows" in html
    assert "Data Types" in html
    assert "Missing Values" in html
    assert "Unique Values" in html
    assert "Numeric Statistics" in html
    assert "Quality Score" in html
    assert f"{result['composite_score']} / 100" in html


def test_generate_escapes_html():
    profiles = [
        {
            "name": "<script>alert('xss')</script>",
            "type": "string",
            "missing_count": 1,
            "missing_pct": 33.33,
            "unique_count": 2,
        }
    ]
    result = {
        "composite_score": 85.0,
        "column_scores": [{"name": "<b>bold</b>", "score": 0.85}],
    }
    output_path = str(OUTPUT_DIR / "escape_test.html")
    generate(profiles, result, 3, 0, output_path)
    html = Path(output_path).read_text(encoding="utf-8")

    assert "<script>alert('xss')</script>" not in html
    assert "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;" in html
    assert "<b>bold</b>" not in html
    assert "&lt;b&gt;bold&lt;/b&gt;" in html


def test_generate_renders_numeric_and_non_numeric():
    profiles = [
        {
            "name": "id",
            "type": "integer",
            "missing_count": 0,
            "missing_pct": 0.0,
            "unique_count": 3,
            "min": 1.0,
            "max": 3.0,
            "mean": 2.0,
            "median": 2.0,
            "std": 1.0,
        },
        {
            "name": "label",
            "type": "string",
            "missing_count": 0,
            "missing_pct": 0.0,
            "unique_count": 3,
        },
    ]
    result = {
        "composite_score": 96.0,
        "column_scores": [
            {"name": "id", "score": 1.0},
            {"name": "label", "score": 1.0},
        ],
    }
    output_path = str(OUTPUT_DIR / "mixed_types_render.html")
    generate(profiles, result, 3, 0, output_path)
    html = Path(output_path).read_text(encoding="utf-8")

    assert "Numeric Statistics" in html
    assert "1.0" in html
    assert "label" in html
    assert "string" in html


def test_generate_complete_fixture_pipeline():
    path, profiles, result, row_count = _run_pipeline("clean_simple.csv", 0)
    html = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "<!DOCTYPE html>" in html
    assert "<html" in html
    assert "</html>" in html
    assert "Quality Score" in html
    assert f"{result['composite_score']} / 100" in html
    for cs in result["column_scores"]:
        assert cs["name"] in html
    for p in profiles:
        assert p["name"] in html
        assert p["type"] in html
