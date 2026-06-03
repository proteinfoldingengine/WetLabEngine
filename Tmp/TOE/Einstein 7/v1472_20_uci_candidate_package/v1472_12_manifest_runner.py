#!/usr/bin/env python3
"""
V1472.12 manifest-gated runner.

This wrapper requires a preregistration manifest before invoking the V1472.11 runner.

Usage:
    python v1472_12_manifest_runner.py manifest.json

The manifest must declare threshold and whether the trace is an independent external trace
before scoring.
"""

from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

REQUIRED = [
    "trace_name",
    "trace_source",
    "is_independent_external_trace",
    "input_file",
    "threshold",
    "pilot_small_trace",
    "event_type_mapping",
    "entropy_definition",
    "damaged_repaired_definition",
    "prior_dependency_definition",
    "provenance_definition",
    "claim_boundary",
]

def validate_manifest(m):
    failures = []
    for k in REQUIRED:
        if k not in m:
            failures.append(f"missing_manifest_field:{k}")

    if "threshold" in m:
        try:
            th = float(m["threshold"])
            if not (0 < th <= 1):
                failures.append("threshold_out_of_range")
        except Exception:
            failures.append("threshold_not_float")

    if m.get("is_independent_external_trace") and m.get("pilot_small_trace"):
        # Not forbidden, but must remain explicitly pilot.
        pass

    if m.get("is_independent_external_trace") and float(m.get("threshold", 0)) < 0.70 and not m.get("pilot_small_trace"):
        failures.append("independent_non_pilot_trace_threshold_below_0.70")

    if "prior_dependency_definition" in m and "event" not in str(m["prior_dependency_definition"]).lower():
        failures.append("prior_dependency_definition_must_reference_event_id")

    if "provenance_definition" in m and "cannot satisfy" not in str(m["provenance_definition"]).lower():
        failures.append("provenance_definition_should_state_cannot_satisfy_prior_dependency")

    return failures

def main():
    if len(sys.argv) != 2:
        print("Usage: python v1472_12_manifest_runner.py manifest.json")
        raise SystemExit(2)

    manifest_path = Path(sys.argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures = validate_manifest(manifest)

    if failures:
        out = {
            "decision": "manifest_rejected",
            "failure_reasons": failures,
            "core_axiom": "No pruning-order trace, no empirical geometry claim."
        }
        print(json.dumps(out, indent=2))
        raise SystemExit(1)

    runner = Path(__file__).with_name("v1472_11_run_trace_preregistered.py")
    if not runner.exists():
        out = {
            "decision": "runner_missing",
            "runner_expected": str(runner),
            "failure_reasons": ["v1472_11_run_trace_preregistered.py must be in same directory"]
        }
        print(json.dumps(out, indent=2))
        raise SystemExit(1)

    cmd = [
        sys.executable,
        str(runner),
        str((manifest_path.parent / Path(manifest["input_file"])).resolve() if not Path(manifest["input_file"]).is_absolute() else Path(manifest["input_file"])),
        "--threshold",
        str(manifest["threshold"]),
    ]
    if manifest.get("pilot_small_trace"):
        cmd.append("--pilot-small-trace")

    res = subprocess.run(cmd, capture_output=True, text=True)

    output = {
        "decision": "manifest_accepted_runner_executed" if res.returncode == 0 else "runner_failed",
        "manifest": manifest,
        "runner_returncode": res.returncode,
        "runner_stdout": res.stdout,
        "runner_stderr": res.stderr,
        "independent_empirical_evidence_candidate": bool(manifest.get("is_independent_external_trace")),
        "claim_boundary": (
            "A pass is an empirical evidence candidate only if the trace is genuinely independent. "
            "It is not proof of physical geometry, physical spacetime, GR, or ADM closure."
        )
    }
    out_path = manifest_path.with_suffix(".v1472_12_manifest_run.json")
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    raise SystemExit(res.returncode)

if __name__ == "__main__":
    main()
