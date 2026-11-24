"""T-269/T-270 bounded test of the NEW ASSUMPTION sharp E-alpha (preregistered at agent-thread 742ee354,
branch grok/ealpha-premise-test 21c1439e). Exact sympy on sparse basis-dictionary operators, plus a
fixed-seed (269) mpmath 50-digit random-input check for P-b. Prints one JSON document.
No verdict below upgrades anything: the premise stays NEW, the native bridge stays NOT_DERIVED."""
import itertools, json, random, sys
import sympy as sp
import mpmath as mp

R0 = sp.Rational
I_ = sp.I
s2 = sp.sqrt(2)
out = {"seed": 269, "sympy": sp.__version__, "mpmath": mp.__version__, "python": sys.version.split()[0]}

# ---------- sparse exact linear algebra on labelled basis tuples ----------
def vadd(acc, vec, c=1):
    for k, v in vec.items():
        acc[k] = sp.nsimplify(acc.get(k, 0) + c * v) if False else acc.get(k, 0) + c * v
    return acc

def clean(vec):
    r = {}
    for k, v in vec.items():
        v = sp.simplify(v)
        if v != 0:
            r[k] = v
    return r

def apply(V, vec):
    """V: function basis-tuple -> sparse vector (dict)."""
    acc = {}
    for k, c in vec.items():
        vadd(acc, V(k), c)
    return clean(acc)

def ptrace_op(x, y, keep):
    """Tr over positions not in keep of |x><y| (x,y sparse vectors over tuples). Returns dict (a,b)->coeff."""
    acc = {}
    for kx, cx in x.items():
        for ky, cy in y.items():
            tx = tuple(kx[i] for i in range(len(kx)) if i not in keep)
            ty = tuple(ky[i] for i in range(len(ky)) if i not in keep)
            if tx != ty:
                continue
            a = tuple(kx[i] for i in keep); b = tuple(ky[i] for i in keep)
            acc[(a, b)] = acc.get((a, b), 0) + cx * sp.conjugate(cy)
    return {k: sp.simplify(v) for k, v in acc.items() if sp.simplify(v) != 0}

def opeq(A, B):
    keys = set(A) | set(B)
    return all(sp.simplify(A.get(k, 0) - B.get(k, 0)) == 0 for k in keys)

def opsum(ops_coeffs):
    acc = {}
    for op, c in ops_coeffs:
        for k, v in op.items():
            acc[k] = acc.get(k, 0) + c * v
    return {k: sp.simplify(v) for k, v in acc.items() if sp.simplify(v) != 0}

def to_matrix(op, labels):
    idx = {l: i for i, l in enumerate(labels)}
    M = sp.zeros(len(labels))
    for (a, b), v in op.items():
        M[idx[a], idx[b]] += v
    return M

def half_trace_norm(M):
    M = sp.Matrix(M)
    if M.is_diagonal():
        return sp.nsimplify(sp.simplify(sum(sp.Abs(M[i, i]) for i in range(M.rows)) / 2))
    ev = M.eigenvals()
    return sp.simplify(sum(sp.Abs(e) * m for e, m in ev.items()) / 2)

# ---------- single-event benchmark (S,E,R) ----------
X = ['o', 'p', 'u', 'v']

def Cmap(s, t, P, U):
    """C_k(|s><t|) for one P1 event with erased u=U, parent p=P on basis labels; returns dict."""
    if s != U and t != U:
        return {(s, t): 1}
    if s == U and t == U:
        return {(P, P): 1}
    return {}

def frame_W(e0, eu):
    """frames are dicts (E,R)->coeff. W|j> = |j> e0 (j != u), W|u> = |p> eu. tuples (S,E,R)."""
    def V(k):
        (s,) = k
        if s == 'u':
            return {('p',) + kk: c for kk, c in eu.items()}
        return {(s,) + kk: c for kk, c in e0.items()}
    return V

ket = lambda e, r: {(e, r): 1}
def lin(*pairs):
    acc = {}
    for c, v in pairs:
        for k, x in v.items():
            acc[k] = acc.get(k, 0) + c * x
    return {k: sp.simplify(x) for k, x in acc.items() if sp.simplify(x) != 0}

