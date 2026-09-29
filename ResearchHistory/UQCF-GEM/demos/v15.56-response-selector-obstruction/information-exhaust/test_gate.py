import importlib.util, pathlib, unittest
HERE=pathlib.Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def module(self):
  p=HERE/'gate.py'; self.assertTrue(p.exists(),'16.16 gate implementation absent: expected RED')
  s=importlib.util.spec_from_file_location('g1616',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_exact_rank_classifier(self):
  m=self.module(); self.assertEqual(m.ranks([[0,1]],[[0,2]]),(1,1,1,1,1,False))
  self.assertEqual(m.ranks([[1,0]],[[0,1]]),(1,1,2,1,0,True))
 def test_zero_maps(self):
  m=self.module(); self.assertEqual(m.ranks([[0,0]],[[0,0]]),(0,0,0,2,2,False))
 def test_parent_binding_and_complete_audit(self):
  m=self.module(); r=m.audit(); self.assertTrue(r['all_valid']); self.assertEqual(len(r['pairs']),72)
  self.assertEqual(r['counts']['local_records'],1728); self.assertEqual(r['counts']['loop_records'],504)
if __name__=='__main__':unittest.main()
