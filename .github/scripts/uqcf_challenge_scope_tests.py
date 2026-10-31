"""Offline synthetic plumbing controls; no scientific execution or remote requests.

Run: python .github/scripts/uqcf_challenge_scope_tests.py
All remote reads, Git state, keyed transport, and run-list replies are synthetic.
The imported preparability modules' original main programs are never executed.
"""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import socket
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import uqcf_challenge_scope_review as producer
import uqcf_preparability_review as helper

AUDITOR_PATH = HERE / "uqcf_challenge_scope_publication.py"
auditor = None
if AUDITOR_PATH.exists():
    spec = importlib.util.spec_from_file_location("challenge_scope_independent_audit", AUDITOR_PATH)
    auditor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(auditor)

FREEZE = "a" * 40
TARGET = "b" * 40
SOURCE = "c" * 40
PLUMBING = "d" * 40
TRIGGER = "e" * 40
SENTINEL = "SYNTHETIC-NONCREDENTIAL-TEST-SENTINEL"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def accepted():
    return dict(verdict="ACCEPTED", findings=[], missing_assumptions=[], counterexamples=[],
                limitations=["Synthetic limitation, not a scientific result."],
                constructive_analysis=[
                    "Synthetic proof reconstruction for source section 1; mock data only."],
                native_bridge_status="NOT_DERIVED",
                next_native_obligation="Synthetic open obligation.")


def response(verdict=None, **overrides):
    value = dict(modelVersion=helper.MODEL,
                 candidates=[dict(finishReason="STOP", content=dict(role="model", parts=[
                     dict(text="synthetic hidden explanation", thought=True),
                     dict(text=json.dumps(accepted() if verdict is None else verdict))]))],
                 usageMetadata=dict(promptTokenCount=12, candidatesTokenCount=30),
                 opaqueSyntheticField={"preserve": ["all", "bytes"]})
    value.update(overrides)
    return encoded(value)


class MockResponse:
    def __init__(self, raw):
        self.raw = raw

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.raw


class MockTransport:
    def __init__(self, raw=None, fail_get=None, fail_post=None, metadata=None):
        self.raw = response() if raw is None else raw
        self.fail_get, self.fail_post = fail_get, fail_post
        self.metadata = metadata
        self.requests = []

    def open(self, request, timeout=None):
        self.requests.append(request)
        if request.get_method() == "GET":
            if self.fail_get:
                raise self.fail_get
            return MockResponse(self.metadata if self.metadata is not None else
                                encoded(dict(name="models/" + helper.MODEL,
                                             supportedGenerationMethods=["generateContent"])))
        if self.fail_post:
            raise self.fail_post
        return MockResponse(self.raw)