def local(a, b, vec):
    """apply a (on E) ⊗ b (on R), 2x2 sympy matrices, to a K-vector."""
    acc = {}
    for (e, r), c in vec.items():
        for e2 in (0, 1):
            for r2 in (0, 1):
                acc[(e2, r2)] = acc.get((e2, r2), 0) + a[e2, e] * b[r2, r] * c
    return {k: sp.simplify(x) for k, x in acc.items() if sp.simplify(x) != 0}

th = sp.pi / 8
ga = sp.Matrix([[R0(3, 5), R0(-4, 5)], [R0(4, 5), R0(3, 5)]])
gb = sp.Matrix([[R0(3, 5), 4 * I_ / 5], [4 * I_ / 5, R0(3, 5)]])
assert sp.simplify(ga * ga.H - sp.eye(2)) == sp.zeros(2) and sp.simplify(gb * gb.H - sp.eye(2)) == sp.zeros(2)
FR = {
    'W_R': (ket(0, 0), ket(0, 1)),
    'W_R^g': (local(ga, gb, ket(0, 0)), local(ga, gb, ket(0, 1))),
    'W_E': (ket(0, 0), ket(1, 0)),
    'W_Bell': (lin((1 / s2, ket(0, 0)), (1 / s2, ket(1, 1))), lin((1 / s2, ket(0, 0)), (-1 / s2, ket(1, 1)))),
    'W_W': (ket(0, 0), lin((1 / s2, ket(0, 1)), (1 / s2, ket(1, 0)))),
    'W_ER': (ket(0, 0), ket(1, 1)),
    'W_theta(pi/8)': (lin((sp.cos(th), ket(0, 0)), (sp.sin(th), ket(1, 1))), lin((sp.cos(th), ket(0, 1)), (sp.sin(th), ket(1, 0)))),
}
EXPECT_ADMIT = {'W_R': True, 'W_R^g': True, 'W_E': False, 'W_Bell': False, 'W_W': False, 'W_ER': False, 'W_theta(pi/8)': False}

def single_checks(name, e0, eu):
    V = frame_W(e0, eu)
    res = {}
    # implements C on every matrix unit (trace E,R: keep position 0)
    ok = True
    for s in X:
        for t in X:
            got = ptrace_op(V((s,)), V((t,)), keep=[0])
            want = {((a,), (b,)): c for (a, b), c in Cmap(s, t, 'p', 'u').items()}
            ok &= opeq(got, want)
    res['implements_C_all_matrix_units'] = bool(ok)
    # isometry
    res['isometry'] = bool(all(sp.simplify(sum(V((s,)).get(k, 0) * sp.conjugate(V((t,)).get(k, 0)) for k in set(V((s,))) | set(V((t,)))) - (1 if s == t else 0)) == 0 for s in X for t in X))
    # (i) product / same-E-factor / orthogonal-R form
    Kv = lambda vec: {(k[1], k[2]): c for k, c in vec.items()}
    rhoE0 = to_matrix(ptrace_op(e0, e0, keep=[0]), [(0,), (1,)])
    rhoEu = to_matrix(ptrace_op(eu, eu, keep=[0]), [(0,), (1,)])
    sameE = sp.simplify(rhoE0 - rhoEu) == sp.zeros(2)
    pureE = sp.simplify((rhoE0 * rhoE0 - rhoE0)) == sp.zeros(2)
    form_i = bool(sameE and pureE)  # same pure E factor => both product; orthogonality of e0,eu then forces orthogonal R factors
    res['form_i_sameE_pure'] = form_i
    # (ii) D_E, D_R on benchmark pair z+ = (1,1,2,1)/5, z- = (1,1,1,2)/5
    zp = dict(zip(X, [R0(1, 5), R0(1, 5), R0(2, 5), R0(1, 5)]))
    zm = dict(zip(X, [R0(1, 5), R0(1, 5), R0(1, 5), R0(2, 5)]))
    def marg(z, pos):
        return opsum([(ptrace_op(V((s,)), V((s,)), keep=[pos]), z[s]) for s in X])
    DE = half_trace_norm(to_matrix(marg(zp, 1), [(0,), (1,)]) - to_matrix(marg(zm, 1), [(0,), (1,)]))
    DR = half_trace_norm(to_matrix(marg(zp, 2), [(0,), (1,)]) - to_matrix(marg(zm, 2), [(0,), (1,)]))
    res['D_E'] = str(sp.nsimplify(sp.simplify(DE))); res['D_R'] = str(sp.simplify(DR))
    form_ii = bool(sp.simplify(DE) == 0 and sp.simplify(DR - R0(1, 5)) == 0)
    res['form_ii_DE0_DR1/5'] = form_ii
    # basis form J_R W = W pi_u
    JR = lambda vec: {k: c for k, c in vec.items() if k[2] == 1}
    res['basis_form_JRW_eq_Wpiu'] = bool(all(opeq({(k, 0): v for k, v in JR(V((s,))).items()}, {(k, 0): v for k, v in (V((s,)) if s == 'u' else {}).items()}) for s in X))
    res['admitted'] = form_i and form_ii
    res['forms_agree'] = form_i == form_ii
    res['expected_admit'] = EXPECT_ADMIT[name]
    res['matches_expectation'] = res['admitted'] == EXPECT_ADMIT[name]
    return res

