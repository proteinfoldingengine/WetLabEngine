"""UNEXECUTED test-first specifications for the D24 archival preparation.

Written before verify_archive.py. No import or test run was performed during
preparation, by explicit instruction. This is not claimed as a RED/GREEN cycle.
Tiny fixtures exercise arithmetic/schema helpers ONLY; they are deliberately
not archives and cannot establish scientific coverage. The integration suite
requires real, separately authorized complete regenerated archives plus the
original pinned summaries. Never fabricate a complete accepted fixture.

Future use, only after separate execution authorization:
  python -m unittest discover -s <package-directory> -p test_archive_mutations.py
Set all four D24_* input-path environment variables below to enable full-archive
controls. Their absence produces explicit skipped integration tests, never a
claim that complete coverage passed. Exporter subprocess tests additionally
require D24_EXPORTER_EXECUTION_AUTHORIZED=yes.
Fresh byte-reproduction checks require D24_FRESH_PRODUCER_ARCHIVE and
D24_FRESH_CHECKER_ARCHIVE, produced separately under authorization. Acceptance
requires ALL integration, fresh-reproduction and exporter controls enabled with
zero skipped required controls; unittest OK with skips is insufficient. Distinct
files and identical bytes do not prove independent runs: that provenance belongs
in the future separately pinned outer execution manifest.
"""

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction

import verify_archive as V


def assert_fresh_archive_bytes(original_path, fresh_path):
    """Test-only byte comparison; does not certify scientific contents or run provenance."""
    original, fresh = Path(original_path), Path(fresh_path)
    if original.resolve() == fresh.resolve() or original.samefile(fresh):
        raise AssertionError("fresh reproduction path must be distinct from original")
    original_bytes, fresh_bytes = original.read_bytes(), fresh.read_bytes()
    for raw in (original_bytes, fresh_bytes):
        if raw != V.canonical_bytes(V.strict_loads(raw)):
            raise AssertionError("fresh comparison requires canonical deterministic JSON bytes")
    if original_bytes != fresh_bytes:
        raise AssertionError("complete fresh archive bytes differ")


def tiny_constraints():
    """Unrelated three-variable toy LP: x00=1, x11=x00, 0<=x10<=x00."""
    keys = ((0, 0), (1, 0), (1, 1))
    rows = (
        (((1, 0), 1),),
        (((0, 0), 1), ((1, 0), -1)),
        (((1, 1), 1),),
    )
    equalities = (
        ((((0, 0), 1),), Fraction(1)),
        ((((0, 0), -1), ((1, 1), 1)), Fraction(0)),
    )
    return keys, rows, equalities


def tiny_endpoint(sense=1):
    return {
        "target": [1, 0], "sense": sense,
        "value": "0" if sense == 1 else "1",
        "primal": ["1", "0" if sense == 1 else "1", "1"],
        "ineq_multipliers": ["1", "0", "0"] if sense == 1 else ["0", "1", "0"],
        "eq_multipliers": ["0", "0"] if sense == 1 else ["-1", "0"],
    }


