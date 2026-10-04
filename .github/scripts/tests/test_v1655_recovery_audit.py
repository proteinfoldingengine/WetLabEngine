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


class CurrentRunContextTests(unittest.TestCase):
    def setUp(self):
        self.context = audit.AuditContext(500, "a" * 40, 2,
            ".github/workflows/v16.55-renewable-guard-validation.yml",
            "466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f")
        self.provenance = {"run_id": "500", "attempt": "2", "sha": "a" * 40,
                           "workflow_sha": "a" * 40}
        self.metadata = {"id": 500, "run_attempt": 2, "head_sha": "a" * 40,
                         "path": self.context.workflow, "status": "in_progress",
                         "conclusion": None}

    def test_current_run_allows_in_progress_without_spoofing_environment(self):
        self.assertTrue(callable(getattr(audit, "validate_current_run", None)),
                        "current-run validation is not implemented")
        before = dict(os.environ)
        audit.validate_current_run(self.metadata, self.context, self.provenance)
        audit.validate_current_run(dict(self.metadata, status="completed", conclusion="success"),
                                   self.context, self.provenance)
        self.assertEqual(dict(os.environ), before)

    def test_current_run_rejects_every_wrong_identity_and_non_success_terminal(self):
        self.assertTrue(callable(getattr(audit, "validate_current_run", None)),
                        "current-run validation is not implemented")
        for mutation in ({"id": 499}, {"run_attempt": 1}, {"head_sha": "b" * 40},
                         {"path": "other.yml"}, {"status": "completed", "conclusion": "cancelled"},
                         {"status": "completed", "conclusion": "failure"},
                         {"status": "in_progress", "conclusion": "success"}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                audit.validate_current_run(dict(self.metadata, **mutation), self.context, self.provenance)
        for key, value in (("run_id", "499"), ("attempt", "1"), ("sha", "b" * 40),
                           ("workflow_sha", "b" * 40)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                audit.validate_current_run(self.metadata, self.context, dict(self.provenance, **{key: value}))

    def test_current_primary_requires_controls_and_all_eight_successful_producers(self):
        self.assertTrue(callable(getattr(audit, "validate_current_jobs", None)),
                        "producer-job validation is not implemented")
        names = ["controls"] + ["domains (" + str(i) + ")" for i in range(8)]
        jobs = [{"name": name, "run_id": 500, "run_attempt": 2, "head_sha": "a" * 40,
                 "status": "completed", "conclusion": "success"} for name in names]
        audit.validate_current_jobs(jobs, "primary", self.context)
        for bad in (jobs[:-1], jobs + [dict(jobs[0])],
                    [dict(jobs[0], conclusion="skipped")] + jobs[1:],
                    [dict(jobs[0], head_sha="b" * 40)] + jobs[1:],
                    [dict(jobs[0], run_attempt=1)] + jobs[1:]):
            with self.assertRaises(ValueError):
                audit.validate_current_jobs(bad, "primary", self.context)

    def test_current_reproduction_inherited_and_join_require_complete_named_jobs(self):
        self.assertTrue(callable(getattr(audit, "validate_current_jobs", None)),
                        "producer-job validation is not implemented")
        cases = {
            "reproduction": ["reproduction (" + str(i) + ")" for i in range(8)],
            "inherited": ["controls", "inherited-development", "inherited-foundation"]
                         + ["inherited-domains (" + str(i) + ")" for i in range(8)],
            "package": ["audit-primary", "audit-reproduction", "audit-inherited"],
        }
        for component, names in cases.items():
            jobs = [{"name": name, "run_id": 500, "run_attempt": 2, "head_sha": "a" * 40,
                     "status": "completed", "conclusion": "success"} for name in names]
            audit.validate_current_jobs(jobs, component, self.context)
            with self.assertRaises(ValueError):
                audit.validate_current_jobs(jobs[:-1], component, self.context)

    def test_current_artifact_rejects_prior_run_wrong_attempt_and_expiration(self):
        self.assertTrue(callable(getattr(audit, "validate_current_artifact", None)),
                        "current artifact binding is not implemented")
        item = {"id": 100, "name": "v1655-primary-0-" + "a" * 40 + "-attempt-2",
                "size_in_bytes": 10, "digest": "sha256:" + "c" * 64, "expired": False,
                "workflow_run": {"id": 500, "head_sha": "a" * 40}}
        audit.validate_current_artifact(item, self.context)
        for mutation in ({"workflow_run": {"id": 499, "head_sha": "a" * 40}},
                         {"workflow_run": {"id": 500, "head_sha": "b" * 40}},
                         {"name": "v1655-primary-0-" + "a" * 40 + "-attempt-1"},
                         {"expired": True}, {"digest": None}, {"size_in_bytes": 0}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                audit.validate_current_artifact(dict(item, **mutation), self.context)


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


if __name__ == "__main__":
    unittest.main()
