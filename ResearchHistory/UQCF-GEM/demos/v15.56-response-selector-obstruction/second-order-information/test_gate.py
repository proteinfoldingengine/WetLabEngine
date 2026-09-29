import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py';self.assertTrue(p.exists(),'16.20 gate implementation absent: expected RED');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_second_coeff(self):
  m=self.module();import sympy as sp
  C=sp.diag(1,0,0);V=sp.diag(0,1,0);W=sp.zeros(3)
  self.assertEqual(m.scalar_coeffs(C,V,W)[0],[1,0,1])
 def test_audit(self):
  m=self.module();r=m.audit();self.assertTrue(r['all_valid']);self.assertEqual(r['version'],'16.20');self.assertEqual(r['metrics']['groups'],72)
if __name__=='__main__':unittest.main()
