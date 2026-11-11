import itertools, sys
from functools import lru_cache
def trees(n):
    # parent arrays with parent[i] < i (labelled, increasing) -> covers all unlabelled rooted trees up to relabel
    for par in itertools.product(*[range(i) for i in range(1,n)]):
        yield (None,)+par
def anc_closed(X, par):
    return all(par[v] in X for v in X if v!=0)
def sequences(X, par):
    # all sequences of nonempty removals keeping prefix-closed, root kept, ending anywhere (we take maximal-length? take all prefixes implicitly)
    yield []
    Xl=sorted(X)
    cand=[v for v in Xl if v!=0]
    for k in range(1,len(cand)+1):
        for R in itertools.combinations(cand,k):
            Y=X-set(R)
            if anc_closed(Y,par):
                for rest in sequences(frozenset(Y),par):
                    yield [frozenset(R)]+rest
def run(n):
    stats=dict(cases=0,inv=0,mismatch=0); ex=[]
    for par in trees(n):
        X0=frozenset(range(n))
        for seq in sequences(X0,par):
            if not seq: continue
            # levels
            Xs=[X0]
            for R in seq: Xs.append(Xs[-1]-R)
            def r(v,Y):
                while v not in Y: v=par[v]
                return v
            m=len(seq)
            F=[{t:frozenset(z for z in X0 if r(z,Xs[j])==t) for t in Xs[j]} for j in range(m+1)]
            pis=[frozenset(F[j].values()) for j in range(m+1)]
            # shells partition S_j
            S=[]
            for j in range(m+1):
                blocks=[]
                for t in Xs[j]:
                    blocks.append(frozenset([t]))
                    for l in range(1,j+1):
                        if t in Xs[l]:
                            A=F[l][t]-F[l-1][t]
                            if A: blocks.append(A)
                S.append(frozenset(blocks))
            G=[]
            for p in itertools.permutations(range(n)):
                if all(frozenset(frozenset(p[z] for z in b) for b in pi)==pi for pi in pis): G.append(p)
            inv=all(frozenset(frozenset(p[z] for z in b) for b in Sj)==Sj for p in G for Sj in S)
            if inv:
                stats['cases']+=1; stats['inv']+=1; continue
            def join(parts):
                par_={z:z for z in range(n)}
                def f(a):
                    while par_[a]!=a: a=par_[a]
                    return a
                for P in parts:
                    for b in P:
                        b=sorted(b)
                        for z in b[1:]: par_[f(z)]=f(b[0])
                cl={}
                for z in range(n): cl.setdefault(f(z),set()).add(z)
                return frozenset(frozenset(c) for c in cl.values())
            core=[join([frozenset(frozenset(p[z] for z in b) for b in Sj) for p in G]) for Sj in S]
            finer=any(len(core[j])>len(pis[j]) for j in range(m+1))
            dec=all(all(any(b<=c for c in core[j-1]) for b in core[j]) for j in range(1,m+1))
            # core_j coarsens core_{j-1}?  each block of core_{j-1} inside a block of core_j
            dec=all(all(any(b<=c for c in core[j]) for b in core[j-1]) for j in range(1,m+1))
            clos=dec
            for j in range(1,m+1):
                kept=[b for b in core[j-1] if b in core[j]]
                atoms=set()
                for F_ in pis[j]:
                    rest=set(F_)
                    for b in kept:
                        if b<=F_: atoms.add(b); rest-=b
                    if rest: atoms.add(frozenset(rest))
                if frozenset(atoms)!=core[j]: clos=False
            stats['cases']+=1
            k='fail_finer%s_closure%s'%(finer,clos); stats[k]=stats.get(k,0)+1
            if not clos and len(ex)<3: ex.append((par,[sorted(R) for R in seq],[sorted(map(sorted,c)) for c in core]))
            continue
            # canonical leveled dendrogram form of block B at level l
            def canon(B,l):
                if l==0: return ('L',)
                kids=sorted(canon(c,l-1) for c in pis[l-1] if c<=B)
                return (l,tuple(kids))
            bad=False
            for j in range(1,m+1):
                for t in Xs[j]:
                    rem=[s for s in seq[j-1] if r(s,Xs[j])==t]
                    for s in rem:
                        if canon(F[j-1][t],j-1)==canon(F[j-1][s],j-1):
                            if not (len(F[j-1][t])==1 and len(rem)==1): bad=True
            C = not bad
            stats['cases']+=1; stats['inv']+=inv
            if C!=inv:
                stats['mismatch']+=1
                if len(ex)<5: ex.append((par,[sorted(R) for R in seq],inv,C))
    return stats,ex
for n in range(2,int(sys.argv[1])+1):
    st,ex=run(n); print(n,st)
    for e in ex: print('  mismatch',e)
