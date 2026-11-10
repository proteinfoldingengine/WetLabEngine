#!/usr/bin/env python3
"""Independent exact symbolic reconstruction. Execute only after scientific freeze.

Outputs canonical JSON containing rational matrix entries. Symbolic amplitude
identities are asserted internally; no floating point or random inputs are used.
"""
import json
import sympy as s


def unit(n, i, j=None):
    m = s.zeros(n)
    m[i, i if j is None else j] = 1
    return m


def ix(j, e, r):
    return 4*j + 2*e + r


def ptr_source(x):
    return s.Matrix(4, 4, lambda i,j: sum(x[ix(i,e,r),ix(j,e,r)] for e in range(2) for r in range(2)))


def ptr_receiver(x):
    return s.Matrix(2, 2, lambda r,t: sum(x[ix(j,e,r),ix(j,e,t)] for j in range(4) for e in range(2)))


def eq(a,b):
    assert (a-b).applyfunc(s.simplify) == s.zeros(*a.shape), (a,b)


def encode(x):
    if isinstance(x, s.MatrixBase):
        return [[encode(v) for v in row] for row in x.tolist()]
    if isinstance(x, dict):
        return {k:encode(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)):
        return [encode(v) for v in x]
    if isinstance(x, str):
        return x
    v = s.simplify(x)
    assert v.is_Rational, v
    return str(v)


