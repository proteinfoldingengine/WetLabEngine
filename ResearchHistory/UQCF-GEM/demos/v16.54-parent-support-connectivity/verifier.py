"""Independent set-based universe reconstruction and certificate verification.

This module imports no producer model, enumerator, or mechanism implementation.
"""
from collections import defaultdict
from functools import lru_cache
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
    return _direct_cover(tuple(frozenset(row) for row in rows))

@lru_cache(maxsize=10000)
def _direct_cover(constraints):
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
    if family=='M7' and kind=='split_local':low=q;high=q+1
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
                edges=_independent_core(_groups(sizes),h,cyclic);wanted=sorted(edges+[edges[0]]*(len(roots)-len(edges)),key=lambda row:tuple(sorted(row)))
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
    elif family in ('M7','M8','M9'):
        errors+=_verify_extensions(c,r,path)
    else:errors.append('unsupported family')
    return errors

def verify_record(case,record):
    try:return _verify_record(case,record)
    except (KeyError,ValueError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        return ['malformed or invalid certificate: '+type(exc).__name__+': '+str(exc)]

def _toggle_state(rows,i,x,add):
    answer=list(rows)
    if (x in answer[i])==add:raise ValueError('redundant prescribed move')
    answer[i]=answer[i]|{x} if add else answer[i]-{x}
    return tuple(answer)

def _verify_extensions(c,r,path):
    family,p,roots,ch=c['identity'];initial=tuple(map(frozenset,roots));facts=r['facts'];q=p['q'];errors=[]
    if path[0]!=initial:errors.append('extension initial endpoint')
    if family=='M7':
        if p['k']<sum(p['a']):errors.append('palette API must refuse')
        active=[sorted(set().union(*v)) for v in path]
        if facts.get('active_labels')!=active:errors.append('false active-label history')
        if p['kind']=='split_local':
            x,i,y=ch
            if sum(x in row for row in initial)<2 or y in set().union(*initial):errors.append('invalid first split')
            middle=_toggle_state(initial,i,y,True);end=_toggle_state(middle,i,x,False)
            if path!=[initial,middle,end]:errors.append('first split trace')
            return errors
        target=tuple(frozenset(p['k']-1-x for x in row) for row in roots)
        if path[-1]!=target:errors.append('palette endpoint labels changed')
        left=_states(facts['left_path']);right=_states(facts['right_path']);preliminary=_states(facts['preliminary_path'])
        if left[0]!=initial or right[0]!=target or left[-1]!=right[-1]:errors.append('canonical splitting endpoints')
        if preliminary!=left+list(reversed(right))[1:]:errors.append('split route concatenation')
        e,_=_primitive(preliminary,p,q-1,None);errors+=e
        expected_canonical=tuple(map(frozenset,_groups(p['a'])))
        if left[-1]!=expected_canonical:errors.append('splitting canonical intervals')
        for leg,records in ((left,facts['left_splits']),(right,facts['right_splits'])):
            cursor=0
            for ev in records:
                vertex=leg[cursor];used=set().union(*vertex)
                candidates=[(x,i,y) for x in sorted(used) if sum(x in row for row in vertex)>1 for i,row in enumerate(vertex) if x in row for y in range(p['k']) if y not in used]
                if not candidates:errors.append('unnecessary split');break
                x,i,y=min(candidates)
                middle=_toggle_state(vertex,i,y,True);end=_toggle_state(middle,i,x,False)
                if ev!={'choice':[x,i,y],'start':cursor,'end':cursor+2} or leg[cursor:cursor+3]!=[vertex,middle,end]:errors.append('prescribed splitting trace')
                cursor+=2
            if sum(map(len,leg[cursor]))!=len(set().union(*leg[cursor])):errors.append('incomplete role splitting')
    elif family=='M8':
        if path[-1]!=initial:errors.append('support reduction endpoint identity')
        original=_states(facts['original_path']);compact=_states(facts['compact_path']);mapped=_states(facts['mapped_path'])
        expected=[initial];x=ch['label'];used=set().union(*initial)
        for y in range(len(used),len(used)+ch['length']):
            owners=[i for i,row in enumerate(expected[-1]) if x in row]
            for i in owners:expected.append(_toggle_state(expected[-1],i,y,True))
            for i in owners:expected.append(_toggle_state(expected[-1],i,x,False))
            x=y
        expected+=list(reversed(expected))[1:]
        if original!=expected:errors.append('prescribed original rename loop')
        projected=[initial];selected=[];boundaries=[]
        for vertex in original:
            small=tuple(frozenset(sorted(row)[:floor]) for row,floor in zip(vertex,p['a']));selected.append([sorted(row) for row in small])
            for i,row in enumerate(small):
                for x,y in zip(sorted(projected[-1][i]-row),sorted(row-projected[-1][i])):
                    projected.append(_toggle_state(projected[-1],i,y,True));projected.append(_toggle_state(projected[-1],i,x,False))
            boundaries.append(len(projected)-1)
        if compact!=projected or facts['selections']!=selected or facts['projection_boundaries']!=boundaries:errors.append('compact projection trace')
        reserve=[x for x in range(p['k']) if x not in used][:sum(p['a'])+1]
        if facts['reserve']!=reserve or len(mapped)!=len(compact) or len(facts['assignments'])!=len(compact):errors.append('reserve dimensions')
        images={}
        for v,w,pairs in zip(compact,mapped,facts['assignments']):
            active=set().union(*v)
            for x in sorted(active-used):
                if x not in images:images[x]=min(set(reserve)-set(images.values()))
            images={x:y for x,y in images.items() if x in active}
            if pairs!=[[x,y] for x,y in sorted(images.items())]:errors.append('reserve assignment/release mismatch')
            expected=tuple(frozenset(x if x in used else images[x] for x in row) for row in v)
            if w!=expected or len(set(images.values()))!=len(images):errors.append('noninjective support simulation')
            if covering_number(v)!=covering_number(w):errors.append('simulation changed hitting number')
        for trace in (original,compact,mapped):
            e,_=_primitive(trace,p,q-1,None);errors+=e
        if mapped[0]!=initial or mapped[-1]!=initial:errors.append('mapped endpoint identity')
        allowed=used|set(reserve)
        if any(not row<=allowed for vertex in path for row in vertex):errors.append('final path exceeds finite reserve')
    elif family=='M9':
        parentcase={'identity':['M6',dict(p,kind='guards'),roots,ch]}
        parent=facts['parent_record'];errors+=verify_record(parentcase,parent)
        if r['path']!=parent['path']:errors.append('native parent differs from M6 final path')
        nodes=[[]];targets={0:q};initial_nested=[frozenset(range(p['k']))]
        for row in initial:
            child=len(nodes);nodes[0].append(child);nodes.append([]);initial_nested.append(row);targets[child]=p['h']
            for x in sorted(row)[:p['h']]:nodes[child].append(len(nodes));nodes.append([]);initial_nested.append(frozenset([x]))
        if r['nodes']!=nodes or r['targets']!={str(v):t for v,t in targets.items()}:errors.append('native fixture substitution')
        nested=_states(r['nested_path']);errors+=verify_nested(r['nested_path'],nodes,targets,p['k'])
        if nested[0]!=tuple(initial_nested):errors.append('native initial leaves')
        boundaries=facts['parent_boundaries']
        if len(boundaries)!=len(path) or boundaries[0]!=0 or boundaries[-1]!=len(nested)-1:errors.append('native parent boundaries')
        for i,bound in enumerate(boundaries):
            if tuple(nested[bound][v] for v in nodes[0])!=path[i]:errors.append('native parent projection')
        # Independently check exact internal children at every lifted state.
        for vertex in nested:
            if any(covering_number([vertex[w] for w in nodes[v]])!=t for v,t in targets.items() if v):errors.append('child deviation during parent repair')
        parent='f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8';base='ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/'
        hashes={name:hashlib.sha256(subprocess.check_output(['git','show',parent+':'+base+name])).hexdigest() for name in ('producer.py','feasibility.py')}
        if facts['inherited_parent']!=parent or facts['inherited_sha256']!=hashes:errors.append('inherited clearance binding')
    return errors

def verify_nested(raw,nodes,targets,k):
    try:
        path=_states(raw);errors=[];targets={int(v):q for v,q in targets.items()}
        if len(path)>1000000:errors.append('native vertex resource bound')
        parent={child:v for v,children in enumerate(nodes) for child in children}
        if set(parent)!=set(range(1,len(nodes))) or sum(map(len,nodes))!=len(nodes)-1:return ['invalid native tree']
        if set(targets)!={i for i,children in enumerate(nodes) if children}:return ['native target inventory']
        for step,vertex in enumerate(path):
            if len(vertex)!=len(nodes):return ['native vertex dimensions']
            if vertex[0]!=frozenset(range(k)):errors.append('native fixed root changed')
            if any(not row or not row<=set(range(k)) for row in vertex):errors.append('native nonempty palette')
            if any(not vertex[v]<=vertex[parent[v]] for v in parent):errors.append('native nesting')
            total=sum(abs(covering_number([vertex[c] for c in nodes[v]])-q) for v,q in targets.items())
            if total>1:errors.append('global native deviation exceeds one')
            if step:
                changed=[i for i,(a,b) in enumerate(zip(path[step-1],vertex)) if a!=b]
                if len(changed)!=1 or changed[0]==0 or len(path[step-1][changed[0]]^vertex[changed[0]])!=1:errors.append('native primitive violation')
        return errors
    except (ValueError,TypeError,KeyError,IndexError) as exc:return ['malformed native certificate: '+str(exc)]

# Independent reconstruction of each maximum-layer transformation.
def _bridge(a,b):
    trace=[a]
    for i,row in enumerate(b):
        for x in sorted(row-trace[-1][i]):trace.append(_toggle_state(trace[-1],i,x,True))
    for i,row in enumerate(b):
        for x in sorted(trace[-1][i]-row):trace.append(_toggle_state(trace[-1],i,x,False))
    return trace

@lru_cache(maxsize=10000)
def _least_cover(rows):
    active=sorted(set().union(*rows))
    for size in range(len(active)+1):
        for selected in combinations(active,size):
            if all(set(selected)&row for row in rows):return selected
    raise ValueError('unhittable native roots')

def _layer_check(original,final,q,metadata,p):
    errors=[];current=original;computed=[]
    while max(map(covering_number,current))>q:
        peak=max(map(covering_number,current))
        if covering_number(current[0])>=peak or covering_number(current[-1])>=peak:return ['nonfixed maximum-layer endpoints']
        replacements=[_packet(v,*_least_cover(v)[:2]) if covering_number(v)==peak else v for v in current]
        converted=[replacements[0]]
        for target in replacements[1:]:converted.extend(_bridge(converted[-1],target)[1:])
        e,values=_primitive(converted,p,q-1,peak-1);errors+=e
        computed.append({'peak':peak,'before':len(current),'after':len(converted)})
        if len(converted)>1000000:return errors+['layer vertex resource bound']
        current=converted
    if metadata!=computed:errors.append('false or omitted maximum-layer records')
    if current!=final:errors.append('final path differs from prescribed layer replacement')
    return errors

def _full_trace_contract(c,r):
    family,p,roots,ch=c['identity'];facts=r['facts'];path=_states(r['path']);errors=[]
    if r['status']=='REFUSED':return errors
    if family=='M1' and p['kind']=='layers':
        legs=[];initial=tuple(map(frozenset,roots))
        for reverse in (False,True):
            leg=[initial]
            for step in range(ch['peak']-p['q']):
                h=_least_cover(leg[-1]);x,y=(h[-1],h[-2]) if reverse else h[:2];original=leg[-1]
                for i,row in enumerate(original):
                    if y in row and x not in leg[-1][i]:leg.append(_toggle_state(leg[-1],i,x,True))
            legs.append(leg)
        original=list(reversed(legs[0]))+legs[1][1:]
        if _states(facts['original_path'])!=original:errors.append('prescribed M1 merge legs changed')
        errors+=_layer_check(original,path,p['q'],facts.get('layers'),p)
    elif family=='M4':
        original=_states(facts.get('preliminary_path',r['path']));cursor=0
        e,_=_primitive(original,p);errors+=e
        for record in facts['clones']:
            if record['start']!=cursor:errors.append('uncovered clone trace interval')
            expected=[original[cursor]]
            for j,i in enumerate(record['slots']):
                target=list(expected[-1]);target[i]=frozenset(record['demands'][j]) if j<len(record['demands']) else frozenset(range(p['k']))
                expected.extend(_bridge(expected[-1],tuple(target))[1:])
            end=cursor+len(expected)-1
            if record['end']!=end or original[cursor:end+1]!=expected:errors.append('clone slot-by-slot trace changed')
            cursor=end
        if cursor!=len(original)-1:errors.append('unchecked clone trace tail')
        if facts['completed_tau'][-1]==p['q']:errors+=_layer_check(original,path,p['q'],facts.get('layers'),p)
        elif original!=path:errors.append('unsafe diagnostic path replaced')
    elif family=='M6':errors+=_layer_check(_states(facts['preliminary_path']),path,p['q'],facts.get('layers'),p)
    elif family=='M7' and p['kind']=='split_path':errors+=_layer_check(_states(facts['preliminary_path']),path,p['q'],facts.get('layers'),p)
    elif family=='M8':errors+=_layer_check(_states(facts['mapped_path']),path,p['q'],facts.get('layers'),p)
    if family=='M2':errors+=_event_semantics(c,r,path)
    if family=='M6':errors+=_guard_phase_check(c,r)
    if family in ('M7','M9'):errors+=_extension_trace_check(c,r)
    if family=='M5' and p['kind']!='obstruction':errors+=_star_semantics(c,r,path)
    return errors

_basic_verify_record=verify_record

def verify_record(case,record):
    errors=_basic_verify_record(case,record)
    if errors:return errors
    try:return _full_trace_contract(case,record)
    except (KeyError,ValueError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        return ['malformed transformation certificate: '+type(exc).__name__+': '+str(exc)]

def _event_semantics(c,r,path):
    _,p,roots,ch=c['identity'];errors=[];cursor=0;target=tuple(map(frozenset,ch['target']));waiting=None
    pending=[tuple(edge) for edge in ch['edges']] if p['kind']=='forced_cycle' else [(x,y,i) for i,row in enumerate(path[0]) for x,y in zip(sorted(row-target[i]),sorted(target[i]-row))]
    for ev in r['events']:
        if ev['start']!=cursor:errors.append('overlapping or nonconsecutive event intervals')
        vertex=path[cursor];kind=ev['kind']
        if p['kind']=='element':
            desired={x:i for i,row in enumerate(target) for x in row}
            x=min(x for i,row in enumerate(vertex) for x in row if desired[x]!=i) if waiting is None else waiting
            old=next(i for i,row in enumerate(vertex) if x in row);dest=desired[x]
            if kind=='element_buffer':
                if waiting is not None or len(vertex[dest])!=p['capacities'][dest]:errors.append('false element buffer precondition')
                y=min(y for y in vertex[dest] if desired[y]!=dest);spare=next(i for i,row in enumerate(vertex) if len(row)<p['capacities'][i])
                if (ev['label'],ev['source'],ev['target'],ev['old_owner'])!=(y,dest,spare,old):errors.append('false element buffer/old-owner facts')
                waiting=x
            elif kind=='element_transfer':
                if (ev['label'],ev['source'],ev['target'])!=(x,old,dest):errors.append('nonprescribed element placement')
                waiting=None
            else:errors.append('wrong element event type')
        else:
            free=sorted(e for e in pending if sum(e[1] in row for row in vertex)<2)
            if kind=='direct_vacancy':
                edge=(ev['source'],ev['target'],ev['row'])
                if not free or edge!=free[0]:errors.append('nonprescribed direct vacancy order')
                if edge not in pending:errors.append('nonpending transfer')
                else:pending.remove(edge)
            elif kind=='buffered_cycle':
                edges=list(map(tuple,ev['edges']));z=ev['buffer']
                if free:errors.append('cycle used before available direct transfer')
                if p['kind']=='forced_cycle' and (set(edges)!=set(map(tuple,ch['edges'])) or len(edges)!=len(ch['edges'])):errors.append('substituted prescribed cycle pairing')
                walk=[];seen={};at=min(e[0] for e in pending)
                while at not in seen:
                    seen[at]=len(walk);edge=min(e for e in pending if e[0]==at);walk.append(edge);at=edge[1]
                chosen=walk[seen[at]:]
                rotation=next(j for j,e in enumerate(chosen) if z not in vertex[e[2]])
                chosen=chosen[rotation:]+chosen[:rotation]
                if edges!=chosen:errors.append('nonprescribed cycle selection or rotation')
                spare=ch['buffer'] if p['kind']=='forced_cycle' else next(x for x in range(p['k']) if sum(x in row for row in vertex)<2)
                if z!=spare or any(e[1]==z for e in pending):errors.append('invalid cycle spare column')
                for edge in edges:
                    if edge not in pending:errors.append('nonpending cycle edge')
                    else:pending.remove(edge)
            else:errors.append('wrong incidence event type')
        cursor=ev['end']
    if cursor!=len(path)-1 or waiting is not None:errors.append('unfinished event schedule')
    if p['kind']!='element' and pending:errors.append('unconsumed pending transfers')
    return errors


def _permutation_trace(initial,mapping):
    labels=sorted(set(mapping)|set(mapping.values()));permutation=dict(mapping)
    for x,y in zip(sorted(set(labels)-set(mapping)),sorted(set(labels)-set(mapping.values()))):permutation[x]=y
    trace=[initial];images={x:x for x in labels}
    for original in labels:
        if images[original]!=permutation[original]:
            a,b=images[original],permutation[original]
            changed=tuple(frozenset(b if x==a else a if x==b else x for x in row) for row in trace[-1])
            trace.extend(_bridge(trace[-1],changed)[1:])
            images={x:b if y==a else a if y==b else y for x,y in images.items()}
    return trace

def _root_order_trace(initial,target):
    trace=[initial]
    for i,row in enumerate(target):
        if trace[-1][i]!=row:
            j=next(j for j in range(i+1,len(target)) if trace[-1][j]==row)
            changed=list(trace[-1]);changed[i],changed[j]=changed[j],changed[i]
            trace.extend(_bridge(trace[-1],tuple(changed))[1:])
    return trace

def _star_semantics(c,r,path):
    _,p,roots,ch=c['identity'];facts=r['facts'];errors=[]
    def check_leg(leg,parameters,records,local=False):
        h=parameters['h'];cyclic=parameters['form']=='cyclic';groups=_groups(parameters['sizes'])
        expected=[leg[0]];edges=_independent_core(groups,h,cyclic);reps={next(i for i,row in enumerate(leg[0]) if row==edge) for edge in edges}
        for i in range(len(roots)):
            if i not in reps:
                target=list(expected[-1]);target[i]=frozenset(range(p['k']));expected.extend(_bridge(expected[-1],tuple(target))[1:])
        computed=[]
        while local and not computed or not local and max(map(len,groups))-min(map(len,groups))>=2:
            widths=list(map(len,groups))
            if local:i,j=ch
            else:
                choices=[(i,(i+1)%3) for i in range(3) if widths[i]>=widths[(i+1)%3]+2] if cyclic else [(i,j) for i in range(len(groups)) for j in range(len(groups)) if widths[i]>=widths[j]+2]
                if not choices:
                    i=widths.index(max(widths));choices=[(i,(i+1)%3)]
                i,j=min(choices)
            u=min(groups[i]);oldcore=_independent_core(groups,h,cyclic)
            slots=sorted(next(z for z,row in enumerate(expected[-1]) if row==edge) for edge in oldcore if u in edge)
            before=[sum(x*x for x in widths),len(oldcore)];groups[i].remove(u);groups[j].add(u)
            desired=[row for row in _independent_core(groups,h,cyclic) if u in row]
            if len(desired)>len(slots):return ['star slot shortage']
            start=len(expected)-1
            for n,z in enumerate(slots):
                target=list(expected[-1]);target[z]=desired[n] if n<len(desired) else frozenset(range(p['k']));expected.extend(_bridge(expected[-1],tuple(target))[1:])
            record={'source':i,'destination':j,'label':u,'slots':slots,'new_star':[sorted(row) for row in desired],'start':start,'end':len(expected)-1}
            if not local:
                after=[sum(len(g)**2 for g in groups),len(_independent_core(groups,h,cyclic))]
                if not after<before:errors.append('nondecreasing scheduled potential')
                record.update(before=before,after=after)
            computed.append(record)
            if covering_number(expected[-1])!=p['q']:errors.append('star endpoint not exact')
        if records!=computed:errors.append('omitted or false prescribed star/schedule evidence')
        if not local:
            ordered=min((groups[i:]+groups[:i] for i in range(3)),key=lambda gs:tuple(map(len,gs))) if cyclic else sorted(groups,key=len)
            canonical=_groups(list(map(len,ordered)));mapping={x:y for old,new in zip(ordered,canonical) for x,y in zip(sorted(old),sorted(new))}
            expected.extend(_permutation_trace(expected[-1],mapping)[1:])
            edges=_independent_core(canonical,h,cyclic);reps={next(i for i,row in enumerate(expected[-1]) if row==edge) for edge in edges}
            for i in range(len(roots)):
                if i not in reps:
                    target=list(expected[-1]);target[i]=edges[0];expected.extend(_bridge(expected[-1],tuple(target))[1:])
            desired=sorted(edges+[edges[0]]*(len(roots)-len(edges)),key=lambda row:tuple(sorted(row)))
            expected.extend(_root_order_trace(expected[-1],desired)[1:])
        if leg!=expected:errors.append('star/canonicalization complete trace mismatch')
        return []
    if p['kind']=='relocate':errors+=check_leg(path,p,[facts['relocation']],True)
    elif p['kind']=='module_pair':
        left=_states(facts['left_path']);right=_states(facts['right_path'])
        if left[0]!=tuple(map(frozenset,roots)) or right[0]!=tuple(map(frozenset,ch['target'])) or left[-1]!=right[-1] or path!=left+list(reversed(right))[1:]:errors.append('module pair legs')
        errors+=check_leg(left,p,facts['balancing']);errors+=check_leg(right,dict(p,sizes=[4,4]),facts['right_balancing'])
    else:errors+=check_leg(path,p,facts['balancing'])
    return errors

def _guard_phase_check(c,r):
    _,p,roots,ch=c['identity'];facts=r['facts'];n=p['N'];count=len(roots);trace=[tuple(map(frozenset,roots))]
    indices=sorted(((i+ch['shift'])%count for i in range(n)),key=lambda i:(ch['target'][i],i))
    order=[i for i in range(count) if i not in indices]+indices;target=tuple(map(frozenset,ch['target']));permuted=tuple(target[i] for i in order)
    for i in range(n,2*n):
        v=list(trace[-1]);v[i]=permuted[i];trace.extend(_bridge(trace[-1],tuple(v))[1:])
    guard_end=len(trace)-1
    for i in range(n):
        v=list(trace[-1]);v[i]=permuted[i];trace.extend(_bridge(trace[-1],tuple(v))[1:])
    coexist_end=len(trace)-1
    trace.extend(_root_order_trace(trace[-1],target)[1:])
    if type(facts['guard_end']) is not int or type(facts['coexist_end']) is not int or facts['guard_end']!=guard_end or facts['coexist_end']!=coexist_end or _states(facts['preliminary_path'])!=trace:return ['guard phase boundaries or full trace changed']
    return []

def _extension_trace_check(c,r):
    family,p,roots,ch=c['identity'];facts=r['facts'];errors=[]
    if family=='M7' and p['kind']=='split_path':
        for name in ('left','right'):
            leg=_states(facts[name+'_path']);expected=[leg[0]]
            while True:
                used=set().union(*expected[-1]);shared=[x for x in sorted(used) if sum(x in row for row in expected[-1])>1]
                if not shared:break
                x=shared[0];i=next(i for i,row in enumerate(expected[-1]) if x in row);y=min(set(range(p['k']))-used)
                expected.append(_toggle_state(expected[-1],i,y,True));expected.append(_toggle_state(expected[-1],i,x,False))
            canonical=_groups(p['a']);mapping={x:y for old,new in zip(expected[-1],canonical) for x,y in zip(sorted(old),sorted(new))}
            expected.extend(_permutation_trace(expected[-1],mapping)[1:])
            if leg!=expected:errors.append('split canonicalization complete trace mismatch')
    if family=='M9':
        nodes=r['nodes'];parentpath=_states(r['path']);trace=[tuple(_states(r['nested_path'])[0])];records=[];boundaries=[0]
        for before,after in zip(parentpath,parentpath[1:]):
            i,x=next((i,x) for i,(a,b) in enumerate(zip(before,after)) for x in sorted(a^b));child=nodes[0][i];add=x in after[i]
            if not add:
                active=set().union(*(trace[-1][v] for v in nodes[child]))
                if x in active:
                    y=min(before[i]-active);used=[v for v in nodes[child] if x in trace[-1][v]];start=len(trace)-1
                    for v in used:trace.append(_toggle_state(trace[-1],v,y,True))
                    for v in reversed(used):trace.append(_toggle_state(trace[-1],v,x,False))
                    records.append({'child':child,'x':x,'y':y,'start':start,'end':len(trace)-1})
            trace.append(_toggle_state(trace[-1],child,x,add));boundaries.append(len(trace)-1)
        if _states(r['nested_path'])!=trace or facts['clearance']!=records or facts['parent_boundaries']!=boundaries:errors.append('native inherited-clearance full trace/events/boundaries mismatch')
    return errors
