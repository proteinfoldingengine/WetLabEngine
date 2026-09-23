from __future__ import annotations
import unittest
from dataclasses import replace
from fractions import Fraction
from factorization import compact_operator, verify_factorization
from evidence import actual_carriers, reference_operator


class FactorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carrier = actual_carriers()[0]

    def test_actual_l5_matches_every_frozen_coefficient(self):
        compact = compact_operator(self.carrier)
        frozen = reference_operator(self.carrier)
        self.assertEqual(compact.labels, frozen.labels)
        self.assertEqual(compact.cycles, frozen.cycles)
        self.assertEqual(compact.entries, frozen.entries)

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
