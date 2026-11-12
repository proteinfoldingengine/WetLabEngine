"""receiver_identification d18 freeze (section 24, initial blindness from the read ledger): PRODUCER.
Pure-Python exact Fractions. Parent-array enumeration with AHU codes; field by exact Gauss-Jordan solve of the grounded
weighted Laplacian (no cone-total formula); reads evaluated as vertex-coordinate matrices on N[v]; parameter and Lemma 24.1
spaces as exact nullspaces over Q."""
import hashlib, json, sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d18_review")
TABLES = {"unit": lambda k: Fr(1), "three": lambda k: Fr(3), "depth": lambda k: Fr(k),
          "alt": lambda k: Fr(1) if k % 2 == 1 else Fr(-2)}
MT = {"one": lambda k: Fr(1), "k": lambda k: Fr(k), "inv": lambda k: Fr(1, k), "alt": lambda k: Fr(1) if k % 2 == 1 else Fr(-2),
      "invalt": lambda k: Fr(1) if k % 2 == 1 else Fr(-1, 2)}
FAM = {"F1": ("unit", "one"), "F2": ("three", "one"), "F3": ("depth", "inv"), "F4": ("alt", "invalt"),
       "F5": ("depth", "one"), "F6": ("unit", "k"), "F7": ("alt", "one")}
CONST = ("F1", "F2", "F3", "F4")
GS = [Fr(1), Fr(-2), Fr(5, 3)]
VIOL = []


def canon_of(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n):
        ch[par[v]].append(v)
    memo = {}
    def s(v):
        if v not in memo:
            memo[v] = "(" + "".join(sorted(s(u) for u in ch[v])) + ")"
        return memo[v]
    return s, ch


def trees(nmax):
    out = {}; level = [[None]]
    out[canon_of([None])[0](0)] = [None]
    for _ in range(2, nmax + 1):
        new = []
        for par in level:
            for a in range(len(par)):
                q = par + [a]; c = canon_of(q)[0](0)
                if c not in out:
                    out[c] = q; new.append(q)
        level = new
    return out


def depth(par, v):
    d = 0
    while par[v] is not None:
        v = par[v]; d += 1
    return d


def solve(A, b):
    n = len(A); M = [row[:] + [bb] for row, bb in zip(A, b)]
    for i in range(n):
        piv = next(r for r in range(i, n) if M[r][i] != 0); M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]; M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


class Echelon:
    """incremental exact row echelon over Q."""
    def __init__(self, m):
        self.m = m; self.rows = {}
    def add(self, r):
        r = list(r)
        for c in range(self.m):
            if r[c] != 0 and c in self.rows:
                f = r[c]; r = [x - f * y for x, y in zip(r, self.rows[c])]
        c = next((c for c in range(self.m) if r[c] != 0), None)
        if c is None:
            return
        inv = 1 / r[c]; r = [x * inv for x in r]
        for c2, row in self.rows.items():
            if row[c] != 0:
                f = row[c]; self.rows[c2] = [x - f * y for x, y in zip(row, r)]
        self.rows[c] = r
    def nullity(self):
        return self.m - len(self.rows)
    def basis(self):
        piv = sorted(self.rows); out = []
        for fc in [c for c in range(self.m) if c not in self.rows]:
            v = [Fr(0)] * self.m; v[fc] = Fr(1)
            for pc in piv:
                v[pc] = -self.rows[pc][fc]
            out.append(v)
        return out


def field(par, x, a):
    n = len(par)
    if n == 1:
        return [Fr(0)]
    w = {v: 1 / a(depth(par, v)) for v in range(1, n)}
    L = [[Fr(0)] * n for _ in range(n)]
    for v in range(1, n):
        p = par[v]; L[v][v] += w[v]; L[p][p] += w[v]; L[v][p] -= w[v]; L[p][v] -= w[v]
    idx = list(range(1, n))
    return [Fr(0)] + solve([[L[i][j] for j in idx] for i in idx], [x[i] for i in idx])