def main():
    I4,I16=s.eye(4),s.eye(16)
    atoms=[unit(4,j) for j in range(4)]
    units=[unit(4,i,j) for i in range(4) for j in range(4)]
    o,p,u,v=atoms
    Q=I4-u
    def C(x): return Q*x*Q+x[2,2]*p
    V={name:s.zeros(16,4) for name in ('WR','B','Bell','A')}
    for j in range(4):
        k=1 if j==2 else j
        V['WR'][ix(k,0,int(j==2)),j]=1
        V['B'][ix(k,int(j==2),0),j]=1
        V['Bell'][ix(k,0,0),j]=1
        V['Bell'][ix(k,1,1),j]=-1 if j==2 else 1
        V['A'][ix(k,int(j==2),0),j]=1
        V['A'][ix(k,int(j==2),1),j]=-1 if j==2 else 1
    scale2={k:s.Rational(1,2) if k in ('Bell','A') else s.Integer(1) for k in V}
    W={k:s.sqrt(scale2[k])*m for k,m in V.items()}
    L=[s.zeros(4,16),s.zeros(4,16)]
    for r in range(2):
        for j in (0,1,3): L[r][j,ix(j,0,r)]=1
        L[r][2,ix(1,1,r)]=(-1)**r
    P=sum((l.T*l for l in L),s.zeros(16))
    complement=I16-P
    eq(P*P,P)
    assert P.rank()==8
    eq(P,s.kronecker_product(Q,unit(2,0),s.eye(2))+s.kronecker_product(p,unit(2,1),s.eye(2)))
    completion=[s.zeros(4,16) for _ in range(8)]
    for k,b in enumerate(i for i in range(16) if complement[i,i]==1): completion[k][0,b]=1
    normalization=sum((l.T*l for l in L+completion),s.zeros(16))
    eq(normalization,I16)
    def D(x): return sum((l*x*l.T for l in L),s.zeros(4))+s.trace(complement*x)*o
    def adjoint(h): return sum((l.T*h*l for l in L),s.zeros(16))+h[0,0]*complement
    for r in range(2):
        eq(L[r]*W['A'],I4/s.sqrt(2))
        eq(L[r]*W['B'],I4 if r==0 else s.zeros(4))
    eq(W['A'].T*W['B'],I4/s.sqrt(2))
    for k in ('A','B'): eq(complement*W[k],s.zeros(16,4))
    H=[s.zeros(16) for _ in range(4)]
    for j in range(4):
        for e in range(2):
            for r in range(2):
                label=2 if j==1 and (e,r) in ((0,1),(1,0)) else j
                H[label][ix(j,e,r),ix(j,e,r)]=1
    eq(sum(H,s.zeros(16)),I16)
    for a in range(4):
        for b in range(4): eq(H[a]*H[b],H[a] if a==b else s.zeros(16))
    def Dcl(x): return sum((s.trace(h*x)*a for h,a in zip(H,atoms)),s.zeros(4))
    encodings={}; classical={}; quantum={}
    for name,w in W.items():
        eq(w.T*w,I4)
        image=w*w.T
        rest=I16-image
        # Individual completion uses tau=Pi_o. Its adjoint Kraus sum
        # is image + rest^2, since rest is an orthogonal projector.
        eq(rest*rest,rest)
        normalization_w=image+rest.T*rest
        eq(normalization_w,I16)
        def DW(x): return w.T*x*w+s.trace(rest*x)*o
        images=[w*x*w.T for x in units]
        channel=[ptr_source(x) for x in images]
        receiver=[ptr_receiver(x) for x in images]
        recovery=[DW(x) for x in images]
        for a,b,x in zip(channel,recovery,units): eq(a,C(x)); eq(b,x)
        encodings[name]={'columns_scaled':V[name],'gram':w.T*w,'column_scale_squared':scale2[name], 'channel':channel,'r_receiver':receiver,'individual_recovery':recovery,'individual_tp':normalization_w,'individual_image_projection':image}
        classical[name]=[Dcl(x) for x in images]
        quantum[name]=[D(x) for x in images]
        for index,x in enumerate(units):
            if name in ('WR','B'):
                eq(classical[name][index],s.diag(*[x[j,j] for j in range(4)]))
            if name in ('A','B'): eq(quantum[name][index],x)
            if name=='B': eq(receiver[index],s.trace(x)*unit(2,0))
            if name=='A':
                plus=s.Matrix([[1,1],[1,1]])/2
                minus=s.Matrix([[1,-1],[-1,1]])/2
                eq(receiver[index],s.trace(Q*x)*plus+x[2,2]*minus)
    eq(classical['Bell'][10],p)
    assert classical['Bell'][10]!=u
    assert classical['WR'][6]!=units[6]
    G=adjoint(u)
    GE=s.kronecker_product(I4,unit(2,1),s.eye(2))
    eq(G,s.kronecker_product(p,unit(2,1),s.eye(2)))
    eq(G*G,G)
    eq(P*G*P,P*GE*P)
    F=s.Matrix([[1,-1],[-1,1]])/2
    effect=s.kronecker_product(I4,s.eye(2),F)
    pulls={k:w.T*effect*w for k,w in W.items()}
    eq(pulls['A'],u); eq(pulls['B'],I4/2)
    rp=(o+p+2*u+v)/5; rm=(o+p+u+2*v)/5; delta=rp-rm
    eq(delta,(u-v)/5)
    assert s.trace(rp)==s.trace(rm)==1
    assert rp[1,1]==rm[1,1]
    pair={'source_plus':rp,'source_minus':rm,'delta':delta,'channel_plus':C(rp),'channel_minus':C(rm),'r_plus':{},'r_minus':{},'r_delta':{},'F_probabilities':{},'E_probabilities':{},'initial_R':unit(2,0)}
    for k,w in W.items():
        a=w*rp*w.T; b=w*rm*w.T
        ar=ptr_receiver(a); br=ptr_receiver(b)
        pair['r_plus'][k]=ar; pair['r_minus'][k]=br; pair['r_delta'][k]=ar-br
        pair['F_probabilities'][k]=[s.trace(F*ar),s.trace(F*br),s.trace(F*(ar-br))]
        pair['E_probabilities'][k]=[s.trace(GE*a),s.trace(GE*b)]
    assert pair['F_probabilities']['A']==[s.Rational(2,5),s.Rational(1,5),s.Rational(1,5)]
    assert pair['F_probabilities']['B']==[s.Rational(1,2),s.Rational(1,2),0]
    for k in ('A','B'): assert pair['E_probabilities'][k]==[s.Rational(2,5),s.Rational(1,5)]
    assert s.trace(p*C(rp))==s.Rational(3,5) and s.trace(p*C(rm))==s.Rational(2,5)
    eq(pair['r_delta']['WR'],s.diag(-s.Rational(1,5),s.Rational(1,5)))
    eq(pair['r_delta']['Bell'],s.zeros(2))
    gradeP=s.Matrix([[1,0,0,0],[0,1,1,0],[0,0,0,1]])
    gradeI=s.Matrix([[1,0,0],[0,1,0],[0,0,0],[0,0,1]])
    loss=I4-gradeI*gradeP
    witness=s.Matrix([0,-1,1,0])
    eq(gradeP*gradeI,s.eye(3)); eq(gradeP*witness,s.zeros(3,1))
    eq(loss,witness*s.Matrix([[0,0,1,0]]))
    for x in [s.Matrix([rp[j,j] for j in range(4)]),s.Matrix([rm[j,j] for j in range(4)])]: eq(gradeI*gradeP*x+loss*x,x)
    badL=L[1].copy(); badL[2,ix(1,1,1)]=1
    pu=unit(4,1,2); apu=W['A']*pu*W['A'].T
    wrong=L[0]*apu*L[0].T+badL*apu*badL.T+s.trace(complement*apu)*o
    eq(wrong,s.zeros(4)); assert wrong!=pu
    off=unit(16,ix(2,0,0))
    dropped=sum((l*off*l.T for l in L),s.zeros(4))
    eq(dropped,s.zeros(4)); assert s.trace(dropped)!=s.trace(off)
    old=D(W['WR']*u*W['WR'].T); eq(old,p); assert old!=u
    z=unit(16,ix(0,1,0)); offvalues=[s.trace(G*z),s.trace(GE*z)]
    assert offvalues==[0,1]
    output={'schema':'fixed-common-decoder-v1','declared_channel':[C(x) for x in units],'encodings':encodings,'classical':classical,'quantum':quantum,
      'common':{'L0':L[0],'L1':L[1],'L_products':[l.T*l for l in L],'complement_kraus':completion,'complement_products':[l.T*l for l in completion],'P':P,'complement':complement,'kraus_normalization':normalization,'G':G,'GE':GE,'PGP':P*G*P,'PGEP':P*GE*P,'F':F,'pullback_F':pulls,'intertwiner_scaled':{k:{'L0':L[0]*m,'L1':L[1]*m,'complement':complement*m} for k,m in V.items()}},
      'pair':pair,'grades':{'P':gradeP,'I':gradeI,'PI':gradeP*gradeI,'loss_map':loss,'kernel_witness':witness,'kernel_image':gradeP*witness,'loss_plus':loss*s.Matrix([rp[j,j] for j in range(4)]),'loss_minus':loss*s.Matrix([rm[j,j] for j in range(4)])},
      'adverse':{'dropped_complement_output':dropped,'removed_phase_pu':wrong,'old_WR_u':old,'offcode_G_GE':offvalues}}
    print(json.dumps(encode(output),sort_keys=True,separators=(',',':')))


if __name__=='__main__':
    main()
