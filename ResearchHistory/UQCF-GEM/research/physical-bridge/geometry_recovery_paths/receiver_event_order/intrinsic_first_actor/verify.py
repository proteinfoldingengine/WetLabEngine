"""Separate coordinate/set test of the recovery theorem and full-atlas trigger certificate."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import json

SHAPE=((0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
       (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),
       (9,3),(9,8),(10,0),(10,1),(10,10))
def point(x,y):
    return x%11+11*(y%11)

def catalog():
    return [frozenset(point(tx+sx*(y if sw else x),ty+sy*(x if sw else y)) for x,y in SHAPE)
            for sw,sx,sy,tx,ty in product((False,True),(-1,1),(-1,1),range(11),range(11))]

def main():
    results=json.loads(Path(__file__).with_name('results.json').read_text())
    sites=range(121)
    supports=catalog()
    initial=[set(k+1 for k,s in enumerate(supports) if i in s) for i in sites]
    W=[[4*len(a^b) for b in initial] for a in initial]
    all_pairs=list(combinations(sites,2))
    near={i:{j for j in sites if W[i][j]==704} for i in sites}
    assert all(len(row)==4 for row in near.values())
    assert all({W[j][k] for j,k in combinations(near[i],2)}=={1088,1216} for i in sites)
    line={point(x,3*x) for x in range(11)}
    assert all(line&s for s in supports) and all(any(line&s=={i} for s in supports) for i in line)
    translated = [{point(i % 11 + dx, i // 11 + dy) for i in line}
                  for dx, dy in product(range(11), repeat=2)]
    assert len(translated) == 121
    assert all(all(cover & support for support in supports) for cover in translated)
    assert all(sum(i in cover for cover in translated) == len(line) for i in sites)
    stats=[]
    for entry in results['cases']:
        cut=set(entry['addresses']); old=initial[0]-cut
        low={j for j in near[0] if len(initial[j]^old)*4==688}
        high=near[0]-low
        assert len(high)==len(low)==2
        # Two high-side *opposite* spokes are initially down 16 as well.
        extremes={point(2*(j%11),2*(j//11)) for j in high}
        assert all(4*len(initial[j]^old)==W[0][j]-16 for j in extremes)
        required={j:1 for j in low|extremes}
        required.update({j:-1 for j in high})
        allowed=set()
        for addr in range(1,969):
            after=old^{addr}
            if all(len(initial[j]^after)-len(initial[j]^old)==d for j,d in required.items()):
                allowed.add(addr)
        # The two remaining opposite tests each need +2 units across the whole path.
        rest={point(2*(j%11),2*(j//11)) for j in low}
        assert all(4*len(initial[j]^old)==W[0][j]-8 for j in rest)
        score={a:sum(len(initial[j]^(old^{a}))-len(initial[j]^old) for j in rest) for a in allowed}
        choices=[set(g) for g in combinations(sorted(allowed),4) if sum(score[a] for a in g)==4]
        assert choices==[cut]
        # Every undo subset is a distinct state. The minimum away from 0 is an internal 704 reference.
        mu_away=min(W[i][j] for i,j in all_pairs if i>0)
        counts=Counter()
        for k in range(5):
            for pending in combinations(sorted(cut),k):
                row=initial[0]-set(pending)
                mu=min(mu_away,min(4*len(row^initial[j]) for j in range(1,121)))
                assert (mu_away-mu)//4==k
                counts[k]+=1
        stats.append(dict(deep_progress_addresses=sorted(allowed),unique_full_set=sorted(cut),undo_layers=list(sorted(counts.items()))))
    # Independent line census. Only the remote holders of one of the eight affected
    # leaves can win them. Their relative order determines every affected winner.
    arms=[{41,217,278,454},{91,157,338,404}]
    pool=sorted(set().union(*(supports[a-1]&line for arm in arms for a in arm))-{0})
    census=Counter()
    from math import factorial
    for priority in permutations(pool):
        wins=[Counter(next(i for i in priority if i in supports[a-1]) for a in arm) for arm in arms]
        reached=set(wins[0])|set(wins[1])
        different=sum(wins[0][r]!=wins[1][r] for r in reached)
        census[len(reached),different]+=factorial(10)//factorial(len(pool))
    assert [[*k,v] for k,v in sorted(census.items())]==results['source_first_orders']
    return dict(line_meets_all_supports=True,full_cover_upper_bound=11,
                minimum_distinct_sources_needed_for_possible_trigger_lower_bound=11,
                relevant_remote_priorities=len(pool),shortest_repairs=stats,
                exact_source_first_priority_census=[[a,b,v] for (a,b),v in sorted(census.items())])

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