def children(par):
    ch = [[] for _ in par]
    for v in range(1, len(par)):
        ch[par[v]].append(v)
    return ch


def rule_matrix(par, beta, gamma, gamma0):
    """vertex-coordinate read matrix: f = R phi."""
    n = len(par); ch = children(par); R = [[Fr(0)] * n for _ in range(n)]
    if ch[0]:
        g0 = gamma0(len(ch[0]))
        for u in ch[0]:
            R[0][u] += g0; R[0][0] -= g0
    for v in range(1, n):
        k = depth(par, v); b = beta(k, len(ch[v]))
        R[v][par[v]] += b; R[v][v] -= b
        if ch[v]:
            g = gamma(k, len(ch[v]))
            for u in ch[v]:
                R[v][u] += g; R[v][v] -= g
    return R


def depth_rule(par, m):
    return rule_matrix(par, lambda k, n: m(k), lambda k, n: m(k + 1), lambda n: m(1))


def apply(R, phi):
    return [sum((r * p for r, p in zip(row, phi)), Fr(0)) for row in R]


def unit(n, z):
    x = [Fr(0)] * n; x[z] = Fr(1); return x


def prune(par, l):
    mp = {}; j = 0
    for v in range(len(par)):
        if v != l:
            mp[v] = j; j += 1
    q = [None] * (len(par) - 1)
    for v in range(len(par)):
        if v != l and par[v] is not None:
            q[mp[v]] = mp[par[v]]
    return q, mp


def P(x, par, l, mp):
    y = [Fr(0)] * (len(x) - 1)
    for v in range(len(x)):
        if v != l:
            y[mp[v]] = x[v]
    y[mp[par[l]]] += x[l]
    return y


def balanced(x):
    return [x[0] - sum(x)] + list(x[1:])


def cone(par, z):
    ch = children(par); s = [z]; out = []
    while s:
        v = s.pop(); out.append(v); s.extend(ch[v])
    return out


def params(univ):
    ps = set()
    for par in univ:
        ch = children(par)
        if ch[0]:
            ps.add(("g0", len(ch[0])))
        for v in range(1, len(par)):
            k = depth(par, v); ps.add(("b", k, len(ch[v])))
            if ch[v]:
                ps.add(("g", k, len(ch[v])))
    return sorted(ps, key=str)


def forms(par, phi, idx):
    """reads as linear forms in the uniform parameters, from vertex-coordinate edge differences."""
    n = len(par); ch = children(par); F = [[Fr(0)] * len(idx) for _ in range(n)]
    for u in ch[0]:
        F[0][idx[("g0", len(ch[0]))]] += phi[u] - phi[0]
    for v in range(1, n):
        k = depth(par, v)
        F[v][idx[("b", k, len(ch[v]))]] -= phi[v] - phi[par[v]]
        for u in ch[v]:
            F[v][idx[("g", k, len(ch[v]))]] += phi[u] - phi[v]
    return F


