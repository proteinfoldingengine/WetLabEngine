"""T-289 J2 producer (PR #130 remediation). Exact sympy checks of the corrected claims C1, C2 of
CORRECTIONS_T275.md, frozen in PROSPECTIVE_REMEDIATION_PLAN_T289.md (grok/ealpha-premise-test 8e95288d).
Prints one JSON document. Supporting mathematics inside the SUPPLIED benchmark; nothing here upgrades any
status (sharp E-alpha NEW ASSUMPTION, native receiver delivery NOT_DERIVED)."""
import json, sys
import sympy as sp

R = sp.Rational
out = {"script": "t289_c1c2.py", "sympy": sp.__version__, "python": sys.version.split()[0]}
V = {}

# ---------------- carriers ----------------
X = ['o', 'p', 'u', 'v']
A_S = ['o', 'p1', 'u1', 'p2', 'u2', 'v']
B_S = [(a, b) for a in X for b in X]
def ev_A(k):  # (parent, erased) of event k on carrier A
    return {1: ('p1', 'u1'), 2: ('p2', 'u2')}[k]
def P_A(k, s):
    p, u = ev_A(k); return p if s == u else s
def er_A(k, s):
    return s == ev_A(k)[1]
def P_B(k, s):
    s = list(s)
    if s[k - 1] == 'u': s[k - 1] = 'p'
    return tuple(s)
def er_B(k, s):
    return s[k - 1] == 'u'

def kraus_event(S, P, er, k):
    n = len(S); idx = {s: i for i, s in enumerate(S)}
    Q = sp.zeros(n); L = sp.zeros(n)
    for s in S:
        if er(k, s): L[idx[P(k, s)], idx[s]] = 1
        else: Q[idx[s], idx[s]] = 1
    return [Q, L]

def kraus_rank(mats):
    """rank of the Gram matrix G_ij = Tr(K_i^dag K_j) = Choi rank of sum_i K_i . K_i^dag"""
    G = sp.Matrix(len(mats), len(mats), lambda i, j: (mats[i].H * mats[j]).trace())
    return int(G.rank())

def composite(S, P, er, events):
    ks = [sp.eye(len(S))]
    for k in events:
        ks = [b * a for a in ks for b in kraus_event(S, P, er, k)]
    return ks

def chan(ks, rho):
    acc = sp.zeros(rho.rows)
    for K in ks: acc += K * rho * K.H
    return acc

# C1(i)
rA = kraus_rank(composite(A_S, P_A, er_A, [1, 2])); rB = kraus_rank(composite(B_S, P_B, er_B, [1, 2]))
out['choi_rank_C1C2'] = {'A': rA, 'B': rB}
V['C1_i_A_rank3'] = rA == 3
V['C1_i_B_rank4'] = rB == 4

# C1(ii)/(iv): witness U_i = swap(|u_i,0>, |p_i,i>) on S (x) W, W a qutrit (R for (ii), E for (iv));
# the other register is a qubit held at |0> and must be untouched.
def witness_check(write_to):
    S = A_S; nS = len(S); dW = 3; dO = 2
    # ordering: (s, e, r); write register W is r if write_to=='R' else e
    dims = (nS, dO, dW) if write_to == 'R' else (nS, dW, dO)
    basis = [(i, a, b) for i in range(nS) for a in range(dims[1]) for b in range(dims[2])]
    idx = {t: n for n, t in enumerate(basis)}; N = len(basis)
    def wslot(t): return t[2] if write_to == 'R' else t[1]
    def mk(i, w):
        return (i, 0, w) if write_to == 'R' else (i, w, 0)
    def swap_U(a, b):
        U = sp.eye(N); ia, ib = idx[a], idx[b]
        U[ia, ia] = 0; U[ib, ib] = 0; U[ia, ib] = 1; U[ib, ia] = 1
        return U
    si = {s: i for i, s in enumerate(S)}
    U1 = swap_U(mk(si['u1'], 0), mk(si['p1'], 1)); U2 = swap_U(mk(si['u2'], 0), mk(si['p2'], 2))
    res = {'commute': (U1 * U2 - U2 * U1) == sp.zeros(N)}
    U = U1 * U2
    # Kraus <k|U|0_W> on S, other register at 0
    K = []
    for k in range(dW):
        M = sp.zeros(nS)
        for i in range(nS):
            for j in range(nS):
                M[i, j] = U[idx[mk(i, k)], idx[mk(j, 0)]]
        K.append(M)
    ksC = composite(A_S, P_A, er_A, [1, 2])
    expect = [ksC[0], None, None]  # Q1Q2 then the two jumps
    def proj(a, b):
        M = sp.zeros(nS); M[si[a], si[b]] = 1; return M
    res['kraus_match'] = (K[0] == kraus_event(A_S, P_A, er_A, 1)[0] * kraus_event(A_S, P_A, er_A, 2)[0]
                          and K[1] == proj('p1', 'u1') and K[2] == proj('p2', 'u2'))
    ok_ch = True; ok_other = True
    for i in range(nS):
        for j in range(nS):
            rho = sp.zeros(nS); rho[i, j] = 1
            ok_ch &= chan(K, rho) == chan(ksC, rho)
            # full evolution of |i><j| (x) |0><0| (x) |0><0|, reduce onto the untouched register
            vi = U[:, idx[mk(i, 0)]]; vj = U[:, idx[mk(j, 0)]]
            red = sp.zeros(2)
            for x in range(N):
                for y in range(N):
                    tx, ty = basis[x], basis[y]
                    ox = tx[1] if write_to == 'R' else tx[2]; oy = ty[1] if write_to == 'R' else ty[2]
                    rest_x = (tx[0], wslot(tx)); rest_y = (ty[0], wslot(ty))
                    if rest_x == rest_y and (vi[x] != 0 and vj[y] != 0):
                        red[ox, oy] += vi[x] * vj[y]
            want = sp.zeros(2); want[0, 0] = 1 if i == j else 0
            ok_other &= red == want
    res['channel_eq_C1C2_all_matrix_units'] = bool(ok_ch)
    res['other_register_untouched'] = bool(ok_other)
    res['rank'] = kraus_rank(K)
    return res
