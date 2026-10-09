import itertools
import json
from pins import SCOPE

def queries(k): return [h for h in range(1, 1 << k) if h.bit_count() <= 2]

def field(f, k): return [sum(not (s & h) for s in f) for h in queries(k)]

def decode(delta, k):
    if len(delta) != len(queries(k)): raise ValueError('wrong dimension')
    dd = dict(zip(queries(k), delta))
    changed = [x for x in range(k) if dd[1 << x]]
    if not changed:
        if any(delta): raise ValueError('non-atomic field change')
        return None
    if len(changed) != 1: raise ValueError('multiple singleton changes')
    x = changed[0]; sign = dd[1 << x]
    if sign not in (-1, 1): raise ValueError('invalid singleton magnitude')
    old = (1 << x) if sign == 1 else 0
    for y in range(k):
        if y != x:
            val = dd[(1 << x) | (1 << y)]
            if val not in (0, sign): raise ValueError('invalid pair change')
            if val == 0: old |= 1 << y
    new = old ^ (1 << x)
    expected = [b-a for a,b in zip(field([old],k),field([new],k))]
    if delta != expected: raise ValueError('inconsistent untouched coordinates')
    return {'label': x, 'direction': 'delete' if sign == 1 else 'add', 'before': old, 'after': new}

def produce():
    records = []
    for a,b,r,x,c in itertools.product(range(8), range(8), range(2), range(3), range(2)):
        f = [a,b]; g = f.copy()
        if c: g[r] ^= 1 << x
        before,after = field(f,3),field(g,3)
        delta = [v-u for u,v in zip(before,after)]
        records.append({'id':[a,b,r,x,c], 'before':before, 'after':after, 'decoded':decode(delta,3)})
    native = {'a':[56,88], 'b':[88,56], 'a_after':[184,88], 'b_after':[216,56],
              'dup':[56,56], 'dup0':[184,56], 'dup1':[56,184], 'batch_mid':[184,88], 'batch_end':[56,88]}
    return {'scope':SCOPE, 'records':records, 'native':native,
            'coverage':{'events':[[1,2,0,2,1],[5,2,1,0,1]],'final':[5,3]},
            'claims':{'root_address_decoded':False,'prospective_guard_derived':False,
                      'initial_count_access_derived':False,'batch_inversion_claimed':False}}

if __name__ == '__main__': print(json.dumps(produce(),sort_keys=True,separators=(',',':')))
