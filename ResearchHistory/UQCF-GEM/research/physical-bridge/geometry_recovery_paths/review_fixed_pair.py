"""Challenge the frozen joint-reading proof and preserve the exact review disposition."""
import base64
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from review_cover_return_compact import MODEL, ROOT, accepted, checked, digest, parse_response, wire

SCI = "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/"
DEMOS = "review_sources/ResearchHistory/UQCF-GEM/demos/"
DOCS = {
    SCI + "FIXED_PAIR_FIDELITY.md": "633aa79b44fa9642d53ace360c66f625e8e05257",
    SCI + "FIXED_PAIR_FIDELITY_PLAN.md": "89a12649f8a0d12708b3a84dfefd100e5c8301d4",
    SCI + "FIXED_PAIR_MATCHED_COVER_PLAN.md": "7428a4db132501b916ba2d641319ae135940a2c3",
    SCI + "fixed_pair_certificate.json": "c7a7f2f7734778f053ba396c4b48b784f00872d3",
    SCI + "fixed_pair_matched.json.xz": "a3e75a8fd00b5a3c195630182546978960d50a7e",
    DEMOS + "v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    DEMOS + "v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
}
TOPICS = {"matched_witness", "positive_fidelity", "information_order", "scope"}
QUESTION = """Critically examine the complete attached proof as an independent mathematical reviewer.
For matched_witness compute the four-leaf local vectors, two intersections, joint roots, and cover fields,
and distinguish unique prior partner of S from global uniqueness. For positive_fidelity prove or disprove
its equivalence and test change of coalition, zero and signed grades, and record masking.
For information_order derive both implications on general positive rooted trees, and check the nested
counterexample. For scope trace what the two historical operations actually receive and return, where
the distinction resides and what remains unproved. Attempt explicit counterexamples before accepting.
Return a single JSON object with verdict ACCEPTED, REVISE, or FAIL; findings, missing_assumptions,
counterexamples and limitations arrays; native_bridge_status OPEN unless justified otherwise;
proof_checks keyed matched_witness, positive_fidelity, information_order and scope, with a worked
paragraph under each key. Include exact_checks with keys four_leaf_roots, six_leaf_roots,
cover_matched_contrasts, unique_partner_contrasts, receiver_writes_from_atomic. Use ACCEPTED
only for the entire scoped argument and only with empty substantive objection arrays.
Attached numerical counts are bounded evidence. Independently work the examples; do not attest a
full numerical enumeration you did not perform."""


def prompt():
    files = {file: checked(file, sha) for file, sha in DOCS.items()}
    chunks = [QUESTION, files[SCI + "FIXED_PAIR_FIDELITY.md"].decode()]
    for file, first, last in ((DEMOS + "v16.23-overlap-descent/engine.py", 50, 80),
                              (DEMOS + "v16.26-consistency-increment-law/engine.py", 9, 25)):
        lines = files[file].decode().splitlines()
        chunks.extend([f"Verbatim {file}, lines {first}-{last}", "\n".join(lines[first-1:last])])
    cert = json.loads(files[SCI + "fixed_pair_certificate.json"])
    match = json.loads(lzma.decompress(files[SCI + "fixed_pair_matched.json.xz"]))
    chunks.append(json.dumps(dict(primary=cert["counts"], supplement=match["summary"], witness=match["witness"]),
                             sort_keys=True))
    return ("\n\n".join(chunks) + "\n").encode()