class SyntheticFixture:
    """An isolated synthetic checkout and immutable read store."""
    def __init__(self, root):
        self.root = Path(root)
        self.out = self.root / "challenge_scope_review"
        self.out.mkdir()
        self.target_path = str(Path(producer.BASE).parent / producer.NOTE)
        self.note = b"Synthetic target only.\n"
        self.source_full = "synthetic α source\nsecond line\n".encode()
        self.source_path = "synthetic/source.md"
        self.source_row = dict(label="Synthetic source", path=self.source_path,
                               full_bytes=len(self.source_full),
                               full_sha256=digest(self.source_full),
                               git_blob=git_blob(self.source_full),
                               byte_start=0, byte_end=len(self.source_full),
                               content=self.source_full.decode())
        self.packet = dict(source_commit=SOURCE, sources=[self.source_row])
        self.freeze = dict(
            target=dict(commit=TARGET, path=self.target_path, bytes=len(self.note),
                        sha256=digest(self.note), git_blob=git_blob(self.note)),
            research_base_sha=SOURCE, pr_number=107, pr_branch=producer.BRANCH,
            model=dict(name=helper.MODEL, temperature=0, max_output_tokens=32768,
                       response_mime_type="application/json", availability_get_limit=1,
                       generation_request_limit=1, automatic_retry=False,
                       workflow_rerun_allowed=False))
        self.helpers = {".github/scripts/synthetic_helper.py": digest(b"synthetic helper\n")}
        self.remote_bytes = {
            (TARGET, ".github/scripts/synthetic_helper.py"): b"synthetic helper\n",
            (SOURCE, self.source_path): self.source_full,
            (TARGET, self.target_path): self.note}
        self.write(".github/scripts/synthetic_helper.py", b"synthetic helper\n")
        self.write(self.target_path, self.note)
        self.marker = dict(kind="PR107 one-request analytical review trigger",
                           freeze_sha=FREEZE, target_sha=TARGET, plumbing_sha=PLUMBING)
        self.write(producer.MARKER, encoded(self.marker))
        self.parents = PLUMBING
        self.changes = "A\t" + producer.MARKER
        self.ancestor = FREEZE
        self.env = dict(GITHUB_SHA=TRIGGER, UQCF_WORKFLOW_SHA=TRIGGER,
                        GITHUB_REPOSITORY=producer.REPO,
                        GITHUB_REF="refs/heads/" + producer.BRANCH,
                        GITHUB_EVENT_NAME="push", GITHUB_RUN_ATTEMPT="1",
                        GITHUB_RUN_ID="123456", GH_READ_TOKEN="SYNTHETIC-READ-TOKEN",
                        GEMINI_API_KEY=SENTINEL,
                        UQCF_PUSH_BEFORE=PLUMBING)
        self.rebuild()

    def write(self, relative, raw):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def rebuild(self):
        packet_raw = encoded(self.packet)
        prompt_raw = b"Synthetic adversarial review instructions. No science.\n"
        self.freeze["documents"] = {
            "SOURCE_PACKET.json": digest(packet_raw),
            "REVIEW_PROMPT.md": digest(prompt_raw)}
        self.docs = {"FREEZE.json": encoded(self.freeze),
                     "SOURCE_PACKET.json": packet_raw, "REVIEW_PROMPT.md": prompt_raw,
                     producer.NOTE: self.note}
        for name in ("FREEZE.json", "SOURCE_PACKET.json", "REVIEW_PROMPT.md"):
            self.write(producer.BASE + "/" + name, self.docs[name])
            self.remote_bytes[(FREEZE, producer.BASE + "/" + name)] = self.docs[name]

    def fetch(self, sha, path):
        return self.remote_bytes[(sha, path)]

    def git(self, *args):
        values = {("rev-parse", "HEAD"): TRIGGER,
                  ("show", "-s", "--format=%P", "HEAD"): self.parents,
                  ("diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD"): self.changes}
        if args[:1] == ("merge-base",):
            return self.ancestor
        if args in values:
            return values[args]
        raise AssertionError("Unmocked Git operation: " + repr(args))

    def git_bytes(self, *args):
        if args == ("show", "HEAD:" + producer.MARKER):
            return (self.root / producer.MARKER).read_bytes()
        return (self.git(*args) + "\n").encode()

    def run(self):
        return dict(freeze_sha=FREEZE, target_sha=TARGET, checkout_sha=TRIGGER,
                    workflow_sha=TRIGGER, run_id="123456", run_attempt="1")

    @contextlib.contextmanager
    def patched(self):
        old_cwd = Path.cwd()
        os.chdir(self.root)
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
                stack.enter_context(mock.patch.object(producer, "FREEZE_SHA", FREEZE))
                stack.enter_context(mock.patch.object(producer, "OUT", self.out))
                stack.enter_context(mock.patch.object(producer, "HELPERS", self.helpers))
                stack.enter_context(mock.patch.object(producer, "remote", self.fetch))
                stack.enter_context(mock.patch.object(producer, "git", self.git))
                stack.enter_context(mock.patch.object(producer, "inputs",
                                                     lambda: (self.docs, self.freeze)))
                stack.enter_context(mock.patch.object(producer, "unique_run_gate", return_value={
                    "workflow_id": 77, "eligible_run_id": 123456, "listed_total": 1}))
                yield
        finally:
            os.chdir(old_cwd)

    def make_integrity(self):
        with self.patched():
            with contextlib.redirect_stdout(io.StringIO()):
                producer.integrity()

    def make_review(self, transport=None):
        transport = transport or MockTransport()
        with self.patched(), mock.patch.object(urllib.request, "build_opener", return_value=transport):
            with contextlib.redirect_stdout(io.StringIO()):
                producer.review()
        return transport

    def manifest(self):
        (self.out / "artifact_manifest.json").write_bytes(encoded({
            path.name: dict(bytes=len(path.read_bytes()), sha256=digest(path.read_bytes()))
            for path in self.out.iterdir() if path.name != "artifact_manifest.json"}))

    def evidence(self):
        self.make_integrity()
        self.make_review()
        self.manifest()

    @contextlib.contextmanager
    def audit_patched(self):
        if auditor is None:
            raise AssertionError("Independent auditor module is required")
        helper_ids = {path: auditor.identity(self.remote_bytes[(TARGET, path)])
                      for path in self.helpers}
        values = dict(FREEZE_SHA=FREEZE, TARGET_SHA=TARGET, SOURCE_SHA=SOURCE,
                      TARGET_IDENTITY=auditor.identity(self.note),
                      FROZEN_DOCUMENTS={name: auditor.identity(raw)
                                        for name, raw in self.docs.items() if name != producer.NOTE},
                      HELPER_IDENTITIES=helper_ids, HELPERS=self.helpers)
        with contextlib.ExitStack() as stack:
            for name, value in values.items():
                stack.enter_context(mock.patch.object(auditor, name, value))
            yield

    def audit(self):
        with self.audit_patched():
            return auditor.audit(
                self.out, fetcher=self.fetch, run=self.run(), checkout_root=self.root,
                environ=self.env, git_reader=self.git_bytes,
                marker_reader=lambda path: (self.root / path).read_bytes())