out['admission'] = {n: single_checks(n, *FR[n]) for n in FR}

# ---------- P-c regression: R(pi_p) == R(pi_v) under W_R ----------
VR = frame_W(*FR['W_R'])
out['P_c_regression_R(pi_p)==R(pi_v)_W_R'] = bool(opeq(ptrace_op(VR(('p',)), VR(('p',)), keep=[2]), ptrace_op(VR(('v',)), VR(('v',)), keep=[2])))

# ---------- two-event carriers ----------
A_S = ['o', 'p1', 'u1', 'p2', 'u2', 'v']
B_S = [(a, b) for a in X for b in X]
EV_A = {1: ('p1', 'u1'), 2: ('p2', 'u2')}

def Pk_A(k, s):
    P, U = EV_A[k]
    return P if s == U else s
def Pk_B(k, s):
    s = list(s)
    if s[k - 1] == 'u':
        s[k - 1] = 'p'
    return tuple(s)
def erased_A(k, s):
    return s == EV_A[k][1]
def erased_B(k, s):
    return s[k - 1] == 'u'

# native commutation P1P2 = P2P1 and channel commutation C1C2 = C2C1 (exact, on carriers)
def native_comm(S, Pk):
    return all(Pk(1, Pk(2, s)) == Pk(2, Pk(1, s)) for s in S)

def chan_A(k, s, t):
    P, U = EV_A[k]
    return Cmap(s, t, P, U)
def chan_B(k, s, t):
    i = k - 1
    if s[1 - i] != t[1 - i] and False:
        pass
    loc = Cmap(s[i], t[i], 'p', 'u')
    r = {}
    for (a, b), c in loc.items():
        s2_ = list(s); t2_ = list(t); s2_[i] = a; t2_[i] = b
        r[(tuple(s2_), tuple(t2_))] = c
    return r
def chan_apply(ch, k, op):
    acc = {}
    for (s, t), c in op.items():
        for kk, v in ch(k, s, t).items():
            acc[kk] = acc.get(kk, 0) + c * v
    return {kk: v for kk, v in acc.items() if v != 0}
def chan_comm(S, ch):
    for s in S:
        for t in S:
            u = {(s, t): 1}
            if not opeq(chan_apply(ch, 1, chan_apply(ch, 2, u)), chan_apply(ch, 2, chan_apply(ch, 1, u))):
                return False
    return True
out['native_P1P2_eq_P2P1'] = {'A': native_comm(A_S, Pk_A), 'B': native_comm(B_S, Pk_B)}
out['channel_C1C2_eq_C2C1'] = {'A': chan_comm(A_S, chan_A), 'B': chan_comm(B_S, chan_B)}

# Choi rank of composite C1C2 (Kraus products)
def choi_rank(S, kraus_list):
    idx = {s: i for i, s in enumerate(S)}
    n = len(S)
    def K(k, which):
        M = sp.zeros(n)
        P_, U_ = which
        for s in S:
            if k == 'Q':
                if not U_(s):
                    M[idx[s], idx[s]] = 1
            else:
                if U_(s):
                    M[idx[P_(s)], idx[s]] = 1
        return M
    mats = kraus_list(K)
    cols = [sp.Matrix(m.reshape(n * n, 1)) for m in mats]
    return sp.Matrix.hstack(*cols).rank()
