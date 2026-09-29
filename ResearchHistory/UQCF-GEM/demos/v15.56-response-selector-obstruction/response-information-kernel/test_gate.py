import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py';self.assertTrue(p.exists(),'16.19 gate implementation absent: expected RED');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_linear_kernel(self):
  m=self.module();self.assertEqual(m.classify_matrix([[1,0],[0,0]]),(2,1,1,'NONTRIVIAL_RESPONSE_INFORMATION_KERNEL'))
 def test_complete(self):
  m=self.module();self.assertEqual(m.classify_matrix([[1,0],[0,1]]),(2,2,0,'LOCAL_SCALARS_COMPLETE_ON_REALIZED_RESPONSE'))
 def test_parent_audit(self):
  m=self.module();r=m.audit();self.assertTrue(r['all_valid']);self.assertEqual(r['version'],'16.19')
if __name__=='__main__':unittest.main()
