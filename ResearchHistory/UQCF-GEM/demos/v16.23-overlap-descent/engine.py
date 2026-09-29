"""v16.23 producer: actual source fibers and quotient-response gluing.

No physical model is fitted. The verifier does not import this module.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import lzma
import sympy as sp

GENESIS='v1623-fixed-genesis'
PARENT_HASH='59c2c2f6d1091e7102e51932ed4ee7827668d12db7f1b08ffb0724791c8df713'
HISTORICAL=((-1,0,0,1,1,2,2),(-1,0,1,1,2,2),(-1,0,0,0,2,2,3),(-1,0,0,1,3,2,5))

def validate(p):
    if type(p) not in (tuple,list) or not p or any(type(x) is not int for x in p) or p[0]!=-1:
        raise ValueError('exact rooted parent array required')
    for v in range(1,len(p)):
        seen=set();u=v
        while u:
            if u in seen or not 0<=u<len(p):raise ValueError('cycle or missing ancestor')
            seen.add(u);u=p[u]
            if not 0<=u<len(p):raise ValueError('missing ancestor')
    return tuple(p)

def retained(p,ys):
    p=validate(p)
    if type(ys) not in (list,tuple) or not ys or any(type(v) is not int for v in ys):
        raise ValueError('exact retained identities required')
    ys=tuple(ys)
    if len(set(ys))!=len(ys) or 0 not in ys or any(not 0<=v<len(p) for v in ys):raise ValueError('illegal retained set')
    if any(p[v] not in ys for v in ys if v):raise ValueError('missing retained ancestor')
    return ys

def scalars(x,n):
    if type(x) not in (list,tuple) or len(x)!=n:raise ValueError('source length mismatch')
    if any(type(v) not in (int,str,F) for v in x):raise ValueError('exact source coefficients required')
    try:return tuple(F(v) for v in x)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc

@lru_cache(None)
def ancestors(p,v):
    out=[v]
    while v:v=p[v];out.append(v)
    return tuple(out)

def push(p,X,Y,values):
    p=validate(p);X=retained(p,X);Y=retained(p,Y);x=scalars(values,len(X))
    if not set(Y)<=set(X):raise ValueError('incompatible pruning endpoints')
    out={y:F(0) for y in Y}
    for v,a in zip(X,x):
        candidates=[z for z in ancestors(p,v) if z in out]
        w=max(candidates,key=lambda z:len(ancestors(p,z)));out[w]+=a
    return tuple(out[y] for y in Y)

def glue(p,Y,Z,y,z,positive=False):
    p=validate(p);Y=retained(p,Y);Z=retained(p,Z);y=scalars(y,len(Y));z=scalars(z,len(Z))
    if positive and any(a<0 for a in y+z):raise ValueError('nonnegative local source required')
    U=tuple(sorted(set(Y)|set(Z)));J=tuple(sorted(set(Y)&set(Z)))
    c=push(p,Y,J,y)
    if c!=push(p,Z,J,z):raise ValueError('incompatible overlap sources')
    yy=dict(zip(Y,y));zz=dict(zip(Z,z));cc=dict(zip(J,c))
    out=tuple(yy.get(v,0)+zz.get(v,0)-cc.get(v,0) for v in U)
    if positive and any(a<0 for a in out):raise ValueError('no nonnegative global source')
    return out

def glue_many(p,views,values,positive=False):
    p=validate(p)
    if not views or len(views)!=len(values):raise ValueError('nonempty matched cover required')
    current=retained(p,views[0]);x=scalars(values[0],len(current))
    if positive and any(a<0 for a in x):raise ValueError('nonnegative local source required')
    for V,y in zip(views[1:],values[1:]):
        V=retained(p,V);y=scalars(y,len(V))
        if positive and any(a<0 for a in y):raise ValueError('nonnegative local source required')
        x=glue(p,current,V,x,y);current=tuple(sorted(set(current)|set(V)))
    if positive and any(a<0 for a in x):raise ValueError('no nonnegative global source')
    return x

def glue_response(p,Y,Z,y,z):
    p=validate(p);Y=retained(p,Y);Z=retained(p,Z);y=scalars(y,len(Y));z=scalars(z,len(Z))
    yy={v:a-y[Y.index(0)] for v,a in zip(Y,y)};zz={v:a-z[Z.index(0)] for v,a in zip(Z,z)}
    if any(yy[v]!=zz[v] for v in set(Y)&set(Z)):raise ValueError('incompatible response classes')
    return tuple(yy[v] if v in yy else zz[v] for v in sorted(set(Y)|set(Z)))

def code(p):
    p=validate(p)
    def rec(v):return '('+''.join(sorted(rec(w) for w in range(1,len(p)) if p[w]==v))+')'
    return rec(0)

def parse_code(c):
    stack=[];p=[]
    for t in c:
        if t=='(':p.append(stack[-1] if stack else -1);stack.append(len(p)-1)
        else:stack.pop()
    return tuple(p)

def shapes(limit):
    if type(limit) is not int or not 1<=limit<=5:raise ValueError('preregistered size bound')
    out=set()
    for n in range(1,limit+1):
        for par in product(*(range(i) for i in range(1,n))):out.add(code((-1,)+par))
    return [parse_code(c) for c in sorted(out,key=lambda c:(len(c),c))]

def subsets(p,reverse=False):
    out=[]
    for mask in range(1<<(len(p)-1)):
        V=(0,)+tuple(v for v in range(1,len(p)) if mask&(1<<(v-1)))
        if all(p[v] in V for v in V if v):out.append(V if not reverse else (0,)+tuple(reversed(V[1:])))
    return out

@lru_cache(None)
def maps(p,X,Y):
    X=retained(p,X);Y=retained(p,Y)
    if not set(Y)<=set(X):raise ValueError('incompatible pruning endpoints')
    n,m=len(X),len(Y);P=sp.zeros(m,n);I=sp.zeros(n,m)
    xx=[v for v in X if v];yy=[v for v in Y if v];R=sp.zeros(m-1,n-1);H=sp.zeros(n-1,m-1)
    for j,v in enumerate(X):
        a=max((u for u in ancestors(p,v) if u in Y),key=lambda u:len(ancestors(p,u)))
        P[Y.index(a),j]=1
    for j,v in enumerate(Y):I[X.index(v),j]=1
    for j,v in enumerate(yy):R[j,xx.index(v)]=1
    for j,v in enumerate(xx):
        a=max((u for u in ancestors(p,v) if u in Y),key=lambda u:len(ancestors(p,u)))
        if a:H[j,yy.index(a)]=1
    return P,I,R,H

def encode(M):return {'rows':M.rows,'cols':M.cols,'data':[str(a) for a in M]}

@lru_cache(None)
def compositions(n,total):
    if n==1:return ((total,),)
    return tuple((i,)+r for i in range(total+1) for r in compositions(n-1,total-i))

def cone_summary(p,Y,Z,U,J):
    compatible=good=bad=0;witness=None
    for total in range(3):
        ys=compositions(len(Y),total);zs=compositions(len(Z),total)
        target={}
        for z in zs:target.setdefault(push(p,Z,J,z),[]).append(z)
        for y in ys:
            c=push(p,Y,J,y)
            for z in target.get(c,[]):
                compatible+=1;raw=glue(p,Y,Z,y,z);by=dict(zip(sorted(U),raw));g=tuple(by[u] for u in U)
                if all(a>=0 for a in g):good+=1
                else:
                    bad+=1
                    if witness is None:witness={'y':[str(a) for a in y],'z':[str(a) for a in z],'global':[str(a) for a in g]}
    return {'compatible':compatible,'gluable':good,'obstructed':bad,'witness':witness}

def case(p,tag,reverse=False):
    p=validate(p);ks=subsets(p,reverse);lookup={frozenset(k):i for i,k in enumerate(ks)};pairs=[]
    for yi,Y in enumerate(ks):
        for zi,Z in enumerate(ks):
            ui=lookup[frozenset(Y)|frozenset(Z)];ji=lookup[frozenset(Y)&frozenset(Z)];U,J=ks[ui],ks[ji]
            pY,iY,rY,hY=maps(p,U,Y);pZ,iZ,rZ,hZ=maps(p,U,Z)
            pyj,_,ryj,_=maps(p,Y,J);pzj,_,rzj,_=maps(p,Z,J);_,iJ,_,hJ=maps(p,U,J)
            source={'A':encode(pY.col_join(pZ)),'D':encode(pyj.row_join(-pzj)),'B':encode((iY-iJ*pyj).row_join(iZ))}
            response={'A':encode(rY.col_join(rZ)),'D':encode(ryj.row_join(-rzj)),'B':encode((hY-hJ*ryj).row_join(hZ))}
            pairs.append({'views':[yi,zi],'union':ui,'overlap':ji,'genesis':GENESIS,'source':source,'response':response,'positive':cone_summary(p,Y,Z,U,J)})
    return {'tag':tag,'genesis':GENESIS,'parents':list(p),'keeps':[list(k) for k in ks],'pairs':pairs,'triples':[list(k) for k in product(range(len(ks)),repeat=3)]}

def relabel(p):
    n=len(p);perm=(0,)+tuple(reversed(range(1,n)));out=[-1]*n
    for v in range(1,n):out[perm[v]]=perm[p[v]]
    return tuple(out)

def produce(limit=5,historical=True):
    trees=[('U1:'+code(p),p) for p in shapes(limit)]
    if historical:trees += [('U2:'+str(i+1),p) for i,p in enumerate(HISTORICAL)]
    instances=[]
    for tag,p in trees:
        for variant,q,reverse in [('original',p,False),('relabeled',relabel(p),True)]:
            print('produce',tag,variant,flush=True);d=case(q,tag,reverse);d['variant']=variant;instances.append(d)
    return {'version':'16.23','genesis':GENESIS,'scalar':'formal-rational-sources','max_vertices':limit,'historical':historical,'parent_raw_sha256':PARENT_HASH,'instances':instances,
      'witnesses':{'pair':{'parents':[-1,0,0],'views':[[0,1],[0,2]],'local':[['0','1'],['0','1']],'signed_global':['-1','1','1']},
                   'triple':{'parents':[-1,0,0,0],'views':[[0,1],[0,2],[0,3]],'local':[['1','1'],['1','1'],['1','1']],'signed_global':['-1','1','1','1']}}}

if __name__=='__main__':
    out=produce();e=Path(__file__).resolve().parent/'evidence';e.mkdir(exist_ok=True)
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();(e/'certificates.json.xz').write_bytes(lzma.compress(raw))
    info={'instances':len(out['instances']),'pairs':sum(len(c['pairs']) for c in out['instances']),'triples':sum(len(c['triples']) for c in out['instances']),'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest()}
    (e/'PRODUCTION.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))
