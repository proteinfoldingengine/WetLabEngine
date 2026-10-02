"""Full-universe and verifier-rejection contracts, before implementation."""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from universe import generate_cases
from verifier import reconstruct_cases, verify_universe, verify_protocol


def toy(n):
    return {'identity': ['control', [n], [[0], [1], [2]], []]}


class Task1(unittest.TestCase):
    def test_full_independent_universe(self):
        protocol = json.loads((HERE / 'protocol.json').read_text())
        seen = set()
        def production():
            for case in generate_cases(protocol):
                seen.add(case['identity'][0])
                yield case
        self.assertEqual(verify_universe(reconstruct_cases(protocol), production()), [])
        self.assertEqual(seen, set(protocol['families']))

    def test_missing_rejected(self):
        self.assertTrue(verify_universe(iter([toy(0), toy(1)]), iter([toy(0)])))

    def test_duplicate_rejected(self):
        self.assertTrue(verify_universe(iter([toy(0), toy(1)]), iter([toy(0), toy(1), toy(1)])))

    def test_equal_count_substitution_rejected(self):
        self.assertTrue(verify_universe(iter([toy(0), toy(1)]), iter([toy(0), toy(2)])))

    def test_wrong_input_rejected(self):
        bad = toy(0)
        bad['roots'] = [[0], [0], [0]]
        good = toy(0)
        good['roots'] = [[0], [1], [2]]
        self.assertTrue(verify_universe(iter([good]), iter([bad])))

    def test_false_plan_hash_rejected(self):
        protocol = json.loads((HERE / 'protocol.json').read_text())
        protocol['approved_plan_sha256'] = '0' * 64
        self.assertTrue(verify_protocol(protocol, HERE))

    def test_false_proof_hash_rejected(self):
        protocol = json.loads((HERE / 'protocol.json').read_text())
        protocol['proofs'][next(iter(protocol['proofs']))] = '0' * 64
        self.assertTrue(verify_protocol(protocol, HERE))

    def test_valid_protocol(self):
        protocol = json.loads((HERE / 'protocol.json').read_text())
        self.assertEqual(verify_protocol(protocol, HERE), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
