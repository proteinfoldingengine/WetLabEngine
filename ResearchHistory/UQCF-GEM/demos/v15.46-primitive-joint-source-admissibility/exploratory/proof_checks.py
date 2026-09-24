"""Exploratory mathematical checks, not a UQCF engine implementation or CI certificate.

Only stdlib exact rational arithmetic. No external data, geometry, time parameter,
logarithmic regulator, spectrum threshold, or optimization is used.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sys

CHECKS = []

def require(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)

def bits(n):
    return tuple(product((0, 1), repeat=n))

def marginal(p, keep):
    out = {key: Q(0) for key in bits(len(keep))}
    for key, v in p.items():
        out[tuple(key[i] for i in keep)] += v
    return out

def parity(t):
    return {key: (1+t*(-1)**sum(key))/8 for key in bits(3)}

def ratio(p, a, b, c, key):
    # Diagonal-state exp(D_{A:C|B}); all regions are tuples of axis indices.
    def v(region):
        return marginal(p, region)[tuple(key[i] for i in region)]
    return v(a+b+c)*v(b)/(v(a+b)*v(b+c))

def transpose(a):
    return tuple(zip(*a))

def mm(a, b):
    return tuple(tuple(sum((x*y for x,y in zip(row,col)), Q(0))
                       for col in transpose(b)) for row in a)

def plus(a, b):
    return tuple(tuple(x+y for x,y in zip(row,col)) for row,col in zip(a,b))

def scale(t, a):
    return tuple(tuple(t*x for x in row) for row in a)

def eye(n):
    return tuple(tuple(Q(i==j) for j in range(n)) for i in range(n))

def kron(a, b):
    return tuple(tuple(x*y for x in ar for y in br) for ar in a for br in b)

def tensor3(a, b, c):
    return kron(kron(a,b),c)

def ptrace(a, keep):
    n = len(a).bit_length()-1
    states = bits(n)
    kept = bits(len(keep))
    index = {x:i for i,x in enumerate(kept)}
    gone = tuple(i for i in range(n) if i not in keep)
    out = [[Q(0) for _ in kept] for _ in kept]
    for i,s in enumerate(states):
        for j,t in enumerate(states):
            if all(s[k]==t[k] for k in gone):
                out[index[tuple(s[k] for k in keep)]][index[tuple(t[k] for k in keep)]] += a[i][j]
    return tuple(map(tuple,out))

def trace(a):
    return sum((a[i][i] for i in range(len(a))),Q(0))

def run():
    CHECKS.clear()
    params = (Q(0),Q(1,3),Q(1,2),Q(-1,2))
    records = []
    for t in params:
        p = parity(t)
        require(f'parity {t}: positive normalized', min(p.values())>0 and sum(p.values())==1)
        for keep in ((0,), (1,), (2,), (0,1), (0,2), (1,2)):
            m = marginal(p, keep)
            require(f'parity {t}: uniform marginal {keep}', set(m.values())=={Q(1,2**len(keep))})
        rr = tuple(ratio(p,(0,),(1,),(2,),key) for key in bits(3))
        require(f'parity {t}: exact log-ratio eigenvalues', rr==tuple(1+t*(-1)**sum(key) for key in bits(3)))
        records.append({'t':str(t),'minimum_eigenvalue':str(min(p.values())),
                        'exp_defect_eigenvalues':list(map(str, sorted(set(rr))))})
    p0,p1 = parity(Q(0)),parity(Q(1,2))
    require('same pair marginals, different modular defects',
            all(marginal(p0,k)==marginal(p1,k) for k in ((0,1),(0,2),(1,2)))
            and any(ratio(p0,(0,),(1,),(2,),k)!=ratio(p1,(0,),(1,),(2,),k) for k in bits(3)))
    # A correlated, strictly positive classical Markov chain, not just product noise.
    pa = (Q(2,5),Q(3,5))
    pb = ((Q(3,4),Q(1,4)),(Q(1,3),Q(2,3)))
    pc = ((Q(2,7),Q(5,7)),(Q(4,5),Q(1,5)))
    pm = {k:pa[k[0]]*pb[k[0]][k[1]]*pc[k[1]][k[2]] for k in bits(3)}
    require('correlated Markov control normalized',sum(pm.values())==1)
    require('correlated Markov control has exactly zero defect',
            all(ratio(pm,(0,),(1,),(2,),k)==1 for k in bits(3)))
    left = parity(Q(1,3))
    for label,right in (('Markov spectator',pm),('two nonzero defects',parity(Q(1,2)))):
        joint = {s+t:left[s]*right[t] for s in bits(3) for t in bits(3)}
        for k in bits(6):
            require(f'tensor composition {label} {k}',
                    ratio(joint,(0,3),(1,4),(2,5),k)==
                    ratio(left,(0,),(1,),(2,),k[:3])*ratio(right,(0,),(1,),(2,),k[3:]))
    p4 = {k:Q(i+1,136) for i,k in enumerate(bits(4))}
    for k in bits(4):
        require(f'chain refinement {k}', ratio(p4,(0,),(1,),(2,3),k)==
                ratio(p4,(0,),(1,),(2,),k)*ratio(p4,(0,),(1,2),(3,),k))
    # Exact rational local unitary on the parity family. Formal log coefficients
    # multiply spectral projectors, so covariance of the projectors suffices.
    I2,I8 = eye(2),eye(8)
    X = ((Q(0),Q(1)),(Q(1),Q(0)))
    Z = ((Q(1),Q(0)),(Q(0),Q(-1)))
    P = tensor3(Z,Z,Z)
    U = ((Q(3,5),Q(-4,5)),(Q(4,5),Q(3,5)))
    V = tensor3(U,I2,I2)
    require('local frame is exactly orthogonal',mm(V,transpose(V))==I8)
    rotated = mm(mm(V,P),transpose(V))
    require('rotated parity involution',mm(rotated,rotated)==I8)
    for sign in (-1,1):
        e = scale(Q(1,2),plus(I8,scale(Q(sign),P)))
        er = scale(Q(1,2),plus(I8,scale(Q(sign),rotated)))
        require(f'formal log projector covariance {sign}',mm(mm(V,e),transpose(V))==er and mm(er,er)==er)
    rho = scale(Q(1,8),plus(I8,scale(Q(1,2),rotated)))
    for keep in ((0,1),(0,2),(1,2)):
        require(f'rotated state marginal {keep}',ptrace(rho,keep)==scale(Q(1,4),eye(4)))
    # A genuinely noncommuting-overlap family (no numerical matrix logarithm).
    P = tensor3(X,X,I2)
    R = tensor3(I2,Z,Z)
    H = plus(P,R)
    zero = scale(Q(0),I8)
    require('noncommuting overlap anticommutation',plus(mm(P,R),mm(R,P))==zero)
    require('overlap operators are not commuting',mm(P,R)!=mm(R,P))
    require('global spectral polynomial H^2=2I',mm(H,H)==scale(Q(2),I8))
    t = Q(1,4)
    rq = scale(Q(1,8),plus(I8,scale(t,H)))
    require('noncommuting state trace one',trace(rq)==1)
    require('noncommuting state full-rank exact positivity condition',2*t*t<1)
    require('noncommuting AB marginal',ptrace(rq,(0,1))==scale(Q(1,4),plus(eye(4),scale(t,kron(X,X)))))
    require('noncommuting BC marginal',ptrace(rq,(1,2))==scale(Q(1,4),plus(eye(4),scale(t,kron(Z,Z)))))
    require('noncommuting B marginal',ptrace(rq,(1,))==scale(Q(1,2),I2))
    # gamma(t)=sum_{n>=1}(2^n-1)t^(2n+1)/(2n+1)>0.
    # The infinite-series proof is in the note; these are finite exact witnesses.
    terms = [Q(2**n-1,2*n+1)*t**(2*n+1) for n in range(1,6)]
    require('strictly positive analytic-series witness terms',all(v>0 for v in terms))
    return {'schema':'uqcf-post-v1545-modular-source-exploratory-v1',
            'scope':'EXPLORATORY_MATHEMATICAL_SCREEN_NOT_V1546_CERTIFICATION',
            'runtime':sys.version.split()[0], 'checks_passed':len(CHECKS),
            'parity_family':records, 'tensor_ratio_checks':128,'chain_ratio_checks':16,
            'pairwise_descent':'FALSIFIED_FOR_THIS_CANDIDATE',
            'new_source_law_adopted':False,'incidence_bridge':'NOT_DEFINED',
            'global_compatibility_violation':False,'physical_gravity':False,
            'noncommuting_example':{'t':str(t),'full_rank_condition':str(2*t*t)+' < 1',
                                    'first_positive_gamma_term':str(terms[0])},
            'check_names':CHECKS}

if __name__=='__main__':
    result=run()
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode('ascii')
    target=Path(__file__).with_name('EXPLORATORY_CHECKS.json')
    target.write_bytes(raw)
    print(json.dumps({k:v for k,v in result.items() if k!='check_names'},sort_keys=True,indent=2))
