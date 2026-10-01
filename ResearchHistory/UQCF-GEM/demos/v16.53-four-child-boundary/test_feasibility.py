import importlib.util
import unittest
from itertools import product
import verifier as v

class Feasibility(unittest.TestCase):
    def test_all_frozen_feasibility_rows(self):
        self.assertIsNotNone(importlib.util.find_spec('feasibility'),'FEASIBILITY_IMPLEMENTATION_MISSING')
        import feasibility as f
        for widths in product((1,2),repeat=4):
            for q in range(1,5):
                for k in range(1,5):
                    with self.subTest(widths=widths,q=q,k=k):
                        self.assertEqual(f.at_width(widths,q,k),v.canonical_roots(widths,q,k))
    def test_disjoint_minimum_beyond_frozen_palette(self):
        self.assertIsNotNone(importlib.util.find_spec('feasibility'),'FEASIBILITY_IMPLEMENTATION_MISSING')
        import feasibility as f
        for widths in product((1,2),repeat=4):
            m,roots=f.minimum(widths,4)
            self.assertEqual(m,sum(widths))
            self.assertEqual([len(A) for A in roots],list(widths))
            self.assertEqual(v.hitting([set(A) for A in roots]),4)

if __name__=='__main__':unittest.main(verbosity=2)
