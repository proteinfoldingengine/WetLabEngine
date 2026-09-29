import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py';self.assertTrue(p.exists(),'16.14F gate absent: expected RED');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_quotient_dimension(self):
  m=self.module();self.assertEqual(m.graded_dimensions([8,6,3,2]),[2,3,1])
 def test_no_splitting(self):
  m=self.module();r=m.audit();self.assertTrue(r['associated_graded_canonical']);self.assertFalse(r['canonical_intergrade_transport']);self.assertFalse(r['uses_splitting'])
if __name__=='__main__':unittest.main()
