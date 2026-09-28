import unittest,pathlib,importlib.util
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: coherence-family audit absent');q=importlib.util.spec_from_file_location('f1611',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_convex_channel_domain(self):
  g=self.gate()
  for a,b in [(0,-1),(0,1),(1,-1),(1,1),(s.Rational(1,3),s.Rational(1,2))]:
   w=g.weights(a,b);self.assertEqual(sum(w),1);self.assertTrue(all(x>=0 for x in w))
  with self.assertRaises(ValueError):g.weights(1,2)
 def test_zero_normal_not_enough(self):
  g=self.gate();self.assertFalse(g.zero_certificate(s.diag(1,0,0),s.zeros(3),s.diag(0,1,0))['certified']);self.assertTrue(g.zero_certificate(s.diag(1,0,0),s.diag(1,0,0),s.zeros(3))['certified'])
 def test_continuum_bound(self):
  g=self.gate();m=s.diag(1,0,0);self.assertTrue(g.continuum_bound([m,s.diag(0,1,0)],1,1)['certified']);self.assertFalse(g.continuum_bound([m,s.diag(0,0,1)],1,1)['certified']);self.assertTrue(g.continuum_bound([m],1,2)['certified'])
 def test_affine_source_endpoints(self):
  g=self.gate();d={(0,0,1,0):s.Integer(1)};lam=s.Symbol('lam',real=True);x=g.family_action(d,lam)
  for sign in [-1,1]:self.assertEqual(g.L.V.clean({w:c.subs(lam,sign) for w,c in x.items()}),g.T.action(d,sign))
 def test_verdict_negative_cases(self):
  g=self.gate();self.assertEqual(g.classify(True,False,False,False),'FAMILY_IDENTITIES_NOT_CONFIRMED');self.assertEqual(g.classify(True,True,False,True),'ZERO_COHERENCE_RANK_CHANGE');self.assertEqual(g.classify(True,True,True,False),'CONTINUUM_LIMIT_NOT_CERTIFIED');self.assertEqual(g.classify(False,True,True,True),'INVALID')
 def test_rank_one_determinant_regression(self):
  g=self.gate();self.assertTrue(hasattr(g,'det3'),'division-free determinant absent')
  with g.mp.workdps(80):
   m=g.mp.matrix([[1,2,3],[2,4,6],[3,6,9]])
   self.assertEqual(g.det3(m),0);self.assertEqual(g.det3(g.mp.diag([-1,1,1])),-1)
   self.assertEqual(g.det3(g.mp.matrix([[1,2,3],[0,1,4],[5,6,0]])),1)
   import json
   fixture=json.loads(pathlib.Path(__file__).with_name('DETERMINANT_REGRESSION.json').read_text())
   m=g.mp.matrix([[g.mp.make_mpf(tuple(x)) for x in row] for row in fixture['mpf_tuples']])
   with self.assertRaises(TypeError):g.mp.det(m)
   self.assertLess(abs(g.det3(m)),g.mp.mpf('1e-75'))
