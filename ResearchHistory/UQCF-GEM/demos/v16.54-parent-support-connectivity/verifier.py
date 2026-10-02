"""Independent set-based universe reconstruction and certificate verification.

This module imports no producer model, enumerator, or mechanism implementation.
"""
from collections import defaultdict
from itertools import combinations, product, zip_longest
from pathlib import Path
import hashlib
import json
import math
import os
import sqlite3
import subprocess
import tempfile

PLAN_SHA = 'd4d13e0ebb6feb63c0f235ff5c06d7ab36cb9c497f07df988f306e1d683e1d63'
PARENT = 'f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8'

def serial(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))

def item(family, kind, k, a, q, rows, choice, **fields):
    p = {'kind':kind, 'k':k, 'a':list(a), 'q':q}
    p.update(fields)
    return {'identity':[family,p,[sorted(set(row)) for row in rows],choice]}

def covering_number(rows):
    constraints = [frozenset(row) for row in rows]
    if any(not row for row in constraints):
        return math.inf
    labels = sorted(set().union(*constraints)) if constraints else []
    for size in range(len(labels)+1):
        for chosen in combinations(labels,size):
            if all(set(chosen).intersection(row) for row in constraints):
                return size
    raise AssertionError('finite nonempty constraints must have a transversal')

def assignments(k, capacities):
    bins = [set() for _ in capacities]
    def put(label):
        if label == k:
            yield [sorted(row) for row in bins]
            return
        for slot,limit in enumerate(capacities):
            if len(bins[slot]) < limit:
                bins[slot].add(label)
                yield from put(label+1)
                bins[slot].remove(label)
    yield from put(0)

def independent_m1(protocol):
    for k in range(4,7):
        options = [[x,y] for x in range(k) for y in range(k) if x != y]
        for length in range(1,k+1):
            for final in combinations(range(k),length):
                rows = [{x} for x in range(k)]+[set(final)]
                for width in range(1,length+1):
                    a = [1]*k+[width]
                    for first in options:
                        yield item('M1','packet',k,a,k,rows,first)
                        for second in options:
                            yield item('M1','double_packet',k,a,k,rows,[first,second])
                    for label in range(k):
                        for slot in range(k+1):
                            if label in rows[slot]:
                                continue
                            neighbor = [set(row) for row in rows]
                            neighbor[slot].add(label)
                            peer_options = options if covering_number(neighbor)==k else [None]
                            for first in options:
                                for second in peer_options:
                                    for reverse in (True,False):
                                        yield item('M1','neighbor',k,a,k,rows,
                                                   {'edge':[slot,label],'left':first,
                                                    'right':second,'reverse':reverse})
                    yield item('M1','layers',k,a,3,rows,{'peak':k})

