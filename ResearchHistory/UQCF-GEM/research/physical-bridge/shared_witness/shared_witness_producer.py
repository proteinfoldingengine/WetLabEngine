"""Full carrier subset oracle; no import from independent verifier."""
import itertools
import json
CORE = [set('ab'), set('cd'), set('ef'), set('gh')]
def roots(s):
    return [r | ({'w'} if i < 2 and s[i]=='1' else set()) for i,r in enumerate(CORE)]
def hitting(rr):
    carrier=sorted(set.union(*rr))
    for k in range(len(carrier)+1):
        if any(all(set(c)&r for r in rr) for c in itertools.combinations(carrier,k)):
            return k

def produce():
    ids=[''.join(s) for s in itertools.product('01',repeat=2)]
    states=[{'id':s,'tau':hitting(roots(s))} for s in ids]
    values={r['id']:r['tau'] for r in states}
    outcomes=[]
    for s in ids:
        for c in ('+1','-1','+2','-2'):
            outcomes.append([s,c,s])
            i=int(c[1])-1; wanted='1' if c[0]=='+' else '0'
            if s[i]!=wanted:
                t=s[:i]+wanted+s[i+1:]
                if all(len(r)>=2 for r in roots(t)) and 3<=hitting(roots(t))<=4:
                    outcomes.append([s,c,t])
    outcomes.sort()
    assert values['00']==values['01'] and '00'[1]!='01'[1]
    assert values['11']!=values['01'] and '11'[1]=='01'[1]
    assert values['10']==values['00']
    assert all([s,c,s] in outcomes for s in ids for c in ('+1','-1','+2','-2'))
    single=[hitting([CORE[0]|({'w'} if b else set()),*CORE[1:]]) for b in (0,1)]
    assert single==[4,4]
    assert len({tuple(tuple(sorted(r & set('abcdefgh'))) for r in roots(s)) for s in ids})==1
    return {'schema':1,'scope_commit':'6b38dddb62b34ced1098c88f214b0190b2ebec7c',
        'proof_commit':'1c5d58a857a633854ab7485e9a0d0cf409f333c5','states':states,
        'outcomes':outcomes,'locked_outcomes':[e for e in outcomes if e[0][0]==e[2][0]=='1' and e[1][1]=='2'],
        'fibers':{str(t):[s for s in ids if values[s]==t] for t in sorted(set(values.values()))},
        'controls':{'premature_decoder':['00','01'],'silent_anchor':['11','-1','01'],
                    'invisible_anchor_cleanup':['10','-1','00'],'all_reject':['00','+1','00','+2','00'],
                    'single_root_tau':single,'tau_omitted':ids},
        'claims':{'guaranteed_synchronization':False,'physical_observer_derived':False,'locked_decoder_exact':True}}
if __name__=='__main__':print(json.dumps(produce(),sort_keys=True,indent=2))
