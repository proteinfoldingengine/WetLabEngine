"""Self-review regressions: distinct exact data types must not collapse."""
from copy import deepcopy
from pathlib import Path
import unittest
import obstruction_contract as oc
import source_automorphisms as sa
import obstruction_witness as ow
import verify_obstruction as vo


class ExactTypeTests(unittest.TestCase):
    def test_mapping_and_sequence_are_distinct_observations(self):
        self.assertTrue(vo.finite_factorization(({"x": 1}, (("x", 1),)), ("A", "B"))["factorable"])

    def test_boolean_contract_flag_cannot_be_replaced_by_integer(self):
        c = deepcopy(oc.load_contract(Path(__file__).resolve().parents[4]))
        f = sa.frozen_fixture(c)
        a = sa.enumerate_automorphisms(c, f)
        w = ow.find_witness(c, f, a)
        c["prohibited_inputs"]["gravity"] = 1
        self.assertIn("FROZEN_CONTRACT_CHANGED", vo.verify_obstruction(c, f, a, w)["reasons"])


if __name__ == "__main__":
    unittest.main()
