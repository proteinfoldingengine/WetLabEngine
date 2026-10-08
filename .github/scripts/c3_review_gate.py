#!/usr/bin/env python3
"""Audit AI review evidence; never treat an AI verdict as theorem certification."""
import hashlib
import json
import pathlib
import re
import sys

base = pathlib.Path("review_artifact")
report = pathlib.Path("audit_artifact")
report.mkdir(exist_ok=True)
output = {"status": "UNVERIFIED", "reason": None, "verdict": None,
          "scientific_closeout": False}
try:
    manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
    raw = (base / "gemini_review.txt").read_text(encoding="utf-8").strip()
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if digest != manifest.get("response_sha256"):
        raise ValueError("Review response digest mismatch")
    expected = {
        "COUPLED_C3_SAFE_PROBE_SCOPE.md",
        "COUPLED_C3_SAFE_PROBE_RESULT.md",
        "COUPLED_C3_SAFE_PROBE_AUDIT.md",
        "COUPLED_C3_SAFE_PROBE_CLARIFICATION.md",
        "COUPLED_C3_SAFE_PROBE_VERDICT_ADJUDICATION.md",
        "COUPLED_C3_SAFE_PROBE_COORDINATE_AUDIT.md",
    }
    if set(manifest.get("input_sha256", {})) != expected:
        raise ValueError("Unexpected or missing research proof inputs")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("research_commit", ""))):
        raise ValueError("Unpinned research commit")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("workflow_commit", ""))):
        raise ValueError("Unpinned workflow commit")
    # Allow a single Markdown JSON fence, but never infer a verdict from prose.
    if raw.startswith("```"):
        raw = re.sub(r"^\x60{3}(?:json)?\s*|\s*\x60{3}$", "", raw).strip()
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("Gemini response is not a JSON object")
    verdict = obj.get("verdict")
    if verdict not in ("ACCEPTED", "REVISE", "REJECT"):
        raise ValueError("Gemini verdict missing or invalid")
    for key in ("findings", "missing_assumptions", "counterexamples", "limitations"):
        if not isinstance(obj.get(key), list):
            raise ValueError("Missing review list: " + key)
    output.update(status="REVIEW_RECORDED", verdict=verdict,
                  reason="AI verdict recorded; mathematical certification requires separate scrutiny",
                  response_sha256=digest, research_commit=manifest["research_commit"],
                  workflow_commit=manifest["workflow_commit"],
                  findings_count=len(obj["findings"]),
                  missing_assumptions_count=len(obj["missing_assumptions"]),
                  counterexamples_count=len(obj["counterexamples"]))
    if verdict == "REVISE" and not obj["missing_assumptions"] and not obj["counterexamples"]:
        output["status"] = "NEEDS_HUMAN_RECONCILIATION"
        output["reason"] = "REVISE has no listed missing assumptions or counterexamples; inspect findings for actionable objection"
    if verdict == "ACCEPTED" and (obj["missing_assumptions"] or obj["counterexamples"]):
        output["status"] = "NEEDS_HUMAN_RECONCILIATION"
        output["reason"] = "Accepted verdict conflicts with unresolved objections"
except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
    output["reason"] = type(exc).__name__ + ": " + str(exc)

(report / "review_gate.json").write_text(
    json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(output, sort_keys=True))
if output["status"] not in ("REVIEW_RECORDED", "NEEDS_HUMAN_RECONCILIATION"):
    sys.exit(1)
