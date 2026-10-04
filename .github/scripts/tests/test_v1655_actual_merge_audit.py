"""Mechanical current-run/source/join gates; scientific commands run on GitHub."""
import copy
import importlib
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

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


class PublicationOrchestrationTests(unittest.TestCase):
    api = JoinContractTests.api
    fixtures = JoinContractTests.fixtures
    # Breaks caught: missing transport mkdir, absent exact metadata roles,
    # unchecked control IDs/member maps, duplicate ZIP extraction names.
    def test_original_transport_creates_parent_and_matches_actual_member_bytes(self):
        api = self.api()
        self.assertTrue(callable(getattr(api, "preserve_original", None)),
                        "original transport orchestration is missing")
        payload = b"native-evidence"
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.writestr("evidence.json", payload)
        original = buffer.getvalue()
        item = {"id": 7, "name": "actual-original", "size_in_bytes": len(original),
                "digest": "sha256:" + hashlib.sha256(original).hexdigest()}
        members = [{"name": "evidence.json", "bytes": 15, "sha256": hashlib.sha256(payload).hexdigest()}]
        def external_transport(supplied, destination):
            self.assertEqual(supplied, item)
            destination.write_bytes(original)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = api.preserve_original(item, root / "temporary", root / "publication", members,
                                           download=external_transport)
            self.assertEqual(result["published_at"], "originals/7")
            self.assertEqual(result["bytes"], len(original))
            self.assertFalse((root / "temporary/originals/7.zip").exists())
            manifest = json.loads((root / "publication/originals/7/PARTS.json").read_text())
            reconstructed = b"".join((root / "publication/originals/7" / row["name"]).read_bytes() for row in manifest["parts"])
            self.assertEqual(reconstructed, original)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                api.preserve_original(item, root / "temporary", root / "publication", [],
                                      download=external_transport)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                api.preserve_original(item, root / "temporary", root / "publication",
                                      [dict(members[0], sha256="f" * 64)], download=external_transport)

    def test_component_metadata_requires_exact_roles_not_self_authored_manifest_only(self):
        api = self.api()
        self.assertTrue(callable(getattr(api, "validate_component_roles", None)),
                        "exact component metadata gate is missing")
        common = {name: {} for name in ("STATUS.json", "ORIGINAL_RUN.json", "ORIGINAL_ARTIFACTS.json",
            "PRODUCING_JOBS.json", "EXECUTABLE_SOURCE_BINDING.json", "ORIGINAL_ARCHIVE_AUDIT.json",
            "ORIGINAL_MEMBER_MANIFESTS.json", "MANIFEST.json")}
        extras = {"primary": ("AGGREGATE.json", "SCIENTIFIC_BYTES.json", "FULL_CONTROLS.json"),
                  "reproduction": ("AGGREGATE.json", "SCIENTIFIC_BYTES.json"),
                  "inherited": ("INHERITED_AGGREGATE.json", "FULL_CONTROLS.json")}
        for component, names in extras.items():
            files = {**common, **{name: {} for name in names}}
            api.validate_component_roles(files, component)
            for name in files:
                bad = dict(files); del bad[name]
                with self.subTest(component=component, name=name), self.assertRaises(ValueError):
                    api.validate_component_roles(bad, component)
            with self.assertRaises(ValueError):
                api.validate_component_roles({**files, "recursive.zip": {}}, component)

    def test_control_receipts_require_source_derived_exact_ids(self):
        api = self.api()
        self.assertTrue(callable(getattr(api, "validate_control_receipt", None)),
                        "source-derived control receipt gate is missing")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder, filename in ((BASE + "tests", "test_native.py"),
                                     (".github/scripts/tests", "test_v1655_mechanical.py")):
                path = root / folder / filename; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("class C:\n    def test_witness(self):\n        pass\n")
            receipt = {"status": "PASS", "control_ids": ["test_native.C.test_witness"],
                       "mechanical_control_ids": ["test_v1655_mechanical.C.test_witness"]}
            api.validate_control_receipt(receipt, root)
            for mutation in ({"status": "INCOMPLETE"}, {"control_ids": []},
                             {"control_ids": receipt["control_ids"] * 2},
                             {"mechanical_control_ids": ["test_v1655_mechanical.C.test_substitute"]}):
                with self.assertRaises(ValueError):
                    api.validate_control_receipt(dict(receipt, **mutation), root)

    def test_member_map_requires_each_component_owned_ledger_and_identical_shared_map(self):
        api = self.api(); context, _, _, _, _ = self.fixtures()
        self.assertTrue(callable(getattr(api, "validate_member_maps", None)),
                        "exact original member-map ownership gate is missing")
        files, index = {}, {}
        next_id = 1
        for component, stems in (
            ("primary", ["v1655-full-controls"] + ["v1655-primary-" + str(i) for i in range(8)]),
            ("reproduction", ["v1655-reproduction-" + str(i) for i in range(8)]),
            ("inherited", ["v1655-full-controls", "v1655-inherited-development", "v1655-inherited-foundation"]
                           + ["v1655-inherited-domain-" + str(i) for i in range(8)]),
        ):
            ledger, members = [], {}
            for stem in stems:
                if stem not in index:
                    index[stem] = next_id; next_id += 1
                artifact_id = index[stem]
                ledger.append({"id": artifact_id, "name": stem + "-" + "a" * 40 + "-attempt-2",
                               "bytes": 10, "digest": "sha256:" + "b" * 64})
                members[str(artifact_id)] = [{"name": "source.json", "bytes": 2, "sha256": "c" * 64}]
            files[component] = {"ORIGINAL_ARCHIVE_AUDIT.json": ledger, "ORIGINAL_MEMBER_MANIFESTS.json": members}
        originals = api.validate_original_ledgers([value["ORIGINAL_ARCHIVE_AUDIT.json"] for value in files.values()], context)
        self.assertEqual(len(api.validate_member_maps(files, originals, context)), 27)
        for component in files:
            bad = copy.deepcopy(files)
            bad[component]["ORIGINAL_MEMBER_MANIFESTS.json"].pop(next(iter(bad[component]["ORIGINAL_MEMBER_MANIFESTS.json"])))
            with self.assertRaises(ValueError):
                api.validate_member_maps(bad, originals, context)
        bad = copy.deepcopy(files)
        bad["inherited"]["ORIGINAL_MEMBER_MANIFESTS.json"][str(index["v1655-full-controls"])][0]["sha256"] = "f" * 64
        with self.assertRaises(ValueError):
            api.validate_member_maps(bad, originals, context)

    def test_duplicate_metadata_zip_names_are_rejected_before_extraction(self):
        buffer = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("STATUS.json", b"first")
                archive.writestr("STATUS.json", b"second")
        payload = buffer.getvalue()
        item = {"id": 7, "archive_download_url": "https://api.github.com/repos/proteinfoldingengine/WetLabEngine/actions/artifacts/7/zip",
                "size_in_bytes": len(payload), "digest": "sha256:" + hashlib.sha256(payload).hexdigest()}
        opener = type("ExternalResponse", (), {"open": lambda self, request: io.BytesIO(payload)})()
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(audit.os.environ, {"GH_TOKEN": "fixture-token"}), \
             mock.patch.object(audit.urllib.request, "build_opener", return_value=opener):
            with self.assertRaisesRegex(ValueError, "duplicate ZIP member"):
                audit.download_artifact(item, Path(directory) / "component.zip")


if __name__ == "__main__":
    unittest.main()
