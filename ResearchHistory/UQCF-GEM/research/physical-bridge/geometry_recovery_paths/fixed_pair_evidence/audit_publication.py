"""Audit the native run, foundation, review disposition and fresh checkout from original ZIPs."""
import base64
from hashlib import sha1, sha256
import json
import lzma
from pathlib import Path
import re
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
SCI = HERE.parent
OUTPUTS = ("fixed_pair_certificate.json", "fixed_pair_universe.json.xz", "fixed_pair_matched.json.xz")


def need(test, msg):
    if not test:
        raise ValueError(msg)


def object_(archive, name):
    return json.loads(archive.read(name))


def manifest(z):
    lines = [line.split("  ", 1) for line in z.read("SHA256SUMS").decode().splitlines()]
    files = set(z.namelist()) - {"SHA256SUMS"}
    need({name for _, name in lines} == files and len(lines) == len(files), "incomplete file manifest")
    for hashed, name in lines:
        need(sha256(z.read(name)).hexdigest() == hashed, name)


def main(directory=HERE, *, receiver=False):
    info = json.loads((directory / "run.json").read_bytes())
    science = directory.parent
    prefix = "receiver-turn-" if receiver else "fixed-pair-"
    outputs = OUTPUTS + ("receiver_turn_certificate.json", "receiver_turn_universe.json.xz") if receiver else OUTPUTS
    expected = {prefix + k for k in ("replay", "foundation", "review", "publication")}
    need({a["name"] for a in info["archives"]} == expected and len(info["archives"]) == 4, "four original ZIPs")
    for item in info["archives"]:
        data = (directory / (item["name"] + ".zip")).read_bytes()
        need(len(data) == item["size"] and "sha256:" + sha256(data).hexdigest() == item["digest"], item["name"])
    jobs = {j["name"]: j["conclusion"] for j in info["jobs"]}
    need(all(jobs[k] == "success" for k in ("replay", "publication", "foundational-regression")), "scientific jobs")
    need(info["head"] == info["workflow_head"] and info["inherited"] == "e61d5b0e827f7b412824ad46021e2ad6cc6f7875",
         "source revisions")
    byte_sets = {}
    for job, headfile in (("replay", "science-head.txt"), ("publication", "workflow-head.txt")):
        with ZipFile(directory / (prefix + job + ".zip")) as z:
            manifest(z)
            need(z.read(headfile).decode().strip() == info["head"], job + " head")
            for name in outputs:
                contents = z.read(name)
                need(contents == (science / name).read_bytes(), "fresh scientific bytes " + name)
                byte_sets[name] = sha256(contents).hexdigest()
            first, second = (object_(z, f) for f in ("independent.log", "matched_independent.log"))
            need(first["status"] == second["status"] == "PASS" and first["rejecting_controls"] == 10 and
                 first["star_preparations"] == 1296 and first["source_deletions"] == 2592 and first["view_pairs"] == 2551 and
                 first["distinguished_joint_root"] == 864 and second["equal_cover_and_contrast"] == 816 and
                 second["equal_cover_contrast_unique_partner"] == 216 and second["pairs"] == 1944, "complete enumerations")
            if receiver:
                rt = object_(z, "receiver_independent.log")
                need(rt == dict(status="PASS", rejecting_controls=9, parent_arrays=42, source_role_pairs=84,
                     histories=168, distinct_parent_pairs=76, sibling_pairs=8, distinguished_receiver_parent=76,
                     matched_source_and_receiver_cover=84, candidate_trials=920, positive_receiver_moves=168),
                     "complete receiver reconstruction")
            if job == "replay":
                need(z.read("historical-head.txt").decode().strip() == info["inherited"], "history")
                for name in z.namelist():
                    if name == "review_fixed_pair.py" and not receiver:
                        data = z.read(name)
                        need(sha1(f"blob {len(data)}\0".encode() + data).hexdigest() ==
                             "63a7f1a41f75c5a024f4e5547af118fb4e3b4df4", "original frozen reviewer")
                    elif name.endswith((".md", ".py")):
                        need(z.read(name) == (science / name).read_bytes(), "archived source " + name)
            else:
                audit_bytes = z.read("publication_audit.json")
                verification = z.read("VERIFICATION.json")
    with ZipFile(directory / (prefix + "foundation.zip")) as z:
        manifest(z)
        need(z.read("inherited-head.txt").decode().strip() == info["inherited"] and
             z.read("workflow-head.txt").decode().strip() == info["head"], "foundation")
        v = object_(z, "VERIFICATION.json")
        need(v["all_valid"] and v["coverage"]["instances"] == 21 and object_(z, "TEST_RECEIPT.json")["passed"]
             and z.read("VERIFICATION.json") == verification, "foundation receipt")
        need(sha256(lzma.decompress(z.read("certificates.json.xz"))).hexdigest() ==
             "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6", "inherited data")
        for file, n in (("tests.log", 22), ("parent-tests.log", 15), ("historical.log", 2)):
            content = z.read(file).decode()
            need(re.search(r"Ran " + str(n) + r" tests? in ", content) and "\nOK" in content, file)
    audit = json.loads(audit_bytes)
    with ZipFile(directory / (prefix + "review.zip")) as z:
        request = z.read("request.json")
        prompt = z.read("prompt.txt")
        need(json.loads(request)["contents"][0]["parts"][0]["text"].encode() == prompt and
             json.loads(request)["generationConfig"]["maxOutputTokens"] == 6144, "frozen external request")
        need(audit["request_sha256"] == sha256(request).hexdigest() and audit["prompt_sha256"] == sha256(prompt).hexdigest()
             and audit["checkout_sha"] == audit["workflow_sha"] == info["head"] and
             audit["run_id"] == str(info["run_id"]) and audit["attempt"] == str(info["attempt"]), "external binding")
        if "provider_error.json" in z.namelist():
            marker = "provider_error.json"
            err = object_(z, marker)
            need(audit == dict(audit="SCIENTIFIC_REPLAY_ONLY", **err) and err["stage"] in ("generateContent", "model_metadata")
                 and err["external_review"] == "NO_MODEL_VERDICT" and 400 <= err["http_status"] < 600 and
                 not set(z.namelist()) & {"response.json", "review.txt", "receipt.json"} and
                 jobs["argument-review"] == info["conclusion"] == "failure", "provider failure")
            status = "PENDING_HTTP_" + str(err["http_status"])
        else:
            marker = "response.json"
            response = object_(z, marker)
            text = "\n".join(part["text"] for part in response["candidates"][0]["content"]["parts"]
                            if not part.get("thought") and "text" in part).strip()
            reviewed = json.loads(text)
            receipt = object_(z, "receipt.json")
            need(text.encode() == z.read("review.txt") and audit["response_sha256"] == sha256(z.read(marker)).hexdigest()
                 and audit == dict(audit=audit["audit"], **receipt), "original verdict")
            if audit["audit"] == "PASS":
                need(reviewed["verdict"] == "ACCEPTED" and reviewed["native_bridge_status"] == "OPEN" and
                     all(reviewed[k] == [] for k in ("findings", "counterexamples", "missing_assumptions")) and
                     jobs["argument-review"] == info["conclusion"] == "success", "external acceptance")
                status = "ACCEPTED"
            else:
                need(jobs["argument-review"] == info["conclusion"] == "failure", "external objection")
                status = "REVIEW_REQUIRES_ADJUDICATION"
        if "model_metadata.json" in z.namelist():
            metadata = object_(z, "model_metadata.json")
            need(metadata["name"] == "models/" + audit["model_requested"] and
                 "generateContent" in metadata["supportedGenerationMethods"], "model binding")
        echoed = dict(row.split("_B64=", 1) for row in (directory / "publication_readback.log").read_text().splitlines())
        need(set(echoed) == {marker, "publication_audit.json"} and
             base64.b64decode(echoed[marker], validate=True) == z.read(marker) and
             base64.b64decode(echoed["publication_audit.json"], validate=True) == audit_bytes, "original publication output")
    result = dict(run=info["run_id"], science_head=info["head"], scientific_replay="PASS", fresh_publication="PASS",
                external_review=status, foundation_instances=21, certificate_hashes_sha256=byte_sets,
                matched_comparisons=1944, equal_cover_different_joint_root=816, unique_source_partner=216)
    if receiver:
        result.update(receiver_histories=168, receiver_parent_contrasts=76, sibling_parent_nulls=8,
                      receiver_turn_is_supplied=True)
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