def elimination(univ, a, D):
    ps = params(univ); idx = {p: i for i, p in enumerate(ps)}; m = len(ps)
    E = {"PN": Echelon(m), "SC": Echelon(m), "K": Echelon(m), "ALL": Echelon(m)}
    rows_all = []
    for par in univ:
        n = len(par); ch = children(par)
        for z in range(1, n):
            x = unit(n, z); FW = forms(par, field(par, balanced(x), a), idx)
            rk = [sum(col) for col in zip(*FW)]
            E["K"].add(rk); E["ALL"].add(rk); rows_all.append(rk)
            for l in range(1, n):
                if ch[l]:
                    continue
                q, mp = prune(par, l); xp = P(x, par, l, mp)
                FY = forms(q, field(q, balanced(xp), a), idx); p = par[l]
                sc = [sum(col) for col in zip(*FY)]
                sc = [s - t for s, t in zip(sc, rk)]
                E["SC"].add(sc); E["ALL"].add(sc); rows_all.append(sc)
                for v in range(n):
                    if v == l:
                        continue
                    r = [s - t for s, t in zip(FY[mp[v]], FW[v])]
                    if v == p:
                        r = [s - t for s, t in zip(r, FW[l])]
                    E["PN"].add(r); E["ALL"].add(r); rows_all.append(r)
    dims = {k: e.nullity() for k, e in E.items()}
    fam_ok = True
    for j in range(1, D + 1):
        sol = [Fr(0)] * m
        for p, i in idx.items():
            kk = p[1] if p[0] == "b" else (p[1] + 1 if p[0] == "g" else 1)
            sol[i] = Fr(1) if kk == j else Fr(0)
        fam_ok &= all(sum((r * s for r, s in zip(row, sol)), Fr(0)) == 0 for row in rows_all)
    # structure: every basis vector of the PN space is a depth-table rule
    struct = True
    for v in E["PN"].basis():
        val = {}
        for p, i in idx.items():
            kk = p[1] if p[0] == "b" else (p[1] + 1 if p[0] == "g" else 1)
            if val.setdefault(kk, v[i]) != v[i]:
                struct = False
    return dims, fam_ok and struct, len(ps)


def lemma(par):
    n = len(par); ch = children(par)
    nb = {v: sorted(set(([par[v]] if par[v] is not None else []) + [v] + ch[v])) for v in range(n)}
    unk = [(v, q) for v in range(n) for q in nb[v]]; ix = {u: i for i, u in enumerate(unk)}
    E = Echelon(len(unk))
    for v in range(n):
        r = [Fr(0)] * len(unk)
        for q in nb[v]:
            r[ix[(v, q)]] = Fr(1)
        E.add(r)
    for q in range(n):
        r = [Fr(0)] * len(unk)
        for v in range(n):
            if (v, q) in ix:
                r[ix[(v, q)]] = Fr(1)
        E.add(r)
    ok = True
    for b in E.basis():
        for c in range(1, n):
            if b[ix[(par[c], c)]] != b[ix[(c, par[c])]]:
                ok = False
    return E.nullity(), ok


def analyse(par):
    n = len(par); ch = children(par); dep = [depth(par, v) for v in range(n)]
    rec = {"lemma": lemma(par)}
    fam = {}
    for f, (an, mn) in FAM.items():
        a, m = TABLES[an], MT[mn]; mu = lambda k: m(k) * a(k)
        R = depth_rule(par, m)
        K = True; comp = 0; gen = True; blind = [False] * n; own = [False] * n
        reads = {}
        for z in range(1, n):
            x = unit(n, z); fr = apply(R, field(par, balanced(x), a)); reads[z] = fr
            K &= sum(fr) == 0
            c = {v: sum(x[w] for w in cone(par, v)) for v in range(1, n)}
            for v in range(n):
                if v == 0:
                    pred = mu(1) * sum((c[u] for u in ch[0]), Fr(0))
                else:
                    k = dep[v]; pred = -mu(k) * x[v] + (mu(k + 1) - mu(k)) * sum((c[u] for u in ch[v]), Fr(0))
                comp += fr[v] == pred
            gen &= fr[0] == mu(1)
        for p in range(1, n):
            desc = [z for z in cone(par, p) if z != p]
            blind[p] = all(reads[z][p] == 0 for z in desc)
            own[p] = all(reads[z][p] == (-mu(dep[p]) if z == p else 0) for z in range(1, n))
        fam[f] = {"K": K, "comp": comp, "gen": gen if n >= 2 else None, "blind": blind, "own": own}
    rec["fam"] = fam
    rs = {}
    for mn in ("one", "k", "inv", "alt"):
        m = MT[mn]; out = []
        for aa in range(1, n):
            if not ch[aa]:
                continue
            X = cone(par, aa); X.sort(); loc = {v: i for i, v in enumerate(X)}
            if X[0] != aa:
                X.remove(aa); X.insert(0, aa); loc = {v: i for i, v in enumerate(X)}
            qpar = [None] + [loc[par[v]] for v in X[1:]]
            RW, RX = depth_rule(par, m), depth_rule(qpar, m); ok = True
            for qv in X:
                psi = [Fr(0)] * len(X); psi[loc[qv]] = Fr(1)
                hphi = [psi[loc[v]] if v in loc else psi[0] for v in range(n)]
                lhs = apply(RW, hphi); fx = apply(RX, psi)
                rhs = [fx[loc[v]] if v in loc else Fr(0) for v in range(n)]
                ok &= lhs == rhs
            out.append((dep[aa], ok))
        rs[mn] = out
    rec["rs"] = rs
    return rec


