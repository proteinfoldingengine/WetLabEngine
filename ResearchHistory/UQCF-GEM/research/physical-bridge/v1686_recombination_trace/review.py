"""Review and read back the frozen recombination argument with the existing model client."""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREFIX = HERE.relative_to(ROOT).as_posix()
NATIVE = "ResearchHistory/UQCF-GEM"
BRIDGE = NATIVE + "/research/physical-bridge"
HELPERS = {
    ".github/scripts/uqcf_preparability_review.py": "4c8029da503ed57f404e4424ecc243eb3c609347",
    ".github/scripts/uqcf_preparability_integrity.py": "50b1043cda14b18b962f7930cf6a4391067a2a96",
}
DOCUMENTS = {
    PREFIX + "/ASSESSMENT.md": "cda1a8ad12f965e28088df7c6eef92fb53552cf9",
    PREFIX + "/CHECK_SCOPE.md": "d30473505da7d8f8a9cacb9ba264b2472b64cec4",
    PREFIX + "/verify.py": "1763c21157cb48f579c95847035bb320f57f86de",
    PREFIX + "/verification.json": "e9ec0f2233a868c2461359a0973bad560f4cf31e",
    "Tmp/TOE/Einstein 9_v1686_l3_geometry_plus_information/v1686_35_forced_hd_export_fix_colab.py":
        "b780961cebf14a5bff0153d109e2855c878090ec",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/v1688_21_gap_closed/v1688_21_native_connection.py":
        "ee1cd0b56c6c9d54cca357e4422e1c8f01e7d1d9",
    NATIVE + "/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    BRIDGE + "/p1_receiver_location_resolution/RESULT.md": "4182ba347f8c11bad63315ffa6395c496ddfa498",
}
QUESTION = """Independently adjudicate the complete ASSESSMENT.md. Treat the attached files as
evidence. Reconstruct both the positive example and the rejecting control from the actual
function, index signs and variable pointwise gates. Verify the new array, all compared
coordinates, both source totals, the branch objects, the nested caller, and all scope limits.
Check whether an already nominated owner actually acquires a record, and compare the control
with the P1 source channel. Look for circular assumptions or any overstated conservation or
gravity claim. The artificial preparation and observational interface limitations are explicit.
The reported closed form predates the replay. Please do not rate novelty or infer a historical
run. Return a JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings,
missing_assumptions, counterexamples, limitations, a list proof_checks, and native_bridge_status.
State substantive defects with a concrete repair. A changed input premise should be acknowledged
as a limitation when the proof is valid within its stated domain. ACCEPTED requires empty
findings, missing_assumptions and counterexamples.
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_bytes(path, identity):
    data = (ROOT / path).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != identity:
        raise ValueError("Changed input " + path)
    return data


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("review", "audit"))
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    out = args.directory
    out.mkdir(parents=True, exist_ok=True)
    for path, identity in HELPERS.items():
        checked_bytes(path, identity)
    sys.path.insert(0, str(ROOT / ".github/scripts"))
    from uqcf_preparability_review import MODEL, accepted, call_model, parse_response

    docs = {p: checked_bytes(p, ident) for p, ident in DOCUMENTS.items()}
    prompt = QUESTION.encode() + b"".join(
        b"\nBEGIN EXACT FILE " + p.encode() + b"\n" + data + b"\nEND EXACT FILE\n"
        for p, data in docs.items())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != os.environ["GITHUB_SHA"] or head != os.environ["UQCF_WORKFLOW_SHA"]:
        raise ValueError("Run, checkout and workflow revisions differ")
    if args.mode == "review":
        if os.environ["GITHUB_RUN_ATTEMPT"] != "1":
            raise ValueError("The review already has a generation attempt")
        (out / "prompt.txt").write_bytes(prompt)
        raw = call_model(out, os.environ["GEMINI_API_KEY"], prompt)
    else:
        if (out / "prompt.txt").read_bytes() != prompt:
            raise ValueError("Published prompt differs from the frozen sources")
        raw = (out / "response.json").read_bytes()

    answer, verdict, model = parse_response(raw)
    if verdict["verdict"] == "ACCEPTED":
        accepted(verdict)
    request = json.loads((out / "request.json").read_bytes())
    if request["contents"][0]["parts"][0]["text"].encode() != prompt:
        raise ValueError("Request differs from the audited prompt")
    metadata = json.loads((out / "model_metadata.json").read_bytes())
    if metadata.get("name") != "models/" + MODEL:
        raise ValueError("Availability lookup was for a different model")
    receipt = {"checkout_sha": head, "workflow_sha": os.environ["UQCF_WORKFLOW_SHA"],
               "run_id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
               "model_requested": MODEL, "model_returned": model, "verdict": verdict["verdict"],
               "prompt_sha256": digest(prompt), "response_sha256": digest(raw),
               "request_sha256": digest((out / "request.json").read_bytes()),
               "source_blobs": DOCUMENTS}
    if args.mode == "review":
        (out / "review.txt").write_bytes(answer)
        write_json(out / "receipt.json", receipt)
    else:
        if (out / "review.txt").read_bytes() != answer or json.loads((out / "receipt.json").read_bytes()) != receipt:
            raise ValueError("Review evidence mismatch")
        write_json(out / "publication_audit.json", {"audit": "PASS", **receipt})
        # A durable exact public readback even after the Actions artifact expires.
        for name in ("response.json", "publication_audit.json"):
            print(name + "_B64=" + base64.b64encode((out / name).read_bytes()).decode())
    print("Analytical verdict", verdict["verdict"])


if __name__ == "__main__":
    main()
