"""Bit-mask constructions from the frozen X14/X15/X32/X33 proofs.

These produce complete paths, never a reachability/disconnection claim.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb

LIMIT=1000000
class ResourceLimit(RuntimeError):pass
def mask(row):return sum(1<<x for x in row)
def labels(bits):return [x for x in range(bits.bit_length()) if bits>>x&1]
def vertex(roots):return [labels(root) for root in roots]
def bits(roots):return tuple(mask(row) for row in roots)

@lru_cache(maxsize=10000)
def minimum_cover(k,roots):
    for size in range(k+1):
        for candidate in combinations(range(k),size):
            chosen=mask(candidate)
            if all(root&chosen for root in roots):return candidate
    raise ValueError("empty support")
def tau(k,roots):return len(minimum_cover(k,roots))

class Path:
    def __init__(self,k,floors,roots):
        self.k=k;self.floors=floors;self.roots=list(roots);self.vertices=[tuple(roots)]
    def toggle(self,i,x,add):
        bit=1<<x
        if bool(self.roots[i]&bit)==add:raise AssertionError("ineligible incidence")
        self.roots[i]^=bit
        if self.roots[i].bit_count()<self.floors[i]:raise AssertionError("original floor")
        self.vertices.append(tuple(self.roots))
        if len(self.vertices)>LIMIT:raise ResourceLimit("per-identity primitive bound")
    def replace(self,i,target):
        for x in labels(target&~self.roots[i]):self.toggle(i,x,True)
        for x in labels(self.roots[i]&~target):self.toggle(i,x,False)
    def join(self,target):
        for i in range(len(target)):
            for x in labels(target[i]&~self.roots[i]):self.toggle(i,x,True)
        for i in range(len(target)):
            for x in labels(self.roots[i]&~target[i]):self.toggle(i,x,False)
    def swap(self,i,j):
        a,b=self.roots[i],self.roots[j]
        self.replace(i,a|b);self.replace(j,a|b)
        self.replace(i,b);self.replace(j,a)
    def extend(self,vertices):
        if tuple(self.roots)!=vertices[0]:raise AssertionError("actual join mismatch")
        for state in vertices[1:]:
            changes=[(i,x) for i,(a,b) in enumerate(zip(self.roots,state)) for x in labels(a^b)]
            if len(changes)!=1:raise AssertionError("not one incidence")
            i,x=changes[0];self.toggle(i,x,bool(state[i]&(1<<x)))
    def serial(self):return [vertex(state) for state in self.vertices]

def compact(k,floors,original):
    path=Path(k,floors,original);H=minimum_cover(k,tuple(original));hm=mask(H)
    for i,root in enumerate(original):
        retained=next(mask(subset) for subset in combinations(labels(root),floors[i]) if mask(subset)&hm)
        path.replace(i,retained)
    return path,list(H)

def convert(k,floors,vertices):
    """Maximum-layer A: literal one-incidence unions between lowered vertices."""
    current=vertices;layers=[]
    if tau(k,current[0])!=4 or tau(k,current[-1])!=4:raise AssertionError("A exact endpoint domain")
    while True:
        values=[tau(k,state) for state in current];peak=max(values)
        if peak<=4:return current,layers
        lowered=[]
        for state,value in zip(current,values):
            if value==peak:
                x,y=minimum_cover(k,state)[:2]
                state=tuple(root|(1<<x) if root&(1<<y) else root for root in state)
            lowered.append(state)
        merged=Path(k,floors,lowered[0])
        for target in lowered[1:]:merged.join(target)
        after=max(tau(k,state) for state in merged.vertices)
        if after>=peak:raise AssertionError("A maximum layer failed to decrease")
        layers.append(dict(before=peak,after=after,vertices_before=len(current),vertices_after=len(merged.vertices)))
        current=merged.vertices

def degrees(k,roots):return [sum(bool(root&(1<<x)) for root in roots) for x in range(k)]

def level(k,floors,roots):
    path=Path(k,floors,roots);events=[]
    while True:
        degree=degrees(k,path.roots);donors=[x for x,d in enumerate(degree) if d>3]
        if not donors:break
        x=donors[0];y=next(y for y,d in enumerate(degree) if d<3)
        i=next(i for i,root in enumerate(path.roots) if root&(1<<x) and not root&(1<<y))
        before=sum(max(d-3,0) for d in degree);start=len(path.vertices)-1
        path.toggle(i,y,True);path.toggle(i,x,False)
        after=sum(max(d-3,0) for d in degrees(k,path.roots))
        events.append(dict(x=x,y=y,i=i,start=start,end=len(path.vertices)-1,before=before,after=after))
    return path,events

def pending(current,destination):
    return sorted((x,y,i) for i,(a,b) in enumerate(zip(current,destination)) for x,y in zip(labels(a&~b),labels(b&~a)))

def first_cycle(edges):
    adjacency={}
    for edge in edges:adjacency.setdefault(edge[0],[]).append(edge)
    def walk(start,current,visited,chosen):
        for edge in adjacency.get(current,[]):
            nxt=edge[1]
            if nxt==start:return chosen+[edge]
            if nxt not in visited:
                result=walk(start,nxt,visited|{nxt},chosen+[edge])
                if result:return result
        return None
    for start in sorted(adjacency):
        result=walk(start,start,{start},[])
        if result:return result
    raise AssertionError("balanced pending graph has no eligible cycle")

def saturated(k,floors,source,destination):
    path=Path(k,floors,source);events=[]
    while tuple(path.roots)!=tuple(destination):
        edges=pending(path.roots,destination);cycle=first_cycle(edges);start=len(path.vertices)-1
        before=len(edges)
        for x,y,i in [cycle[0]]+list(reversed(cycle[1:])):
            path.toggle(i,y,True);path.toggle(i,x,False)
        after=len(pending(path.roots,destination))
        if after!=before-len(cycle):raise AssertionError("cycle progress")
        events.append(dict(edges=[list(e) for e in cycle],start=start,end=len(path.vertices)-1,before=before,after=after))
    return path,events

def bound(k,floors):
    counts=Counter(floors)
    return sum(n*(k-h)//(n//2+1) for h,n in counts.items())

def guard(k,roots,indices):
    return all(any(not roots[i]&mask(pair) for i in indices) for pair in combinations(range(k),2))

def phi(k,roots,L,p,D):
    s=len(D);ell=len(L);denominator=comb(ell-s,p-s);value=Fraction(0)
    for pair in combinations(range(k),2):
        witness=sum(not roots[i]&mask(pair) for i in L if i not in D)
        n=ell-s-witness;j=p-s-witness
        value+=Fraction(comb(n,j) if 0<=j<=n else 0,denominator)
    return value

def select_patches(k,roots,L,p):
    D=[];value=phi(k,roots,L,p,D);steps=[dict(D=[],phi=str(value))]
    if value>=1:return None,steps
    while len(D)<p:
        chosen=next(i for i in L if i not in D and phi(k,roots,L,p,D+[i])<=value)
        D.append(chosen);value=phi(k,roots,L,p,D);steps.append(dict(D=D[:],phi=str(value)))
    if value!=0:raise AssertionError("unfinished conditional placement")
    return D,steps

def assignment(floors,U,J):
    result=[None]*len(floors)
    for h in sorted(set(floors)):
        slots=[i for i,v in enumerate(floors) if v==h]
        tokens=[i for i in U if i in slots];positions=[i for i in J if i in slots]
        for slot,token in zip(positions,tokens):result[slot]=token
        unused=[i for i in slots if i not in tokens];remaining=[i for i in slots if result[i] is None]
        for slot,token in zip(remaining,unused):result[slot]=token
    return result

def permute(k,floors,roots,desired):
    path=Path(k,floors,roots);tokens=list(range(len(roots)));events=[]
    for slot,token in enumerate(desired):
        if tokens[slot]==token:continue
        other=tokens.index(token)
        if floors[slot]!=floors[other]:raise AssertionError("mixed original floor permutation")
        start=len(path.vertices)-1;path.swap(slot,other);tokens[slot],tokens[other]=tokens[other],tokens[slot]
        events.append(dict(i=slot,j=other,start=start,end=len(path.vertices)-1))
    return path,events

def phase(path,placed,allowed,fixed):
    start=len(path.vertices)-1
    for i in sorted(allowed):path.replace(i,placed[i])
    end=len(path.vertices)-1;pair_witnesses=[]
    for state in path.vertices[start:end+1]:
        pair_witnesses.append([next(i for i in sorted(fixed) if not state[i]&mask(pair)) for pair in combinations(range(path.k),2)])
    return dict(start=start,end=end,allowed=sorted(allowed),fixed=sorted(fixed),pair_witnesses=pair_witnesses)

def good_label(k,floors,roots):
    for x in range(k):
        if all(sum(not roots[i]&(1<<x) for i,h0 in enumerate(floors) if h0==h)<=floors.count(h)//2 for h in sorted(set(floors))):
            return x,[i for i,root in enumerate(roots) if not root&(1<<x)]
    raise AssertionError("derived simultaneous label unavailable")

def native_lift(k,floors,source,parent_vertices):
    """Star specialization of fixed-root clearance, with actual child primitives."""
    parent=list(source);leaves=[[1<<x for x in labels(root)[:floor]] for root,floor in zip(source,floors)]
    vertices=[];clearances=[]
    def save():
        vertices.append(dict(parent=vertex(parent),leaves=[[labels(leaf) for leaf in children] for children in leaves]))
        if len(vertices)>LIMIT:raise ResourceLimit("native per-identity bound")
    save()
    for destination in parent_vertices[1:]:
        edits=[(i,x) for i,(a,b) in enumerate(zip(parent,destination)) for x in labels(a^b)]
        if len(edits)!=1:raise AssertionError("parent path primitive")
        i,x=edits[0];adding=bool(destination[i]&(1<<x))
        if not adding:
            active=0
            for leaf in leaves[i]:active|=leaf
            if active&(1<<x):
                y=next(y for y in labels(parent[i]) if not active&(1<<y))
                child=next(j for j,leaf in enumerate(leaves[i]) if leaf&(1<<x));start=len(vertices)-1
                leaves[i][child]|=1<<y;save();leaves[i][child]&=~(1<<x);save()
                clearances.append(dict(root=i,child=child,x=x,y=y,start=start,end=len(vertices)-1))
        parent[i]=destination[i];save()
    return dict(vertices=vertices,clearances=clearances)

def produce(case):
    k=case["k"];floors=case["floors"];A=bits(case["A"]);C=bits(case["C"])
    record=dict(identity=case["identity"],status="PATH",preliminary=[],final=[],meta={})
    def refuse(reason):record["status"]=reason;return record
    if any(root.bit_count()<floor for roots in (A,C) for root,floor in zip(roots,floors)):return refuse("INVALID_INPUT_FLOOR")
    if tau(k,A)!=4 or tau(k,C)!=4:return refuse("NONEXACT_INPUT")
    method=case.get("parent_method",case["method"])
    meta=record["meta"];meta["cover"]=list(minimum_cover(k,A));meta["upper_entry"]=[vertex(A),vertex(C)]
    if method=="boundary":
        record["preliminary"]=[vertex(A)];record["final"]=[vertex(A)];return record
    if method=="X15N":
        source,sourceevents=level(k,floors,A);destination,destevents=level(k,floors,C)
        middle,cycles=saturated(k,floors,source.roots,destination.roots)
        whole=Path(k,floors,A);whole.extend(source.vertices);whole.extend(middle.vertices);whole.extend(list(reversed(destination.vertices)))
        final,layers=convert(k,floors,whole.vertices)
        meta.update(leveling=dict(source=dict(vertices=source.serial(),events=sourceevents),destination=dict(vertices=destination.serial(),events=destevents)),cycle_path=middle.serial(),cycles=cycles,conversion=layers,progress=sourceevents+destevents+cycles)
        preliminary=whole.vertices
    elif method in ("X32","X33"):
        if method=="X33" and bound(k,floors)>=k:return refuse("SUFFICIENT_BOUND_NOT_MET")
        if method=="X33":
            source,H_A=compact(k,floors,A);destination,H_C=compact(k,floors,C)
            AA=tuple(source.roots);CC=tuple(destination.roots)
            x,I=good_label(k,floors,AA);y,U=good_label(k,floors,CC);J=[]
            for h in sorted(set(floors)):
                slots=[i for i,v in enumerate(floors) if v==h];count=sum(i in U for i in slots)
                J.extend([i for i in slots if i not in I][:count])
            extra=dict(source_label=x,destination_label=y,source_guard=I,destination_guard=U)
            meta["covers"]=[dict(vertex=vertex(A),H=H_A),dict(vertex=vertex(C),H=H_C)]
        else:
            AA=A;CC=C;source=Path(k,floors,A);destination=Path(k,floors,C)
            L=case["L"];F=case["F"];U=case["U"]
            if not guard(k,A,L) or not guard(k,C,F+U):return refuse("INVALID_GUARD_INPUT")
            J,steps=select_patches(k,A,L,len(U))
            if J is None:return refuse("SUFFICIENT_BOUND_NOT_MET")
            meta["placement"]=dict(L=L,p=len(U),steps=steps);extra={}
        # X32 keeps F tokens at their original indices. Complete the L assignment.
        if method=="X32":
            desired=list(range(len(floors)))
            for position,token in zip(J,U):desired[position]=token
            for position,token in zip([i for i in L if i not in J],[i for i in L if i not in U]):desired[position]=token
        else:desired=assignment(floors,U,J)
        placed=tuple(CC[token] for token in desired);M,swaps=permute(k,floors,CC,desired)
        lower=Path(k,floors,AA);phases=[]
        if method=="X32":
            phases.append(phase(lower,placed,F,L))
            phases.append(phase(lower,placed,J,sorted(set(L)-set(J))))
            phases.append(phase(lower,placed,sorted(set(L)-set(J)),sorted(F+J)))
        else:
            phases.append(phase(lower,placed,J,I))
            phases.append(phase(lower,placed,sorted(set(range(len(floors)))-set(J)),J))
        clipped,layers=convert(k,floors,lower.vertices)
        prelim=Path(k,floors,A);prelim.extend(source.vertices);prelim.extend(lower.vertices);prelim.extend(list(reversed(M.vertices)));prelim.extend(list(reversed(destination.vertices)))
        finished=Path(k,floors,A);finished.extend(source.vertices);finished.extend(clipped);finished.extend(list(reversed(M.vertices)));finished.extend(list(reversed(destination.vertices)))
        preliminary=prelim.vertices;final=finished.vertices
        meta.update(assignment=desired,handover=dict(source=vertex(AA),destination=vertex(CC),placed=vertex(placed),J=J,vertices=lower.serial(),phases=phases,**extra),permutation=dict(vertices=M.serial(),swaps=swaps),preparation=dict(source=source.serial(),destination=destination.serial()),conversion=layers)
        meta["upper_entry"].extend([vertex(AA),vertex(CC),vertex(placed)])
    else:raise ValueError("unknown mechanism")
    record["preliminary"]=[vertex(state) for state in preliminary];record["final"]=[vertex(state) for state in final]
    if len(record["preliminary"])+len(record["final"])>LIMIT:raise ResourceLimit("per-identity combined primitive bound")
    if case["method"]=="NATIVE":record["nested"]=native_lift(k,floors,A,final)
    return record