class TinyArithmeticAndSchemaSpecifications(unittest.TestCase):
    def check_endpoint(self, endpoint):
        keys, rows, equalities = tiny_constraints()
        return V.check_endpoint(endpoint, "A", keys, rows, equalities,
                                (1, 0), endpoint["sense"])

    def test_toy_lower_and_upper_have_exact_certificates(self):
        self.assertEqual(self.check_endpoint(tiny_endpoint()), Fraction(0))
        self.assertEqual(self.check_endpoint(tiny_endpoint(-1)), Fraction(1))

    def test_rationals_are_strings_in_fraction_canonical_form(self):
        for invalid in (1, True, 0.5, None, "1.0", "0/1", "2/4", "+1", "01",
                        "-0", "1/-2", " 1", "1 ", "NaN", "Infinity", "1/0"):
            with self.subTest(invalid=invalid), self.assertRaises(V.ArchiveError):
                V.parse_rational(invalid)
        self.assertEqual(V.parse_rational("-1/2"), Fraction(-1, 2))

    def test_duplicate_json_keys_are_rejected_at_every_depth(self):
        for data in ('{"x":1,"x":2}', '{"a":{"x":1,"x":1}}'):
            with self.assertRaisesRegex(V.ArchiveError, "duplicate JSON key"):
                V.strict_loads(data)

    def test_float_and_nonfinite_json_numbers_are_rejected(self):
        for data in ('{"x":1.0}', '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(V.ArchiveError):
                V.strict_loads(data)

    def test_exact_integer_types_reject_booleans(self):
        for value in (True, False, 1.0, "1"):
            with self.assertRaises(V.ArchiveError):
                V.exact_int(value, "toy integer")

    def test_schema_rejects_unknown_and_missing_fields(self):
        for obj in ({"x": 1, "extra": 2}, {}):
            with self.assertRaises(V.ArchiveError):
                V.exact_fields(obj, {"x"}, "toy schema")

    def test_sparse_rows_reject_zero_boolean_duplicate_and_unordered_terms(self):
        keys, _, _ = tiny_constraints()
        invalid_rows = ([[0, 0, 0]], [[0, 0, True]], [[0, 0, 1], [0, 0, 2]],
                        [[1, 0, 1], [0, 0, 1]], [[3, 0, 1]], [])
        for row in invalid_rows:
            with self.subTest(row=row), self.assertRaises(V.ArchiveError):
                V.parse_sparse_row(row, keys, "toy row")

    def test_endpoint_identity_rejects_missing_extra_duplicate_and_reordering(self):
        valid = [tiny_endpoint(), tiny_endpoint(-1)]
        V.check_endpoint_identities(valid, ((1, 0),))
        for endpoints in (valid[:1], valid + [valid[0]], [valid[0], valid[0]],
                          list(reversed(valid))):
            with self.assertRaisesRegex(V.ArchiveError, "endpoint identities"):
                V.check_endpoint_identities(endpoints, ((1, 0),))

    def test_altered_primal_is_rejected(self):
        endpoint = tiny_endpoint()
        endpoint["primal"][1] = "-1"
        with self.assertRaisesRegex(V.ArchiveError, "primal infeasible"):
            self.check_endpoint(endpoint)

    def test_negative_inequality_multiplier_is_rejected(self):
        endpoint = tiny_endpoint()
        endpoint["ineq_multipliers"][0] = "-1"
        with self.assertRaisesRegex(V.ArchiveError, "negative inequality multiplier"):
            self.check_endpoint(endpoint)

    def test_incorrect_dual_is_rejected(self):
        endpoint = tiny_endpoint()
        endpoint["ineq_multipliers"][0] = "2"
        with self.assertRaisesRegex(V.ArchiveError, "dual identity"):
            self.check_endpoint(endpoint)

    def test_feasible_but_nonattaining_primal_is_rejected(self):
        endpoint = tiny_endpoint()
        endpoint["primal"][1] = "1/2"
        with self.assertRaisesRegex(V.ArchiveError, "primal-dual gap"):
            self.check_endpoint(endpoint)

    def test_wrong_unsigned_endpoint_value_is_rejected(self):
        endpoint = tiny_endpoint(-1)
        endpoint["value"] = "-1"
        with self.assertRaisesRegex(V.ArchiveError, "endpoint value"):
            self.check_endpoint(endpoint)

    def test_vector_length_and_sense_types_are_strict(self):
        endpoint = tiny_endpoint()
        endpoint["primal"].append("0")
        with self.assertRaises(V.ArchiveError):
            self.check_endpoint(endpoint)
        endpoint = tiny_endpoint()
        endpoint["sense"] = True
        with self.assertRaises(V.ArchiveError):
            self.check_endpoint(endpoint)

    def test_noncanonical_tree_strings_are_rejected(self):
        for carrier in ("", "()()", "(()", "(x)", "(()(()))"):
            with self.assertRaises(V.ArchiveError):
                V.parse_carrier(carrier)
        self.assertEqual(V.tree_string(V.parse_carrier("((())())")), "((())())")

    def test_deterministic_serialization_ignores_dictionary_insertion_order(self):
        a = {"z": "é", "a": ["1/2", 1]}
        b = {"a": ["1/2", 1], "z": "é"}
        self.assertEqual(V.canonical_bytes(a), V.canonical_bytes(b))
        self.assertTrue(V.canonical_bytes(a).endswith(b"\n"))
        self.assertIn("é".encode("utf-8"), V.canonical_bytes(a))

    def test_report_creation_is_exclusive_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "report.json"
            target.write_bytes(b"existing evidence\n")
            with self.assertRaises(FileExistsError):
                V.write_new_json(target, {"status": "RED"})
            self.assertEqual(target.read_bytes(), b"existing evidence\n")

    def test_fresh_comparison_rejects_same_path_and_changed_bytes(self):
        # These objects are explicitly toy serializer fixtures, not D24 archives.
        with tempfile.TemporaryDirectory() as directory:
            original, fresh = Path(directory) / "toy-original.json", Path(directory) / "toy-fresh.json"
            original.write_bytes(V.canonical_bytes({"fixture_kind": "toy", "value": "1"}))
            fresh.write_bytes(V.canonical_bytes({"fixture_kind": "toy", "value": "2"}))
            with self.assertRaisesRegex(AssertionError, "must be distinct"):
                assert_fresh_archive_bytes(original, original)
            with self.assertRaisesRegex(AssertionError, "complete fresh archive bytes differ"):
                assert_fresh_archive_bytes(original, fresh)

    def test_complete_domain_may_not_be_replaced_by_a_tiny_fixture(self):
        report = V.validate_bundle_objects({}, {}, {}, {}, "0" * 64, "0" * 64)
        self.assertEqual(report["status"], "RED")
        self.assertTrue(report["errors"])

    def test_public_validator_has_no_supplied_domain_override(self):
        with self.assertRaises(TypeError):
            V.validate_bundle_objects({}, {}, {}, {}, "0" * 64, "0" * 64, expected={})

    def test_missing_report_parent_is_rejected_before_input_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            absent = Path(directory) / "missing-parent" / "report.json"
            result = subprocess.run([sys.executable, str(Path(V.__file__)),
                                     "absent-producer", "absent-checker", "absent-original-p",
                                     "absent-original-c", str(absent)],
                                    capture_output=True, text=True, timeout=15, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("report parent", result.stderr)
            self.assertFalse(absent.exists())


INPUT_ENV = ("D24_PRODUCER_ARCHIVE", "D24_CHECKER_ARCHIVE",
             "D24_ORIGINAL_PRODUCER_JSON", "D24_ORIGINAL_CHECKER_JSON")


@unittest.skipUnless(all(os.environ.get(name) for name in INPUT_ENV),
                     "Requires real complete archives from separately authorized execution")
class CompleteArchiveMutationSpecifications(unittest.TestCase):
    """Never synthesizes an accepted archive. Mutation baseline is supplied evidence."""

    @classmethod
    def setUpClass(cls):
        paths = [Path(os.environ[name]) for name in INPUT_ENV]
        cls.archive_paths = {"producer": paths[0], "checker": paths[1]}
        cls.original_paths = {"producer": paths[2], "checker": paths[3]}
        cls.producer = V.strict_loads(paths[0].read_bytes())
        cls.checker = V.strict_loads(paths[1].read_bytes())
        cls.original_producer = V.load_original_summary(paths[2], "producer")
        cls.original_checker = V.load_original_summary(paths[3], "checker")
        cls.producer_export_sha = V.sibling_exporter_sha256("producer")
        cls.checker_export_sha = V.sibling_exporter_sha256("checker")
        cls.baseline = cls.validate(cls.producer, cls.checker)
        if cls.baseline["status"] != "VERIFIED":
            raise AssertionError("The unmodified real evidence must first verify: "
                                 + json.dumps(cls.baseline, sort_keys=True))

    @classmethod
    def validate(cls, producer, checker):
        return V.validate_bundle_objects(
            producer, checker, cls.original_producer, cls.original_checker,
            cls.producer_export_sha, cls.checker_export_sha)

    def mutation(self, change, fragment):
        for role in ("producer", "checker"):
            with self.subTest(role=role):
                producer, checker = copy.deepcopy(self.producer), copy.deepcopy(self.checker)
                archive = producer if role == "producer" else checker
                change(archive)
                report = self.validate(producer, checker)
                self.assertEqual(report["status"], "RED")
                self.assertTrue(any(fragment in error for error in report["errors"]),
                                report["errors"])

    def test_complete_accepted_domain_identity_and_coverage(self):
        self.assertEqual(self.baseline["coverage"]["producer"]["classes"], 30)
        self.assertEqual(self.baseline["coverage"]["checker"]["systems"], 80)
        for role in ("producer", "checker"):
            self.assertEqual(self.baseline["coverage"][role]["targets"], 1030)
            self.assertEqual(self.baseline["coverage"][role]["endpoints"], 2060)
        self.assertEqual(self.baseline["diagnostic_scope"]["checker"], "attainment_only")

    @unittest.skipUnless(os.environ.get("D24_FRESH_PRODUCER_ARCHIVE")
                         and os.environ.get("D24_FRESH_CHECKER_ARCHIVE"),
                         "Requires separate authorized fresh-reproduction archive paths")
    def test_separate_fresh_exports_match_complete_archives_byte_for_byte(self):
        fresh_producer = Path(os.environ["D24_FRESH_PRODUCER_ARCHIVE"])
        fresh_checker = Path(os.environ["D24_FRESH_CHECKER_ARCHIVE"])
        fresh_report = V.validate_files(fresh_producer, fresh_checker,
                                        self.original_paths["producer"], self.original_paths["checker"])
        self.assertEqual(fresh_report["status"], "VERIFIED", fresh_report["errors"])
        for role, variable in (("producer", "D24_FRESH_PRODUCER_ARCHIVE"),
                               ("checker", "D24_FRESH_CHECKER_ARCHIVE")):
            with self.subTest(role=role):
                assert_fresh_archive_bytes(self.archive_paths[role], Path(os.environ[variable]))

    def test_full_file_validation_rejects_altered_whitespace_and_key_order(self):
        variants = {
            "whitespace": (json.dumps(self.producer, sort_keys=True, indent=4, ensure_ascii=False)
                           + "\n").encode("utf-8"),
            "key_order": (json.dumps(dict(reversed(list(self.producer.items()))),
                                     sort_keys=False, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
        }
        with tempfile.TemporaryDirectory() as directory:
            for name, raw in variants.items():
                with self.subTest(mutation=name):
                    mutated = Path(directory) / (name + ".json")
                    mutated.write_bytes(raw)
                    report = V.validate_files(mutated, self.archive_paths["checker"],
                                               self.original_paths["producer"], self.original_paths["checker"])
                    self.assertEqual(report["status"], "RED")
                    self.assertTrue(any("not canonical deterministic JSON" in error
                                        for error in report["errors"]), report["errors"])

    def test_wrong_evidence_kind(self):
        self.mutation(lambda a: a.__setitem__("evidence_kind", "original"), "evidence_kind")

    def test_wrong_origin_and_bool_attempt(self):
        for field in ("code_sha", "result_sha256", "freeze_sha256", "source_sha256", "summary_sha256"):
            with self.subTest(field=field):
                self.mutation(lambda a: a["origin"].__setitem__(field, "forged"), "origin")
        self.mutation(lambda a: a["origin"].__setitem__("run_id", 39300667906), "origin")
        self.mutation(lambda a: a["origin"].__setitem__("attempt", True), "origin")

    def test_missing_extra_and_count_preserving_substituted_class(self):
        self.mutation(lambda a: a["classes"].pop("BIN_5"), "class identities")
        def add_extra(a):
            a["classes"]["BOGUS"] = copy.deepcopy(a["classes"]["BIN_5"])
        self.mutation(add_extra, "class identities")
        def substitute(a):
            a["classes"]["BOGUS"] = a["classes"].pop("BIN_5")
        self.mutation(substitute, "class identities")

    def test_missing_duplicated_and_count_preserving_target_substitution(self):
        def targets(a): return a["systems"]["BIN_5|D=1"]["targets"]
        self.mutation(lambda a: targets(a).pop(), "target identities")
        self.mutation(lambda a: targets(a).__setitem__(1, copy.deepcopy(targets(a)[0])),
                      "target identities")
        self.mutation(lambda a: targets(a).__setitem__(1, [2, 0]), "target identities")

    def test_missing_or_altered_equalities_and_wrong_blindness(self):
        def system(a): return a["systems"]["BIN_5|D=1"]
        self.mutation(lambda a: system(a)["equalities"].pop(), "equalities")
        self.mutation(lambda a: system(a)["equalities"][0].__setitem__("rhs", "2"), "equalities")
        self.mutation(lambda a: system(a).__setitem__("blind", False), "blind")

    def test_forged_exporter_hash(self):
        self.mutation(lambda a: a.__setitem__("exporter_sha256", "0" * 64), "exporter_sha256")

    def test_caller_cannot_substitute_expected_exporter_digests(self):
        producer, checker = copy.deepcopy(self.producer), copy.deepcopy(self.checker)
        producer["exporter_sha256"] = checker["exporter_sha256"] = "0" * 64
        report = V.validate_bundle_objects(producer, checker, self.original_producer,
                                           self.original_checker, "0" * 64, "0" * 64)
        self.assertEqual(report["status"], "RED")
        self.assertTrue(any("actual sibling" in error for error in report["errors"]))

    def test_forged_legacy_summary_hash(self):
        self.mutation(lambda a: a.__setitem__("legacy_summary_sha256", "0" * 64),
                      "legacy_summary_sha256")

    def test_missing_extra_and_duplicated_endpoint(self):
        def endpoints(a): return a["systems"]["BIN_5|D=1"]["endpoints"]
        self.mutation(lambda a: endpoints(a).pop(), "endpoint identities")
        self.mutation(lambda a: endpoints(a).append(copy.deepcopy(endpoints(a)[0])),
                      "endpoint identities")
        self.mutation(lambda a: endpoints(a).__setitem__(1, copy.deepcopy(endpoints(a)[0])),
                      "endpoint identities")

    def test_missing_and_count_preserving_substituted_system(self):
        self.mutation(lambda a: a["systems"].pop("BIN_5|D=1"), "system identities")
        def substitute(a):
            a["systems"]["BOGUS|D=1"] = a["systems"].pop("BIN_5|D=1")
        self.mutation(substitute, "system identities")

    def test_missing_duplicate_and_substituted_row(self):
        self.mutation(lambda a: a["classes"]["BIN_5"]["pos_rows"].pop(), "pos_rows")
        def duplicate(a):
            rows = a["classes"]["BIN_5"]["pos_rows"]
            rows[1] = copy.deepcopy(rows[0])
        self.mutation(duplicate, "pos_rows")
        def substitute(a):
            a["classes"]["BIN_5"]["pos_rows"][0][0][2] *= 2
        self.mutation(substitute, "pos_rows")

    def test_missing_duplicate_and_count_preserving_carrier_substitution(self):
        self.mutation(lambda a: a["classes"]["BIN_5"]["carriers"].pop(), "carriers")
        def duplicate(a):
            carriers = a["classes"]["BIN_5"]["carriers"]
            carriers[1] = carriers[0]
        self.mutation(duplicate, "carriers")
        def substitute(a):
            carriers = a["classes"]["BIN_5"]["carriers"]
            carriers[-1] = "(" * 10 + ")" * 10
            carriers.sort()
        self.mutation(substitute, "carriers")

    def test_wrong_value_and_noncanonical_rational(self):
        def endpoint(a): return a["systems"]["BIN_5|D=1"]["endpoints"][0]
        self.mutation(lambda a: endpoint(a).__setitem__("value", "2"), "endpoint value")
        self.mutation(lambda a: endpoint(a).__setitem__("value", "2/2"), "canonical rational")

    def test_corrupt_primal_negative_multiplier_and_dual(self):
        def endpoint(a): return a["systems"]["BIN_5|D=1"]["endpoints"][0]
        self.mutation(lambda a: endpoint(a)["primal"].__setitem__(0, "2"),
                      "primal equality")
        self.mutation(lambda a: endpoint(a)["ineq_multipliers"].__setitem__(0, "-1"),
                      "negative inequality multiplier")
        def wrong_dual(a):
            e = endpoint(a)
            e["eq_multipliers"][0] = str(Fraction(e["eq_multipliers"][0]) + 1)
        self.mutation(wrong_dual, "dual identity")

    def test_unknown_field_is_not_silently_accepted(self):
        self.mutation(lambda a: a.__setitem__("pretend_complete", True), "top-level fields")

    def test_checker_diagnostic_must_remain_attainment_only(self):
        checker = copy.deepcopy(self.checker)
        checker["diagnostic"]["kind"] = "independent_bound_proof"
        report = self.validate(self.producer, checker)
        self.assertEqual(report["status"], "RED")
        self.assertTrue(any("attainment_only" in error for error in report["errors"]))

    def test_original_summary_byte_hash_substitution_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-the-original.json"
            path.write_bytes(b"{}\n")
            for role in ("producer", "checker"):
                with self.assertRaisesRegex(V.ArchiveError, "original summary SHA256"):
                    V.load_original_summary(path, role)

    @unittest.skipUnless(os.environ.get("D24_EXPORTER_EXECUTION_AUTHORIZED") == "yes",
                         "Exporter subprocess checks require explicit execution authorization")
    def test_exporters_refuse_overwriting_either_output(self):
        for role in ("producer", "checker"):
            exporter = Path(V.__file__).with_name(role + "_export.py")
            for occupied in ("summary", "archive"):
                with self.subTest(role=role, occupied=occupied), tempfile.TemporaryDirectory() as d:
                    summary, archive = Path(d) / "summary.json", Path(d) / "archive.json"
                    existing = summary if occupied == "summary" else archive
                    existing.write_bytes(b"must preserve existing evidence\n")
                    completed = subprocess.run([sys.executable, str(exporter), str(summary), str(archive)],
                                               capture_output=True, timeout=15, check=False)
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertEqual(existing.read_bytes(), b"must preserve existing evidence\n")
                    missing = archive if occupied == "summary" else summary
                    self.assertFalse(missing.exists())

    @unittest.skipUnless(os.environ.get("D24_EXPORTER_EXECUTION_AUTHORIZED") == "yes",
                         "Exporter module imports require explicit execution authorization")
    def test_exporter_helpers_are_deterministic_and_refuse_existing_paths(self):
        for role in ("producer", "checker"):
            source = Path(V.__file__).with_name(role + "_export.py")
            spec = importlib.util.spec_from_file_location("d24_future_" + role, source)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            payload = {"z": "é", "a": ["1/2", 1]}
            self.assertEqual(module._archive_json_bytes(payload), V.canonical_bytes(payload))
            with tempfile.TemporaryDirectory() as directory:
                summary, archive = Path(directory) / "summary.json", Path(directory) / "archive.json"
                summary.write_bytes(b"preserve\n")
                with self.assertRaises((FileExistsError, ValueError, RuntimeError)):
                    module._require_new_paths(str(summary), str(archive))
                self.assertEqual(summary.read_bytes(), b"preserve\n")
                self.assertFalse(archive.exists())


if __name__ == "__main__":
    unittest.main()
