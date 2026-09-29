import importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'dependency_gates.py';self.assertTrue(p.exists(),'16.17-16.18 dependency implementation absent: expected RED');s=importlib.util.spec_from_file_location('d',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_zero_quotient_stops_structure(self):
  m=self.module();self.assertEqual(m.adjudicate_1617(0),'FORCED_STRUCTURE_NOT_IDENTIFIED')
 def test_blocked_structure_stops_curvature(self):
  m=self.module();self.assertEqual(m.adjudicate_1618('FORCED_STRUCTURE_NOT_IDENTIFIED'),'DEPENDENCY_BLOCKED_NO_NATIVE_STRUCTURE')
if __name__=='__main__':unittest.main()