def background(n, l):
    return [Fr((-1) ** v * (v + 2), 1 + v % 3) if v != l else Fr(0) for v in range(n)]


def events(par, U):
    n = len(par); ch = children(par)
    for f, (an, mn) in FAM.items():
        a, m = TABLES[an], MT[mn]; mu = lambda k: m(k) * a(k)
        thetas = [-mu(1), Fr(0), Fr(2)] if f in CONST else []
        e = U["event"][f]
        for l in range(1, n):
            if ch[l]:
                continue
            p = par[l]; q, mp = prune(par, l); RW, RY = depth_rule(par, m), depth_rule(q, m)
            k = depth(par, p)
            for g in GS:
                outs = []
                for mem in (0, 1):
                    x = background(n, l); x[l] = g * mem; xp = P(x, par, l, mp)
                    fw = apply(RW, field(par, balanced(x), a)); fy = apply(RY, field(q, balanced(xp), a))
                    ok = all(fy[mp[v]] == fw[v] + (fw[l] if v == p else 0) for v in range(n) if v != l)
                    e["pn_cases"] += 1; e["pn_ok"] += ok
                    if not ok:
                        VIOL.append("pn " + f)
                    outs.append((x, xp, fw, fy))
                (x0, xp0, fw0, fy0), (x1, xp1, fw1, fy1) = outs
                before = fw1[p] - fw0[p]; after = fy1[mp[p]] - fy0[mp[p]]
                if p != 0:
                    e["nonroot_contrast_ok"] += before == g * (mu(k + 1) - mu(k)) and after == -mu(k) * g
                    e["nonroot_blind_before"] += before == 0
                else:
                    e["genesis_contrast_ok"] += before == mu(1) * g and after == 0
                    for th in thetas:
                        t = U["total"][f][str(th)]
                        tb = before + th * (sum(x1) - sum(x0)); ta = after + th * (sum(xp1) - sum(xp0))
                        t["contrast_ok"] += tb == (mu(1) + th) * g and ta == th * g
                        t["blind_before"] += tb == 0
                        for (x, xp, fw, fy) in outs:
                            t["pn_cases"] += 1
                            t["pn_ok"] += fy[0] + th * sum(xp) == fw[0] + th * sum(x) + fw[l]
        if f in CONST:
            th = -mu(1); R = depth_rule(par, m)
            for z in range(n):
                x = unit(n, z); fr = apply(R, field(par, balanced(x), a)); fr[0] += th * sum(x)
                U["total"][f]["neg_id"] += sum(fr[v] == -mu(1) * x[v] for v in range(n))


