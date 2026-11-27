"""Independent exact enumeration. Uses integer incidence masks and no historical imports."""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json

def vertices(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1<<i))


def shapes(bound):
    level=[(-1,)]
    for _ in range(bound):
        first={}
        for p in sorted(level):
            def code(v):
                return '('+''.join(sorted(code(i) for i,u in enumerate(p) if u==v))+')'
            first.setdefault(code(0),p)
        yield from sorted(first.items())
        level=[p+(i,) for p in level for i in range(len(p))]


class Tree:
    def __init__(self,p):
        self.p=p
        self.full=(1<<len(p))-1
        self.kids=[sum(1<<j for j in range(1,len(p)) if p[j]==i) for i in range(len(p))]
        self.rows=[n for n in range(1,self.full+1,2) if
                   all(n>>p[t]&1 for t in vertices(n) if t!=0)]
        self.profile=lru_cache(None)(self._profile)

    def _profile(self,state):
        # The first cardinality at which a child set fits a union is its minimum.
        costs=[0 if not ch else len(state)+1 for ch in self.kids]
        unions=[0]*(1<<len(state))
        for subset in range(1,len(unions)):
            bit=subset & -subset
            u=unions[subset^bit] | state[bit.bit_length()-1]
            unions[subset]=u
            for v,ch in enumerate(self.kids):
                if ch and ch & u==ch:
                    costs[v]=min(costs[v],subset.bit_count())
        return costs,max([1]+costs)

    def covers(self,n):
        for ys in combinations(self.rows,n):
            u=0
            for row in ys:
                u|=row
            if u==self.full:
                yield ys

    def steps(self,ys):
        pre,h=self.profile(ys)
        for i,y in enumerate(ys):
            other=0
            for j,row in enumerate(ys):
                if i!=j:
                    other|=row
            for leaf in vertices(y & other & ~1):
                if self.kids[leaf] & y:
                    continue
                zs=ys[:i]+(y^(1<<leaf),)+ys[i+1:]
                post,k=self.profile(zs)
                parent=self.p[leaf]
                yield i,leaf,zs,pre[parent],post[parent],h,k


def enumerate_domains():
    atoms=Counter()
    paths_total=0
    counts_by_bit=Counter()
    path_digest=sha256()
    masked=[]
    two={}
    originals={}
    for name,p in shapes(7):
        tree=Tree(p)
        saw_two=False
        receipt_digest=sha256()
        for n in (range(1,5) if len(p)<=5 else [2]):
            for ys in tree.covers(n):
                for i,a,zs,t,u,h,k in tree.steps(ys):
                    if u-t != k-h:
                        if n==2:
                            saw_two=True
                        if len(p)<=5:
                            masked.append((list(p),list(ys),i,a))
                    if len(p)<=5:
                        atoms['total']+=1
                        atoms['local']+=u-t
                        atoms['global']+=k-h
                        row=(tuple(map(vertices,ys)),i,a,t,u,h,k,t!=u)
                        receipt_digest.update((repr(row)+'\n').encode())
                if len(p)>4:
                    continue
                words=defaultdict(list)
                def visit(state,word):
                    if len(word)>=2:
                        words[state].append(word)
                    if len(word)<5:
                        for j,b,new,t,u,h,k in tree.steps(state):
                            visit(new,word+((j,b,u-t),))
                visit(ys,())
                for zs,items in sorted(words.items()):
                    paths_total+=len(items)
                    for word in items:
                        counts_by_bit.update(str(bool(bit)) for _,_,bit in word)
                    path_digest.update((repr((p,ys,zs,sorted(items)))+'\n').encode())
        two[name]=saw_two
        if len(p)<=5:
            originals[name]=receipt_digest.hexdigest()
    return atoms,masked,paths_total,counts_by_bit,path_digest.hexdigest(),two,originals


def extended_control(allow_repeated_views):
    # Compare *all* three-chart withdrawal histories on the only minimal branching
    # shape. Fixed event ordinal, actor word, local input/output, endpoints,
    # full height word and addressed height map all enter each collision key.
    t=Tree((-1,0,0,1,1))
    histories=events=conflicts=0
    example=None
    starts = t.covers(3)
    if allow_repeated_views:
        starts = (rows for rows in combinations_with_replacement(t.rows, 3)
                  if rows[0] | rows[1] | rows[2] == t.full)
    count_starts = 0
    for start in starts:
        count_starts += 1
        seen={}
        def visit(state,steps,actor_word,heights,event_map):
            nonlocal histories,events,conflicts,example
            if steps:
                histories+=1
                for pos,(actor,leaf,before,after,bit) in enumerate(steps):
                    events+=1
                    key=(state,actor_word,heights,tuple(sorted(event_map)),pos,actor,leaf,before,after)
                    if key in seen and seen[key][0]!=bit:
                        conflicts+=1
                        if example is None:
                            example=dict(start=start,first=seen[key][1],second=steps,position=pos)
                    else:
                        seen.setdefault(key,(bit,steps))
            for i,a,z,t0,t1,h,k in t.steps(state):
                visit(z,steps+((i,a,state[i],z[i],t1>t0),),actor_word+(i,),heights+(k,),
                      event_map+((i,a,k-h),))
        visit(start,(),(),(t.profile(start)[1],),())
    return dict(cover_count=count_starts, nonempty_histories=histories,marked_occurrences=events,
                conflicting_arrivals=conflicts,first_conflict=example)


if __name__=='__main__':
    import sys
    data=json.loads(Path(__file__).with_name('results.json').read_bytes())
    ref=json.loads(Path(sys.argv[1]).read_bytes())
    atoms,miss,n,counts,digest,two,originals=enumerate_domains()
    a=data['archive']
    assert [atoms[k] for k in ('total','local','global')]==[a['atoms'],a['local_triggers'],a['global_rises']]
    assert [list(x) for x in sorted(miss)]==a['masked_atoms']
    assert originals=={s['code']:s['digest'] for s in ref['instances']}
    assert n==a['paths'] and counts==a['path_event_occurrences'] and digest==a['address_and_bit_path_digest']
    assert all(two[k]==(v==2) for k,v in data['tree_minima'].items())
    print(json.dumps(dict(shapes_by_minimum=Counter(data['tree_minima'].values()),confirmed_path_digest=digest,
                          confirmed_early_shape_digests=len(originals),fixed_position_three_chart=extended_control(False),
                          fixed_position_three_chart_allow_duplicates=extended_control(True)),
                     sort_keys=True,indent=2))