def krausA(K):
    k1 = [K(t, (lambda s: Pk_A(1, s), lambda s: erased_A(1, s))) for t in ('Q', 'L')]
    k2 = [K(t, (lambda s: Pk_A(2, s), lambda s: erased_A(2, s))) for t in ('Q', 'L')]
    return [a * b for a in k1 for b in k2]
def krausB(K):
    k1 = [K(t, (lambda s: Pk_B(1, s), lambda s: erased_B(1, s))) for t in ('Q', 'L')]
    k2 = [K(t, (lambda s: Pk_B(2, s), lambda s: erased_B(2, s))) for t in ('Q', 'L')]
    return [a * b for a in k1 for b in k2]
out['choi_rank_C1C2'] = {'A': int(choi_rank(A_S, krausA)), 'B': int(choi_rank(B_S, krausB))}

# ---------- extensions. Tuple layout: (s, e, rcontent). E is a qubit initially 0 (E untouched = stays 0). ----------
def make_ext(name, carrier, mirror=False):
    Pk = Pk_A if carrier == 'A' else Pk_B
    er = erased_A if carrier == 'A' else erased_B
    if name == 'X1':
        fresh = (0, 0)
        def write(k, r):
            if r[k - 1] != 0:
                return None
            r = list(r); r[k - 1] = 1; return tuple(r)
    elif name == 'X3':
        fresh = ()
        def write(k, r):
            if k in r:
                return None
            return r + (k,)
    elif name == 'OVERWRITE':  # rejecting control: R qutrit holds latest label, old content displaced into E
        fresh = 0
    else:
        raise ValueError
    def V(k):
        def Vk(key):
            s, e, r = key
            if name == 'OVERWRITE':
                if er(k, s):
                    if e != 0:
                        return None
                    return {(Pk(k, s), r, k): 1}
                return {(s, e, r): 1}
            if er(k, s):
                w = write(k, r)
                if w is None:
                    return None
                if mirror:  # E-writing mirror control: record goes to E register instead; R untouched
                    raise ValueError
                return {(Pk(k, s), e, w): 1}
            return {(s, e, r): 1}
        return Vk
    return V, fresh

def make_mirror(name, carrier):
    """mirror control: identical write rule, but the record register is E and R stays blank."""
    Pk = Pk_A if carrier == 'A' else Pk_B
    er = erased_A if carrier == 'A' else erased_B
    freshE = (0, 0) if name == 'X1' else ()
    def write(k, r):
        if name == 'X1':
            if r[k - 1] != 0:
                return None
            r = list(r); r[k - 1] = 1; return tuple(r)
        if k in r:
            return None
        return r + (k,)
    def V(k):
        def Vk(key):
            s, e, r = key
            if er(k, s):
                w = write(k, e)
                if w is None:
                    return None
                return {(Pk(k, s), w, r): 1}
            return {(s, e, r): 1}
        return Vk
    return V, freshE, 0

