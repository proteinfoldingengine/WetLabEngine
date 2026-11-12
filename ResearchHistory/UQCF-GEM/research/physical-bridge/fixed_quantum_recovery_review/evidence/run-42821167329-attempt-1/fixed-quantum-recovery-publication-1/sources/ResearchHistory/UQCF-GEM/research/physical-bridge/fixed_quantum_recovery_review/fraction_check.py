#!/usr/bin/env python3
"""Independent rational reconstruction. No external packages or producer imports.

Each encoding is (integer columns, squared common amplitude factor). Outputs
use E_ij in lexicographic (i,j) order. Amplitude intertwiners are returned before
applying that common factor; all density-operator outputs are actual outputs.
"""
import json
from fractions import Fraction as Q


def zero(m, n):
    return [[Q(0) for _ in range(n)] for _ in range(m)]


def eye(n):
    a = zero(n, n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def unit(m, n, i, j):
    a = zero(m, n)
    a[i][j] = Q(1)
    return a


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(*arrays):
    return [[sum((a[i][j] for a in arrays), Q(0))
             for j in range(len(arrays[0][0]))] for i in range(len(arrays[0]))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def tr(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def sand(k, x):
    return mul(mul(k, x), transpose(k))


def idx(s, e, r):
    return 4 * s + 2 * e + r


def reduce_s(x):
    return [[sum((x[idx(s,e,r)][idx(t,e,r)] for e in range(2) for r in range(2)), Q(0))
             for t in range(4)] for s in range(4)]


def reduce_r(x):
    return [[sum((x[idx(s,e,r)][idx(s,e,t)] for s in range(4) for e in range(2)), Q(0))
             for t in range(2)] for r in range(2)]


def encode(w, factor, x):
    return scale(factor, sand(w, x))


def serialize(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {k: serialize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serialize(v) for v in x]
    return x


def reconstruct():
    units = [unit(4,4,i,j) for i in range(4) for j in range(4)]
    tau = unit(4,4,0,0)
    wr, b, bell, a = (zero(16,4) for _ in range(4))
    for j in (0,1,3):
        wr[idx(j,0,0)][j] = b[idx(j,0,0)][j] = Q(1)
        bell[idx(j,0,0)][j] = bell[idx(j,1,1)][j] = Q(1)
        a[idx(j,0,0)][j] = a[idx(j,0,1)][j] = Q(1)
    wr[idx(1,0,1)][2] = b[idx(1,1,0)][2] = Q(1)
    bell[idx(1,0,0)][2], bell[idx(1,1,1)][2] = Q(1), Q(-1)
    a[idx(1,1,0)][2], a[idx(1,1,1)][2] = Q(1), Q(-1)
    enc = {'WR':(wr,Q(1)), 'B':(b,Q(1)), 'Bell':(bell,Q(1,2)), 'A':(a,Q(1,2))}
    ls = [zero(4,16), zero(4,16)]
    for r in range(2):
        for j in (0,1,3):
            ls[r][j][idx(j,0,r)] = Q(1)
        ls[r][2][idx(1,1,r)] = Q((-1)**r)
    products = [mul(transpose(l),l) for l in ls]
    p = add(*products)
    comp = add(eye(16), scale(-1,p))
    complement_kraus = [unit(4,16,0,k) for k in range(16) if comp[k][k] == 1]
    complement_products = [mul(transpose(k),k) for k in complement_kraus]
    def quantum(x):
        return add(*(sand(l,x) for l in ls),scale(tr(mul(comp,x)),tau))
    labels = [s for s in range(4) for e in range(2) for r in range(2)]
    labels[idx(1,0,1)] = labels[idx(1,1,0)] = 2
    def classical(x):
        out = zero(4,4)
        for k, label in enumerate(labels):
            out[label][label] += x[k][k]
        return out
    f = [[Q(1,2),Q(-1,2)],[Q(-1,2),Q(1,2)]]
    full_f = zero(16,16)
    ge = zero(16,16)
    for s in range(4):
        for e in range(2):
            for r in range(2):
                ge[idx(s,e,r)][idx(s,e,r)] = Q(e)
                for t in range(2):
                    full_f[idx(s,e,r)][idx(s,e,t)] = f[r][t]
    piu = unit(4,4,2,2)
    g = add(*(sand(transpose(l),piu) for l in ls))
    source_plus = zero(4,4)
    source_minus = zero(4,4)
    for j, (v,w) in enumerate(zip((1,1,2,1),(1,1,1,2))):
        source_plus[j][j], source_minus[j][j] = Q(v,5), Q(w,5)
    delta = add(source_plus,scale(-1,source_minus))
    result = {'schema':'fixed-common-decoder-v1','encodings':{},'classical':{},'quantum':{},
              'common':{'L0':ls[0],'L1':ls[1], 'L_products':products,
                        'complement_kraus':complement_kraus,'complement_products':complement_products,
                        'P':p,'complement':comp,'kraus_normalization':add(*products,*complement_products),
                        'G':g,'GE':ge,'PGP':sand(p,g),'PGEP':sand(p,ge),'F':f,
                        'pullback_F':{},'intertwiner_scaled':{}},
              'pair':{'source_plus':source_plus,'source_minus':source_minus,'delta':delta,
                      'r_plus':{},'r_minus':{},'r_delta':{},'F_probabilities':{},'E_probabilities':{},
                      'initial_R':unit(2,2,0,0)}}
    for name,(w,factor) in enc.items():
        proj = scale(factor,mul(w,transpose(w)))
        remainder = add(eye(16),scale(-1,proj))
        def recover_individual(x):
            return add(scale(factor,sand(transpose(w),x)),scale(tr(mul(remainder,x)),tau))
        encoded = [encode(w,factor,x) for x in units]
        result['encodings'][name] = {'columns_scaled':w,'column_scale_squared':factor,
            'gram':scale(factor,mul(transpose(w),w)), 'channel':[reduce_s(x) for x in encoded],
            'r_receiver':[reduce_r(x) for x in encoded],
            'individual_recovery':[recover_individual(x) for x in encoded],
            'individual_tp':add(proj,remainder),'individual_image_projection':proj}
        result['classical'][name] = [classical(x) for x in encoded]
        result['quantum'][name] = [quantum(x) for x in encoded]
        result['common']['pullback_F'][name] = scale(factor,sand(transpose(w),full_f))
        result['common']['intertwiner_scaled'][name] = {'L0':mul(ls[0],w),'L1':mul(ls[1],w), 'complement':mul(comp,w)}
        xp,xm = encode(w,factor,source_plus),encode(w,factor,source_minus)
        rp,rm = reduce_r(xp),reduce_r(xm)
        result['pair']['r_plus'][name], result['pair']['r_minus'][name] = rp,rm
        result['pair']['r_delta'][name] = add(rp,scale(-1,rm))
        fp,fm = tr(mul(f,rp)),tr(mul(f,rm))
        result['pair']['F_probabilities'][name] = [fp,fm,fp-fm]
        result['pair']['E_probabilities'][name] = [tr(mul(ge,xp)),tr(mul(ge,xm))]
    # Compute channel directly from its separately stated source formula.
    q = eye(4)
    q[2][2] = Q(0)
    def channel(x):
        return add(sand(q,x),scale(x[2][2],unit(4,4,1,1)))
    result['declared_channel'] = [channel(x) for x in units]
    result['pair']['channel_plus'] = channel(source_plus)
    result['pair']['channel_minus'] = channel(source_minus)
    gp = [[Q(x) for x in row] for row in ((1,0,0,0),(0,1,1,0),(0,0,0,1))]
    gi = [[Q(x) for x in row] for row in ((1,0,0),(0,1,0),(0,0,0),(0,0,1))]
    loss = add(eye(4),scale(-1,mul(gi,gp)))
    witness = [[Q(x)] for x in (0,-1,1,0)]
    result['grades'] = {'P':gp,'I':gi,'PI':mul(gp,gi),'loss_map':loss,
        'kernel_witness':witness,'kernel_image':mul(gp,witness),
        'loss_plus':mul(loss,[[source_plus[j][j]] for j in range(4)]),
        'loss_minus':mul(loss,[[source_minus[j][j]] for j in range(4)])}
    outside = unit(16,16,idx(2,0,0),idx(2,0,0))
    bad_l1 = [row[:] for row in ls[1]]
    bad_l1[2][idx(1,1,1)] = Q(1)
    apu = encode(a,Q(1,2),unit(4,4,1,2))
    offcode = unit(16,16,idx(0,1,0),idx(0,1,0))
    result['adverse'] = {
        'dropped_complement_output':add(*(sand(l,outside) for l in ls)),
        'removed_phase_pu':add(sand(ls[0],apu),sand(bad_l1,apu),scale(tr(mul(comp,apu)),tau)),
        'old_WR_u':quantum(encode(wr,Q(1),piu)),
        'offcode_G_GE':[tr(mul(g,offcode)),tr(mul(ge,offcode))]}
    # Assertions are intentionally evaluated only on an authorized script run.
    for name in enc:
        assert result['encodings'][name]['gram'] == eye(4), name
        assert result['encodings'][name]['channel'] == result['declared_channel'], name
        assert result['encodings'][name]['individual_recovery'] == units, name
        assert result['encodings'][name]['individual_tp'] == eye(16), name
    assert mul(p,p) == p and tr(p) == 8
    assert result['common']['kraus_normalization'] == eye(16)
    for name in ('A','B'):
        assert result['quantum'][name] == units, name
        assert mul(comp,enc[name][0]) == zero(16,4)
        assert result['pair']['E_probabilities'][name] == [Q(2,5),Q(1,5)]
    assert mul(ls[0],b) == eye(4) and mul(ls[1],b) == zero(4,4)
    assert mul(ls[0],a) == eye(4) and mul(ls[1],a) == eye(4)
    assert mul(transpose(a),b) == eye(4)  # Actual A†B has factor 1/sqrt(2).
    for name in ('WR','B'):
        for j in range(4):
            assert result['classical'][name][5*j] == units[5*j]
        assert result['classical'][name][1] != units[1]
    assert result['classical']['Bell'][10] == unit(4,4,1,1)
    for k,x in enumerate(units):
        assert result['encodings']['B']['r_receiver'][k] == scale(tr(x),unit(2,2,0,0))
        plus = [[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]]
        assert result['encodings']['A']['r_receiver'][k] == add(scale(tr(mul(q,x)),plus),scale(x[2][2],f))
    assert result['common']['pullback_F']['A'] == piu
    assert result['common']['pullback_F']['B'] == scale(Q(1,2),eye(4))
    assert result['pair']['F_probabilities']['A'] == [Q(2,5),Q(1,5),Q(1,5)]
    assert result['pair']['F_probabilities']['B'] == [Q(1,2),Q(1,2),Q(0)]
    declared_g = zero(16,16)
    for r in range(2):
        declared_g[idx(1,1,r)][idx(1,1,r)] = Q(1)
    assert g == declared_g and mul(g,g) == g
    assert sand(p,g) == sand(p,ge) and g != ge
    assert mul(gp,gi) == eye(3) and mul(gp,witness) == zero(3,1)
    assert loss == mul(witness,[[Q(0),Q(0),Q(1),Q(0)]])
    assert add(mul(gi,gp),loss) == eye(4)
    assert result['adverse']['dropped_complement_output'] == zero(4,4)
    assert result['adverse']['removed_phase_pu'] == zero(4,4)
    assert result['adverse']['old_WR_u'] == unit(4,4,1,1)
    assert result['adverse']['offcode_G_GE'] == [Q(0),Q(1)]
    return serialize(result)


if __name__ == '__main__':
    print(json.dumps(reconstruct(),sort_keys=True,separators=(',',':')))
