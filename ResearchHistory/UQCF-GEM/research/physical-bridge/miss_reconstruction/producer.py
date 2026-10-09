import itertools
import json
from pins import SCOPE

def moments(supports, k, d):
    return [sum(not (s & h) for s in supports)
            for h in range(1 << k) if h.bit_count() <= d]

def produce():
    records = []
    for d in range(4):
        for n in range(5):
            for family in itertools.combinations_with_replacement(range(8), n):
                records.append({'d': d, 'n': n, 'supports': list(family),
                                'moments': moments(family, 3, d)})
    even = [s for s in range(32) if s.bit_count() % 2 == 0]
    odd = [s for s in range(32) if s.bit_count() % 2 == 1]
    worlds = [[3, 6, 5] + [24 | (s << 5) for s in f] for f in (even, odd)]
    return {'scope': SCOPE, 'records': records,
            'parity': {'even': even, 'odd': odd,
                       'native_moments': [moments(w[3:], 10, 4) for w in worlds]},
            'claims': {'labelled_assignment_recovered': False,
                       'initialization_derived': False,
                       'full_palette_required': True, 'known_N_required': True}}

if __name__ == '__main__': print(json.dumps(produce(), sort_keys=True, separators=(',', ':')))
