"""Independent v16.23 verifier: exact equalizers and global positive preimages.

Imports neither engine.py nor either parent implementation. Pruefer enumeration,
parent stepping, equalizer elimination, and direct global positive enumeration
supply independent routes. No producer verdict fields are trusted.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
import hashlib,json,lzma,re
import sympy as sp

CHECKS=0
GENESIS='v1623-fixed-genesis'
PHASH='59c2c2f6d1091e7102e51932ed4ee7827668d12db7f1b08ffb0724791c8df713'

def require(ok,msg):
    global CHECKS
    CHECKS+=1
    if not ok:raise ValueError(msg)

def rational(a):
    require(type(a) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?',a) is not None,'invalid exact rational')
    return sp.Rational(a)

def decode(d):
    require(type(d) is dict and set(d)=={'rows','cols','data'},'missing or invalid matrix fields')
    n,m=d['rows'],d['cols'];require(type(n) is int and type(m) is int and 0<=n<=32 and 0<=m<=32,'invalid matrix dimensions')
    require(type(d['data']) is list and len(d['data'])==n*m,'matrix entry count')
    return sp.Matrix(n,m,[rational(z) for z in d['data']])

def encode(M):return {'rows':M.rows,'cols':M.cols,'data':[str(a) for a in M]}

def parents(p):
    require(type(p) in (list,tuple) and 0<len(p)<=7,'invalid carrier size')
    require(all(type(a) is int for a in p) and p[0]==-1,'exact parent identifiers required')
    for v in range(1,len(p)):
        u=v;seen=set()
        while u!=0:
            require(0<u<len(p) and u not in seen,'invalid ancestry or cycle');seen.add(u);u=p[u]
    return tuple(p)

def keep(p,V):
    require(type(V) in (list,tuple) and V and all(type(v) is int for v in V),'invalid retained identities')
    require(len(set(V))==len(V) and 0 in V and all(0<=v<len(p) for v in V),'illegal retained carrier')
    for v in V:
        u=v
        while u:require(p[u] in V,'missing retained ancestor');u=p[u]
    return tuple(V)

def shape_code(p,V=None):
    V=set(range(len(p))) if V is None else set(V)
    def f(v):return '('+''.join(sorted(f(w) for w in V if w and p[w]==v))+')'
    return f(0)

def independent_shapes(limit):
    codes=set()
    for n in range(1,limit+1):
        for word in product(range(n),repeat=max(0,n-2)):
            adj=[set() for _ in range(n)];deg=[1]*n
            if n>1:
                for v in word:deg[v]+=1
                for v in word:
                    a=next(i for i,d in enumerate(deg) if d==1)
                    adj[a].add(v);adj[v].add(a);deg[a]-=1;deg[v]-=1
                a,b=[i for i,d in enumerate(deg) if d==1];adj[a].add(b);adj[b].add(a)
            def rec(v,prev):return '('+''.join(sorted(rec(w,v) for w in adj[v] if w!=prev))+')'
            codes.add(rec(0,-1))
    return codes

@lru_cache(None)
def raw_maps(p,X,Y):
    location={a:i for i,a in enumerate(Y)};P=sp.zeros(len(Y),len(X));I=sp.zeros(len(X),len(Y))
    xn=[a for a in X if a];yn=[a for a in Y if a];R=sp.zeros(len(yn),len(xn));H=sp.zeros(len(xn),len(yn))
    for j,a in enumerate(X):
        b=a
        while b not in location:b=p[b]
        P[location[b],j]=1
    for j,a in enumerate(Y):I[X.index(a),j]=1
    for j,a in enumerate(yn):R[j,xn.index(a)]=1
    for j,a in enumerate(xn):
        b=a
        while b not in location:b=p[b]
        if b:H[j,yn.index(b)]=1
    return P,I,R,H

@lru_cache(None)
def fiber_indices(p,X,Y):
    out=[]
    for a in X:
        while a not in Y:a=p[a]
        out.append(Y.index(a))
    return tuple(out)

def aggregate(p,X,Y,x):
    out=[0]*len(Y)
    for j,a in enumerate(fiber_indices(p,X,Y)):out[a]+=x[j]
    return tuple(out)

@lru_cache(None)
def masses(n,total):
    out=[]
    for multiset in combinations_with_replacement(range(n),total):
        x=[0]*n
        for i in multiset:x[i]+=1
        out.append(tuple(x))
    return tuple(out)

def pos_check(p,Y,Z,U,J,reported):
    require(type(reported) is dict and set(reported)=={'compatible','gluable','obstructed','witness'},'invalid cone certificate')
    compatible=good=bad=0
    for total in range(3):
        images={}
        for g in masses(len(U),total):
            k=(aggregate(p,U,Y,g),aggregate(p,U,Z,g))
            require(k not in images,'nonunique positive global preimage');images[k]=g
        grouped={}
        for z in masses(len(Z),total):grouped.setdefault(aggregate(p,Z,J,z),[]).append(z)
        for y in masses(len(Y),total):
            c=aggregate(p,Y,J,y)
            for z in grouped.get(c,[]):
                compatible+=1;yy=dict(zip(Y,y));zz=dict(zip(Z,z));cc=dict(zip(J,c))
                g=tuple(yy.get(v,0)+zz.get(v,0)-cc.get(v,0) for v in U)
                nonneg=all(a>=0 for a in g);exists=(y,z) in images
                require(nonneg==exists,'cone criterion disagrees with direct global enumeration')
                if exists:require(images[y,z]==g,'wrong positive preimage');good+=1
                else:bad+=1
    for key,value in [('compatible',compatible),('gluable',good),('obstructed',bad)]:
        require(type(reported[key]) is int and reported[key]==value,'false cone '+key)
    w=reported['witness']
    if bad:
        require(type(w) is dict and set(w)=={'y','z','global'},'missing negative witness')
        y=tuple(rational(a) for a in w['y']);z=tuple(rational(a) for a in w['z']);g=tuple(rational(a) for a in w['global'])
        require(len(y)==len(Y) and len(z)==len(Z) and len(g)==len(U),'witness domains')
        require(all(a>=0 and a.q==1 for a in y+z) and sum(y)==sum(z) and sum(y) in (0,1,2),'inadmissible local witness')
        c=aggregate(p,Y,J,y);require(c==aggregate(p,Z,J,z),'incompatible witness')
        require(aggregate(p,U,Y,g)==y and aggregate(p,U,Z,g)==z and any(a<0 for a in g),'corrupt negative witness image')
    else:require(w is None,'spurious negative witness')
    return compatible,good,bad

def kernel(D):
    ns=D.nullspace()
    return sp.Matrix.hstack(*ns) if ns else sp.zeros(D.cols,0)

def equalizer(A,D,B,expected_n):
    require(D.cols==A.rows and B.rows==A.cols and B.cols==A.rows,'gluing map type mismatch')
    require(D*A==sp.zeros(D.rows,A.cols),'incompatible defining maps')
    require(A.rank()==expected_n and A.cols==expected_n,'joint map not injective')
    K=kernel(D);require(K.cols==expected_n,'not the complete compatibility space')
    require(B*A==sp.eye(expected_n),'gluer fails reconstruction')
    require((A*B-sp.eye(A.rows))*K==sp.zeros(A.rows,K.cols),'gluer fails on compatible data')
    n=A.cols;m=A.rows;u=sp.eye(n);v=sp.eye(m)
    if n>1:u[0,n-1]=sp.Rational(1,3)
    if m>1:v[m-1,0]=sp.Rational(2,5)
    a=v.inv()*A*u;b=u.inv()*B*v;d=D*v;k=v.inv()*K
    require(b*a==sp.eye(n) and d*a==sp.zeros(d.rows,n),'coordinate-dependent reconstruction')
    require((a*b-sp.eye(m))*k==sp.zeros(m,k.cols),'coordinate-dependent compatibility')
    return K

def check_section(P,I,a,b):
    require(P*I==sp.eye(P.rows),'invalid source section')
    require(a*I==I*b,'retained naturality failed')

def balanced(V):
    vn=[v for v in V if v];M=sp.zeros(len(V),len(vn))
    for j,v in enumerate(vn):M[V.index(v),j]=1;M[V.index(0),j]=-1
    return M

def pair_expected(p,Y,Z,U,J):
    pY,iY,rY,hY=raw_maps(p,U,Y);pZ,iZ,rZ,hZ=raw_maps(p,U,Z)
    pyj,_,ryj,_=raw_maps(p,Y,J);pzj,_,rzj,_=raw_maps(p,Z,J)
    return pY.col_join(pZ),pyj.row_join(-pzj),rY.col_join(rZ),ryj.row_join(-rzj)

def _verify_case(d,parent_family=None):
    require(type(d) is dict and all(k in d for k in ['parents','keeps','pairs','triples','genesis','tag']),'missing instance fields')
    require(d['genesis']==GENESIS and type(d['tag']) is str,'foreign instance identity')
    p=parents(d['parents']);ks=[keep(p,V) for V in d['keeps']];key={frozenset(V):i for i,V in enumerate(ks)}
    expected=[]
    for choices in product((False,True),repeat=len(p)-1):
        V=(0,)+tuple(i+1 for i,b in enumerate(choices) if b)
        if all(p[v] in V for v in V if v):expected.append(frozenset(V))
    require(len(ks)==len(key)==len(expected) and set(key)==set(expected),'missing/duplicate retained carriers')
    n=len(ks);records={};stats={'pairs':0,'triples':0,'positive_compatible':0,'positive_gluable':0,'positive_obstructed':0,'parent_basis_diagrams':0,'balanced_equalizers':0,'coordinate_diagrams':0}
    X=tuple(range(len(p)));matrix_cache={}
    for r in d['pairs']:
        require(type(r) is dict and all(k in r for k in ['views','union','overlap','genesis','source','response','positive']),'missing pair certificate')
        require(type(r['views']) is list and len(r['views'])==2 and all(type(i) is int and 0<=i<n for i in r['views']),'invalid view identities')
        a,b=r['views'];require((a,b) not in records and r['genesis']==GENESIS,'duplicate pair or foreign origin')
        Y,Z=ks[a],ks[b];u=key[frozenset(Y)|frozenset(Z)];j=key[frozenset(Y)&frozenset(Z)];U,J=ks[u],ks[j]
        require(type(r['union']) is int and r['union']==u and type(r['overlap']) is int and r['overlap']==j,'wrong union or overlap')
        A,D,QA,QD=pair_expected(p,Y,Z,U,J)
        Bs=[]
        for kind,aa,dd in [('source',A,D),('response',QA,QD)]:
            require(type(r[kind]) is dict and set(r[kind])=={'A','B','D'},'missing required map')
            ra=decode(r[kind]['A']);rd=decode(r[kind]['D']);rb=decode(r[kind]['B'])
            require(ra==aa and rd==dd,'incorrect '+kind+' defining map')
            equalizer(ra,rd,rb,len(U) if kind=='source' else len(U)-1)
            Bs.append(rb);stats['coordinate_diagrams']+=1
        B,QB=Bs
        lift=sp.diag(balanced(Y),balanced(Z));Ds=D*lift;Ks=kernel(Ds)
        require(Ks.cols==len(U)-1,'balanced overlap dimension')
        require(sp.ones(1,len(U))*B*lift*Ks==sp.zeros(1,Ks.cols),'gluing does not preserve balance');stats['balanced_equalizers']+=1
        Pxy,Iyx,_,_=raw_maps(p,X,Y);Pxz,Izx,_,_=raw_maps(p,X,Z);Pxu,Iux,_,_=raw_maps(p,X,U);Pxj,Ijx,_,_=raw_maps(p,X,J)
        Ey=Iyx*Pxy;Ez=Izx*Pxz;Eu=Iux*Pxu;Ej=Ijx*Pxj
        require(Ey*Ez==Ez*Ey==Ej and Ey+Ez-Ej==Eu,'retained lattice projector identity')
        stack=Pxy.col_join(Pxz);ku=kernel(Pxu)
        require(stack*ku==sp.zeros(stack.rows,ku.cols) and stack.rank()==len(U),'joint readout loses more/less than outside union')
        c,g,f=pos_check(p,Y,Z,U,J,r['positive']);stats['positive_compatible']+=c;stats['positive_gluable']+=g;stats['positive_obstructed']+=f
        if parent_family is not None:
            for getT in parent_family:
                TY,TZ,TU=getT(p,Y),getT(p,Z),getT(p,U)
                pick=[i for i,v in enumerate(U) if v]
                lhs=TU*(B*lift)[pick,:]*Ks;rhs=QB*sp.diag(TY,TZ)*Ks
                require(lhs==rhs,'parent response basis violates new overlap diagram');stats['parent_basis_diagrams']+=1
        records[a,b]=(u,B,QB)
        matrix_cache[a,b]=(u,[[int(t) if t.q==1 else F(str(t)) for t in B.row(i)] for i in range(B.rows)],[[int(t) if t.q==1 else F(str(t)) for t in QB.row(i)] for i in range(QB.rows)])
        stats['pairs']+=1
    require(set(records)==set(product(range(n),repeat=2)),'missing pair coverage')
    seen=set()
    def combine(a,b,x,y,kind):
        u,B,QB=matrix_cache[a,b];M=B if kind=='source' else QB;v=x+y
        return u,tuple(sum(z*w for z,w in zip(row,v)) for row in M)
    for raw in d['triples']:
        require(type(raw) is list and len(raw)==3 and all(type(i) is int and 0<=i<n for i in raw),'invalid triple key')
        a,b,c=raw;require(tuple(raw) not in seen,'duplicate triple');seen.add(tuple(raw))
        U=ks[key[frozenset(ks[a])|frozenset(ks[b])|frozenset(ks[c])]]
        for kind,dim in [('source',len(U)),('response',len(U)-1)]:
            for col in range(dim):
                x=tuple(int(i==col) for i in range(dim))
                if kind=='source':ys=[aggregate(p,U,ks[j],x) for j in (a,b,c)]
                else:
                    vals=dict(zip([v for v in U if v],x));ys=[tuple(vals[v] for v in ks[j] if v) for j in (a,b,c)]
                ab,vab=combine(a,b,ys[0],ys[1],kind);left,lv=combine(ab,c,vab,ys[2],kind)
                bc,vbc=combine(b,c,ys[1],ys[2],kind);right,rv=combine(a,bc,ys[0],vbc,kind)
                require(left==right and ks[left]==U and lv==rv==x,'triple associativity/reconstruction')
        stats['triples']+=1
    require(seen==set(product(range(n),repeat=3)),'missing triple coverage')
    return stats

def verify_case(d,parent_family=None):
    try:return _verify_case(d,parent_family)
    except (KeyError,IndexError,TypeError,ZeroDivisionError) as exc:raise ValueError('malformed certificate: '+str(exc)) from exc

@lru_cache(None)
def canonical_order(p,V):
    def rec(v):
        children=[w for w in V if w and p[w]==v]
        children.sort(key=lambda w:(subcode(w),w))
        return [v]+[u for w in children for u in rec(w)]
    def subcode(v):return '('+''.join(sorted(subcode(w) for w in V if w and p[w]==v))+')'
    return tuple(rec(0))

def parent_families():
    path=Path(__file__).resolve().parent.parent/'v16.22-response-selection-closure/evidence/certificates.json.xz'
    raw=lzma.decompress(path.read_bytes());require(hashlib.sha256(raw).hexdigest()==PHASH,'parent certificate hash mismatch')
    old=json.loads(raw);trees=[parents(p) for p in old['parents']];lookup={shape_code(p):i for i,p in enumerate(trees)}
    off=[];total=0
    for p in trees:off.append(total);total+=(len(p)-1)**2
    basis=[sp.Matrix([rational(z) for z in b]) for b in old['basis']]
    V=sp.Matrix.hstack(*basis);rows=old['rows'];A=sp.zeros(len(rows),total)
    for i,row in enumerate(rows):
        for j,z in row:A[i,j]=rational(z)
    require(V.rows==total and V.rank()==V.cols and A*V==sp.zeros(A.rows,V.cols),'invalid parent solution basis')
    require(A.rank()+V.cols==total,'incomplete parent solution space')
    out=[]
    for vector in basis:
        cache={}
        def getT(p,Y,vec=vector,cache=cache):
            k=(p,Y)
            if k not in cache:
                order=canonical_order(p,Y);code=shape_code(p,Y);i=lookup[code];m=len(Y)-1
                M=sp.Matrix(m,m,list(vec[off[i]:off[i]+m*m]));yn=[v for v in Y if v];C=sp.zeros(m)
                for a,v in enumerate(order[1:]):C[a,yn.index(v)]=1
                cache[k]=C.T*M*C
            return cache[k]
        out.append(getT)
    return out

def witness_checks(ws):
    require(type(ws) is dict and set(ws)=={'pair','triple'},'missing required witnesses')
    result={}
    for name,expected_p,expected_views,expected_local,expected_g in [
        ('pair',[-1,0,0],[[0,1],[0,2]],[['0','1']]*2,['-1','1','1']),
        ('triple',[-1,0,0,0],[[0,1],[0,2],[0,3]],[['1','1']]*3,['-1','1','1','1'])]:
        d=ws[name];require(d=={'parents':expected_p,'views':expected_views,'local':expected_local,'signed_global':expected_g},'changed preregistered witness')
        p=parents(d['parents']);X=tuple(range(len(p)));views=[keep(p,y) for y in d['views']]
        g=tuple(rational(x) for x in d['signed_global']);xs=[tuple(rational(x) for x in y) for y in d['local']]
        for y,x in zip(views,xs):require(aggregate(p,X,y,g)==x and all(a>=0 for a in x),'invalid witness marginal')
        require(any(a<0 for a in g),'witness not negative')
        A=sp.Matrix.vstack(*(raw_maps(p,X,Y)[0] for Y in views));require(A.rank()==len(X),'nonunique global witness')
        total=int(sum(xs[0]));possible=masses(len(X),total)
        require(not any(all(aggregate(p,X,Y,z)==x for Y,x in zip(views,xs)) for z in possible),'positive global witness exists')
        pairwise=True
        for i in range(len(views)):
            for j in range(i):
                U=tuple(sorted(set(views[i])|set(views[j])))
                exists=any(aggregate(p,U,views[i],z)==xs[i] and aggregate(p,U,views[j],z)==xs[j] for z in masses(len(U),total))
                pairwise=pairwise and exists
        require(pairwise==(name=='triple'),'incorrect pairwise-positive distinction')
        result[name]={'unique_signed_global':[str(x) for x in g],'positive_global_exists':False,'all_pairs_positive_gluable':pairwise}
    return result

def verify_all(d):
    require(type(d) is dict and d['version']=='16.23' and d['genesis']==GENESIS and d['scalar']=='formal-rational-sources','invalid campaign identity')
    require(type(d['max_vertices']) is int and d['max_vertices']==5 and d['historical'] is True and d['parent_raw_sha256']==PHASH,'not complete frozen universe')
    shapes=independent_shapes(5);hist=((-1,0,0,1,1,2,2),(-1,0,1,1,2,2),(-1,0,0,0,2,2,3),(-1,0,0,1,3,2,5))
    expected={(tag,var) for tag in ['U1:'+x for x in shapes]+['U2:'+str(i+1) for i in range(4)] for var in ('original','relabeled')}
    seen=set();summary={};totals={};family=parent_families()
    for c in d['instances']:
        ident=(c['tag'],c['variant']);require(ident in expected and ident not in seen,'missing/duplicate/wrong instance');seen.add(ident)
        p=parents(c['parents']);code=shape_code(p)
        if c['tag'].startswith('U1:'):require(code==c['tag'][3:] and code in shapes,'wrong shape instance')
        else:require(code==shape_code(hist[int(c['tag'][3:])-1]),'changed inherited fixture')
        counts=verify_case(c,family if c['tag'].startswith('U1:') else None)
        print('verified',c['tag'],c['variant'],counts,flush=True);summary[c['tag']+'|'+c['variant']]=counts
        for k,v in counts.items():totals[k]=totals.get(k,0)+v
    require(seen==expected,'incomplete instance coverage')
    for tag,_ in expected:require(summary[tag+'|original']==summary[tag+'|relabeled'],'relabel/storage metamorphism changed result')
    witnesses=witness_checks(d['witnesses'])
    return {'version':'16.23','execution_status':'COMPLETED','input_validity':'VALID','proof_status':'bounded exact certificates; general arguments O1-O7','scope':'shared finite prefix trees; formal signed and nonnegative rational diagnostics',
      'instances':len(seen),'shape_counts':{str(n):sum(len(c)==2*n for c in shapes) for n in range(1,6)},'totals':totals,'by_instance':summary,
      'parent_comparison_dimension_preserved':len(family),'witnesses':witnesses,'checks_executed':CHECKS}

if __name__=='__main__':
    p=Path(__file__).resolve().parent/'evidence';raw=lzma.decompress((p/'certificates.json.xz').read_bytes());r=verify_all(json.loads(raw));r['raw_sha256']=hashlib.sha256(raw).hexdigest()
    (p/'VERIFICATION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='by_instance'},sort_keys=True))
