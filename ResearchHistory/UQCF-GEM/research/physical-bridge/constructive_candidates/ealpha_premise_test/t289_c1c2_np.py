"""T-289 J2 independent checker (numpy only). Builds the composite channel C1C2 directly from its action on
matrix units (no Kraus family), takes Choi rank by SVD (tol 1e-10), builds witnesses as permutation matrices,
and evaluates C2 on the 1771-point rational simplex grid (denominator 20) plus two named points.
Usage: t289_c1c2_np.py [producer.json]   (with a producer file: compare verdicts and coverage)
       t289_c1c2_np.py --control R3|R4|R5   (rejecting controls; prints REJECTED/ACCEPTED)"""
import json, sys, itertools
import numpy as np
TOL = 1e-10
REQUIRED = ['C1_i_A_rank3', 'C1_i_B_rank4', 'C1_ii_qutrit_witness', 'C1_iii_N1_rank_N+1', 'C1_iii_N2_rank_N+1',
            'C1_iii_N3_rank_N+1', 'C1_iv_E_mirror_same', 'C2_i_cov_eq_zu(zo+zv)', 'C2_ii_slack_eq_I(A;B)',
            'C2_iii_a_slack0', 'C2_iii_b_slack1bit']

def one_event_on_unit(s, t, parent, erased):
    """C_k(|s><t|) for labels: erased diagonal moves to parent, erased coherences die."""
    if s != erased and t != erased: return [((s, t), 1.0)]
    if s == erased and t == erased: return [((parent(s), parent(t)), 1.0)]
    return []

def channel_matrix(S, events):
    """superoperator on vec(rho) of the composition of events (applied in order)."""
    n = len(S); ix = {s: i for i, s in enumerate(S)}
    M = np.zeros((n * n, n * n))
    for s in S:
        for t in S:
            cur = [((s, t), 1.0)]
            for (parent, erased_of) in events:
                nxt = []
                for (a, b), c in cur:
                    ea = erased_of(a); eb = erased_of(b)
                    if not ea and not eb: nxt.append(((a, b), c))
                    elif ea and eb: nxt.append(((parent(a), parent(b)), c))
                cur = nxt
            for (a, b), c in cur:
                M[ix[a] * n + ix[b], ix[s] * n + ix[t]] += c
    return M

def choi_rank(S, events):
    n = len(S); ix = {s: i for i, s in enumerate(S)}
    M = channel_matrix(S, events)
    J = np.zeros((n * n, n * n))
    for s in S:
        for t in S:
            out = M[:, ix[s] * n + ix[t]].reshape(n, n)
            J += np.kron(np.outer(np.eye(n)[ix[s]], np.eye(n)[ix[t]]), out)
    sv = np.linalg.svd(J, compute_uv=False)
    return int((sv > TOL * max(1.0, sv[0])).sum()), M

X = ['o', 'p', 'u', 'v']
A_S = ['o', 'p1', 'u1', 'p2', 'u2', 'v']
evA = [(lambda s: 'p1' if s == 'u1' else s, lambda s: s == 'u1'), (lambda s: 'p2' if s == 'u2' else s, lambda s: s == 'u2')]
B_S = [(a, b) for a in X for b in X]
def evB(i):
    return (lambda s: tuple('p' if (j == i and s[j] == 'u') else s[j] for j in range(2)), lambda s: s[i] == 'u')

def witness(write_to, U2slot=2, S=A_S):
    nS = len(S); dW, dO = 3, 2
    def lab(i, w): return (i, 0, w) if write_to == 'R' else (i, w, 0)
    dims = (nS, dO, dW) if write_to == 'R' else (nS, dW, dO)
    basis = list(itertools.product(range(dims[0]), range(dims[1]), range(dims[2])))
    ix = {b: n for n, b in enumerate(basis)}; N = len(basis)
    si = {s: i for i, s in enumerate(S)}
    def perm(a, b):
        P = np.eye(N); P[[ix[a], ix[b]]] = P[[ix[b], ix[a]]]; return P
    U1 = perm(lab(si['u1'], 0), lab(si['p1'], 1))
    U2 = perm(lab(si['u2'], 0), lab(si['p2'], U2slot))
    U = U1 @ U2
    _, M = choi_rank(S, evA)
    ok_ch, ok_other, maxdev = True, True, 0.0
    test_inputs = [np.outer(np.eye(nS)[i], np.eye(nS)[j]) for i in range(nS) for j in range(nS)]
    psi = np.zeros(nS); psi[si['u1']] = psi[si['u2']] = 1 / np.sqrt(2)
    test_inputs.append(np.outer(psi, psi))
    for rho in test_inputs:
        full = np.zeros((N, N))
        for i in range(nS):
            for j in range(nS):
                if rho[i, j] != 0:
                    full[ix[lab(i, 0)], ix[lab(j, 0)]] = rho[i, j]
        ev = (U @ full @ U.T).reshape(dims + dims)
        if write_to == 'R':
            redS = np.einsum('aebceb->ac', ev); redO = np.einsum('aebafb->ef', ev)
        else:
            redS = np.einsum('awbcwb->ac', ev); redO = np.einsum('awbawd->bd', ev)
        want = (M @ rho.reshape(-1)).reshape(nS, nS)
        maxdev = max(maxdev, float(np.abs(redS - want).max()))
        ok_ch &= np.allclose(redS, want, atol=TOL)
        w0 = np.zeros((2, 2)); w0[0, 0] = np.trace(rho)
        ok_other &= np.allclose(redO, w0, atol=TOL)
    return {'commute': bool(np.allclose(U1 @ U2, U2 @ U1)), 'channel_eq': bool(ok_ch),
            'other_untouched': bool(ok_other), 'max_dev': maxdev}