class OfflineTest(unittest.TestCase):
    def setUp(self):
        # Even accidental missed mocks cannot connect to any network endpoint.
        self.network_guard = contextlib.ExitStack()
        for owner, name in ((socket.socket, "connect"), (socket.socket, "connect_ex"),
                            (socket, "getaddrinfo")):
            self.network_guard.enter_context(mock.patch.object(
                owner, name, side_effect=AssertionError("Network forbidden in offline tests")))
        self.tmp = tempfile.TemporaryDirectory(prefix="uqcf-synthetic-test-")
        self.fixture = SyntheticFixture(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()
        self.network_guard.close()


class ProducerSourceTests(OfflineTest):
    def test_valid_synthetic_target_and_source(self):
        f = self.fixture
        producer.verify_target(f.freeze["target"], f.note)
        self.assertEqual(producer.verify_source(f.source_row, f.source_full)["excerpt_bytes"],
                         len(f.source_full))

    def test_target_rejects_size_hash_blob_and_invalid_utf8(self):
        f = self.fixture
        for field, value in (("bytes", True), ("bytes", 3), ("sha256", "0" * 64),
                             ("git_blob", "0" * 40)):
            with self.subTest(field=field, value=value):
                lock = {**f.freeze["target"], field: value}
                with self.assertRaises(ValueError):
                    producer.verify_target(lock, f.note)
        raw = b"\xff"
        with self.assertRaises(UnicodeDecodeError):
            producer.verify_target(dict(bytes=1, sha256=digest(raw), git_blob=git_blob(raw)), raw)

    def test_source_rejects_hash_blob_size_interval_and_content(self):
        f = self.fixture
        bad = [("full_bytes", True), ("full_bytes", 1), ("full_sha256", "0" * 64),
               ("git_blob", "0" * 40), ("byte_start", -1), ("byte_start", True),
               ("byte_start", len(f.source_full)), ("byte_end", len(f.source_full) + 1),
               ("byte_end", False), ("content", "altered"), ("content", [])]
        for field, value in bad:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                producer.verify_source({**f.source_row, field: value}, f.source_full)

    def test_source_rejects_unsafe_paths_before_fetch(self):
        for path in ("", "/absolute", "../escape", "a/../b", "./file", "a//b",
                     "a/./b", "a\\b", "a/", "null\x00byte", None):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    producer.verify_source({**self.fixture.source_row, "path": path},
                                           self.fixture.source_full)
                with mock.patch.object(urllib.request, "urlopen") as opened:
                    with self.assertRaises(ValueError):
                        producer.remote(TARGET, path)
                    opened.assert_not_called()

    def test_remote_rejects_nonimmutable_refs(self):
        for sha in ("HEAD", "main", "", "a" * 39, "A" * 40, TARGET + "/x"):
            with self.subTest(sha=sha), mock.patch.object(urllib.request, "urlopen") as opened:
                with self.assertRaises(ValueError):
                    producer.remote(sha, "safe/file.md")
                opened.assert_not_called()

    def test_duplicate_json_keys_rejected(self):
        for raw in (b'{"a":1,"a":2}', b'{"nested":{"a":1,"a":2}}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                producer.parse(raw)

    def test_integrity_rejects_duplicate_source_excerpt(self):
        f = self.fixture
        f.packet["sources"].append(copy.deepcopy(f.source_row))
        f.rebuild()
        with f.patched(), self.assertRaisesRegex(ValueError, "Duplicate source"):
            producer.integrity()

    def test_integrity_rejects_source_commit_and_helper_mutation(self):
        f = self.fixture
        f.packet["source_commit"] = "f" * 40
        f.rebuild()
        with f.patched(), self.assertRaisesRegex(ValueError, "Source commit"):
            producer.integrity()
        f.packet["source_commit"] = SOURCE
        f.rebuild()
        f.write(".github/scripts/synthetic_helper.py", b"tampered")
        with f.patched(), self.assertRaisesRegex(ValueError, "helper closure"):
            producer.integrity()

    def test_exact_frozen_inputs_and_document_hashes(self):
        f = self.fixture
        original_inputs = producer.inputs
        with f.patched():
            self.assertEqual(original_inputs(fetch=f.fetch)[0], f.docs)
            f.remote_bytes[(FREEZE, producer.BASE + "/REVIEW_PROMPT.md")] += b"altered"
            with self.assertRaisesRegex(ValueError, "Frozen document mismatch"):
                original_inputs(fetch=f.fetch)
        f.rebuild()
        f.freeze["documents"]["REVIEW_PROMPT.md"] = "0" * 64
        bad_freeze = encoded(f.freeze)
        f.write(producer.BASE + "/FREEZE.json", bad_freeze)
        f.remote_bytes[(FREEZE, producer.BASE + "/FREEZE.json")] = bad_freeze
        with f.patched(), self.assertRaisesRegex(ValueError, "Freeze manifest"):
            original_inputs(fetch=f.fetch)

    def test_frozen_model_limits_reject_retry_model_token_changes(self):
        f = self.fixture
        original_inputs = producer.inputs
        for field, value in (("generation_request_limit", 2), ("automatic_retry", True),
                             ("workflow_rerun_allowed", True), ("name", "different-model"),
                             ("temperature", 1), ("max_output_tokens", 32767)):
            with self.subTest(field=field):
                old = f.freeze["model"][field]
                f.freeze["model"][field] = value
                f.rebuild()
                with f.patched(), self.assertRaisesRegex(ValueError, "Frozen request limits"):
                    original_inputs(fetch=f.fetch)
                f.freeze["model"][field] = old


class ProducerIdentityTests(OfflineTest):
    def test_valid_exact_marker_and_run(self):
        with self.fixture.patched():
            self.assertEqual(producer.identity(self.fixture.freeze), self.fixture.run())
            self.assertEqual(producer.marker_gate(self.fixture.freeze), PLUMBING)

    def test_reject_run_attempt_event_repository_ref_and_sha_changes(self):
        f = self.fixture
        fields = dict(GITHUB_RUN_ATTEMPT="2", GITHUB_EVENT_NAME="workflow_dispatch",
                      GITHUB_REPOSITORY="attacker/other", GITHUB_REF="refs/heads/main",
                      GITHUB_SHA="f" * 40, UQCF_WORKFLOW_SHA="f" * 40)
        for field, value in fields.items():
            with self.subTest(field=field), f.patched():
                os.environ[field] = value
                with self.assertRaises(ValueError):
                    producer.identity(f.freeze)

    def test_reject_merge_trigger_and_other_changed_paths(self):
        f = self.fixture
        for parents in ("", PLUMBING + " " + SOURCE):
            f.parents = parents
            with self.subTest(parents=parents), f.patched(), self.assertRaises(ValueError):
                producer.marker_gate(f.freeze)
        f.parents = PLUMBING
        for changes in ("M\t" + producer.MARKER, "", "A\t" + producer.MARKER + "\nM\tother"):
            f.changes = changes
            with self.subTest(changes=changes), f.patched(), self.assertRaises(ValueError):
                producer.marker_gate(f.freeze)

    def test_reject_marker_byte_and_identity_mutations(self):
        f = self.fixture
        mutations = [encoded(f.marker) + b"\n", encoded(f.marker).rstrip(),
                     encoded({**f.marker, "freeze_sha": "f" * 40}),
                     encoded({**f.marker, "target_sha": "f" * 40}),
                     encoded({**f.marker, "plumbing_sha": "f" * 40})]
        for raw in mutations:
            f.write(producer.MARKER, raw)
            with self.subTest(raw=raw), f.patched(), self.assertRaises(ValueError):
                producer.marker_gate(f.freeze)

    def test_reject_nonancestor_freeze(self):
        f = self.fixture
        f.ancestor = "f" * 40
        with f.patched(), self.assertRaises(ValueError):
            producer.marker_gate(f.freeze)

    def test_reject_substituted_parent_against_trusted_push_before(self):
        f = self.fixture
        f.parents = "f" * 40
        f.write(producer.MARKER, encoded({**f.marker, "plumbing_sha": f.parents}))
        with f.patched(), self.assertRaises(ValueError):
            producer.marker_gate(f.freeze)

    def test_reject_missing_zero_and_malformed_push_before(self):
        f = self.fixture
        for value in ("", "0" * 40, "not-a-sha"):
            with self.subTest(value=value), f.patched():
                os.environ["UQCF_PUSH_BEFORE"] = value
                with self.assertRaises(ValueError):
                    producer.marker_gate(f.freeze)

    def test_unique_run_accepts_only_single_current_first_attempt(self):
        f = self.fixture
        current = dict(id=123456, run_attempt=1, head_sha=TRIGGER, event="push",
                       path=producer.WORKFLOW, head_branch=producer.BRANCH, workflow_id=77)
        listing = dict(total_count=1, workflow_runs=[dict(id=123456)])
        calls = []
        def api(path, token):
            calls.append((path, token))
            return current if path.startswith("/actions/runs/") else listing
        with mock.patch.dict(os.environ, f.env, clear=True):
            self.assertEqual(producer.unique_run_gate(f.run(), api=api)["eligible_run_id"], 123456)
            self.assertEqual(len(calls), 2)
            for field, value in (("id", 1), ("run_attempt", 2), ("head_sha", SOURCE),
                                 ("event", "pull_request"), ("path", "other"),
                                 ("head_branch", "main")):
                with self.subTest(field=field):
                    original = current[field]
                    current[field] = value
                    with self.assertRaises(ValueError):
                        producer.unique_run_gate(f.run(), api=api)
                    current[field] = original
            for bad in (dict(total_count=2, workflow_runs=[dict(id=123456), dict(id=123457)]),
                        dict(total_count=101, workflow_runs=[dict(id=123456)]),
                        dict(total_count=1, workflow_runs=[dict(id=4)]),
                        dict(total_count=0, workflow_runs=[])):
                listing.clear()
                listing.update(bad)
                with self.subTest(listing=bad), self.assertRaises(ValueError):
                    producer.unique_run_gate(f.run(), api=api)


class ProducerTransportTests(OfflineTest):
    def test_exact_one_get_one_post_key_only_in_header(self):
        f, transport = self.fixture, MockTransport()
        f.make_integrity()
        f.make_review(transport)
        self.assertEqual([r.get_method() for r in transport.requests], ["GET", "POST"])
        for request in transport.requests:
            self.assertEqual(request.get_header("X-goog-api-key"), SENTINEL)
            self.assertNotIn(SENTINEL, request.full_url)
            self.assertNotIn(SENTINEL.encode(), request.data or b"")
        self.assertEqual((f.out / "response.json").read_bytes(), transport.raw)
        self.assertEqual((f.out / "request.json").read_bytes(), transport.requests[1].data)
        self.assertEqual((f.out / "prompt.txt").read_bytes(), producer.build_prompt(f.docs))

    def test_no_retry_on_get_or_ambiguous_post_timeout(self):
        f = self.fixture
        f.make_integrity()
        for fail_get, fail_post, expected in ((TimeoutError("synthetic GET timeout"), None, ["GET"]),
                                            (None, TimeoutError("synthetic POST timeout"), ["GET", "POST"])):
            transport = MockTransport(fail_get=fail_get, fail_post=fail_post)
            with self.subTest(expected=expected), self.assertRaises(TimeoutError):
                f.make_review(transport)
            self.assertEqual([r.get_method() for r in transport.requests], expected)

    def test_no_redirect_handler_rejects_all_redirects(self):
        handler = producer.NoRedirect()
        for method in ("GET", "POST"):
            for code in (301, 302, 303, 307, 308):
                request = urllib.request.Request("https://generativelanguage.googleapis.com/mock",
                    data=b"{}" if method == "POST" else None,
                    headers={"x-goog-api-key": SENTINEL}, method=method)
                with self.subTest(method=method, code=code), self.assertRaises(urllib.error.HTTPError) as caught:
                    handler.redirect_request(request, None, code, "redirect", {},
                                             "https://synthetic-other.invalid/stolen")
                self.assertEqual(caught.exception.code, code)

    def test_review_constructs_no_redirect_opener(self):
        f, transport = self.fixture, MockTransport()
        f.make_integrity()
        with f.patched(), mock.patch.object(urllib.request, "build_opener", return_value=transport) as builder:
            with contextlib.redirect_stdout(io.StringIO()):
                producer.review()
        args, kwargs = builder.call_args
        self.assertEqual(len(args), 1)
        self.assertIsInstance(args[0], producer.NoRedirect)
        self.assertEqual(kwargs, {})

    def test_absent_key_stops_before_transport(self):
        f = self.fixture
        f.make_integrity()
        with f.patched(), mock.patch.object(urllib.request, "build_opener") as opened:
            os.environ["GEMINI_API_KEY"] = ""
            with self.assertRaisesRegex(ValueError, "credential missing"):
                producer.review()
            opened.assert_not_called()

    def test_run_artifact_or_prompt_mismatch_stops_before_transport(self):
        f = self.fixture
        for field, value in (("run_attempt", "2"), ("checkout_sha", SOURCE),
                             ("workflow_sha", SOURCE), ("run_id", "other"),
                             ("expected_prompt_sha256", "0" * 64),
                             ("scientific_execution", True), ("status", "FAIL"),
                             ("plumbing_sha", SOURCE), ("helper_identity", {}), ("documents", {})):
            f.make_integrity()
            evidence = producer.parse((f.out / "integrity.json").read_bytes())
            evidence[field] = value
            (f.out / "integrity.json").write_bytes(encoded(evidence))
            with self.subTest(field=field), f.patched(), \
                    mock.patch.object(urllib.request, "build_opener") as opened:
                with self.assertRaises(ValueError):
                    producer.review()
                opened.assert_not_called()

    def test_credential_echo_is_redacted_and_acceptance_stops(self):
        f = self.fixture
        f.make_integrity()
        raw = response(opaqueSyntheticField=SENTINEL)
        with self.assertRaises(producer.CredentialEcho):
            f.make_review(MockTransport(raw))
        self.assertFalse((f.out / "response.json").exists())
        self.assertEqual((f.out / "credential-echo-redacted.bin").read_bytes(),
                         raw.replace(SENTINEL.encode(), b"[REDACTED-CREDENTIAL]"))
        disclosure = producer.parse((f.out / "credential-echo.json").read_bytes())
        self.assertEqual(disclosure, dict(original_bytes=len(raw), original_sha256=digest(raw)))
        for path in f.out.iterdir():
            self.assertNotIn(SENTINEL.encode(), path.read_bytes(), path.name)

    def test_metadata_credential_echo_stops_before_post_or_original_persistence(self):
        f = self.fixture
        f.make_integrity()
        metadata = encoded(dict(name="models/" + helper.MODEL,
                                supportedGenerationMethods=["generateContent"], echo=SENTINEL))
        transport = MockTransport(metadata=metadata)
        with self.assertRaises(producer.CredentialEcho):
            f.make_review(transport)
        self.assertEqual([r.get_method() for r in transport.requests], ["GET"])
        self.assertFalse((f.out / "model_metadata.json").exists())
        self.assertFalse((f.out / "request.json").exists())
        for path in f.out.iterdir():
            self.assertNotIn(SENTINEL.encode(), path.read_bytes(), path.name)
        disclosure = producer.parse((f.out / "credential-echo.json").read_bytes())
        self.assertEqual(disclosure, dict(original_bytes=len(metadata), original_sha256=digest(metadata)))

    def test_unavailable_wrong_or_malformed_model_never_posts(self):
        f = self.fixture
        f.make_integrity()
        for metadata in (b"not JSON", encoded(dict(name="other", supportedGenerationMethods=["generateContent"])),
                         encoded(dict(name="models/" + helper.MODEL, supportedGenerationMethods=[]))):
            transport = MockTransport(metadata=metadata)
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                f.make_review(transport)
            self.assertEqual([r.get_method() for r in transport.requests], ["GET"])

    def test_guard_rejects_wrong_method_url_post_first_and_repeat(self):
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + helper.MODEL
        f = self.fixture
        for method, url in (("DELETE", endpoint), ("POST", endpoint + ":generateContent"),
                            ("GET", endpoint + "?key=forbidden"), ("GET", "https://other.invalid/")):
            transport = MockTransport()
            guard = producer.guarded_model_opener(SENTINEL, transport.open)
            request = urllib.request.Request(url, method=method)
            with self.subTest(method=method, url=url), f.patched(), self.assertRaises(ValueError):
                guard(request, timeout=1)
            self.assertEqual(transport.requests, [])
        transport = MockTransport()
        guard = producer.guarded_model_opener(SENTINEL, transport.open)
        get = urllib.request.Request(endpoint, method="GET")
        post = urllib.request.Request(endpoint + ":generateContent", data=b"{}", method="POST")
        with f.patched():
            with guard(get, timeout=1) as opened:
                opened.read()
            with self.assertRaises(ValueError):
                guard(get, timeout=1)
            with guard(post, timeout=1) as opened:
                opened.read()
            with self.assertRaises(ValueError):
                guard(post, timeout=1)
        self.assertEqual([r.get_method() for r in transport.requests], ["GET", "POST"])

    def test_guard_timeout_consumes_allowance(self):
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + helper.MODEL
        for failing_method in ("GET", "POST"):
            transport = MockTransport(
                fail_get=TimeoutError("synthetic") if failing_method == "GET" else None,
                fail_post=TimeoutError("synthetic") if failing_method == "POST" else None)
            guard = producer.guarded_model_opener(SENTINEL, transport.open)
            request = urllib.request.Request(
                endpoint if failing_method == "GET" else endpoint + ":generateContent",
                method=failing_method)
            with self.fixture.patched():
                if failing_method == "POST":
                    with guard(urllib.request.Request(endpoint, method="GET"), timeout=1) as opened:
                        opened.read()
                with self.assertRaises(TimeoutError):
                    guard(request, timeout=1)
                with self.assertRaises(ValueError):
                    guard(request, timeout=1)
            self.assertEqual(sum(r.get_method() == failing_method for r in transport.requests), 1)

    def test_http_error_preserved_sanitized_allowlisted_and_not_retried(self):
        f = self.fixture
        f.make_integrity()
        raw = b"synthetic HTTP failure " + SENTINEL.encode()
        exc = urllib.error.HTTPError("https://synthetic.invalid", 429, "rate limited",
            {"Date": "synthetic", "Content-Type": "application/json", "Retry-After": "30",
             "x-request-id": SENTINEL, "Set-Cookie": "do not retain"}, io.BytesIO(raw))
        transport = MockTransport(fail_post=exc)
        with self.assertRaises(urllib.error.HTTPError):
            f.make_review(transport)
        self.assertEqual([r.get_method() for r in transport.requests], ["GET", "POST"])
        metadata = producer.parse((f.out / "http-error-metadata.json").read_bytes())
        self.assertEqual(metadata["original_sha256"], digest(raw))
        self.assertTrue(metadata["credential_redacted"])
        self.assertNotIn("Set-Cookie", metadata["headers"])
        self.assertEqual(metadata["headers"]["x-request-id"], "[REDACTED-CREDENTIAL]")
        self.assertNotIn(SENTINEL.encode(), (f.out / "http-error.bin").read_bytes())

    def test_redirect_body_preserved_and_key_not_forwarded(self):
        f = self.fixture
        f.make_integrity()
        raw = b"synthetic redirect body " + SENTINEL.encode()
        requests = []
        class Redirecting:
            def open(self, request, timeout=None):
                requests.append(request)
                return producer.NoRedirect().redirect_request(
                    request, io.BytesIO(raw), 302, "redirect",
                    {"Location": "https://untrusted.invalid/", "Content-Type": "text/plain"},
                    "https://untrusted.invalid/")
        with self.assertRaises(urllib.error.HTTPError):
            f.make_review(Redirecting())
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].get_method(), "GET")
        self.assertEqual((f.out / "http-error.bin").read_bytes(),
                         raw.replace(SENTINEL.encode(), b"[REDACTED-CREDENTIAL]"))
        metadata = producer.parse((f.out / "http-error-metadata.json").read_bytes())
        self.assertEqual(metadata["status"], 302)
        self.assertEqual(metadata["original_sha256"], digest(raw))
        self.assertNotIn("Location", metadata["headers"])

    def test_producer_failure_wrapper_is_sanitized_and_manifested(self):
        f = self.fixture
        with f.patched(), mock.patch.object(producer, "review",
                                           side_effect=ValueError(SENTINEL)), \
                mock.patch.object(sys, "argv", ["synthetic-test", "review"]):
            with self.assertRaises(SystemExit) as caught:
                producer.main()
        self.assertNotIn(SENTINEL, str(caught.exception))
        failure = (f.out / "failure-review.json").read_bytes()
        self.assertNotIn(SENTINEL.encode(), failure)
        self.assertEqual(producer.parse(failure)["error_type"], "ValueError")
        manifest = producer.parse((f.out / "artifact_manifest.json").read_bytes())
        self.assertEqual(manifest["failure-review.json"]["sha256"], digest(failure))


