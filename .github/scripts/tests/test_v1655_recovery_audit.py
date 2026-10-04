import copy
import importlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
audit = importlib.import_module("v1655_recovery_audit")
publish = importlib.import_module("v1655_durable_publish")


class RecoveryContextTests(unittest.TestCase):
    def setUp(self):
        self.request = {
            "audited_run_id": 37180275767,
            "audited_sha": "60c48b818366354d26366af35726788553865455",
            "audited_attempt": 1,
            "audited_workflow": ".github/workflows/v16.55-renewable-guard-validation.yml",
            "certified_parent": "466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f",
            "mode": "publication_recovery",
        }

    def test_exact_original_tuple_is_required(self):
        context = audit.validate_request(self.request)
        self.assertEqual(context.run_id, 37180275767)
        self.assertEqual(context.sha, "60c48b818366354d26366af35726788553865455")
        self.assertEqual(context.attempt, 1)
        for key, value in (("audited_run_id", 0), ("audited_sha", "0" * 40), ("audited_attempt", 2)):
            bad = copy.deepcopy(self.request)
            bad[key] = value
            with self.assertRaises(ValueError):
                audit.validate_request(bad)

    def test_original_run_metadata_is_checked_without_environment_spoofing(self):
        context = audit.validate_request(self.request)
        metadata = {
            "id": context.run_id,
            "run_attempt": context.attempt,
            "head_sha": context.sha,
            "path": context.workflow,
            "status": "completed",
            "conclusion": "cancelled",
        }
        before = dict(os.environ)
        audit.validate_original_run(metadata, context)
        self.assertEqual(dict(os.environ), before)
        bad = dict(metadata, head_sha="f" * 40)
        with self.assertRaises(ValueError):
            audit.validate_original_run(bad, context)

    def test_expected_artifact_names_are_exact(self):
        context = audit.validate_request(self.request)
        self.assertEqual(
            audit.original_artifact_name("v1655-primary-3", context),
            "v1655-primary-3-60c48b818366354d26366af35726788553865455-attempt-1",
        )


class EvidenceContractTests(unittest.TestCase):
    def test_each_inherited_domain_requires_exact_archived_source(self):
        wanted = {"campaign.py": "a" * 64, "verifier.py": "b" * 64}
        audit.validate_exact_source_manifest(dict(wanted), dict(wanted), wanted)
        with self.assertRaises(ValueError):
            audit.validate_exact_source_manifest(dict(wanted), {"campaign.py": "a" * 64}, wanted)
        with self.assertRaises(ValueError):
            audit.validate_exact_source_manifest({**wanted, "extra.py": "c" * 64}, dict(wanted), wanted)

    def test_inherited_domain_source_inventory_matches_frozen_selector(self):
        base = "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity"
        paths = [
            base + "/campaign.py",
            base + "/README.md",
            base + "/protocol.json",
            base + "/CERTIFICATION.json",
            base + "/tests/test_campaign.py",
            base + "/tests/fixture.json",
            base + "/evidence/result.json",
            base + "/nested/proof.md",
        ]
        self.assertEqual(
            audit.domain_source_relatives(paths, base),
            ["campaign.py", "README.md", "protocol.json", "tests/test_campaign.py"],
        )

    def test_foundation_metadata_binds_original_run_without_spoofing(self):
        context = audit.validate_request({
            "audited_run_id": 37180275767,
            "audited_sha": "60c48b818366354d26366af35726788553865455",
            "audited_attempt": 1,
            "audited_workflow": ".github/workflows/v16.55-renewable-guard-validation.yml",
            "certified_parent": "466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f",
            "mode": "publication_recovery",
        })
        metadata = {
            "head": context.sha,
            "workflow_sha": context.sha,
            "trigger_sha": context.sha,
            "run_id": str(context.run_id),
            "run_attempt": str(context.attempt),
            "verified_parent": "b6bf95798ec5892963c29f4020f8b75069fd2e3b",
            "preregistration": "8fcc46597ab7c2b83fe9dd2fd0611a07e66169cd",
        }
        before = dict(os.environ)
        audit.validate_foundation_metadata(metadata, context)
        self.assertEqual(dict(os.environ), before)
        with self.assertRaises(ValueError):
            audit.validate_foundation_metadata({**metadata, "run_id": "0"}, context)

    def test_component_status_requires_terminal_pass_and_both_provenances(self):
        context = audit.validate_request({
            "audited_run_id": 37180275767,
            "audited_sha": "60c48b818366354d26366af35726788553865455",
            "audited_attempt": 1,
            "audited_workflow": ".github/workflows/v16.55-renewable-guard-validation.yml",
            "certified_parent": "466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f",
            "mode": "publication_recovery",
        })
        recovery = {"run_id": "400", "attempt": "1", "sha": "a" * 40, "workflow_sha": "a" * 40}
        status = {"status": "PASS", "component": "primary", "audited": context.as_dict(), "recovery": recovery}
        audit.validate_component_status(status, "primary", context, recovery)
        for mutation in (
            dict(status="INCOMPLETE"),
            dict(component="reproduction"),
            dict(audited={**context.as_dict(), "attempt": 2}),
        ):
            bad = dict(status)
            bad.update(mutation)
            with self.assertRaises(ValueError):
                audit.validate_component_status(bad, "primary", context, recovery)

    def test_primary_and_reproduction_require_exact_scientific_bytes(self):
        primary = {"0/records.jsonl.gz": "a" * 64, "1/records.jsonl.gz": "b" * 64}
        audit.compare_scientific_bytes(primary, dict(primary))
        with self.assertRaises(ValueError):
            audit.compare_scientific_bytes(primary, {**primary, "1/records.jsonl.gz": "c" * 64})
        with self.assertRaises(ValueError):
            audit.compare_scientific_bytes(primary, {"0/records.jsonl.gz": "a" * 64})

    def test_inherited_baseline_requires_83_ids_and_77_hashes(self):
        expected_ids = [f"m.C.test_{i}" for i in range(83)]
        expected_hashes = {f"{i}/X": f"{i:064x}" for i in range(77)}
        audit.validate_inherited_baseline(expected_ids, list(expected_ids), expected_hashes, dict(expected_hashes))
        with self.assertRaises(ValueError):
            audit.validate_inherited_baseline(expected_ids, expected_ids[:-1], expected_hashes, dict(expected_hashes))
        with self.assertRaises(ValueError):
            audit.validate_inherited_baseline(expected_ids, list(expected_ids), expected_hashes, {**expected_hashes, "extra": "0" * 64})


