import pathlib,importlib.util,unittest
import sympy as s
class Tests(unittest.TestCase):
 def gate(self):
  p=pathlib.Path(__file__).with_name('gate.py');self.assertTrue(p.exists(),'expected RED: network audit absent');q=importlib.util.spec_from_file_location('g1614',p);g=importlib.util.module_from_spec(q);q.loader.exec_module(g);return g
 def fixture(self):
  return [s.Matrix(3,3,lambda i,j:1+e+2*i-3*j+(i==j)) for e in range(6)]
 def test_all_cycles_and_reversal(self):
  g=self.gate();c=self.fixture();self.assertEqual(len(g.CYCLES),7);self.assertEqual(sorted(map(len,g.CYCLES)),[3]*4+[4]*3)
  for cy in g.CYCLES:self.assertEqual(g.cycle_trace(c,cy),g.cycle_trace(c,tuple(reversed(cy))))
 def test_product_rule_and_gradient(self):
  g=self.gate();c=self.fixture();v=[s.eye(3)*(e+1) for e in range(6)];t=s.Symbol('t')
  for cy in g.CYCLES:
   self.assertEqual(g.cycle_derivative(c,v,cy),s.expand(g.cycle_trace([a+t*b for a,b in zip(c,v)],cy)).coeff(t,1))
   only=[s.zeros(3) for _ in range(6)];only[5]=v[5];self.assertEqual(g.inner(g.gradient(c,cy),v[5]),g.cycle_derivative(c,only,cy))
 def test_moving_frame_invariance(self):
  g=self.gate();c=self.fixture();v=[s.eye(3) for _ in c];ks=[s.Matrix([[0,-i-1,2],[i+1,0,-3],[-2,3,0]]) for i in range(4)];gs=[s.eye(3),s.diag(-1,-1,1),s.diag(1,-1,-1),s.diag(-1,1,-1)]
  cc=[gs[i]*m*gs[j].T for m,(i,j) in zip(c,g.EDGES)];vv=[gs[i]*(m+ks[i]*b-b*ks[j])*gs[j].T for m,b,(i,j) in zip(v,c,g.EDGES)]
  for cy in g.CYCLES:self.assertEqual(g.cycle_derivative(c,v,cy),g.cycle_derivative(cc,vv,cy))
 def test_normal_reference_and_zero_coherence(self):
  g=self.gate();c=[s.eye(3) for _ in range(6)];c[5]=s.diag(1,0,0);n=s.diag(0,2,3);p=s.diag(1,0,0);h=(s.eye(3)-p)*g.gradient(c,(0,2,3))*(s.eye(3)-p)
  self.assertEqual(g.inner(h,n),5);self.assertEqual(g.inner(h,s.zeros(3)),0);self.assertEqual(g.inner(h,-n),-5)
 def test_exact_cancellation(self):
  g=self.gate();c=[s.eye(3) for _ in range(6)];v=[s.zeros(3) for _ in c];v[0]=s.eye(3);v[1]=-s.eye(3);self.assertEqual(g.cycle_derivative(c,v,(0,1,2)),0)
 def test_projected_reference_bound(self):
  g=self.gate();mp=g.mp;p=mp.diag([1,0,0]);ref=mp.diag([100,2,0]);n=mp.diag([0,3,0]);self.assertEqual(g.normal_bound(ref,p,p,n),6)
