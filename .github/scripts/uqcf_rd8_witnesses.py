"""Exact checks of the three disclosed calibration fixtures, not a universal search."""
import unittest
import sympy as S

def ket(d,i):return S.eye(d)[:,i]
def projector(x):return x*x.H
f=[0,1,1,3] # o,p,u,v -> o,p,p,v
plus=[S.Rational(x,5) for x in (1,1,2,1)];minus=[S.Rational(x,5) for x in (1,1,1,2)]
def iso(es):return S.Matrix.hstack(*[S.kronecker_product(ket(4,f[j]),es[j]) for j in range(4)])
def reduced_R(e,de,dr):
 a=S.Matrix(de,dr,list(e));return a.T*a.conjugate()
def full_complement(es,z):return sum((z[j]*projector(es[j]) for j in range(4)),S.zeros(es[0].rows))
def zeros(es):return all((es[j].H*es[k])[0]==0 for j in [1,2] for k in [0,3])
class Witnesses(unittest.TestCase):
 def test_counterexample_and_rejected_two_zero_sufficiency(self):
  es=[ket(2,1),ket(2,0),ket(2,1),ket(2,1)];w=iso(es)
  self.assertEqual(w.H*w,S.eye(4))
  self.assertEqual((es[1].H*es[0])[0],0);self.assertEqual((es[1].H*es[3])[0],0)
  self.assertEqual(projector(es[2]),projector(es[3]));self.assertFalse(zeros(es))
  self.assertEqual(full_complement(es,plus),full_complement(es,minus))
  self.assertEqual(full_complement(es,plus),S.diag(S.Rational(1,5),S.Rational(4,5)))
  self.assertEqual((plus[1]+plus[2])-(minus[1]+minus[2]),S.Rational(1,5))
 def test_fixed_factor_informative_blind_pair(self):
  indices=[0,1,2,0]
  informative=[S.kronecker_product(ket(3,0),ket(3,j)) for j in indices]
  blind=[S.kronecker_product(ket(3,j),ket(3,0)) for j in indices]
  for es in [informative,blind]:self.assertEqual(iso(es).H*iso(es),S.eye(4));self.assertTrue(zeros(es))
  # Every source matrix unit has the same coefficient and output matrix.
  for j in range(4):
   for k in range(4):self.assertEqual((informative[k].H*informative[j])[0],(blind[k].H*blind[j])[0])
  m=S.diag(0,1,1)
  for j in range(4):
   self.assertEqual(S.trace(m*reduced_R(informative[j],3,3)),int(j in [1,2]))
   self.assertEqual(reduced_R(blind[j],3,3),projector(ket(3,0)))
  delta=sum(((plus[j]-minus[j])*reduced_R(informative[j],3,3) for j in range(4)),S.zeros(3))
  self.assertEqual(S.trace(m*delta),S.Rational(1,5))
 def test_mixed_support_effect_and_global_not_local_control(self):
  # Check the general positivity argument on a rank-deficient mixed calibration;
  # this is an exact illustrative check, not verification over all density matrices.
  m=S.diag(1,1,0,0);a=S.diag(S.Rational(1,3),S.Rational(2,3),0,0);b=S.diag(0,0,S.Rational(1,4),S.Rational(3,4))
  self.assertEqual(S.trace(m*a),1);self.assertEqual(S.trace(m*b),0);self.assertEqual(a*b,S.zeros(4))
  bellplus=(S.kronecker_product(ket(2,0),ket(2,0))+S.kronecker_product(ket(2,1),ket(2,1)))/S.sqrt(2)
  bellminus=(S.kronecker_product(ket(2,0),ket(2,0))-S.kronecker_product(ket(2,1),ket(2,1)))/S.sqrt(2)
  self.assertEqual((bellplus.H*bellminus)[0],0)
  self.assertEqual(reduced_R(bellplus,2,2),reduced_R(bellminus,2,2))
if __name__=='__main__':unittest.main(verbosity=2)
