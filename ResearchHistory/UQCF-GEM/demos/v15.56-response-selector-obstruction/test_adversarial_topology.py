"""v15.56 Task 25 RED: adversarial topology-response discrimination."""
import unittest
import adversarial_topology as at
class AdversarialTopologyTests(unittest.TestCase):
 def test_degree_matched(self):
  r=at.run(); self.assertGreaterEqual(r["degree_matched_pair_count"],1)
 def test_isospectral_search(self):
  r=at.run(); self.assertGreaterEqual(r["cospectral_pair_count"],1)
 def test_degree_matched_signal(self):
  self.assertGreater(at.run()["min_degree_matched_response_separation"],1e-3)
 def test_cospectral_signal(self):
  self.assertGreater(at.run()["min_cospectral_response_separation"],1e-3)
 def test_relabel_null(self):
  self.assertLess(at.run()["max_isomorphic_relabel_separation"],1e-10)
if __name__=="__main__": unittest.main()