def run_ext(V, S, carrier, fresh_e, fresh_r, label, U_R=None, upos=1):
    """upos = position of the factor that must stay untouched (1 = E for E-alpha; 2 = R for the E<->R mirror control)."""
    ch = chan_A if carrier == 'A' else chan_B
    er = erased_A if carrier == 'A' else erased_B
    res = {}
    def Vsafe(k):
        f = V(k)
        def g(key):
            r = f(key)
            if r is None:
                raise RuntimeError('undefined on reachable domain')
            return r
        return g
    try:
        V1, V2 = Vsafe(1), Vsafe(2)
        fresh = lambda s: {(s, fresh_e, fresh_r): 1}
        # domains: range of the other event's (fresh) output
        dom = {1: set(), 2: set()}
        for s in S:
            for kk in apply(V2, fresh(s)): dom[1].add(kk)
            for kk in apply(V1, fresh(s)): dom[2].add(kk)
        # (W) well-posed: per-event isometry on its domain and channel condition (C_k ⊗ id_E) after tracing R, on all matrix units
        W_ok = True
        for k, Vk in ((1, V1), (2, V2)):
            D = sorted(dom[k], key=str)
            imgs = {x: Vk(x) for x in D}
            for x in D:
                for y in D:
                    ip = sum(imgs[x].get(z, 0) * sp.conjugate(imgs[y].get(z, 0)) for z in set(imgs[x]) | set(imgs[y]))
                    if sp.simplify(ip - (1 if x == y else 0)) != 0:
                        W_ok = False
                    got = ptrace_op(imgs[x], imgs[y], keep=[0, upos])
                    base = ptrace_op({x: 1}, {y: 1}, keep=[0, upos])
                    want = {}
                    for ((a, ea), (b, eb)), c in base.items():
                        for (a2, b2), c2 in ch(k, a, b).items():
                            want[((a2, ea), (b2, eb))] = want.get(((a2, ea), (b2, eb)), 0) + c * c2
                    if not opeq(got, want):
                        W_ok = False
        res['W_well_posed'] = bool(W_ok)
        # (O) S⊗E channels of V12 and V21 equal on every matrix unit; composite implements C1C2 (trace E and R)
        V12 = {s: apply(V1, apply(V2, fresh(s))) for s in S}
        V21 = {s: apply(V2, apply(V1, fresh(s))) for s in S}
        O_ok = True; comp_ok = True
        for s in S:
            for t in S:
                if not opeq(ptrace_op(V12[s], V12[t], keep=[0, upos]), ptrace_op(V21[s], V21[t], keep=[0, upos])):
                    O_ok = False
                want = chan_apply(ch, 1, chan_apply(ch, 2, {(s, t): 1}))
                want = {((a,), (b,)): c for (a, b), c in want.items()}
                if not opeq(ptrace_op(V12[s], V12[t], keep=[0]), want):
                    comp_ok = False
        res['O_SE_channel_equal'] = bool(O_ok)
        res['composite_implements_C1C2'] = bool(comp_ok)
        if U_R is not None:
            res['explicit_U_R'] = U_R[0]
            res['explicit_U_R_identity_holds'] = bool(all(opeq(V12[s], {(a, e, U_R[1](r)): c for (a, e, r), c in V21[s].items()}) for s in S))
        # E untouched
        fz = fresh_e if upos == 1 else fresh_r
        res['untouched_factor_fixed'] = bool(all(k[upos] == fz for s in S for k in V12[s]) and all(k[upos] == fz for s in S for k in V21[s]))
        res['E_untouched_all_outputs'] = bool(all(k[1] == fresh_e for s in S for k in V12[s]) and all(k[1] == fresh_e for s in S for k in V21[s]))
        # (B) per-event benchmark contrasts at E and R (diagonal inputs, other event active)
        if carrier == 'A':
            pairs = {1: ([1, 1, 4, 1, 1, 2], [1, 1, 2, 1, 1, 4]), 2: ([1, 1, 1, 1, 4, 2], [1, 1, 1, 1, 2, 4])}
            pairs = {k: tuple(dict(zip(A_S, [R0(x, 10) for x in z])) for z in v) for k, v in pairs.items()}
        else:
            zp = dict(zip(X, [R0(1, 5), R0(1, 5), R0(2, 5), R0(1, 5)])); zm = dict(zip(X, [R0(1, 5), R0(1, 5), R0(1, 5), R0(2, 5)]))
            pairs = {1: ({(a, b): zp[a] * zp[b] for a, b in B_S}, {(a, b): zm[a] * zp[b] for a, b in B_S}),
                     2: ({(a, b): zp[a] * zp[b] for a, b in B_S}, {(a, b): zp[a] * zm[b] for a, b in B_S})}
        Bres = {}
        for k, (zplus, zminus) in pairs.items():
            def marg(z, pos):
                return opsum([(ptrace_op(V12[s], V12[s], keep=[pos]), z[s]) for s in S])
            dd = {}
            for pos, nm in ((1, 'D_E'), (2, 'D_R')):
                mp_, mm_ = marg(zplus, pos), marg(zminus, pos)
                labs = sorted({a for (a, b) in list(mp_) + list(mm_)} | {b for (a, b) in list(mp_) + list(mm_)}, key=str)
                dd[nm] = sp.simplify(half_trace_norm(to_matrix(mp_, labs) - to_matrix(mm_, labs)))
            Bres['event%d' % k] = {kk: str(v) for kk, v in dd.items()}
            Bres['event%d_ok' % k] = bool(dd['D_E'] == 0 and sp.simplify(dd['D_R'] - R0(1, 5)) == 0)
        res['B_contrasts'] = Bres
        res['B_E_blind_orbit'] = bool(res['E_untouched_all_outputs'] and Bres['event1_ok'] and Bres['event2_ok'])
        # triviality diagnostics
        res['doubly_written_branches'] = sum(1 for s in S if er(1, s) and er(2, s))
        res['PASS'] = bool(W_ok and O_ok and comp_ok and res['B_E_blind_orbit'])
    except RuntimeError as ex:
        res['W_well_posed'] = False; res['PASS'] = False; res['error'] = str(ex)
    return res

