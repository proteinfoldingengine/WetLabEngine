import pathlib,importlib.util,unittest
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: interpretation gate absent');q=importlib.util.spec_from_file_location('g1615',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def test_independent_gradient(self):
  g=self.gate();c=[s.Matrix(3,3,lambda i,j:1+e+2*i-j+(i==j)) for e in range(6)];t=s.Symbol('t');v=s.Matrix([[2,3,1],[4,0,5],[1,2,6]])
  for cy in g.A.CYCLES:
   for e in range(6):
    cc=list(c);cc[e]=cc[e]+t*v;want=s.expand(g.A.cycle_trace(cc,cy)).coeff(t,1);self.assertEqual(g.A.inner(g.reference(c,cy,e),v),want)
 def test_structural_and_directional_blindness(self):
  g=self.gate();z=s.zeros(3);n=s.diag(0,1,0);self.assertEqual(g.classify_references([z]*7,n)['classification'],'STRUCTURAL_NORMAL_BLINDNESS');h=s.diag(0,0,1);self.assertEqual(g.classify_references([h]+[z]*6,n)['classification'],'DIRECTION_SPECIFIC_KERNEL');self.assertEqual(g.classify_references([h]+[z]*6,h)['classification'],'NORMAL_COUPLED')
 def test_local_scalar_derivatives(self):
  g=self.gate();c=s.Matrix([[1,2,0],[0,3,1],[2,0,4]]);v=s.eye(3);t=s.Symbol('t');m=c+t*v
  expected=[s.expand(s.trace((m.T*m)**k)).coeff(t,1) for k in [1,2,3]]+[s.expand(m.det()).coeff(t,1)];self.assertEqual(g.local_derivatives(c,v),expected)
 def test_normal_gram_blindness_and_orientation(self):
  g=self.gate();e=s.Symbol('e',positive=True);c=s.diag(1,e,0);n=s.diag(0,0,2);self.assertEqual(g.local_derivatives(c,n),[0,0,0,2*e]);self.assertEqual(g.local_derivatives(c.subs(e,0),n),[0,0,0,0])
 def test_identity_order_and_zero_direction(self):
  g=self.gate();c=s.eye(3);self.assertEqual(g.local_derivatives(c,s.zeros(3)),[0]*4)
