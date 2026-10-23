"""Independent, read-only PR107 publication audit; no model/science imports.

Only immutable raw GitHub files are fetched. The review producer and its
decision helpers are deliberately not imported. All validation functions accept
bytes or injectable read-only dependencies for offline plumbing tests.
"""
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import urllib.error
import urllib.parse
import urllib.request


FREEZE_SHA = "fe57d057aa42ca934d6b29721a7f07f237b9d876"
TARGET_SHA = "0eb63cf6c6a5ea74310ea45b689dc4458923342b"
SOURCE_SHA = "b2831f6f31904c6a981297c7bf4ce570698ec955"
REPOSITORY = "proteinfoldingengine/WetLabEngine"
BRANCH = "gpt/single-event-challenge-scope-20261020"
PREFIX = ("ResearchHistory/UQCF-GEM/research/physical-bridge/"
          "single_event_receiver_gain_challenge/")
FREEZE_PREFIX = PREFIX + "review/"
TARGET_NAME = "GPT_CHALLENGE_SCOPE_CLARIFICATION.md"
MODEL = "gemini-3.1-pro-preview"
MARKER = ".github/uqcf_challenge_scope_review.trigger"
OUT = Path("challenge_scope_review")
DEST = Path("challenge_scope_publication")
REVIEW_MEMBERS = frozenset((
    "integrity.json", "prompt.txt", "model_metadata.json", "request.json",
    "response.json", "review.txt", "verdict.json", "review_identity.json",
))
BASE_FIELDS = ("freeze_sha", "target_sha", "checkout_sha", "workflow_sha",
               "run_id", "run_attempt")
REVIEW_FIELDS = frozenset(BASE_FIELDS + (
    "model_returned", "prompt_sha256", "response_sha256",
))
VERDICT_FIELDS = frozenset((
    "verdict", "findings", "missing_assumptions", "counterexamples",
    "limitations", "constructive_analysis", "native_bridge_status",
    "next_native_obligation",
))
TARGET_IDENTITY = {
    "bytes": 9759,
    "sha256": "30bec269c5b625cd3ccd586f7de426862d7487d3cb5e6d55d4b52ee485920e3c",
    "git_blob": "af83d58cdbe3f201ef84729bd0c376899761a60a",
}
FROZEN_DOCUMENTS = {
    "FREEZE.json": {
        "bytes": 5157,
        "sha256": "a7e76f13e52e0c43a6662790e7baa4284c846be930641a7e45f5716af673b355",
        "git_blob": "ffb48e5d709130e8e73cac47112d96b06c75ccd8",
    },
    "SOURCE_PACKET.json": {
        "bytes": 123788,
        "sha256": "675dd2bf73bd62d18146af5aec8a5f8e6e31d475ac2bc1e47a6602ec6b634832",
        "git_blob": "7e5c8ef732c3dac5d06ca8e4f92384946e6819a0",
    },
    "REVIEW_PROMPT.md": {
        "bytes": 5609,
        "sha256": "8874d4b526372e84302e0b2674801cf5be11775132626cba3c0d16f81c761831",
        "git_blob": "c8074bc4b77f75bf24e39f6890567b4c9b14b033",
    },
}
# Complete non-stdlib closure of the producer's reused model-call helper.
# Verify these as data; never import them into the independent auditor.
HELPER_IDENTITIES = {
    ".github/scripts/uqcf_preparability_review.py": {
        "bytes": 9903,
        "sha256": "5df876c5f878f069b4b1bcc31b0d7d0d651ab07feb8ef9b30f4613f06543e6a1",
        "git_blob": "4c8029da503ed57f404e4424ecc243eb3c609347",
    },
    ".github/scripts/uqcf_preparability_integrity.py": {
        "bytes": 8570,
        "sha256": "4698601ef060de2bca10331f3f05fd35d01d4b7bee0336d309985195e306f18b",
        "git_blob": "50b1043cda14b18b962f7930cf6a4391067a2a96",
    },
}
HELPERS = {path: value["sha256"] for path, value in HELPER_IDENTITIES.items()}
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
MAX_REMOTE_BYTES = 8 * 1024 * 1024


class AuditError(ValueError):
    """A fixed, nonsecret reason code, safe to retain in failure metadata."""


