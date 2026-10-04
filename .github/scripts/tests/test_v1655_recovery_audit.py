import copy
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
audit = importlib.import_module("v1655_recovery_audit")


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


if __name__ == "__main__":
    unittest.main()

