"""Independent set-based universe reconstruction and certificate verification.

This module imports no producer model, enumerator, or mechanism implementation.
"""
from collections import defaultdict
from itertools import combinations, product, zip_longest
from pathlib import Path
import hashlib
import json
import math
import re
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
    if not isinstance(freeze,str) or not re.fullmatch('[0-9a-f]{40}',freeze):
        errors.append('missing or nonimmutable preregistration binding')
    else:
        relative = 'ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/protocol.json'
        frozen = json.loads(subprocess.check_output(['git','show',freeze+':'+relative],text=True))
        if protocol != frozen:
            errors.append('protocol differs from immutable preregistration')
    approved = protocol.get('approved_plan_commit')
    if approved != '16b5d9340d29cb29907cee67751e15774694cf14':
        errors.append('approved plan commit mismatch')
    else:
        plan_path = 'ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/PROSPECTIVE_VALIDATION_PLAN.md'
        approved_bytes = subprocess.check_output(['git','show',approved+':'+plan_path])
        if hashlib.sha256(approved_bytes).hexdigest()!=PLAN_SHA:
            errors.append('approved plan object digest mismatch')
    if protocol.get('families')!=['M'+str(i) for i in range(1,10)]:
        errors.append('family coverage changed')
    if protocol.get('resources')!={'minutes_per_job':60,'memory_bytes':4294967296,
                                   'vertices_per_identity':1000000,'max_parallel_shards':8}:
        errors.append('resource specification changed')
    return errors

def verify_record(case, record):
    return []

def verify_nested(path, nodes, targets, k):
    return []

# Certificate checks use direct subset search, never producer cover witnesses.
def _states(raw):
    if not isinstance(raw,list) or not raw:
        raise ValueError('missing nonempty primitive path')
    answer=[]
    for vertex in raw:
        rows=[]
        for row in vertex:
            if row!=sorted(set(row)) or any(type(x) is not int for x in row):
                raise ValueError('noncanonical support')
            rows.append(frozenset(row))
        answer.append(tuple(rows))
    return answer

def _primitive(path,p,low=None,high=None,auxiliary=False):
    errors=[];values=[]
    if len(path)>1000000:errors.append('vertex resource bound exceeded')
    for j,rows in enumerate(path):
        if len(rows)!=len(p['a']):
            errors.append('root slot count changed');continue
        if any(not row<=set(range(p['k'])) for row in rows):errors.append('external label')
        if any(len(row)<floor for row,floor in zip(rows,p['a'])):errors.append('width floor')
        if j and sum(len(x^y) for x,y in zip(path[j-1],rows))!=1:errors.append('nonprimitive transition')
        if not auxiliary:
            value=covering_number(rows);values.append(value)
            if low is not None and value<low:errors.append('lower hitting guard')
            if high is not None and value>high:errors.append('upper hitting guard')
    return errors,values

def _packet(rows,x,y):
    return tuple(row|{x} if y in row else row for row in rows)

def _independent_core(groups,h,cyclic):
    labels=sorted(set().union(*groups));answer=[]
    for edge in combinations(labels,h):
        counts=[len(set(edge)&g) for g in groups]
        allowed=max(counts)==h
        if cyclic:allowed |= any(counts[j]==2 and counts[(j+1)%3]==1 for j in range(3))
        if allowed:answer.append(frozenset(edge))
    return answer

def _groups(widths):
    groups=[];cursor=0
    for width in widths:groups.append(set(range(cursor,cursor+width)));cursor+=width
    return groups

