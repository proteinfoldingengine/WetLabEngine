"""Ancestor-first parent-array enumeration; independent verifier uses Prüfer trees."""
from itertools import product
from lineage import Carrier

def rooted_shapes(max_vertices=5):
    out = {}
    for n in range(1, max_vertices+1):
        for parents in product(*(range(i) for i in range(1,n))):
            children = {i: [] for i in range(n)}
            for child, parent in enumerate(parents,1): children[parent].append(child)
            def code(v): return '('+''.join(sorted(code(c) for c in children[v]))+')'
            signature = code(0)
            if signature not in out:
                keys = []
                def walk(v, path):
                    keys.append(path)
                    for i,c in enumerate(sorted(children[v], key=code)): walk(c,path+(i,))
                walk(0,())
                out[signature] = tuple(keys)
    return dict(sorted(out.items()))

def legal_masks(keys):
    valid = []
    for mask in range(1, 1 << len(keys)):
        subset = tuple(k for i,k in enumerate(keys) if mask & (1<<i))
        try: Carrier('enumeration', subset)
        except ValueError: continue
        valid.append(mask)
    return tuple(valid)

def chains(masks, full, max_arrows=3):
    def extend(prefix):
        if len(prefix)>1: yield tuple(prefix)
        if len(prefix)==max_arrows+1: return
        for nxt in masks:
            if nxt & prefix[-1] == nxt:
                yield from extend(prefix+[nxt])
    yield from extend([full])
