"""Benchmark dataset generator for DataLens scalability testing.

Generates deterministic CSV files with controlled characteristics:
- Columns 1–10: integers (1–1000)
- Columns 11–15: floats (random decimals)
- Columns 16–18: strings (short words)
- Columns 19–20: mixed (integers + occasional empty strings)
- 5% duplicate rows
- 10% empty strings (concentrated in columns 16–18)

Usage:
    python benchmarks/benchmark_generator.py <rows> <cols> <output_path>
"""

import csv
import random
import sys
from pathlib import Path


WORDS = [
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
    "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
]


def generate_csv(rows: int, cols: int, output_path: str, seed: int = 42) -> None:
    random.seed(seed)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    column_names = [f"col_{i+1:03d}" for i in range(cols)]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(column_names)

        # Pre-generate 5% duplicate rows
        duplicate_count = max(1, rows // 20)
        duplicates = []
        for _ in range(duplicate_count):
            row = _generate_row(cols)
            duplicates.append(row)

        generated = 0
        dup_index = 0

        while generated < rows:
            if generated < duplicate_count and generated % 20 == 0 and dup_index < len(duplicates):
                writer.writerow(duplicates[dup_index])
                dup_index += 1
            else:
                writer.writerow(_generate_row(cols))
            generated += 1


def _generate_row(cols: int) -> list[str]:
    row = []
    for c in range(cols):
        if c < 10:
            row.append(str(random.randint(1, 1000)))
        elif c < 15:
            row.append(f"{random.uniform(0, 1000):.4f}")
        elif c < 18:
            if random.random() < 0.1:
                row.append("")
            else:
                row.append(random.choice(WORDS))
        else:
            if random.random() < 0.05:
                row.append("")
            else:
                row.append(str(random.randint(1, 1000)))
    return row


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python benchmarks/benchmark_generator.py <rows> <cols> <output_path>", file=sys.stderr)
        sys.exit(1)
    generate_csv(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
