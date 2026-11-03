"""PR107 frozen analytical review only. No scientific program is executed."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

FREEZE_SHA = "fe57d057aa42ca934d6b29721a7f07f237b9d876"
REPO = "proteinfoldingengine/WetLabEngine"
BRANCH = "gpt/single-event-challenge-scope-20261020"
BASE = "ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain_challenge/review"
NOTE = "GPT_CHALLENGE_SCOPE_CLARIFICATION.md"
MARKER = ".github/uqcf_challenge_scope_review.trigger"
WORKFLOW = ".github/workflows/uqcf-challenge-scope-review.yml"
OUT = Path("challenge_scope_review")
HELPERS = {
    ".github/scripts/uqcf_preparability_review.py": "5df876c5f878f069b4b1bcc31b0d7d0d651ab07feb8ef9b30f4613f06543e6a1",
    ".github/scripts/uqcf_preparability_integrity.py": "4698601ef060de2bca10331f3f05fd35d01d4b7bee0336d309985195e306f18b",
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON field")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode()


def write(name, value):
    (OUT / name).write_bytes(encoded(value))


def git(*args):
    return subprocess.check_output(["git", *args]).decode().strip()


def remote(sha, path):
    require(re.fullmatch(r"[0-9a-f]{40}", sha), "Immutable SHA required")
    require(isinstance(path, str) and path and not path.startswith("/")
            and "\\" not in path and "\x00" not in path
            and all(p not in ("", ".", "..") for p in path.split("/")),
            "Invalid source path")
    url = "https://raw.githubusercontent.com/" + REPO + "/" + sha + "/" + urllib.parse.quote(path, safe="/")
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def verify_target(lock, raw):
    require(type(lock["bytes"]) is int and len(raw) == lock["bytes"], "Target byte count")
    require(digest(raw) == lock["sha256"], "Target SHA256")
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(blob == lock["git_blob"], "Target Git blob")
    raw.decode("utf-8")


def verify_source(source, full):
    path = source["path"]
    require(isinstance(path, str) and path and not path.startswith("/")
            and "\\" not in path and "\x00" not in path
            and all(x not in ("", ".", "..") for x in path.split("/")), "Source path")
    require(type(source["full_bytes"]) is int and len(full) == source["full_bytes"], "Full source size")
    require(digest(full) == source["full_sha256"], "Full source hash")
    blob = hashlib.sha1(b"blob " + str(len(full)).encode() + b"\0" + full).hexdigest()
    require(blob == source["git_blob"], "Full source Git blob")
    start, end = source["byte_start"], source["byte_end"]
    require(type(start) is int and type(end) is int and 0 <= start < end <= len(full), "Source interval")
    require(isinstance(source["content"], str), "Source content type")
    excerpt = source["content"].encode()
    require(full[start:end] == excerpt, "Exact source interval")
    return dict(path=path, full_bytes=len(full), full_sha256=digest(full), git_blob=blob,
                byte_start=start, byte_end=end, excerpt_bytes=len(excerpt), excerpt_sha256=digest(excerpt))


def inputs(fetch=remote):
    docs = {name: Path(BASE, name).read_bytes()
            for name in ("FREEZE.json", "SOURCE_PACKET.json", "REVIEW_PROMPT.md")}
    for name, raw in docs.items():
        raw.decode("utf-8")
        require(raw == fetch(FREEZE_SHA, BASE + "/" + name), "Frozen document mismatch")
    freeze = parse(docs["FREEZE.json"])
    require(freeze["documents"] == {n: digest(docs[n]) for n in ("SOURCE_PACKET.json", "REVIEW_PROMPT.md")},
            "Freeze manifest mismatch")
    require(freeze["model"] == dict(name="gemini-3.1-pro-preview", temperature=0, max_output_tokens=32768,
            response_mime_type="application/json", availability_get_limit=1, generation_request_limit=1,
            automatic_retry=False, workflow_rerun_allowed=False), "Frozen request limits")
    lock = freeze["target"]
    docs[NOTE] = Path(lock["path"]).read_bytes()
    verify_target(lock, docs[NOTE])
    require(docs[NOTE] == fetch(lock["commit"], lock["path"]), "Immutable target mismatch")
    return docs, freeze


def build_prompt(docs):
    require(set(docs) == {NOTE, "SOURCE_PACKET.json", "FREEZE.json", "REVIEW_PROMPT.md"}, "Prompt inputs")
    raw = docs["REVIEW_PROMPT.md"]
    for name in (NOTE, "SOURCE_PACKET.json", "FREEZE.json"):
        value = docs[name]
        raw += ("\nEXACT DOCUMENT " + name + "\nUTF8-BYTES " + str(len(value)) + "\n").encode()
        raw += value + b"\nEND EXACT DOCUMENT\n"
    return raw


def identity(freeze):
    checkout = git("rev-parse", "HEAD")
    require(checkout == os.environ["GITHUB_SHA"] == os.environ["UQCF_WORKFLOW_SHA"], "Checkout/event/workflow SHA")
    require(os.environ["GITHUB_REPOSITORY"] == REPO, "Repository")
    require(os.environ["GITHUB_REF"] == "refs/heads/" + BRANCH, "PR branch")
    require(os.environ["GITHUB_EVENT_NAME"] == "push", "Expected marker push")
    require(os.environ["GITHUB_RUN_ATTEMPT"] == "1", "No workflow rerun permitted")
    return dict(freeze_sha=FREEZE_SHA, target_sha=freeze["target"]["commit"], checkout_sha=checkout,
                workflow_sha=os.environ["UQCF_WORKFLOW_SHA"], run_id=os.environ["GITHUB_RUN_ID"],
                run_attempt=os.environ["GITHUB_RUN_ATTEMPT"])


def marker_gate(freeze):
    parents = git("show", "-s", "--format=%P", "HEAD").split()
    require(len(parents) == 1, "Trigger must have one parent")
    parent = parents[0]
    require(parent == os.environ["UQCF_PUSH_BEFORE"], "Trigger parent differs from trusted pre-push head")
    value = dict(kind="PR107 one-request analytical review trigger", freeze_sha=FREEZE_SHA,
                 target_sha=freeze["target"]["commit"], plumbing_sha=parent)
    require(Path(MARKER).read_bytes() == encoded(value), "Exact trigger marker")
    changes = git("diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD").splitlines()
    require(changes == ["A\t" + MARKER], "Trigger must add only one marker")
    require(git("merge-base", FREEZE_SHA, parent) == FREEZE_SHA, "Freeze is not an ancestor")
    return parent


def github_json(path, token):
    require(token, "Read token missing")
    request = urllib.request.Request("https://api.github.com/repos/" + REPO + path,
        headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json"})
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=60) as response:
        return parse(response.read())


def unique_run_gate(run, api=github_json):
    token = os.environ.get("GH_READ_TOKEN", "")
    current = api("/actions/runs/" + run["run_id"], token)
    require(str(current["id"]) == run["run_id"] and current["run_attempt"] == 1, "Current run identity")
    require(current["head_sha"] == run["checkout_sha"] and current["event"] == "push", "Current trigger identity")
    require(current["path"] == WORKFLOW and current["head_branch"] == BRANCH, "Current workflow identity")
    query = "?branch=" + urllib.parse.quote(BRANCH, safe="") + "&per_page=100"
    listed = api("/actions/workflows/" + str(current["workflow_id"]) + "/runs" + query, token)
    runs = listed["workflow_runs"]
    require(listed["total_count"] == 1 and len(runs) == 1 and str(runs[0]["id"]) == run["run_id"],
            "Prior or concurrent workflow run exists; no duplicate request")
    return dict(workflow_id=current["workflow_id"], eligible_run_id=current["id"], listed_total=1)


def integrity():
    docs, freeze = inputs()
    run = identity(freeze)
    parent = marker_gate(freeze)
    unique = unique_run_gate(run)
    helper_identity = {}
    for path, expected in HELPERS.items():
        raw = Path(path).read_bytes()
        require(digest(raw) == expected, "Pinned helper closure changed")
        require(raw == remote(freeze["target"]["commit"], path), "Immutable helper mismatch")
        helper_identity[path] = expected
    packet = parse(docs["SOURCE_PACKET.json"])
    require(packet["source_commit"] == freeze["research_base_sha"], "Source commit")
    require(isinstance(packet["sources"], list) and packet["sources"], "Empty source packet")
    fetched, rows, seen = {}, [], set()
    for source in packet["sources"]:
        path = source["path"]
        if path not in fetched:
            fetched[path] = remote(packet["source_commit"], path)
        row = verify_source(source, fetched[path])
        key = (path, row["byte_start"], row["byte_end"])
        require(key not in seen, "Duplicate source excerpt")
        seen.add(key)
        rows.append(row)
    expected_prompt = build_prompt(docs)
    write("integrity.json", dict(run, status="PASS", scientific_execution=False,
          documents={name: digest(raw) for name, raw in docs.items()},
          source_commit=packet["source_commit"], sources=rows, helper_identity=helper_identity,
          plumbing_sha=parent, unique_run=unique, expected_prompt_sha256=digest(expected_prompt)))
    print("Frozen inputs, source intervals, marker identity and single-run gate PASS.")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect rejected without forwarding", headers, fp)


class CredentialEcho(ValueError):
    pass


def guarded_model_opener(key, opener):
    """Bound keyed transport; reject redirects, duplicate calls and credential echoes."""
    require(bool(key), "Generation credential missing")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview"
    counts = {"GET": 0, "POST": 0}

    class Response:
        def __init__(self, wrapped):
            self.wrapped = wrapped

        def __enter__(self):
            self.wrapped.__enter__()
            return self

        def __exit__(self, *args):
            return self.wrapped.__exit__(*args)

        def read(self):
            raw = self.wrapped.read()
            if key.encode() in raw:
                (OUT / "credential-echo-redacted.bin").write_bytes(
                    raw.replace(key.encode(), b"[REDACTED-CREDENTIAL]"))
                write("credential-echo.json", dict(original_bytes=len(raw), original_sha256=digest(raw)))
                raise CredentialEcho("Credential echo blocked before helper persistence")
            return raw

    def bounded(request, timeout):
        method = request.get_method()
        require(method in counts, "Unexpected keyed request method")
        expected = endpoint if method == "GET" else endpoint + ":generateContent"
        require(request.full_url == expected, "Unexpected keyed endpoint")
        require(counts[method] == 0, "No keyed request retry")
        require(method == "GET" or counts["GET"] == 1, "Model availability must precede generation")
        require(method != "GET" or counts["POST"] == 0, "Availability after generation")
        counts[method] += 1  # An ambiguous timeout consumes the sole allowance.
        return Response(opener(request, timeout=timeout))
    return bounded


def retain_http_failure(exc, key):
    raw = exc.read()
    sanitized = raw.replace(key.encode(), b"[REDACTED-CREDENTIAL]") if key else raw
    (OUT / "http-error.bin").write_bytes(sanitized)
    safe_headers = {name: value.replace(key, "[REDACTED-CREDENTIAL]") if key else value
                    for name, value in exc.headers.items()
                    if name.lower() in {"date", "content-type", "retry-after", "x-request-id"}}
    write("http-error-metadata.json", dict(status=exc.code, original_bytes=len(raw),
          original_sha256=digest(raw), credential_redacted=sanitized != raw, headers=safe_headers))


def check_verdict(verdict):
    require(isinstance(verdict, dict) and verdict.get("verdict") == "ACCEPTED", "Not accepted")
    require(all(verdict.get(name) == [] for name in ("findings", "missing_assumptions", "counterexamples")),
            "Unresolved substantive objection")
    def has_prose(value):
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, dict):
            return bool(value) and any(has_prose(item) for item in value.values())
        if isinstance(value, list):
            return bool(value) and any(has_prose(item) for item in value)
        return False
    require(isinstance(verdict.get("limitations"), list)
            and all(isinstance(x, (str, dict)) and has_prose(x) for x in verdict["limitations"]),
            "Invalid limitations")
    constructive = verdict.get("constructive_analysis")
    require(isinstance(constructive, list) and constructive and all(isinstance(x, (str, dict)) and has_prose(x)
            for x in constructive), "Missing constructive reconstruction")
    require(verdict.get("native_bridge_status") == "NOT_DERIVED", "Unexpected native derivation claim")
    require(isinstance(verdict.get("next_native_obligation"), str)
            and verdict["next_native_obligation"].strip(), "Missing native obligation")


def review():
    docs, freeze = inputs()
    run = identity(freeze)
    parent = marker_gate(freeze)
    check = parse((OUT / "integrity.json").read_bytes())
    require(check.get("status") == "PASS" and check.get("scientific_execution") is False, "Integrity gate")
    require(all(check.get(k) == v for k, v in run.items()), "Integrity run identity")
    require(check["plumbing_sha"] == parent and check["helper_identity"] == HELPERS, "Plumbing identity")
    require(check["documents"] == {n: digest(raw) for n, raw in docs.items()}, "Input identity")
    for path, expected in HELPERS.items():
        require(digest(Path(path).read_bytes()) == expected, "Helper closure mismatch")
    prompt = build_prompt(docs)
    require(digest(prompt) == check["expected_prompt_sha256"], "Prompt gate")
    (OUT / "prompt.txt").write_bytes(prompt)
    key = os.environ.get("GEMINI_API_KEY", "")
    require(bool(key), "Generation credential missing")
    from uqcf_preparability_review import call_model, parse_response
    opener = urllib.request.build_opener(NoRedirect())
    try:
        raw = call_model(OUT, key, prompt, opener=guarded_model_opener(key, opener.open))
        if key.encode() in raw:
            (OUT / "response.json").write_bytes(raw.replace(key.encode(), b"[REDACTED-CREDENTIAL]"))
            write("credential-redaction.json", dict(original_bytes=len(raw), original_sha256=digest(raw)))
            raise CredentialEcho("Credential echo redacted; exact-response acceptance stopped")
        answer, verdict, model = parse_response(raw)
        (OUT / "review.txt").write_bytes(answer)
        write("verdict.json", verdict)
        write("review_identity.json", dict(run, model_returned=model,
              prompt_sha256=digest(prompt), response_sha256=digest(raw)))
        check_verdict(verdict)
    except urllib.error.HTTPError as exc:
        retain_http_failure(exc, key)
        raise
    finally:
        # The inherited helper persists metadata before parsing it. Sanitize any
        # improbable service echo before the always-upload artifact step.
        for path in list(OUT.iterdir()):
            if path.is_file():
                raw = path.read_bytes()
                if key.encode() in raw:
                    path.write_bytes(raw.replace(key.encode(), b"[REDACTED-CREDENTIAL]"))
                    write("credential-redaction-" + path.name + ".json",
                          dict(original_bytes=len(raw), original_sha256=digest(raw)))
    print("Independent whole-argument review ACCEPTED; native bridge NOT_DERIVED.")


def main():
    require(len(sys.argv) == 2 and sys.argv[1] in {"integrity", "review"}, "Mode required")
    mode = sys.argv[1]
    OUT.mkdir(exist_ok=True)
    try:
        {"integrity": integrity, "review": review}[mode]()
    except Exception as exc:
        write("failure-" + mode + ".json", dict(status="NOT_ACCEPTED_OR_INFRASTRUCTURE_FAILURE",
              error_type=type(exc).__name__, http_status=getattr(exc, "code", None)))
        raise SystemExit("Review gate stopped; sanitized failure retained; no retry.")
    finally:
        write("artifact_manifest.json", {p.name: dict(bytes=p.stat().st_size, sha256=digest(p.read_bytes()))
              for p in OUT.iterdir() if p.is_file() and p.name != "artifact_manifest.json"})


if __name__ == "__main__":
    main()
