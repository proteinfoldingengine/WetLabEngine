from __future__ import annotations

import json
import subprocess
import sys
import unittest
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


class EvidenceTests(unittest.TestCase):
    def _repository(self):
        temporary = TemporaryDirectory()
        root = Path(temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        artifact = root / "artifact.txt"
        artifact.write_text("frozen\n")
        subprocess.run(["git", "add", "artifact.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "parent"], cwd=root, check=True)
        parent = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        demo = root / "ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry"
        demo.mkdir(parents=True)
        return temporary, root, demo, artifact, parent

    def test_verified_manifest_reports_blob_ancestry_and_spec_pin(self):
        from evidence import git_blob, verify_evidence

        temporary, root, demo, artifact, parent = self._repository()
        self.addCleanup(temporary.cleanup)
        spec = root / "spec.md"
        spec.write_text("approved\n")
        manifest = {
            "schema": "uqcf-v1543-dependencies-v1",
            "parent": parent,
            "spec": {"path": "spec.md", "blob": git_blob(spec.read_bytes())},
            "evidence": {"artifact": {"path": "artifact.txt", "blob": git_blob(artifact.read_bytes())}},
            "acquisition": {}, "evaluator": {}, "parent_replay": {}, "regression": {},
            "external": {"numpy": "installed-distribution"},
        }
        (demo / "dependencies.json").write_text(json.dumps(manifest))

        with patch("importlib.metadata.version", return_value="installed-distribution"):
            receipt = verify_evidence(root)

        self.assertEqual(receipt["parent"], parent)
        self.assertEqual(receipt["spec"]["blob"], manifest["spec"]["blob"])
        self.assertEqual(receipt["evidence"]["artifact"]["path"], str(artifact.resolve()))

    def test_external_version_mismatch_and_missing_distribution_are_rejected(self):
        from evidence import git_blob, verify_evidence

        temporary, root, demo, artifact, parent = self._repository()
        self.addCleanup(temporary.cleanup)
        manifest = {
            "schema": "uqcf-v1543-dependencies-v1", "parent": parent,
            "spec": {"path": "artifact.txt", "blob": git_blob(artifact.read_bytes())},
            "evidence": {}, "acquisition": {}, "evaluator": {}, "parent_replay": {},
            "regression": {}, "external": {"numpy": "9.9"},
        }
        (demo / "dependencies.json").write_text(json.dumps(manifest))
        with patch("importlib.metadata.version", return_value="9.8"), self.assertRaisesRegex(ValueError, "external dependency"):
            verify_evidence(root)
        with patch("importlib.metadata.version", side_effect=PackageNotFoundError), self.assertRaisesRegex(ValueError, "external dependency"):
            verify_evidence(root)

    def test_repository_only_receipt_makes_no_external_verification_claim(self):
        from evidence import git_blob, verify_repository_evidence

        temporary, root, demo, artifact, parent = self._repository()
        self.addCleanup(temporary.cleanup)
        manifest = {
            "schema": "uqcf-v1543-dependencies-v1", "parent": parent,
            "spec": {"path": "artifact.txt", "blob": git_blob(artifact.read_bytes())},
            "evidence": {}, "acquisition": {}, "evaluator": {}, "parent_replay": {},
            "regression": {}, "external": {"numpy": "9.9"},
        }
        (demo / "dependencies.json").write_text(json.dumps(manifest))
        receipt = verify_repository_evidence(root)
        self.assertNotIn("external", receipt)

    def test_duplicate_manifest_key_at_any_depth_is_rejected(self):
        from evidence import git_blob, verify_repository_evidence

        temporary, root, demo, artifact, parent = self._repository()
        self.addCleanup(temporary.cleanup)
        raw = json.dumps({
            "schema": "uqcf-v1543-dependencies-v1", "parent": parent,
            "spec": {"path": "artifact.txt", "blob": git_blob(artifact.read_bytes())},
            "evidence": {}, "acquisition": {}, "evaluator": {}, "parent_replay": {},
            "regression": {}, "external": {"numpy": "9.9"},
        }).replace('"path": "artifact.txt"', '"path": "other.txt", "path": "artifact.txt"')
        (demo / "dependencies.json").write_text(raw)
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            verify_repository_evidence(root)

    def test_altered_pin_is_rejected(self):
        from evidence import verify_evidence

        temporary, root, demo, artifact, parent = self._repository()
        self.addCleanup(temporary.cleanup)
        manifest = {
            "schema": "uqcf-v1543-dependencies-v1", "parent": parent,
            "spec": {"path": "artifact.txt", "blob": "0" * 40},
            "evidence": {}, "acquisition": {}, "evaluator": {}, "parent_replay": {},
            "regression": {}, "external": {"numpy": "9.9"},
        }
        (demo / "dependencies.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "blob mismatch"):
            verify_evidence(root)

    def test_missing_ancestor_is_rejected(self):
        from evidence import git_blob, verify_evidence

        temporary, root, demo, artifact, _ = self._repository()
        self.addCleanup(temporary.cleanup)
        manifest = {
            "schema": "uqcf-v1543-dependencies-v1", "parent": "1" * 40,
            "spec": {"path": "artifact.txt", "blob": git_blob(artifact.read_bytes())},
            "evidence": {}, "acquisition": {}, "evaluator": {}, "parent_replay": {},
            "regression": {}, "external": {"numpy": "9.9"},
        }
        (demo / "dependencies.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "ancestor"):
            verify_evidence(root)

    def test_origin_spoof_rejected(self):
        from evidence import verify_origins
        with self.assertRaises(ValueError):
            verify_origins((SimpleNamespace(__name__="transport", __file__="/tmp/transport.py"),),
                           {"transport": "df552284c16d43bc876340fbc13fe91eb9ee6a00"})

    def test_forbidden_import_rejected(self):
        from firewall import verify_firewall
        with TemporaryDirectory() as directory:
            path = Path(directory) / "application.py"
            path.write_text("import response_generation\n")
            with self.assertRaisesRegex(ValueError, "forbidden import"):
                verify_firewall((path,))

    def test_acquisition_may_import_source_aware_producer(self):
        from firewall import verify_firewall
        with TemporaryDirectory() as directory:
            path = Path(directory) / "acquire.py"
            path.write_text("import response_generation\n")
            self.assertEqual(verify_firewall((path,))["acquire.py"]["role"], "acquisition")

    def test_dynamic_import_and_evaluation_are_rejected(self):
        from firewall import verify_firewall
        for source in ("__import__('transport')\n", "eval('1 + 1')\n", "from x import *\n"):
            with self.subTest(source=source), TemporaryDirectory() as directory:
                path = Path(directory) / "application.py"
                path.write_text(source)
                with self.assertRaises(ValueError):
                    verify_firewall((path,))

    def test_attribute_dynamic_import_and_reflection_are_rejected(self):
        from firewall import verify_firewall
        sources = ("import importlib\nimportlib.import_module('transport')\n", "value.__class__\n")
        for source in sources:
            with self.subTest(source=source), TemporaryDirectory() as directory:
                path = Path(directory) / "evaluate.py"
                path.write_text(source)
                with self.assertRaises(ValueError):
                    verify_firewall((path,))

    def test_evaluator_has_no_process_capability_but_coordinator_does(self):
        from firewall import verify_firewall
        with TemporaryDirectory() as directory:
            evaluator = Path(directory) / "evaluate.py"
            evaluator.write_text("import subprocess\nsubprocess.run(['true'])\n")
            with self.assertRaisesRegex(ValueError, "forbidden import"):
                verify_firewall((evaluator,))
            coordinator = Path(directory) / "response_geometry_gate.py"
            coordinator.write_text("import subprocess\nsubprocess.run(['true'])\n")
            self.assertEqual(verify_firewall((coordinator,))[coordinator.name]["role"], "entrypoint")

    def test_boundary_modules_pass_their_declared_entrypoint_policy(self):
        from firewall import verify_firewall
        receipt = verify_firewall((HERE / "evidence.py", HERE / "firewall.py"))
        self.assertEqual({entry["role"] for entry in receipt.values()}, {"entrypoint"})


if __name__ == "__main__":
    unittest.main()
