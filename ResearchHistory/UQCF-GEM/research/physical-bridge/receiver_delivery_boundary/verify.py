"""T-240 independent verifier (stdlib only: fractions, json, hashlib).
Recomputes the entire canonical universe from the preregistered definitions with its own index arithmetic,
its own partition enumerator (restricted growth strings) and its own trace-norm routine, then requires exact
identity with the producer certificate and evaluates the preregistered predictions P1-P7.
Usage: verify.py certificate.json produce.py"""
import hashlib, json, sys
from fractions import Fraction as F
from math import isqrt

S = 'opuv'
F5 = F(1, 5)


def sqrt_exact(q):
    q = F(q)
    if q < 0:
        raise ValueError('negative')
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    if n * n != q.numerator or d * d != q.denominator:
        raise ValueError('irrational trace norm; outside verifier scope')
    return F(n, d)


def vec(entries):
    v = [F(0)] * 4
    for c, i in entries:
        v[i] += F(c)
    return v


FAM = {  # (e0, eu) over K basis |e r>, index 2e+r, re-declared from PREREGISTRATION.md section 4
    'W_E': (vec([(1, 0)]), vec([(1, 2)])),
    'W_R': (vec([(1, 0)]), vec([(1, 1)])),
    'W_M': (vec([(1, 0)]), vec([(F(3, 5), 2), (F(4, 5), 1)])),
    'W_N': (vec([(F(3, 5), 0), (F(4, 5), 3)]), vec([(1, 1)])),
}


def columns(e0, eu):
    """column j of W as dict {(s,k): amp}"""
    cols = {}
    for j in S:
        s, e = ('p', eu) if j == 'u' else (j, e0)
        cols[j] = {(s, k): a for k, a in enumerate(e) if a != 0}
    return cols


def inner(c1, c2):
    return sum(a * c2.get(key, 0) for key, a in c1.items())


def apply_W_to_unit(cols, a, b):
    """W |a><b| W^T as dict {((s,k),(t,l)): x}"""
    out = {}
    for k1, x in cols[a].items():
        for k2, y in cols[b].items():
            out[(k1, k2)] = out.get((k1, k2), 0) + x * y
    return out


def C_unit(a, b):
    """C(|a><b|) as dict {(s,t): x}"""
    if a == 'u' and b == 'u':
        return {('p', 'p'): F(1)}
    if a == 'u' or b == 'u':
        return {}
    return {(a, b): F(1)}


def trK(M):
    out = {}
    for ((s, k), (t, l)), x in M.items():
        if k == l:
            out[(s, t)] = out.get((s, t), 0) + x
    return {key: x for key, x in out.items() if x != 0}


def rgs_partitions(n):
    def rec(prefix, m):
        if len(prefix) == n:
            yield list(prefix)
            return
        for c in range(m + 2):
            yield from rec(prefix + [c], max(m, c))
    for code in rec([0], 0):
        blocks = {}
        for i, c in enumerate(code):
            blocks.setdefault(c, []).append(S[i])
        yield list(blocks.values())


def plabel(blocks):
    return '|'.join(''.join(b) for b in sorted((sorted(b, key=S.index) for b in blocks), key=lambda b: S.index(b[0])))


def diff_state(cols, zp, zm):
    D = {}
    for j in S:
        w = zp[S.index(j)] - zm[S.index(j)]
        if w == 0:
            continue
        for key, x in apply_W_to_unit(cols, j, j).items():
            D[key] = D.get(key, 0) + w * x
    return D


def kmat(D, block, keep):
    """K_A matrix after compressing to block and tracing S-block and K_B. keep in {'none','R','E','K'}"""
    dims = {'none': 1, 'R': 2, 'E': 2, 'K': 4}[keep]
    M = [[F(0)] * dims for _ in range(dims)]
    for ((s, k), (t, l)), x in D.items():
        if s != t or s not in block:
            continue
        ek, rk, el, rl = k // 2, k % 2, l // 2, l % 2
        if keep == 'none' and k == l:
            M[0][0] += x
        elif keep == 'R' and ek == el:
            M[rk][rl] += x
        elif keep == 'E' and rk == rl:
            M[ek][el] += x
        elif keep == 'K':
            M[k][l] += x
    return M


