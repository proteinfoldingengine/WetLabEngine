"""Successor producer (sympy) for CORRECTION_T241 section 4 (V1-V5) and CORRECTION_T242 section 4 (V6, V6b, V7).
Deterministic; no randomness. Emits a JSON certificate on stdout. Plan frozen before this file existed
(CORRECTION_T241 at 8157f7b4, CORRECTION_T242 at e16a7b79)."""
import hashlib, json, sys
from pathlib import Path
import sympy as sp

R = sp.Rational
O, P, U, V = 0, 1, 2, 3          # H_S basis o, p, u, v
KD = 4                            # K = E (x) R, index 2e + r


def kv(*pairs):
    v = sp.zeros(KD, 1)
    for c, i in pairs:
        v[i] += c
    return v


def sv(i):
    v = sp.zeros(4, 1); v[i] = 1; return v


def iso(e0, eu):
    W = sp.zeros(16, 4)
    for j in range(4):
        W[:, j] = sp.kronecker_product(sv(P), eu) if j == U else sp.kronecker_product(sv(j), e0)
    return W


def channel_C(X):
    Y = sp.zeros(4, 4)
    for a in (O, P, V):
        for b in (O, P, V):
            Y[a, b] = X[a, b]
    Y[P, P] += X[U, U]
    return Y


def trK(M):
    return sp.Matrix(4, 4, lambda a, b: sum(M[a * KD + k, b * KD + k] for k in range(KD)))


def theta_real(c):
    s = sp.sqrt(1 - c ** 2)
    return (kv((1, 0)), kv((c, 2), (s, 1)))   # e_u = c a0(x)b1 + s a1(x)b0 ; a=R, b=E


REAL = {
    'W_E': (kv((1, 0)), kv((1, 2))),
    'W_R': (kv((1, 0)), kv((1, 1))),
    'W_c3_5': theta_real(R(3, 5)),
    'W_c4_5': theta_real(R(4, 5)),
    'W_N': (kv((R(3, 5), 0), (R(4, 5), 3)), kv((1, 1))),
    'W_X': (kv((1, 3)), kv((1, 0))),
}
THETA = {'1': 'W_E', '4/5': 'W_c4_5', '3/5': 'W_c3_5', '0': 'W_R'}

PSI = sp.Matrix([0, sp.sqrt(2) / 2, R(1, 2), R(1, 2)])
P_PSI = PSI * PSI.T
ALG = {  # minimal central projections of the commutative source algebra A_S
    'psi': [P_PSI, sp.eye(4) - P_PSI],
    'C1': [sp.eye(4)],
    'pi_p': [sv(P) * sv(P).T, sp.eye(4) - sv(P) * sv(P).T],
}
Z = {'plus': [R(1, 5), R(1, 5), R(2, 5), R(1, 5)], 'minus': [R(1, 5), R(1, 5), R(1, 5), R(2, 5)]}
Zp = {'plus': [R(1, 5), R(2, 5), R(1, 5), R(1, 5)], 'minus': [R(1, 5), R(1, 5), R(2, 5), R(1, 5)]}


def s(x):
    return str(sp.nsimplify(sp.simplify(x)))


def tnorm(M):
    return sum(abs(k) * m for k, m in M.eigenvals().items())


def delta_iface(D, projs):
    """Delta of A_S (x) 1_E (x) B(R): (1/2) sum_b || Tr_{S,E}[(Q_b (x) 1) D] ||_1 on R."""
    tot = 0
    for Q in projs:
        M = sp.zeros(2, 2)
        QK = sp.kronecker_product(Q, sp.eye(KD))
        X = QK * D
        for r in range(2):
            for q in range(2):
                M[r, q] = sum(X[a * KD + 2 * e + r, a * KD + 2 * e + q] for a in range(4) for e in range(2))
        tot += tnorm(sp.simplify(M))
    return sp.simplify(tot / 2)


def delta_S(Dy, projs):
    return sp.simplify(sum(abs(sp.simplify((Q * Dy).trace())) for Q in projs) / 2)


