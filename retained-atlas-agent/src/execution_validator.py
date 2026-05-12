import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path):
    if not path.exists():
        return None, f"Missing results file: {path}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as e:
        return None, f"Could not parse JSON: {e}"


def find_controller_rows(data):
    rows = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                row = value.copy()
                row["_name"] = key
                rows.append(row)

    return rows


def is_saturated(x):
    if x is None:
        return False
    try:
        return float(x) <= 0.0 or float(x) >= 1.0
    except Exception:
        return False


def validate(data):
    failures = []
    warnings = []

    if data is None:
        return {
            "interpretation_allowed": False,
            "overall_status": "fail",
            "failures": ["No JSON data available."],
            "warnings": [],
            "controller_checks": [],
        }

    rows = find_controller_rows(data)

    if not rows:
        failures.append("No controller/result rows found.")

    controller_checks = []

    for row in rows:
        name = row.get("_name", "unknown")

        trigger_rate = row.get("trigger_rate")
        bad_rate = row.get("bad_rate")
        auc = row.get("AUC", row.get("auc"))
        validity_gate = row.get("validity_gate", {})
        valid_for_interpretation = validity_gate.get("valid_for_interpretation")

        row_failures = []
        row_warnings = []

        if trigger_rate is not None and is_saturated(trigger_rate):
            row_failures.append("trigger_rate_saturated")

        if bad_rate is not None:
            try:
                br = float(bad_rate)
                if br <= 0.0 or br >= 1.0:
                    row_failures.append("bad_rate_saturated")
                elif not (0.05 <= br <= 0.95):
                    row_warnings.append("bad_rate_extreme")
            except Exception:
                row_warnings.append("bad_rate_unreadable")

        if auc is None:
            row_warnings.append("auc_missing")
        else:
            try:
                float(auc)
            except Exception:
                row_failures.append("auc_invalid")

        if valid_for_interpretation is False:
            row_failures.append("validity_gate_false")

        horizon_area = row.get("horizon_area")
        horizon_width = row.get("horizon_width")

        if horizon_area == 0.0 and horizon_width == 0.0:
            row_warnings.append("horizon_metrics_zero")

        controller_checks.append(
            {
                "name": name,
                "trigger_rate": trigger_rate,
                "bad_rate": bad_rate,
                "auc": auc,
                "valid_for_interpretation": valid_for_interpretation,
                "failures": row_failures,
                "warnings": row_warnings,
            }
        )

    valid_rows = [
        r for r in controller_checks
        if not r["failures"]
    ]

    if not valid_rows:
        failures.append("No fully interpretable result rows found.")

    if len(valid_rows) < 2 and len(rows) >= 2:
        failures.append("Fewer than two valid rows available for comparison.")

    interpretation_allowed = len(failures) == 0

    return {
        "interpretation_allowed": interpretation_allowed,
        "overall_status": "pass" if interpretation_allowed else "fail",
        "failures": failures,
        "warnings": warnings,
        "valid_row_count": len(valid_rows),
        "total_row_count": len(rows),
        "controller_checks": controller_checks,
    }


def write_markdown(version, validation):
    lines = [
        f"# {version} — Execution Validation",
        "",
        f"## Overall Status",
        validation["overall_status"],
        "",
        f"## Interpretation Allowed",
        str(validation["interpretation_allowed"]),
        "",
        "## Failures",
    ]

    if validation["failures"]:
        for f in validation["failures"]:
            lines.append(f"- {f}")
    else:
        lines.append("- None")

    lines += ["", "## Controller Checks"]

    for row in validation["controller_checks"]:
        lines += [
            "",
            f"### {row['name']}",
            f"- trigger_rate: {row['trigger_rate']}",
            f"- bad_rate: {row['bad_rate']}",
            f"- auc: {row['auc']}",
            f"- valid_for_interpretation: {row['valid_for_interpretation']}",
            f"- failures: {row['failures']}",
            f"- warnings: {row['warnings']}",
        ]

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    version = args.version
    run_dir = ROOT / "runs" / version
    result_path = run_dir / f"{version}_results.json"

    data, error = read_json(result_path)

    if error:
        validation = {
            "interpretation_allowed": False,
            "overall_status": "fail",
            "failures": [error],
            "warnings": [],
            "valid_row_count": 0,
            "total_row_count": 0,
            "controller_checks": [],
        }
    else:
        validation = validate(data)

    json_path = run_dir / f"{version}_validation.json"
    md_path = run_dir / f"{version}_validation.md"

    json_path.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    md_path.write_text(write_markdown(version, validation), encoding="utf-8")

    print(json.dumps(validation, indent=2))
    print(f"\nSaved validation: {json_path}")
    print(f"Saved validation report: {md_path}")


if __name__ == "__main__":
    main()
