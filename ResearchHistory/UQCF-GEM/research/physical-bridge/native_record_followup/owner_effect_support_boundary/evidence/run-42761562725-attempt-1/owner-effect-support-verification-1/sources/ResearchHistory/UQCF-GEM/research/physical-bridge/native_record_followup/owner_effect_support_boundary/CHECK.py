#!/usr/bin/env python3
"""POSTHOC fixed-example arithmetic for the owner-effect support note.
Not a preregistered campaign, exhaustive scientific enumeration, independent
verification, or native physical mechanism. Requires sympy.
"""
import sympy as s

I4 = s.eye(4)
b = [I4[:, j] for j in range(4)]  # o,p,u,v; also 00,01,10,11 in K
pi = [x*x.T for x in b]
Q = I4-pi[2]
xp = s.diag(*[s.Rational(n, 5) for n in (1,1,2,1)])
xm = s.diag(*[s.Rational(n, 5) for n in (1,1,1,2)])
drho = xp-xm
blank = pi[0]
Arank = s.diag(1,1,1,0)
Afull = s.diag(1,s.Rational(1,2),s.Rational(1,3),s.Rational(1,4))
Amissing = pi[3]

def realization(e0, eu):
    return s.Matrix.hstack(*[
        s.kronecker_product(b[1] if j == 2 else b[j], eu if j == 2 else e0)
        for j in range(4)
    ])

def trace_k(m):
    return s.Matrix(4,4,lambda i,j:sum(m[4*i+k,4*j+k] for k in range(4)))

cases = [
    ("W_R", b[0], b[1], s.Rational(1,5), s.Rational(1,10)),
    ("W_E", b[0], b[2], s.Rational(1,5), s.Rational(1,15)),
    ("Bell_Phi", (b[0]+b[3])/s.sqrt(2), (b[0]-b[3])/s.sqrt(2),
     s.Rational(1,10), s.Rational(1,8)),
    ("W_star", b[0], b[3], s.Integer(0), s.Rational(1,20)),
]
for name,e0,eu,rank_expected,full_expected in cases:
    W = realization(e0,eu)
    assert s.simplify(W.T*W-I4) == s.zeros(4)
    for i in range(4):
        for j in range(4):
            E = b[i]*b[j].T
            assert s.simplify(trace_k(W*E*W.T)-(Q*E*Q+E[2,2]*pi[1])) == s.zeros(4)
    delta = s.simplify(W*drho*W.T)
    values = []
    for A,expected in ((Arank,rank_expected),(Afull,full_expected)):
        F = s.kronecker_product(pi[1],A)
        assert s.trace(F*s.kronecker_product(drho,blank)) == 0
        observed = s.simplify(s.trace(F*delta))
        assert observed == expected
        values.append(observed)
    Favg = s.kronecker_product(pi[1],(Arank+Amissing)/2)
    assert s.simplify(s.trace(Favg*delta)) == s.Rational(1,10)
    print(name, "source_channel=16/16", "initial_contrast=0",
          "rank_deficient="+str(values[0]), "full_support="+str(values[1]),
          "complete_menu=1/10")

assert min(Afull.eigenvals()) == s.Rational(1,4)
assert Arank.rank() == 3 and Arank*b[3] == s.zeros(4,1)
assert Arank+Amissing == I4
# Reject the false sufficiency claim "nonzero supported effect is enough".
assert Arank != s.zeros(4)
Wstar = realization(b[0],b[3])
blind = s.trace(s.kronecker_product(pi[1],Arank)*Wstar*drho*Wstar.T)
assert blind == 0
print("REJECTED: nonzero owner-supported effect implies universal separation")
print("PASS: fixed exact checks; no universal theorem inferred from enumeration")

