import importlib,unittest
class Tests(unittest.TestCase):
 def m(self):return importlib.import_module('engine'),importlib.import_module('verify')
 def test_atomic_strict_one(self):
  e,v=self.m();p=(-1,0,0,0);before=[(0,1,2),(0,2,3),(0,1,3)];d=e.atomic(p,before,0,2);self.assertEqual(d['delta_h'],1);self.assertTrue(d['trigger']);v.verify_atomic(d)
 def test_atomic_zero(self):
  e,v=self.m();p=(-1,0,0);before=[(0,1,2),(0,1,2)];d=e.atomic(p,before,0,2);self.assertEqual(d['delta_h'],0);self.assertFalse(d['trigger']);v.verify_atomic(d)
 def test_changed_union_rejected(self):
  e,_=self.m()
  with self.assertRaises(ValueError):e.atomic((-1,0),[(0,1)],0,1)
 def test_nonleaf_rejected(self):
  e,_=self.m()
  with self.assertRaises(ValueError):e.atomic((-1,0,1),[(0,1,2),(0,1,2)],0,1)
 def test_false_jump_rejected(self):
  e,v=self.m();d=e.atomic((-1,0,0,0),[(0,1,2),(0,2,3),(0,1,3)],0,2);d['delta_h']=2
  with self.assertRaises(ValueError):v.verify_atomic(d)
 def test_false_trigger_rejected(self):
  e,v=self.m();d=e.atomic((-1,0,0),[(0,1,2),(0,1,2)],0,2);d['trigger']=True
  with self.assertRaises(ValueError):v.verify_atomic(d)
 def test_factorization_telescopes(self):
  e,v=self.m();p=(-1,0,0,1);before=[(0,1,3),(0,1,2,3),(0,2)];after=[(0,1),(0,1,2,3),(0,2)]
  d=e.factor(p,before,after);self.assertEqual(sum(x['delta_h'] for x in d['steps']),d['h_after']-d['h_before']);v.verify_factor(d)
 def test_complete_small(self):
  e,v=self.m();doc=e.produce(4);r=v.verify_document(doc,4);self.assertGreater(r['atomic'],0)
if __name__=='__main__':unittest.main(verbosity=2)
