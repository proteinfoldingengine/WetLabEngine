"""Producer-only ordered primitive moves and maximum-layer replacement."""
from functools import lru_cache
from itertools import combinations

LIMIT = 1000000

def state(rows):
    return tuple(frozenset(row) for row in rows)

def plain(rows):
    return [sorted(row) for row in rows]

@lru_cache(maxsize=10000)
def minimum_cover(canonical):
    if not canonical:
        return ()
    if any(not row for row in canonical):
        raise ValueError('empty root has no transversal')
    labels = sorted(set().union(*map(set,canonical)))
    # Coverage masks over DISTINCT roots; no search over unused palette labels.
    full = (1<<len(canonical))-1
    dp = {0:()}
    for x in labels:
        mask = sum(1<<i for i,row in enumerate(canonical) if x in row)
        for covered,witness in list(dp.items()):
            new = covered|mask
            candidate = witness+(x,)
            old = dp.get(new)
            if old is None or (len(candidate),candidate)<(len(old),old):
                dp[new]=candidate
    return dp[full]

def cover(rows):
    return minimum_cover(tuple(sorted(set(tuple(sorted(row)) for row in rows))))

def tau(rows):
    return len(cover(rows))

class Path:
    def __init__(self, rows):
        self.vertices = [state(rows)]
    @property
    def last(self):
        return self.vertices[-1]
    def toggle(self,i,x,add):
        rows = list(self.last)
        if (x in rows[i])==add:
            return
        rows[i]=rows[i]|{x} if add else rows[i]-{x}
        if len(self.vertices)>=LIMIT:
            raise RuntimeError('INCOMPLETE: primitive vertex resource bound')
        self.vertices.append(tuple(rows))
    def extend(self,vertices):
        assert self.last==vertices[0]
        if len(self.vertices)+len(vertices)-1>LIMIT:
            raise RuntimeError('INCOMPLETE: primitive vertex resource bound')
        self.vertices.extend(vertices[1:])
    def replace(self,i,row):
        row=frozenset(row)
        for x in sorted(row-self.last[i]):self.toggle(i,x,True)
        for x in sorted(self.last[i]-row):self.toggle(i,x,False)
    def join(self,target):
        target=state(target)
        # Complete all additions before any deletion: the two endpoint guards
        # apply on their respective halves of this union route.
        for i,row in enumerate(target):
            for x in sorted(row-self.last[i]):self.toggle(i,x,True)
        for i,row in enumerate(target):
            for x in sorted(self.last[i]-row):self.toggle(i,x,False)
    def packet(self,x,y,original=None):
        base=self.last if original is None else original
        for i,row in enumerate(base):
            if y in row:self.toggle(i,x,True)
    def swap_roots(self,i,j):
        target=list(self.last);target[i],target[j]=target[j],target[i]
        self.join(target)
    def swap_labels(self,x,y):
        self.join([{y if z==x else x if z==y else z for z in row} for row in self.last])
    def reorder(self,target):
        target=state(target)
        for i,row in enumerate(target):
            if self.last[i]!=row:
                j=next(j for j in range(i+1,len(target)) if self.last[j]==row)
                self.swap_roots(i,j)
    def rename(self,mapping):
        # Complete a partial bijection to a permutation before decomposing it.
        labels=sorted(set(mapping)|set(mapping.values()))
        remaining=sorted(set(labels)-set(mapping.values()))
        mapping=dict(mapping)
        for x,y in zip(sorted(set(labels)-set(mapping)),remaining):mapping[x]=y
        current={x:x for x in labels}
        for x in labels:
            if current[x]!=mapping[x]:
                old,new=current[x],mapping[x]
                self.swap_labels(old,new)
                current={z:new if w==old else old if w==new else w for z,w in current.items()}

def shadow(rows,pair=None):
    pair = tuple(cover(rows)[:2]) if pair is None else pair
    if len(pair)!=2:raise ValueError('minimum cover must contain two labels')
    p=Path(rows);p.packet(*pair)
    return p.last

def clip(vertices,q):
    current=list(vertices)
    layers=[]
    while max(map(tau,current))>q:
        peak=max(map(tau,current))
        assert tau(current[0])<peak and tau(current[-1])<peak
        lowered=[shadow(row) if tau(row)==peak else row for row in current]
        result=Path(lowered[0])
        for row in lowered[1:]:result.join(row)
        layers.append({'peak':peak,'before':len(current),'after':len(result.vertices)})
        current=result.vertices
    return current,layers
