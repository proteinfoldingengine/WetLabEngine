import unittest,pathlib,importlib.util
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: physical paths audit absent');spec=importlib.util.spec_from_file_location('paths1608',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
 def test_exact_density_certificate(self):
  g=self.gate();r=s.eye(4)*s.Rational(1,3);c=g.density_certificate(r);self.assertEqual(c['trace'],s.Rational(4,3));self.assertTrue(c['valid']);self.assertEqual(c['normalized_trace'],1)
  with self.assertRaises(ValueError):g.density_certificate(s.diag(1,1,-1,1))
  with self.assertRaises(ValueError):g.density_certificate(s.Matrix([[1,1],[0,1]]))
 def test_canonical_complex_ldl_regression(self):
  import json
  g=self.gate();h=json.loads(pathlib.Path(__file__).with_name('complex-density-regression.json').read_text());rho=s.Matrix([[s.Rational(x)+s.I*s.Rational(y) for x,y in row] for row in h])
  bound=min(s.re(rho[i,i])-sum(abs(s.re(rho[i,j]))+abs(s.im(rho[i,j])) for j in range(4) if j!=i) for i in range(4))
  self.assertGreater(bound,0)
  self.assertTrue(g.density_certificate(rho)['valid'])
 def test_connected_path_quadratic(self):
  g=self.gate();z={(0,0,0,0):s.Rational(1,4)};x={(0,0,1,0):s.Rational(1,8),(0,0,0,2):s.Rational(1,12)};c,v,w,poly=g.connected_path(z,x);self.assertEqual(c,s.zeros(3));self.assertEqual(v,s.zeros(3));self.assertEqual(w[0,1],-s.Rational(1,6));self.assertEqual(poly[0,1],-g.PARAM**2/6)
 def test_normalization_is_not_connected_rescaling(self):
  g=self.gate();d={(0,0,0,0):s.Rational(1,2),(0,0,1,0):s.Rational(1,8),(0,0,0,2):s.Rational(1,12)};raw=g.D.connected(d);normalized=g.D.connected({w:c/2 for w,c in d.items()});self.assertEqual(normalized,raw/4);self.assertNotEqual(normalized,raw/2)
 def test_identity_order_equality_not_zero(self):
  g=self.gate();d={(0,0,0,0):s.Rational(1,4),(0,0,3,0):s.Rational(1,20)};z,paths=g.path_directions(d,s.Integer(1),'plane');self.assertEqual(paths['after'],paths['before']);self.assertTrue(paths['after']);self.assertTrue(g.channel_certificate()['valid'])
 def test_verdict_invalid_precedence(self):
  g=self.gate();self.assertEqual(g.verdict(False,[True]),'INVALID');self.assertEqual(g.verdict(True,[True]*96),'PHYSICAL_PATH_SUPPORT_DISCONTINUITY_FORCED');self.assertEqual(g.verdict(True,[False]*96),'NO_FIRST_ORDER_PHYSICAL_PATH_OBSTRUCTION');self.assertEqual(g.verdict(True,[True,False]),'MIXED_PHYSICAL_PATH_STABILITY')
