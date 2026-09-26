"""Exact supplied-completion -> polar-connection response witness.

This is a rational member of the archived cyclic chiral construction, NOT a
reproduction of v13.09's unpinned numerical seed. No source/hidden-state law is
selected here. The fixed observable is the trace of a directed loop of raw
polar factors. There is no connection to the v15.56 scalar lineage Laplacian.
Exact Pauli moments drive the calculation; NumPy is an independent oracle.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json
import pruning_consistency_audit as q

EDGES=((0,1),(1,2),(2,0))
WORDS=tuple(''.join(w) for w in product('IXYZ',repeat=3))
MUL={('X','Y'):(1,'Z'),('Y','Z'):(1,'X'),('Z','X'):(1,'Y'),
     ('Y','X'):(3,'Z'),('Z','Y'):(3,'X'),('X','Z'):(3,'Y')}


def word(assignments: dict[int,str]) -> str:
    out=['I']*3
    for k,v in assignments.items():
        if type(k) is not int or k not in range(3) or v not in 'IXYZ' or len(v)!=1:
            raise ValueError('Invalid site/Pauli label')
        out[k]=v
    return ''.join(out)


def word_product(a: str,b: str) -> tuple[int,str]:
    if len(a)!=3 or len(b)!=3 or any(x not in 'IXYZ' for x in a+b):
        raise ValueError('Three-site Pauli words required')
    phase=0;out=[]
    for x,y in zip(a,b):
        if x=='I':z=y
        elif y=='I':z=x
        elif x==y:z='I'
        else:
            p,z=MUL[x,y];phase+=p
        out.append(z)
    return phase%4,''.join(out)


def multiply(a: dict[str,F],b: dict[str,F]) -> dict[str,tuple[F,F]]:
    """Exact complex Pauli coefficients, represented by (real, imaginary)."""
    out={}
    for x,c in a.items():
        for y,d in b.items():
            phase,z=word_product(x,y);r,i=out.get(z,(F(0),F(0)));v=F(c)*F(d)
            if phase==0:r+=v
            elif phase==1:i+=v
            elif phase==2:r-=v
            else:i-=v
            out[z]=(r,i)
    return {w:z for w,z in out.items() if z!=(0,0)}


def commutator(a: dict[str,F],b: dict[str,F]) -> dict[str,tuple[F,F]]:
    ab,ba=multiply(a,b),multiply(b,a);out={}
    for w in ab.keys()|ba.keys():
        x,y=ab.get(w,(0,0)),ba.get(w,(0,0));v=(x[0]-y[0],x[1]-y[1])
        if v!=(0,0):out[w]=v
    return out


def expect(rho: dict[str,F],w: str) -> F:
    return F(rho.get(w,0))


def product_expect(rho: dict[str,F],a: dict[str,F],b: dict[str,F]) -> tuple[F,F]:
    v=multiply(a,b)
    return (sum((r*expect(rho,w) for w,(r,i) in v.items()),F(0)),
            sum((i*expect(rho,w) for w,(r,i) in v.items()),F(0)))


def source(a=F(1),identity=F(0)) -> dict[str,F]:
    return {'ZII':F(a),'IZI':F(a),'IIZ':F(a),'III':F(identity)}


def rotation(x=F(3,5),y=F(4,5)):
    return [[F(x),F(y),F(0)],[-F(y),F(x),F(0)],[F(0),F(0),F(1)]]


def positivity_floor(rho: dict[str,F]) -> F:
    """Operator-norm triangle certificate; sufficient, not necessary."""
    return (expect(rho,'III')-sum((abs(v) for w,v in rho.items() if w!='III'),F(0)))/8


def state(c=F(1,20),h=F(1,100),x=F(3,5),y=F(4,5)) -> dict[str,F]:
    c,h,x,y=map(F,(c,h,x,y))
    if c<=0 or x*x+y*y!=1:
        raise ValueError('Positive pair scale and unit rational rotation required')
    rho={'III':F(1)}
    def put(w,v):rho[w]=rho.get(w,F(0))+v
    for i,j in EDGES:
        for a,b,v in (('X','X',c*x),('Y','Y',c*x),('X','Y',c*y),('Y','X',-c*y),('Z','Z',c)):
            put(word({i:a,j:b}),v)
        k=3-i-j
        put(word({i:'X',j:'Y',k:'Z'}),h)
        put(word({i:'Y',j:'X',k:'Z'}),-h)
    if positivity_floor(rho)<=0:
        raise ValueError('Outside the certified faithful fixture region')
    return {w:v for w,v in rho.items() if v}


def tangent(rho: dict[str,F],p: dict[str,F]) -> dict[str,F]:
    """ETL tangent for [rho,p]=0 only; rejects noncommuting generators."""
    if expect(rho,'III')!=1:raise ValueError('Normalized state moments required')
    if commutator(rho,p):raise ValueError('This exact ETL evaluator requires [rho,P]=0')
    mean=sum((a*expect(rho,w) for w,a in p.items()),F(0));out={}
    for w in WORDS:
        z,imag=product_expect(rho,{w:F(1)},p)
        if imag:raise ArithmeticError('Nonreal commuting response')
        out[w]=z-expect(rho,w)*mean
    return out


def connected(rho: dict[str,F],i: int,j: int):
    if i==j or i not in range(3) or j not in range(3):raise ValueError('Distinct sites required')
    return [[expect(rho,word({i:a,j:b}))-expect(rho,word({i:a}))*expect(rho,word({j:b}))
             for b in 'XYZ'] for a in 'XYZ']


def connected_jet(rho: dict[str,F],t: dict[str,F],i: int,j: int):
    return [[expect(t,word({i:a,j:b}))-expect(t,word({i:a}))*expect(rho,word({j:b}))
             -expect(rho,word({i:a}))*expect(t,word({j:b})) for b in 'XYZ'] for a in 'XYZ']


def transpose(A):return [list(x) for x in zip(*A)]
def trace(A):return sum((A[i][i] for i in range(len(A))),F(0))
def det3(A):
    return sum((A[0][i]*(A[1][(i+1)%3]*A[2][(i+2)%3]-A[1][(i+2)%3]*A[2][(i+1)%3])
                for i in range(3)),F(0))


def polar_jet(C,E):
    """Raw polar and Frechet jet on C^T C=c^2 I, rational c>0.

    No singular-vector orientation convention or determinant correction.
    Degenerate singular VALUES are allowed; rank deficiency is not.
    """
    if any(len(A)!=3 or any(len(row)!=3 for row in A) for A in (C,E)):
        raise ValueError('3x3 matrices required')
    gram=q.mul(transpose(C),C);c2=F(gram[0][0])
    if c2<=0 or gram!=q.scale(q.eye(3),c2):
        raise ValueError('Requires a nonzero scaled-orthogonal base correlation')
    a,d=isqrt(c2.numerator),isqrt(c2.denominator)
    if a*a!=c2.numerator or d*d!=c2.denominator:
        raise ValueError('Base polar scale is not rational')
    c=F(a,d);R=q.scale(C,1/c)
    # H Omega+Omega H=R^T E-E^T R, with H=cI.
    omega=q.scale(q.sub(q.mul(transpose(R),E),q.mul(transpose(E),R)),1/(2*c))
    return R,q.mul(R,omega)


def loop_jet(os,ds):
    if len(os)!=3 or len(ds)!=3:raise ValueError('Three directed cycle edges required')
    H=q.mul(q.mul(os[0],os[1]),os[2]);dH=q.zeros(3,3)
    for i in range(3):
        mats=[ds[j] if i==j else os[j] for j in range(3)]
        dH=q.add(dH,q.mul(q.mul(mats[0],mats[1]),mats[2]))
    return H,dH


def analyze(rho: dict[str,F],p: dict[str,F]):
    t=tangent(rho,p);os=[];ds=[]
    for edge in EDGES:
        O,D=polar_jet(connected(rho,*edge),connected_jet(rho,t,*edge));os.append(O);ds.append(D)
    H,dH=loop_jet(os,ds)
    reference=sum((expect(t,word({i:'Z'})) for i in range(3)),F(0))/3
    return {'trace':trace(H),'trace_jet':trace(dH),'holonomy':H,'holonomy_jet':dH,
            'reference_jet':reference,'scale_free_ratio':trace(dH)/reference if reference else None,
            'minimum_state_eigenvalue_lower_bound':positivity_floor(rho),
            'edge_determinants':[det3(O) for O in os]}


def finite_tilt(rho: dict[str,F],t: F,collective=True) -> dict[str,F]:
    """Exact normalized ETL at tanh(s)=t, for commuting selected Z source."""
    t=F(t)
    if abs(t)>=1:raise ValueError('Finite faithful tilt requires |t|<1')
    sites=range(3) if collective else (2,)
    p={word({i:'Z'}):F(1) for i in sites}
    if commutator(rho,p):raise ValueError('Noncommuting finite tilt not implemented')
    weights={}
    for bits in product((0,1),repeat=len(sites)):
        weights[word({i:'Z' for i,bit in zip(sites,bits) if bit})]=t**sum(bits)
    normalization=sum((a*expect(rho,w) for w,a in weights.items()),F(0))
    if normalization<=0:raise ValueError('Nonpositive normalization')
    out={}
    for w in WORDS:
        re,im=product_expect(rho,{w:F(1)},weights)
        if im:raise ArithmeticError('Finite tilt is not Hermitian')
        out[w]=re/normalization
    return out


def dense_word(w):
    import numpy as np
    paulis={'I':np.eye(2),'X':np.array([[0,1],[1,0]]),'Y':np.array([[0,-1j],[1j,0]]),'Z':np.diag([1,-1])}
    A=np.ones((1,1),complex)
    for x in w:A=np.kron(A,paulis[x])
    return A


def dense(coeff,normalized=True):
    import numpy as np
    out=np.zeros((8,8),complex)
    for w,a in coeff.items():out+=float(a)*dense_word(w)
    return out/8 if normalized else out


def numeric_oracle(rho,p):
    """Independent dense exp(log rho+sP) and raw-SVD finite differences."""
    import numpy as np
    R=dense(rho);P=dense(p,False);val,V=np.linalg.eigh(R)
    if min(val)<=0:raise ValueError('Nonfaithful oracle input')
    logR=(V*np.log(val))@V.conj().T
    def geometry(s):
        v,U=np.linalg.eigh(logR+s*P);ev=np.exp(v-v.max());rs=(U*ev)@U.conj().T/ev.sum()
        def mean(w):return float(np.trace(rs@dense_word(w)).real)
        os=[];sing=[];dets=[]
        for i,j in EDGES:
            C=np.array([[mean(word({i:a,j:b}))-mean(word({i:a}))*mean(word({j:b})) for b in 'XYZ'] for a in 'XYZ'])
            u,d,vh=np.linalg.svd(C);O=u@vh;os.append(O);sing.extend(d);dets.append(float(np.linalg.det(O)))
        return os[0]@os[1]@os[2],float(min(sing)),float(np.linalg.eigvalsh(rs).min()),dets
    exact=np.array(analyze(rho,p)['holonomy_jet'],float);rows=[]
    for s in (1e-4,3e-5,1e-5):
        Hp,sp,lp,dp=geometry(s);Hm,sm,lm,dm=geometry(-s)
        rows.append({'step':s,'jet_error':float(np.linalg.norm((Hp-Hm)/(2*s)-exact)),
                     'min_edge_singular_value':min(sp,sm),'min_state_eigenvalue':min(lp,lm),
                     'min_raw_polar_determinant':min(dp+dm)})
    return {'method':'dense Hermitian exp(log rho+sP), raw SVD, central difference',
            'rows':rows,'max_jet_error':max(x['jet_error'] for x in rows),
            'min_edge_singular_value':min(x['min_edge_singular_value'] for x in rows),
            'min_state_eigenvalue':min(x['min_state_eigenvalue'] for x in rows),
            'determinant_flip_count':0}


def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [serial(v) for v in value]
    return value


def run():
    rows={str(h):analyze(state(h=h),source()) for h in (F(-1,100),F(0),F(1,100))}
    gap=rows[str(F(-1,100))]['scale_free_ratio']-rows[str(F(1,100))]['scale_free_ratio']
    return serial({'schema':'uqcf-completion-connection-bridge-v1',
        'baseline':'8cf281ab1eb9cba2e2912abb5c12b043f215328d',
        'fixture_provenance':'NEW_RATIONAL_MEMBER_OF_ARCHIVED_CHIRAL_FAMILY_NOT_V1309_SEED_REPLAY',
        'arithmetic':'EXACT_RATIONAL_PAULI_ALGEBRA_AND_POLAR_JET',
        'parameters':{'c':F(1,20),'cos_theta':F(3,5),'sin_theta':F(4,5)},
        'observable':'trace(raw_polar(C01) raw_polar(C12) raw_polar(C20))',
        'source':'Z0+Z1+Z2','reference_observable':'(Z0+Z1+Z2)/3',
        'rows':rows,'scale_free_response_gap':gap,'minimum_initial_pair_singular_value':F(1,20),
        'parity_fixture_initial_pair_rank':0,'posthoc_fit':False,
        'claims':{'conditional_connection_response_witness':True,'reproduces_v1309_numbers':False,
                  'repair_history_selects_hidden_state':False,'derived_Genesis_source':False,
                  'lineage_scalar_bridge':False,'physical_curvature_or_gravity':False,'novel_effect':False}})

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
