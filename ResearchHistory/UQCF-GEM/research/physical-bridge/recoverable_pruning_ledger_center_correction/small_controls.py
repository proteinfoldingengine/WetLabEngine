"""Six frozen tiny controls. Diagonal coordinates are exact matrix coordinates.
Graph production and rational subspace intersection have independent decisions.
No historical producer/checker imports; no random or expanding enumeration.
"""
from fractions import Fraction as F
import json

def rref(rows, width=None):
    a=[list(map(F,r)) for r in rows]
    n=len(a); m=len(a[0]) if a else (width or 0)
    assert all(len(r)==m for r in a)
    pivots=[];r=0
    for c in range(m):
        pivot=next((k for k in range(r,n) if a[k][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        scale=a[r][c];a[r]=[v/scale for v in a[r]]
        for k in range(n):
            if k!=r:
                factor=a[k][c];a[k]=[x-factor*y for x,y in zip(a[k],a[r])]
        pivots.append(c);r+=1
        if r==n:break
    return a,pivots

def canonical(rows):
    a,_=rref(rows)
    return [r for r in a if any(r)]

def nullspace(rows,width):
    a,p=rref(rows,width);free=[c for c in range(width) if c not in p];out=[]
    for c in free:
        v=[F(0)]*width;v[c]=F(1)
        for row,pivot in enumerate(p):v[pivot]=-a[row][c]
        out.append(v)
    return out

def intersection_basis(left,right):
    # Solve U*a=V*b directly, never reading incidences or graph output.
    if not left or not right:return []
    d=len(left[0]);m=len(left);n=len(right)
    equations=[[F(left[i][k]) for i in range(m)]+[-F(right[j][k]) for j in range(n)] for k in range(d)]
    kernel=nullspace(equations,m+n)
    vectors=[[sum(v[i]*F(left[i][k]) for i in range(m)) for k in range(d)] for v in kernel]
    return canonical(vectors)

def graph_center(old,new):
    # All frozen projectors are diagonal, so multiplication is coordinatewise.
    # This method neither calls rref/intersection nor tests subspace membership.
    m=len(old);n=len(new);d=len(old[0]);adj=[set() for _ in range(m+n)]
    for i,p in enumerate(old):
        for j,q in enumerate(new):
            if any(F(p[k])*F(q[k]) for k in range(d)):
                adj[i].add(m+j);adj[m+j].add(i)
    unseen=set(range(m+n));out=[]
    while unseen:
        todo=[min(unseen)];component=set()
        while todo:
            v=todo.pop()
            if v in component:continue
            component.add(v);todo.extend(adj[v]-component)
        unseen-=component
        left=[sum(F(old[i][k]) for i in component if i<m) for k in range(d)]
        right=[sum(F(new[j-m][k]) for j in component if j>=m) for k in range(d)]
        assert left==right and any(left)
        out.append(left)
    return out

def member(vector,span):return len(canonical(span+[vector]))==len(canonical(span))
def norm(v):return sum(abs(F(x)) for x in v)
def fixed_checks():
    cases=[('scalar_C2',[[1,0],[0,1]],[[1,1]],1),
           ('four_address',[[int(i==j) for j in range(4)] for i in range(4)],[[1,0,0,0],[0,1,1,0],[0,0,0,1]],3),
           ('incomparable_centers',[[1,0,0],[0,1,1]],[[1,1,0],[0,0,1]],1)]
    result=[]
    for name,old,new,dimension in cases:
        graph=canonical(graph_center(old,new));linear=intersection_basis(old,new)
        assert graph==linear and len(linear)==dimension
        individual=canonical([p for p in old if member(p,new)])
        assert individual!=linear  # deliberate old-formula rejection in all three examples
        result.append(dict(case=name,dimension=dimension,common_center=[[str(v) for v in r] for r in linear],old_individual_span_rejected=True))
    plus=list(map(F,[1,1,2,1]));minus=list(map(F,[1,1,1,2]));effect=[0,1,1,0]
    contrast=sum(F(e)*(x-y) for e,x,y in zip(effect,plus,minus))/5
    assert contrast==F(1,5) and plus[1]==minus[1]
    # Bare C1 straddles; joining selected p and the unit restores both sectors.
    old=[[1,0],[0,1]];unit=[1,1];p=[1,0]
    final=canonical([unit,p]);assert len(final)==2 and len(canonical([p]))==1
    assert canonical(graph_center(old,old))==canonical(old)
    assert len(intersection_basis(old,[unit]))==1
    result.append(dict(case='closure_unitalization',bare_common_dimension=1,final_common_dimension=2,omitted_unit_dimension=1))
    assert norm([1,-1])==2 and norm([0])==0
    old_raw=[F(1,5),-F(1,5)];new_raw=old_raw+[F(0)]
    before=norm([x/F(1,5) for x in old_raw]);after=norm(new_raw)
    assert before==2 and after==F(2,5) and norm(old_raw)==norm(new_raw)
    result.append(dict(case='nonhereditary_and_mass',nonhereditary_contrast=['2','0'],conditional_contrast=[str(before),str(after)],raw_contrast=str(norm(new_raw))))
    old3=[[1,0,0],[0,1,0],[0,0,1]];final3=[[1,0,0],[0,1,1]]
    assert member(old3[0],final3) and not member(old3[1],final3)
    selected_unital=[[1,0,0],[1,1,1]]
    assert canonical(selected_unital)==canonical(final3)
    result.append(dict(case='hereditary_selected_not_whole_center',selected_e1_survives=True,e2_lost=True,selected_unital_record_dimension=2))
    return dict(status='PASS',scope='Six fixed exact controls only; no universal theorem or historical conformance certification',cases=result,retained_effect_contrast=str(contrast),native_bridge='NOT_DERIVED')
if __name__=='__main__':print(json.dumps(fixed_checks(),indent=2,sort_keys=True))
