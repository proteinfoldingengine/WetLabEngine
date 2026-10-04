"""Independent set-based reconstruction from the approved formula definitions.

No producer module is imported. Binary zero sums are reconstructed by bit parity.
"""
from itertools import combinations

def binary_input(dimension,extra=0):
    palette=frozenset(range(2**dimension-1));low=[];high=[]
    for size,store in ((4,low),(3,high)):
        for omitted in combinations(sorted(palette),size):
            if all(sum(((x+1)>>bit)&1 for x in omitted)%2==0 for bit in range(dimension)):
                store.append(sorted(palette.difference(omitted)))
    supports=low+high+[high[0][:] for _ in range(extra)]
    return len(palette),supports,[len(palette)-4]*len(low)+[len(palette)-3]*(len(high)+extra),len(low)

def cyclic_input(extra):
    supports=[]
    for slot in range(9):supports.append(sorted(((slot+offset)%9 for offset in (0,1,3))))
    supports.extend([supports[0][:] for _ in range(extra)])
    return 9+extra,supports,[3]*(9+extra)

def patch_input():
    k,supports,_,_=binary_input(3)
    tokens=((1,2,3),(1,4,5),(2,4,6),(2,5,7),(3,6,7),(3,4,5),(1,6,7),(3,4,7),(3,5,6),(4,5,6,7),(1,3,5,7),(1,3,4,6),(1,2,5,6),(1,2,4,7))
    target=[[label-1 for label in row] for row in tokens]
    supports=supports+[list(range(7)) for _ in range(26)]
    target=target+[list(range(7)) for _ in range(26)]
    return k,supports,target

def mapped(supports,k,shift,reverse,root_shift,low_count=None,high_shift=0):
    result=[]
    n=len(supports)
    for slot in range(n):
        if low_count is None:old=(slot-root_shift)%n
        elif slot<low_count:old=(slot-root_shift)%low_count
        else:old=low_count+(slot-low_count-high_shift)%(n-low_count)
        result.append(sorted((shift+k-1-x)%k if reverse else (shift+x)%k for x in supports[old]))
    return result

def entry(family,parameters,operation,augmentation,k,floors,source,target,method,**details):
    return {"identity":[family,parameters,operation,augmentation],"k":k,"floors":floors,"A":source,"C":target,"method":method,**details}

def reconstruct_cases():
    for extra in (0,1,2):
        k,source,floors=cyclic_input(extra)
        for shift in range(k):
            for root_shift in range(k):
                for reverse in (0,1):
                    yield entry("R1",{"d":extra},{"a":shift,"b":root_shift,"v":reverse},"NONE",k,floors,source,mapped(source,k,shift,reverse,root_shift),"X15N")
    k,source,target=patch_input();n=len(source)
    for shift in range(k):
        for root_shift in range(n):
            for reverse in (0,1):
                yield entry("R2",{},{"a":shift,"b":root_shift,"v":reverse},"NONE",k,[3]*n,source,mapped(target,k,shift,reverse,root_shift),"X32",L=list(range(n)),F=[],U=sorted((j+root_shift)%n for j in range(5)))
    for dimension in (3,4):
        k=2**dimension-1
        for extra in (0,1,k):
            k,source,floors,low=binary_input(dimension,extra);high=len(source)-low
            for shift in (0,1,k-1):
                for reverse in (0,1):
                    for low_shift in sorted(set((0,1,low-1))):
                        for high_shift in sorted(set((0,1,high-1))):
                            operation=dict(a=shift,v=reverse,bL=low_shift,bF=high_shift)
                            target=mapped(source,k,shift,reverse,low_shift,low,high_shift)
                            yield entry("R3",dict(m=dimension,d=extra),operation,"NONE",k,floors,source,target,"X33")
                            for slot in sorted(set((0,len(source)-1))):
                                for label in sorted(frozenset(range(k))-frozenset(target[slot])):
                                    enlarged=[row[:] for row in target];enlarged[slot]=sorted(target[slot]+[label])
                                    yield entry("R3",dict(m=dimension,d=extra),operation,dict(op="ADD",i=slot,x=label),k,floors,source,enlarged,"X33")
    k,source,target=patch_input();n=len(source)
    yield entry("R4",dict(type="FULL_PATCH_BOUND",k=k,r=n),"NONE","NONE",k,[3]*n,source,target,"X32",L=list(range(n)),F=[],U=list(range(n)))
    floors=[5 if i==7 else 3 for i in range(n)]
    yield entry("R4",dict(type="INVALID_INPUT_FLOOR",k=k,r=n),"NONE","NONE",k,floors,source,target,"X32",L=list(range(n)),F=[],U=list(range(5)))
    k,source,floors,low=binary_input(3)
    yield entry("R4",dict(type="ZERO_PATCH",k=k,r=len(source)),"NONE","NONE",k,floors,source,source,"X32",L=list(range(low)),F=list(range(low,len(source))),U=[])
    k,source,floors,low=binary_input(4);target=mapped(source,k,1,1,1,low,1)
    yield entry("R4",dict(type="ZERO_CAPACITY_GRADE",m=4,d=0),dict(a=1,v=1,bL=1,bF=1),"NONE",k,floors+[k],source+[list(range(k))],target+[list(range(k))],"X33")
    k,source,floors=cyclic_input(1)
    yield entry("R5",dict(parent="R1",d=1),dict(a=1,b=1,v=1),"NONE",k,floors,source,mapped(source,k,1,1,1),"NATIVE",parent_method="X15N")
    k,source,target=patch_input();n=len(source)
    yield entry("R5",dict(parent="R2"),dict(a=1,b=1,v=1),"NONE",k,[3]*n,source,mapped(target,k,1,1,1),"NATIVE",parent_method="X32",L=list(range(n)),F=[],U=sorted((j+1)%n for j in range(5)))
    k,source,floors,low=binary_input(4,15)
    yield entry("R5",dict(parent="R3",m=4,d=k),dict(a=1,v=1,bL=1,bF=1),"NONE",k,floors,source,mapped(source,k,1,1,1,low,1),"NATIVE",parent_method="X33")