def controls_data(par, U):
    n = len(par); ch = children(par); a = TABLES["unit"]
    R = rule_matrix(par, lambda k, nn: Fr(1), lambda k, nn: Fr(0), lambda nn: Fr(0))
    for l in range(1, n):
        if ch[l]:
            continue
        p = par[l]; q, mp = prune(par, l)
        RY = rule_matrix(q, lambda k, nn: Fr(1), lambda k, nn: Fr(0), lambda nn: Fr(0)); fail = False
        for z in range(1, n):
            x = unit(n, z); xp = P(x, par, l, mp)
            fw = apply(R, field(par, balanced(x), a)); fy = apply(RY, field(q, balanced(xp), a))
            if not all(fy[mp[v]] == fw[v] + (fw[l] if v == p else 0) for v in range(n) if v != l):
                fail = True
        U["R1_fail_prunings"] += fail
    R2 = rule_matrix(par, lambda k, nn: Fr(1 + nn), lambda k, nn: Fr(1), lambda nn: Fr(1))
    U["R2_fail_carriers"] += any(sum(apply(R2, field(par, balanced(unit(n, z)), a))) != 0 for z in range(1, n))


def universe(nmax):
    T = trees(nmax); univ = list(T.values()); D = nmax - 1
    U = {"carriers": len(univ), "event": {f: {"pn_cases": 0, "pn_ok": 0, "nonroot_contrast_ok": 0, "nonroot_blind_before": 0,
                                               "genesis_contrast_ok": 0} for f in FAM},
         "total": {}, "R1_fail_prunings": 0, "R2_fail_carriers": 0}
    for f in CONST:
        mu1 = MT[FAM[f][1]](1) * TABLES[FAM[f][0]](1)
        U["total"][f] = {str(th): {"contrast_ok": 0, "blind_before": 0, "pn_cases": 0, "pn_ok": 0} for th in (-mu1, Fr(0), Fr(2))}
        U["total"][f]["neg_id"] = 0
    pos = wc = lv = gl = 0; lem_ok = 0; lines = []
    fam = {f: {"K_carriers": 0, "composite": 0, "genesis_read": 0, "blind": 0, "own_grade": 0} for f in FAM}
    rsc = {mn: 0 for mn in ("one", "k", "inv", "alt")}; cones = 0
    for cs, par in T.items():
        n = len(par); ch = children(par)
        for v in range(1, n):
            pos += 1; wc += bool(ch[v]); lv += not ch[v]; gl += (not ch[v]) and par[v] == 0
        rec = analyse(par)
        lem_ok += rec["lemma"] == (n - 1, True)
        for f in FAM:
            r = rec["fam"][f]; F = fam[f]
            F["K_carriers"] += r["K"]; F["composite"] += r["comp"]; F["genesis_read"] += bool(r["gen"])
            F["blind"] += sum(r["blind"][1:]); F["own_grade"] += sum(r["own"][1:])
        cones += len(rec["rs"]["one"])
        for mn in rsc:
            rsc[mn] += sum(ok for _, ok in rec["rs"][mn])
        events(par, U); controls_data(par, U)
        dep = [depth(par, v) for v in range(n)]
        verts = sorted([dep[v], len(ch[v])] + [int(rec["fam"][f]["blind"][v]) for f in FAM] + [int(rec["fam"][f]["own"][v]) for f in FAM]
                       for v in range(1, n))
        rsl = sorted([d] + [int(dict(enumerate(rec["rs"][mn]))[i][1]) for mn in ("one", "k", "inv", "alt")]
                     for i, (d, _) in enumerate(rec["rs"]["one"]))
        lines.append(json.dumps([cs, rec["lemma"][0], verts, rsl], separators=(",", ":")))
    U.update({"positions": pos, "positions_with_children": wc, "leaves": lv, "genesis_leaves": gl, "cones": cones,
              "lemma_ok_carriers": lem_ok, "families": fam, "rs_f": rsc})
    elim = {}
    for an in ("unit", "depth", "alt"):
        dims, ok, npar = elimination(univ, TABLES[an], D)
        elim[an] = {"dims": dims, "family_exact": ok}
    U["parameters"] = npar; U["max_depth"] = D; U["elimination"] = elim
    U["digest"] = hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()
    U["universe_digest"] = hashlib.sha256("\n".join(sorted(T)).encode()).hexdigest()
    return U