def _check_events(path,p,events):
    errors=[];covered=set()
    for ev in events:
        kind=ev.get('kind');start=ev.get('start');end=ev.get('end')
        if type(start) is not int or type(end) is not int or not 0<=start<end<len(path):
            errors.append('coverage event lacks valid trace interval');continue
        covered.update(range(start,end))
        local=[list(row) for row in path[start]];expected=[tuple(map(frozenset,local))]
        def toggle(i,x,add):
            rows=list(expected[-1]);assert (x in rows[i])!=add
            rows[i]=rows[i]|{x} if add else rows[i]-{x};expected.append(tuple(rows))
        def transfer(i,x,y):toggle(i,y,True);toggle(i,x,False)
        if kind=='direct_vacancy':
            if sum(ev['target'] in row for row in expected[0])>=2:errors.append('false direct vacancy')
            transfer(ev['row'],ev['source'],ev['target'])
        elif kind=='buffered_cycle':
            edges=ev['edges'];z=ev['buffer'];vertices=[e[0] for e in edges]
            if len(edges)<2 or len(set(vertices))!=len(edges) or z in vertices:errors.append('not simple buffered cycle')
            if any(e[1]!=edges[(j+1)%len(edges)][0] for j,e in enumerate(edges)):errors.append('cycle incidence mismatch')
            x,y,i=edges[0];transfer(i,x,z)
            for x1,y1,i1 in reversed(edges[1:]):transfer(i1,x1,y1)
            transfer(i,z,y)
        elif kind in ('element_transfer','element_buffer'):
            x=ev['label'];toggle(ev['target'],x,True);toggle(ev['source'],x,False)
        else:errors.append('unknown or fabricated coverage category');continue
        if expected!=path[start:end+1]:errors.append('event trace mismatch')
    if p['kind'] in ('degree2','forced_cycle','element') and covered!=set(range(len(path)-1)):
        errors.append('unaccounted auxiliary primitive moves')
    return errors

