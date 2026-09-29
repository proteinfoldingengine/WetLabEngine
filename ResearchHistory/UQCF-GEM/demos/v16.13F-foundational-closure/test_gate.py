import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py';self.assertTrue(p.exists(),'16.13F closure gate absent: expected RED');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_inventory(self):
  m=self.module();r=m.audit();self.assertTrue(r['all_valid']);self.assertEqual(r['version'],'16.13F');self.assertNotIn('geometry',r['inputs_used'])
 def test_no_unearned_response_map(self):
  m=self.module();r=m.audit();self.assertFalse(r['uses_response_coarse_map_A'])
if __name__=='__main__':unittest.main()