def main():
    cert = {'schema': 'uqcf-t241-successor-v1', 'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Ws = {n: iso(*REAL[n]) for n in REAL}
    rd = {}
    for n, W in Ws.items():
        units = [(a, b) for a in range(4) for b in range(4)]
        rd[n] = {'e0': [s(x) for x in REAL[n][0]], 'eu': [s(x) for x in REAL[n][1]],
                 'isometry': bool(sp.simplify(W.T * W - sp.eye(4)) == sp.zeros(4, 4)),
                 'implements_C': all(sp.simplify(trK(W * sv(a) * sv(b).T * W.T) - channel_C(sv(a) * sv(b).T)) == sp.zeros(4, 4) for a, b in units)}
    cert['realizations'] = rd
    drho = sp.diag(*Z['plus']) - sp.diag(*Z['minus'])
    Dy = channel_C(drho)
    Dout = {n: W * drho * W.T for n, W in Ws.items()}
    # V1 / V2
    cert['V1'] = {'pre_event_contrast': s(delta_S(drho, ALG['psi'])), 'd_S': s(delta_S(Dy, ALG['psi'])),
                  'Delta': {n: s(delta_iface(Dout[n], ALG['psi'])) for n in ('W_E', 'W_R')}}
    cert['V2'] = {a: {'d_S': s(delta_S(Dy, ALG[a])), 'Delta': {c: s(delta_iface(Dout[THETA[c]], ALG[a])) for c in THETA}} for a in ALG}
    # V3
    pre = {k: s(Zp[k][P]) for k in Zp}
    cy = {k: channel_C(sp.diag(*Zp[k])) for k in Zp}
    cert['V3'] = {'pre_pi_p': pre, 'post_equal': bool(cy['plus'] == cy['minus']), 'post_y': [s(cy['plus'][i, i]) for i in range(4)]}
    # V4: F = 1_S (x) |01><01|  (e=0, r=1 -> index 1)
    F4 = sp.kronecker_product(sp.eye(4), kv((1, 1)) * kv((1, 1)).T)
    cert['V4'] = {n: s(abs((F4 * Dout[n]).trace())) for n in ('W_R', 'W_E')}
    # V5 (i): scalar Y-blocks f = (1/3, 1/2, ., 1/4); fixed nonscalar u-block and off-diagonal blocks
    fY = {O: R(1, 3), P: R(1, 2), V: R(1, 4)}
    F5 = sp.zeros(16, 16)
    for j, f in fY.items():
        F5[j * KD:(j + 1) * KD, j * KD:(j + 1) * KD] = f * sp.eye(KD)
    F5[U * KD:(U + 1) * KD, U * KD:(U + 1) * KD] = sp.diag(1, 2, 3, 4) / 7
    G = sp.zeros(KD, KD); G[0, 1] = R(1, 9); G[2, 3] = R(2, 11)
    F5[O * KD:(O + 1) * KD, P * KD:(P + 1) * KD] = G
    F5[P * KD:(P + 1) * KD, O * KD:(O + 1) * KD] = G.T
    stats = {n: {k: s((F5 * W * sp.diag(*Z[k]) * W.T).trace()) for k in Z} for n, W in Ws.items()}
    sig = {k: s(sum(fY[j] * channel_C(sp.diag(*Z[k]))[j, j] for j in fY)) for k in Z}
    cert['V5'] = {'i': {'stats': stats, 'sigma_f_y': sig},
                  'ii': {}}
    F5b = sp.zeros(16, 16); F5b[P * KD, P * KD] = 1   # F_p = diag(1,0,0,0), all else 0
    cert['V5']['ii'] = {n: s(abs((F5b * Dout[n]).trace())) for n in Ws}
    # V6 / V6b: Dot's F = V (P_psi (x) 1) V^dag, V = sum_j pi_j (x) U_j, U_u = X
    def dotF(X):
        Vm = sp.zeros(16, 16)
        for j in range(4):
            Uj = X if j == U else sp.eye(KD)
            Vm += sp.kronecker_product(sv(j) * sv(j).T, Uj)
        return sp.simplify(Vm * sp.kronecker_product(P_PSI, sp.eye(KD)) * Vm.T)
    sx = sp.Matrix([[0, 1], [1, 0]])
    Xsx = sp.kronecker_product(sx, sp.eye(2))    # sigma_x on E (index 2e+r)
    def blocks_info(F):
        blk = lambda j, k: F[j * KD:(j + 1) * KD, k * KD:(k + 1) * KD]
        scal = lambda M: M == M[0, 0] * sp.eye(KD)
        return {'diag_blocks': [s(blk(j, j)[0, 0]) if scal(blk(j, j)) else 'nonscalar' for j in range(4)],
                'all_blocks_scalar': all(scal(sp.simplify(blk(j, k))) for j in range(4) for k in range(4))}
    v6 = {}
    for name, X in (('V6', Xsx), ('V6b', sp.eye(KD))):
        F = dotF(X)
        bi = blocks_info(F)
        e0 = REAL['W_E'][0]
        init = sp.simplify((F * sp.kronecker_product(drho, e0 * e0.T)).trace())
        v6[name] = {'idempotent': bool(sp.simplify(F * F - F) == sp.zeros(16, 16)), 'diag_blocks': bi['diag_blocks'],
                    'in_BHS_tensor_1K': bi['all_blocks_scalar'],
                    'b_nonzero_solution_exists': bi['all_blocks_scalar'],
                    'initial_contrast': s(abs(init)),
                    'pair_contrast': {n: s(abs(sp.simplify((F * Dout[n]).trace()))) for n in Ws}}
    cert['V6'] = v6['V6']; cert['V6b'] = v6['V6b']
    # V7: A_S = span{1, P_psi}, K_A = R: F = 1(x)G1 (x) 1_E-ordering handled via R-index; invariant subspace dimension
    # parameters: G1, G2 in B(R) (8 complex params, real matrix units suffice); Y-blocks F_j = G1 + |psi_j|^2 G2 on R
    cvars = sp.symbols('g0:8')
    G1 = sp.Matrix(2, 2, cvars[:4]); G2 = sp.Matrix(2, 2, cvars[4:])
    eqs = []
    for j in (O, P, V):
        Fj = G1 + (PSI[j] ** 2) * G2
        eqs += [Fj[0, 1], Fj[1, 0], Fj[0, 0] - Fj[1, 1]]
    A = sp.Matrix([[sp.diff(e, g) for g in cvars] for e in eqs])
    dim = len(cvars) - A.rank()
    # compression check for F = (1/3) 1 + (1/2) P_psi (x) 1_R
    alpha, beta = R(1, 3), R(1, 2)
    f = {j: alpha + beta * PSI[j] ** 2 for j in (O, P, V)}
    comp = {}
    phis = {'a0': sp.Matrix([1, 0]), 'a1': sp.Matrix([0, 1]), 'a+': sp.Matrix([1, 1]) / sp.sqrt(2)}
    for pn, phi in phis.items():
        Gs = sp.zeros(4, 4)
        Fop = sp.kronecker_product(alpha * sp.eye(4) + beta * P_PSI, sp.eye(2))   # on S (x) R
        for a in range(4):
            for b in range(4):
                Gs[a, b] = sp.simplify(sum(phi[r] * Fop[a * 2 + r, b * 2 + q] * phi[q] for r in range(2) for q in range(2)))
        comp[pn] = {k: s((Gs * channel_C(sp.diag(*Z[k]))).trace()) for k in Z}
    cert['V7'] = {'invariant_dim': int(dim),
                  'compression': comp,
                  'sigma_f_y': {k: s(sum(f[j] * channel_C(sp.diag(*Z[k]))[j, j] for j in f)) for k in Z}}
    cert['sympy'] = sp.__version__
    sys.stdout.write(json.dumps(cert, indent=1, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
