"""Unit and integration tests for cli.py."""

import subprocess
import sys
from pathlib import Path

from datalens.loader import load_csv
from datalens.profiler import profile
from datalens.quality import compute_score
from datalens.report import generate


FIXTURES_DIR = Path(__file__).parent / "fixtures"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def _run_main(csv_path: str):
    sys.argv = ["datalens", csv_path]
    from datalens.cli import main
    main()


def test_main_missing_file_exits_nonzero():
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        _run_main(str(FIXTURES_DIR / "nonexistent.csv"))
    assert exc_info.value.code == 1


def test_main_success_prints_summary(capsys):
    csv_path = str(FIXTURES_DIR / "clean_simple.csv")
    _run_main(csv_path)
    captured = capsys.readouterr()
    assert "Report written to:" in captured.out
    assert "Rows:" in captured.out
    assert "Columns:" in captured.out
    assert "Quality Score:" in captured.out


def test_main_integration_clean_simple(tmp_path):
    env = {**__import__("os").environ, "PYTHONPATH": str(Path(__file__).parent.parent / "src")}
    result = subprocess.run(
        [sys.executable, "-m", "datalens", str(FIXTURES_DIR / "clean_simple.csv")],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=env,
    )
    assert result.returncode == 0
    report_path = tmp_path / "reports" / "clean_simple.html"
    assert report_path.exists()
    assert "Report written to:" in result.stdout
    assert "Rows:" in result.stdout
    assert "Columns:" in result.stdout
    assert "Quality Score:" in result.stdout
