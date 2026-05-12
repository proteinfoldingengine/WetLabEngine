import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Tuple[Any, str | None]:
    if not path.exists():
        return None, f"Missing results file: {path}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as e:
        return None, f"Could not parse JSON: {e}"


def as_float(x, default=None):
    try:
        if x is None:
            return default
        value = float(x)
        if math.isnan(value) or math.isinf(value):
            return default
        return value
    except Exception:
        return default


def find_result_rows(data: Any) -> List[Dict[str, Any]]:
    """
    Robustly find possible result/controller/regime rows in common result shapes.
    """
    rows = []

    if not isinstance(data, dict):
        return rows

    # Common top-level controller rows:
    # {"A_norm": {...}, "D_A": {...}, "combined": {...}}
    for key, value in data.items():
        if isinstance(value, dict):
            row = value.copy()
            row["_name"] = key
            row["_path"] = key
            rows.append(row)

        # Common list containers:
        # {"candidates": [{...}], "controllers": [{...}], "sweep": [{...}]}
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    row = item.copy()
                    row["_name"] = item.get("name", item.get("controller", f"{key}_{i}"))
                    row["_path"] = f"{key}[{i}]"
                    rows.append(row)

    # Common nested selected regime:
    for key in ["chosen_regime", "chosen_result", "selected_regime", "selected_result"]:
        value = data.get(key)
        if isinstance(value, dict):
            row = value.copy()
            row["_name"] = key
            row["_path"] = key
            rows.append(row)

    return rows


def get_phase_bad(row: Dict[str, Any]):
    phase_counts = row.get("phase_counts", {})
    if isinstance(phase_counts, dict):
        for key in ["bad", "bad_basin", "failed", "collapse"]:
            if key in phase_counts:
                return as_float(phase_counts.get(key), None)
    return None


def row_validity(row: Dict[str, Any]) -> Dict[str, Any]:
    name = row.get("_name", "unknown")

    trigger_rate = as_float(row.get("trigger_rate"), None)
    bad_rate = as_float(row.get("bad_rate"), None)
    auc = as_float(row.get("AUC", row.get("auc")), None)
    balanced_accuracy = as_float(row.get("balanced_accuracy"), None)
    horizon_area = as_float(row.get("horizon_area"), None)
    horizon_width = as_float(row.get("horizon_width"), None)
    score_var = as_float(row.get("score_var", row.get("variance")), None)
    phase_bad = get_phase_bad(row)

    validity_gate = row.get("validity_gate", {})
    valid_for_interpretation = None
    if isinstance(validity_gate, dict):
        valid_for_interpretation = validity_gate.get("valid_for_interpretation")

    failures = []
    warnings = []

    # Core scientific degeneracy checks.
    if bad_rate is None:
        warnings.append("bad_rate_missing")
    elif bad_rate <= 0.0:
        failures.append("bad_rate_zero")
    elif bad_rate >= 1.0:
        failures.append("bad_rate_saturated_one")
    elif not (0.05 <= bad_rate <= 0.95):
        warnings.append("bad_rate_extreme")

    if trigger_rate is None:
        warnings.append("trigger_rate_missing")
    elif trigger_rate <= 0.0:
        failures.append("trigger_rate_zero")
    elif trigger_rate >= 1.0:
        failures.append("trigger_rate_saturated_one")
    elif trigger_rate <= 0.05:
        failures.append("trigger_rate_too_low")

    if horizon_area is not None or horizon_width is not None:
        ha = horizon_area if horizon_area is not None else 0.0
        hw = horizon_width if horizon_width is not None else 0.0
        if ha <= 0.0 and hw <= 0.0:
            warnings.append("horizon_metrics_zero")

    if phase_bad is not None and phase_bad <= 0:
        failures.append("phase_counts_bad_zero")

    if auc is None:
        warnings.append("auc_missing_or_undefined")
    elif not (0.0 <= auc <= 1.0):
        failures.append("auc_invalid")
    elif auc == 0.5:
        warnings.append("auc_at_chance")

    if balanced_accuracy is None:
        warnings.append("balanced_accuracy_missing")
    elif not (0.0 <= balanced_accuracy <= 1.0):
        failures.append("balanced_accuracy_invalid")
    elif balanced_accuracy == 0.5:
        warnings.append("balanced_accuracy_at_chance")

    if score_var is not None and score_var <= 0:
        failures.append("score_variance_zero")

    if valid_for_interpretation is False:
        failures.append("validity_gate_false")

    if valid_for_interpretation is None:
        warnings.append("validity_gate_missing_or_no_valid_for_interpretation")

    row_interpretable = len(failures) == 0

    return {
        "name": name,
        "path": row.get("_path", name),
        "bad_rate": bad_rate,
        "trigger_rate": trigger_rate,
        "auc": auc,
        "balanced_accuracy": balanced_accuracy,
        "horizon_area": horizon_area,
        "horizon_width": horizon_width,
        "score_var": score_var,
        "phase_counts_bad": phase_bad,
        "valid_for_interpretation": valid_for_interpretation,
        "row_interpretable": row_interpretable,
        "failures": failures,
        "warnings": warnings,
    }


