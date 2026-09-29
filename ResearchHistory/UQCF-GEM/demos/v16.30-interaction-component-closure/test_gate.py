import unittest,importlib
class Tests(unittest.TestCase):
 def mods(self):
  return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_max_only_cross_parent_has_no_local_edge(self):
  p,v=self.mods();c=p.control_max_only();v.verify_case(c);self.assertNotEqual(c['global_mixed'],0);self.assertTrue(all(x==0 for x in c['local_mixed']))
 def test_masked_has_local_edge_with_zero_global(self):
  p,v=self.mods();c=p.control_masked();v.verify_case(c);self.assertEqual(c['global_mixed'],0);self.assertTrue(any(x!=0 for x in c['local_mixed']))
 def test_pure_three_way_checker_detected(self):
  _,v=self.mods();self.assertNotEqual(v.mobius_top({0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:1},3),0)
 def test_cross_parent_edge_rejected(self):
  p,v=self.mods();d=p.small_document();d['cases'][0]['edges'].append([[0,2],[0,3]])
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_complete_small(self):
  p,v=self.mods();r=v.verify_document(p.produce(3));self.assertEqual(r['execution_status'],'COMPLETED')
if __name__=='__main__':unittest.main(verbosity=2)
