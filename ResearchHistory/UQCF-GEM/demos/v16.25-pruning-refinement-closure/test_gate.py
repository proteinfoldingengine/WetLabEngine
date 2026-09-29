"""v16.25 RED tests frozen before implementation."""
import importlib, unittest
from fractions import Fraction as F
class Tests(unittest.TestCase):
 def modules(self):
  return importlib.import_module('engine'),importlib.import_module('verify')
 def test_monotonic_refinement_and_strict_example(self):
  e,v=self.modules();p=(-1,0,0,0)
  coarse=[(0,1,2),(0,2,3)]
  fine=[(0,1),(0,2),(0,3)]
  d=e.certify_refinement(p,coarse,fine)
  self.assertLessEqual(d['h_before'],d['h_after']);self.assertEqual((d['h_before'],d['h_after']),(2,3));v.verify_case(d)
 def test_identity_refinement(self):
  e,v=self.modules();p=(-1,0,0);ys=[(0,1),(0,2)]
  d=e.certify_refinement(p,ys,ys);self.assertEqual(d['h_before'],d['h_after']);v.verify_case(d)
 def test_direct_equals_staged_pushforward_exactly(self):
  e,_=self.modules();p=(-1,0,1,1);x=(F(1,3),F(1,6),F(1,4),F(1,4))
  self.assertEqual(e.push(p,(0,1),x),e.push_between(p,(0,1,2,3),(0,1),e.push(p,(0,1,2,3),x)))
  z=e.push(p,(0,1,2),x)
  self.assertEqual(e.push(p,(0,1),x),e.push_between(p,(0,1,2),(0,1),z))
 def test_two_factorizations_same_final(self):
  e,_=self.modules();p=(-1,0,1,1,0);x=(1,2,3,4,5)
  direct=e.push(p,(0,1),x)
  a=e.push_between(p,(0,1,2,3,4),(0,1,2),x)
  a=e.push_between(p,(0,1,2),(0,1),a)
  b=e.push_between(p,(0,1,2,3,4),(0,1,3),x)
  b=e.push_between(p,(0,1,3),(0,1),b)
  self.assertEqual(direct,a);self.assertEqual(a,b)
 def test_illegal_nonprefix_refinement_rejected(self):
  e,_=self.modules()
  with self.assertRaises(ValueError):e.certify_refinement((-1,0,1),[(0,1,2)],[(0,2)])
 def test_changed_union_not_comparable(self):
  e,_=self.modules()
  with self.assertRaisesRegex(ValueError,'same union'):e.certify_refinement((-1,0,0),[(0,1,2)],[(0,1)])
 def test_not_componentwise_subview_rejected(self):
  e,_=self.modules()
  with self.assertRaises(ValueError):e.certify_refinement((-1,0,0),[(0,1),(0,2)],[(0,2),(0,1)])
 def test_verifier_rejects_false_lower_after(self):
  e,v=self.modules();d=e.certify_refinement((-1,0,0,0),[(0,1,2),(0,2,3)],[(0,1),(0,2),(0,3)])
  d['h_after']=1
  with self.assertRaises(ValueError):v.verify_case(d)
 def test_verifier_rejects_corrupt_composition(self):
  e,v=self.modules();d=e.certify_refinement((-1,0,1),[(0,1,2)],[(0,1,2)])
  d['composition'][0]['direct'][0]='99'
  with self.assertRaises(ValueError):v.verify_case(d)
 def test_complete_small_universe(self):
  e,v=self.modules();doc=e.produce(4);r=v.verify_document(doc,4)
  self.assertGreater(r['refinements'],0);self.assertGreater(r['strict'],0)
if __name__=='__main__':unittest.main(verbosity=2)
