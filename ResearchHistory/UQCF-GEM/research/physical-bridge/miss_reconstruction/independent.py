import json
import sys
from pins import SCOPE

def compositions(total, slots):
    if slots == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total-first, slots-1):
                yield (first,) + rest

def zeta(family, k, d):
    a = [0] * (1 << k)
    for support in family: a[((1 << k)-1) ^ support] += 1
    for bit in range(k):
        for mask in range(1 << k):
            if not (mask & (1 << bit)): a[mask] += a[mask | (1 << bit)]
    return [a[h] for h in range(1 << k) if bin(h).count('1') <= d]

def hitting(roots):
    if not roots: return 0
    first = min(roots, key=len)
    return 1 + min(hitting([r for r in roots if x not in r]) for x in first)

def check(data):
    expected = []
    for n in range(5):
        for counts in compositions(n, 8):
            f = [s for s, count in enumerate(counts) for _ in range(count)]
            for d in range(4):
                expected.append({'d': d, 'n': n, 'supports': f, 'moments': zeta(f, 3, d)})
    expected.sort(key=lambda r: (r['d'], r['n'], r['supports']))
    even, odd = [], []
    for s in range(32):
        parity = 0
        for bit in range(5): parity ^= (s >> bit) & 1
        (odd if parity else even).append(s)
    native = [[24 + 32*s for s in f] for f in (even, odd)]
    certificate = {'scope': SCOPE, 'records': expected,
                   'parity': {'even': even, 'odd': odd,
                              'native_moments': [zeta(f, 10, 4) for f in native]},
                   'claims': {'labelled_assignment_recovered': False,
                              'initialization_derived': False,
                              'full_palette_required': True, 'known_N_required': True}}
    if data != certificate: raise ValueError('exact canonical identity/value/provenance mismatch')
    minima = {str(d): None for d in range(4)}
    seen = {}
    for row in expected:
        key = (row['d'], row['n'], tuple(row['moments']))
        if key in seen and seen[key] != row['supports']:
            old = minima[str(row['d'])]
            minima[str(row['d'])] = row['n'] if old is None else min(old, row['n'])
        seen[key] = row['supports']
    if minima != {'0': 1, '1': 2, '2': 4, '3': None}: raise ValueError('unexpected collision boundary')
    if certificate['parity']['native_moments'][0] != certificate['parity']['native_moments'][1]:
        raise ValueError('parity moments differ')
    taus = []
    for f in native:
        roots = [{i for i in range(10) if (s >> i) & 1} for s in [3, 6, 5]+f]
        if any(len(r) < 2 for r in roots): raise ValueError('native floor violation')
        taus.append(hitting(roots))
    if taus != [3, 3] or even == odd: raise ValueError('invalid native boundary')
    # Without N, full-palette supports are invisible to every nonempty miss query.
    if zeta([7], 3, 3)[1:] != zeta([7, 7], 3, 3)[1:]: raise ValueError('N control')
    # The aggregate record is invariant under a nontrivial labelled-slot swap.
    if zeta([1, 2], 3, 3) != zeta([2, 1], 3, 3): raise ValueError('address control')
    return {'status': 'PASS_BOUNDED_NOT_GENERAL_PROOF', 'records': len(expected),
            'families': len(expected)//4, 'minimum_collision_size': minima,
            'native': {'tau': taus, 'residuals_per_world': 16,
                       'roots_per_world': 19, 'nonempty_queries': len(zeta(native[0], 10, 4))-1}}

if __name__ == '__main__':
    print(json.dumps(check(json.load(open(sys.argv[1]))), sort_keys=True, indent=2))
