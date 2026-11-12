"""receiver_identification d24 freeze producer (sections 28-30). Variables nu(k, i); parent-array AHU enumeration;
(POS) rows from cone sums over common ancestors; ranges by floating LP (HiGHS) with EXACT rational certification
(primal point and dual multipliers verified over Q). Witnesses W0-W10, instances Y1-Y7, controls R1-R10."""
import sys, json, hashlib
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

def canon(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    def c(v): return "(" + "".join(sorted(c(u) for u in ch[v])) + ")"
    return c(0)

def universe(N):
    seen = {"()"}; fr = [(-1,)]; out = [(-1,)]
    for _ in range(2, N + 1):
        nf = []
        for par in fr:
            for p in range(len(par)):
                q = par + (p,); k = canon(q)
                if k not in seen: seen.add(k); nf.append(q); out.append(q)
        fr = nf
    return out

def info(par):
    n = len(par); dep = [0] * n; ch = [[] for _ in range(n)]
    for v in range(1, n): dep[v] = dep[par[v]] + 1; ch[par[v]].append(v)
    anc = []
    for v in range(n):
        a = [v]
        while a[-1] != 0: a.append(par[a[-1]])
        anc.append(set(a))
    return dep, ch, anc

def maxch(par): return max(len(c) for c in info(par)[1])
def nonbranch(par, m):
    dep, ch, _ = info(par); return all(len(ch[v]) <= 1 for v in range(len(par)) if dep[v] == m)
def branch_depths(par):
    dep, ch, _ = info(par); return {dep[v] for v in range(len(par)) if len(ch[v]) >= 2}

def comb(D, miss=None):
    par = [-1] + list(range(D))
    for k in range(D):
        if k != miss: par.append(k)
    return tuple(par)

def closure(T):
    out = {canon(T): T}; fr = [T]
    while fr:
        nf = []
        for par in fr:
            dep, ch, _ = info(par)
            for l in range(1, len(par)):
                if ch[l]: continue
                keep = [v for v in range(len(par)) if v != l]; mp = {v: i for i, v in enumerate(keep)}
                q = tuple(-1 if v == 0 else mp[par[v]] for v in keep); k = canon(q)
                if k not in out: out[k] = q; nf.append(q)
        fr = nf
    return list(out.values())

def digest(cls): return hashlib.sha256("\n".join(sorted(canon(t) for t in cls)).encode()).hexdigest()

# holding of v under e_z as a dict over nu-keys (k, i)
def hold(par, v, z, I=None):
    dep, ch, anc = info(par); row = {}
    def add(u, sg):
        for w in anc[u] & anc[z]:
            key = (dep[u], dep[w]); row[key] = row.get(key, 0) + sg
    add(v, 1)
    for u in ch[v]: add(u, -1)
    return {k: c for k, c in row.items() if c != 0}

def hval(par, v, z, nu):
    return sum((Fr(c) * nu(*k) for k, c in hold(par, v, z).items()), Fr(0))

def pos_rows(cls):
    rows = set()
    for par in cls:
        for v in range(len(par)):
            for z in range(len(par)):
                r = hold(par, v, z)
                if r: rows.add(tuple(sorted(r.items())))
    return sorted(rows)

def Akey(j, i): return {(j, a): 1 for a in range(i + 1)}

def lp_ranges(cls, D, blind=True, targets=None):
    rows = pos_rows(cls)
    K = max(max(info(t)[0]) for t in cls)
    keys = [(k, i) for k in range(K + 1) for i in range(k + 1)]; ix = {k: n for n, k in enumerate(keys)}; nv = len(keys)
    Aub = np.zeros((len(rows), nv))
    for r, row in enumerate(rows):
        for k, c in row: Aub[r, ix[k]] = -c
    eqs = [({(0, 0): 1}, 1)]
    if blind:
        for d in range(1, D + 1):
            e = {}
            for k, c in Akey(d, d).items(): e[k] = e.get(k, 0) + c
            for k, c in Akey(d - 1, d - 1).items(): e[k] = e.get(k, 0) - c
            eqs.append(({k: c for k, c in e.items() if c}, 0))
    Aeq = np.zeros((len(eqs), nv)); beq = np.array([float(b) for _, b in eqs])
    for r, (e, _) in enumerate(eqs):
        for k, c in e.items(): Aeq[r, ix[k]] = c
    if targets is None: targets = [(j, i) for j in range(D + 1) for i in range(j + 1)]
    out = {}; certs_ok = True
    for (j, i) in targets:
        ends = []
        for sense in (1, -1):
            cvec = np.zeros(nv)
            for k, c in Akey(j, i).items(): cvec[ix[k]] = sense * c
            res = linprog(cvec, A_ub=Aub, b_ub=np.zeros(len(rows)), A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * nv, method="highs")
            if res.status != 0: ends.append(None); certs_ok = False; continue
            x = [Fr(float(v)).limit_denominator(10**6) for v in res.x]
            lam = [Fr(float(-m)).limit_denominator(10**6) for m in res.ineqlin.marginals]
            mu = [Fr(float(m)).limit_denominator(10**6) for m in res.eqlin.marginals]
            ok = all(l >= 0 for l in lam)
            # primal exact feasibility
            for row in rows:
                if sum(Fr(c) * x[ix[k]] for k, c in row) < 0: ok = False
            for e, b in eqs:
                if sum(Fr(c) * x[ix[k]] for k, c in e.items()) != b: ok = False
            # dual exact: c = sum lam r + sum mu a
            recon = [Fr(0)] * nv
            for l, row in zip(lam, rows):
                if l:
                    for k, c in row: recon[ix[k]] += l * c
            for m, (e, _) in zip(mu, eqs):
                for k, c in e.items(): recon[ix[k]] += m * c
            cex = [Fr(0)] * nv
            for k, c in Akey(j, i).items(): cex[ix[k]] = Fr(sense * c)
            if recon != cex: ok = False
            primal = sum(cex[n] * x[n] for n in range(nv)); dual = sum(m * b for m, (e, b) in zip(mu, eqs))
            if primal != dual: ok = False
            certs_ok &= ok
            ends.append(sense * primal)
        out[f"A({j},{i})"] = [str(ends[0]), str(ends[1])] if None not in ends else None
    return out, certs_ok, len(rows)

# named tables
def T_zero(k, i): return Fr(0)
def T_id(kap): return lambda k, i: Fr(kap) if i == k else Fr(0)
def T_off(k, i): return Fr({(0, 0): 1, (1, 1): 1, (2, 2): 1, (2, 0): 1, (2, 1): -1}.get((k, i), 1 if i == k else 0))
def T_284c(k, i): return Fr(0) if i != k else (Fr(1) if k <= 1 else Fr(2))
def T_dump(k, i): return Fr(1) if i == 0 else Fr(0)
def T_gpt(k, i): return {(0, 0): Fr(1), (1, 0): Fr(1, 2)}.get((k, i), Fr(0))
def T_horizon(B, D): return lambda k, i: Fr(1) if (i == k and k <= D) else (Fr(1, B) if (k == D + 1 and i == D) else Fr(0))
def T_nut(m, t):
    t = Fr(t)
    def f(k, i):
        if k == m + 1:
            if i == m: return t
            if i == m + 1: return 1 - t
            return Fr(0)
        return Fr(1) if i == k else Fr(0)
    return f
def T_ext(B, m, j):
    # cumulative A(d, m) = B^-(d-m-1) for m < d <= j, others kappa-id; nu(d, m) = A(d,m) - A(d,m-1), nu(d, m+1) = A(d,m+1)-A(d,m)
    def A(d, i):
        if m < d <= j and i == m: return Fr(1, B ** (d - m - 1))
        return Fr(1) if i >= d else Fr(0)
    return lambda k, i: A(k, i) - (A(k, i - 1) if i > 0 else Fr(0))

def chain(d): return tuple([-1] + list(range(d)))
def pos_ok(cls, nu): return all(hval(t, v, z, nu) >= 0 for t in cls for v in range(len(t)) for z in range(len(t)))
def Aval(nu, j, i): return sum((nu(j, a) for a in range(i + 1)), Fr(0))
def blind_ok(nu, D): return all(hval(chain(d), d - 1, d, nu) == 0 for d in range(1, D + 1))
def gain(nu, d): return hval(chain(d - 1), d - 1, d - 1, nu) - hval(chain(d), d - 1, d, nu)
def SL_ok(cls, nu):
    for t in cls:
        dep, ch, _ = info(t)
        for l in range(1, len(t)):
            if not ch[l] and any(hval(t, l, z, nu) != 0 for z in range(len(t)) if z != l): return False
    return True
def Gplus_ok(cls, nu):
    for t in cls:
        tp = tuple([-1, 0] + [p + 1 for p in t[1:]])
        for z in range(len(t)):
            if hval(tp, 0, z + 1, nu) != 0: return False
            for v in range(len(t)):
                if hval(tp, v + 1, z + 1, nu) != hval(t, v, z, nu): return False
    return True

def main(outp):
    U = {N: universe(N) for N in (5, 6, 7, 8)}
    classes = {}
    for N in (5, 6, 7, 8): classes[f"BIN_{N}"] = [t for t in U[N] if maxch(t) <= 2]
    for N in (7, 8): classes[f"ALL_{N}"] = U[N]
    classes["CH_7"] = [chain(d) for d in range(7)]
    for D in range(1, 5):
        classes[f"COMB_{D}"] = closure(comb(D))
        for k in range(D): classes[f"COMB_{D}-{k}"] = closure(comb(D, k))
    for B, ms in ((2, range(5)), (3, range(4))):
        for m in ms: classes[f"K_{B},{m}"] = [t for t in U[7] if maxch(t) <= B and nonbranch(t, m)]
    systems = []
    for N in (5, 6, 7, 8): systems += [(f"BIN_{N}", D) for D in range(1, N)]
    for N in (7, 8): systems += [(f"ALL_{N}", D) for D in range(1, N)]
    systems += [("CH_7", D) for D in range(1, 7)]
    for D in range(1, 5):
        systems.append((f"COMB_{D}", D)); systems += [(f"COMB_{D}-{k}", D) for k in range(D)]
    systems += [(f"K_2,{m}", D) for m in range(5) for D in range(m + 1, 6)]
    systems += [(f"K_3,{m}", D) for m in range(4) for D in range(m + 1, 5)]
    res = {"classes": {n: {"carriers": len(c), "digest": digest(c)} for n, c in sorted(classes.items())}, "ranges": {}, "rows": {}}
    allcert = True
    for (n, D) in systems:
        r, ok, nr = lp_ranges(classes[n], D)
        res["ranges"][f"{n}|D={D}"] = r; res["rows"][f"{n}|D={D}"] = nr; allcert &= ok
    r, ok, nr = lp_ranges(classes["BIN_7"], 0, blind=False, targets=[(1, 0)])
    res["diagnostic_nobl_BIN_7"] = r["A(1,0)"]; allcert &= ok
    res["certified_exact"] = allcert
    A7, A8 = classes["ALL_7"], classes["ALL_8"]
    W = {}
    W["W0"] = all(hval(t, v, z, T_zero) == 0 for t in A7 for v in range(len(t)) for z in range(len(t))) and SL_ok(A7, T_zero) and Gplus_ok(A7, T_zero) and all(gain(T_zero, d) == 0 for d in range(1, 7))
    W["W1"] = all(pos_ok(A7, T_id(k)) and pos_ok(A8, T_id(k)) and Gplus_ok(A7, T_id(k)) and all(gain(T_id(k), d) == k for d in range(1, 7)) for k in (1, 2)) and Gplus_ok(A7, T_id(-3)) and not pos_ok(A7, T_id(-3))
    W["W2"] = blind_ok(T_off, 6) and hval(chain(2), 2, 0, T_off) == 1
    W["W3"] = SL_ok(A7, T_284c) and blind_ok(T_284c, 1) and not Gplus_ok(A7, T_284c) and not blind_ok(T_284c, 2)
    W["W4"] = pos_ok(classes["CH_7"], T_dump) and blind_ok(T_dump, 6) and hval(chain(1), 1, 0, T_dump) == 1 and hval((-1, 0, 0), 0, 1, T_dump) == -1
    W["W5"] = pos_ok(classes["BIN_7"], T_gpt) and hval(chain(1), 0, 1, T_gpt) == Fr(1, 2)
    w6 = True
    for B in (2, 3):
        capB = [t for t in U[7] if maxch(t) <= B]
        for D in range(1, 6):
            nu = T_horizon(B, D); fan = tuple(list(chain(D)) + [D] * (B + 1))
            w6 &= pos_ok(capB, nu) and blind_ok(nu, D) and hval(chain(D + 1), D + 1, D, nu) == Fr(1, B) and hval(fan, D, D, nu) == Fr(-1, B)
    W["W6"] = w6
    w7 = True
    for t in (Fr(1, 3), Fr(1, 2), Fr(1)):
        for m in range(4):
            cls = [x for x in U[7] if nonbranch(x, m)]; nu = T_nut(m, t)
            phi = tuple(list(chain(m)) + [m, m])
            ok = pos_ok(cls, nu) and all(blind_ok(nu, D) for D in range(m + 1, 6))
            ok &= hval(phi, m, m + 1, nu) == -t and hval(chain(m + 1), m + 1, m, nu) == t
            w7 &= ok
    W["W7"] = w7
    w8 = True
    for B in (2, 3):
        for m in range(3):
            for j in range(m + 1, 6):
                nu = T_ext(B, m, j)
                w8 &= pos_ok(classes[f"K_{B},{m}"], nu) and blind_ok(nu, 6) and hval(chain(j), j, m, nu) == Fr(1, B ** (j - m - 1))
    W["W8"] = w8
    w9 = []
    for D in range(1, 5):
        g = comb(D); bd = branch_depths(g)
        small = sum(1 for t in U[8] if len(t) <= 2 * D and set(range(D)) <= branch_depths(t))
        exact = sum(1 for t in U[8] if len(t) == 2 * D + 1 and set(range(D)) <= branch_depths(t)) if 2 * D + 1 <= 8 else None
        w9.append([len(g), maxch(g), set(range(D)) <= bd, small, exact])
    W["W9"] = w9
    W["W10"] = all((1 if z == l else 0) == (1 if l in info(t)[2][z] else 0) for t in A7 for l in range(1, len(t)) if not info(t)[1][l] for z in range(len(t)))
    res["witnesses"] = W
    res["instances"] = {
        "Y1": [str(hval(chain(2), v, 0, T_off)) for v in range(3)],
        "Y2": str(hval((-1, 0, 0), 0, 1, T_dump)),
        "Y3": str(hval((-1, 0), 0, 1, T_gpt)),
        "Y4": [str(hval(chain(2), 2, 1, T_horizon(2, 1))), str(hval((-1, 0, 1, 1, 1), 1, 1, T_horizon(2, 1)))],
        "Y5": [str(hval((-1, 0, 0), 0, 1, T_nut(0, Fr(1, 2)))), str(hval((-1, 0), 1, 0, T_nut(0, Fr(1, 2))))],
        "Y6": str(hval(chain(3), 3, 0, T_ext(3, 0, 3))),
        "Y7": canon(comb(2)),
    }
    cap3 = [t for t in U[7] if maxch(t) <= 3]
    R = {
        "R1": pos_ok(classes["BIN_5"], T_dump),
        "R2": res["ranges"]["CH_7|D=6"]["A(1,0)"][1] == "0",
        "R3": pos_ok(A7, T_off),
        "R4": hval(chain(1), 0, 1, T_gpt) == 0,
        "R5": pos_ok(cap3, T_horizon(2, 1)),
        "R6": any(pos_ok(classes["BIN_7"], T_nut(m, Fr(1, 2))) for m in range(4)),
        "R7": any(gain(T_zero, d) != 0 for d in range(1, 7)),
        "R8": Gplus_ok(A7, T_284c),
        "R9": any(res["ranges"][f"COMB_{D}-{k}|D={D}"][f"A({k+1},{k})"][1] == "0" for D in range(1, 5) for k in range(D)),
        "R10": any(r[3] != 0 for r in w9),
    }
    res["controls"] = {k: ("ACCEPTED" if v else "REJECTED") for k, v in R.items()}
    res["diagnostic_row_counts_total"] = sum(res["rows"].values())
    res["role"] = "producer"
    rp = "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_review/RESULT.md"
    try: res["result_sha256"] = hashlib.sha256(open(rp, "rb").read()).hexdigest()
    except OSError: res["result_sha256"] = None
    with open(outp, "w") as f: json.dump(res, f, indent=1, sort_keys=True)
    print("certified", allcert, "systems", len(systems))

if __name__ == "__main__": main(sys.argv[1])
