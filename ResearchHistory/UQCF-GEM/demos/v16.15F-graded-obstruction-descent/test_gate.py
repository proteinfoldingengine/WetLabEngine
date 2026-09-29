import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py';self.assertTrue(p.exists(),'16.15F gate absent: expected RED');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_kernel_basis(self):
  m=self.module();A=[[1,1,0],[0,0,1]];b=m.nullspace(A);self.assertEqual(len(b),1)
 def test_audit(self):
  m=self.module();r=m.audit();self.assertTrue(r['all_valid']);self.assertEqual(r['version'],'16.15F')
if __name__=='__main__':unittest.main()
