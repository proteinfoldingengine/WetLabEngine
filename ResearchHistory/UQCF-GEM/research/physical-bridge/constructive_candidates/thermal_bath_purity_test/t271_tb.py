"""T-271 frozen exact test: ingredient TB (thermal full-rank E, pure blank R). sympy exact; numpy/mpmath supplementary.
Basis order everywhere: S (o,p,u,v) x E x R. Frames on K are in (E,R) order, ket(e,r) = index e*2+r."""
import json, random, sys, itertools
import sympy as sp
import numpy as np
import mpmath as mp

out = {'python': sys.version.split()[0], 'sympy': sp.__version__, 'mpmath': mp.__version__, 'numpy': np.__version__, 'seed': 271}
R_ = sp.Rational
s2 = sp.sqrt(2)
o, p, u, v = 0, 1, 2, 3

def unit(n, i):
    m = sp.zeros(n, 1); m[i] = 1; return m

def kron(*ms):
    r = ms[0]
    for m in ms[1:]:
        r = sp.kronecker_product(r, m)
    return r

def ptrace(M, dims, keep):
    """partial trace of square matrix M on tensor dims, keeping list keep."""
    n = len(dims); kd = [dims[i] for i in keep]; D = int(np.prod(kd)) if kd else 1
    out_ = sp.zeros(D, D)
    for a in itertools.product(*[range(d) for d in dims]):
        for b in itertools.product(*[range(d) for d in dims]):
            if any(a[i] != b[i] for i in range(n) if i not in keep):
                continue
            ia = int(np.ravel_multi_index(a, dims)); ib = int(np.ravel_multi_index(b, dims))
            if M[ia, ib] == 0:
                continue
            ka = int(np.ravel_multi_index([a[i] for i in keep], kd)) if kd else 0
            kb = int(np.ravel_multi_index([b[i] for i in keep], kd)) if kd else 0
            out_[ka, kb] += M[ia, ib]
    return out_

def C(rho):
    Q = sp.diag(1, 1, 0, 1); L = sp.zeros(4, 4); L[p, u] = 1
    return Q * rho * Q + L * rho * L.T

def EU(i, j, n=4):
    m = sp.zeros(n, n); m[i, j] = 1; return m

def Phi(M, rho, sE, sR, dE, dR=2):
    big = kron(rho, sE, sR)
    om = M * big * M.H
    return ptrace(om, [4, dE, dR], [0])

def realizes(M, sE, sR, dE, dR=2):
    return all(sp.simplify(Phi(M, EU(i, j), sE, sR, dE, dR) - C(EU(i, j))) == sp.zeros(4, 4) for i in range(4) for j in range(4))

def perm_matrix(f, dE, dR=2):
    n = 4 * dE * dR; M = sp.zeros(n, n)
    for s in range(4):
        for e in range(dE):
            for r in range(dR):
                t = f(s, e, r)
                M[(t[0] * dE + t[1]) * dR + t[2], (s * dE + e) * dR + r] = 1
    assert M.T * M == sp.eye(n)
    return M

# ---- unitaries (d_E = 2)
def f_WR(s, e, r):  # W_R (x) I_E
    if (s, r) == (u, 0): return (p, e, 1)
    if (s, r) == (p, 1): return (u, e, 0)
    return (s, e, r)
def f_WE(s, e, r):  # canonical W_E (x) I_R : transposition |u,0>_SE <-> |p,1>_SE
    if (s, e) == (u, 0): return (p, 1, r)
    if (s, e) == (p, 1): return (u, 0, r)
    return (s, e, r)
def f_WR_swap(s, e, r):
    t = f_WR(s, e, r); return (t[0], t[2], t[1])
M_WR = perm_matrix(f_WR, 2); M_WE = perm_matrix(f_WE, 2); M_WRS = perm_matrix(f_WR_swap, 2)

def kv(e, r):
    m = sp.zeros(4, 1); m[e * 2 + r] = 1; return m
FR0 = {
    'W_E': (kv(0, 0), kv(1, 0)),
    'W_Bell': ((kv(0, 0) + kv(1, 1)) / s2, (kv(0, 0) - kv(1, 1)) / s2),
    'W_W': (kv(0, 0), (kv(0, 1) + kv(1, 0)) / s2),
}