ext = {}
for carrier, S in (('A', A_S), ('B', B_S)):
    V, fr = make_ext('X1', carrier)
    r1 = run_ext(V, S, carrier, 0, fr, 'X1', U_R=('identity', lambda r: r))
    r1['trivial_reason'] = '(a) writes act on disjoint R factors by construction' + ('; (b) also holds' if r1.get('doubly_written_branches') == 0 else '')
    r1['verdict'] = ('PASS, non-discriminating' if r1['PASS'] else ('FAIL (ill-posed)' if not r1['W_well_posed'] else 'FAIL'))
    V, fr = make_ext('X3', carrier)
    swap = lambda r: {(1, 2): (2, 1), (2, 1): (1, 2)}.get(r, r)
    r3 = run_ext(V, S, carrier, 0, fr, 'X3', U_R=('swap [1,2]<->[2,1]', swap))
    triv3 = r3.get('doubly_written_branches', 1) == 0
    r3['trivial_reason'] = '(b) no doubly-written branch' if triv3 else 'none: a branch is written twice into the same register'
    r3['verdict'] = ('FAIL (ill-posed)' if not r3['W_well_posed'] else ('FAIL' if not r3['PASS'] else ('PASS, non-discriminating' if triv3 else 'PASS')))
    # X2 single shared qubit: rule-independent obstruction via Choi rank, plus explicit OR and XOR candidates
    cr = out['choi_rank_C1C2'][carrier]
    x2 = {'rule_independent_obstruction': 'composite would dilate C1C2 with environment dim 2 (E pure); needs Choi rank <= 2',
          'choi_rank': cr, 'obstruction_holds': cr > 2}
    for rule in ('OR', 'XOR'):
        Pk = Pk_A if carrier == 'A' else Pk_B; er = erased_A if carrier == 'A' else erased_B
        def Vq(k, rule=rule, Pk=Pk, er=er):
            def f(key):
                s, e, r = key
                if er(k, s):
                    return {(Pk(k, s), e, (1 if rule == 'OR' else 1 - r)): 1}
                return {(s, e, r): 1}
            return f
        x2[rule] = {kk: vv for kk, vv in run_ext(Vq, S, carrier, 0, 0, 'X2-' + rule).items() if kk in ('W_well_posed', 'composite_implements_C1C2', 'O_SE_channel_equal', 'PASS', 'error')}
    x2['verdict'] = 'FAIL (ill-posed)' if x2['obstruction_holds'] else 'UNDECIDED'
    passing = [(n, r['verdict']) for n, r in (('X1', r1), ('X3', r3))]
    if x2['verdict'].startswith('PASS'):
        passing.append(('X2', x2['verdict']))
    pv = [v for n, v in passing if v.startswith('PASS')]
    agg = 'FAIL' if not pv else ('PASS' if 'PASS' in pv else 'PASS, non-discriminating')
    ext[carrier] = {'X1': r1, 'X2': x2, 'X3': r3, 'aggregate': agg}

# rejecting controls for the P-a checker
rej = {}
V, fr = make_ext('OVERWRITE', 'B')
ro = run_ext(V, B_S, 'B', 0, fr, 'OVERWRITE')
rej['overwrite_to_E_B'] = {'O_SE_channel_equal': ro.get('O_SE_channel_equal'), 'E_untouched_all_outputs': ro.get('E_untouched_all_outputs'),
                           'rejected': (ro.get('O_SE_channel_equal') is False) and (ro.get('E_untouched_all_outputs') is False)}
