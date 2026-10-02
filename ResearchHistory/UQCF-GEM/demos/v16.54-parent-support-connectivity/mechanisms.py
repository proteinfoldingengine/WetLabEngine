"""Deterministic constructions; independent certificate checks live in verifier."""
from itertools import combinations, permutations
import math
from model import Path,state,plain,tau,cover,shadow,clip

def result(c,path,facts=None,status='PASS',events=None,**extra):
    return dict(identity=c['identity'],status=status,path=[plain(v) for v in path],
                tau=[tau(v) for v in path] if c['identity'][1]['q'] is not None else [],
                facts=facts or {},events=events or [],**extra)

def packet_family(c):
    _,p,rows,ch=c['identity'];kind=p['kind'];a=state(rows);route=Path(a);facts={}
    if kind=='packet':
        route.packet(*ch,a);facts['source_rows']=[i for i,row in enumerate(a) if ch[1] in row]
    elif kind=='double_packet':
        facts['source_rows']=[[i for i,row in enumerate(a) if pair[1] in row] for pair in ch]
        for pair in ch:route.packet(*pair,a)
    elif kind=='neighbor':
        neighbor=Path(a);neighbor.toggle(*ch['edge'],True);b=neighbor.last
        left=shadow(a,ch['left']);right=shadow(b,ch['right']) if ch['right'] else b
        route=Path(left);route.join(right)
        if ch['reverse']:route.vertices.reverse()
        facts={'original':[plain(a),plain(b)]}
    elif kind=='layers':
        legs=[]
        for reverse in (False,True):
            leg=Path(a)
            while tau(leg.last)>p['q']:
                h=cover(leg.last)
                pairs=list(permutations(h,2))
                leg.packet(*(pairs[-1] if reverse else pairs[0]))
            legs.append(leg.vertices)
        original=list(reversed(legs[0]))+legs[1][1:]
        route.vertices,layers=clip(original,p['q'])
        facts={'original_path':[plain(v) for v in original],'layers':layers}
    else:raise ValueError(kind)
    return result(c,route.vertices,facts)

def transfer(route,row,x,y):
    route.toggle(row,y,True);route.toggle(row,x,False)

def degree_two(c):
    _,p,rows,ch=c['identity'];route=Path(rows);target=state(ch['target']);events=[]
    pending=([tuple(e) for e in ch['edges']] if p['kind']=='forced_cycle' else
             [(x,y,i) for i,row in enumerate(route.last)
              for x,y in zip(sorted(row-target[i]),sorted(target[i]-row))])
    while pending:
        occupancy=lambda x:sum(x in row for row in route.last)
        free=next((e for e in pending if occupancy(e[1])<2),None)
        if free is not None:
            x,y,i=free;start=len(route.vertices)-1;transfer(route,i,x,y);pending.remove(free)
            events.append(dict(kind='direct_vacancy',start=start,end=len(route.vertices)-1,row=i,source=x,target=y))
            continue
        # Following outgoing edges from a full destination yields a simple cycle.
        seen={};walk=[];v=min(e[0] for e in pending)
        while v not in seen:
            seen[v]=len(walk)
            e=min(e for e in pending if e[0]==v);walk.append(e);v=e[1]
        cycle=walk[seen[v]:]
        z=ch['buffer'] if p['kind']=='forced_cycle' else next(x for x in range(p['k']) if occupancy(x)<2)
        offset=next(j for j,e in enumerate(cycle) if z not in route.last[e[2]])
        cycle=cycle[offset:]+cycle[:offset]
        start=len(route.vertices)-1;x,y,i=cycle[0];transfer(route,i,x,z)
        for a,b,j in reversed(cycle[1:]):transfer(route,j,a,b)
        transfer(route,i,z,y)
        events.append(dict(kind='buffered_cycle',start=start,end=len(route.vertices)-1,
                           edges=[list(e) for e in cycle],buffer=z))
        for e in cycle:pending.remove(e)
    assert route.last==target
    return result(c,route.vertices,events=events)

def element(c):
    _,p,rows,ch=c['identity'];route=Path(rows);target=state(ch['target']);caps=p['capacities'];events=[]
    desired={x:i for i,row in enumerate(target) for x in row}
    while route.last!=target:
        x=min(x for i,row in enumerate(route.last) for x in row if desired[x]!=i)
        old=next(i for i,row in enumerate(route.last) if x in row);dest=desired[x]
        if len(route.last[dest])==caps[dest]:
            y=min(y for y in route.last[dest] if desired[y]!=dest)
            spare=next(i for i,row in enumerate(route.last) if len(row)<caps[i])
            start=len(route.vertices)-1
            route.toggle(spare,y,True);route.toggle(dest,y,False)
            events.append(dict(kind='element_buffer',start=start,end=len(route.vertices)-1,
                               label=y,source=dest,target=spare,old_owner=old))
        start=len(route.vertices)-1
        route.toggle(dest,x,True);route.toggle(old,x,False)
        events.append(dict(kind='element_transfer',start=start,end=len(route.vertices)-1,
                           label=x,source=old,target=dest))
    return result(c,route.vertices,events=events)