def complement_frames(e0, eu):
    B = [e0, eu]
    def proj_out(x):
        y = x
        for b in B:
            y = y - b * (b.H * x)[0]
        return sp.simplify(y)
    cands0 = [kv(1, 0), kv(1, 1), kv(0, 1)]
    for c in cands0:
        y = proj_out(c)
        nn = sp.sqrt(sp.simplify((y.H * y)[0]))
        if nn != 0:
            f0 = sp.simplify(y / nn); break
    B.append(f0)
    for c in [kv(1, 1), kv(0, 1), kv(0, 0)]:
        y = proj_out(c)
        nn = sp.sqrt(sp.simplify((y.H * y)[0]))
        if nn != 0:
            fu = sp.simplify(y / nn); break
    return f0, fu

def frame_iso(frames_by_k):
    """16x16 matrix; columns with R-input 0 from frames; R-input 1 columns zero (only R=|0> inputs are used)."""
    M = sp.zeros(16, 16)
    for k, (f0, fu) in enumerate(frames_by_k):
        for s in range(4):
            col = (s * 2 + k) * 2 + 0
            sout, f = (p, fu) if s == u else (s, f0)
            vec = kron(unit(4, sout), f)
            M[:, col] = vec
    cols = [(s * 2 + k) * 2 for s in range(4) for k in range(2)]
    Ms = M[:, cols]
    assert sp.simplify(Ms.H * Ms) == sp.eye(8)
    return M

COMP = {}
for nm, (e0, eu) in FR0.items():
    f0, fu = complement_frames(e0, eu)
    COMP[nm + '^c'] = frame_iso([(e0, eu), (f0, fu)])
    out.setdefault('completion_frames', {})[nm + '^c'] = {'e1_0': [str(x) for x in f0], 'e1_u': [str(x) for x in fu]}

def dm(v):
    return v * v.H
tau_q = sp.diag(R_(2, 3), R_(1, 3)); tau_h = sp.diag(R_(1, 2), R_(1, 2)); blank = sp.diag(1, 0)
rho_star = sp.diag(0, R_(1, 2), R_(1, 2), 0)

def pval(M, sE, sR, dE, dR=2):
    return sp.nsimplify(sp.simplify(Phi(M, rho_star, sE, sR, dE, dR)[p, p]))

def KF(rho, tau, k):
    evs = sorted([a * b for a in [rho[i, i] for i in range(rho.shape[0])] for b in [tau[i, i] for i in range(tau.shape[0])]], reverse=True)
    return sum(evs[:k])

def tn_half(A):
    ev = A.eigenvals(); return sp.nsimplify(sp.simplify(sum(sp.Abs(x) * m for x, m in ev.items()) / 2))
zp = sp.diag(R_(1, 5), R_(1, 5), R_(2, 5), R_(1, 5)); zm = sp.diag(R_(1, 5), R_(1, 5), R_(1, 5), R_(2, 5))
def contrasts(M, sE, sR, dE=2):
    res = {}
    for name, keep in (('D_E', [1]), ('D_R', [2])):
        a = ptrace(M * kron(zp, sE, sR) * M.H, [4, dE, 2], keep); b = ptrace(M * kron(zm, sE, sR) * M.H, [4, dE, 2], keep)
        res[name] = str(tn_half(sp.simplify(a - b)))
    return res

def owner_equal(M, sE, sR, dE=2):
    a = ptrace(M * kron(dm(unit(4, p)), sE, sR) * M.H, [4, dE, 2], [1, 2]); b = ptrace(M * kron(dm(unit(4, v)), sE, sR) * M.H, [4, dE, 2], [1, 2])
    return bool(sp.simplify(a - b) == sp.zeros(a.shape[0]))

CTRL = {'W_R(x)I_E': M_WR, 'W_E_fixed_mirror(R-untouched)': M_WE, 'W_R;SWAP': M_WRS, **COMP}
res = {}
for tn, tau in (('tau_q=diag(2/3,1/3)', tau_q), ('tau_half=I/2', tau_h)):
    r = {}
    for nm, M in CTRL.items():
        r[nm] = {'realizes_C': realizes(M, tau, blank, 2), 'p_value_rho_star': str(pval(M, tau, blank, 2)), **contrasts(M, tau, blank), 'pi_p_pi_v_equal_K_states': owner_equal(M, tau, blank)}
    r['KF_bound_R_untouched'] = str(KF(rho_star, tau, 2))
    res[tn] = r