V, fr = make_ext('X3', 'B')
rid = run_ext(V, B_S, 'B', 0, fr, 'X3-idU', U_R=('identity (forced)', lambda r: r))
rej['X3_B_with_U_R_identity'] = {'explicit_U_R_identity_holds': rid['explicit_U_R_identity_holds'], 'rejected': rid['explicit_U_R_identity_holds'] is False}
rej['X2_OR_composite_A'] = {'composite_implements_C1C2': ext['A']['X2']['OR']['composite_implements_C1C2'],
                            'rejected': ext['A']['X2']['OR']['composite_implements_C1C2'] is False}
mir = {}
for carrier, S in (('A', A_S), ('B', B_S)):
    for nm in ('X1', 'X3'):
        V, fe, frr = make_mirror(nm, carrier)
        # in the mirror the E slot is the register; reuse run_ext with fresh_e=register, fresh_r=0
        rm = run_ext(V, S, carrier, fe, frr, 'mirror-' + nm, upos=2)
        mir[carrier + '-' + nm] = {'W_well_posed': rm['W_well_posed'], 'O_SE_channel_equal': rm.get('O_SE_channel_equal'),
                                   'composite_implements_C1C2': rm.get('composite_implements_C1C2'), 'R_untouched': rm.get('untouched_factor_fixed'), 'B_E_blind_orbit': rm.get('B_E_blind_orbit'),
                                   'same_W_O_as_Ealpha': (rm['W_well_posed'] == ext[carrier][nm]['W_well_posed']) and (rm.get('O_SE_channel_equal') == ext[carrier][nm]['O_SE_channel_equal']) and (rm.get('composite_implements_C1C2') == ext[carrier][nm]['composite_implements_C1C2']),
                                   'B_contrasts': rm.get('B_contrasts')}
rej['mirror_E_writing'] = mir
out['P_a'] = ext
out['P_a_rejecting_controls'] = rej
out['P_a_headline_carrier_A'] = ext['A']['aggregate']
out['P_a_secondary_carrier_B'] = ext['B']['aggregate']

# ---------- P-b ----------
z_o, z_p, z_u, z_v = sp.symbols('z_o z_p z_u z_v', positive=True)
H = lambda *ps: -sum(p * sp.log(p) for p in ps)
grouping = sp.simplify(sp.expand_log(H(z_o, z_p, z_u, z_v) - H(z_o, z_p + z_u, z_v) - (z_p + z_u) * H(z_u / (z_p + z_u), z_p / (z_p + z_u)), force=True))
out['P_b_diag_grouping_identity_residual'] = str(grouping)
# F2 exact: premise realizations give omega_K = |alpha><alpha| ⊗ omega_R on 20 random rational inputs
rng = random.Random(269)
def rand_rat_rho(n):
    A = sp.Matrix(n, n, lambda i, j: sp.Rational(rng.randint(-5, 5)) + I_ * sp.Rational(rng.randint(-5, 5)))
    M = A * A.H
    return M / M.trace()
def dense_W(e0, eu):
    V = frame_W(e0, eu)
    labs = [(s, e, r) for s in X for e in (0, 1) for r in (0, 1)]
    M = sp.zeros(16, 4)
    for j, s in enumerate(X):
        for k, c in V((s,)).items():
            M[labs.index(k), j] = c
    return M, labs
def ptrace_dense(rho, labs, keep):
    kl = sorted({tuple(l[i] for i in keep) for l in labs})
    M = sp.zeros(len(kl))
    for a, la in enumerate(labs):
        for b, lb in enumerate(labs):
            if all(la[i] == lb[i] for i in range(3) if i not in keep):
                M[kl.index(tuple(la[i] for i in keep)), kl.index(tuple(lb[i] for i in keep))] += rho[a, b]
    return M, kl
F2 = {}
for nm in ('W_R', 'W_R^g'):
    W, labs = dense_W(*FR[nm])
    # alpha = E factor of e0 (pure E marginal)
    rE0 = to_matrix(ptrace_op(FR[nm][0], FR[nm][0], keep=[0]), [(0,), (1,)])
    ok = True
    for _ in range(20):
        rho = rand_rat_rho(4)
        om = W * rho * W.H
        K, kl = ptrace_dense(om, labs, keep=[1, 2])
        Rm, _ = ptrace_dense(om, labs, keep=[2])
        ok &= sp.simplify(K - sp.kronecker_product(rE0, Rm)) == sp.zeros(4)
    F2[nm] = bool(ok)
out['P_b_F2_premise_omegaK_eq_alpha_tensor_omegaR'] = F2

