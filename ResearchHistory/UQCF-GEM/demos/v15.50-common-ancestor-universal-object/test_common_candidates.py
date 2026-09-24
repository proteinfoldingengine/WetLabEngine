"""v15.50 Task 2 RED: target-blind U candidate family."""
from pathlib import Path
import unittest
import common_contract as cc
import common_candidates as ca

class CommonCandidateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=cc.load_contract(root); cls.cs=ca.enumerate_candidates(cls.c)
 def test_nonempty_deterministic_family(self):
  self.assertGreater(len(self.cs),0)
  self.assertEqual(self.cs,ca.enumerate_candidates(self.c))
 def test_all_candidates_target_blind(self):
  self.assertTrue(all(ca.check_target_blindness(self.c,u)["status"]=="TARGET_BLIND_PASS" for u in self.cs))
 def test_no_pair_object(self):
  bad=dict(self.cs[0]); bad["pair_object"]=True
  self.assertEqual(ca.check_target_blindness(self.c,bad)["status"],"PAIR_OBJECT_REJECTED")
 def test_no_quantum_labels(self):
  bad=dict(self.cs[0]); bad["quantum_labels"]=["q0"]
  self.assertEqual(ca.check_target_blindness(self.c,bad)["status"],"TARGET_LABEL_CONTAMINATION")
 def test_no_dictionary(self):
  bad=dict(self.cs[0]); bad["node_site_dictionary"]=[0,1,2,3]
  self.assertEqual(ca.check_target_blindness(self.c,bad)["status"],"TARGET_LABEL_CONTAMINATION")
 def test_no_target_dimension(self):
  bad=dict(self.cs[0]); bad["hilbert_dimension"]=32
  self.assertEqual(ca.check_target_blindness(self.c,bad)["status"],"TARGET_LABEL_CONTAMINATION")
 def test_no_downstream_fields(self):
  bad=dict(self.cs[0]); bad["curvature"]=1
  self.assertEqual(ca.check_target_blindness(self.c,bad)["status"],"DOWNSTREAM_CONTAMINATION")
if __name__=="__main__": unittest.main()
