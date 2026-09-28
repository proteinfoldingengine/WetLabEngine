import unittest,pathlib,importlib.util
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: reversal audit absent');q=importlib.util.spec_from_file_location('r1610',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_source_transfer_and_cptp(self):
  g=self.gate();self.assertTrue(g.source_certificate()['valid'])
 def test_exact_reversal_requires_nonzero(self):
  g=self.gate();n=s.diag(0,2,0);self.assertTrue(g.reversal(n,-n));self.assertFalse(g.reversal(n,n));self.assertFalse(g.reversal(s.zeros(3),s.zeros(3)))
 def test_gap_theorem(self):
  g=self.gate()
  with g.mp.workdps(80):
   c=g.mp.diag([2,0,0]);n=g.mp.diag([0,3,-4]);b=g.B.polar(c,1);u=g.B.polar(n,2);self.assertLess(abs(g.F.norm((b+u)-(b-u))**2-8),g.mp.mpf('1e-60'))
 def test_ordered_paths_share_baseline(self):
  g=self.gate();d={(0,0,0,0):s.Rational(1,4),(0,0,1,0):s.Rational(1,16)};a=s.Rational(1,3)
  for sign in [-1,1]:
   z,p=g.paths(d,a,'plane',sign);self.assertEqual(z,g.L.exact_prepare(g.L.exact_middle(d,a),'plane'));self.assertEqual(set(p),{'after','before'})
