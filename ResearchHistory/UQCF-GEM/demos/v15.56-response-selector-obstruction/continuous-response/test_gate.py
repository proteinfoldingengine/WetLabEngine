import unittest,pathlib,importlib.util
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: continuous-response audit absent');q=importlib.util.spec_from_file_location('r1612',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_uniform_coefficient_bound(self):
  g=self.gate();self.assertEqual(g.entry_bound([s.diag(-2,3,0),s.diag(1,0,0)]),6)
 def test_gram_normal_blindness_and_sign_loss(self):
  g=self.gate();c=s.diag(2,0,0);n=s.diag(0,3,0);self.assertEqual(g.gram_derivative(c,n),s.zeros(3));self.assertEqual((c+n).T*(c+n),(c-n).T*(c-n));self.assertNotEqual(c+n,c-n)
 def test_normal_energy_coefficients(self):
  g=self.gate();n=s.diag(0,2,0);m=s.diag(0,3,0);t=s.Symbol('t');co=g.energy_coefficients(n,m);self.assertEqual(sum((t**(i+2)*z for i,z in enumerate(co)),s.zeros(3)),((t*n+t*t*m).T*(t*n+t*t*m)).applyfunc(s.expand))
 def test_weighted_polar_tiny_rank_and_orientation(self):
  g=self.gate()
  with g.mp.workdps(80):
   c=g.mp.diag([-2,g.mp.mpf('1e-45'),0]);u,h,w=g.weighted_polar(c,2);self.assertLess(g.mp.norm(w-c),g.mp.mpf('1e-65'));self.assertLess(u[0,0],0);self.assertGreater(h[1,1],0)
 def test_verdict_negative(self):
  g=self.gate();self.assertEqual(g.classify(False,True),'INVALID');self.assertEqual(g.classify(True,False),'CONTINUOUS_RESPONSE_CRITERIA_NOT_CONFIRMED')