def hb(x):
    return 0.0 if x <= 0 or x >= 1 else float(-x * np.log2(x) - (1 - x) * np.log2(1 - x))
def slack(z):
    zo, zp, zu, zv = z
    return hb(zu) - ((zp + zu) * hb(zu / (zp + zu)) if zp + zu > 0 else 0.0)
def mutual_info(z):
    zo, zp, zu, zv = z
    joint = {(1, 1): zu, (0, 1): zp, (0, 0): zo + zv, (1, 0): 0.0}
    pa = {1: zu, 0: 1 - zu}; pb = {1: zp + zu, 0: zo + zv}
    return sum(p * np.log2(p / (pa[x] * pb[y])) for (x, y), p in joint.items() if p > 0)
GRID = [tuple(np.array(c) / 20.0) for c in itertools.product(range(21), repeat=4) if sum(c) == 20]

def compute():
    r = {}
    rA, _ = choi_rank(A_S, evA); rB, _ = choi_rank(B_S, [evB(0), evB(1)])
    r['choi_rank_C1C2'] = {'A': rA, 'B': rB}
    wR = witness('R'); wE = witness('E')
    r['witness_R'] = wR; r['witness_E_mirror'] = wE
    ranks = {}
    for Nn in (1, 2, 3):
        S = ['o'] + [f'p{i}' for i in range(1, Nn + 1)] + [f'u{i}' for i in range(1, Nn + 1)] + ['v']
        evs = [((lambda k: (lambda s: f'p{k}' if s == f'u{k}' else s))(k), (lambda k: (lambda s: s == f'u{k}'))(k)) for k in range(1, Nn + 1)]
        ranks[str(Nn)] = choi_rank(S, evs)[0]
    r['disjoint_erasure_choi_rank'] = ranks
    cov_ok = all(abs((z[2] - z[2] * (z[1] + z[2])) - z[2] * (z[0] + z[3])) < 1e-12 for z in GRID)
    mi_ok = all(abs(slack(z) - mutual_info(z)) < 1e-12 for z in GRID)
    eq_ok = all((abs(slack(z)) < 1e-12) == (z[2] == 0 or z[0] + z[3] == 0) for z in GRID)
    s1 = slack((0, .5, .5, 0)); s2 = slack((0, 0, .5, .5))
    r['grid_points'] = len(GRID); r['C2_equality_iff_on_grid'] = bool(eq_ok)
    r['slack_bits'] = {'(0,1/2,1/2,0)': s1, '(0,0,1/2,1/2)': s2}
    v = {'C1_i_A_rank3': rA == 3, 'C1_i_B_rank4': rB == 4,
         'C1_ii_qutrit_witness': wR['commute'] and wR['channel_eq'] and wR['other_untouched'],
         'C1_iv_E_mirror_same': wE['commute'] and wE['channel_eq'] and wE['other_untouched'],
         'C2_i_cov_eq_zu(zo+zv)': cov_ok, 'C2_ii_slack_eq_I(A;B)': mi_ok,
         'C2_iii_a_slack0': abs(s1) < 1e-12, 'C2_iii_b_slack1bit': abs(s2 - 1) < 1e-12}
    for Nn in (1, 2, 3): v[f'C1_iii_N{Nn}_rank_N+1'] = ranks[str(Nn)] == Nn + 1
    r['verdicts'] = {k: bool(x) for k, x in v.items()}
    return r

def compare(prod, mine):
    pv = prod.get('verdicts', {}); errs = []
    for k in REQUIRED:
        if k not in pv: errs.append(f'missing {k}')
        elif pv[k] is not True or mine['verdicts'][k] is not True: errs.append(f'{k}: producer {pv[k]} checker {mine["verdicts"][k]}')
    if prod.get('choi_rank_C1C2') != mine['choi_rank_C1C2']: errs.append('choi_rank_C1C2 mismatch')
    if prod.get('disjoint_erasure_choi_rank') != mine['disjoint_erasure_choi_rank']: errs.append('disjoint ranks mismatch')
    return errs

def control(name):
    if name == 'R3':  # withdrawn disjunct predicts equality at (0,0,1/2,1/2); refuted iff slack != 0
        return 'REJECTED' if abs(slack((0, 0, .5, .5))) > 1e-12 else 'ACCEPTED'
    if name == 'R4':  # qubit receiver: realizable only if rank <= 2
        return 'REJECTED' if choi_rank(A_S, evA)[0] > 2 else 'ACCEPTED'
    if name == 'R5':  # wrong witness: second event written into slot 1
        return 'REJECTED' if not witness('R', U2slot=1)['channel_eq'] else 'ACCEPTED'
    raise SystemExit('unknown control')

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--control':
        print(control(sys.argv[2])); sys.exit(0)
    mine = compute(); mine['numpy'] = np.__version__; mine['script'] = 't289_c1c2_np.py'
    if len(sys.argv) == 2:
        errs = compare(json.load(open(sys.argv[1])), mine)
        mine['comparison_errors'] = errs; mine['agree'] = not errs
        print(json.dumps(mine, indent=1, sort_keys=True)); sys.exit(0 if not errs else 1)
    print(json.dumps(mine, indent=1, sort_keys=True)); sys.exit(0 if all(mine['verdicts'].values()) else 1)
