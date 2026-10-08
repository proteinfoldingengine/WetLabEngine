"""Independent root-representative product oracle and integer transition relation."""
import itertools
import json
import sys
class CheckError(ValueError):pass
def loads(s):
    def unique(pairs):
        obj={}
        for k,v in pairs:
            if k in obj:raise CheckError('duplicate JSON key')
            obj[k]=v
        return obj
    try:return json.loads(s,object_pairs_hook=unique)
    except (ValueError,TypeError) as e:raise CheckError(str(e)) from e

def reconstruct():
    labels=[(0,1),(2,3),(4,5),(6,7)]
    def supports(n):
        return [labels[0]+((8,) if n&2 else ()),labels[1]+((8,) if n&1 else ()),labels[2],labels[3]]
    def tau(rs):return min(len(set(p)) for p in itertools.product(*rs))
    def sid(n):return format(n,'02b')
    ts={n:tau(supports(n)) for n in range(4)}
    edges=set()
    for n in range(4):
        for bit,root in ((2,'1'),(1,'2')):
            for sign in ('+','-'):
                c=sign+root;edges.add((sid(n),c,sid(n)))
                if bool(n&bit)!=(sign=='+'):
                    target=n^bit
                    if min(map(len,supports(target)))>=2 and ts[target] in (3,4):
                        edges.add((sid(n),c,sid(target)))
    ordered=[list(e) for e in sorted(edges)]
    locked=[e for e in ordered if e[1] in ('+2','-2') and int(e[0],2)&2 and int(e[2],2)&2]
    for a,c,b in locked:
        if int(b[1])!=4-ts[int(b,2)] or ((a!=b)!=(ts[int(a,2)]!=ts[int(b,2)])):
            raise CheckError('locked theorem fails')
    assert ts[0]==ts[1] and (0&1)!=(1&1)
    assert ts[3]!=ts[1] and (3&1)==(1&1)
    assert ts[2]==ts[0]
    assert ('00','+1','00') in edges and ('00','+2','00') in edges
    single=[tau(labels),tau([labels[0]+(8,),*labels[1:]])]
    assert single==[4,4]
    core_views={tuple(tuple(v for v in r if v!=8) for r in supports(n)) for n in range(4)}
    assert len(core_views)==1
    return {'schema':1,'scope_commit':'6b38dddb62b34ced1098c88f214b0190b2ebec7c',
        'proof_commit':'1c5d58a857a633854ab7485e9a0d0cf409f333c5',
        'states':[{'id':sid(n),'tau':ts[n]} for n in range(4)],'outcomes':ordered,'locked_outcomes':locked,
        'fibers':{str(t):[sid(n) for n in range(4) if ts[n]==t] for t in sorted(set(ts.values()))},
        'controls':{'premature_decoder':['00','01'],'silent_anchor':['11','-1','01'],
        'invisible_anchor_cleanup':['10','-1','00'],'all_reject':['00','+1','00','+2','00'],
        'single_root_tau':single,'tau_omitted':[sid(n) for n in range(4)]},
        'claims':{'guaranteed_synchronization':False,'physical_observer_derived':False,'locked_decoder_exact':True}}

def verify(report):
    expected=reconstruct()
    # Serialization distinguishes true from 1 and preserves every list identity/duplicate.
    if json.dumps(report,sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise CheckError('canonical full-domain mismatch')
    return {'status':'PASS','states':len(expected['states']),'outcomes':len(expected['outcomes']),
            'locked_outcomes':len(expected['locked_outcomes']),'physical_observer_derived':False}
if __name__=='__main__':
    with open(sys.argv[1]) as f:report=loads(f.read())
    print(json.dumps(verify(report),sort_keys=True))
