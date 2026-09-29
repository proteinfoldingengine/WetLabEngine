"""v16.22 producer: unrestricted root-coordinate response matrices.

No diagonal/symmetric ansatz is imposed on the unknown matrices. Production
uses ancestor-first tree enumeration and exact sparse linear elimination.
"""
from itertools import product, permutations
from pathlib import Path
from math import gcd
import hashlib
import json
import lzma
import sympy as sp


def validate(p):
    if not isinstance(p,(tuple,list)) or not p or p[0] != -1:
        raise ValueError('rooted parent array required')
    if any(type(v) is not int for v in p):
        raise ValueError('integer parent identifiers required')
    for v in range(1,len(p)):
        seen=set(); u=v
        while u:
            if u in seen or not 0 <= u < len(p):
                raise ValueError('cycle or missing ancestor')
            seen.add(u); u=p[u]
            if not 0 <= u < len(p):
                raise ValueError('missing ancestor')
    return tuple(p)


def shape_code(p):
    p=validate(p)
    def visit(v):
        return '('+''.join(sorted(visit(w) for w in range(1,len(p)) if p[w]==v))+')'
    return visit(0)


def from_code(code):
    stack=[]; p=[]
    for token in code:
        if token=='(':
            p.append(stack[-1] if stack else -1); stack.append(len(p)-1)
        else:
            stack.pop()
    return tuple(p)


def shapes(limit):
    if type(limit) is not int or not 1 <= limit <= 5:
        raise ValueError('preregistered bound is 1..5')
    codes=set()
    for n in range(1,limit+1):
        for parents in product(*(range(i) for i in range(1,n))):
            codes.add(shape_code((-1,)+parents))
    return [from_code(c) for c in sorted(codes,key=lambda x:(len(x),x))]


def embeddings(trees):
    by_code={shape_code(p):i for i,p in enumerate(trees)}; out=[]
    for xi,p in enumerate(trees):
        for mask in range(1 << (len(p)-1)):
            keep=(0,)+tuple(v for v in range(1,len(p)) if mask & (1 << (v-1)))
            if any(p[v] not in keep for v in keep if v):
                continue
            sub=(-1,)+tuple(keep.index(p[v]) for v in keep[1:])
            yi=by_code[shape_code(sub)]; q=trees[yi]
            for perm in permutations(keep[1:]):
                f=(0,)+perm
                if all(p[f[v]]==f[q[v]] for v in range(1,len(q))):
                    out.append({'fine':xi,'coarse':yi,'embedding':list(f)})
    return sorted(out,key=lambda a:(a['fine'],a['coarse'],a['embedding']))


def maps(p,q,f):
    p=validate(p); q=validate(q); f=tuple(f)
    if (len(f)!=len(q) or not f or f[0]!=0 or
        any(type(v) is not int or not 0 <= v < len(p) for v in f) or
        len(set(f))!=len(f) or any(p[f[v]]!=f[q[v]] for v in range(1,len(q)))):
        raise ValueError('illegal retained embedding')
    n,m=len(p)-1,len(q)-1; loc={v:i for i,v in enumerate(f)}
    P=sp.zeros(m,n); I=sp.zeros(n,m); R=sp.zeros(m,n); H=sp.zeros(n,m)
    for v in range(1,len(p)):
        prefixes=[]; u=v
        while True:
            if u in loc: prefixes.append(u)
            if u==0: break
            u=p[u]
        ancestor=prefixes[0]; a=loc[ancestor]
        if a: P[a-1,v-1]=1; H[v-1,a-1]=1
    for a,v in enumerate(f[1:],1):
        I[v-1,a-1]=1; R[a-1,v-1]=1
    return P,I,R,H


def offsets(trees):
    out=[]; n=0
    for p in trees: out.append(n); n+=(len(p)-1)**2
    return out,n


def constraint_rows(trees,arrows):
    off,nv=offsets(trees); unique=set()
    def variable(t,i,j): return off[t]+(len(trees[t])-1)*i+j
    def save(row):
        row={k:int(v) for k,v in row.items() if v}
        if not row: return
        divisor=0
        for z in row.values(): divisor=gcd(divisor,abs(z))
        sign=1 if row[min(row)]>0 else -1
        unique.add(tuple((k,v*sign//divisor) for k,v in sorted(row.items())))
    def add(row,k,v): row[k]=row.get(k,0)+v
    for a in arrows:
        x,y=a['fine'],a['coarse']; n,m=len(trees[x])-1,len(trees[y])-1
        P,I,R,H=maps(trees[x],trees[y],a['embedding'])
        for i in range(m):
            for j in range(n):
                row={}
                for k in range(n): add(row,variable(x,k,j),R[i,k])
                for k in range(m): add(row,variable(y,i,k),-P[k,j])
                save(row)
        for i in range(n):
            for j in range(m):
                row={}
                for k in range(n): add(row,variable(x,i,k),I[k,j])
                for k in range(m): add(row,variable(y,k,j),-H[i,k])
                save(row)
    return sorted(unique)


def root_laplacian(p):
    p=validate(p); L=sp.zeros(len(p))
    for v in range(1,len(p)):
        u=p[v]; L[v,v]+=1; L[u,u]+=1; L[v,u]-=1; L[u,v]-=1
    return L[1:,1:]


def candidate(p,use_depth=False):
    p=validate(p); paths=[]; depths={0:0}
    for v in range(1,len(p)):
        path=[]; u=v
        while u: path.append(u); u=p[u]
        paths.append(set(path)); depths[v]=len(path)
    return sp.Matrix(len(p)-1,len(p)-1,
        lambda i,j:sum(depths[v] if use_depth else 1 for v in paths[i] & paths[j]))


def encode(m): return [[str(m[i,j]) for j in range(m.cols)] for i in range(m.rows)]


def produce(limit=5):
    trees=shapes(limit); arrows=embeddings(trees); off,nv=offsets(trees)
    rows=constraint_rows(trees,arrows)
    A=sp.SparseMatrix(len(rows),nv,{(i,j):v for i,row in enumerate(rows) for j,v in row})
    ns=A.nullspace()
    green=[root_laplacian(p).inv() if len(p)>1 else sp.zeros(0) for p in trees]
    return {
        'version':'16.22','scalar':'Q-formal-signed-diagnostic','genesis':'v1622-fixed-genesis',
        'max_vertices':limit,'parents':[list(p) for p in trees],'arrows':arrows,
        'rows':[[[i,str(v)] for i,v in row] for row in rows],
        'basis':[[str(z) for z in b] for b in ns],
        'green':[encode(m) for m in green],
        'families':{'unit':[encode(candidate(p)) for p in trees],
                    'depth':[encode(candidate(p,True)) for p in trees]},
        'stats':{'objects':len(trees),'arrows':len(arrows),'unknowns':nv,
                 'constraints':len(rows),'rank':nv-len(ns),'nullity':len(ns)}}


if __name__=='__main__':
    out=produce(); e=Path(__file__).resolve().parent/'evidence'; e.mkdir(exist_ok=True)
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
    (e/'certificates.json.xz').write_bytes(lzma.compress(raw))
    (e/'PRODUCTION.json').write_text(json.dumps({'stats':out['stats'],
        'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw)},indent=2)+'\n')
    print(json.dumps(out['stats'],sort_keys=True))
