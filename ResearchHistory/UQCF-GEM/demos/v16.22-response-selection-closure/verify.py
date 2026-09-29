"""v16.22 independent verifier.

Does not import the producer or its enumeration/elimination. It enumerates
Pruefer trees and retained injections; edge-coordinate equality constraints
are solved by disjoint sets, then checked against arbitrary supplied root-
coordinate generators and the unchanged reference inverse.
"""
from itertools import product, permutations
from pathlib import Path
from functools import lru_cache
from math import gcd
import copy
import hashlib
import json
import lzma
import re
import sympy as sp


class VerificationError(ValueError): pass


def require(ok,message):
    if not ok: raise VerificationError(message)


def rational(z):
    require(type(z) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?',z) is not None,
            'invalid exact rational representation')
    return sp.Rational(z)


def matrix(data):
    require(type(data) is list,'matrix must be a list')
    if not data: return sp.zeros(0)
    require(all(type(r) is list and len(r)==len(data[0]) for r in data),'ragged matrix')
    return sp.Matrix([[rational(z) for z in r] for r in data])


@lru_cache(None)
def _independent_shapes(limit):
    require(type(limit) is int and 1<=limit<=5,'invalid enumeration bound')
    codes=set()
    for n in range(1,limit+1):
        for word in product(range(n),repeat=max(0,n-2)):
            neighbors=[set() for _ in range(n)]
            if n>1:
                degree=[1]*n
                for x in word: degree[x]+=1
                for x in word:
                    leaf=next(i for i,d in enumerate(degree) if d==1)
                    neighbors[leaf].add(x);neighbors[x].add(leaf)
                    degree[leaf]-=1;degree[x]-=1
                last=[i for i,d in enumerate(degree) if d==1]
                u,v=last;neighbors[u].add(v);neighbors[v].add(u)
            def encode(v,parent):
                return '('+''.join(sorted(encode(w,v) for w in neighbors[v] if w!=parent))+')'
            codes.add(encode(0,-1))
    def parents(code):
        stack=[]; out=[]
        for c in code:
            if c=='(':
                out.append(stack[-1] if stack else -1);stack.append(len(out)-1)
            else: stack.pop()
        return tuple(out)
    return tuple(parents(c) for c in sorted(codes,key=lambda z:(len(z),z)))


def independent_shapes(limit): return list(_independent_shapes(limit))


@lru_cache(None)
def _arrows(trees):
    result=[]
    for x,p in enumerate(trees):
        for y,q in enumerate(trees):
            if len(q)>len(p): continue
            for rest in permutations(range(1,len(p)),len(q)-1):
                f=(0,)+rest
                if all(p[f[v]]==f[q[v]] for v in range(1,len(q))):
                    result.append((x,y,f))
    return tuple(sorted(result))


@lru_cache(None)
def arrows_maps(trees,arrow):
    x,y,f=arrow;p,q=trees[x],trees[y];n,m=len(p)-1,len(q)-1
    require(len(f)==len(q) and f[0]==0 and len(set(f))==len(f),'invalid embedding')
    location={v:i for i,v in enumerate(f)}
    # Parent stepping, independently of longest-prefix construction.
    P=sp.zeros(m,n);I=sp.zeros(n,m);R=sp.zeros(m,n);H=sp.zeros(n,m)
    for v in range(1,len(p)):
        u=v
        while u not in location:u=p[u]
        a=location[u]
        if a:P[a-1,v-1]=1;H[v-1,a-1]=1
    for a in range(1,len(q)):
        I[f[a]-1,a-1]=1;R[a-1,f[a]-1]=1
    return P,I,R,H


def offset_table(trees):
    out=[];total=0
    for p in trees:out.append(total);total+=(len(p)-1)**2
    return out,total


