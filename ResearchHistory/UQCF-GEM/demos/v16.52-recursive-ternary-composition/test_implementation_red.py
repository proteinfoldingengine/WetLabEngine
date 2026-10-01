"""Nested and mixed interface behavior, frozen before producer creation."""
import importlib.util
import unittest
import verifier as v

class RecursiveBehavior(unittest.TestCase):
 def check(self, tree, q, k):
  self.assertIsNotNone(importlib.util.find_spec('producer'), 'RECURSIVE_PRODUCER_MISSING')
  import producer as p
  start=p.initial(tree,k,q,'reversal','inflated')
  path=p.normalize(start,tree,k,q)
  _,independent_start,end=v.model(tree,q,k,'reversal','inflated')
  self.assertEqual(start,independent_start)
  self.assertLessEqual(v.path_check(tree,k,q,path,start,end)[0],1)
  self.assertGreater(len(path),1)
 def test_nested_ternary(self):self.check(v.SHAPES['A'],[2,3],3)
 def test_binary_parent_ternary_child(self):self.check(v.SHAPES['J'],[2,2,2,2,2,2],4)

if __name__=='__main__':unittest.main(verbosity=2)
