import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_positive_witness(self):
  p,v=self.m();d=p.produce(3);v.verify_document(d);self.assertGreaterEqual(d['positive_barriers'],0)
 def test_false_zero_rejected(self):
  p,v=self.m();d=p.produce(3)
  if d['barriers']:
   d['barriers'][0]['B1']=0
   with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.m();self.assertEqual(v.verify_document(p.produce(3))['execution_status'],'COMPLETED')
if __name__=='__main__':unittest.main(verbosity=2)