def check(condition, code):
    if not condition:
        raise AuditError(code)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(raw):
    return {
        "bytes": len(raw),
        "sha256": sha256(raw),
        "git_blob": hashlib.sha1(
            b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        ).hexdigest(),
    }


def parse_json(raw):
    """Reject ambiguous duplicate names, non-UTF-8, NaN and Infinity."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            check(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def invalid_constant(_value):
        raise AuditError("NONFINITE_JSON_NUMBER")

    def finite_float(value):
        result = float(value)
        check(math.isfinite(result), "NONFINITE_JSON_NUMBER")
        return result

    try:
        text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
        check(isinstance(text, str), "INVALID_JSON_INPUT")
        return json.loads(text, object_pairs_hook=unique, parse_float=finite_float,
                          parse_constant=invalid_constant)
    except AuditError:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError):
        raise AuditError("INVALID_JSON") from None


def path_is_safe(path):
    return (isinstance(path, str) and bool(path)
            and "\\" not in path and "\x00" not in path
            and not PurePosixPath(path).is_absolute()
            and all(part not in ("", ".", "..") for part in path.split("/"))
            and str(PurePosixPath(path)) == path)


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def same_json(left, right):
    """JSON value equality without Python's false == 0 / true == 1 shortcut."""
    return json.dumps(left, ensure_ascii=False, allow_nan=False, sort_keys=True) == \
        json.dumps(right, ensure_ascii=False, allow_nan=False, sort_keys=True)


def require_identity(raw, expected, code):
    check(isinstance(raw, bytes), "NONBYTE_DOCUMENT")
    check(isinstance(expected, dict)
          and set(expected) == {"bytes", "sha256", "git_blob"}
          and type(expected["bytes"]) is int
          and identity(raw) == expected, code)
    try:
        raw.decode("utf-8")
    except UnicodeError:
        raise AuditError("NON_UTF8_DOCUMENT") from None


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise AuditError("IMMUTABLE_FETCH_REDIRECT")


def fetch(sha, path):
    """One uncredentialed GET of an immutable repository path; no retry."""
    check(valid_sha(sha), "UNPINNED_REMOTE_COMMIT")
    check(path_is_safe(path), "UNSAFE_REMOTE_PATH")
    url = ("https://raw.githubusercontent.com/" + REPOSITORY + "/" + sha
           + "/" + urllib.parse.quote(path, safe="/"))
    request = urllib.request.Request(url, method="GET")
    with urllib.request.build_opener(NoRedirects()).open(request, timeout=60) as response:
        check(response.geturl() == url, "IMMUTABLE_FETCH_URL_CHANGED")
        raw = response.read(MAX_REMOTE_BYTES + 1)
    check(len(raw) <= MAX_REMOTE_BYTES, "OVERSIZED_REMOTE_DOCUMENT")
    return raw


def read_regular_file(path, limit=MAX_ARTIFACT_BYTES):
    """Reject links, directories and oversized files before reading bytes."""
    path = Path(path)
    info = path.lstat()
    check(stat.S_ISREG(info.st_mode), "NONREGULAR_EVIDENCE_FILE")
    check(info.st_size <= limit, "OVERSIZED_EVIDENCE_FILE")
    raw = path.read_bytes()
    check(len(raw) == info.st_size, "EVIDENCE_CHANGED_DURING_READ")
    return raw


def read_review_artifacts(directory):
    directory = Path(directory)
    check(not directory.is_symlink() and directory.is_dir(),
          "INVALID_REVIEW_DIRECTORY")
    names = {entry.name for entry in directory.iterdir()}
    check(names == REVIEW_MEMBERS | {"artifact_manifest.json"},
          "UNEXPECTED_OR_MISSING_REVIEW_MEMBERS")
    manifest_raw = read_regular_file(directory / "artifact_manifest.json")
    manifest = parse_json(manifest_raw)
    check(isinstance(manifest, dict) and set(manifest) == REVIEW_MEMBERS,
          "UNEXPECTED_REVIEW_MANIFEST_MEMBERS")
    artifacts = {}
    for name in sorted(REVIEW_MEMBERS):
        locked = manifest[name]
        check(isinstance(locked, dict)
              and set(locked) == {"bytes", "sha256"}
              and type(locked["bytes"]) is int
              and locked["bytes"] >= 0
              and isinstance(locked["sha256"], str)
              and re.fullmatch(r"[0-9a-f]{64}", locked["sha256"]) is not None,
              "INVALID_REVIEW_MANIFEST_RECORD")
        raw = read_regular_file(directory / name)
        check(locked == {"bytes": len(raw), "sha256": sha256(raw)},
              "REVIEW_MEMBER_HASH_MISMATCH")
        artifacts[name] = raw
    return artifacts, manifest, manifest_raw


