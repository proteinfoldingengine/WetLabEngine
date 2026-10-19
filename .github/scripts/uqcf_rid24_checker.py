"""receiver_identification d24 freeze checker (independent of the producer). Variables A(k, i) (cumulative depth
entries); trees as nested tuples grown by leaf attachment; holdings from deepest common ancestors; range ends certified
by the explicit multiplier certificates of the written proofs (Theorem 29.1 Steps 2-3, Theorem 30.1, Proposition 30.3(a))
on named carriers verified to belong to the class, and attained by explicit tables verified against every row."""
import sys, json, hashlib
from fractions import Fraction as Fr
from collections import deque

def norm(T): return tuple(sorted(norm(c) for c in T))
def attach_all(T):
    out = {norm(T + ((),))}
    for n, c in enumerate(T):
        for c2 in attach_all(c): out.add(norm(T[:n] + (c2,) + T[n + 1:]))
    return out
def universe(N):
    layers = [{()}]
    for _ in range(N - 1):
        layers.append({s for T in layers[-1] for s in attach_all(T)})
    return [T for L in layers for T in sorted(L)]
def cstr(T): return "(" + "".join(sorted(cstr(c) for c in T)) + ")"
def digest(cls): return hashlib.sha256("\n".join(sorted(cstr(T) for T in cls)).encode()).hexdigest()

class Tree:
    def __init__(self, T):
        self.par = [None]; self.dep = [0]; self.ch = [[]]; q = deque([(T, 0)])
        while q:
            node, v = q.popleft()
            for c in node:
                u = len(self.par); self.par.append(v); self.dep.append(self.dep[v] + 1); self.ch.append([]); self.ch[v].append(u); q.append((c, u))
        self.n = len(self.par)
    def dca_depth(self, a, b):
        while self.dep[a] > self.dep[b]: a = self.par[a]
        while self.dep[b] > self.dep[a]: b = self.par[b]
        while a != b: a, b = self.par[a], self.par[b]
        return self.dep[a]
    def hold(self, v, z):
        f = {}
        k = (self.dep[v], self.dca_depth(v, z)); f[k] = f.get(k, 0) + 1
        for u in self.ch[v]:
            k = (self.dep[u], self.dca_depth(u, z)); f[k] = f.get(k, 0) - 1
        return {a: b for a, b in f.items() if b}
    def hval(self, v, z, A): return sum((Fr(c) * A(*k) for k, c in self.hold(v, z).items()), Fr(0))

def from_par(par):
    ch = {v: [] for v in range(len(par))}
    for v in range(1, len(par)): ch[par[v]].append(v)
    def build(v): return norm(tuple(build(u) for u in ch[v]))
    return build(0)
def chainT(d):
    T = ()
    for _ in range(d): T = (T,)
    return T
def chain_plus(d, extra):  # chain of depth d with `extra` additional leaf children at its deepest vertex
    T = tuple(() for _ in range(extra))
    for _ in range(d): T = (T,)
    return norm(T)
def fork(k): return chain_plus(k, 2)
def combT(D, miss=None):
    par = [-1] + list(range(D))
    for k in range(D):
        if k != miss: par.append(k)
    return from_par(par)
def subtrees_closure(T):
    out = {norm(T)}; st = [norm(T)]
    def leaf_dels(T):
        res = set()
        for n, c in enumerate(T):
            if c == (): res.add(norm(T[:n] + T[n + 1:]))
            else:
                for c2 in leaf_dels(c): res.add(norm(T[:n] + (c2,) + T[n + 1:]))
        return res
    while st:
        x = st.pop()
        for y in leaf_dels(x):
            if y not in out: out.add(y); st.append(y)
    return sorted(out)
def maxch(T): return max([len(T)] + [maxch(c) for c in T]) if T else 0
def branch_set(T, d=0):
    s = {d} if len(T) >= 2 else set()
    for c in T: s |= branch_set(c, d + 1)
    return s