out['controls_TB'] = res

# jointly swapped mirror: tau on R, E pure blank
sw = {}
for nm, M in (('W_E(x)I_R', M_WE), ('W_R(x)I_E', M_WR)):
    sw[nm] = {'realizes_C': realizes(M, blank, tau_q, 2), 'p_value_rho_star': str(pval(M, blank, tau_q, 2))}
sw['KF_bound_E_untouched_in_swapped_world'] = str(KF(rho_star, tau_q, 2))
out['jointly_swapped_mirror_tau_q_on_R'] = sw

# threshold d_E = 4
def f_thr(shift_pairs):
    def f(s, e, r):
        for (a, b) in shift_pairs:
            if (s, e) == (u, a): return (p, b, r)
            if (s, e) == (p, b): return (u, a, r)
        return (s, e, r)
    return f
M_t = perm_matrix(f_thr([(0, 2), (1, 3)]), 4)
tau2 = sp.diag(R_(1, 2), R_(1, 2), 0, 0); tau3 = sp.diag(R_(1, 3), R_(1, 3), R_(1, 3), 0)
out['threshold_dE4'] = {
    'rank2_R_untouched_realizes_C': realizes(M_t, tau2, blank, 4),
    'rank2_KF': str(KF(rho_star, tau2, 4)),
    'rank3_construction_p_value': str(pval(M_t, tau3, blank, 4)),
    'rank3_KF': str(KF(rho_star, tau3, 4)),
}

# numpy Haar supplementary: R-untouched U_SE (8x8), d_E=2
rng = np.random.default_rng(271)
def haar(n):
    Z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    Qm, Rm = np.linalg.qr(Z); d = np.diag(Rm); return Qm * (d / abs(d))
hv = {}
for tn, t in (('tau_q', np.diag([2 / 3, 1 / 3])), ('tau_half', np.diag([.5, .5]))):
    rs = np.diag([0, .5, .5, 0]); big = np.kron(rs, t); Pp = np.kron(np.diag([0, 1, 0, 0]), np.eye(2)); mx = 0
    for _ in range(2000):
        U = haar(8); mx = max(mx, np.trace(Pp @ U @ big @ U.conj().T).real)
    hv[tn] = round(float(mx), 12)
out['haar_R_untouched_max_p_value'] = hv

# (iv) two events with fresh slots, permutation evaluator
def perm_channel_check(Sdim, envdims, envweights, f, Cref):
    """f maps (s, env tuple) -> (s', env'); env input distribution diagonal with weights. Returns equality with Cref on all matrix units."""
    envs = list(itertools.product(*[range(d) for d in envdims]))
    ok = True
    for a in range(Sdim):
        for b in range(Sdim):
            M = sp.zeros(Sdim, Sdim)
            for en in envs:
                w = envweights(en)
                if w == 0: continue
                sa, ea = f(a, en); sb, eb = f(b, en)
                if ea == eb: M[sa, sb] += w
            ok &= (M == Cref(EU(a, b, Sdim)))
    return bool(ok)
def pval_perm(Sdim, envdims, envweights, f, rho, target):
    envs = list(itertools.product(*[range(d) for d in envdims])); val = 0
    for s in range(Sdim):
        for en in envs:
            w = envweights(en) * rho[s, s]
            if w != 0 and f(s, en)[0] == target: val += w
    return val
# carrier A one-hot: o0 p1 1 u1 2 p2 3 u2 4 v 5 ; env (E, R1, R2)
def CA(rho):
    Q = sp.diag(1, 1, 0, 1, 0, 1); L1 = sp.zeros(6); L1[1, 2] = 1; L2 = sp.zeros(6); L2[3, 4] = 1
    return Q * rho * Q + L1 * rho * L1.T + L2 * rho * L2.T
def fA(s, en):
    e, r1, r2 = en
    if s == 2 and r1 == 0: s, r1 = 1, 1
    elif s == 1 and r1 == 1: s, r1 = 2, 0
    if s == 4 and r2 == 0: s, r2 = 3, 1
    elif s == 3 and r2 == 1: s, r2 = 4, 0
    return s, (e, r1, r2)
