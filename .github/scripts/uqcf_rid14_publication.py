"""receiver_identification d14 freeze: separate publication audit. Immutable GitHub readback of the
frozen and code bytes at the run SHA; recomputes artifact digests of the verify and review jobs."""
import base64, hashlib, json, os, urllib.request
from pathlib import Path

REPO = os.environ["GITHUB_REPOSITORY"]
SHA = os.environ["GITHUB_SHA"]
ROOT = "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d14_review"
FILES = [ROOT + "/RESULT.md", ROOT + "/FOLLOWUP.md", ROOT + "/CORRESPONDENCE.md", ROOT + "/FREEZE.md",
         ".github/scripts/uqcf_rid14_producer.py", ".github/scripts/uqcf_rid14_checker.py",
         ".github/scripts/uqcf_rid14_compare.py", ".github/scripts/uqcf_rid14_review.py",
         ".github/scripts/uqcf_rid14_publication.py", ".github/workflows/uqcf-gem-rid14-review.yml"]
FROZEN_RESULT_SHA = "f6cc849663224a5a2c877cd32a6700ecad9df1ea2d4f723a040c66e55dbc38f9"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def readback(path):
    url = "https://api.github.com/repos/%s/contents/%s?ref=%s" % (REPO, path, SHA)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + os.environ["GH_READ_TOKEN"],
                                               "Accept": "application/vnd.github+json"})
    return base64.b64decode(json.loads(urllib.request.urlopen(req, timeout=60).read())["content"])


def main():
    out = Path("rid14_publication")
    out.mkdir(exist_ok=True)
    rep = {"sha": SHA, "run_id": os.environ.get("GITHUB_RUN_ID"), "files": {}}
    ok = True
    for f in FILES:
        remote, local = readback(f), Path(f).read_bytes()
        rep["files"][f] = {"remote_sha256": sha(remote), "match": remote == local}
        ok &= remote == local
    ok &= rep["files"][ROOT + "/RESULT.md"]["remote_sha256"] == FROZEN_RESULT_SHA
    v = json.loads(Path("rid14_verify/compare.json").read_bytes())
    for n, key in (("producer.json", "producer_sha256"), ("checker.json", "checker_sha256")):
        ok &= sha(Path("rid14_verify/" + n).read_bytes()) == v[key]
    m = json.loads(Path("rid14_review/manifest.json").read_bytes())
    for n, h in m["hashes"].items():
        ok &= sha(Path("rid14_review/" + n).read_bytes()) == h
    ok &= m["verify_sha256"] == sha(Path("rid14_verify/compare.json").read_bytes())
    rep.update({"verify_status": v["status"], "verdict": m["verdict"], "model_returned": m["model_returned"],
                "review_sha256": m["hashes"]["review.txt"], "status": "PASS" if ok else "FAIL"})
    (out / "publication.json").write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    print(json.dumps(rep, indent=1, sort_keys=True))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
