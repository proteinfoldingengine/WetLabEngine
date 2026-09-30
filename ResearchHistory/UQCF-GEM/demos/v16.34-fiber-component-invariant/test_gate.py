import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_minimum_cover_exact_control(self):
  p,v=self.m();c=p.control();v.verify_state(c)
 def test_omitted_minimum_cover_rejected(self):
  p,v=self.m();c=p.control();c['minimum_covers'][0].pop()
  with self.assertRaises(ValueError):v.verify_state(c)
 def test_connectivity_not_trusted(self):
  p,v=self.m();d=p.produce(3);d['component_count']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.m();r=v.verify_document(p.produce(3));self.assertEqual(r['execution_status'],'COMPLETED')
if __name__=='__main__':unittest.main(verbosity=2)
