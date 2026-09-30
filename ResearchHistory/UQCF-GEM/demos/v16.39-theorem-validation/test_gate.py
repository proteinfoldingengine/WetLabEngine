import unittest,copy
import construct,check
class Construction(unittest.TestCase):
 def test_two_view_swap(self):
  p=[-1,0,0];a=[3,5];b=[5,3];q=[2,0,0]
  proof=construct.build(p,2,q,a,b)
  check.path_states(p,2,q,a,b,proof)
 def test_obstruction_classification(self):
  p=[-1,0,0,1,1];q=[2,2,0,0,0];a=[11,19,5];b=[19,11,5]
  c=construct.classify(p,3,q,a,b)
  self.assertFalse(c['sc']);self.assertFalse(c['endpoint_full'])
  self.assertEqual(c,check.classify(p,3,q,a,b))
 def test_reject_illegal_jump(self):
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],{'states':[[3,5],[5,3]],'zero_prefix':0,'zero_suffix':0})
 def test_reject_wrong_endpoint(self):
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],{'states':[[3,5]],'zero_prefix':0,'zero_suffix':0})
 def test_reject_false_zero_normalization(self):
  proof=construct.build([-1,0,0],2,[2,0,0],[3,5],[5,3])
  proof['zero_prefix']=len(proof['states'])-1
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],proof)
if __name__=='__main__':unittest.main(verbosity=2)
