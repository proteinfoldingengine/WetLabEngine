"""Exact certificate of the already identified C2 counterexample and E3 control."""
import json
import sympy as s

Q = s.diag(1, 1, 0, 1, 0, 1)
L1 = s.zeros(6); L1[1, 2] = 1
L2 = s.zeros(6); L2[3, 4] = 1
ks = [Q, L1, L2]
gram = s.Matrix([[(a.T*b).trace() for b in ks] for a in ks])
rank = gram.rank()
spectrum = sorted([int(v) for v, n in gram.eigenvals().items() for _ in range(n) if v != 0], reverse=True)
perm = list(range(18))
for source, bath_target, owner in [(2, 1, 1), (4, 2, 3)]:
    a, b = source*3, owner*3+bath_target
    perm[a], perm[b] = perm[b], perm[a]
U = s.zeros(18)
for col, row in enumerate(perm):
    U[row, col] = 1
assert U.T*U == s.eye(18)
derived = [s.Matrix(6, 6, lambda i,j: U[i*3+e, j*3]) for e in range(3)]
assert derived == ks
actions = []
for i in range(6):
    for j in range(6):
        x = s.zeros(6); x[i, j] = 1
        y = sum((k*x*k.T for k in derived), s.zeros(6))
        assert y == sum((k*x*k.T for k in ks), s.zeros(6))
        actions.append([[a, b, int(y[a,b])] for a in range(6) for b in range(6) if y[a,b] != 0])
cases = []
for d in (2,3):
    cases.append({'id': f'A-pure-E{d}', 'dE':d, 'rank_tau':1, 'fan_in':[2,2],
        'local_bound_satisfied': 2 <= d, 'pure_kraus_capacity': d,
        'realizable_R_untouched': False if d < rank else derived == ks,
        'witness': None if d == 2 else {'permutation':perm, 'matrix_unit_actions':actions}})
print(json.dumps({'schema':'thermal-C2-v1', 'provenance':{'scope':'SUPPLIED_CHANNEL',
    'native_bridge':'NOT_DERIVED', 'original_head':'23543a5b8c5f8938fe0d25c42be975296c8055fb'},
    'choi_rank':rank,'nonzero_choi_spectrum':spectrum,'cases':cases}, indent=2,sort_keys=True))