def tn_small(M):
    n = len(M)
    if n == 1:
        return abs(M[0][0])
    if n == 2:
        tr, det = M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]
        return abs(tr) if det >= 0 else sqrt_exact(tr * tr - 4 * det)
    raise ValueError('use rotated norm')


def tn_rotated(M, U):
    """trace norm of 4x4 M via the claimed orthogonal U (checked separately): U^T M U must be diagonal."""
    n = 4
    MU = [[sum(M[i][k] * U[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    R = [[sum(U[k][i] * MU[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    if any(R[i][j] != 0 for i in range(n) for j in range(n) if i != j):
        raise ValueError('rotated matrix not diagonal; outside verifier scope')
    return sum(abs(R[i][i]) for i in range(n))


def main():
    cert_path, prod_path = sys.argv[1], sys.argv[2]
    cert = json.load(open(cert_path))
    gates = {}
    prod_hash = hashlib.sha256(open(prod_path, 'rb').read()).hexdigest()
    gates['producer_hash_matches'] = cert.get('producer_sha256') == prod_hash
    # membership and orbit
    Us = {}
    mem_ok = True
    for n, (e0, eu) in FAM.items():
        cols = columns(e0, eu)
        iso = all(inner(cols[a], cols[b]) == (1 if a == b else 0) for a in S for b in S)
        impl = all(trK(apply_W_to_unit(cols, a, b)) == C_unit(a, b) for a in S for b in S)
        U = [[F(x) for x in row] for row in cert['membership'][n]['U']]
        orth = all(sum(U[k][i] * U[k][j] for k in range(4)) == (1 if i == j else 0) for i in range(4) for j in range(4))
        # (I x U) W_E = W  <=>  U e0(W_E) = e0, U eu(W_E) = eu ; W_E has e0=|00>, eu=|10>
        orbit = [U[i][0] for i in range(4)] == e0 and [U[i][2] for i in range(4)] == eu
        Us[n] = U
        rec = cert['membership'][n]
        mine = {'isometry': iso, 'implements_C_all_16_units': impl, 'U_orthogonal': orth, 'equals_IxU_W_E': orbit}
        mem_ok &= all(mine.values()) and all(rec[k] == v for k, v in mine.items())
    swap_ok = FAM['W_R'][1] == [FAM['W_E'][1][2 * (i % 2) + i // 2] for i in range(4)] and FAM['W_R'][0] == FAM['W_E'][0]
    gates['P1_membership_orbit_swap'] = mem_ok and swap_ok and cert['membership'].get('W_R_equals_IxSWAP_W_E') is True
    # recompute universe
    pairs = {'canonical': ([F5, F5, 2 * F5, F5], [F5, F5, F5, 2 * F5]),
             'removed_summand': ([F5, 2 * F5, F5, F5], [F5, F5, 2 * F5, F5])}
    keepmap = {'T0': 'none', 'TR': 'R', 'TE': 'E', 'TK': 'K'}
    mine = {}
    for pname, (zp, zm) in pairs.items():
        dz = [a - b for a, b in zip(zp, zm)]
        dy = {'o': dz[0], 'p': dz[1] + dz[2], 'v': dz[3]}
        for blocks in rgs_partitions(4):
            lab = plabel(blocks)
            blind = all(sum(dz[S.index(s)] for s in b) == 0 for b in blocks)
            ret = sum(abs(sum(dy.get(s, 0) for s in b)) for b in blocks) / 2
            con = {}
            for n, (e0, eu) in FAM.items():
                D = diff_state(columns(e0, eu), zp, zm)
                con[n] = {}
                for t, keep in keepmap.items():
                    norms = [tn_rotated(kmat(D, b, keep), Us[n]) if keep == 'K' else tn_small(kmat(D, b, keep)) for b in blocks]
                    con[n][t] = str(sum(norms) / 2)
            mine[(pname, lab)] = {'pair': pname, 'partition': lab, 'initially_blind': blind, 'retained_output_contrast': str(ret), 'contrast': con}
    recs = cert.get('records', [])
    keys = [(r.get('pair'), r.get('partition')) for r in recs]
    gates['record_set_exact'] = len(keys) == len(set(keys)) == len(mine) == 30 and set(keys) == set(mine)
    gates['records_identical'] = gates['record_set_exact'] and all(mine[(r['pair'], r['partition'])] == r for r in recs)
    M = {k: v for k, v in mine.items()}
    fam = list(FAM)
    q = lambda s: F(s)
    gates['P2_T0_TK_realization_invariant'] = all(len({M[k]['contrast'][n][t] for n in fam}) == 1 for k in M for t in ('T0', 'TK'))
    p3 = True
    for k, r in M.items():
        t0 = q(r['contrast']['W_E']['T0'])
        p3 &= t0 == q(r['retained_output_contrast'])
        for t, best in (('TR', 'W_E'), ('TE', 'W_R')):
            vals = {n: q(r['contrast'][n][t]) for n in fam}
            p3 &= min(vals.values()) == t0 == vals[best]
    gates['P3_min_equals_retained_contrast'] = p3
    tr = M[('canonical', 'opuv')]['contrast']
    gates['P4_trivial_partition_values'] = (
        all(tr[n]['T0'] == '0' and tr[n]['TK'] == '1/5' for n in fam)
        and [tr[n]['TR'] for n in fam] == ['0', '1/5', '16/125', '9/125']
        and [tr[n]['TE'] for n in fam] == ['1/5', '0', '9/125', '16/125'])
    good = sorted(k[1] for k, r in M.items() if k[0] == 'canonical' and r['initially_blind'] and q(r['retained_output_contrast']) > 0)
    gates['P5_blind_and_guaranteed'] = (good == sorted(['o|p|uv', 'ouv|p', 'op|uv'])
                                        and all(M[('canonical', g)]['retained_output_contrast'] == '1/5' for g in good)
                                        and M[('canonical', 'o|puv')]['initially_blind'] and M[('canonical', 'o|puv')]['retained_output_contrast'] == '0')
    rs = M[('removed_summand', 'opuv')]['contrast']
    gates['P6_removed_summand'] = (all(q(r['retained_output_contrast']) == 0 for k, r in M.items() if k[0] == 'removed_summand')
                                   and rs['W_E']['TR'] == '0' and rs['W_R']['TR'] == '1/5' and all(rs[n]['TK'] == '1/5' for n in fam))
    def trE(e):
        return [[sum(e[2 * x + r] * e[2 * x + s] for x in range(2)) for s in range(2)] for r in range(2)]
    pred = cert.get('predicates', {})
    mine_pred = {n: {'invariant_choi_equals_C': all(trK(apply_W_to_unit(columns(*FAM[n]), a, b)) == C_unit(a, b) for a in S for b in S),
                     'factor_naming_kR': trE(FAM[n][1]) != trE(FAM[n][0])} for n in fam}
    gates['P7_predicates'] = (pred == mine_pred and all(mine_pred[n]['invariant_choi_equals_C'] for n in fam)
                              and [mine_pred[n]['factor_naming_kR'] for n in fam] == [False, True, True, True])
    status = 'GREEN' if all(gates.values()) else 'RED'
    sys.stdout.write(json.dumps({'status': status, 'gates': gates, 'records_checked': len(recs)}, indent=1, sort_keys=True) + '\n')
    if status != 'GREEN':
        sys.exit(1)


if __name__ == '__main__':
    main()
