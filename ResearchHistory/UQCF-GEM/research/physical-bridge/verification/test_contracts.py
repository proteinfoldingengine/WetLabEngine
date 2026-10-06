"""Tests precede implementation; run only in the declared GitHub workflow."""
import hashlib
import math
from pathlib import Path
import re
import unittest

import certificate as cert
import reference as ref

ROOT = Path(__file__).resolve().parents[1]


class Contracts(unittest.TestCase):
    def test_direct_transversal_and_exception_conventions(self):
        self.assertEqual(ref.tau(3, (1, 2, 4)), 3)
        self.assertEqual(ref.tau(0, ()), 0)
        self.assertEqual(ref.tau(1, (1,)), 1)
        self.assertEqual(ref.tau(1, (0,)), math.inf)

    def test_exact_pair_and_cover_fields(self):
        self.assertEqual(cert.fields(3, (1, 2, 4)), {
            'W': {3: 1, 5: 1, 6: 1},
            'C': {h: int(h == 7) for h in range(8)},
        })

    def test_both_primitive_update_identities(self):
        after = {'W': {3: 0, 5: 1, 6: 1},
                 'C': {h: int(h in (3, 7)) for h in range(8)}}
        self.assertEqual(cert.predict(3, (1, 2, 4), ('add', 2, 0)), after)
        before = {'W': {3: 1, 5: 1, 6: 1},
                  'C': {h: int(h == 7) for h in range(8)}}
        self.assertEqual(cert.predict(3, (1, 2, 5), ('del', 2, 0)), before)

    def test_addition_margins_decide_the_original_control(self):
        roots, floors = (1, 2, 5, 8), (1, 1, 1, 1)
        self.assertEqual(cert.margin(4, roots, ('add', 3, 1)), 1)
        self.assertEqual(cert.margin(4, roots, ('add', 3, 2)), 2)
        self.assertIs(cert.legal(4, roots, floors, ('add', 3, 1)), False)
        self.assertIs(cert.legal(4, roots, floors, ('add', 3, 2)), True)

    def test_deletion_surviving_cover_and_floor_are_separate(self):
        roots = (4, 3, 2, 16, 8)
        self.assertIs(cert.legal(5, roots, (1,)*5, ('del', 1, 0)), True)
        self.assertIs(cert.legal(5, roots, (1,)*5, ('del', 1, 1)), False)
        self.assertIs(cert.legal(5, roots, (1, 2, 1, 1, 1), ('del', 1, 0)), False)
        self.assertIs(ref.legal(5, roots, (1,)*5, ('del', 1, 0)), True)

    def test_same_candidate_can_acquire_empty_shadow(self):
        move = ('add', 0, 0)
        self.assertEqual(cert.margin(4, (12, 4, 1, 2), move), 2)
        self.assertEqual(cert.margin(4, (14, 4, 1, 2), move), math.inf)
        self.assertIs(cert.legal(4, (14, 4, 1, 2), (1,)*4, move), True)

    def test_independent_complete_identity_generators(self):
        expected = [((1,), (1,)), ((2,), (1,)), ((3,), (1,)), ((3,), (2,))]
        self.assertEqual(sorted(cert.universe(2, 1)), expected)
        self.assertEqual(sorted(ref.universe(2, 1)), expected)

    def test_coverage_rejects_omission_and_duplicate(self):
        expected = [((1,), (1,)), ((2,), (1,)), ((3,), (1,)), ((3,), (2,))]
        self.assertIs(ref.coverage_ok(expected, expected), True)
        self.assertIs(ref.coverage_ok(expected[:-1], expected), False)
        self.assertIs(ref.coverage_ok(expected + expected[:1], expected), False)

    def test_consolidated_overlap_fixtures_match_original_sources(self):
        original = (ROOT / 'A12_5_OVERLAP_LOCALITY_NOGO.md').read_text()
        consolidated = (ROOT / 'A12_CONSOLIDATED_PROOF_AND_AUDIT.md').read_text()
        for label in ('L', 'I'):
            block = original.split('State ' + label + ':', 1)[1]
            expected = re.findall(r'R[0-5]=\{([^}]+)\}', block)[:6]
            found = re.search(r'    ' + label + r': \(([^\n]+)\)', consolidated)
            self.assertIsNotNone(found, 'Missing consolidated fixture ' + label)
            actual = re.findall(r'\{([^}]+)\}', found.group(1))
            self.assertEqual([frozenset(s.split(',')) for s in actual],
                             [frozenset(s.split(',')) for s in expected],
                             'Consolidation must not substitute A12.5 supports')

    def test_frozen_original_blob_identities(self):
        pairs = {
            'A12_1_SIGNED_ADMISSIBILITY_RESPONSE_SCOPE.md': '64685e2fcad2f77f6a590685368a1ac21896e057',
            'A12_1_SIGNED_ADMISSIBILITY_RESPONSE.md': '54cf74c9d01548368b7e32814f2f06e7fba5d628',
            'A12_2_COLLECTIVE_RESPONSE_SCOPE.md': '48c7698a38a69685643f040b59a6f040be3ac054',
            'A12_2_COLLECTIVE_RESPONSE_HIERARCHY.md': 'bfb364b75e18a279f2e4aa53254370f563a9545c',
            'A12_3_DUAL_CERTIFICATE_FIELDS_SCOPE.md': '0e8ac8ba64fe72e17c207d6532c7c51fd71b300a',
            'A12_3_DUAL_CERTIFICATE_FIELDS.md': 'b9fa20d44002d0d743278f3fd21cce3214d02600',
            'A12_4_CANDIDATE_RESPONSE_MARGINS_SCOPE.md': '7a7593740c65b87473cbe0bb36432064c278a428',
            'A12_4_CANDIDATE_RESPONSE_MARGINS.md': 'a0d38aeacac80f036f9cb997f08f921f4e0f4b59',
            'A12_5_OVERLAP_LOCALITY_NOGO_SCOPE.md': '001804a390c1ed9603e8bc15abac30cd255b981e',
            'A12_5_OVERLAP_LOCALITY_NOGO.md': '0da2ddad7ed177219f3fed50e7e152b2e1ffa679',
            'A12_SELF_CONTAINED_AUDIT_PROTOCOL.md': 'db1e349268f7b864219bf37d1f5917abbc3e1fef',
            'reviews/A12_1_5_EXTERNAL_MATH_REVIEW_01a10f15.json': '10138796a22237e30760bfe96e025ddc215a09da',
        }
        for name, expected in pairs.items():
            data = (ROOT / name).read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            self.assertEqual(actual, expected, name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
