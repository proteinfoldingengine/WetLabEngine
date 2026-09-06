"""Exact phase-persistence audit; uses the v9.170 coordinate-map builder."""
import collections
import sympy as s
import v9170_higher_incidence_certificate as old
u=s.Symbol('u', positive=True)
K=s.QQ.algebraic_field(s.sqrt(2)).frac_field(u)
old.z=10*u**2
old.field=K

def coords(V):
    F=V.applyfunc(lambda v:2 if v in (0,3,4) else u*(1 if v==1 else s.sqrt(2)))
    vec=[]
    for k in range(5):
        col={}
        for i in range(5):
            a=1 if i==k else F[i,k]
            for ijk in ((i,i,k),(i,k,i)):col[ijk]=col.get(ijk,0)+a
        vec.append(col)
    for i in range(5):
        N=[j for j in range(5) if V[i,j]>=3]
        for j in N:
            for k in N:vec.append({(i,j,k):s.Integer(1)})
    return vec

def certified_eliminate(M):
    basis={}; factors=set()
    for row in sorted(M.to_dod().values(),key=len):
        row=row.copy()
        while row:
            p=min(row);a=row[p]
            if p not in basis:
                factors.add(a)
                basis[p]={j:b/a for j,b in row.items()}
                break
            for j,b in basis[p].items():
                value=row.get(j,K.zero)-a*b
                if value:row[j]=value
                else:row.pop(j,None)
    return len(basis),factors

if __name__=='__main__':
    hist=collections.Counter();factors=set()
    expected={(3,2):311,(2,2):313,(2,4):321,(5,0):315,(0,5):315}
    arrangements=old.normalized_arrangements()
    assert len(arrangements)==56
    for i,V in enumerate(arrangements):
        mu=old.maps(coords(V))
        M=old.dm_from_rows(list(mu[0].values())+list(mu[1].values()),625)
        rank,ff=certified_eliminate(M);factors.update(ff);hist[625-rank]+=1
        S=V.applyfunc(lambda x:1 if x>=3 else 0)
        motif=(int(s.trace(S**2)/2),int(s.trace(S**3)/3))
        assert 625-rank==expected[motif]
        if V==old.VA:assert 625-rank==315
        if V==old.VB:assert 625-rank==311
        print(i+1,625-rank,flush=True)
    print('HIST',hist,flush=True)
    polys=set()
    for f in factors:
        for expr in s.fraction(K.to_sympy(f)):
            for poly,mult in s.factor_list(expr,u,extension=s.sqrt(2))[1]:
                polys.add(s.Poly(poly,u,extension=s.sqrt(2)).monic().as_expr())
    print('PIVOT FACTORS',sorted(polys,key=str),flush=True)
    assert polys=={u,u-1,u-2,u-2*s.sqrt(2),u-s.sqrt(2),u**2-2*s.sqrt(2)}
    # Their real zeros are 0,1,2,2sqrt(2),sqrt(2),+/-sqrt(2sqrt(2)).
    # The only zero in the CLOSED phase interval is the upper endpoint sqrt(2).
    lo=2/s.sqrt(3);hi=s.sqrt(2)
    assert (lo-1).is_positive and (hi-lo).is_positive
    assert (2-hi).is_positive and (2*s.sqrt(2)-hi).is_positive
    assert (2*s.sqrt(2)-hi**2).is_positive
    assert hist=={311:10,313:20,315:6,321:20}
    zz=10*u**2;tt=1-zz/(s.Rational(13,10)*zz+12)
    DD=10+3*u**2;cc=(1-tt)/(5*zz)
    d3=(1-tt)/5*(s.Rational(3,10)-4/zz)
    d4=(1-tt)/5*(s.Rational(4,10)-4/zz)
    assert s.cancel(10*DD*cc+5*(d3+d4)-1)==0
    assert s.simplify(tt.subs(u,lo)-s.Rational(6,11))==0
    assert s.simplify(tt.subs(u,hi)-s.Rational(9,19))==0
    print('PASS: all 56 ranks persist on the ENTIRE OPEN phase; no interior exceptions.')