def nb_at(T, m, d=0):
    if d == m: return len(T) <= 1
    return all(nb_at(c, m, d + 1) for c in T)
def depth(T): return 1 + max(depth(c) for c in T) if T else 0

def rowset(cls):
    rs = set()
    for T in cls:
        t = Tree(T)
        for v in range(t.n):
            for z in range(t.n):
                h = t.hold(v, z)
                if h: rs.add(frozenset(h.items()))
    return rs
def vertex_at(t, dep_target):  # first vertex on the longest path at a given depth
    v = 0
    while t.dep[v] < dep_target:
        v = max(t.ch[v], key=lambda u: (len(t.ch[u]) > 0, -u))
    return v

def addf(f, g, s=Fr(1)):
    for k, c in g.items(): f[k] = f.get(k, Fr(0)) + s * c
def clean(f): return {k: c for k, c in f.items() if c != 0}

class Cert:
    def __init__(self, cls, rs, D):
        self.cls = set(cls); self.rs = rs; self.D = D; self.viol = 0
    def row(self, T, vdep, zdep, top_extra=0):
        """holding row of the vertex at depth vdep on carrier T (chain-like), grade at depth zdep of the main path"""
        if T not in self.cls: self.viol += 1; return {}
        t = Tree(T)
        v = vertex_at(t, vdep); z = vertex_at(t, zdep)
        h = t.hold(v, z)
        if frozenset(h.items()) not in self.rs: self.viol += 1
        return {k: Fr(c) for k, c in h.items()}
    def eq_diag(self, d):  # A(d,d) - 1 as combination of equalities (valid for d <= D)
        if d > self.D: self.viol += 1
        return {(d, d): Fr(1), "c": Fr(-1)}

def check_upper_zero(C, j, i):
    """certificate 0 - A(j,i) = sum lam r + equalities; returns the residual identity check."""
    combo = {}
    # Step 2 on Phi_i: receiver holds A(i,i) - A(i+1,i+1) - A(i+1,i) for z = one child
    T = fork(i)
    if T not in C.cls: C.viol += 1
    tt = Tree(T); v = [u for u in range(tt.n) if tt.dep[u] == i][0]; z = tt.ch[v][0]
    h = tt.hold(v, z)
    if frozenset(h.items()) not in C.rs: C.viol += 1
    addf(combo, {k: Fr(c) for k, c in h.items()})
    # + (A(i+1,i+1) - A(i,i)) equality
    if i + 1 > C.D: C.viol += 1
    addf(combo, {(i + 1, i + 1): Fr(1), (i, i): Fr(-1)})
    for d in range(i + 2, j + 1):  # Step 3: chain of depth d, z at depth i, vertex at depth d-1
        addf(combo, C.row(chainT(d), d - 1, i))
    target = {(j, i): Fr(-1)}
    return clean(combo) == target

def leak_identity(C, j, i, c):
    # exact identity: sum_{d} w_d r_d + w_0 r_0 - w_0 (A(i,i)-1) = U - A(j,i), w_0 = c^-(j-i-1), w_d = c^-(j-d+1)... built bottom-up
    total = {}
    U = Fr(1, c ** (j - i - 1))
    w = U  # weight of base row
    addf(total, C.row(chainT(i + 1), i, i), w)
    addf(total, {(i, i): Fr(-1)}, w); const = w
    for d in range(i + 2, j + 1):
        wd = Fr(1, c ** (j - d + 1))
        addf(total, C.row(chain_plus(d - 1, c), d - 1, i), wd)
    total = clean(total)
    return total == {(j, i): Fr(-1)} and const == U, U

def lower_zero(C, j, i):
    h = C.row(chainT(j), j, i)
    return h == {(j, i): Fr(1)}

# A-tables
def A_zero(k, i): return Fr(0)
def A_id(kap): return lambda k, i: Fr(kap) if i >= k else Fr(0)
def A_off(k, i):
    if k == 2 and i in (0, 1): return Fr(1) if i == 0 else Fr(0)
    return Fr(1) if i >= k else Fr(0)
