"""Mechanical current-run/source/join gates; scientific commands run on GitHub."""
import copy
import importlib
import importlib.util
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
BASE = "ResearchHistory/UQCF-GEM/demos/v16.55-renewable-guard-repair/"
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / BASE))
transport = importlib.import_module("transport")
audit = importlib.import_module("v1655_recovery_audit")


class MergeSourceTests(unittest.TestCase):
    def test_inventory_requires_entire_external_executable_closure(self):
        self.assertTrue(callable(getattr(transport, "select_inventory", None)),
                        "explicit executable-closure selector is missing")
        paths = [
            ".github/workflows/v16.55-controls.yml",
            ".github/workflows/v16.55-renewable-guard-validation.yml",
            ".github/scripts/v1655_actual_merge_audit.py",
            ".github/scripts/v1655_recovery_audit.py",
            ".github/scripts/v1655_durable_publish.py",
            ".github/scripts/tests/test_v1655_recovery_audit.py",
            ".github/scripts/tests/test_v1655_actual_merge_audit.py",
            BASE + "campaign.py", BASE + "verifier.py", BASE + "transport.py",
            BASE + "MERGE_CONTRACT.json", BASE + "evidence/reviews/report.md",
        ]
        listing = ["100644 blob " + "a" * 40 + "\t" + path for path in paths]
        expected = {path: "a" * 40 for path in paths[:-2]}
        self.assertEqual(transport.select_inventory(listing), expected)
        for path in paths[:7]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                transport.select_inventory([line for line in listing if not line.endswith("\t" + path)])

    def test_merge_contract_rejects_wrong_parents_modified_source_and_exclusions(self):
        self.assertTrue(callable(getattr(transport, "validate_merge_contract", None)),
                        "pure exact merge binding is missing")
        inventory = {"workflow": "a" * 40, "helper": "b" * 40}
        contract = {"integration_parent": "c" * 40, "reviewed_source_parent": "d" * 40,
                    "preregistration_sha": "891470cfc817f26d9721f96278b2c0f8652c3fdf",
                    "reporting_exclusions": list(transport.REPORTING_EXCLUSIONS),
                    "scientific_git_blobs": inventory}
        parents = ["c" * 40, "e" * 40]
        transport.validate_merge_contract(contract, parents, inventory, dict(inventory))
        for bad_parents in ([], parents[:1], ["f" * 40, parents[1]], parents + ["f" * 40]):
            with self.assertRaises(ValueError):
                transport.validate_merge_contract(contract, bad_parents, inventory, inventory)
        for mutation in ({"preregistration_sha": "0" * 40},
                         {"reporting_exclusions": list(transport.REPORTING_EXCLUSIONS) + ["extra.py"]},
                         {"scientific_git_blobs": {"workflow": "a" * 40}}):
            with self.assertRaises(ValueError):
                transport.validate_merge_contract(dict(contract, **mutation), parents, inventory, inventory)
        with self.assertRaises(ValueError):
            transport.validate_merge_contract(contract, parents, inventory, {**inventory, "helper": "f" * 40})


