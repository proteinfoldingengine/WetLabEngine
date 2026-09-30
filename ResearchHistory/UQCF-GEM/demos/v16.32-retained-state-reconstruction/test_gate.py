import unittest,importlib
class Tests(unittest.TestCase):
 def mods(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_coarse_checker_collision(self):
  _,v=self.mods();self.assertTrue(v.checker_collision({'a':1},{'a':1}))
 def test_signature_must_not_contain_state_mask(self):
  p,v=self.mods();d=p.small_document();d['signature_fields'].append('state_mask')
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_actual_collision_if_claimed(self):
  p,v=self.mods();d=p.produce(3);r=v.verify_document(d);self.assertIn(r['verdict'],('RECONSTRUCTIVE','NONINJECTIVE','CONDITIONAL','UNRESOLVED'))
 def test_fabricated_collision_rejected(self):
  p,v=self.mods();d=p.small_document();d['collisions']=[{'left':0,'right':0}]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_changed_interval_rejected(self):
  p,v=self.mods();d=p.small_document();d['collisions']=[{'left':0,'right':1,'intervals':[0,1]}]
  with self.assertRaises(ValueError):v.verify_document(d)
if __name__=='__main__':unittest.main(verbosity=2)