wR = witness_check('R'); wE = witness_check('E')
out['witness_R'] = {k: (bool(v) if not isinstance(v, int) or isinstance(v, bool) else v) for k, v in wR.items()}
out['witness_E_mirror'] = {k: (bool(v) if not isinstance(v, int) or isinstance(v, bool) else v) for k, v in wE.items()}
V['C1_ii_qutrit_witness'] = bool(wR['commute'] and wR['kraus_match'] and wR['channel_eq_C1C2_all_matrix_units'] and wR['other_register_untouched'])
V['C1_iv_E_mirror_same'] = bool(wE['commute'] and wE['kraus_match'] and wE['channel_eq_C1C2_all_matrix_units'] and wE['other_register_untouched'] and wE['rank'] == wR['rank'] == rA)

# C1(iii): N disjoint one-hot erasures on o, p_1..p_N, u_1..u_N, v
ranks = {}
for Nn in (1, 2, 3):
    S = ['o'] + [f'p{i}' for i in range(1, Nn + 1)] + [f'u{i}' for i in range(1, Nn + 1)] + ['v']
    P = lambda k, s: f'p{k}' if s == f'u{k}' else s
    er = lambda k, s: s == f'u{k}'
    ranks[str(Nn)] = kraus_rank(composite(S, P, er, list(range(1, Nn + 1))))
    V[f'C1_iii_N{Nn}_rank_N+1'] = ranks[str(Nn)] == Nn + 1
out['disjoint_erasure_choi_rank'] = ranks

# C2
zo, zp, zu, zv = sp.symbols('z_o z_p z_u z_v', positive=True)
cov = zu - zu * (zp + zu)  # P(A and B) - P(A)P(B), A={u} subset B={p,u}
V['C2_i_cov_eq_zu(zo+zv)'] = sp.simplify((cov - zu * (zo + zv)).subs(zv, 1 - zo - zp - zu)) == 0
a, b = zu, zp; c = 1 - zu - zp
h = lambda x: -x * sp.log(x) - (1 - x) * sp.log(1 - x)
slack = h(a) - (a + b) * h(a / (a + b))
joint = {(1, 1): a, (0, 1): b, (0, 0): c}
pA = {1: a, 0: 1 - a}; pB = {1: a + b, 0: c}
MI = sum(p * sp.log(p / (pA[x] * pB[y])) for (x, y), p in joint.items())
diff = sp.expand_log(sp.expand(slack - MI), force=True)
V['C2_ii_slack_eq_I(A;B)'] = sp.simplify(diff) == 0
def slack_bits(z):
    o_, p_, u_, v_ = [R(x) for x in z]
    def hb(x):
        x = R(x)
        return sum((-t * sp.log(t, 2) for t in (x, 1 - x) if t != 0), sp.Integer(0))
    s = hb(u_) - ((p_ + u_) * hb(u_ / (p_ + u_)) if p_ + u_ != 0 else 0)
    return sp.nsimplify(sp.simplify(s))
s1 = slack_bits((0, R(1, 2), R(1, 2), 0)); s2 = slack_bits((0, 0, R(1, 2), R(1, 2)))
out['slack_bits'] = {'(0,1/2,1/2,0)': str(s1), '(0,0,1/2,1/2)': str(s2)}
V['C2_iii_a_slack0'] = s1 == 0
V['C2_iii_b_slack1bit'] = s2 == 1

out['verdicts'] = {k: bool(v) for k, v in V.items()}
out['all_true'] = all(out['verdicts'].values())
print(json.dumps(out, indent=1, sort_keys=True))