def current_identity(environ=None, git_head=None):
    """Bind both jobs to the live Actions repository/ref/event/checkout/run."""
    env = os.environ if environ is None else environ
    check(valid_sha(FREEZE_SHA), "FREEZE_SHA_NOT_PINNED")
    if git_head is None:
        git_head = subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
    workflow_sha = env.get("UQCF_WORKFLOW_SHA")
    check(env.get("GITHUB_REPOSITORY") == REPOSITORY, "WRONG_REPOSITORY")
    check(env.get("GITHUB_REF") == "refs/heads/" + BRANCH, "WRONG_BRANCH")
    check(env.get("GITHUB_EVENT_NAME") == "push", "WRONG_EVENT_TYPE")
    check(valid_sha(git_head) and git_head == env.get("GITHUB_SHA")
          == workflow_sha, "EVENT_CHECKOUT_WORKFLOW_MISMATCH")
    check(env.get("GITHUB_WORKFLOW_SHA", workflow_sha) == workflow_sha,
          "GITHUB_WORKFLOW_SHA_MISMATCH")
    check(env.get("GITHUB_RUN_ATTEMPT") == "1", "WORKFLOW_RERUN_FORBIDDEN")
    run_id = env.get("GITHUB_RUN_ID")
    check(isinstance(run_id, str)
          and re.fullmatch(r"[1-9][0-9]*", run_id) is not None,
          "INVALID_RUN_ID")
    return {
        "freeze_sha": FREEZE_SHA, "target_sha": TARGET_SHA,
        "checkout_sha": git_head, "workflow_sha": workflow_sha,
        "run_id": run_id, "run_attempt": "1",
    }


def git_bytes(*arguments):
    return subprocess.check_output(["git", *arguments], stderr=subprocess.DEVNULL)


