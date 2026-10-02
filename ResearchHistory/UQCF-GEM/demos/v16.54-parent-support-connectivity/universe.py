"""Producer enumeration of the approved finite mechanism domains."""
from collections import defaultdict
from itertools import combinations, permutations, product
import json
import math
import sqlite3
import tempfile

def bits(mask):
    return [i for i in range(mask.bit_length()) if mask & (1 << i)]

def case(family, kind, k, floors, q, roots, choice, **extra):
    return {'identity': [family, dict(kind=kind, k=k, a=list(floors), q=q, **extra),
                         [sorted(row) for row in roots], choice]}

def parts(sizes):
    start, answer = 0, []
    for size in sizes:
        answer.append(list(range(start, start + size)))
        start += size
    return answer

def core(groups, rank, cyclic=False):
    rows = [list(e) for g in groups for e in combinations(g, rank)]
    if cyclic:
        rows += [sorted([*e, z]) for j in range(3)
                 for e in combinations(groups[j], 2) for z in groups[(j+1)%3]]
    return sorted(rows)

def m1(protocol):
    for t in (4, 5, 6):
        pairs = list(permutations(range(t), 2))
        for mask in range(1, 1 << t):
            tail = bits(mask)
            roots = [[x] for x in range(t)] + [tail]
            for floor in range(1, len(tail)+1):
                a = [1]*t + [floor]
                for pair in pairs:
                    yield case('M1', 'packet', t, a, t, roots, list(pair))
                for first, second in product(pairs, repeat=2):
                    yield case('M1', 'double_packet', t, a, t, roots, [list(first), list(second)])
                for i, row in enumerate(roots):
                    for x in range(t):
                        if x in row:
                            continue
                        same = i == t or tail == [i]
                        for left in pairs:
                            for right in pairs if same else [None]:
                                for reverse in (False, True):
                                    yield case('M1', 'neighbor', t, a, t, roots,
                                               {'edge': [i,x], 'left': list(left),
                                                'right': list(right) if right else None,
                                                'reverse': reverse})
                yield case('M1', 'layers', t, a, 3, roots, {'peak': t})

