import unittest,pathlib,importlib.util
import sympy as s
import mpmath as mp
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: boundary audit absent');q=importlib.util.spec_from_file_location('b1609',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_rank_saturation_and_slower_mode(self):
  g=self.gate();c=s.diag(1,0,0);v=s.diag(0,1,0);self.assertTrue(g.rank_certificate(c,v,s.zeros(3),1,1)['certified']);self.assertFalse(g.rank_certificate(c,v,s.diag(0,0,1),1,1)['certified'])
 def test_boundary_polar_support(self):
  g=self.gate()
  with mp.workdps(80):
   u=g.polar(mp.diag([2,0,0]),1)+g.polar(mp.diag([0,3,0]),1);self.assertLess(mp.norm(u-mp.diag([1,1,0])),mp.mpf('1e-60'))
 def test_tiny_support_and_orientation_preserved(self):
  g=self.gate()
  with mp.workdps(80):
   self.assertLess(mp.norm(g.polar(mp.diag([1,mp.mpf('1e-40'),0]),2)-mp.diag([1,1,0])),mp.mpf('1e-60'));self.assertLess(mp.det(g.polar(mp.diag([-1,1,1]),3)),0)
 def test_positive_scale_only(self):
  g=self.gate();n=s.diag(0,1,0);self.assertTrue(g.positive_scale(n,n/3,s.Rational(1,3)));self.assertFalse(g.positive_scale(n,-n,s.Integer(-1)))
 def test_uncertified_order_classification(self):
  g=self.gate();self.assertTrue(hasattr(g,'pair_classification'),'fallback classifier absent')
  self.assertEqual(g.pair_classification(False,['1']*4),'ORDER_LIMIT_DIFFERENCE_OBSERVED')
  self.assertEqual(g.pair_classification(False,['0']*4),'NUMERICAL_AGREEMENT_ONLY')
  self.assertEqual(g.pair_classification(False,['0','1','0','1']),'UNRESOLVED')