def saturated(c):
    _,p,rows,ch=c['identity'];route=Path(rows)
    if p['kind']=='classify':
        return result(c,route.vertices,{'feasible':tau(route.last)==p['q']})
    target=state(ch['target']);q=p['q']
    while route.last!=target:
        i,x=next((i,x) for i in range(q) for x in sorted(route.last[i]-target[i]))
        j=next(j for j in range(q) if x in target[j])
        y=min(route.last[j]-target[j])
        route.toggle(i,y,True);route.toggle(j,x,True)
        route.toggle(i,x,False);route.toggle(j,y,False)
    return result(c,route.vertices)

def auxiliary_tau(rows):
    return math.inf if any(not row for row in rows) else tau(rows)

def clone_sequence(c):
    _,p,rows,ch=c['identity'];route=Path(rows);facts={'clones':[]};completed=[tau(route.last)]
    for u,v in ch['operations']:
        old=route.last;t=tau(old)
        slots=sorted((i for i,row in enumerate(old) if u in row and v not in row),key=lambda i:(p['a'][i],i))
        demands=sorted({frozenset((row-{v})|{u}) for row in old if v in row and u not in row},key=lambda row:(len(row),tuple(sorted(row))))
        compatible=len(demands)<=len(slots) and all(p['a'][i]<=len(row) for i,row in zip(slots,demands))
        if not compatible:
            return result(c,route.vertices,{'reason':'slot criterion','clones':facts['clones']},status='REFUSED')
        fixed=[row for i,row in enumerate(old) if i not in slots]
        f=auxiliary_tau([row for row in old if u not in row]);lam=auxiliary_tau([row-{u,v} for row in fixed])
        start=len(route.vertices)-1
        for j,i in enumerate(slots):route.replace(i,demands[j] if j<len(demands) else range(p['k']))
        value=tau(route.last);completed.append(value)
        facts['clones'].append(dict(u=u,v=v,slots=slots,demands=[sorted(row) for row in demands],
            f=f,contraction='infinity' if math.isinf(lam) else lam,before=t,after=value,
            safe=lam>=t,exact=lam>=t and (f==t-1 or lam==t),start=start,end=len(route.vertices)-1))
    facts['completed_tau']=completed
    # Diagnostic unsafe sequences deliberately retain their accumulated losses.
    if completed[-1]==p['q']:
        facts['preliminary_path']=[plain(v) for v in route.vertices]
        route.vertices,facts['layers']=clip(route.vertices,p['q'])
    return result(c,route.vertices,facts)

def group_core(groups,h,cyclic):
    answer={frozenset(e) for group in groups for e in combinations(sorted(group),h)}
    if cyclic:
        answer|={frozenset((*e,z)) for j in range(3) for e in combinations(sorted(groups[j]),2) for z in groups[(j+1)%3]}
    return sorted(answer,key=lambda row:tuple(sorted(row)))

def group_parts(sizes):
    start=0;groups=[]
    for n in sizes:groups.append(set(range(start,start+n)));start+=n
    return groups

def normalize_extras(route,groups,h,cyclic,k):
    representatives={}
    for row in group_core(groups,h,cyclic):
        representatives[row]=next(i for i,r in enumerate(route.last) if r==row)
    for i in range(len(route.last)):
        if i not in representatives.values():route.replace(i,range(k))

def relocate(route,groups,i,j,h,cyclic,k):
    u=min(groups[i]);oldcore=group_core(groups,h,cyclic)
    slots=sorted(next(z for z,row in enumerate(route.last) if row==edge) for edge in oldcore if u in edge)
    groups[i].remove(u);groups[j].add(u)
    newstar=[row for row in group_core(groups,h,cyclic) if u in row]
    assert len(slots)>=len(newstar)
    for index,z in enumerate(slots):route.replace(z,newstar[index] if index<len(newstar) else range(k))
    return {'source':i,'destination':j,'label':u,'slots':slots,'new_star':[sorted(row) for row in newstar]}