def m2(protocol):
    grouped = defaultdict(list)
    for masks in product(range(1,16), repeat=3):
        if sum(x.bit_count() for x in masks) >= 8:
            continue
        if any(sum(bool(x & (1 << j)) for x in masks) > 2 for j in range(4)):
            continue
        grouped[tuple(x.bit_count() for x in masks)].append([bits(x) for x in masks])
    for a, states in sorted(grouped.items()):
        for left, right in product(states, repeat=2):
            yield case('M2','degree2',4,a,None,left,{'target':right})
    for caps in product(range(5), repeat=3):
        if sum(caps) < 5:
            continue
        owners = [o for o in product(range(3), repeat=4)
                  if all(o.count(i) <= caps[i] for i in range(3))]
        for left, right in product(owners, repeat=2):
            blocks = [[x for x in range(4) if left[x] == i] for i in range(3)]
            target = [[x for x in range(4) if right[x] == i] for i in range(3)]
            yield case('M2','element',4,[0,0,0],None,blocks,{'target':target},
                       capacities=list(caps),representation='blocks')
    yield case('M2','forced_cycle',5,[2,2,4],None,[[0,2],[1,3],[0,1,2,3]],
               {'target':[[1,3],[0,2],[0,1,2,3]],
                'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4})

def m3(protocol):
    for q,z in product((3,4),(0,1,2)):
        for k in (q,q+1):
            grouped = defaultdict(list)
            for owner in product(range(q),repeat=k):
                if len(set(owner)) != q:
                    continue
                rows = [[x for x in range(k) if owner[x] == i] for i in range(q)]
                grouped[tuple(map(len,rows))].append(rows)
            for widths,states in grouped.items():
                for left,right in product(states,repeat=2):
                    yield case('M3','saturated',k,list(widths)+[k]*z,q,
                               left+[list(range(k)) for _ in range(z)],
                               {'target':right+[list(range(k)) for _ in range(z)]},hubs=z)
    for labels in product(range(3),repeat=3):
        yield case('M3','classify',3,[1,1,1],3,[[x] for x in labels],{})

def m4(protocol):
    unsafe = [[0,1,2],[0,3,4],[1,5,6],[2,7,8]]
    fan = [[0,1,2],[0,1,3],[0,1,4],[0,5,6],[1,7,8],[2,3,4]]
    specs = [('unsafe',unsafe,9,3,[[0,1]],3,'HYPEREDGE_CLONE_BOUNDARY.md'),
             ('unsafe_twice',unsafe+[[x+9 for x in row] for row in unsafe],18,6,
              [[0,1],[9,10]],3,'HYPEREDGE_CLONE_BOUNDARY.md')]
    for g in (0,1,2):
        rows = fan+[list(range(9+3*j,12+3*j)) for j in range(g)]
        specs.append(('fan',rows,9+3*g,3+g,[[0,1]],3,'CONTRACTION_CLONE_GUARD.md'))
    specs.append(('empty',[[0,1],[0,2],[1,3],[4,5]],6,3,[[0,1]],2,
                  'PROSPECTIVE_VALIDATION_PLAN.md'))
    for tag,rows,k,q,ops,h,document in specs:
        digest = protocol['approved_plan_sha256'] if document.endswith('PLAN.md') else protocol['proofs'][document]
        for shift in range(len(rows)):
            moved = [rows[(j-shift)%len(rows)] for j in range(len(rows))]
            yield case('M4','clone_sequence',k,[h]*len(rows),q,moved,
                       {'operations':ops,'shift':shift},tag=tag,source=document,source_sha256=digest)

def m5(protocol):
    templates = []
    for h,m in product((3,4),(1,2,3)):
        for sizes in product(range(h,h+3),repeat=m):
            if sum(sizes)<=10 and sum(s-h+1 for s in sizes)>=3:
                templates.append(('module',h,sizes))
    for k in (6,7,8,9):
        for a in range(1,k-1):
            for b in range(1,k-a):
                templates.append(('cyclic',3,(a,b,k-a-b)))
    for form,h,sizes in templates:
        base = core(parts(sizes),h,form=='cyclic')
        k = sum(sizes)
        q = k-3 if form=='cyclic' else sum(s-h+1 for s in sizes)
        moves = [[i,(i+1)%3] for i in range(3) if sizes[i]>=sizes[(i+1)%3]+1] if form=='cyclic' else [
            [i,j] for i in range(len(sizes)) for j in range(len(sizes)) if sizes[i]>=sizes[j]+2]
        for d in (0,1,2):
            for extras in ('P',) if d==0 else ('P','duplicate'):
                rows = base+[(list(range(k)) if extras=='P' else base[0]) for _ in range(d)]
                extra = dict(form=form,h=h,sizes=list(sizes),extras=extras,d=d)
                yield case('M5','balance',k,[h]*len(rows),q,rows,{},**extra)
                for move in moves:
                    yield case('M5','relocate',k,[h]*len(rows),q,rows,move,**extra)
    left,right = core(parts((3,5)),3),core(parts((4,4)),3)
    yield case('M5','module_pair',8,[3]*11,4,left,{'target':right+[right[0]]*3},
               h=3,sizes=[3,5],form='module')
    rows = core(parts((3,2,2)),3,True)
    yield case('M5','obstruction',7,[3]*len(rows),4,rows,{},sizes=[3,2,2])

def guard_case(h,q,r,shift,reverse,family='M6'):
    n,k = math.comb(h+q-2,h),2*h+q-2
    rows = [list(e) for e in combinations(range(h+q-2),h)]
    rows += [list(range(h+q-2,k))]+[list(range(k)) for _ in range(r-n-1)]
    transformed = [sorted(k-1-x for x in row) if reverse else list(row) for row in rows]
    target = [transformed[(i-shift)%r] for i in range(r)]
    return case(family,'native' if family=='M9' else 'guards',k,[h]*r,q,rows,
                {'shift':shift,'reversal':reverse,'target':target},h=h,N=n)

def m6(protocol):
    for h,q in product((2,3),(3,4)):
        n = math.comb(h+q-2,h)
        for r in (2*n-1,2*n):
            for shift,reverse in product(range(r),(0,1)):
                yield guard_case(h,q,r,shift,reverse)

def restricted_groups(r,q):
    def visit(word):
        if len(word)==r:
            if max(word)+1==q:
                yield word
            return
        for color in range(min(q,max(word)+2)):
            yield from visit(word+[color])
    yield from visit([0])

def m7(protocol):
    for q in (3,4):
        for r in (q,q+1,q+2):
            groups = list(restricted_groups(r,q))
            for a in product((1,2,3),repeat=r):
                total = sum(a)
                if total>10:
                    continue
                for colors in groups:
                    next_label,rows = q,[]
                    for i,width in enumerate(a):
                        rows.append([colors[i]]+list(range(next_label,next_label+width-1)))
                        next_label += width-1
                    for k in (total-1,total,total+1):
                        if next_label>k:
                            continue
                        yield case('M7','split_path',k,a,q,rows,{},groups=colors)
                        if k>=total:
                            for x in range(next_label):
                                owners = [i for i,row in enumerate(rows) if x in row]
                                if len(owners)>=2:
                                    for i,y in product(owners,range(next_label,k)):
                                        yield case('M7','split_local',k,a,q,rows,[x,i,y],groups=colors)

def m8(protocol):
    for rows in ([[0],[1],[2]],[[0,1],[1,2],[0,2],[3,4]]):
        a = list(map(len,rows))
        total = sum(a)
        active = sorted(set(x for row in rows for x in row))
        for x,length in product(active,(1,total+2,total+3)):
            yield case('M8','support',len(active)+total+1+length,a,3,rows,{'label':x,'length':length})

def m9(protocol):
    for h,q in product((2,3),(3,4)):
        yield guard_case(h,q,2*math.comb(h+q-2,h),1,1,'M9')

def generate_cases(protocol):
    with tempfile.TemporaryDirectory(prefix='v1654-producer-universe-') as tmp:
        db = sqlite3.connect(tmp+'/cases.sqlite')
        db.execute('CREATE TABLE cases(identity TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        for family in protocol['families']:
            for item in globals()[family.lower()](protocol):
                ident = json.dumps(item['identity'],sort_keys=True,separators=(',',':'))
                payload = json.dumps(item,sort_keys=True,separators=(',',':'))
                db.execute('INSERT INTO cases VALUES (?,?)',(ident,payload))
            db.commit()
        for payload, in db.execute('SELECT payload FROM cases ORDER BY identity COLLATE BINARY'):
            yield json.loads(payload)
        db.close()
