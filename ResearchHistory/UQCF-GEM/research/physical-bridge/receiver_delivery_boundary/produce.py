"""T-240 producer (sympy): receiver-delivery boundary for the accepted P1 blind/informative pair.
Deterministic; no randomness, no seed. Emits a JSON certificate on stdout."""
import hashlib, json, sys
from pathlib import Path
import sympy as sp

R = sp.Rational
SITES = ['o', 'p', 'u', 'v']
IDX = {s: i for i, s in enumerate(SITES)}
KD = 4  # K = E (x) R, basis |e r>: 00,01,10,11


def ket(n, i):
    v = sp.zeros(n, 1); v[i] = 1; return v


def channel_C(X):
    Q = sp.eye(4); Q[IDX['u'], IDX['u']] = 0
    out = Q * X * Q
    out[IDX['p'], IDX['p']] += X[IDX['u'], IDX['u']]
    return out


def iso(e0, eu):
    """W as a 16x4 matrix: W|j> = |j>|e0> (j=o,p,v), W|u> = |p>|eu>."""
    W = sp.zeros(4 * KD, 4)
    for j in SITES:
        s, e = (j, e0) if j != 'u' else ('p', eu)
        col = sp.kronecker_product(ket(4, IDX[s]), e)
        W[:, IDX[j]] = col
    return W


def ptrace_K(M):
    out = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            out[a, b] = sum(M[a * KD + k, b * KD + k] for k in range(KD))
    return out


SWAP = sp.zeros(4, 4)
for e in range(2):
    for r in range(2):
        SWAP[r * 2 + e, e * 2 + r] = 1


def kvec(*pairs):
    v = sp.zeros(KD, 1)
    for c, i in pairs:
        v[i] += c
    return v


E0 = kvec((1, 0))
FAMILY = {
    'W_E': (E0, kvec((1, 2))),
    'W_R': (E0, kvec((1, 1))),
    'W_M': (E0, kvec((R(3, 5), 2), (R(4, 5), 1))),
    'W_N': (kvec((R(3, 5), 0), (R(4, 5), 3)), kvec((1, 1))),
}
U_OF = {
    'W_E': sp.eye(4),
    'W_R': SWAP,
    'W_M': sp.Matrix([[1, 0, 0, 0], [0, R(-3, 5), R(4, 5), 0], [0, R(4, 5), R(3, 5), 0], [0, 0, 0, 1]]),
    'W_N': sp.Matrix([[R(3, 5), 0, 0, R(4, 5)], [0, 0, 1, 0], [0, 1, 0, 0], [R(4, 5), 0, 0, R(-3, 5)]]),
}


def partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def label(part):
    return '|'.join(''.join(sorted(b, key=SITES.index)) for b in sorted(part, key=lambda b: SITES.index(sorted(b, key=SITES.index)[0])))


def block_matrix(D, block, ktype):
    """M_B: compress S to block, trace S-block and K_B; return K_A matrix (sympy)."""
    proj = [IDX[s] for s in block]
    # D is 16x16 on S (x) E (x) R; index = s*4 + e*2 + r
    if ktype == 'T0':
        return sp.Matrix([[sum(D[s * 4 + k, s * 4 + k] for s in proj for k in range(4))]])
    if ktype == 'TK':
        return sp.Matrix(4, 4, lambda k, l: sum(D[s * 4 + k, s * 4 + l] for s in proj))
    if ktype == 'TR':  # keep R, trace E
        return sp.Matrix(2, 2, lambda r, q: sum(D[s * 4 + e * 2 + r, s * 4 + e * 2 + q] for s in proj for e in range(2)))
    if ktype == 'TE':  # keep E, trace R
        return sp.Matrix(2, 2, lambda e, f: sum(D[s * 4 + e * 2 + r, s * 4 + f * 2 + r] for s in proj for r in range(2)))
    raise ValueError(ktype)


def trace_norm(M):
    ev = M.eigenvals()
    return sp.nsimplify(sum(abs(k) * m for k, m in ev.items()))


def contrast(D, part, ktype):
    return sp.nsimplify(sum(trace_norm(block_matrix(D, b, ktype)) for b in part) / 2)


def rho(z):
    return sp.diag(*z)


PAIRS = {'canonical': ([R(1, 5), R(1, 5), R(2, 5), R(1, 5)], [R(1, 5), R(1, 5), R(1, 5), R(2, 5)]),
         'removed_summand': ([R(1, 5), R(2, 5), R(1, 5), R(1, 5)], [R(1, 5), R(1, 5), R(2, 5), R(1, 5)])}


def main():
    cert = {'schema': 'uqcf-t240-receiver-delivery-v1', 'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Ws = {n: iso(*FAMILY[n]) for n in FAMILY}
    WE = Ws['W_E']
    mem = {}
    for n, W in Ws.items():
        isometry = (W.T * W == sp.eye(4))
        implements = all(ptrace_K(W * ket(4, a) * ket(4, b).T * W.T) == channel_C(ket(4, a) * ket(4, b).T) for a in range(4) for b in range(4))
        U = U_OF[n]
        orth = (U.T * U == sp.eye(4))
        orbit = (sp.kronecker_product(sp.eye(4), U) * WE == W)
        mem[n] = {'isometry': bool(isometry), 'implements_C_all_16_units': bool(implements), 'U_orthogonal': bool(orth),
                  'equals_IxU_W_E': bool(orbit), 'U': [[str(x) for x in U.row(i)] for i in range(4)]}
    mem['W_R_equals_IxSWAP_W_E'] = bool(sp.kronecker_product(sp.eye(4), SWAP) * WE == Ws['W_R'])
    cert['membership'] = mem
    parts = sorted((label(p), p) for p in partitions(SITES))
    recs = []
    for pname, (zp, zm) in PAIRS.items():
        pre = rho(zp) - rho(zm)
        post = channel_C(rho(zp)) - channel_C(rho(zm))
        for lab, part in parts:
            blind = sum(abs(sum(pre[IDX[s], IDX[s]] for s in b)) for b in part) == 0
            t0_ret = sp.nsimplify(sum(abs(sum(post[IDX[s], IDX[s]] for s in b)) for b in part) / 2)
            row = {'pair': pname, 'partition': lab, 'initially_blind': bool(blind), 'retained_output_contrast': str(t0_ret), 'contrast': {}}
            for n, W in Ws.items():
                D = W * rho(zp) * W.T - W * rho(zm) * W.T
                row['contrast'][n] = {t: str(contrast(D, part, t)) for t in ('T0', 'TR', 'TE', 'TK')}
            recs.append(row)
    cert['records'] = recs
    # P7 predicates
    def choi_reduced(W):
        return [str(x) for a in range(4) for b in range(4) for x in ptrace_K(W * ket(4, a) * ket(4, b).T * W.T)]
    choiC = [str(x) for a in range(4) for b in range(4) for x in channel_C(ket(4, a) * ket(4, b).T)]
    def trE(e):
        P = e * e.T
        return sp.Matrix(2, 2, lambda r, q: sum(P[x * 2 + r, x * 2 + q] for x in range(2)))
    cert['predicates'] = {n: {'invariant_choi_equals_C': choi_reduced(Ws[n]) == choiC,
                              'factor_naming_kR': bool(trE(FAMILY[n][1]) != trE(FAMILY[n][0]))} for n in Ws}
    cert['sympy'] = sp.__version__
    sys.stdout.write(json.dumps(cert, indent=1, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