def instances():
    one = MT["one"]; a1 = TABLES["unit"]; ad = TABLES["depth"]
    def reads(par, x, a, m):
        return [str(v) for v in apply(depth_rule(par, m), field(par, balanced(x), a))]
    ch2 = [None, 0, 1]
    Z = {"Z1.e2": reads(ch2, unit(3, 2), a1, one), "Z1.e1": reads(ch2, unit(3, 1), a1, one),
         "Z2.depth_one": reads(ch2, unit(3, 2), ad, one), "Z2.depth_inv": reads(ch2, unit(3, 2), ad, MT["inv"]),
         "Z3.lemma_dim": lemma([None, 0, 1, 1])[0]}
    par = [None, 0, 1, 2]; rec = analyse(par)
    Z["Z4.rsf_alt"] = [ok for _, ok in rec["rs"]["alt"]][:2]
    out = {}
    for th in (Fr(0), Fr(-1)):
        R = depth_rule([None, 0], one); RY = depth_rule([None], one)
        def f0(par_, R_, x):
            return apply(R_, field(par_, balanced(x), a1))[0] + th * sum(x)
        b = f0([None, 0], R, [Fr(0), Fr(1)]) - f0([None, 0], R, [Fr(0), Fr(0)])
        af = f0([None], RY, [Fr(1)]) - f0([None], RY, [Fr(0)])
        out[str(th)] = [str(b), str(af)]
    Z["Z5.theta0"] = out["0"]; Z["Z5.theta_neg1"] = out["-1"]
    R2 = rule_matrix(ch2, lambda k, nn: Fr(1 + nn), lambda k, nn: Fr(1), lambda nn: Fr(1))
    Z["Z6.childcount_sum"] = str(sum(apply(R2, field(ch2, balanced(unit(3, 1)), a1))))
    return Z


def main():
    res = (ROOT / "RESULT.md").read_bytes()
    cert = {"role": "producer", "result_sha256": hashlib.sha256(res).hexdigest(), "universes": {}}
    for name, nmax in (("U7", 7), ("U8", 8)):
        cert["universes"][name] = universe(nmax)
    cert["instances"] = instances()
    cert["violations"] = sorted(set(VIOL))
    cert["controls"] = controls(cert["universes"])
    Path(sys.argv[1]).write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
    for u in cert["universes"].values():
        print(json.dumps({k: u[k] for k in u if k not in ("digest",)}, sort_keys=True))
    print(json.dumps(cert["instances"]), cert["controls"], cert["violations"])


def controls(us):
    def rej(bad):
        return "ACCEPTED_WRONGLY" if bad else "REJECTED"
    c = {}
    c["R1_cone_read_satisfies_PN"] = rej(any(u["R1_fail_prunings"] == 0 for u in us.values()))
    c["R2_childcount_rule_satisfies_K"] = rej(any(u["R2_fail_carriers"] == 0 for u in us.values()))
    c["R3_F5_blind_at_every_position_with_children"] = rej(any(u["families"]["F5"]["blind"] == u["positions"] for u in us.values()))
    c["R4_inverse_depth_reads_satisfy_RS_F"] = rej(any(u["rs_f"]["inv"] == u["cones"] for u in us.values()))
    c["R5_PN_space_larger_than_depth_tables"] = rej(any(e["dims"]["PN"] > u["max_depth"] for u in us.values() for e in u["elimination"].values()))
    c["R6_genesis_blind_with_theta_zero"] = rej(any(u["total"][f]["0"]["blind_before"] > 0 for u in us.values() for f in CONST))
    c["R7_named_family_violates_PN"] = rej(any(e["pn_ok"] != e["pn_cases"] for u in us.values() for e in u["event"].values()))
    c["R8_lemma_dim_or_structure_fails"] = rej(any(u["lemma_ok_carriers"] != u["carriers"] for u in us.values()))
    return c


if __name__ == "__main__":
    main()
