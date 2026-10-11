import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import independent
import producer


class EscapeObstructionTests(unittest.TestCase):
    def test_exact_frozen_source_universe(self):
        matchings = producer.perfect_matchings()
        profiles = producer.multiplicity_profiles()
        self.assertEqual(12, len(matchings))
        self.assertEqual(64, len(profiles))
        self.assertEqual(768, len(matchings) * len(profiles))
        self.assertEqual(matchings, independent.perfect_matchings())

    def test_host_is_k6_minus_only_45(self):
        self.assertEqual(14, len(producer.H_EDGES))
        self.assertNotIn((4, 5), producer.H_EDGES)
        for u in range(6):
            for v in range(u + 1, 6):
                self.assertEqual((u, v) != (4, 5), (u, v) in producer.H_EDGES)

    def test_every_source_has_actual_x_escape_and_no_v_escape(self):
        for matching in producer.perfect_matchings():
            for profile in producer.multiplicity_profiles():
                classifications = producer.classify_candidates(matching, profile)
                self.assertTrue(any(r["kind"] == "X" and r["admitted"] for r in classifications))
                self.assertFalse(any(r["kind"] == "V" and r["admitted"] for r in classifications))

    def test_no_matching_independent_set_is_deficient(self):
        for matching in producer.perfect_matchings():
            rows = producer.independent_set_rows(matching)
            self.assertTrue(any(r["independent"] for r in rows))
            self.assertFalse(any(r["independent"] and r["deficient"] for r in rows))

    def test_saturated_bridge_substitution_is_rejected(self):
        matching = producer.perfect_matchings()[0]
        profile = (1, 1, 1, 1, 1, 1)
        witness = producer.saturated_bridge_substitution_control(matching, profile)
        self.assertFalse(witness["accepted"])
        self.assertEqual("floor_violation", witness["reason"])

    def test_route_slices_preserve_exact_invariants_and_no_vacancy(self):
        matching = producer.perfect_matchings()[0]
        profile = (1, 2, 1, 2, 1, 2)
        route = next(producer.iter_admitted_routes(matching, profile))
        self.assertGreater(len(route), 1)
        for state in route:
            self.assertTrue(state["floors_ok"])
            self.assertTrue(state["hitting_ok"])
            self.assertTrue(state["domination_ok"])
            self.assertTrue(state["hidden_ok"])
            self.assertFalse(state["vacancy"])

    def test_complete_stream_agrees_with_independent_checker(self):
        with tempfile.TemporaryDirectory() as td:
            stream = Path(td) / "stream.jsonl"
            certificate = Path(td) / "certificate.json"
            produced = producer.write_campaign(stream, certificate)
            checked = independent.check_campaign(stream)
            self.assertEqual(produced["stream_sha256"], checked["stream_sha256"])
            self.assertEqual(produced["row_counts"], checked["row_counts"])
            self.assertEqual(768, produced["source_count"])

    def test_checker_rejects_truncation_extra_and_canonical_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            stream = Path(td) / "stream.jsonl"
            producer.write_campaign(stream, Path(td) / "certificate.json")
            original = stream.read_bytes()
            lines = original.splitlines(keepends=True)
            cases = {
                "truncated": b"".join(lines[:-1]),
                "extra": original + lines[-1],
                "noncanonical": original.replace(b'\":', b'\" :', 1),
            }
            for name, payload in cases.items():
                candidate = Path(td) / f"{name}.jsonl"
                candidate.write_bytes(payload)
                with self.subTest(name=name), self.assertRaises(independent.Rejection):
                    independent.check_campaign(candidate)

    def test_declared_rejecting_controls_all_fire(self):
        controls = producer.run_rejecting_controls()
        expected = {
            "forbidden_45", "missing_matching_edge", "false_x",
            "missing_third_vertex", "minimum_degree_substitution",
            "false_deficiency", "saturated_bridge_substitution",
            "canonical_corruption",
        }
        self.assertEqual(expected, set(controls))
        self.assertTrue(all(v["rejected"] for v in controls.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