mp.mp.dps = 50
rngm = random.Random(269)
def mpS(M):
    ev = mp.eighe(M)[0] if hasattr(mp, 'eighe') else mp.eigh(M)[0]
    return -mp.fsum([x * mp.log(x, 2) for x in ev if x > mp.mpf(10) ** -45])
def mp_rand_rho(rank):
    A = mp.matrix(4, rank)
    for i in range(4):
        for j in range(rank):
            A[i, j] = mp.mpc(rngm.gauss(0, 1), rngm.gauss(0, 1))
    M = A * A.transpose_conj()
    tr = mp.fsum([M[i, i] for i in range(4)])
    return M / tr
def mp_ptrace(om, labs, keep):
    kl = sorted({tuple(l[i] for i in keep) for l in labs})
    M = mp.matrix(len(kl), len(kl))
    for a, la in enumerate(labs):
        for b, lb in enumerate(labs):
            if all(la[i] == lb[i] for i in range(3) if i not in keep):
                M[kl.index(tuple(la[i] for i in keep)), kl.index(tuple(lb[i] for i in keep))] += om[a, b]
    return M
def mpC(rho):
    idx = {s: i for i, s in enumerate(X)}
    M = mp.matrix(4, 4)
    for s in X:
        for t in X:
            for (a, b), c in Cmap(s, t, 'p', 'u').items():
                M[idx[a], idx[b]] += c * rho[idx[s], idx[t]]
    return M
inputs = []
for i in range(200):
    inputs.append(mp_rand_rho(1 + i % 4))
diag_specials = [[0, R0(1, 2), R0(1, 2), 0], [R0(1, 5), R0(1, 5), R0(2, 5), R0(1, 5)], [R0(1, 10), R0(3, 10), R0(3, 10), R0(3, 10)]]
Pb = {}
for nm in FR:
    W, labs = dense_W(*FR[nm])
    Wm = mp.matrix([[complex(sp.N(W[i, j], 60)) if False else mp.mpc(str(sp.re(sp.N(W[i, j], 60))), str(sp.im(sp.N(W[i, j], 60)))) for j in range(4)] for i in range(16)])
    minR = None; minK = None; maxE = mp.mpf(0); violR = 0
    allin = inputs + [mp.diag([mp.mpf(sp.Rational(x).p) / sp.Rational(x).q for x in d]) for d in diag_specials]
    rec_special = []
    for n_, rho in enumerate(allin):
        om = Wm * rho * Wm.transpose_conj()
        dS = mpS(rho) - mpS(mpC(rho))
        SR = mpS(mp_ptrace(om, labs, [2])); SE = mpS(mp_ptrace(om, labs, [1])); SK = mpS(mp_ptrace(om, labs, [1, 2]))
        sl = SR - dS; sk = SK - dS
        minR = sl if minR is None or sl < minR else minR
        minK = sk if minK is None or sk < minK else minK
        maxE = SE if SE > maxE else maxE
        if sl < -mp.mpf(10) ** -40:
            violR += 1
        if n_ >= len(inputs):
            rec_special.append({'z': [str(x) for x in diag_specials[n_ - len(inputs)]], 'S_R': mp.nstr(SR, 12), 'S_E': mp.nstr(SE, 12), 'dS': mp.nstr(dS, 12)})
    Pb[nm] = {'min_slack_R_ineq': mp.nstr(minR, 15), 'R_ineq_violations': violR, 'min_slack_K_ineq(F1)': mp.nstr(minK, 15),
              'F1_holds': bool(minK > -mp.mpf(10) ** -40), 'max_S_E_bits': mp.nstr(maxE, 15),
              'R_ineq_holds_all': violR == 0, 'S_E_zero_all': bool(maxE < mp.mpf(10) ** -40), 'diag_specials': rec_special}
out['P_b_numeric'] = Pb
out['P_b_downgraded_to_consistency_check'] = bool(all(Pb[n]['F1_holds'] for n in Pb) and all(F2.values()))
out['P_b_premise_realizations_pass_consistency'] = bool(all(Pb[n]['R_ineq_holds_all'] and Pb[n]['S_E_zero_all'] for n in ('W_R', 'W_R^g')))
print(json.dumps(out, indent=1, sort_keys=True, default=str))