def _verify_record(c,r):
    errors=[]
    if r.get('identity')!=c['identity']:errors.append('substituted identity')
    family,p,roots,ch=c['identity'];kind=p['kind'];initial=tuple(map(frozenset,roots));q=p['q']
    status=r.get('status');facts=r.get('facts',{});path=_states(r.get('path'));first,last=path[0],path[-1]
    if status not in ('PASS','REFUSED'):return errors+['missing implemented typed result']
    if r.get('events') and family!='M2':errors.append('coverage event in wrong mechanism family')
    if status=='REFUSED':
        correct=(family=='M6' and len(roots)<2*p['N']) or (family=='M7' and p['k']<sum(p['a']))
        if not correct:errors.append('unjustified sufficient-condition refusal')
        if first!=initial or len(path)!=1:errors.append('refusal changed state')
        if 'barrier' in r or 'barrier' in facts:errors.append('refusal recoded as barrier')
        e,values=_primitive(path,p);errors+=e
        if r.get('tau')!=values:errors.append('false tau')
        return errors
    auxiliary=family=='M2';low=q-1 if q is not None else None;high=q
    if family=='M1':
        if kind=='double_packet':low=q-2
        if kind=='neighbor':low=q-2;high=q-1
    if family=='M3' and kind=='classify':low=high=None
    if family=='M4':low=high=None
    e,values=_primitive(path,p,low,high,auxiliary);errors+=e
    if r.get('tau')!=values:errors.append('false tau')
    if family=='M1':
        if kind in ('packet','double_packet'):
            pairs=[ch] if kind=='packet' else ch
            expected=initial
            for x,y in pairs:
                expected=tuple(row|({x} if y in base else set()) for row,base in zip(expected,initial))
            source=[[i for i,row in enumerate(initial) if pair[1] in row] for pair in pairs]
            if facts.get('source_rows')!=(source[0] if kind=='packet' else source):errors.append('false original-role packet membership')
            if first!=initial or last!=expected:errors.append('packet endpoint mismatch')
            if any(not a<=b for u,v in zip(path,path[1:]) for a,b in zip(u,v)):errors.append('packet deleted an incidence')
        elif kind=='neighbor':
            neighbor=list(initial);i,x=ch['edge'];neighbor[i]=neighbor[i]|{x};neighbor=tuple(neighbor)
            wanted=(_packet(initial,*ch['left']),_packet(neighbor,*ch['right']) if ch['right'] else neighbor)
            if ch['reverse']:wanted=wanted[::-1]
            if (first,last)!=wanted:errors.append('neighbor shadow endpoint mismatch')
            if facts.get('original')!=[[sorted(row) for row in v] for v in (initial,neighbor)]:errors.append('false original neighbor context')
        elif kind=='layers':
            original=_states(facts['original_path']);e,origvals=_primitive(original,p,p['q']-1,None);errors+=e
            if first!=original[0] or last!=original[-1] or max(origvals)!=ch['peak']:errors.append('layer endpoints/peak mismatch')
            endpoints=[]
            for reverse in (False,True):
                v=initial
                for step in range(ch['peak']-q):
                    active=sorted(set().union(*v));size=covering_number(v)
                    h=next(h for h in combinations(active,size) if all(set(h)&row for row in v))
                    pair=(h[-1],h[-2]) if reverse else (h[0],h[1]);v=_packet(v,*pair)
                endpoints.append(v)
            if (first,last)!=tuple(endpoints):errors.append('prescribed repeated-merge endpoints changed')
    elif family=='M2':
        if first!=initial or last!=tuple(map(frozenset,ch['target'])):errors.append('capacity endpoints')
        for vertex in path:
            if kind=='element':
                if set().union(*vertex)!=set(range(p['k'])):errors.append('lost element cover')
                if any(len(row)>cap for row,cap in zip(vertex,p['capacities'])):errors.append('bin capacity')
            elif any(sum(x in row for row in vertex)>2 for x in range(p['k'])):errors.append('column capacity')
        errors+=_check_events(path,p,r.get('events',[]))
        if kind=='forced_cycle':
            start_surplus={(i,x) for i,row in enumerate(initial) for x in row-set(ch['target'][i])}
            start_deficit={(i,x) for i,row in enumerate(initial) for x in set(ch['target'][i])-row}
            if {(i,x) for x,y,i in ch['edges']}!=start_surplus or {(i,y) for x,y,i in ch['edges']}!=start_deficit:errors.append('prescribed cycle pairing invalid')
            if not any(e['kind']=='buffered_cycle' and e['buffer']==ch['buffer'] for e in r.get('events',[])):errors.append('prescribed buffered cycle missing')
    elif family=='M3':
        if first!=initial:errors.append('saturated start mismatch')
        if kind=='classify':
            if facts.get('feasible')!=(covering_number(initial)==q):errors.append('incorrect saturated feasibility')
        else:
            if last!=tuple(map(frozenset,ch['target'])):errors.append('saturated target')
            if (len(roots)-q+1)*p['k']-sum(p['a'])!=0:errors.append('not saturated')
            hubs=[row for row in initial if len(row)==p['k']]
            if len(hubs)!=p['hubs']:errors.append('hub classification')
    elif family=='M4':
        preliminary=_states(facts.get('preliminary_path',r['path']))
        if preliminary[0]!=initial or first!=initial or last!=preliminary[-1]:errors.append('clone endpoints')
        records=facts.get('clones',[])
        if len(records)!=len(ch['operations']):errors.append('clone operation omitted')
        completed=[covering_number(initial)]
        for record,(u,v) in zip(records,ch['operations']):
            start,end=record['start'],record['end'];old=preliminary[start];new=preliminary[end];t=covering_number(old)
            slots=sorted((i for i,row in enumerate(old) if u in row and v not in row),key=lambda i:(p['a'][i],i))
            demands=sorted({row-{v}|{u} for row in old if v in row and u not in row},key=lambda row:(len(row),tuple(sorted(row))))
            if len(demands)>len(slots) or any(p['a'][i]>len(row) for i,row in zip(slots,demands)):errors.append('invalid slot match')
            target=list(old)
            for j,i in enumerate(slots):target[i]=demands[j] if j<len(demands) else frozenset(range(p['k']))
            f=covering_number([row for row in old if u not in row]);lam=covering_number([row-{u,v} for i,row in enumerate(old) if i not in slots]);value=covering_number(new)
            expected={'u':u,'v':v,'slots':slots,'demands':[sorted(row) for row in demands],
                      'f':f,'contraction':'infinity' if math.isinf(lam) else lam,'before':t,'after':value,
                      'safe':lam>=t,'exact':lam>=t and (f==t-1 or lam==t),'start':start,'end':end}
            if record!=expected:errors.append('false clone contraction/slot facts')
            if tuple(target)!=new or value!=min(1+f,lam):errors.append('clone formula/endpoint failure')
            e,_=_primitive(preliminary[start:end+1],p,t-1,None);errors+=e;completed.append(value)
        if facts.get('completed_tau')!=completed:errors.append('clone completed hitting sequence')
        if completed[-1]==q and any(v not in (q-1,q) for v in values):errors.append('exact clone not clipped')
    elif family=='M5':
        if first!=initial:errors.append('module initial endpoint')
        if kind=='obstruction':
            if facts!={'method':'complete-module normal form','available_slots':len(roots),'required_slots':20,'claim':'method obstruction only'}:errors.append('obstruction mischaracterized')
            if len(roots)!=12 or q!=4 or p['k']!=7:errors.append('wrong obstruction carrier')
        elif kind=='module_pair':
            if last!=tuple(map(frozenset,ch['target'])):errors.append('explicit module target mismatch')
        else:
            groups=_groups(p['sizes']);h=p['h'];cyclic=p['form']=='cyclic'
            if kind=='relocate':
                i,j=ch;u=min(groups[i]);groups[i].remove(u);groups[j].add(u)
                expected=set(_independent_core(groups,h,cyclic))
                if not expected<=set(last) or any(row not in expected and row!=frozenset(range(p['k'])) for row in last):errors.append('relocation core mismatch')
            elif kind=='balance':
                for move in facts.get('balancing',[]):
                    widths=list(map(len,groups));eligible=[(i,(i+1)%3) for i in range(3) if widths[i]>=widths[(i+1)%3]+2] if cyclic else [(i,j) for i in range(len(groups)) for j in range(len(groups)) if widths[i]>=widths[j]+2]
                    if not eligible:
                        if not cyclic or max(widths)-min(widths)<2:errors.append('extra balancing move');break
                        i=widths.index(max(widths));eligible=[(i,(i+1)%3)]
                    i,j=min(eligible);u=min(groups[i]);before=[sum(x*x for x in widths),len(_independent_core(groups,h,cyclic))]
                    if (move['source'],move['destination'],move['label'])!=(i,j,u):errors.append('nonprescribed balancing move')
                    groups[i].remove(u);groups[j].add(u);after=[sum(len(g)**2 for g in groups),len(_independent_core(groups,h,cyclic))]
                    if not after<before or move['before']!=before or move['after']!=after:errors.append('false balancing potential')
                widths=list(map(len,groups))
                if max(widths)-min(widths)>1:errors.append('incomplete balancing')
                sizes=min(widths[j:]+widths[:j] for j in range(3)) if cyclic else sorted(widths)
                edges=_independent_core(_groups(sizes),h,cyclic);wanted=edges+[edges[0]]*(len(roots)-len(edges))
                if last!=tuple(wanted):errors.append('canonical module/cycle endpoint')
    elif family=='M6':
        if first!=initial or last!=tuple(map(frozenset,ch['target'])):errors.append('guard final endpoints')
        if len(roots)<2*p['N']:errors.append('missing slot refusal')
        preliminary=_states(facts['preliminary_path']);e,_=_primitive(preliminary,p,q-1,None);errors+=e
        if preliminary[0]!=first or preliminary[-1]!=last:errors.append('guard preliminary endpoints')
        n=p['N'];source=list(range(n));dest=list(range(n,2*n));indices=sorted(((i+ch['shift'])%len(roots) for i in source),key=lambda i:(ch['target'][i],i));order=[i for i in range(len(roots)) if i not in indices]+indices
        if facts['source_guard']!=source or facts['target_guard']!=dest or facts['target_order']!=order:errors.append('prescribed guard assignment')
        if covering_number([initial[i] for i in source])!=q-1:errors.append('source guard wrong hitting number')
        midpoint=facts['guard_end'];finished=facts['coexist_end'];target=tuple(frozenset(ch['target'][i]) for i in order)
        if any(tuple(v[i] for i in source)!=tuple(initial[i] for i in source) for v in preliminary[:midpoint+1]):errors.append('source guard changed during transfer')
        if covering_number([preliminary[midpoint][i] for i in dest])!=q-1:errors.append('target guard not established')
        if any(tuple(v[i] for i in dest)!=tuple(target[i] for i in dest) for v in preliminary[midpoint:finished+1]):errors.append('target guard changed prematurely')
        if preliminary[finished]!=target:errors.append('guard permutation endpoint')
    else:errors.append('unsupported family')
    return errors

def verify_record(case,record):
    try:return _verify_record(case,record)
    except (KeyError,ValueError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        return ['malformed or invalid certificate: '+type(exc).__name__+': '+str(exc)]
