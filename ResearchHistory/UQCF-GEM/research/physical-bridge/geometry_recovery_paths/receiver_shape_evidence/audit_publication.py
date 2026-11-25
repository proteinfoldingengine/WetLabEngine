"""Read the four original workflow archives and the two independent job-log markers."""
import base64
from hashlib import sha256
import json
import lzma
from pathlib import Path
import re
import sys
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SCI = HERE.parent
sys.path.insert(0, str(SCI))
from fixed_pair_evidence.audit_publication import manifest, need, object_

INHERITED = "e61d5b0e827f7b412824ad46021e2ad6cc6f7875"
OUTPUTS = ("receiver_shape_traces.json.xz", "receiver_shape_certificate.json")


def scientific(z, head, replay):
    manifest(z)
    headfile = "science-head.txt" if replay else "workflow-head.txt"
    need(z.read(headfile).decode().strip() == head, "scientific checkout")
    sums = {}
    for name in OUTPUTS:
        raw = z.read(name)
        need(raw == (SCI / name).read_bytes(), "published scientific data " + name)
        sums[name] = sha256(raw).hexdigest()
    cert = object_(z, OUTPUTS[1])
    summary = {k:v for k,v in cert.items() if k not in ("anchored_fixed_example", "per_target")}
    need(summary == object_(z, "independent.log") and summary["histories"] == 5184
         and summary["matched_pairs"] == 2592 and summary["both_first_b"] == 264
         and summary["pairs_with_silent_arm"] == 288 and summary["fixed_target_pairs"] == 144
         and summary["every_order_first_b"] == ["HHS"] and summary["some_orders_first_b"] == ["SHH", "SHS"]
         and len(set(summary["rejecting_controls"])) == 12 and summary["status"] == "PASS", "independent reconstruction")
    payload = lzma.decompress(z.read(OUTPUTS[0]))
    producer = object_(z, "producer.log" if replay else "fresh.log")
    need(producer == dict(archived_calls=5184, raw_sha256=sha256(payload).hexdigest(), status="PASS"), "primary replay")
    need(len(json.loads(payload)) == producer["archived_calls"], "raw trace count")
    if replay:
        need(z.read("historical-head.txt").decode().strip() == INHERITED, "historical checkout")
        for name in z.namelist():
            if name.endswith((".py", ".md")):
                need(z.read(name) == (SCI / name).read_bytes(), "archived source " + name)
    return sums


def main():
    info = json.loads((HERE / "run.json").read_bytes())
    head = info["head"]
    need(head == info["workflow_head"] and info["inherited"] == INHERITED, "revision binding")
    jobs = {job["name"]:job["conclusion"] for job in info["jobs"]}
    need(all(jobs[key] == "success" for key in ("replay", "publication", "foundational-regression")), "science jobs")
    archives = info["archives"]
    expected = {"receiver-shape-" + name for name in ("replay", "foundation", "review", "publication")}
    need(len(archives) == 4 and {a["name"] for a in archives} == expected, "original archives")
    for entry in archives:
        path = HERE / (entry["name"] + ".zip")
        data = path.read_bytes()
        need(len(data) == entry["size"] and "sha256:" + sha256(data).hexdigest() == entry["digest"], entry["name"])
        with ZipFile(path) as z:
            need(z.testzip() is None, "ZIP member integrity")
    with ZipFile(HERE / "receiver-shape-replay.zip") as z:
        sums = scientific(z, head, True)
    with ZipFile(HERE / "receiver-shape-foundation.zip") as z:
        manifest(z)
        need(z.read("workflow-head.txt").decode().strip() == head and z.read("inherited-head.txt").decode().strip()
             == INHERITED, "foundation revisions")
        v = object_(z, "VERIFICATION.json")
        need(v["all_valid"] and v["coverage"]["instances"] == 21 and object_(z, "TEST_RECEIPT.json")["passed"],
             "21 foundational certificates")
        need(sha256(lzma.decompress(z.read("certificates.json.xz"))).hexdigest() ==
             "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6", "foundation bytes")
        for name, count in (("tests.log", 22), ("parent-tests.log", 15), ("historical.log", 2)):
            log = z.read(name).decode()
            need(re.search(r"Ran " + str(count) + r" tests? in ", log) and "\nOK" in log, name)
        foundation = z.read("VERIFICATION.json")
    with ZipFile(HERE / "receiver-shape-publication.zip") as z:
        need(scientific(z, head, False) == sums and z.read("VERIFICATION.json") == foundation, "fresh publication")
        audit_raw = z.read("publication_audit.json")
        audit = json.loads(audit_raw)
    with ZipFile(HERE / "receiver-shape-review.zip") as z:
        question, request = z.read("prompt.txt"), z.read("request.json")
        wire = json.loads(request)
        need(wire["contents"][0]["parts"][0]["text"].encode() == question and
             wire["generationConfig"]["maxOutputTokens"] == 6144 and audit["request_sha256"] == sha256(request).hexdigest()
             and audit["prompt_sha256"] == sha256(question).hexdigest() and audit["checkout_sha"] == head
             and audit["workflow_sha"] == head and audit["run_id"] == str(info["run_id"])
             and audit["attempt"] == str(info["attempt"]), "external argument binding")
        if "model_metadata.json" in z.namelist():
            model = object_(z, "model_metadata.json")
            need(model["name"] == "models/" + audit["model_requested"] and
                 "generateContent" in model["supportedGenerationMethods"], "model identity")
        if "provider_error.json" in z.namelist():
            marker = "provider_error.json"
            error = object_(z, marker)
            need(audit == dict(audit="SCIENTIFIC_REPLAY_ONLY", **error) and
                 error["external_review"] == "NO_MODEL_VERDICT" and 400 <= error["http_status"] < 600 and
                 not set(z.namelist()) & {"response.json", "receipt.json", "review.txt"} and
                 jobs["argument-review"] == info["conclusion"] == "failure", "provider failure")
            status = "PENDING_HTTP_" + str(error["http_status"])
        else:
            marker = "response.json"
            reply = object_(z, marker)
            text = "\n".join(part["text"] for part in reply["candidates"][0]["content"]["parts"]
                             if "text" in part and not part.get("thought")).strip()
            need(z.read("review.txt") == text.encode() and sha256(z.read(marker)).hexdigest() == audit["response_sha256"]
                 and audit == dict(audit=audit["audit"], **object_(z, "receipt.json")), "original model verdict")
            status = "ACCEPTED" if audit["audit"] == "PASS" else "REVIEW_REQUIRES_ADJUDICATION"
            need((jobs["argument-review"] == "success") == (status == "ACCEPTED"), "review result")
            if status == "ACCEPTED":
                response = json.loads(text)
                need(response["verdict"] == "ACCEPTED" and response["native_bridge_status"] == "OPEN"
                     and all(not response[k] for k in ("findings","counterexamples","missing_assumptions")), "acceptance")
        echoed = dict(line.split("_B64=",1) for line in (HERE/"publication_readback.log").read_text().splitlines())
        need(set(echoed) == {marker, "publication_audit.json"}
             and base64.b64decode(echoed[marker], validate=True) == z.read(marker)
             and base64.b64decode(echoed["publication_audit.json"], validate=True) == audit_raw, "job log readback")
    return dict(science_head=head, run_id=info["run_id"], histories=5184, matched_pairs=2592,
                fixed_target_pairs=144, both_first_b=264, every_order_targets=["HHS"],
                rejecting_controls=12, foundational_certificates=21, inherited_tests=[22,15,2],
                scientific_replay="PASS", fresh_publication="PASS", external_review=status, outputs_sha256=sums)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
