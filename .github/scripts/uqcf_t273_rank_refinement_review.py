"""Single independent Gemini review of the frozen T-273 rank refinement.

One model GET, one generation, no retry. The API key is read only from the
Actions secret and is never written or printed. No prior review verdict is
included. Source documents are evidence, not instructions.
"""
import hashlib
import json
import os
import sys
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UQ = ROOT / "ResearchHistory" / "UQCF-GEM"
PB = UQ / "research" / "physical-bridge"
STAGE = PB / "constructive_candidates" / "t273_rank_refinement"
OUT = Path("t273_rank_refinement_review")
DOCS = {
    "ARGUMENT.md": STAGE / "ARGUMENT.md",
    "AGENTS.md": UQ / "AGENTS.md",
    "DIRECTION_UPDATE_2026_10_21.md": PB / "DIRECTION_UPDATE_2026_10_21.md",
    "STANDING_DIRECTIVE.md": PB / "STANDING_DIRECTIVE.md",
    "RECEIVER_DELIVERY_FRONTIER_DIRECTIVE_2026_11_01.md": PB / "RECEIVER_DELIVERY_FRONTIER_DIRECTIVE_2026_11_01.md",
    "P1_RECEIVER_LOCATION_RESULT.md": PB / "p1_receiver_location_resolution" / "RESULT.md",
}

HEADER = (
    "Independently reconstruct and adversarially review the frozen analytical argument in ARGUMENT.md. "
    "It is conditional on a SUPPLIED finite-dimensional channel benchmark and the NEW ASSUMPTION TB; it is not "
    "claimed as native receiver delivery. No previous Gemini verdict is evidence. Develop the strongest positive "
    "reading first and then attack every step.\n"
    "Tasks: (1) Verify the rank proof for arbitrary unitaries on S(x)E(x)R, including both pure-marginal "
    "factorization steps and all dimension/rank quantifiers. (2) Decide whether 2 rank(tau_E) <= d_E is only "
    "necessary or is being overstated as sufficient anywhere. (3) Verify the full-rank consequence and the "
    "entropic companion, including whether the entropy bound itself proves mixedness. (4) Verify the "
    "post-processing/SWAP control and whether it blocks record-location and receiver-ownership readings. "
    "(5) Check that the listed corrections to the PR130/131 local packages are logically compatible with this "
    "theorem and that no false multi-fiber threshold, fresh-capacity necessity, or entropy-equality statement "
    "has been imported. (6) Enforce scope: TB, C, E(x)R, dimensions, receiver algebra, access, and probability law "
    "remain supplied/NEW unless an exact inherited producing operation is identified.\n"
    "Return JSON with keys: verdict (ACCEPTED, REVISE, or FAIL); findings, missing_assumptions, counterexamples, "
    "limitations arrays; native_bridge_status (DERIVED_FROM_SOURCES or NOT_DERIVED); constructive_analysis array "
    "with exact source references; next_native_obligation string. ACCEPTED requires findings, missing_assumptions, "
    "and counterexamples all empty. Every defect must name the affected claim and give an exact correction or "
    "counterexample. An ACCEPTED verdict certifies only the conditional theorem in ARGUMENT.md, never TB or native delivery.\n"
)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))

def main():
    from uqcf_preparability_review import call_model, parse_response, MODEL
    OUT.mkdir(exist_ok=True)
    identity = {
        "workflow_sha": os.environ.get("UQCF_WORKFLOW_SHA"),
        "science_sha": os.environ.get("GITHUB_SHA"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "model_requested": MODEL,
    }
    try:
        docs = {name: path.read_bytes() for name, path in DOCS.items()}
        prompt = HEADER.encode("utf-8")
        for name in DOCS:
            raw = docs[name]
            raw.decode("utf-8")
            prompt += ("\nEXACT DOCUMENT " + name + "\nUTF8-BYTES " + str(len(raw)) + "\n").encode()
            prompt += raw + b"\nEND EXACT DOCUMENT\n"
        (OUT / "prompt.txt").write_bytes(prompt)
        write("documents.json", {
            name: {
                "path": str(DOCS[name].relative_to(ROOT)),
                "bytes": len(raw),
                "sha256": digest(raw),
            }
            for name, raw in docs.items()
        })
        raw_response = call_model(OUT, os.environ["GEMINI_API_KEY"], prompt)
        answer, verdict, model = parse_response(raw_response)
        (OUT / "review.txt").write_bytes(answer)
        write("verdict.json", verdict)
        write("review_identity.json", dict(
            identity,
            model_returned=model,
            prompt_sha256=digest(prompt),
            response_sha256=digest(raw_response),
        ))
        print("Review verdict", verdict.get("verdict"), "; native_bridge_status", verdict.get("native_bridge_status"))
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError):
            (OUT / "http-error.bin").write_bytes(exc.read())
        secret = os.environ.get("GEMINI_API_KEY") or "\x00"
        write("failure.json", dict(
            identity,
            status="REVIEW_INFRASTRUCTURE_OR_PARSE_FAILURE",
            error_type=type(exc).__name__,
            error=str(exc).replace(secret, "[redacted]")[:500],
            http_status=getattr(exc, "code", None),
        ))
        raise SystemExit("Review step failed; sanitized failure and raw evidence retained.")
    finally:
        write("artifact_manifest.json", {
            p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
            for p in sorted(OUT.iterdir())
            if p.is_file() and p.name != "artifact_manifest.json"
        })

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