def audit_trigger(integrity, run, environ=None, git_reader=None, marker_reader=None):
    """Check the trusted push-before SHA against the actual commit and marker."""
    env = os.environ if environ is None else environ
    git_read = git_bytes if git_reader is None else git_reader
    before = env.get("UQCF_PUSH_BEFORE")
    check(valid_sha(before) and before != "0" * 40
          and integrity.get("plumbing_sha") == before,
          "PUSH_BEFORE_PLUMBING_MISMATCH")
    parent_bytes = git_read("show", "-s", "--format=%P", "HEAD")
    check(parent_bytes.decode("ascii").strip().split() == [before],
          "TRIGGER_PARENT_MISMATCH")
    changes = git_read("diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD")
    check(changes.decode("utf-8").splitlines() == ["A\t" + MARKER],
          "TRIGGER_NOT_MARKER_ONLY")
    check(git_read("merge-base", FREEZE_SHA, before).decode("ascii").strip()
          == FREEZE_SHA, "FREEZE_NOT_ANCESTOR")
    expected = (json.dumps({
        "kind": "PR107 one-request analytical review trigger",
        "freeze_sha": FREEZE_SHA, "target_sha": TARGET_SHA,
        "plumbing_sha": before,
    }, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    marker = (read_regular_file(Path(MARKER)) if marker_reader is None
              else marker_reader(MARKER))
    check(marker == expected and git_read("show", "HEAD:" + MARKER) == expected,
          "EXACT_TRIGGER_MARKER_MISMATCH")
    unique = integrity.get("unique_run")
    check(isinstance(unique, dict)
          and set(unique) == {"workflow_id", "eligible_run_id", "listed_total"}
          and type(unique["workflow_id"]) is int and unique["workflow_id"] > 0
          and type(unique["eligible_run_id"]) is int
          and str(unique["eligible_run_id"]) == run["run_id"]
          and type(unique["listed_total"]) is int and unique["listed_total"] == 1,
          "INVALID_UNIQUE_RUN_EVIDENCE")
    return {"plumbing_sha": before, "unique_run": unique}


def audit_source_excerpt(source, full):
    check(isinstance(source, dict), "INVALID_SOURCE_RECORD")
    check(set(source) == {"label", "path", "full_bytes", "full_sha256",
                          "git_blob", "byte_start", "byte_end", "content"},
          "UNEXPECTED_SOURCE_RECORD_FIELDS")
    check(isinstance(source["label"], str) and source["label"].strip(),
          "INVALID_SOURCE_LABEL")
    check(path_is_safe(source["path"]), "UNSAFE_SOURCE_PATH")
    full_id = {
        "bytes": source["full_bytes"], "sha256": source["full_sha256"],
        "git_blob": source["git_blob"],
    }
    require_identity(full, full_id, "SOURCE_FULL_IDENTITY_MISMATCH")
    start, end = source["byte_start"], source["byte_end"]
    check(type(start) is int and type(end) is int
          and 0 <= start < end <= len(full), "INVALID_SOURCE_INTERVAL")
    content = source["content"]
    check(isinstance(content, str), "INVALID_SOURCE_CONTENT")
    excerpt = full[start:end]
    try:
        check(excerpt.decode("utf-8").encode("utf-8") == excerpt
              and content.encode("utf-8") == excerpt,
              "SOURCE_EXCERPT_MISMATCH")
    except UnicodeError:
        raise AuditError("SOURCE_EXCERPT_NOT_UTF8") from None
    return {
        "path": source["path"], "full_bytes": len(full),
        "full_sha256": sha256(full), "git_blob": identity(full)["git_blob"],
        "byte_start": start, "byte_end": end,
        "excerpt_bytes": len(excerpt), "excerpt_sha256": sha256(excerpt),
    }


def audit_sources(packet, locked_sources, fetcher=fetch):
    check(isinstance(packet, dict) and packet.get("source_commit") == SOURCE_SHA,
          "WRONG_SOURCE_COMMIT")
    records = packet.get("sources")
    check(isinstance(records, list) and records, "EMPTY_SOURCE_PACKET")
    check(isinstance(locked_sources, list) and len(locked_sources) == len(records),
          "SOURCE_COUNT_MISMATCH")
    cache, seen, labels, result = {}, set(), set(), []
    for source, locked in zip(records, locked_sources):
        check(isinstance(source, dict) and path_is_safe(source.get("path")),
              "INVALID_SOURCE_RECORD")
        path = source["path"]
        if path not in cache:
            cache[path] = fetcher(SOURCE_SHA, path)
        actual = audit_source_excerpt(source, cache[path])
        key = (path, actual["byte_start"], actual["byte_end"])
        check(key not in seen and source["label"] not in labels,
              "DUPLICATE_SOURCE_PACKET_ENTRY")
        seen.add(key)
        labels.add(source["label"])
        check(same_json(actual, locked), "SOURCE_INTEGRITY_RECORD_MISMATCH")
        result.append(actual)
    return result


def build_prompt(documents):
    check(set(documents) == set(FROZEN_DOCUMENTS) | {TARGET_NAME},
          "UNEXPECTED_PROMPT_DOCUMENTS")
    prompt = documents["REVIEW_PROMPT.md"]
    for name in (TARGET_NAME, "SOURCE_PACKET.json", "FREEZE.json"):
        raw = documents[name]
        try:
            raw.decode("utf-8")
        except UnicodeError:
            raise AuditError("NON_UTF8_PROMPT_DOCUMENT") from None
        prompt += ("\nEXACT DOCUMENT " + name + "\nUTF8-BYTES "
                   + str(len(raw)) + "\n").encode("utf-8")
        prompt += raw + b"\nEND EXACT DOCUMENT\n"
    return prompt


def expected_request(prompt):
    request = {
        "contents": [{"role": "user", "parts": [{"text": prompt.decode("utf-8")}]}],
        "generationConfig": {
            "temperature": 0, "maxOutputTokens": 32768,
            "responseMimeType": "application/json",
        },
    }
    return (json.dumps(request, ensure_ascii=False, sort_keys=True)
            + "\n").encode("utf-8")


def substantive_entry(entry):
    """Accept prose or structured prose; reject null/numeric/empty placeholders."""
    if isinstance(entry, str):
        return bool(entry.strip())
    if isinstance(entry, dict):
        return bool(entry) and any(substantive_entry(value)
                                   for value in entry.values())
    if isinstance(entry, list):
        return bool(entry) and any(substantive_entry(value) for value in entry)
    return False


def audit_verdict(verdict):
    check(isinstance(verdict, dict) and set(verdict) == VERDICT_FIELDS,
          "INVALID_VERDICT_FIELDS")
    check(verdict["verdict"] == "ACCEPTED", "REVIEW_NOT_ACCEPTED")
    for field in ("findings", "missing_assumptions", "counterexamples"):
        check(verdict[field] == [], "UNRESOLVED_SUBSTANTIVE_FINDINGS")
    check(isinstance(verdict["limitations"], list)
          and all(isinstance(entry, (str, dict)) and substantive_entry(entry)
                  for entry in verdict["limitations"]), "INVALID_LIMITATIONS")
    analysis = verdict["constructive_analysis"]
    check(isinstance(analysis, list) and analysis
          and all(isinstance(entry, (str, dict)) and substantive_entry(entry)
                  for entry in analysis), "INVALID_CONSTRUCTIVE_ANALYSIS")
    check(verdict["native_bridge_status"] == "NOT_DERIVED",
          "NATIVE_SCOPE_NOT_ACCEPTABLE")
    check(isinstance(verdict["next_native_obligation"], str)
          and verdict["next_native_obligation"].strip(),
          "INVALID_NEXT_NATIVE_OBLIGATION")
    return verdict


def reconstruct_response(raw):
    response = parse_json(raw)
    check(isinstance(response, dict), "INVALID_RESPONSE_OBJECT")
    returned = response.get("modelVersion")
    check(isinstance(returned, str)
          and (returned == MODEL or re.fullmatch(
              re.escape(MODEL) + r"-[A-Za-z0-9][A-Za-z0-9._-]*", returned)),
          "WRONG_RETURNED_MODEL")
    feedback = response.get("promptFeedback", {})
    check(isinstance(feedback, dict) and not feedback.get("blockReason"),
          "PROMPT_BLOCKED_OR_INVALID")
    candidates = response.get("candidates")
    check(isinstance(candidates, list) and len(candidates) == 1,
          "WRONG_CANDIDATE_COUNT")
    candidate = candidates[0]
    check(isinstance(candidate, dict) and candidate.get("finishReason") == "STOP",
          "INCOMPLETE_REVIEW")
    content = candidate.get("content")
    check(isinstance(content, dict), "INVALID_RESPONSE_CONTENT")
    check(content.get("role", "model") == "model", "WRONG_RESPONSE_ROLE")
    parts = content.get("parts")
    check(isinstance(parts, list) and parts, "INVALID_RESPONSE_PARTS")
    texts = []
    for part in parts:
        check(isinstance(part, dict), "INVALID_RESPONSE_PART")
        check(type(part.get("thought", False)) is bool, "INVALID_THOUGHT_FLAG")
        if "text" in part:
            check(isinstance(part["text"], str), "INVALID_RESPONSE_TEXT")
            if not part.get("thought", False):
                texts.append(part["text"])
    check(texts, "NO_NONTHOUGHT_REVIEW_TEXT")
    answer = "\n".join(texts).strip().encode("utf-8")
    check(answer, "EMPTY_REVIEW_TEXT")
    return answer, parse_json(answer), returned


def audit_helpers(locked, checkout_root=Path("."), fetcher=fetch, reader=None):
    """Independently lock the complete inherited non-stdlib helper closure."""
    check(locked == HELPERS, "HELPER_LOCK_MISMATCH")
    for path, expected in HELPER_IDENTITIES.items():
        require_identity(fetcher(TARGET_SHA, path), expected,
                         "REMOTE_HELPER_IDENTITY_MISMATCH")
        local = (reader(path) if reader is not None
                 else read_regular_file(Path(checkout_root) / path))
        require_identity(local, expected, "CHECKOUT_HELPER_IDENTITY_MISMATCH")
    return dict(HELPERS)


def audit(directory=OUT, *, fetcher=fetch, run=None, checkout_root=Path("."),
          helper_reader=None, environ=None, git_reader=None, marker_reader=None):
    """Return a receipt only after all independent byte/identity gates pass."""
    current = current_identity(environ=environ) if run is None else run
    check(isinstance(current, dict) and set(current) == set(BASE_FIELDS),
          "INVALID_CURRENT_IDENTITY")
    check(valid_sha(FREEZE_SHA) and current["freeze_sha"] == FREEZE_SHA
          and current["target_sha"] == TARGET_SHA
          and valid_sha(current["checkout_sha"])
          and current["checkout_sha"] == current["workflow_sha"]
          and current["run_attempt"] == "1"
          and isinstance(current["run_id"], str)
          and re.fullmatch(r"[1-9][0-9]*", current["run_id"]) is not None,
          "CURRENT_IDENTITY_MISMATCH")
    artifacts, manifest, manifest_raw = read_review_artifacts(directory)
    integrity = parse_json(artifacts["integrity.json"])
    review = parse_json(artifacts["review_identity.json"])
    check(isinstance(integrity, dict) and integrity.get("status") == "PASS"
          and integrity.get("scientific_execution") is False,
          "INTEGRITY_DID_NOT_PASS")
    check(isinstance(review, dict) and set(review) == REVIEW_FIELDS,
          "INVALID_REVIEW_IDENTITY_FIELDS")
    for field in BASE_FIELDS:
        check(integrity.get(field) == current[field] == review[field],
              "INTEGRITY_REVIEW_CURRENT_IDENTITY_MISMATCH")
    trigger = audit_trigger(integrity, current, environ, git_reader, marker_reader)
    documents = {}
    for name, expected in FROZEN_DOCUMENTS.items():
        documents[name] = fetcher(FREEZE_SHA, FREEZE_PREFIX + name)
        require_identity(documents[name], expected, "FROZEN_DOCUMENT_MISMATCH")
    documents[TARGET_NAME] = fetcher(TARGET_SHA, PREFIX + TARGET_NAME)
    require_identity(documents[TARGET_NAME], TARGET_IDENTITY,
                     "TARGET_DOCUMENT_MISMATCH")
    records = {name: sha256(raw) for name, raw in documents.items()}
    check(integrity.get("documents") == records, "DOCUMENT_MANIFEST_MISMATCH")
    freeze = parse_json(documents["FREEZE.json"])
    check(isinstance(freeze, dict), "INVALID_FREEZE")
    check(freeze.get("target") == dict(
        TARGET_IDENTITY, commit=TARGET_SHA, path=PREFIX + TARGET_NAME),
        "FREEZE_TARGET_MISMATCH")
    check(freeze.get("documents") == {
        name: records[name] for name in ("SOURCE_PACKET.json", "REVIEW_PROMPT.md")
    }, "FREEZE_DOCUMENT_LOCK_MISMATCH")
    check(freeze.get("research_base_sha") == SOURCE_SHA
          and freeze.get("pr_number") == 107
          and freeze.get("pr_branch") == BRANCH,
          "FREEZE_SCOPE_IDENTITY_MISMATCH")
    check(freeze.get("model") == {
        "name": MODEL, "temperature": 0, "max_output_tokens": 32768,
        "response_mime_type": "application/json",
        "availability_get_limit": 1, "generation_request_limit": 1,
        "automatic_retry": False, "workflow_rerun_allowed": False,
    }, "FREEZE_MODEL_CONTRACT_MISMATCH")
    packet = parse_json(documents["SOURCE_PACKET.json"])
    check(integrity.get("source_commit") == SOURCE_SHA, "INTEGRITY_SOURCE_MISMATCH")
    sources = audit_sources(packet, integrity.get("sources"), fetcher)
    helper_identity = audit_helpers(integrity.get("helper_identity"),
                                   checkout_root, fetcher, helper_reader)
    prompt = build_prompt(documents)
    check(artifacts["prompt.txt"] == prompt
          and review["prompt_sha256"] == sha256(prompt)
          and integrity.get("expected_prompt_sha256") == sha256(prompt),
          "EXACT_PROMPT_MISMATCH")
    check(artifacts["request.json"] == expected_request(prompt),
          "EXACT_REQUEST_MISMATCH")
    metadata = parse_json(artifacts["model_metadata.json"])
    check(isinstance(metadata, dict)
          and metadata.get("name") == "models/" + MODEL
          and isinstance(metadata.get("supportedGenerationMethods"), list)
          and all(isinstance(method, str)
                  for method in metadata["supportedGenerationMethods"])
          and "generateContent" in metadata["supportedGenerationMethods"],
          "MODEL_AVAILABILITY_MISMATCH")
    response_raw = artifacts["response.json"]
    check(sha256(response_raw) == review["response_sha256"],
          "RAW_RESPONSE_HASH_MISMATCH")
    answer, verdict, returned = reconstruct_response(response_raw)
    check(returned == review["model_returned"], "REVIEW_MODEL_IDENTITY_MISMATCH")
    check(answer == artifacts["review.txt"], "RAW_ANSWER_MISMATCH")
    check(same_json(verdict, parse_json(artifacts["verdict.json"])),
          "STORED_VERDICT_MISMATCH")
    audit_verdict(verdict)
    return dict(
        current, status="PASS", scientific_execution=False,
        documents=records, source_commit=SOURCE_SHA,
        source_count=len(sources), sources=sources, helper_identity=helper_identity,
        plumbing_sha=trigger["plumbing_sha"], unique_run=trigger["unique_run"],
        model_requested=MODEL, model_returned=returned,
        prompt_sha256=sha256(prompt), request_sha256=sha256(artifacts["request.json"]),
        response_sha256=sha256(response_raw), answer_sha256=sha256(answer),
        original_manifest_sha256=sha256(manifest_raw), original_members=manifest,
        native_bridge_status="NOT_DERIVED", limitations=verdict["limitations"],
        constructive_analysis=verdict["constructive_analysis"],
        next_native_obligation=verdict["next_native_obligation"],
        scope=("Independent exact-byte publication audit only. Substantive review "
               "coverage and whether limitations hide objections require human "
               "assessment; this receipt establishes no native derivation."),
    )


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, allow_nan=False,
                       indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_new(path, raw):
    """Never overwrite a previous evidence file."""
    with Path(path).open("xb") as handle:
        handle.write(raw)


def failure_metadata(exc):
    result = {
        "status": "PUBLICATION_AUDIT_FAILED",
        "scientific_execution": False,
        "error_type": type(exc).__name__,
    }
    if isinstance(exc, AuditError):
        result["reason_code"] = str(exc)
    else:
        result["reason_code"] = "UNEXPECTED_ERROR_DETAILS_WITHHELD"
    code = getattr(exc, "code", None)
    if type(code) is int and 100 <= code <= 599:
        result["http_status"] = code
    return result


def main():
    # A fresh directory prevents a stale PASS receipt from surviving a new audit.
    # A failed rerun keeps the old directory byte-for-byte; it is not a new audit.
    if DEST.exists() or DEST.is_symlink():
        raise SystemExit("Publication output already exists; originals preserved. "
                         "Use a fresh workspace for an independent audit.")
    DEST.mkdir()
    failed = False
    try:
        receipt = audit()
        write_new(DEST / "publication.json", json_bytes(receipt))
    except Exception as exc:
        failed = True
        write_new(DEST / "failure.json", json_bytes(failure_metadata(exc)))
    finally:
        output_manifest = {
            path.name: {"bytes": len(raw), "sha256": sha256(raw)}
            for path in sorted(DEST.iterdir())
            if path.is_file() and path.name != "artifact_manifest.json"
            for raw in (read_regular_file(path),)
        }
        write_new(DEST / "artifact_manifest.json", json_bytes(output_manifest))
    if failed:
        raise SystemExit("Publication audit failed; sanitized failure and "
                         "manifest retained. Original review evidence untouched.")
    print("Independent immutable-source, exact-request and raw-response "
          "publication audit PASS; no model request or science execution.")


if __name__ == "__main__":
    main()
