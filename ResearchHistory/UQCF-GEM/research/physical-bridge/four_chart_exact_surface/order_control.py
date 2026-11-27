"""Observe action and endpoint under all top-branch and palette orders."""
from collections import Counter, defaultdict
from itertools import groupby, permutations, product
from pathlib import Path
import sys

sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import producer as p
import verifier as v

def encode(tree,root_bits):
    nodes=p.layout(tree)
    state=[1,1]
    for u,label in zip(nodes[0],root_bits):
        for i in p.vertices(nodes,u):
            state[label]|=1<<i
    return state

def recolor(s,original_sites):
    return [sum(((z>>site)&1)<<i for i,site in enumerate(original_sites)) for z in s]

def first_site(path):
    if len(path)==1:
        return None
    diffs=[x^y for x,y in zip(path[0],path[1]) if x!=y]
    assert len(diffs)==1 and diffs[0].bit_count()==1
    return diffs[0].bit_length()-1

def distance(s,t):
    return sum((x^y).bit_count() for x,y in zip(s,t))

def monotone_successors(tree,q,initial,target):
    # Independent dynamic programming over admissible exact one-bit moves that fix a discrepancy.
    from functools import cache
    @cache
    def visit(state):
        if list(state)==target:
            return True
        return any(visit(t) for _,t in next_states(state))
    def next_states(state):
        for j,z in enumerate(state):
            diff=z^target[j]
            while diff:
                bit=diff & -diff;diff^=bit
                nxt=list(state);nxt[j]^=bit
                try: profile=v.profile_check(tree,2,nxt)
                except v.InterfaceNotPreserved: continue
                if profile==q:yield bit.bit_length()-1,tuple(nxt)
    assert visit(tuple(initial))
    return {i for i,t in next_states(initial) if visit(t)}

def run(name):
    tree=p.TREES[name]; nodes=p.layout(tree); roots=nodes[0]
    count=Counter(); grouped=Counter()
    for start in product(range(2),repeat=3):
        if len(set(start))!=2:continue
        physical=encode(tree,start)
        q=v.profile_check(tree,2,physical)
        goals=defaultdict(list)
        for order in permutations(range(3)):
            new_tree=tuple(tree[i] for i in order)
            mapping=[0]+[s for i in order for s in p.vertices(nodes,roots[i])]
            inverse=[mapping.index(i) for i in range(len(mapping))]
            state=recolor(physical,mapping)
            observed=v.profile_check(new_tree,2,state)
            for palette in permutations(range(2)):
                path=p.normalize(state,new_tree,2,observed,order=palette,trace=[])
                swapped=p.normalize(state[::-1],new_tree,2,observed,order=tuple(1-j for j in palette),trace=[])
                assert path==[frame[::-1] for frame in swapped]
                goal=p.canonical(new_tree,2,observed,order=palette)
                peak=v.path_check(new_tree,2,observed,path,state,goal)[0]
                path=[recolor(s,inverse) for s in path]
                end=path[-1];site=first_site(path)
                goal_bits=tuple(int(bool(end[1]&(1<<i))) for i in roots)
                assert end==encode(tree,goal_bits)
                assert path[0]==physical and len(path)-1==distance(physical,end)
                goals[goal_bits].append((peak,site))
                count['calls']+=1
        assert len(goals)==6
        for g,trials in goals.items():
            assert len(trials)==2
            diff=sum(a!=b for a,b in zip(start,g))
            sites=monotone_successors(tree,q,physical,encode(tree,g))
            exact_seen={s for peak,s in trials if peak==0 and s is not None}
            assert sites==exact_seen
            assert len(sites)==[0,1,1,2][diff]
            grouped[diff,len(sites),sum(peak==0 for peak,_ in trials)]+=1
        if start==(0,0,1):
            print(name,'start A,A,B and target B,B,A: (peak, mapped first site)',goals[(1,1,0)])
    print(name,'calls',count['calls'],'(differing subtrees,exact first sites,exact schedules):',sorted(grouped.items()))

def archive_control():
    import gzip,hashlib,json
    doc=p.produce()
    raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
    packet=gzip.compress(raw,compresslevel=9,mtime=0)
    packet=packet[:9]+bytes([3])+packet[10:]
    assert hashlib.sha1(f'blob {len(packet)}\0'.encode()+packet).hexdigest()=='571d38f08006b7023a65ec64cac77fe23e0db52a'
    observed={}
    for i,row in enumerate(doc['cases']):
        spec=row['spec']; name=spec['tree']; tree=p.TREES[name]
        if name in observed or row['failure'] or spec['k']!=2 or spec['q'][0]!=2:continue
        start=encode(tree,(1,0,1))
        if row['start']!=start:continue
        path=row['path']; nodes=p.layout(tree); roots=nodes[0]
        q=v.profile_check(tree,2,start)
        assert q==spec['q'] and path==p.normalize(start,tree,2,q)
        reversed_tree=tree[::-1]
        mapping=[0]+[s for i in (2,1,0) for s in p.vertices(nodes,roots[i])]
        inverse=[mapping.index(i) for i in range(len(mapping))]
        code=recolor(start,mapping)
        alt=p.normalize(code,reversed_tree,2,v.profile_check(reversed_tree,2,code))
        alt=[recolor(s,inverse) for s in alt]
        target=encode(tree,(0,1,0))
        assert v.path_check(tree,2,q,path,start,target)==[0,0,0]
        assert v.path_check(tree,2,q,alt,start,target)==[0,0,0]
        assert len(path)-1==len(alt)-1==distance(start,target)
        assert (first_site(path),first_site(alt))==(roots[0],roots[2])
        def word(trace,sites):
            return [k for k,_ in groupby(tuple(z&sites for z in s) for s in trace)]
        for root in roots:
            mask=sum(1<<s for s in p.vertices(nodes,root))
            assert word(path,mask)==word(alt,mask)
        old=set(map(tuple,path[1:-1])); new=set(map(tuple,alt[1:-1]))
        assert not old & new
        observed[name]=(i,len(path)-1,first_site(path),first_site(alt))
    assert set(observed)=={'T','U'}
    print('first qualifying archived case, path cost, actual and alternative first site:',observed)

if __name__=='__main__':
    for name in ('T','U'):run(name)
    archive_control()
