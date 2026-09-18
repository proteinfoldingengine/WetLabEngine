import unittest
import countermodels as cm


class CountermodelTests(unittest.TestCase):
    def test_same_reduct_allows_collapsed_and_distinguishing_expansions(self):
        collapsed, distinguishing = cm.fiber_countermodels()
        self.assertTrue(cm.same_frozen_reduct(collapsed, distinguishing))
        self.assertTrue(cm.relation_disagrees(collapsed, distinguishing))

    def test_countermodels_keep_same_q_and_source_role(self):
        collapsed, distinguishing = cm.fiber_countermodels()
        self.assertEqual(collapsed.reduct.q, distinguishing.reduct.q)
        self.assertEqual(collapsed.reduct.source_role,
                         distinguishing.reduct.source_role)
        self.assertEqual(collapsed.reduct.genesis_status,
                         distinguishing.reduct.genesis_status)


if __name__ == '__main__':
    unittest.main()
