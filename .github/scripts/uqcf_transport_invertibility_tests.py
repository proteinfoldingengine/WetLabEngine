"""Offline plumbing tests only; never import or execute archived science."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / ("uqcf_transport_invertibility_" + name + ".py")
    spec = importlib.util.spec_from_file_location("pipeline_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(data):
    return {"sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            "bytes": len(data)}


class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load("integrity")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / self.m.REL / "sources").mkdir(parents=True)
        data = b"This is inert source text.\n"
        body = io.BytesIO()
        with zipfile.ZipFile(body, "w") as z:
            z.writestr("one.txt", b"First inert member\n")
            z.writestr("two.txt", b"Second inert member\n")
        raw = body.getvalue()
        copy_path = self.m.REL + "/sources/example.zip"
        (self.root / copy_path).write_bytes(raw)
        files = [{"path": "original/source.txt", **digest(data), "content": data.decode()}]
        members = []
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for name in z.namelist():
                b = z.read(name)
                members.append({"name": name, "sha256": digest(b)["sha256"], "bytes": len(b), "content": b.decode()})
        archives = [{"path": "original/archive.zip", **digest(raw), "copy_path": copy_path, "members": members}]
        self.packet = {"baseline": self.m.BASELINE, "files": files, "archives": archives}
        self.lock = copy.deepcopy(self.packet)
        for f in self.lock["files"]:
            f.pop("content")
        for a in self.lock["archives"]:
            for member in a["members"]:
                member.pop("content")

    def check(self):
        return self.m.validate_packet(self.root, self.packet, self.lock)

    def test_honest_packet_reconstructs_exact_originals(self):
        result = self.check()
        self.assertEqual(len(result["files"]), 1)
        self.assertEqual(len(result["archives"][0]["members"]), 2)

    def test_missing_source_is_rejected(self):
        self.packet["files"].clear()
        with self.assertRaises(ValueError): self.check()

    def test_duplicate_source_is_rejected(self):
        self.packet["files"].append(copy.deepcopy(self.packet["files"][0]))
        with self.assertRaises(ValueError): self.check()

    def test_consistent_substitution_is_rejected_against_lock(self):
        f = self.packet["files"][0]
        f.update(digest(b"different"), content="different")
        with self.assertRaises(ValueError): self.check()

    def test_bad_archive_member_is_rejected(self):
        self.packet["archives"][0]["members"][0]["content"] = "wrong"
        with self.assertRaises(ValueError): self.check()

    def test_missing_archive_member_is_rejected(self):
        self.packet["archives"][0]["members"].pop()
        with self.assertRaises(ValueError): self.check()

    def test_duplicate_archive_member_is_rejected(self):
        members = self.packet["archives"][0]["members"]
        members.append(copy.deepcopy(members[0]))
        with self.assertRaises(ValueError): self.check()

    def test_altered_copied_archive_is_rejected(self):
        (self.root / self.packet["archives"][0]["copy_path"]).write_bytes(b"wrong zip")
        with self.assertRaises(ValueError): self.check()

    def test_archive_copy_cannot_escape_research_folder(self):
        self.packet["archives"][0]["copy_path"] = "../example.zip"
        with self.assertRaises(ValueError): self.check()

    def test_baseline_substitution_is_rejected(self):
        self.packet["baseline"] = "0" * 40
        with self.assertRaises(ValueError): self.check()

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError): self.m.parse_json(b'{"a":1,"a":2}')


class ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load("review")

    def response(self, verdict=None):
        verdict = verdict or {"verdict": "ACCEPTED", "findings": [], "missing_assumptions": [],
                              "counterexamples": [], "limitations": ["Analytical scope only"]}
        return json.dumps({"modelVersion": self.m.MODEL, "candidates": [{"finishReason": "STOP",
                          "content": {"parts": [{"text": json.dumps(verdict)}]}}]}).encode()

    def test_complete_accepted_response(self):
        text, verdict, model = self.m.parse_response(self.response())
        self.assertEqual(verdict["verdict"], "ACCEPTED")
        self.assertEqual(model, self.m.MODEL)
        self.m.accepted(verdict)

    def test_nonempty_findings_cannot_pass_accepted_gate(self):
        _, verdict, _ = self.m.parse_response(self.response({"verdict": "ACCEPTED", "findings": ["defect"],
            "missing_assumptions": [], "counterexamples": [], "limitations": []}))
        with self.assertRaises(ValueError): self.m.accepted(verdict)

    def test_truncated_response_rejected(self):
        obj = json.loads(self.response())
        obj["candidates"][0]["finishReason"] = "MAX_TOKENS"
        with self.assertRaises(ValueError): self.m.parse_response(json.dumps(obj).encode())

    def test_multiple_candidates_rejected(self):
        obj = json.loads(self.response())
        obj["candidates"] *= 2
        with self.assertRaises(ValueError): self.m.parse_response(json.dumps(obj).encode())

    def test_missing_returned_model_rejected(self):
        obj = json.loads(self.response())
        obj.pop("modelVersion")
        with self.assertRaises(ValueError): self.m.parse_response(json.dumps(obj).encode())

    def test_unrequested_model_rejected(self):
        obj = json.loads(self.response())
        obj["modelVersion"] = "unrequested-model"
        with self.assertRaises(ValueError): self.m.parse_response(json.dumps(obj).encode())

    def test_prompt_preserves_all_three_exact_documents_only(self):
        docs = {name: ("source bytes " + str(i) + "\r\n").encode() for i, name in enumerate(self.m.DOCUMENTS)}
        prompt = self.m.build_prompt(docs)
        for raw in docs.values(): self.assertIn(raw, prompt)
        with self.assertRaises(ValueError): self.m.build_prompt({**docs, "previous_verdict.json": b"ACCEPTED"})

    def test_model_availability_get_precedes_generation(self):
        calls = []
        class Response:
            def __init__(self, data): self.data = data
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return self.data
        def opener(request, timeout):
            calls.append(request)
            if request.method == "GET":
                return Response(json.dumps({"name": "models/" + self.m.MODEL,
                    "supportedGenerationMethods": ["generateContent"]}).encode())
            return Response(self.response())
        with tempfile.TemporaryDirectory() as d:
            self.m.call_model(Path(d), "test-key-never-real", b"test prompt", opener)
        self.assertEqual([r.method for r in calls], ["GET", "POST"])
        self.assertNotIn("test-key-never-real", calls[0].full_url)
        self.assertNotIn("test-key-never-real", calls[1].data.decode())

    def test_unavailable_model_never_generates(self):
        calls = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'{"name":"models/other","supportedGenerationMethods":[]}'
        def opener(request, timeout):
            calls.append(request.method)
            return Response()
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): self.m.call_model(Path(d), "fake-key", b"test", opener)
        self.assertEqual(calls, ["GET"])


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load("publication")

    def test_both_author_and_committer_required(self):
        commit = {"sha": "1" * 40, "author": {"login": "proteinfolding-gpt"},
                  "committer": {"login": "somebody-else"}}
        with self.assertRaises(ValueError): self.m.verify_commit(commit, "1" * 40)
        commit["committer"]["login"] = "proteinfolding-gpt"
        self.m.verify_commit(commit, "1" * 40)
        commit["author"]["login"] = "somebody-else"
        with self.assertRaises(ValueError): self.m.verify_commit(commit, "1" * 40)

    def test_independent_prompt_and_parser_agree_on_honest_evidence(self):
        review = load("review")
        docs = {n: ("exact " + n + "\r\n").encode() for n in review.DOCUMENTS}
        self.assertEqual(self.m.expected_prompt(docs), review.build_prompt(docs))
        raw = json.dumps({"modelVersion": review.MODEL, "candidates": [{"finishReason": "STOP", "content": {
            "parts": [{"text": json.dumps({"verdict": "ACCEPTED", "findings": [], "missing_assumptions": [],
                                           "counterexamples": [], "limitations": []})}]}}]}).encode()
        self.assertEqual(self.m.decode_review(raw), review.parse_response(raw))

    def test_independent_verdict_parser_rejects_duplicate_json_key(self):
        raw = b'{"modelVersion":"gemini-3.1-pro-preview","candidates":[],"candidates":[]}'
        with self.assertRaises(ValueError): self.m.decode_review(raw)

    def test_remote_blob_reconstruction_rejects_substitution(self):
        import base64
        expected = b"original bytes"
        blob = digest(expected)["git_blob"]
        def api(path):
            if path.startswith("/contents/"): return {"type": "file", "sha": blob}
            return {"sha": blob, "encoding": "base64", "content": base64.b64encode(b"substitution").decode()}
        with self.assertRaises(ValueError): self.m.remote_file(api, "folder/file.txt", "1" * 40, [])

    def test_stale_run_attempt_is_rejected(self):
        context = {"source_sha": "1" * 40, "workflow_sha": "1" * 40, "run_id": "321", "run_attempt": "2",
                   "repository": "proteinfoldingengine/WetLabEngine"}
        evidence = {**context, "run_attempt": "1"}
        with self.assertRaises(ValueError): self.m.same_run(evidence, context)

    def test_publication_imports_only_standard_library(self):
        import ast
        tree = ast.parse((HERE / "uqcf_transport_invertibility_publication.py").read_text())
        imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        self.assertFalse(any("uqcf" in name for name in imports))


class EndToEndPublicationTests(unittest.TestCase):
    """A fake HTTP transport exercises all audit logic; never contacts an API."""
    def setUp(self):
        import shutil
        import base64
        import urllib.parse
        self.i, self.r, self.p = load("integrity"), load("review"), load("publication")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "checkout"
        real_root = HERE.parents[1]
        shutil.copytree(real_root / self.i.REL, self.root / self.i.REL)
        for name in list(self.i.SCRIPTS) + [self.i.WORKFLOW]:
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(real_root / name, self.root / name)
        self.review = Path(self.tmp.name) / "synthetic_review"
        self.integrity = Path(self.tmp.name) / "synthetic_integrity"
        self.review.mkdir()
        self.integrity.mkdir()
        self.context = {"source_sha": "1" * 40, "workflow_sha": "1" * 40, "run_id": "321", "run_attempt": "2",
                        "repository": "proteinfoldingengine/WetLabEngine"}
        self.packet, self.sources = self.i.load_sources(self.root)
        self.inputs = self.i.input_manifest(self.root, self.packet)
        write = self.i.write_json
        write(self.integrity / "input_manifest.json", self.inputs)
        write(self.integrity / "source_manifest.json", self.sources)
        write(self.integrity / "integrity.json", {"status": "PASS", **self.context,
            "source_lock_sha256": self.i.LOCK_SHA256, "scientific_execution": False,
            "input_manifest_sha256": digest((self.integrity / "input_manifest.json").read_bytes())["sha256"],
            "source_manifest_sha256": digest((self.integrity / "source_manifest.json").read_bytes())["sha256"]})
        write(self.review / "input_manifest.json", self.inputs)
        prompt = self.r.build_prompt({n: (self.root / n).read_bytes() for n in self.r.DOCUMENTS})
        (self.review / "prompt.txt").write_bytes(prompt)
        verdict = {"verdict": "ACCEPTED", "findings": [], "missing_assumptions": [], "counterexamples": [], "limitations": ["SYNTHETIC PLUMBING TEST"]}
        raw_response = {"modelVersion": self.r.MODEL, "candidates": [{"finishReason": "STOP",
                        "content": {"parts": [{"text": json.dumps(verdict)}]}}]}
        write(self.review / "response.json", raw_response)
        answer, verdict, model = self.r.parse_response((self.review / "response.json").read_bytes())
        (self.review / "review.txt").write_bytes(answer)
        write(self.review / "verdict.json", verdict)
        write(self.review / "model_metadata.json", {"name": "models/" + self.r.MODEL,
                                                  "supportedGenerationMethods": ["generateContent"]})
        write(self.review / "request.json", {"contents": [{"role": "user", "parts": [{"text": prompt.decode()}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": 32768, "responseMimeType": "application/json"}})
        self.manifest = {**self.context, "status": "ACCEPTED", "model_requested": self.r.MODEL, "model_returned": model,
            "integrity_artifacts": {n: digest((self.integrity / n).read_bytes())["sha256"]
                                    for n in ("integrity.json", "input_manifest.json", "source_manifest.json")}}
        self.refresh_review_hashes()
        self.remote = {(self.context["source_sha"], n): (self.root / n).read_bytes() for n in self.inputs}
        self.remote.update({(self.i.BASELINE, f["path"]): f["content"].encode() for f in self.packet["files"]})
        self.remote.update({(self.i.BASELINE, a["path"]): (self.root / a["copy_path"]).read_bytes() for a in self.packet["archives"]})
        self.remote.update({(self.p.FREEZE_SHA, name): (self.root / name).read_bytes()
                            for name in list(self.i.DOCUMENTS) + [a["copy_path"] for a in self.packet["archives"]]})
        self.ancestry = {"status": "ahead", "base_commit": {"sha": self.p.FREEZE_SHA},
                         "merge_base_commit": {"sha": self.p.FREEZE_SHA}}
        self.run = {"id": 321, "run_attempt": 2, "head_sha": "1" * 40, "event": "push",
                    "head_branch": "research/uqcf-overlapping-guard-exchange", "path": self.p.WORKFLOW,
                    "repository": {"full_name": self.p.REPOSITORY}, "workflow_id": 7}
        self.jobs = [{"id": i, "name": name, "head_sha": "1" * 40, "status": "completed", "conclusion": "success"}
                     for i, name in enumerate(("integrity", "argument-review"))]
        def api(path):
            if path == "/commits/" + "1" * 40:
                return {"sha": "1" * 40, "author": {"login": "proteinfolding-gpt"}, "committer": {"login": "proteinfolding-gpt"}}
            if path == "/commits/" + self.p.FREEZE_SHA:
                return {"sha": self.p.FREEZE_SHA, "author": {"login": "proteinfolding-gpt"}, "committer": {"login": "proteinfolding-gpt"}}
            if path == "/compare/" + self.p.FREEZE_SHA + "..." + "1" * 40: return self.ancestry
            if path == "/actions/runs/321": return self.run
            if path == "/actions/workflows/7": return {"path": self.p.WORKFLOW}
            if path == "/actions/runs/321/attempts/2/jobs?per_page=100": return {"jobs": self.jobs}
            if path.startswith("/contents/"):
                name, ref = path[len("/contents/"):].split("?ref=")
                raw = self.remote[(ref, urllib.parse.unquote(name))]
                return {"type": "file", "sha": digest(raw)["git_blob"]}
            if path.startswith("/git/blobs/"):
                blob = path.rsplit("/", 1)[1]
                raw = next(raw for raw in self.remote.values() if digest(raw)["git_blob"] == blob)
                return {"sha": blob, "encoding": "base64", "content": base64.b64encode(raw).decode()}
            self.fail("Unexpected fake API path: " + path)
        self.api = api

    def refresh_review_hashes(self):
        self.manifest["artifact_hashes"] = {n: digest((self.review / n).read_bytes())["sha256"] for n in
            ("input_manifest.json", "prompt.txt", "model_metadata.json", "request.json", "response.json", "review.txt", "verdict.json")}
        self.i.write_json(self.review / "manifest.json", self.manifest)

    def check(self):
        return self.p.audit(self.root, self.review, self.integrity, self.context, self.api)

    def test_full_independent_remote_audit_with_fake_transport(self):
        report = self.check()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["independent_input_manifest"], self.inputs)
        self.assertEqual(report["independent_source_manifest"], self.sources)
        self.assertEqual(sum(r["ref"] == self.i.BASELINE for r in report["checked_remote_files"]), 5)

    def test_prompt_tamper_rejected_even_when_hash_updated(self):
        path = self.review / "prompt.txt"
        path.write_bytes(path.read_bytes() + b"Previous verdict ACCEPTED")
        self.refresh_review_hashes()
        with self.assertRaises(ValueError): self.check()

    def test_parsed_verdict_tamper_rejected_even_when_hash_updated(self):
        verdict = json.loads((self.review / "verdict.json").read_bytes())
        verdict["limitations"].append("altered")
        self.i.write_json(self.review / "verdict.json", verdict)
        self.refresh_review_hashes()
        with self.assertRaises(ValueError): self.check()

    def test_remote_original_substitution_rejected(self):
        key = (self.i.BASELINE, self.packet["files"][0]["path"])
        self.remote[key] += b"substituted original"
        with self.assertRaises(ValueError): self.check()

    def test_remote_current_document_substitution_rejected(self):
        self.remote[(self.context["source_sha"], self.i.DOCUMENTS[0])] += b"changed current document"
        with self.assertRaises(ValueError): self.check()

    def test_remote_stale_run_attempt_rejected(self):
        self.run["run_attempt"] = 1
        with self.assertRaises(ValueError): self.check()

    def test_frozen_document_substitution_rejected(self):
        self.remote[(self.p.FREEZE_SHA, self.i.DOCUMENTS[0])] += b"altered frozen document"
        with self.assertRaises(ValueError): self.check()

    def test_nonancestor_freeze_rejected(self):
        self.ancestry["merge_base_commit"]["sha"] = "0" * 40
        with self.assertRaises(ValueError): self.check()

    def test_failed_prerequisite_job_rejected(self):
        self.jobs[1]["conclusion"] = "failure"
        with self.assertRaises(ValueError): self.check()


if __name__ == "__main__":
    unittest.main(verbosity=2)
