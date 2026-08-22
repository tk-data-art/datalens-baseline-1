"""HTML report generation for DataLens.

Renders profiling and quality data into a self-contained HTML file
using a Jinja2 inline template with auto-escaping.
"""

from pathlib import Path

from jinja2 import Environment, BaseLoader

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DataLens — Data Quality Report</title>
    <style>
        body { font-family: system-ui, sans-serif; margin: 2rem; color: #222; }
        h1 { font-size: 1.4rem; border-bottom: 2px solid #333; padding-bottom: 0.5rem; }
        h2 { font-size: 1.1rem; margin-top: 1.5rem; color: #444; }
        table { border-collapse: collapse; width: 100%; margin-top: 0.5rem; }
        th, td { border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }
        th { background: #f5f5f5; font-weight: 600; }
        tr:nth-child(even) { background: #fafafa; }
        .score { font-size: 1.6rem; font-weight: 700; }
        .section { margin-bottom: 1.5rem; }
    </style>
</head>
<body>
    <h1>DataLens — Data Quality Report</h1>

    <div class="section">
        <h2>Overview</h2>
        <table>
            <tr><th>Row count</th><td>{{ row_count }}</td></tr>
            <tr><th>Column count</th><td>{{ col_count }}</td></tr>
            <tr><th>Duplicate rows</th><td>{{ duplicate_row_count }}</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>Quality Score</h2>
        <p class="score">Quality Score: {{ composite_score }} / 100</p>
        <table>
            <tr><th>Column</th><th>Score</th></tr>
            {% for cs in column_scores %}
            <tr><td>{{ cs.name }}</td><td>{{ "%.2f" % cs.score }}</td></tr>
            {% endfor %}
        </table>
    </div>

    <div class="section">
        <h2>Data Types</h2>
        <table>
            <tr><th>Column</th><th>Type</th></tr>
            {% for p in profiles %}
            <tr><td>{{ p.name }}</td><td>{{ p.type }}</td></tr>
            {% endfor %}
        </table>
    </div>

    <div class="section">
        <h2>Missing Values</h2>
        <table>
            <tr><th>Column</th><th>Missing Count</th><th>Missing %</th></tr>
            {% for p in profiles %}
            <tr>
                <td>{{ p.name }}</td>
                <td>{{ p.missing_count }}</td>
                <td>{{ "%.2f" % p.missing_pct }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="section">
        <h2>Unique Values</h2>
        <table>
            <tr><th>Column</th><th>Unique Count</th></tr>
            {% for p in profiles %}
            <tr><td>{{ p.name }}</td><td>{{ p.unique_count }}</td></tr>
            {% endfor %}
        </table>
    </div>

    {% if numeric_columns %}
    <div class="section">
        <h2>Numeric Statistics</h2>
        <table>
            <tr>
                <th>Column</th>
                <th>Min</th>
                <th>Max</th>
                <th>Mean</th>
                <th>Median</th>
                <th>Std</th>
            </tr>
            {% for p in numeric_columns %}
            <tr>
                <td>{{ p.name }}</td>
                <td>{{ p.min }}</td>
                <td>{{ p.max }}</td>
                <td>{{ p.mean }}</td>
                <td>{{ p.median }}</td>
                <td>{{ p.std }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}
</body>
</html>
"""

_env = Environment(loader=BaseLoader(), autoescape=True)


def generate(
    profiles: list[dict],
    result: dict,
    row_count: int,
    duplicate_row_count: int,
    output_path: str,
) -> None:
    """Generate a self-contained HTML report from profiling and quality data.

    Args:
        profiles: ColumnProfile dicts from profiler.profile().
        result: QualityResult dict from quality.compute_score().
        row_count: Total row count from loader.load_csv().
        duplicate_row_count: Duplicate row count (computed by caller).
        output_path: File path to write the HTML report.
    """
    numeric_columns = [p for p in profiles if "min" in p]

    template = _env.from_string(_TEMPLATE)
    html = template.render(
        profiles=profiles,
        column_scores=result["column_scores"],
        composite_score=result["composite_score"],
        row_count=row_count,
        col_count=len(profiles),
        duplicate_row_count=duplicate_row_count,
        numeric_columns=numeric_columns,
    )

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
