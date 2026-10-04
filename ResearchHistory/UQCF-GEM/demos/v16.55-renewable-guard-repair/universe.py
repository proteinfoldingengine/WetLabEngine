"""Producer-side formula domain. No sampling or endpoint deduplication."""
from itertools import combinations, product
from functools import reduce
from operator import xor

def binary(m,d=0):
    k=2**m-1
    blocks=[[t for t in combinations(range(1,k+1),s) if reduce(xor,t)==0] for s in (4,3)]
    roots=[sorted(set(range(k))-{x-1 for x in t}) for group in blocks for t in sorted(group)]
    ell=len(blocks[0]); f=len(blocks[1])
    roots += [roots[ell][:] for _ in range(d)]
    return k,roots,[k-4]*ell+[k-3]*(f+d),ell

def r1(d):
    roots=[sorted({i,(i+1)%9,(i+3)%9}) for i in range(9)]
    roots += [roots[0][:] for _ in range(d)]
    return 9+d,roots,[3]*(9+d)

def r2():
    k,A,_,_=binary(3)
    Q=["123","145","246","257","367","345","167","347","356","4567","1357","1346","1256","1247"]
    C=[[int(x)-1 for x in t] for t in Q]
    return k,A+[list(range(k)) for _ in range(26)],C+[list(range(k)) for _ in range(26)]

def transform(roots,k,a,v,b=0,ell=None,bF=0):
    out=[None]*len(roots)
    for i,root in enumerate(roots):
        if ell is None:j=(i+b)%len(roots)
        elif i<ell:j=(i+b)%ell
        else:j=ell+(i-ell+bF)%(len(roots)-ell)
        out[j]=sorted((a+(k-1-x if v else x))%k for x in root)
    return out

def case(family,params,tr,aug,k,floors,A,C,method,**extra):
    return dict(identity=[family,params,tr,aug],k=k,floors=floors,A=A,C=C,method=method,**extra)

def generate_cases():
    for d in (0,1,2):
        k,A,floors=r1(d)
        for a,b,v in product(range(k),range(k),(0,1)):
            yield case("R1",{"d":d},dict(a=a,b=b,v=v),"NONE",k,floors,A,transform(A,k,a,v,b),"X15N")
    k,A,C=r2(); r=len(A)
    for a,b,v in product(range(k),range(r),(0,1)):
        yield case("R2",{},dict(a=a,b=b,v=v),"NONE",k,[3]*r,A,transform(C,k,a,v,b),"X32",L=list(range(r)),F=[],U=sorted((i+b)%r for i in range(5)))
    for m in (3,4):
        k=2**m-1
        for d in (0,1,k):
            k,A,floors,ell=binary(m,d); f=len(A)-ell
            for a,v,bL,bF in product((0,1,k-1),(0,1),sorted({0,1,ell-1}),sorted({0,1,f-1})):
                C=transform(A,k,a,v,bL,ell,bF); tr=dict(a=a,v=v,bL=bL,bF=bF)
                yield case("R3",dict(m=m,d=d),tr,"NONE",k,floors,A,C,"X33")
                for i in sorted({0,len(A)-1}):
                    for x in range(k):
                        if x in C[i]:continue
                        augmented=[row[:] for row in C];augmented[i]=sorted(C[i]+[x])
                        yield case("R3",dict(m=m,d=d),tr,dict(op="ADD",i=i,x=x),k,floors,A,augmented,"X33")
    k,A,C=r2();r=len(A)
    yield case("R4",dict(type="FULL_PATCH_BOUND",k=k,r=r),"NONE","NONE",k,[3]*r,A,C,"X32",L=list(range(r)),F=[],U=list(range(r)))
    floors=[3]*r;floors[7]=5
    yield case("R4",dict(type="INVALID_INPUT_FLOOR",k=k,r=r),"NONE","NONE",k,floors,A,C,"X32",L=list(range(r)),F=[],U=list(range(5)))
    k,A,floors,ell=binary(3)
    yield case("R4",dict(type="ZERO_PATCH",k=k,r=len(A)),"NONE","NONE",k,floors,A,A,"X32",L=list(range(ell)),F=list(range(ell,len(A))),U=[])
    k,A,floors,ell=binary(4);C=transform(A,k,1,1,1,ell,1)
    A=A+[list(range(k))];C=C+[list(range(k))];floors=floors+[k]
    yield case("R4",dict(type="ZERO_CAPACITY_GRADE",m=4,d=0),dict(a=1,v=1,bL=1,bF=1),"NONE",k,floors,A,C,"X33")
    k,A,floors=r1(1)
    yield case("R5",dict(parent="R1",d=1),dict(a=1,b=1,v=1),"NONE",k,floors,A,transform(A,k,1,1,1),"NATIVE",parent_method="X15N")
    k,A,C=r2();r=len(A)
    yield case("R5",dict(parent="R2"),dict(a=1,b=1,v=1),"NONE",k,[3]*r,A,transform(C,k,1,1,1),"NATIVE",parent_method="X32",L=list(range(r)),F=[],U=sorted((i+1)%r for i in range(5)))
    k,A,floors,ell=binary(4,15)
    yield case("R5",dict(parent="R3",m=4,d=k),dict(a=1,v=1,bL=1,bF=1),"NONE",k,floors,A,transform(A,k,1,1,1,ell,1),"NATIVE",parent_method="X33")