wq = lambda en: (R_(2, 3) if en[0] == 0 else R_(1, 3)) * (1 if all(x == 0 for x in en[1:]) else 0)
def fA_R0(s, en):  # R-untouched optimal: transposition (u1,E0)<->(p1,E1)
    e = en[0]
    if (s, e) == (2, 0): return 1, (1,) + en[1:]
    if (s, e) == (1, 1): return 2, (0,) + en[1:]
    return s, en
rA = sp.diag(0, R_(1, 2), R_(1, 2), 0, 0, 0)
# carrier B: S1 x S2 with S_k in (o,p,u,v); index s1*4+s2
def CB(rho):
    K1 = [sp.diag(1, 1, 0, 1), sp.zeros(4)]; K1[1][p, u] = 1
    out_ = sp.zeros(16)
    for A in K1:
        for B in K1:
            K = kron(A, B); out_ += K * rho * K.T
    return out_
def fB(s, en):
    e, r1, r2 = en; s1, s2 = divmod(s, 4)
    if s1 == u and r1 == 0: s1, r1 = p, 1
    elif s1 == p and r1 == 1: s1, r1 = u, 0
    if s2 == u and r2 == 0: s2, r2 = p, 1
    elif s2 == p and r2 == 1: s2, r2 = u, 0
    return s1 * 4 + s2, (e, r1, r2)
def fB_R0(s, en):  # R-untouched: (u1p2, E0) <-> (p1p2, E1)
    e = en[0]; a = u * 4 + p; b = p * 4 + p
    if (s, e) == (a, 0): return b, (1,) + en[1:]
    if (s, e) == (b, 1): return a, (0,) + en[1:]
    return s, en
rB = sp.zeros(16)
for s1 in (p, u):
    for s2 in (p, u):
        rB[s1 * 4 + s2, s1 * 4 + s2] = R_(1, 4)
out['two_event_fresh_slots_tau_q'] = {
    'A_WR_slots_(x)I_E_realizes_C1C2': perm_channel_check(6, [2, 2, 2], wq, fA, CA),
    'A_R_untouched_construction_p_value': str(pval_perm(6, [2, 2, 2], wq, fA_R0, rA, 1)),
    'A_KF': str(KF(rA, tau_q, 2)),
    'B_WR_slots_(x)I_E_realizes_C1C2': perm_channel_check(16, [2, 2, 2], wq, fB, CB),
    'B_R_untouched_construction_p_value': str(pval_perm(16, [2, 2, 2], wq, fB_R0, rB, p * 4 + p)),
    'B_KF': str(KF(rB, tau_q, 2)),
}
# owner illustration (2): carrier A, pure E append register dim 3, no R
def fA_E3(s, en):
    if s == 2: return 1, (1,)
    if s == 4: return 3, (2,)
    return s, (0,)
out['owner_illustration_A_E_register'] = {'realizes_C1C2': perm_channel_check(6, [1], lambda en: 1, lambda s, en: fA_E3(s, en), CA),
                                         'erased_address_records_orthogonal': True}

# Q-2 consistency, tau_half, mpmath
mp.mp.dps = 50
rg = random.Random(271)
def tomp(M):
    def cv(x):
        x = sp.N(x, 60); return mp.mpc(mp.mpf(str(sp.re(x))), mp.mpf(str(sp.im(x))))
    return mp.matrix([[cv(M[i, j]) for j in range(M.shape[1])] for i in range(M.shape[0])])
def mpS(M):
    ev = mp.eigh(M)[0]
    return -mp.fsum([x * mp.log(x, 2) for x in ev if x > mp.mpf(10) ** -45])
def mp_rand(rank):
    A = mp.matrix(4, rank)
    for i in range(4):
        for j in range(rank):
            A[i, j] = mp.mpc(rg.gauss(0, 1), rg.gauss(0, 1))
    r = A * A.transpose_conj(); t = sum(r[i, i] for i in range(4)); return r / t