def independent_m2(protocol):
    by_width = defaultdict(list)
    columns = [set(c) for n in range(3) for c in combinations(range(3),n)]
    for incident in product(columns,repeat=4):
        rows = [{j for j in range(4) if i in incident[j]} for i in range(3)]
        widths = tuple(map(len,rows))
        if min(widths)>0 and sum(widths)<8:
            by_width[widths].append(rows)
    for widths, states in by_width.items():
        for old in states:
            for new in states:
                yield item('M2','degree2',4,widths,None,old,{'target':[sorted(s) for s in new]})
    for x in range(5):
        for y in range(5):
            for z in range(5):
                caps = [x,y,z]
                if x+y+z<5:
                    continue
                states = list(assignments(4,caps))
                for old in states:
                    for new in states:
                        yield item('M2','element',4,[0,0,0],None,old,{'target':new},
                                   capacities=caps,representation='blocks')
    yield item('M2','forced_cycle',5,[2,2,4],None,[{0,2},{1,3},{0,1,2,3}],
               {'target':[[1,3],[0,2],[0,1,2,3]],
                'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4})

def independent_m3(protocol):
    for q in range(3,5):
        for k in range(q,q+2):
            groups = defaultdict(list)
            for rows in assignments(k,[k]*q):
                if all(rows):
                    groups[tuple(map(len,rows))].append(rows)
            for widths, states in groups.items():
                for z in range(3):
                    hubs = [list(range(k)) for _ in range(z)]
                    for old in states:
                        for new in states:
                            yield item('M3','saturated',k,list(widths)+[k]*z,q,old+hubs,
                                       {'target':new+hubs},hubs=z)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                yield item('M3','classify',3,[1,1,1],3,[{x},{y},{z}],{})

def independent_m4(protocol):
    def decode(alphabet,words):
        return [sorted(alphabet.index(x) for x in word) for word in words.split()]
    old = decode('uvwabcdef','uvw uab vcd wef')
    new_family = decode('uvabcdefg','uva uvb uvc ude vfg abc')
    descriptions = [dict(tag='unsafe',rows=old,k=9,q=3,ops=[[0,1]],h=3,
                         doc='HYPEREDGE_CLONE_BOUNDARY.md'),
                    dict(tag='unsafe_twice',rows=old+[list(map(lambda x:x+9,e)) for e in old],
                         k=18,q=6,ops=[[0,1],[9,10]],h=3,doc='HYPEREDGE_CLONE_BOUNDARY.md')]
    for satellites in range(3):
        extra = [[9+3*j,10+3*j,11+3*j] for j in range(satellites)]
        descriptions.append(dict(tag='fan',rows=new_family+extra,k=9+3*satellites,
                                 q=3+satellites,ops=[[0,1]],h=3,doc='CONTRACTION_CLONE_GUARD.md'))
    descriptions.append(dict(tag='empty',rows=[[0,1],[0,2],[1,3],[4,5]],k=6,q=3,
                             ops=[[0,1]],h=2,doc='PROSPECTIVE_VALIDATION_PLAN.md'))
    for d in descriptions:
        count = len(d['rows'])
        for shift in range(count):
            rows = [None]*count
            for index,row in enumerate(d['rows']):
                rows[(index+shift)%count] = row
            digest = protocol['approved_plan_sha256'] if d['doc']=='PROSPECTIVE_VALIDATION_PLAN.md' else protocol['proofs'][d['doc']]
            yield item('M4','clone_sequence',d['k'],[d['h']]*count,d['q'],rows,
                       {'operations':d['ops'],'shift':shift},tag=d['tag'],source=d['doc'],source_sha256=digest)

def independent_core(sizes, h, cyclic):
    labels = [i for i,s in enumerate(sizes) for _ in range(s)]
    rows = []
    for support in combinations(range(sum(sizes)),h):
        counts = [sum(labels[x]==i for x in support) for i in range(len(sizes))]
        internal = max(counts)==h
        directed = cyclic and any(counts[i]==2 and counts[(i+1)%3]==1 for i in range(3))
        if internal or directed:
            rows.append(list(support))
    return rows

def independent_m5(protocol):
    descriptions = []
    for k in range(3,11):
        for h in (3,4):
            for count in range(1,4):
                for sizes in product(range(1,k+1),repeat=count):
                    if sum(sizes)==k and all(h<=s<=h+2 for s in sizes) and k-count*(h-1)>=3:
                        descriptions.append(('module',h,sizes))
    for sizes in product(range(1,9),repeat=3):
        if 6<=sum(sizes)<=9:
            descriptions.append(('cyclic',3,sizes))
    for form,h,sizes in descriptions:
        base = independent_core(sizes,h,form=='cyclic')
        k = sum(sizes)
        q = k-3 if form=='cyclic' else k-len(sizes)*(h-1)
        for extra_count in range(3):
            for method in (['P'] if extra_count==0 else ['duplicate','P']):
                rows = base+[(base[0] if method=='duplicate' else list(range(k)))
                             for _ in range(extra_count)]
                fields = dict(form=form,h=h,sizes=list(sizes),extras=method,d=extra_count)
                yield item('M5','balance',k,[h]*len(rows),q,rows,{},**fields)
                for source in range(len(sizes)):
                    for destination in range(len(sizes)):
                        allowed = (destination==(source+1)%3 and sizes[source]>sizes[destination]) if form=='cyclic' else sizes[source]-sizes[destination]>=2
                        if allowed:
                            yield item('M5','relocate',k,[h]*len(rows),q,rows,[source,destination],**fields)
    first = independent_core((3,5),3,False)
    last = independent_core((4,4),3,False)
    yield item('M5','module_pair',8,[3]*11,4,first,{'target':last+[last[0]]*3},h=3,sizes=[3,5],form='module')
    rows = independent_core((3,2,2),3,True)
    yield item('M5','obstruction',7,[3]*len(rows),4,rows,{},sizes=[3,2,2])

def independent_guards(h,q,r,shift,reverse,family):
    c = h+q-2
    edges = []
    for word in product((False,True),repeat=c):
        if sum(word)==h:
            edges.append([i for i,yes in enumerate(word) if yes])
    edges.sort()
    n,k = len(edges),c+h
    old = edges+[list(range(c,k))]+[list(range(k))]*(r-n-1)
    new = [[] for _ in range(r)]
    for source,row in enumerate(old):
        new[(source+shift)%r] = sorted([k-1-x if reverse else x for x in row])
    return item(family,'native' if family=='M9' else 'guards',k,[h]*r,q,old,
                {'shift':shift,'reversal':reverse,'target':new},h=h,N=n)

def independent_m6(protocol):
    for q in (3,4):
        for h in (2,3):
            bound = math.factorial(h+q-2)//(math.factorial(h)*math.factorial(q-2))
            for count in (2*bound,2*bound-1):
                for reverse in (1,0):
                    for shift in range(count):
                        yield independent_guards(h,q,count,shift,reverse,'M6')

def independent_m7(protocol):
    for q in (3,4):
        for r in range(q,q+3):
            partitions = []
            for word in product(range(q),repeat=r):
                encountered = list(dict.fromkeys(word))
                if encountered==list(range(q)):
                    partitions.append(list(word))
            for word in partitions:
                for widths in product(range(1,4),repeat=r):
                    total = sum(widths)
                    if total>10:
                        continue
                    rows = []
                    for row in range(r):
                        start = q+sum(w-1 for w in widths[:row])
                        rows.append([word[row]]+list(range(start,start+widths[row]-1)))
                    used = set().union(*(set(row) for row in rows))
                    for k in range(total-1,total+2):
                        if max(used)>=k:
                            continue
                        yield item('M7','split_path',k,widths,q,rows,{},groups=word)
                        if k<total:
                            continue
                        for slot,row in enumerate(rows):
                            for x in row:
                                if sum(x in other for other in rows)<2:
                                    continue
                                for new in sorted(set(range(k))-used):
                                    yield item('M7','split_local',k,widths,q,rows,[x,slot,new],groups=word)

def independent_m8(protocol):
    for encoded in ('0;1;2','0,1;1,2;0,2;3,4'):
        rows = [list(map(int,part.split(','))) for part in encoded.split(';')]
        widths = list(map(len,rows))
        total = sum(widths)
        used = set().union(*(set(e) for e in rows))
        for length in (1,total+2,total+3):
            for x in sorted(used):
                yield item('M8','support',len(used)+total+1+length,widths,3,rows,
                           {'label':x,'length':length})

def independent_m9(protocol):
    for h in (2,3):
        for q in (3,4):
            n = len(list(combinations(range(h+q-2),h)))
            yield independent_guards(h,q,2*n,1,1,'M9')

def reconstruct_cases(protocol):
    with tempfile.TemporaryDirectory(prefix='v1654-independent-universe-') as folder:
        connection = sqlite3.connect(str(Path(folder)/'expected.sqlite'))
        connection.execute('CREATE TABLE expected (key TEXT UNIQUE NOT NULL, body TEXT NOT NULL)')
        for family in protocol['families']:
            for expected in globals()['independent_'+family.lower()](protocol):
                connection.execute('INSERT INTO expected VALUES (?,?)',
                                   (serial(expected['identity']),serial(expected)))
            connection.commit()
        cursor = connection.execute('SELECT body FROM expected ORDER BY key COLLATE BINARY')
        for row in cursor:
            yield json.loads(row[0])
        connection.close()

def verify_universe(expected, records):
    errors = []
    previous_expected = previous_actual = None
    sentinel = object()
    for index,(want,got) in enumerate(zip_longest(expected,records,fillvalue=sentinel)):
        reason = None
        if want is sentinel or got is sentinel:
            reason = 'universe length/membership mismatch'
        else:
            left,right = serial(want['identity']),serial(got['identity'])
            if previous_expected is not None and left<=previous_expected:
                reason = 'independent universe duplicate/order violation'
            if previous_actual is not None and right<=previous_actual:
                reason = 'production universe duplicate/order violation'
            if serial(want)!=serial(got):
                reason = 'identity or reconstructed input mismatch'
            previous_expected,previous_actual = left,right
        if reason and len(errors)<20:
            errors.append(str(index)+': '+reason)
    return errors

def verify_protocol(protocol, directory):
    root = Path(directory)
    errors = []
    if protocol.get('approved_plan_sha256')!=PLAN_SHA:
        errors.append('unapproved plan digest')
    if hashlib.sha256((root/'PROSPECTIVE_VALIDATION_PLAN.md').read_bytes()).hexdigest()!=PLAN_SHA:
        errors.append('plan source bytes changed')
    if protocol.get('certified_parent')!=PARENT:
        errors.append('certified parent mismatch')
    for name,digest in {**protocol.get('proofs',{}),**protocol.get('reviews',{})}.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            errors.append('proof digest: '+name)
    freeze = os.environ.get('PREREGISTRATION_SHA')
    if freeze:
        relative = 'ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/protocol.json'
        frozen = json.loads(subprocess.check_output(['git','show',freeze+':'+relative],text=True))
        if protocol != frozen:
            errors.append('protocol differs from immutable preregistration')
    if protocol.get('families')!=['M'+str(i) for i in range(1,10)]:
        errors.append('family coverage changed')
    if protocol.get('resources')!={'minutes_per_job':60,'memory_bytes':4294967296,
                                   'vertices_per_identity':1000000,'max_parallel_shards':8}:
        errors.append('resource specification changed')
    return errors

def verify_record(case, record):
    return []
