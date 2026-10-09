import itertools
import json
import sys
from pins import SCOPE

def observed(f,k):
    occupied = [[int(bool(s & (2**x))) for x in range(k)] for s in f]
    columns = [sum(row[x] for row in occupied) for x in range(k)]
    answer=[]
    for h in range(1,2**k):
        xs=[x for x in range(k) if h & (2**x)]
        if len(xs)==1: answer.append(len(f)-columns[xs[0]])
        elif len(xs)==2:
            x,y=xs
            answer.append(len(f)-columns[x]-columns[y]+sum(row[x]*row[y] for row in occupied))
    return answer

def invert(delta,k):
    if not any(delta): return None
    matches=[]
    for bits in itertools.product((False,True),repeat=k):
        s=sum(2**x for x,b in enumerate(bits) if b)
        for x in range(k):
            t=s^(2**x)
            change=[b-a for a,b in zip(observed([s],k),observed([t],k))]
            if change==delta: matches.append({'label':x,'direction':'delete' if bits[x] else 'add','before':s,'after':t})
    if len(matches)!=1: raise ValueError('nonunique or invalid event')
    return matches[0]

def hit(roots):
    if not roots: return 0
    return 1+min(hit([r for r in roots if x not in r]) for x in min(roots,key=len))

def check(data):
    rows=[]
    for bits in itertools.product((0,1),repeat=6):
        f=[sum(bits[3*r+x]*2**x for x in range(3)) for r in range(2)]
        for r in (0,1):
            for x in range(3):
                for c in (0,1):
                    g=f.copy()
                    if c: g[r]=g[r]+(2**x if not (g[r] & 2**x) else -(2**x))
                    before,after=observed(f,3),observed(g,3)
                    delta=[b-a for a,b in zip(before,after)]
                    rows.append({'id':f+[r,x,c],'before':before,'after':after,'decoded':invert(delta,3)})
    rows.sort(key=lambda r:r['id'])
    def encode(text): return sum(2**'abcdeuvx'.index(c) for c in text)
    raw={'a':['deu','dev'],'b':['dev','deu'],'a_after':['deux','dev'],'b_after':['devx','deu'],
         'dup':['deu','deu'],'dup0':['deux','deu'],'dup1':['deu','deux'],
         'batch_mid':['deux','dev'],'batch_end':['deu','dev']}
    native={n:[encode(s) for s in f] for n,f in raw.items()}
    expected={'scope':SCOPE,'records':rows,'native':native,
              'coverage':{'events':[[1,2,0,2,1],[5,2,1,0,1]],'final':[5,3]},
              'claims':{'root_address_decoded':False,'prospective_guard_derived':False,
                        'initial_count_access_derived':False,'batch_inversion_claimed':False}}
    if data!=expected: raise ValueError('exact universe/value/provenance/scope mismatch')
    # Native controls evaluated independently from occupancy/co-occupancy.
    fields={n:observed(f,8) for n,f in native.items()}
    assert fields['a']==fields['b'] and fields['a_after']!=fields['b_after']
    single=[i for i,h in enumerate(h for h in range(1,256) if h.bit_count()<=2) if h.bit_count()==1]
    assert [fields['a_after'][i] for i in single]==[fields['b_after'][i] for i in single]
    assert fields['dup0']==fields['dup1']
    assert fields['a']==fields['batch_end'] and fields['a']!=fields['batch_mid']
    taus=[]
    for f in raw.values():
        roots=[set(s) for s in ['ab','bc','ac']+f]
        assert all(len(s)>=2 for s in roots)
        taus.append(hit(roots))
    assert taus==[3]*9
    known={}
    for event in expected['coverage']['events']:
        row=next(r for r in rows if r['id']==event)
        known[event[2]]=row['decoded']['after']
    assert [known[r] for r in range(2)]==[5,3]
    return {'status':'PASS_BOUNDED_NOT_GENERAL_PROOF','records':len(rows),'committed':384,'noop':384,
            'native_tau':taus,'native_controls':['swapped_root','singletons_insufficient','address_ambiguity','batch_cancellation'],
            'coverage_final':[known[r] for r in range(2)]}

if __name__ == '__main__': print(json.dumps(check(json.load(open(sys.argv[1]))),sort_keys=True,indent=2))