def validate(verdict):
    accepted(verdict)
    checks = verdict.get("proof_checks", {})
    if (verdict["native_bridge_status"] != "OPEN" or set(checks) != TOPICS
            or any(not isinstance(text, str) or len(text.split()) < 15 for text in checks.values())):
        raise ValueError("incomplete argument review")
    expected = dict(four_leaf_roots=[4, 3], six_leaf_roots=[5, 3], cover_matched_contrasts=816,
                    unique_partner_contrasts=216, receiver_writes_from_atomic=0)
    if json.dumps(verdict.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("worked numerical claims do not match")


def main(mode, out):
    if mode not in ("review", "audit"):
        raise ValueError("mode")
    out.mkdir(exist_ok=True, parents=True)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != os.environ["GITHUB_SHA"] or head != os.environ["UQCF_WORKFLOW_SHA"]:
        raise ValueError("frozen-revision mismatch")
    checked(".github/scripts/uqcf_preparability_review.py", "4c8029da503ed57f404e4424ecc243eb3c609347")
    checked(".github/scripts/uqcf_preparability_integrity.py", "50b1043cda14b18b962f7930cf6a4391067a2a96")
    question = prompt()
    request = wire(dict(contents=[dict(role="user", parts=[dict(text=question.decode())])],
                        generationConfig=dict(temperature=0, maxOutputTokens=6144, responseMimeType="application/json")))
    binding = dict(checkout_sha=head, workflow_sha=head, run_id=os.environ["GITHUB_RUN_ID"],
                   attempt=os.environ["GITHUB_RUN_ATTEMPT"], model_requested=MODEL, source_blobs=DOCS,
                   prompt_sha256=digest(question), request_sha256=digest(request))
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + MODEL
    if mode == "review":
        (out / "prompt.txt").write_bytes(question)
        (out / "request.json").write_bytes(request)
        headers = {"x-goog-api-key": os.environ["GEMINI_API_KEY"]}
        stage = "model_metadata"
        try:
            with urlopen(Request(endpoint, headers=headers), timeout=60) as r:
                metadata = r.read()
            (out / "model_metadata.json").write_bytes(metadata)
            info = json.loads(metadata)
            if info.get("name") != "models/" + MODEL or "generateContent" not in info.get("supportedGenerationMethods", []):
                raise ValueError("unexpected model")
            stage = "generateContent"
            with urlopen(Request(endpoint + ":generateContent", data=request,
                                 headers={**headers, "Content-Type": "application/json"}), timeout=420) as r:
                (out / "response.json").write_bytes(r.read())
        except HTTPError as err:
            (out / "provider_error.json").write_bytes(wire(dict(**binding, stage=stage, http_status=err.code,
                                                                external_review="NO_MODEL_VERDICT")))
            print("Provider", stage, "HTTP", err.code, "without a model verdict")
            raise SystemExit(1)
    elif (out / "prompt.txt").read_bytes() != question or (out / "request.json").read_bytes() != request:
        raise ValueError("frozen request readback failed")

    if (out / "provider_error.json").exists():
        error = json.loads((out / "provider_error.json").read_bytes())
        expected = dict(**binding, stage=error["stage"], http_status=error["http_status"], external_review="NO_MODEL_VERDICT")
        if (error != expected or not 400 <= error["http_status"] < 600 or
                any((out / f).exists() for f in ("response.json", "review.txt", "receipt.json"))):
            raise ValueError("ambiguous provider result")
        if error["stage"] == "generateContent" and json.loads((out / "model_metadata.json").read_bytes())["name"] != "models/" + MODEL:
            raise ValueError("model readback")
        audit = dict(audit="SCIENTIFIC_REPLAY_ONLY", **error)
        marker = "provider_error.json"
    else:
        raw = (out / "response.json").read_bytes()
        answer, verdict, model = parse_response(raw)
        receipt = dict(**binding, model_returned=model, verdict=verdict["verdict"], response_sha256=digest(raw))
        if mode == "review":
            (out / "review.txt").write_bytes(answer)
            (out / "receipt.json").write_bytes(wire(receipt))
            validate(verdict)
            print("External verdict", verdict["verdict"])
            return
        if (out / "review.txt").read_bytes() != answer or json.loads((out / "receipt.json").read_bytes()) != receipt:
            raise ValueError("response readback")
        try:
            validate(verdict)
            outcome = "PASS"
        except ValueError:
            outcome = "REVIEW_REQUIRES_ADJUDICATION"
        audit = dict(audit=outcome, **receipt)
        marker = "response.json"
    (out / "publication_audit.json").write_bytes(wire(audit))
    for key in (marker, "publication_audit.json"):
        print(key + "_B64=" + base64.b64encode((out / key).read_bytes()).decode())


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
