"""Replay the two parent-grade controls stated in Dot's source follow-up."""
from pathlib import Path
import json
import sys

from verify import centered, contrast, laplacian, solve_with_parent_gauge

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "foundational-closure-verification"))
from lineage import Carrier, Pruning


def main():
    prune = Pruning(Carrier("shared", ((), (0,), (1,))), Carrier("shared", ((), (1,))))
    fine_lap = laplacian(3, [(0, 1), (0, 2)])
    coarse_lap = laplacian(2, [(0, 1)])
    cases = {"parent_to_leaf": ([1, 0, 0], [-1, 0, 0, 0]),
             "sibling_to_leaf": ([0, 0, 1], [0, 1, 1, 1])}
    b = [0, 1, 0]
    rows = {}
    for name, (a, expected) in cases.items():
        fine_sources = [centered(x) for x in (a, b)]
        fine = [solve_with_parent_gauge(fine_lap, x) for x in fine_sources]
        coarse = [solve_with_parent_gauge(coarse_lap, list(prune.aggregate(x))) for x in fine_sources]
        actual = [b[0] - a[0], prune.aggregate(b)[0] - prune.aggregate(a)[0],
                  contrast(*fine, 0, 2), contrast(*coarse, 0, 1)]
        if actual != expected:
            raise ValueError(f"Parent or potential contrast mismatch in {name}: {actual}")
        rows[name] = [str(v) for v in actual]
    print(json.dumps({"columns": ["parent_grade_before", "parent_grade_after",
                                  "parent_minus_sibling_before", "parent_minus_sibling_after"],
                      "contrasts_b_minus_a": rows, "status": "PASS"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