class ProducerResponseTests(OfflineTest):
    def test_valid_response_exact_answer_and_verdict(self):
        raw = response()
        answer, verdict, model = helper.parse_response(raw)
        self.assertEqual(verdict, accepted())
        self.assertEqual(answer, json.dumps(accepted()).encode())
        self.assertEqual(model, helper.MODEL)
        producer.check_verdict(verdict)

    def test_structured_substantive_prose_is_schema_compatible(self):
        verdict = {**accepted(),
                   "constructive_analysis": [{"source": "Synthetic §1",
                                              "derivation": "Synthetic reconstruction."}],
                   "limitations": [{"scope": "Synthetic limitation."}]}
        producer.check_verdict(verdict)
        auditor.audit_verdict(verdict)

    def test_reject_nonaccepted_and_unresolved_or_missing_verdict_fields(self):
        mutations = [("verdict", "REVISE"), ("verdict", "FAIL"),
                     ("findings", ["open"]), ("missing_assumptions", ["open"]),
                     ("counterexamples", ["counterexample"]), ("limitations", None),
                     ("constructive_analysis", []), ("constructive_analysis", [" "]),
                     ("constructive_analysis", [42]), ("native_bridge_status", "DERIVED_FROM_SOURCES"),
                     ("next_native_obligation", ""), ("next_native_obligation", None)]
        for field, value in mutations:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                producer.check_verdict({**accepted(), field: value})
        for field in accepted():
            value = accepted()
            del value[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                producer.check_verdict(value)

    def test_incomplete_blocked_missing_text_wrong_model_duplicate_response_rejected(self):
        variants = []
        for reason in ("MAX_TOKENS", "SAFETY", "", None):
            obj = json.loads(response())
            obj["candidates"][0]["finishReason"] = reason
            variants.append(encoded(obj))
        variants.extend([response(promptFeedback=dict(blockReason="SAFETY")),
                         response(candidates=[]), response(candidates=[{}, {}]),
                         response(modelVersion="other-model")])
        obj = json.loads(response())
        obj["candidates"][0]["content"]["parts"] = [dict(text="ignored", thought=True)]
        variants.append(encoded(obj))
        variants.append(response().replace(b'"modelVersion":', b'"modelVersion":"wrong", "modelVersion":', 1))
        for raw in variants:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                helper.parse_response(raw)

    def test_nonacceptance_preserves_original_response_answer_verdict(self):
        f = self.fixture
        f.make_integrity()
        verdict = {**accepted(), "verdict": "REVISE", "findings": ["synthetic objection"]}
        raw = response(verdict)
        with self.assertRaisesRegex(ValueError, "Not accepted"):
            f.make_review(MockTransport(raw))
        self.assertEqual((f.out / "response.json").read_bytes(), raw)
        self.assertEqual(producer.parse((f.out / "verdict.json").read_bytes()), verdict)
        self.assertEqual((f.out / "review.txt").read_bytes(), json.dumps(verdict).encode())


class IndependentAuditTests(OfflineTest):
    def setUp(self):
        super().setUp()
        self.assertIsNotNone(auditor, "Independent auditor is required before trigger")

    def mutate_json(self, name, callback):
        path = self.fixture.out / name
        obj = json.loads(path.read_bytes())
        callback(obj)
        path.write_bytes(encoded(obj))
        self.fixture.manifest()

    def test_complete_synthetic_producer_to_independent_audit(self):
        f = self.fixture
        f.evidence()
        result = f.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["scientific_execution"])
        self.assertEqual(result["response_sha256"], digest(response()))
        self.assertEqual(result["native_bridge_status"], "NOT_DERIVED")
        self.assertEqual(result["source_count"], 1)
        self.assertEqual(set(result["original_members"]), auditor.REVIEW_MEMBERS)

    def test_independent_module_does_not_import_producer_or_model_helpers(self):
        import ast
        tree = ast.parse(AUDITOR_PATH.read_text())
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                modules.append(node.module or "")
            elif isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
        self.assertFalse(any(name.startswith(("uqcf_challenge_scope_review",
                                              "uqcf_preparability")) for name in modules))

    def test_reject_altered_exact_prompt_even_with_updated_manifest(self):
        f = self.fixture
        f.evidence()
        path = f.out / "prompt.txt"
        path.write_bytes(path.read_bytes() + b"\n")
        f.manifest()
        self.mutate_json("review_identity.json",
                         lambda obj: obj.update(prompt_sha256=digest(path.read_bytes())))
        with self.assertRaisesRegex(auditor.AuditError, "EXACT_PROMPT"):
            f.audit()

    def test_reject_semantically_same_but_nonexact_request_bytes(self):
        f = self.fixture
        f.evidence()
        path = f.out / "request.json"
        path.write_bytes(json.dumps(json.loads(path.read_bytes()), indent=2).encode())
        f.manifest()
        with self.assertRaisesRegex(auditor.AuditError, "EXACT_REQUEST"):
            f.audit()

    def test_reject_request_prompt_model_settings_and_extra_fields(self):
        f = self.fixture
        mutations = [
            lambda obj: obj["contents"][0]["parts"][0].update(text="altered"),
            lambda obj: obj["generationConfig"].update(temperature=1),
            lambda obj: obj["generationConfig"].update(maxOutputTokens=1),
            lambda obj: obj.update(systemInstruction={"parts": [{"text": "altered"}]})]
        for change in mutations:
            with self.subTest(change=change):
                f.evidence()
                self.mutate_json("request.json", change)
                with self.assertRaisesRegex(auditor.AuditError, "EXACT_REQUEST"):
                    f.audit()

    def test_reject_response_answer_and_verdict_mismatch(self):
        f = self.fixture
        f.evidence()
        self.mutate_json("response.json", lambda obj: obj.update(opaqueSyntheticField="altered"))
        with self.assertRaisesRegex(auditor.AuditError, "RAW_RESPONSE_HASH"):
            f.audit()
        f.evidence()
        path = f.out / "review.txt"
        path.write_bytes(path.read_bytes() + b"\n")
        f.manifest()
        with self.assertRaisesRegex(auditor.AuditError, "RAW_ANSWER"):
            f.audit()
        f.evidence()
        self.mutate_json("verdict.json", lambda obj: obj.update(limitations=["changed"]))
        with self.assertRaisesRegex(auditor.AuditError, "STORED_VERDICT"):
            f.audit()

    def test_reject_incomplete_response_even_if_all_stored_evidence_matches(self):
        f = self.fixture
        f.evidence()
        raw = json.loads((f.out / "response.json").read_bytes())
        raw["candidates"][0]["finishReason"] = "MAX_TOKENS"
        raw = encoded(raw)
        (f.out / "response.json").write_bytes(raw)
        self.mutate_json("review_identity.json",
                         lambda obj: obj.update(response_sha256=digest(raw)))
        with self.assertRaisesRegex(auditor.AuditError, "INCOMPLETE_REVIEW"):
            f.audit()

    def test_reject_consistent_nonaccepted_or_native_derivation(self):
        f = self.fixture
        for change in (dict(verdict="REVISE"), dict(verdict="FAIL"),
                       dict(native_bridge_status="DERIVED_FROM_SOURCES"),
                       dict(findings=["synthetic objection"]),
                       dict(missing_assumptions=["synthetic open assumption"]),
                       dict(counterexamples=["synthetic counterexample"])):
            with self.subTest(change=change):
                f.evidence()
                verdict = {**accepted(), **change}
                raw = response(verdict)
                (f.out / "response.json").write_bytes(raw)
                (f.out / "review.txt").write_bytes(json.dumps(verdict).encode())
                (f.out / "verdict.json").write_bytes(encoded(verdict))
                self.mutate_json("review_identity.json",
                                 lambda obj: obj.update(response_sha256=digest(raw)))
                with self.assertRaises(auditor.AuditError):
                    f.audit()

    def test_reject_cross_job_run_ids_and_attempts(self):
        f = self.fixture
        for filename in ("integrity.json", "review_identity.json"):
            for field, value in (("run_id", "123457"), ("run_attempt", "2"),
                                 ("checkout_sha", SOURCE), ("workflow_sha", SOURCE),
                                 ("freeze_sha", SOURCE), ("target_sha", SOURCE)):
                with self.subTest(filename=filename, field=field):
                    f.evidence()
                    self.mutate_json(filename, lambda obj: obj.update({field: value}))
                    with self.assertRaisesRegex(auditor.AuditError, "IDENTITY_MISMATCH"):
                        f.audit()

    def test_reject_source_record_identity_and_duplicate_excerpt(self):
        f = self.fixture
        with f.audit_patched():
            valid = auditor.audit_source_excerpt(f.source_row, f.source_full)
            self.assertEqual(valid, producer.verify_source(f.source_row, f.source_full))
            for field, value in (("full_bytes", True), ("full_sha256", "0" * 64),
                                 ("git_blob", "0" * 40), ("byte_start", -1),
                                 ("byte_end", 999), ("content", "changed"),
                                 ("path", "../unsafe"), ("path", "null\x00byte")):
                with self.subTest(field=field), self.assertRaises(auditor.AuditError):
                    auditor.audit_source_excerpt({**f.source_row, field: value}, f.source_full)
            packet = copy.deepcopy(f.packet)
            packet["sources"].append(copy.deepcopy(f.source_row))
            with self.assertRaisesRegex(auditor.AuditError, "DUPLICATE_SOURCE"):
                auditor.audit_sources(packet, [valid, valid], f.fetch)
            with self.assertRaisesRegex(auditor.AuditError, "SOURCE_INTEGRITY"):
                auditor.audit_sources(f.packet, [{**valid, "excerpt_sha256": "0" * 64}], f.fetch)

    def test_reject_frozen_remote_target_source_and_helper_mutations(self):
        f = self.fixture
        mutations = [(FREEZE, producer.BASE + "/REVIEW_PROMPT.md"),
                     (TARGET, f.target_path), (SOURCE, f.source_path),
                     (TARGET, ".github/scripts/synthetic_helper.py")]
        for key in mutations:
            with self.subTest(key=key):
                f.evidence()
                original = f.remote_bytes[key]
                f.remote_bytes[key] += b"mutation"
                with self.assertRaises(auditor.AuditError):
                    f.audit()
                f.remote_bytes[key] = original

    def test_reject_artifact_missing_extra_hash_duplicate_and_symlink(self):
        f = self.fixture
        f.evidence()
        path = f.out / "request.json"
        original = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(auditor.AuditError, "UNEXPECTED_OR_MISSING"):
            f.audit()
        path.write_bytes(original)
        (f.out / "extra.bin").write_bytes(b"unreviewed")
        with self.assertRaisesRegex(auditor.AuditError, "UNEXPECTED_OR_MISSING"):
            f.audit()
        (f.out / "extra.bin").unlink()
        path.write_bytes(original + b" ")
        with self.assertRaisesRegex(auditor.AuditError, "MEMBER_HASH"):
            f.audit()
        path.unlink()
        outside = f.root / "outside.json"
        outside.write_bytes(original)
        path.symlink_to(outside)
        with self.assertRaisesRegex(auditor.AuditError, "NONREGULAR"):
            f.audit()

    def test_reject_json_duplicates_nonfinite_and_boolean_number_substitution(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":1e999}'):
            with self.subTest(raw=raw), self.assertRaises(auditor.AuditError):
                auditor.parse_json(raw)
        self.assertFalse(auditor.same_json({"x": True}, {"x": 1}))
        self.assertFalse(auditor.same_json({"x": False}, {"x": 0}))

    def test_independent_live_identity_rejects_wrong_event_branch_attempt(self):
        f = self.fixture
        with f.audit_patched():
            self.assertEqual(auditor.current_identity(f.env, TRIGGER), f.run())
            mutations = dict(GITHUB_RUN_ATTEMPT="2", GITHUB_RUN_ID="0",
                             GITHUB_REPOSITORY="other/repository",
                             GITHUB_REF="refs/heads/main", GITHUB_EVENT_NAME="pull_request",
                             GITHUB_SHA=SOURCE, UQCF_WORKFLOW_SHA=SOURCE,
                             GITHUB_WORKFLOW_SHA=SOURCE)
            for field, value in mutations.items():
                with self.subTest(field=field), self.assertRaises(auditor.AuditError):
                    auditor.current_identity({**f.env, field: value}, TRIGGER)

    def test_independent_trigger_rejects_parent_marker_diff_and_duplicate_run(self):
        f = self.fixture
        f.evidence()
        original_parent = f.parents
        f.parents = SOURCE
        with self.assertRaisesRegex(auditor.AuditError, "TRIGGER_PARENT"):
            f.audit()
        f.parents = original_parent
        f.changes += "\nM\tother"
        with self.assertRaisesRegex(auditor.AuditError, "MARKER_ONLY"):
            f.audit()
        f.changes = "A\t" + producer.MARKER
        f.write(producer.MARKER, encoded(f.marker) + b"\n")
        with self.assertRaisesRegex(auditor.AuditError, "EXACT_TRIGGER"):
            f.audit()
        f.write(producer.MARKER, encoded(f.marker))
        self.mutate_json("integrity.json",
                         lambda obj: obj["unique_run"].update(listed_total=2))
        with self.assertRaisesRegex(auditor.AuditError, "UNIQUE_RUN"):
            f.audit()

    def test_independent_failure_wrapper_preserves_originals_and_sanitizes_error(self):
        f = self.fixture
        f.evidence()
        before = {p.name: p.read_bytes() for p in f.out.iterdir()}
        destination = f.root / "independent-publication"
        with mock.patch.object(auditor, "DEST", destination), \
                mock.patch.object(auditor, "audit", side_effect=RuntimeError(SENTINEL)):
            with self.assertRaises(SystemExit) as caught:
                auditor.main()
            self.assertNotIn(SENTINEL, str(caught.exception))
            for path in destination.iterdir():
                self.assertNotIn(SENTINEL.encode(), path.read_bytes())
            old_output = {p.name: p.read_bytes() for p in destination.iterdir()}
            with self.assertRaisesRegex(SystemExit, "already exists"):
                auditor.main()
            self.assertEqual(old_output, {p.name: p.read_bytes() for p in destination.iterdir()})
        self.assertEqual(before, {p.name: p.read_bytes() for p in f.out.iterdir()})


class StaticWorkflowTests(unittest.TestCase):
    """Inspect only this new workflow; inherited-file diff is a publication gate."""
    @classmethod
    def setUpClass(cls):
        path = HERE / "uqcf-challenge-scope-review.yml"
        if not path.exists():
            path = HERE.parent / "workflows" / "uqcf-challenge-scope-review.yml"
        cls.raw = path.read_text()

    def test_only_exact_marker_push_on_exact_pr_branch(self):
        trigger = self.raw.split("on:\n", 1)[1].split("\npermissions:", 1)[0]
        self.assertEqual(trigger,
                         "  push:\n"
                         "    branches: [gpt/single-event-challenge-scope-20261020]\n"
                         "    paths:\n"
                         "      - '.github/uqcf_challenge_scope_review.trigger'")
        self.assertNotIn("workflow_dispatch", self.raw)
        self.assertNotIn("pull_request_target", self.raw)
        self.assertNotIn("\n  pull_request:", self.raw)

    def test_pinned_actions_read_only_and_exact_checkout_identity(self):
        uses = re.findall(r"uses:\s+(\S+)", self.raw)
        expected = {
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
            "actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093"}
        self.assertTrue(uses)
        self.assertEqual(set(uses), expected)
        self.assertEqual(self.raw.count("fetch-depth: 3"), 3)
        self.assertEqual(self.raw.count("persist-credentials: false"), 3)
        self.assertEqual(self.raw.count("ref: ${{ github.sha }}"), 3)
        self.assertNotRegex(self.raw, r":\s*write\b")
        self.assertIn("  UQCF_WORKFLOW_SHA: ${{ github.workflow_sha }}", self.raw)
        self.assertIn("  UQCF_PUSH_BEFORE: ${{ github.event.before }}", self.raw)

    def test_one_step_local_secret_and_separate_audit_job(self):
        self.assertEqual(self.raw.count("secrets."), 1)
        self.assertRegex(self.raw,
                         r"- name: One independent whole-argument Gemini request\n"
                         r"        env:\n"
                         r"          GEMINI_API_KEY: \$\{\{ secrets.GEMINI_API_KEY \}\}\n"
                         r"        run: python3 .github/scripts/uqcf_challenge_scope_review.py review")
        integrity = self.raw.split("  integrity:\n", 1)[1].split("  argument-review:", 1)[0]
        self.assertIn("    if: github.run_attempt == 1", integrity)
        self.assertIn("      actions: read", integrity)
        self.assertIn("GH_READ_TOKEN: ${{ github.token }}", integrity)
        self.assertIn("run: python3 .github/scripts/uqcf_challenge_scope_tests.py", integrity)
        audit = self.raw.split("  publication-audit:\n", 1)[1]
        self.assertIn("needs: [integrity, argument-review]", audit)
        self.assertIn("run: python3 .github/scripts/uqcf_challenge_scope_publication.py", audit)
        self.assertNotIn("GEMINI_API_KEY", audit)
        self.assertNotIn("secrets.", integrity)

    def test_concurrency_always_upload_and_retention(self):
        self.assertIn("  group: uqcf-pr107-clarification-review", self.raw)
        self.assertIn("  cancel-in-progress: false", self.raw)
        self.assertEqual(self.raw.count("        if: always()"), 3)
        self.assertEqual(self.raw.count("retention-days: 90"), 3)
        self.assertEqual(self.raw.count("if-no-files-found: error"), 3)
        names = re.findall(r"name: (challenge-scope-\S+)", self.raw)
        self.assertEqual(len(names), 5)
        self.assertEqual(len(set(names)), 3)

    def test_freeze_pinned_identically_in_independent_implementations(self):
        self.assertRegex(producer.FREEZE_SHA, r"^[0-9a-f]{40}$")
        self.assertEqual(producer.FREEZE_SHA, auditor.FREEZE_SHA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
