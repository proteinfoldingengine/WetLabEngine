from __future__ import annotations
import unittest
from dataclasses import replace
from fractions import Fraction
from factorization import compact_operator, verify_factorization
from evidence import actual_carriers, reference_operator, verify_evidence


class FactorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carriers = actual_carriers()
        cls.carrier = cls.carriers[0]

    def test_evidence_pins_are_exact(self):
        receipt = verify_evidence()
        self.assertEqual(receipt["input_blob"], "f6435267950cde0985889056a67d5427f60f637f")
        self.assertEqual(receipt["derive_blob"], "ce72e488e17fba63a37cff46d07c64e42ffa14df")

    def test_actual_l5_matches_every_frozen_coefficient(self):
        compact = compact_operator(self.carrier)
        frozen = reference_operator(self.carrier)
        self.assertEqual(compact.labels, frozen.labels)
        self.assertEqual(compact.cycles, frozen.cycles)
        self.assertEqual(compact.entries, frozen.entries)

    def test_all_four_actual_carriers_match_every_frozen_coefficient(self):
        for carrier in self.carriers:
            with self.subTest(L=carrier.L, scale=carrier.scale):
                self.assertEqual(compact_operator(carrier), reference_operator(carrier))

    def test_verify_rejects_damaged_coefficient(self):
        compact = compact_operator(self.carrier)
        rows = [list(row) for row in compact.entries]
        rows[0][0] += Fraction(1)
        damaged = replace(compact, entries=tuple(tuple(row) for row in rows))
        with self.assertRaisesRegex(ValueError, "factorization_mismatch"):
            verify_factorization(self.carrier, candidate=damaged)

    def test_constants_map_to_zero(self):
        compact = compact_operator(self.carrier)
        for row in compact.entries:
            self.assertEqual(sum(row, Fraction(0)), 0)


if __name__ == "__main__":
    unittest.main()