def A_284c(k, i): return (Fr(1) if k <= 1 else Fr(2)) if i >= k else Fr(0)
def A_dump(k, i): return Fr(1)
def A_gpt(k, i): return {(0, 0): Fr(1), (1, 0): Fr(1, 2), (1, 1): Fr(1, 2)}.get((k, i), Fr(0))
def A_hor(B, D):
    def f(k, i):
        if k <= D: return Fr(1) if i >= k else Fr(0)
        if k == D + 1: return Fr(1, B) if i >= D else Fr(0)
        return Fr(0)
    return f
def A_nut(m, t):
    def f(k, i):
        if k == m + 1: return Fr(0) if i < m else (Fr(t) if i == m else Fr(1))
        return Fr(1) if i >= k else Fr(0)
    return f
def A_ext(B, m, j):
    def f(k, i):
        if m < k <= j and i == m: return Fr(1, B ** (k - m - 1))
        return Fr(1) if i >= k else Fr(0)
    return f

def pos_fast(cls, A):
    for T in cls:
        t = Tree(T)
        for v in range(t.n):
            for z in range(t.n):
                if t.hval(v, z, A) < 0: return False
    return True
def blind(A, D): return all(Tree(chainT(d)).hval(d - 1, d, A) == 0 for d in range(1, D + 1))
def gain(A, d): return Tree(chainT(d - 1)).hval(d - 1, d - 1, A) - Tree(chainT(d)).hval(d - 1, d, A)
def leafread_ok(cls, A):
    for T in cls:
        t = Tree(T)
        for l in range(1, t.n):
            if not t.ch[l] and any(t.hval(l, z, A) != 0 for z in range(t.n) if z != l): return False
    return True
def gplus(cls, A):
    for T in cls:
        t = Tree(T); tp = Tree((T,))  # tp vertex 0 = new Genesis; BFS labels shift by one
        for z in range(t.n):
            if tp.hval(0, z + 1, A) != 0: return False
            for v in range(t.n):
                if tp.hval(v + 1, z + 1, A) != t.hval(v, z, A): return False
    return True
def satisfies(cls, A, D):
    return pos_fast(cls, A) and blind(A, D) and A(0, 0) == 1