class DurablePublicationTests(unittest.TestCase):
    def setUp(self):
        self.request = {
            "recovery_run_id": 37196753029,
            "recovery_attempt": 1,
            "recovery_sha": "a75c82f31c5547bf20feb75960fbedf2f7e5c0a6",
            "package_artifact_id": 11301883937,
            "package_artifact_bytes": 1207019319,
            "package_artifact_digest": "sha256:ca76f0dbc839c3899f0162cf7475c06f69ef8c7f7e22b11ebc1e6199606b0bbe",
            "audited_run_id": 37180275767,
            "audited_sha": "60c48b818366354d26366af35726788553865455",
            "audited_attempt": 1,
            "source_parent": "f" * 40,
        }

    def test_exact_package_tuple_is_required(self):
        self.assertEqual(publish.validate_request(self.request), self.request)
        for key, value in (
            ("recovery_run_id", 0),
            ("recovery_sha", "0" * 40),
            ("package_artifact_id", 0),
            ("package_artifact_bytes", 1),
            ("package_artifact_digest", "sha256:" + "0" * 64),
            ("audited_run_id", 0),
        ):
            bad = dict(self.request)
            bad[key] = value
            with self.assertRaises(ValueError):
                publish.validate_request(bad)

    def test_split_parts_reconstruct_exact_bytes_and_digest(self):
        payload = bytes(range(251)) * 41
        expected = publish.sha256_bytes(payload)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "package.zip"
            destination = Path(directory) / "parts"
            source.write_bytes(payload)
            manifest = publish.split_archive(source, destination, len(payload), expected, part_bytes=1024)
            self.assertEqual(manifest["bytes"], len(payload))
            self.assertEqual(manifest["sha256"], expected)
            self.assertGreater(len(manifest["parts"]), 1)
            self.assertEqual(publish.verify_parts(destination), (len(payload), expected))
            (destination / manifest["parts"][0]["name"]).write_bytes(b"corrupt")
            with self.assertRaises(ValueError):
                publish.verify_parts(destination)

    def test_artifact_redirect_does_not_forward_github_credentials(self):
        api_url = "https://api.github.com/repos/proteinfoldingengine/WetLabEngine/actions/artifacts/11301883937/zip"
        signed_url = "https://blob.example/package.zip?sig=secret"
        seen = {}

        class RedirectOpener:
            def open(self, request):
                seen["api"] = request
                raise urllib.error.HTTPError(request.full_url, 302, "Found", {"Location": signed_url}, None)

        def signed_open(request):
            seen["signed"] = request
            return io.BytesIO(b"package-bytes")

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "package.zip"
            publish.download(
                {"archive_download_url": api_url},
                destination,
                api_opener=RedirectOpener(),
                signed_open=signed_open,
                token="github-secret",
            )
            self.assertEqual(destination.read_bytes(), b"package-bytes")
        self.assertEqual(seen["api"].get_header("Authorization"), "Bearer github-secret")
        self.assertIsNone(seen["signed"].get_header("Authorization"))
        self.assertEqual(dict(seen["signed"].header_items()), {})

    def test_split_rejects_wrong_size_or_digest(self):
        payload = b"native-evidence" * 100
        expected = publish.sha256_bytes(payload)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "package.zip"
            source.write_bytes(payload)
            with self.assertRaises(ValueError):
                publish.split_archive(source, Path(directory) / "size", len(payload) + 1, expected, part_bytes=100)
            with self.assertRaises(ValueError):
                publish.split_archive(source, Path(directory) / "digest", len(payload), "0" * 64, part_bytes=100)


if __name__ == "__main__":
    unittest.main()