def balance_route(rows,p):
    route=Path(rows);h=p['h'];k=p['k'];cyclic=p['form']=='cyclic';groups=group_parts(p['sizes']);records=[]
    normalize_extras(route,groups,h,cyclic,k)
    while max(map(len,groups))-min(map(len,groups))>=2:
        widths=list(map(len,groups));before=[sum(x*x for x in widths),len(group_core(groups,h,cyclic))]
        if cyclic:
            eligible=[(i,(i+1)%3) for i in range(3) if widths[i]>=widths[(i+1)%3]+2]
            if not eligible:
                i=widths.index(max(widths));eligible=[(i,(i+1)%3)]
        else:
            eligible=[(i,j) for i in range(len(groups)) for j in range(len(groups)) if widths[i]>=widths[j]+2]
        i,j=min(eligible);start=len(route.vertices)-1
        move=relocate(route,groups,i,j,h,cyclic,k)
        widths=list(map(len,groups));after=[sum(x*x for x in widths),len(group_core(groups,h,cyclic))]
        assert after<before
        records.append(dict(start=start,end=len(route.vertices)-1,before=before,after=after,**move))
    # Canonical ordered sizes: choose lexicographically least cyclic rotation,
    # or the ascending size list for complete modules.
    if cyclic:
        shifts=[groups[i:]+groups[:i] for i in range(3)]
        groups=min(shifts,key=lambda gs:tuple(map(len,gs)))
    else:groups=sorted(groups,key=len)
    canonical=group_parts(list(map(len,groups)))
    mapping={x:y for old,new in zip(groups,canonical) for x,y in zip(sorted(old),sorted(new))}
    route.rename(mapping)
    edges=group_core(canonical,h,cyclic);desired=edges+[edges[0]]*(len(rows)-len(edges))
    reps={next(i for i,row in enumerate(route.last) if row==edge) for edge in edges}
    for i in range(len(rows)):
        if i not in reps:route.replace(i,edges[0])
    route.reorder(desired)
    return route.vertices,records

def modules(c):
    _,p,rows,ch=c['identity'];route=Path(rows)
    if p['kind']=='obstruction':
        return result(c,route.vertices,{'method':'complete-module normal form','available_slots':len(rows),
            'required_slots':math.comb(6,3),'claim':'method obstruction only'})
    if p['kind']=='relocate':
        groups=group_parts(p['sizes']);normalize_extras(route,groups,p['h'],p['form']=='cyclic',p['k'])
        move=relocate(route,groups,*ch,p['h'],p['form']=='cyclic',p['k'])
        return result(c,route.vertices,{'relocation':move})
    left,records=balance_route(rows,p)
    facts={'balancing':records}
    if p['kind']=='module_pair':
        right,other=balance_route(ch['target'],dict(p,sizes=[4,4]))
        assert left[-1]==right[-1]
        left+=list(reversed(right))[1:];facts['right_balancing']=other
    return result(c,left,facts)

def guards(c):
    _,p,rows,ch=c['identity'];n=p['N'];r=len(rows)
    if r<2*n:
        return result(c,[state(rows)],{'reason':'prescribed disjoint N-guard slots unavailable','required_slots':2*n,'available_slots':r},status='REFUSED')
    # Transformation indices specify guard roles even for equal supports.
    guard_indices=sorted(((i+ch['shift'])%r for i in range(n)),
                         key=lambda i:(ch['target'][i],i))
    rest=[i for i in range(r) if i not in guard_indices]
    order=rest+guard_indices
    target=state(ch['target']);permuted=tuple(target[i] for i in order)
    route=Path(rows);j_indices=list(range(r-n,r))
    for j in j_indices:route.replace(j,permuted[j])
    guard_end=len(route.vertices)-1
    for i in range(r-n):route.replace(i,permuted[i])
    coexist_end=len(route.vertices)-1
    route.reorder(target)
    preliminary=route.vertices
    clipped,layers=clip(preliminary,p['q'])
    facts={'source_guard':list(range(n)),'target_guard':j_indices,'target_order':order,
           'guard_end':guard_end,'coexist_end':coexist_end,
           'preliminary_path':[plain(v) for v in preliminary],'layers':layers}
    return result(c,clipped,facts)

# Keep dispatch last so all constructors are explicit, with no fallback search.
def produce(c):
    family,p,rows,ch=c['identity']
    if family=='M1':return packet_family(c)
    if family=='M2':return element(c) if p['kind']=='element' else degree_two(c)
    if family=='M3':return saturated(c)
    if family=='M4':return clone_sequence(c)
    if family=='M5':return modules(c)
    if family=='M6':return guards(c)
    return {'identity':c['identity'],'status':'UNIMPLEMENTED'}