def main(outp):
    U = {N: universe(N) for N in (5, 6, 7, 8)}
    classes = {}
    for N in (5, 6, 7, 8): classes[f"BIN_{N}"] = [T for T in U[N] if maxch(T) <= 2]
    for N in (7, 8): classes[f"ALL_{N}"] = U[N]
    classes["CH_7"] = [chainT(d) for d in range(7)]
    for D in range(1, 5):
        classes[f"COMB_{D}"] = subtrees_closure(combT(D))
        for k in range(D): classes[f"COMB_{D}-{k}"] = subtrees_closure(combT(D, k))
    for B, ms in ((2, range(5)), (3, range(4))):
        for m in ms: classes[f"K_{B},{m}"] = [T for T in U[7] if maxch(T) <= B and nb_at(T, m)]
    systems = []
    for N in (5, 6, 7, 8): systems += [(f"BIN_{N}", D) for D in range(1, N)]
    for N in (7, 8): systems += [(f"ALL_{N}", D) for D in range(1, N)]
    systems += [("CH_7", D) for D in range(1, 7)]
    for D in range(1, 5):
        systems.append((f"COMB_{D}", D)); systems += [(f"COMB_{D}-{k}", D) for k in range(D)]
    systems += [(f"K_2,{m}", D) for m in range(5) for D in range(m + 1, 6)]
    systems += [(f"K_3,{m}", D) for m in range(4) for D in range(m + 1, 5)]
    res = {"classes": {n: {"carriers": len(c), "digest": digest(c)} for n, c in sorted(classes.items())}, "ranges": {}}
    viol = 0; rowcount = {}
    for (n, D) in systems:
        cls = classes[n]; rs = rowset(cls); rowcount[f"{n}|D={D}"] = len(rs); C = Cert(cls, rs, D)
        br = set().union(*[branch_set(T) for T in cls]); c = max(maxch(T) for T in cls)
        out = {}
        idok = satisfies(cls, A_id(1), D)
        if not idok: viol += 1
        for j in range(D + 1):
            for i in range(j + 1):
                if i == j: out[f"A({j},{i})"] = ["1", "1"]; continue  # equalities: A(j,j) = A(0,0) = 1
                if not lower_zero(C, j, i): viol += 1
                if i in br:
                    if not check_upper_zero(C, j, i): viol += 1
                    out[f"A({j},{i})"] = ["0", "0"]
                else:
                    cc = c if c >= 1 else 1
                    ok, Ub = leak_identity(C, j, i, cc)
                    if not ok: viol += 1
                    W = A_ext(cc, i, j)
                    if not (satisfies(cls, W, D) and W(j, i) == Ub): viol += 1
                    out[f"A({j},{i})"] = ["0", str(Ub)]
        viol += C.viol
        res["ranges"][f"{n}|D={D}"] = out
    # diagnostic (no blindness) is not certified by a proof; checker confirms the attaining table only
    res["diagnostic_nobl_BIN_7_attained_upper"] = str(A_gpt(1, 0)) if pos_fast(classes["BIN_7"], A_gpt) else None
    A7, A8 = classes["ALL_7"], classes["ALL_8"]
    W = {}
    W["W0"] = all(Tree(T).hval(v, z, A_zero) == 0 for T in A7 for v in range(Tree(T).n) for z in range(Tree(T).n)) and leafread_ok(A7, A_zero) and gplus(A7, A_zero) and all(gain(A_zero, d) == 0 for d in range(1, 7))
    W["W1"] = all(pos_fast(A7, A_id(k)) and pos_fast(A8, A_id(k)) and gplus(A7, A_id(k)) and all(gain(A_id(k), d) == k for d in range(1, 7)) for k in (1, 2)) and gplus(A7, A_id(-3)) and not pos_fast(A7, A_id(-3))
    W["W2"] = blind(A_off, 6) and Tree(chainT(2)).hval(2, 0, A_off) == 1
    W["W3"] = leafread_ok(A7, A_284c) and blind(A_284c, 1) and not gplus(A7, A_284c) and not blind(A_284c, 2)
    phi0 = Tree(fork(0))
    W["W4"] = pos_fast(classes["CH_7"], A_dump) and blind(A_dump, 6) and Tree(chainT(1)).hval(1, 0, A_dump) == 1 and phi0.hval(0, 1, A_dump) == -1
    W["W5"] = pos_fast(classes["BIN_7"], A_gpt) and Tree(chainT(1)).hval(0, 1, A_gpt) == Fr(1, 2)
    w6 = True
    for B in (2, 3):
        capB = [T for T in U[7] if maxch(T) <= B]
        for D in range(1, 6):
            A = A_hor(B, D); fan = Tree(chain_plus(D, B + 1))
            w6 &= pos_fast(capB, A) and blind(A, D) and Tree(chainT(D + 1)).hval(D + 1, D, A) == Fr(1, B) and fan.hval(D, D, A) == Fr(-1, B)
    W["W6"] = w6
    w7 = True
    for t in (Fr(1, 3), Fr(1, 2), Fr(1)):
        for m in range(4):
            cls = [T for T in U[7] if nb_at(T, m)]; A = A_nut(m, t)
            ph = Tree(fork(m)); v = [u for u in range(ph.n) if ph.dep[u] == m][0]
            ok = pos_fast(cls, A) and all(blind(A, D) for D in range(m + 1, 6))
            ok &= ph.hval(v, ph.ch[v][0], A) == -t and Tree(chainT(m + 1)).hval(m + 1, m, A) == t
            w7 &= ok
    W["W7"] = w7
    w8 = True
    for B in (2, 3):
        for m in range(3):
            for j in range(m + 1, 6):
                A = A_ext(B, m, j)
                w8 &= pos_fast(classes[f"K_{B},{m}"], A) and blind(A, 6) and Tree(chainT(j)).hval(j, m, A) == Fr(1, B ** (j - m - 1))
    W["W8"] = w8
    w9 = []
    for D in range(1, 5):
        g = combT(D); need = set(range(D))
        size = lambda T: 1 + sum(size(c) for c in T)
        small = sum(1 for T in U[8] if size(T) <= 2 * D and need <= branch_set(T))
        exact = sum(1 for T in U[8] if size(T) == 2 * D + 1 and need <= branch_set(T)) if 2 * D + 1 <= 8 else None
        w9.append([size(g), maxch(g), need <= branch_set(g), small, exact])
    W["W9"] = w9
    w10 = True
    for T in A7:
        t = Tree(T)
        for l in range(1, t.n):
            if t.ch[l]: continue
            for z in range(t.n):
                # cone total of l under e_z: 1 iff z in the cone of l, i.e. z == l for a leaf
                a = z
                while a is not None and a != l: a = t.par[a]
                w10 &= ((1 if a == l else 0) == (1 if z == l else 0))
    W["W10"] = w10
    res["witnesses"] = W
    c2 = Tree(chainT(2)); p00 = Tree(fork(0)); fan2 = Tree(chain_plus(1, 3))
    res["instances"] = {
        "Y1": [str(c2.hval(v, 0, A_off)) for v in range(3)],
        "Y2": str(p00.hval(0, 1, A_dump)),
        "Y3": str(Tree(chainT(1)).hval(0, 1, A_gpt)),
        "Y4": [str(c2.hval(2, 1, A_hor(2, 1))), str(fan2.hval(1, 1, A_hor(2, 1)))],
        "Y5": [str(p00.hval(0, 1, A_nut(0, Fr(1, 2)))), str(Tree(chainT(1)).hval(1, 0, A_nut(0, Fr(1, 2))))],
        "Y6": str(Tree(chainT(3)).hval(3, 0, A_ext(3, 0, 3))),
        "Y7": cstr(combT(2)),
    }
    cap3 = [T for T in U[7] if maxch(T) <= 3]
    R = {
        "R1": pos_fast(classes["BIN_5"], A_dump),
        "R2": res["ranges"]["CH_7|D=6"]["A(1,0)"][1] == "0",
        "R3": pos_fast(A7, A_off),
        "R4": Tree(chainT(1)).hval(0, 1, A_gpt) == 0,
        "R5": pos_fast(cap3, A_hor(2, 1)),
        "R6": any(pos_fast(classes["BIN_7"], A_nut(m, Fr(1, 2))) for m in range(4)),
        "R7": any(gain(A_zero, d) != 0 for d in range(1, 7)),
        "R8": gplus(A7, A_284c),
        "R9": any(res["ranges"][f"COMB_{D}-{k}|D={D}"][f"A({k+1},{k})"][1] == "0" for D in range(1, 5) for k in range(D)),
        "R10": any(r[3] != 0 for r in w9),
    }
    res["controls"] = {k: ("ACCEPTED" if v else "REJECTED") for k, v in R.items()}
    res["violations"] = viol
    res["diagnostic_row_counts_total"] = sum(rowcount.values())
    res["role"] = "checker"
    rp = "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d24_review/RESULT.md"
    try: res["result_sha256"] = hashlib.sha256(open(rp, "rb").read()).hexdigest()
    except OSError: res["result_sha256"] = None
    with open(outp, "w") as f: json.dump(res, f, indent=1, sort_keys=True)
    print("violations", viol, "systems", len(systems))

if __name__ == "__main__": main(sys.argv[1])