def has_selected_regime(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    for key in ["chosen_regime", "chosen_result", "selected_regime", "selected_result"]:
        value = data.get(key)
        if value not in [None, {}, [], "null"]:
            return True
    return False


def validate(data: Any) -> Dict[str, Any]:
    failures = []
    warnings = []

    if data is None:
        return {
            "interpretation_allowed": False,
            "overall_status": "fail",
            "failures": ["No JSON data available."],
            "warnings": [],
            "valid_row_count": 0,
            "total_row_count": 0,
            "selected_regime_present": False,
            "controller_checks": [],
        }

    rows = find_result_rows(data)
    selected_regime_present = has_selected_regime(data)

    if not rows:
        failures.append("No result rows found.")

    controller_checks = [row_validity(row) for row in rows]
    valid_rows = [r for r in controller_checks if r["row_interpretable"]]

    # Global scientific validity checks.
    if not selected_regime_present:
        warnings.append("No selected/chosen regime found.")

    # If the run appears to be a controller comparison, require at least 2 valid comparable rows.
    controller_like_names = [
        "A_norm", "D_A", "duration", "horizon", "combined", "baseline"
    ]
    controller_rows = [
        r for r in controller_checks
        if any(token.lower() in str(r["name"]).lower() for token in controller_like_names)
    ]
    valid_controller_rows = [r for r in controller_rows if r["row_interpretable"]]

    if len(controller_rows) >= 2 and len(valid_controller_rows) < 2:
        failures.append("Fewer than two valid controller rows available for comparison.")

    # If all rows have bad_rate 0/1 or trigger_rate 0/1, the run is scientifically useless.
    if controller_checks:
        bad_rates = [r["bad_rate"] for r in controller_checks if r["bad_rate"] is not None]
        trigger_rates = [r["trigger_rate"] for r in controller_checks if r["trigger_rate"] is not None]
        horizon_pairs = [
            (r["horizon_area"], r["horizon_width"])
            for r in controller_checks
            if r["horizon_area"] is not None or r["horizon_width"] is not None
        ]

        if bad_rates and all(br <= 0.0 or br >= 1.0 for br in bad_rates):
            failures.append("All available bad_rate values are saturated.")

        if trigger_rates and all(tr <= 0.0 or tr >= 1.0 for tr in trigger_rates):
            failures.append("All available trigger_rate values are saturated.")

        if horizon_pairs:
            if all((ha or 0.0) <= 0.0 and (hw or 0.0) <= 0.0 for ha, hw in horizon_pairs):
                failures.append("All available horizon metrics are zero.")

    if not valid_rows:
        failures.append("No fully interpretable rows found.")

    interpretation_allowed = len(failures) == 0

    return {
        "interpretation_allowed": interpretation_allowed,
        "overall_status": "pass" if interpretation_allowed else "fail",
        "failures": failures,
        "warnings": warnings,
        "valid_row_count": len(valid_rows),
        "total_row_count": len(rows),
        "selected_regime_present": selected_regime_present,
        "valid_controller_row_count": len(valid_controller_rows),
        "total_controller_row_count": len(controller_rows),
        "controller_checks": controller_checks,
    }


def write_markdown(version: str, validation: Dict[str, Any]) -> str:
    lines = [
        f"# {version} — Scientific Execution Validation",
        "",
        "## Overall Status",
        validation["overall_status"],
        "",
        "## Interpretation Allowed",
        str(validation["interpretation_allowed"]),
        "",
        "## Selected Regime Present",
        str(validation.get("selected_regime_present")),
        "",
        "## Row Counts",
        f"- valid_row_count: {validation.get('valid_row_count')}",
        f"- total_row_count: {validation.get('total_row_count')}",
        f"- valid_controller_row_count: {validation.get('valid_controller_row_count')}",
        f"- total_controller_row_count: {validation.get('total_controller_row_count')}",
        "",
        "## Failures",
    ]

    if validation["failures"]:
        for f in validation["failures"]:
            lines.append(f"- {f}")
    else:
        lines.append("- None")

    lines += ["", "## Warnings"]

    if validation["warnings"]:
        for w in validation["warnings"]:
            lines.append(f"- {w}")
    else:
        lines.append("- None")

    lines += ["", "## Row Checks"]

    for row in validation["controller_checks"]:
        lines += [
            "",
            f"### {row['name']}",
            f"- path: {row['path']}",
            f"- row_interpretable: {row['row_interpretable']}",
            f"- bad_rate: {row['bad_rate']}",
            f"- trigger_rate: {row['trigger_rate']}",
            f"- auc: {row['auc']}",
            f"- balanced_accuracy: {row['balanced_accuracy']}",
            f"- horizon_area: {row['horizon_area']}",
            f"- horizon_width: {row['horizon_width']}",
            f"- score_var: {row['score_var']}",
            f"- phase_counts_bad: {row['phase_counts_bad']}",
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
            "selected_regime_present": False,
            "valid_controller_row_count": 0,
            "total_controller_row_count": 0,
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
