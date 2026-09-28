import unittest,pathlib,importlib.util
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: stratum audit absent')
  spec=importlib.util.spec_from_file_location('stratum1607',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
 def test_normal_block_forces_rank_gain(self):
  g=self.gate();d=g.stratum(s.diag(1,0,0),s.diag(0,1,1));self.assertEqual((d['rank'],d['normal_rank']),(1,2));self.assertEqual(d['jump_bound_squared'],2);self.assertTrue(d['identities_valid'])
 def test_affine_rank_gain_is_not_forced_rank_gain(self):
  g=self.gate();c=s.diag(1,0,0);v=s.Matrix([[0,1,0],[1,0,0],[0,0,0]]);self.assertEqual((c+v).rank(),2);d=g.stratum(c,v);self.assertEqual(d['normal_rank'],0);self.assertEqual(d['classification'],'TANGENT_COMPATIBLE_NOT_PATH_CERTIFIED')
 def test_tiny_exact_support_preserved(self):
  g=self.gate();d=g.stratum(s.diag(1,s.Rational(1,10**40),0),s.diag(0,1,1));self.assertEqual((d['rank'],d['normal_rank']),(2,1));self.assertEqual(d['normal'],s.diag(0,0,1))
 def test_projectors_and_covariance(self):
  g=self.gate();c=s.Matrix([1,2,3])*s.Matrix([[3,1,2]]);v=s.eye(3);u=s.Matrix([[0,1,0],[0,0,1],[1,0,0]]);w=u.T
  a=g.stratum(c,v);b=g.stratum(u*c*w.T,u*v*w.T);self.assertEqual(b['normal'],u*a['normal']*w.T);self.assertTrue(b['identities_valid']);self.assertEqual(a['left']*c,c)
 def test_identity_and_invalid_precedence(self):
  g=self.gate();d=g.stratum(s.eye(3),s.zeros(3));self.assertEqual(d['normal_rank'],0);self.assertEqual(g.verdict(False,[True]),'INVALID');self.assertEqual(g.verdict(True,[True]*48),'SUPPORT_POLAR_DISCONTINUITY_FORCED');self.assertEqual(g.verdict(True,[False]*48),'NO_FIRST_ORDER_RANK_OBSTRUCTION');self.assertEqual(g.verdict(True,[True,False]),'MIXED_SUPPORT_STABILITY')
