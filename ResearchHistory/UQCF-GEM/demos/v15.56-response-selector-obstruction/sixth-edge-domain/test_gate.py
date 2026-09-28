import unittest,pathlib,importlib.util
import sympy as s
import mpmath as mp
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: sixth-edge audit absent')
  spec=importlib.util.spec_from_file_location('domain1606',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
 def test_connected_product_subtraction(self):
  g=self.gate();d={(0,0,1,0):s.Rational(1,8),(0,0,0,2):s.Rational(1,12)}
  c=g.connected(d);self.assertEqual(c[0,1],-s.Rational(1,6));self.assertEqual(c.rank(),1)
 def test_tiny_exact_rank_not_rounded(self):
  g=self.gate();c=s.diag(1,s.Rational(1,10**30),0);self.assertEqual(g.exact_record(c)['rank'],2)
 def test_inherited_domains(self):
  g=self.gate()
  with mp.workdps(50):
   self.assertFalse(g.domain(mp.diag([1,0,0]),mp.eye(3),'plane')['admitted'])
   self.assertTrue(g.domain(mp.diag([1,1,0]),mp.eye(3),'plane')['admitted'])
   self.assertFalse(g.domain(mp.diag([1,1,0]),mp.eye(3),'isotropic')['admitted'])
   self.assertTrue(g.domain(mp.eye(3),mp.eye(3),'isotropic')['admitted'])
   with self.assertRaises(ValueError):g.domain(mp.diag([mp.nan,1,0]),mp.eye(3),'plane')
 def test_invalid_precedence(self):
  g=self.gate();self.assertEqual(g.verdict(False,[False]),'INVALID');self.assertEqual(g.verdict(True,[False]),'SIXTH_EDGE_OUTSIDE_FROZEN_DOMAIN');self.assertEqual(g.verdict(True,[True]),'SIXTH_EDGE_ADMISSIBLE');self.assertEqual(g.verdict(True,[True,False]),'MIXED_DOMAIN')
