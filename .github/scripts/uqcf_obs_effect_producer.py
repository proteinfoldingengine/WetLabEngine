"""observation_effect draft 3 freeze: PRODUCER (exact sympy). Preregistered in
observation_effect_review/FREEZE.md section 2. Writes a certificate of exact values."""
import hashlib, json, sys
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/observation_effect_review")
R = sp.Rational
s2 = sp.sqrt(2)


def kron(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = sp.kronecker_product(out, m)
    return out


def dephase(X):  # tracial faithful pinching onto the diagonal algebra
    return sp.diag(*[X[i, i] for i in range(X.shape[0])])


def block_pinch(X, blocks):
    Y = sp.zeros(*X.shape)
    for b in blocks:
        for i in b:
            for j in b:
                Y[i, j] = X[i, j]
    return Y


def tnorm_half(X):
    X = sp.simplify(X)
    ev = X.eigenvals()
    return sp.nsimplify(sp.simplify(sum(abs(sp.nsimplify(k)) * v for k, v in ev.items()) / 2))


def conj(U, X):
    return U * X * U.H


def tv(p, q):
    return sp.simplify(sum(abs(sp.simplify(a - b)) for a, b in zip(p, q)) / 2)


ket0, ket1 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
P0, P1 = ket0 * ket0.T, ket1 * ket1.T
I2 = sp.eye(2)
Hd = sp.Matrix([[1, 1], [1, -1]]) / s2
CNOT = sp.zeros(4, 4)
for s in (0, 1):
    for r in (0, 1):
        CNOT[2 * s + (r ^ s), 2 * s + r] = 1
QR = [kron(I2, P0), kron(I2, P1)]


def rec(X):
    return [sp.simplify((Q * X).trace()) for Q in QR]


def obs(U, rho):
    return dephase(conj(U, dephase(rho)))


def unobs(U, rho):
    return dephase(conj(U, rho))


def main():
    c = {}
    # W (6.1, 12.2, 12.3)
    U = CNOT * kron(Hd, I2)
    plus, minus = (ket0 + ket1) / s2, (ket0 - ket1) / s2
    rW = [kron(v * v.T, P0) for v in (plus, minus)]
    c["W.tv_obs"] = tv(rec(obs(U, rW[0])), rec(obs(U, rW[1])))
    c["W.tv_unobs"] = tv(rec(unobs(U, rW[0])), rec(unobs(U, rW[1])))
    Delta = rW[0] - dephase(rW[0])
    c["W.kappa"] = tnorm_half(Delta)
    c["W.occ_tv"] = tv(rec(unobs(U, rW[0])), rec(obs(U, rW[0])))
    spec = sorted([k for k, v in Delta.eigenvals().items() for _ in range(v)], reverse=True)
    q = 2
    c["W.kyfan"] = sp.Max(sum(spec[:q]), sum(spec[:4 - q]))
    # P (6.2, 12.2)
    Ry = sp.Matrix([[2, -1], [1, 2]]) / sp.sqrt(5)
    U = CNOT * kron(Ry, I2)
    Xp = sp.Matrix([[0, 1], [1, 0]])
    rP = [kron(P0, P0), kron((I2 - R(3, 4) * Xp) / 2, P0)]
    c["P.tv_obs"] = tv(rec(obs(U, rP[0])), rec(obs(U, rP[1])))
    c["P.tv_unobs"] = tv(rec(unobs(U, rP[0])), rec(unobs(U, rP[1])))
    c["P.global_obs"] = [tnorm_half(rP[0] - rP[1]), tnorm_half(dephase(rP[0]) - dephase(rP[1])),
                         tnorm_half(obs(U, rP[0]) - obs(U, rP[1]))]
    c["P.kappa1"] = tnorm_half(rP[1] - dephase(rP[1]))
    c["P.occ1"] = tv(rec(unobs(U, rP[1])), rec(obs(U, rP[1])))
    c["P.occ0"] = tv(rec(unobs(U, rP[0])), rec(obs(U, rP[0])))
    # H: strictness witness of (F) => (C)
    blocks = [(0, 1), (2, 3)]
    U = sp.eye(4)[:, [0, 2, 1, 3]]
    Pk = [sp.diag(1, 1, 0, 0), sp.diag(0, 0, 1, 1)]
    inA = lambda X: block_pinch(X, blocks) == X
    psi = (sp.eye(4)[:, 0] + sp.eye(4)[:, 2]) / s2
    rho = psi * psi.T
    N = block_pinch(conj(U, rho), blocks)
    O = block_pinch(conj(U, block_pinch(rho, blocks)), blocks)
    cw = lambda X: [sp.simplify((P * X).trace()) for P in Pk]
    normalizes = all(inA(conj(U, X)) for X in [sp.eye(4)[:, [i]] * sp.eye(4)[:, [j]].T
                                               for b in blocks for i in b for j in b])
    c["H.central_equal"] = bool(all(inA(U.H * P * U) for P in Pk) and cw(N) == cw(O) and not normalizes)
    c["H.full_effect"] = 2 * tnorm_half(N - O)  # trace norm ||N rho - O rho||_1
    # Z: cadence
    U = sp.Matrix([[1, -1], [1, 1]]) / s2
    once = dephase(conj(U * U, P0))
    rep = dephase(conj(U, dephase(conj(U, P0))))
    c["Z.cadence"] = tnorm_half(once - rep)
    # S: sector swap relabels the record
    X4 = kron(Xp, I2)
    st = sp.diag(0, 1, 0, 0)
    c["S.swap_record"] = [dephase(conj(X4, dephase(st)))[i, i] for i in range(4)]
    # Classical P2 owner section, matrices on atoms
    def owner_maps(fibers, owners, n):
        P = sp.zeros(len(fibers), n)
        Iw = sp.zeros(n, len(fibers))
        for f, (F, o) in enumerate(zip(fibers, owners)):
            for a in F:
                P[f, a] = 1
            Iw[o, f] = 1
        return P, Iw
    def perm(n, swap):
        i, j = swap
        cols = list(range(n))
        cols[i], cols[j] = j, i
        return sp.eye(n)[:, cols]
    # L: atoms (a,u|b) = 0,1|2
    P, Iw = owner_maps([(0, 1), (2,)], [0, 2], 3)
    T = perm(3, (1, 2))
    x = sp.Matrix([R(1, 2), R(1, 2), 0])
    Etr = sp.Matrix([[R(1, 2), R(1, 2), 0], [R(1, 2), R(1, 2), 0], [0, 0, 1]])
    c["L.owner"] = list(P * T * Iw * P * x)
    c["L.tracial"] = list(P * T * Etr * x)
    c["L.unobs"] = list(P * T * x)
    xu = sp.Matrix([0, 1, 0])
    c["O.perfect"] = tv(list(P * T * xu), list(P * T * Iw * P * xu))
    def DC(P, Iw, T):
        nf, n = P.shape
        D = max(abs(((P * T * Iw - sp.eye(nf)) * sp.eye(nf)[:, y])[f]) for y in range(nf) for f in range(nf))
        C = max(abs(((P * T * (sp.eye(n) - Iw * P)) * sp.eye(n)[:, a])[f]) for a in range(n) for f in range(nf))
        return D, C
    c["G3.D"], c["G3.C"] = DC(P, Iw, T)
    P4, I4 = owner_maps([(0, 1), (2, 3)], [0, 2], 4)
    c["G4.D"], c["G4.C"] = DC(P4, I4, perm(4, (1, 3)))
    # N: nonfaithful kernel counterexample
    Em = Iw * P
    Erho = sp.diag(*list(Em * xu))
    rho_u = sp.diag(*list(xu))
    ker = Erho.nullspace()
    c["N.kernel"] = "inclusion_fails" if any((rho_u * k) != sp.zeros(3, 1) for k in ker) else "inclusion_holds"
    # Q: qubit rotation, symbolic
    th = sp.symbols("theta", real=True)
    Ur = sp.Matrix([[sp.cos(th / 2), -sp.sin(th / 2)], [sp.sin(th / 2), sp.cos(th / 2)]])
    Xq = sp.simplify(Ur.H * P0 * Ur)
    Dq = sp.simplify(1 - dephase(Xq)[0, 0])  # = |E*(X)00 - 1| since 0 <= X00 <= 1; other diagonal entry equal
    Cq = Xq[0, 1]  # C = |Cq|; checked through Cq**2
    ok = sp.simplify(sp.trigsimp(Dq - sp.sin(th / 2) ** 2)) == 0 and \
        sp.simplify(sp.trigsimp(Cq ** 2 - (sp.sin(th) / 2) ** 2)) == 0 and \
        sp.simplify(sp.trigsimp(Cq ** 2 - Dq * (1 - Dq))) == 0
    c["Q.D"], c["Q.C"] = ("sin(theta/2)**2", "Abs(sin(theta))/2") if ok else (str(Dq), str(Cq))
    # M: [D2] witness U = I(x)(I-pi) + V(x)pi on M2(x)I2, V = Pauli X
    pi = P1
    Um = kron(I2, I2 - pi) + kron(Xp, pi)
    Zp = sp.diag(1, -1)
    img = conj(Um, kron(Zp, I2))
    inM2I2 = all(img[2 * a + r, 2 * b + t] == (img[2 * a, 2 * b] if r == t else 0)
                 for a in (0, 1) for b in (0, 1) for r in (0, 1) for t in (0, 1))
    unitary = (Um * Um.H) == sp.eye(4)
    c["M.witness"] = "inZprime_nonnormalizing_keeps_record" if unitary and not inM2I2 else "fails"
    out = {}
    for k, v in c.items():
        if isinstance(v, (list, tuple)):
            out[k] = [str(sp.nsimplify(e)) for e in v]
        elif isinstance(v, (bool, str)):
            out[k] = v if isinstance(v, str) else bool(v)
        else:
            out[k] = str(sp.nsimplify(v))
    meta = {"role": "producer", "algorithm": "sympy exact matrices",
            "sympy": sp.__version__, "result_sha256": hashlib.sha256((ROOT / "RESULT.md").read_bytes()).hexdigest()}
    Path(sys.argv[1]).write_text(json.dumps({"meta": meta, "values": out}, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