class JoinContractTests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec("v1655_actual_merge_audit"),
                             "actual-merge adapter is not implemented")
        return importlib.import_module("v1655_actual_merge_audit")

    def fixtures(self):
        context = audit.AuditContext(500, "a" * 40, 2, audit.AUDITED_WORKFLOW, audit.CERTIFIED_PARENT)
        provenance = {"run_id": "500", "attempt": "2", "sha": "a" * 40, "workflow_sha": "a" * 40}
        diagnostics = {key: 1 for key in (
            "leveling_donor_recipient_root", "leveling_greedy_vacancy_transfers", "temporarily_inexact_entries",
            "saturated_cycles", "repeated_cycle_colors", "restored_cycle_boundaries", "maximum_layer_conversion",
            "multiple_patch_outside_witness", "noncompact_exact_endpoint", "mixed_grade_completion",
            "sufficient_bound_refusal", "zero_patch_restoration", "zero_capacity_grade", "native_clearance")}
        aggregate = {"status": "PASS", "checked": 3763, "expected": 3763,
                     "errors": [], "incomplete": [], "diagnostics": diagnostics,
                     "serialized_vertices": 2915606, "compressed_bytes": 76665072,
                     "common_degree_greedy_transfers": 0, "strict_slack_X15S_exercised": False,
                     "shard_manifests": {str(i): {name: "b" * 64 for name in
                         ("records.jsonl.gz", "identities.jsonl.gz", "SUMMARY.json", "DOMAIN_FREEZE.json")}
                         for i in range(8)}}
        scientific = {str(i) + "/" + name: "b" * 64 for i in range(8)
                      for name in ("records.jsonl.gz", "identities.jsonl.gz", "SUMMARY.json", "DOMAIN_FREEZE.json")}
        ids = ["m.C.test_" + str(i) for i in range(83)]
        hashes = {str(i) + "/X": "c" * 64 for i in range(77)}
        data = {
            "primary": {"AGGREGATE.json": aggregate, "SCIENTIFIC_BYTES.json": scientific},
            "reproduction": {"AGGREGATE.json": copy.deepcopy(aggregate), "SCIENTIFIC_BYTES.json": dict(scientific)},
            "inherited": {"INHERITED_AGGREGATE.json": {"status": "PASS", "total": 2393450,
                           "control_ids": ids, "certified_hashes": hashes}},
        }
        for component in data:
            data[component]["STATUS.json"] = {"status": "PASS", "component": component,
                "audited": context.as_dict(), "recovery": provenance,
                "numbered_certification": "PENDING_ACTUAL_MERGE_WHOLE_EVIDENCE_REVIEW"}
        return context, provenance, data, ids, hashes

    def test_join_accepts_complete_exact_component_science_without_reexecuting_paths(self):
        api = self.api(); context, provenance, data, ids, hashes = self.fixtures()
        result = api.validate_join(data, context, provenance, ids, hashes)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["numbered_certification"], "PENDING_ACTUAL_MERGE_WHOLE_EVIDENCE_REVIEW")

    def test_join_rejects_missing_incomplete_prior_run_and_premature_certification(self):
        api = self.api(); context, provenance, data, ids, hashes = self.fixtures()
        bad = copy.deepcopy(data); del bad["inherited"]
        with self.assertRaises(ValueError):
            api.validate_join(bad, context, provenance, ids, hashes)
        for mutation in ({"status": "INCOMPLETE"}, {"audited": {**context.as_dict(), "run_id": 499}},
                         {"numbered_certification": "CERTIFIED"}):
            bad = copy.deepcopy(data); bad["primary"]["STATUS.json"].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                api.validate_join(bad, context, provenance, ids, hashes)

    def test_join_rejects_science_mismatch_omitted_diagnostic_and_fake_slack(self):
        api = self.api(); context, provenance, data, ids, hashes = self.fixtures()
        bad = copy.deepcopy(data); bad["reproduction"]["SCIENTIFIC_BYTES.json"]["0/SUMMARY.json"] = "d" * 64
        with self.assertRaises(ValueError):
            api.validate_join(bad, context, provenance, ids, hashes)
        for field, value in (("checked", 3762), ("diagnostics", {}), ("strict_slack_X15S_exercised", True),
                             ("errors", ["failed witness"]), ("serialized_vertices", 10000001)):
            bad = copy.deepcopy(data)
            for component in ("primary", "reproduction"):
                bad[component]["AGGREGATE.json"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                api.validate_join(bad, context, provenance, ids, hashes)

    def test_join_rejects_omitted_duplicate_inherited_ids_and_changed_certified_hash(self):
        api = self.api(); context, provenance, data, ids, hashes = self.fixtures()
        for actual in (ids[:-1], ids[:-1] + [ids[0]]):
            bad = copy.deepcopy(data); bad["inherited"]["INHERITED_AGGREGATE.json"]["control_ids"] = actual
            with self.assertRaises(ValueError):
                api.validate_join(bad, context, provenance, ids, hashes)
        bad = copy.deepcopy(data); bad["inherited"]["INHERITED_AGGREGATE.json"]["certified_hashes"]["0/X"] = "d" * 64
        with self.assertRaises(ValueError):
            api.validate_join(bad, context, provenance, ids, hashes)

    def test_original_ledger_requires_exact_27_names_and_identical_duplicate_rows(self):
        api = self.api(); context, _, _, _, _ = self.fixtures()
        stems = ["v1655-full-controls", "v1655-inherited-development", "v1655-inherited-foundation"]
        stems += ["v1655-" + mode + "-" + str(i) for mode in ("primary", "reproduction", "inherited-domain") for i in range(8)]
        rows = [{"id": i + 1, "name": stem + "-" + "a" * 40 + "-attempt-2",
                 "bytes": 10, "digest": "sha256:" + "b" * 64, "local_archive": "temporary/" + str(i) + ".zip"}
                for i, stem in enumerate(stems)]
        result = api.validate_original_ledgers([rows, [dict(rows[0])]], context)
        self.assertEqual(len(result), 27)
        for bad in ([rows[:-1]], [rows, [dict(rows[0], bytes=11)]],
                    [rows[:-1] + [dict(rows[-1], id=rows[0]["id"])]]):
            with self.assertRaises(ValueError):
                api.validate_original_ledgers(bad, context)


if __name__ == "__main__":
    unittest.main()