def required_rows(trees):
    off,nv=offset_table(trees);out=set()
    def index(t,i,j):return off[t]+(len(trees[t])-1)*i+j
    def store(terms):
        row={}
        for k,v in terms:row[k]=row.get(k,0)+int(v)
        row={k:v for k,v in row.items() if v}
        if not row:return
        g=0
        for v in row.values():g=gcd(g,abs(v))
        g*=1 if row[min(row)]>0 else -1
        out.add(tuple((k,str(v//g)) for k,v in sorted(row.items())))
    for a in _arrows(trees):
        x,y,_=a;n,m=len(trees[x])-1,len(trees[y])-1
        P,I,R,H=arrows_maps(trees,a)
        for i,j in product(range(m),range(n)):
            store([(index(x,k,j),R[i,k]) for k in range(n)]+
                  [(index(y,i,k),-P[k,j]) for k in range(m)])
        for i,j in product(range(n),range(m)):
            store([(index(x,i,k),I[k,j]) for k in range(n)]+
                  [(index(y,k,j),-H[i,k]) for k in range(m)])
    return out


def edge_solution_classes(trees):
    off,nv=offset_table(trees);parent=list(range(nv+1));zero=nv
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    def idx(t,i,j):return off[t]+(len(trees[t])-1)*i+j
    # Build constraints for ALL edge-matrix entries; no diagonal ansatz.
    for x,y,f in _arrows(trees):
        n,m=len(trees[x])-1,len(trees[y])-1;inv={v:i for i,v in enumerate(f)}
        for i,j in product(range(1,m+1),range(1,n+1)):
            union(idx(x,f[i]-1,j-1),idx(y,i-1,inv[j]-1) if j in inv else zero)
        for i,j in product(range(1,n+1),range(1,m+1)):
            union(idx(x,i-1,f[j]-1),idx(y,inv[i]-1,j-1) if i in inv else zero)
    groups={}
    for i in range(nv):groups.setdefault(find(i),[]).append(i)
    z=find(zero)
    return [g for k,g in groups.items() if k!=z],groups.get(z,[])


def edge_divergence(p):
    n=len(p)-1;B=sp.zeros(n)
    for v in range(1,len(p)):
        B[v-1,v-1]=1
        if p[v]:B[p[v]-1,v-1]=-1
    return B


def decode_family(c,family):
    require(type(family) is list and len(family)==len(c['parents']),'family coverage')
    mats=[matrix(m) for m in family]
    for p,M in zip(c['parents'],mats):require(M.shape==(len(p)-1,len(p)-1),'family matrix type')
    return mats


def check_family(c,family):
    trees=tuple(tuple(p) for p in c['parents']);mats=decode_family(c,family);count=0
    for a in _arrows(trees):
        x,y,_=a;P,I,R,H=arrows_maps(trees,a)
        require(R*mats[x]==mats[y]*P,'restriction comparison diagram failed')
        require(mats[x]*I==H*mats[y],'inclusion comparison diagram failed')
        count+=2
    return count


def check_coordinate_changes(c):
    trees=tuple(tuple(p) for p in c['parents']);count=0;U=[];V=[]
    for p in trees:
        n=len(p)-1;u=sp.eye(n);v=sp.eye(n)
        if n>1:u[0,n-1]=1;v[n-1,0]=2
        U.append(u);V.append(v)
    for family in c['families'].values():
        mats=decode_family(c,family);changed=[v.inv()*a*u for a,u,v in zip(mats,U,V)]
        for arrow in _arrows(trees):
            x,y,_=arrow;P,I,R,H=arrows_maps(trees,arrow)
            pp=U[y].inv()*P*U[x];ii=U[x].inv()*I*U[y]
            rr=V[y].inv()*R*V[x];hh=V[x].inv()*H*V[y]
            require(rr*changed[x]==changed[y]*pp,'coordinate-changed restriction failed')
            require(changed[x]*ii==hh*changed[y],'coordinate-changed inclusion failed')
            count+=2
    return count


def verify(c):
    required={'version','scalar','genesis','max_vertices','parents','arrows','rows','basis','green','families','stats'}
    require(type(c) is dict and set(c)==required,'missing or extra certificate field');checks=1
    require(c['version']=='16.22' and c['scalar']=='Q-formal-signed-diagnostic','version/scalar mismatch')
    require(c['genesis']=='v1622-fixed-genesis','foreign Genesis domain');checks+=2
    require(type(c['parents']) is list and all(type(p) is list and p and all(type(v) is int for v in p) for p in c['parents']),
            'parent identifiers must be exact integers, not Boolean or floating values');checks+=1
    trees=tuple(independent_shapes(c['max_vertices']))
    require(c['parents']==[list(p) for p in trees],'object coverage or parent-array mismatch');checks+=1
    expected=_arrows(trees);actual=[]
    require(type(c['arrows']) is list,'arrow collection type')
    for a in c['arrows']:
        require(type(a) is dict and set(a)=={'fine','coarse','embedding'},'arrow type')
        require(type(a['fine']) is int and type(a['coarse']) is int and type(a['embedding']) is list
                and all(type(v) is int for v in a['embedding']),'invalid arrow scalar')
        actual.append((a['fine'],a['coarse'],tuple(a['embedding'])))
    require(len(actual)==len(set(actual)) and set(actual)==set(expected),'incomplete or illegal embedding coverage');checks+=1
    rr=[]
    require(type(c['rows']) is list,'constraint collection type')
    for row in c['rows']:
        require(type(row) is list and all(type(e) is list and len(e)==2 and type(e[0]) is int for e in row),'constraint row type')
        for _,z in row:rational(z)
        rr.append(tuple((k,z) for k,z in row))
    want=required_rows(trees)
    require(len(rr)==len(set(rr)) and set(rr)==want,'incomplete or corrupted constraint coverage');checks+=1
    off,nv=offset_table(trees);groups,zero=edge_solution_classes(trees);dim=len(groups)
    st={'objects':len(trees),'arrows':len(expected),'unknowns':nv,'constraints':len(want),'rank':nv-dim,'nullity':dim}
    require(c['stats']==st and all(type(v) is int for v in c['stats'].values()),'forged constraint rank or counts');checks+=1
    require(type(c['basis']) is list and len(c['basis'])==dim,'incomplete solution basis')
    columns=[]
    for b in c['basis']:
        require(type(b) is list and len(b)==nv,'basis dimension')
        b=sp.Matrix([rational(z) for z in b]);columns.append(b)
        for row in want:
            require(sum(rational(z)*b[i] for i,z in row)==0,'generator violates a comparison constraint');checks+=1
        edge=[];family=[]
        for t,p in enumerate(trees):
            n=len(p)-1;A=sp.Matrix(n,n,list(b[off[t]:off[t]+n*n]));B=edge_divergence(p)
            edge.extend(list(B.T*A*B));family.append([[str(A[i,j]) for j in range(n)] for i in range(n)])
        require(all(edge[i]==0 for i in zero),'generator violates zero edge class')
        require(all(all(edge[i]==edge[g[0]] for i in g) for g in groups),'generator violates edge equality class');checks+=2
        checks+=check_family(c,family)
    Bspace=sp.Matrix.hstack(*columns) if columns else sp.zeros(nv,0)
    require(Bspace.rank()==dim,'dependent solution basis');checks+=1
    require(type(c['families']) is dict and set(c['families'])=={'unit','depth'},'candidate family coverage')
    for f in c['families'].values():checks+=check_family(c,f)
    green=decode_family(c,c['green']);unit=decode_family(c,c['families']['unit']);depth=decode_family(c,c['families']['depth'])
    inverse_dim=0
    for p,G,A,Dp in zip(trees,green,unit,depth):
        B=edge_divergence(p);L=B*B.T;n=len(p)-1
        require(L*G==sp.eye(n),'incorrect inverse of fixed original Laplacian')
        require(A==G,'unit candidate differs from fixed original inverse')
        edge=B.T*Dp*B
        d=[]
        for v in range(1,len(p)):
            k=0;u=v
            while u:k+=1;u=p[u]
            d.append(k)
        require(edge==sp.diag(*d) if d else edge==sp.zeros(0),'depth candidate coefficients mismatch')
        inverse_dim+=n*(n-int(L.rank()));checks+=3
    require(inverse_dim==0,'fixed inverse uniqueness rank failed');checks+=1
    # Composition of every pair of retained embeddings, with all four maps.
    aset=set(expected);by_fine={i:[] for i in range(len(trees))}
    for a in expected:by_fine[a[0]].append(a)
    composites=0
    for a in expected:
        x,y,f=a;Pa,Ia,Ra,Ha=arrows_maps(trees,a)
        for b in by_fine[y]:
            _,z,g=b;com=(x,z,tuple(f[v] for v in g))
            require(com in aset,'missing composite retained embedding')
            Pb,Ib,Rb,Hb=arrows_maps(trees,b);P,I,R,H=arrows_maps(trees,com)
            require(P==Pb*Pa and I==Ia*Ib and R==Rb*Ra and H==Ha*Hb,'composition identity failed')
            composites+=1;checks+=2
    coordinate_checks=check_coordinate_changes(c);checks+=coordinate_checks
    normdim=0
    if c['max_vertices']>=2:
        index=trees.index((-1,0));row=Bspace[off[index],:]
        normdim=dim-int(row.rank())
        require(any(row),'first-edge normalization unavailable');checks+=1
    witness=None
    if c['max_vertices']>=3:
        index=trees.index((-1,0,1));a,b=unit[index],depth[index];v=sp.Matrix([-1,1])
        require(a[0,0]==b[0,0]==1 and sp.Matrix.hstack(sp.Matrix(list(a)),sp.Matrix(list(b))).rank()==2,
                'nonproportionality witness failed')
        require(a*v!=b*v,'actual witness response distinction failed');checks+=2
        witness={'parents':[-1,0,1],'source_nonroot':['-1','1'],
                 'unit_root_zero':[str(z) for z in a*v],'depth_root_zero':[str(z) for z in b*v],
                 'same_first_edge_unit':True}
    return {'version':'16.22','execution_status':'COMPLETED','input_validity':'VALID',
            'proof_status':'bounded certificate; general arguments in PROOFS.md',
            'comparison_dimension':dim,'first_edge_normalized_dimension':normdim,
            'inverse_affine_dimension':inverse_dim,'checks_executed':checks,'stats':st,
            'composition_pairs':composites,'coordinate_checks':coordinate_checks,
            'edge_classes':[len(g) for g in groups],'forced_zero_edge_entries':len(zero),
            'witness':witness,'scope':'formal signed diagnostic, retained comparison equations versus fixed inverse definition'}


def rejecting_controls(c):
    controls=[]
    def attempt(name,mutate):
        bad=copy.deepcopy(c);mutate(bad)
        try:verify(bad)
        except VerificationError as err:
            controls.append({'defect':name,'rejected':True,'reason':str(err)})
        else:raise VerificationError('verifier accepted deliberate defect: '+name)
    attempt('false-nullity',lambda z:z['stats'].__setitem__('nullity',777))
    attempt('corrupt-kernel-generator',lambda z:z['basis'][0].__setitem__(0,str(rational(z['basis'][0][0])+1)))
    attempt('incomplete-basis',lambda z:z['basis'].pop())
    attempt('missing-embedding',lambda z:z['arrows'].pop())
    attempt('missing-constraint',lambda z:z['rows'].pop())
    i=c['parents'].index([-1,0,1])
    attempt('Boolean-parent-identifier',lambda z:z['parents'][i].__setitem__(2,True))
    attempt('floating-parent-identifier',lambda z:z['parents'][i].__setitem__(2,1.0))
    attempt('changed-fixed-inverse',lambda z:z['green'].__setitem__(i,copy.deepcopy(z['families']['depth'][i])))
    attempt('foreign-genesis',lambda z:z.__setitem__('genesis','foreign'))
    attempt('float-in-exact-certificate',lambda z:z['basis'][0].__setitem__(0,0.25))
    attempt('missing-required-field',lambda z:z.pop('rows'))
    j=c['parents'].index([-1,0,0])
    attempt('linear-but-nonnatural-sibling-selection',lambda z:z['families']['unit'].__setitem__(j,[['1','0'],['0','2']]))
    return controls


if __name__=='__main__':
    e=Path(__file__).resolve().parent/'evidence';e.mkdir(exist_ok=True)
    try:
        raw=lzma.decompress((e/'certificates.json.xz').read_bytes());c=json.loads(raw)
        r=verify(c);r['raw_sha256']=hashlib.sha256(raw).hexdigest()
        defects=rejecting_controls(c)
        (e/'rejections.json').write_text(json.dumps(defects,indent=2,sort_keys=True)+'\n')
        r['deliberate_defects_rejected']=len(defects)
        (e/'VERIFICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
        print(json.dumps(r,sort_keys=True))
    except Exception as err:
        (e/'INVALID.json').write_text(json.dumps({'execution_status':'INVALID','error':repr(err)},indent=2)+'\n')
        raise
