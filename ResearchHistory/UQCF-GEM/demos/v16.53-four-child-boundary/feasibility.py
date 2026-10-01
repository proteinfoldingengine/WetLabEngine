"""Producer-side exact 15-region multiplicities and positional canonical form."""
from functools import lru_cache

def cover_number(regions):
    distances={0:0}
    for region in regions:
        for mask,n in list(distances.items()):
            joined=mask|region;distances[joined]=min(distances.get(joined,5),n+1)
    return distances.get(15,5)

@lru_cache(None)
def at_width(widths,q,k):
    widths=tuple(widths)
    if len(widths)!=4 or any(type(a)!=int or a<1 for a in widths) or type(q)!=int or q not in range(1,5):raise ValueError('four-child feasibility arguments')
    if type(k)!=int or k<max(widths):return None
    regions=sorted(range(1,16),key=lambda r:tuple(-((r>>i)&1) for i in range(4)))
    best=None;best_key=None
    def search(pos,remaining,slots,columns):
        nonlocal best,best_key
        if not any(remaining):
            if cover_number(set(columns))!=q:return
            roots=tuple(tuple(j for j,r in enumerate(columns) if r&(1<<i)) for i in range(4))
            key=tuple(0 if j in root else 1 for root in roots for j in range(k))
            if best_key is None or key<best_key:best,best_key=roots,key
            return
        if pos==15 or slots==0:return
        region=regions[pos];members=[i for i in range(4) if region&(1<<i)]
        for count in range(min(slots,*(remaining[i] for i in members)),-1,-1):
            left=tuple(a-count if i in members else a for i,a in enumerate(remaining))
            if max(left)>slots-count:continue
            if any(left[i] and not any(r&(1<<i) for r in regions[pos+1:]) for i in range(4)):continue
            search(pos+1,left,slots-count,columns+(region,)*count)
    search(0,widths,k,())
    return best

@lru_cache(None)
def minimum(widths,q):
    widths=tuple(widths)
    for k in range(max(widths),sum(widths)-(4-q)+1):
        roots=at_width(widths,q,k)
        if roots is not None:return k,roots
    raise ValueError('finite feasibility bound violated')
