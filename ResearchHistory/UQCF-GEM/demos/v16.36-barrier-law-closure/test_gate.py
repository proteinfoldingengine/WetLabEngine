import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_missing_gate_rejected(self):
  p,v=self.m();d=p.produce(3);d.pop('gate_c')
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_barrier_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'][0]['B1']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_false_signature_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['pairs']:d['pairs'][0]['candidate_signature']['q']=[]
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.m();self.assertEqual(v.verify_document(p.produce(3))['execution_status'],'COMPLETED')
if __name__=='__main__':unittest.main(verbosity=2)
