import pathlib,importlib.util,unittest
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: gauge audit absent');q=importlib.util.spec_from_file_location('g1613',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_rank_one_proper_flip(self):
  g=self.gate();c=s.diag(2,0,0);n=s.diag(0,3,4);r=g.classify_pair(c,n);self.assertEqual(r['classification'],'SO_SIGN_EQUIVALENT');self.assertEqual(r['J'].det(),1);self.assertEqual(r['J']*n,-n)
 def test_rank_two_orientation_witness(self):
  g=self.gate();r=g.classify_pair(s.diag(2,3,0),s.diag(0,0,4));self.assertEqual(r['classification'],'SO_SIGN_DISTINGUISHED');self.assertEqual(r['alpha'],24);self.assertEqual(r['J'].det(),-1)
 def test_zero_not_misclassified(self):
  g=self.gate();self.assertEqual(g.classify_pair(s.diag(2,3,0),s.zeros(3))['classification'],'INCOMPLETE')
 def test_physical_determinant_coefficients(self):
  g=self.gate();c=s.diag(2,0,0);v=s.diag(1,3,4);w=s.diag(5,6,7);t=s.Symbol('t');p=s.expand((c+t*v+t*t*w).det());self.assertEqual(g.first_two(c,v,w),[p.coeff(t,1),p.coeff(t,2)])
 def test_spectral_edge_collapse(self):
  g=self.gate();e=s.Symbol('e',positive=True);c=s.diag(1,e,0);n=s.diag(0,0,1);self.assertEqual(g.cofactor_pair(c,n),e);self.assertEqual(g.cofactor_pair(c.subs(e,0),n),0)
