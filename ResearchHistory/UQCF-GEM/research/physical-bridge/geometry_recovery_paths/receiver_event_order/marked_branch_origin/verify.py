"""Reconstruct the whole semantic population and all recorded state predicates without project imports."""
import argparse
from collections import Counter
from copy import deepcopy
from itertools import combinations, permutations, product
import json
from pathlib import Path

P={'P':'Pin','Q':'Pin','X1':'P','X2':'P','A':'P','Y1':'Q','Y2':'Q','B':'Q','b1':'B','b2':'B'}
BASE=frozenset({'Pin','P','Q','A','B','b1','b2'})
SRC=frozenset({'Pin','P','Q','X1','X2','Y1','Y2'})
U=BASE|SRC
X={'X1','X2'}
Y={'Y1','Y2'}
K={v:{k for k,p in P.items() if p==v} for v in U}
q={'Pin':1,'P':2,'Q':2,'B':1}
base={'Pin':80,'P':24,'Q':28,'A':2,'B':6,'b1':2,'b2':2}
T=[base|dict.fromkeys(X,v)|dict.fromkeys(Y,9-v) for v in [1,8]]
DEP={v:0 if v=='Pin' else (1 if v in ('P','Q') else 3 if v in ('b1','b2') else 2) for v in U}
def check(q):
    if not q:raise ValueError('evidence mismatch')
def legal(a):
    return (a[0]|a[1])==U and all('Pin' in s and all(p in s for v,p in P.items() if v in s) for s in a)
def profile(a):
    return {v:1 if any(c<=s for s in a) else 2 for v,c in K.items() if c}
def grade(a,world):
    return {v:world[v]-sum(world[w] for w in K[v]&a) for v in a}
def signature(tree,grade,v='Pin'):
    return grade[v],tuple(sorted(signature(tree,grade,w) for w in K[v]&tree))
def pairwork(a,world):
    return tuple(sum(world[v]**2 for v in a[0]^a[1] if DEP[v]==d) for d in (1,2,3))
def ordered():
    for choices in product(permutations(('P','Q')),permutations(('X1','X2','A')),
                           permutations(('Y1','Y2','B')),permutations(('b1','b2'))):
        children=dict(zip(('Pin','P','Q','B'),choices))
        def preorder(v):
            yield v
            for w in children.get(v,()):yield from preorder(w)
        for rid in range(2):
            yield tuple(preorder('Pin')),rid
def verify(records):
    expected=set(ordered())
    ids=[(tuple(r['order']),r['receiver']) for r in records]
    check(len(ids)==len(expected) and set(ids)==expected)
    hist=Counter()
    for r in records:
        ns=tuple(r['order']);rid=r['receiver']
        def state(m):
            check(len(m)==2 and all(type(x) is int and 0<=x<1<<11 for x in m))
            return tuple(frozenset(ns[v] for v in range(11) if x>>v&1) for x in m)
        def equal(record):
            masks, old=record
            a=state(masks)
            check(old==[[[i,g[ns[i]]] for i in range(11) if ns[i] in a[rid]] for g in [grade(a[rid],t) for t in T]])
            sigs=tuple(signature(a[rid],grade(a[rid],t)) for t in T)
            return a,sigs
        prior=state(r['prior'])
        check(prior[rid]==BASE and prior[1-rid]==SRC and legal(prior) and profile(prior)==q)
        check(r['profile']==[q[v] for v in ns if v in q])
        steps={prior[:i]+(prior[i]^{v},)+prior[i+1:] for i,v in product(range(2),U-{'Pin'})}
        admissible={a for a in steps if legal(a)}
        shipped=[state(v) for v in r['first_legal']]
        check(set(shipped)==admissible and len(shipped)==len(admissible))
        fronts=[equal(z) for z in r['exact']]
        fexpected={a for a in admissible if profile(a)==q}
        check({v for v,_ in fronts}==fexpected and len(fronts)==len(fexpected)==4)
        check({a[rid]-BASE for a,_ in fronts}=={frozenset({v}) for v in X|Y})
        check({sig[0] for _,sig in fronts}.isdisjoint(sig[1] for _,sig in fronts))
        vals=[equal(z) for z in r['path']]
        check(vals[0][0]==prior and vals[0][1][0]==vals[0][1][1] and profile(vals[-1][0])==q)
        for (a,_),(b,_) in zip(vals,vals[1:]):
            check(legal(b) and sum(len(x^y) for x,y in zip(a,b))==1)
            check(sum(abs(x-profile(b)[v]) for v,x in q.items())<=1)
        heard=next((j for j,(_,s) in enumerate(vals) if s[0]!=s[1]),None)
        retained=vals[-1][1][0]!=vals[-1][1][1]
        f='idle' if len(vals)==1 else 'R_'+next(iter(vals[1][0][rid]-BASE))[0] if vals[1][0][rid]!=BASE else 'C_'+next(iter(vals[1][0][1-rid]-SRC))
        hist[(f,heard,retained)]+=1
    check(hist=={('R_X',1,True):104,('R_Y',1,True):104,('C_A',3,True):32,('C_B',7,True):32,('idle',None,False):16})
    copies=[BASE|frozenset(z) for x,y in product([(),('X1',),('X2',)],[(),('Y1',),('Y2',)]) for z in [x+y]]
    involution=dict(zip(('X1','X2','Y1','Y2'),('Y1','Y2','X1','X2')))
    paired=lambda a: frozenset(involution.get(v,v) for v in a)
    check(all(paired(v) in copies and pairwork((v,SRC),T[0])==pairwork((paired(v),SRC),T[1]) for v in copies))
    graph={(a,b) for a,b in product(copies,repeat=2) if len(a^b)==1}
    check(len(graph)==24 and {(paired(a),paired(b)) for a,b in graph}==graph)
    return [[list(k),v] for k,v in sorted(hist.items(),key=str)]
def rejection(records):
    attempts=[]
    attempts.append(records[1:])
    attempts.append(records+[records[0]])
    attempts.append(records[1:]+[records[1]])
    for k in range(4):
        x=deepcopy(records)
        if k==0:x[0]['path'][0][1][0][0][1]+=1
        if k==1:x[0]['exact'].pop()
        if k==2:x[0]['path'][0][0][0]^=1
        if k==3:x[0]["prior"][0]^=(1<<10)
        attempts.append(x)
    for x in attempts:
        try:verify(x)
        except (AssertionError,KeyError,IndexError,StopIteration,ValueError):continue
        raise ValueError('corruption passed')
    return len(attempts)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('raw')
    r=json.loads(Path(p.parse_args().raw).read_text())
    print(json.dumps({'history_classes':verify(r),'rejecting_controls':rejection(r),'receiver_only_states':9,'receiver_only_edges':24},sort_keys=True))