def mp_ptrace(M, dims, keep):
    n = len(dims); kd = [dims[i] for i in keep]; D = int(np.prod(kd))
    o_ = mp.matrix(D, D)
    for a in itertools.product(*[range(d) for d in dims]):
        for b in itertools.product(*[range(d) for d in dims]):
            if any(a[i] != b[i] for i in range(n) if i not in keep): continue
            o_[int(np.ravel_multi_index([a[i] for i in keep], kd)), int(np.ravel_multi_index([b[i] for i in keep], kd))] += M[int(np.ravel_multi_index(a, dims)), int(np.ravel_multi_index(b, dims))]
    return o_
def mp_C(r):
    Q = mp.diag([1, 1, 0, 1]); L = mp.matrix(4, 4); L[p, u] = 1
    return Q * r * Q + L * r * L.transpose_conj()
inputs = [mp_rand(1 + t % 4) for t in range(200)] + [mp.diag([0, mp.mpf(1) / 2, mp.mpf(1) / 2, 0]), mp.diag([mp.mpf(1) / 5] * 2 + [mp.mpf(2) / 5, mp.mpf(1) / 5])]
envh = tomp(kron(tau_h, blank))
q2 = {}
for nm, M in CTRL.items():
    if nm.startswith('W_E_fixed'): continue
    Mm = tomp(M); mn = mp.mpf(9)
    for r in inputs:
        big = mp.matrix(16, 16)
        for i in range(4):
            for j in range(4):
                for a in range(4):
                    for b in range(4):
                        big[i * 4 + a, j * 4 + b] = r[i, j] * envh[a, b]
        om = Mm * big * Mm.transpose_conj()
        dS = mpS(r) - mpS(mp_C(r)); mn = min(mn, mpS(mp_ptrace(om, [4, 2, 2], [2])) - dS)
    q2[nm] = {'min_slack_S_R_minus_dS': mp.nstr(mn, 12), 'holds': bool(mn > -mp.mpf(10) ** -30)}
out['Q2_consistency_tau_half'] = q2

# verdicts
cq, ch = out['controls_TB']['tau_q=diag(2/3,1/3)'], out['controls_TB']['tau_half=I/2']
a_ok = cq['W_R(x)I_E']['realizes_C'] and ch['W_R(x)I_E']['realizes_C']
b_ok = (cq['W_E_fixed_mirror(R-untouched)']['p_value_rho_star'] == cq['KF_bound_R_untouched'] == '2/3' and ch['W_E_fixed_mirror(R-untouched)']['p_value_rho_star'] == ch['KF_bound_R_untouched'] == '1/2'
        and not cq['W_E_fixed_mirror(R-untouched)']['realizes_C'] and not ch['W_E_fixed_mirror(R-untouched)']['realizes_C']
        and hv['tau_q'] <= 2 / 3 + 1e-12 and hv['tau_half'] <= 0.5 + 1e-12)
t = out['threshold_dE4']; c_ok = t['rank2_R_untouched_realizes_C'] and t['rank2_KF'] == '1' and t['rank3_construction_p_value'] == t['rank3_KF'] == '2/3'
iv = out['two_event_fresh_slots_tau_q']; iv_ok = iv['A_WR_slots_(x)I_E_realizes_C1C2'] and iv['B_WR_slots_(x)I_E_realizes_C1C2'] and iv['A_R_untouched_construction_p_value'] == iv['A_KF'] == '2/3' and iv['B_R_untouched_construction_p_value'] == iv['B_KF'] == '1/3'
out['Q1'] = {'a': bool(a_ok), 'b': bool(b_ok), 'c': bool(c_ok), 'iv_consistency': bool(iv_ok), 'verdict': 'PASS' if (a_ok and b_ok and c_ok) else 'FAIL'}
out['QL_record_location'] = {'W_R;SWAP_realizes_C_both_tau': bool(cq['W_R;SWAP']['realizes_C'] and ch['W_R;SWAP']['realizes_C']),
                             'W_R;SWAP_contrasts_tau_q': {k: cq['W_R;SWAP'][k] for k in ('D_E', 'D_R')},
                             'verdict': 'NOT ADMISSIBLE (record location not fixed by TB; Lemma PP)'}
out['Q2'] = 'consistency only (forced): ' + ('holds for all' if all(x['holds'] for x in q2.values()) else 'VIOLATED')
print(json.dumps(out, indent=1, sort_keys=True))
