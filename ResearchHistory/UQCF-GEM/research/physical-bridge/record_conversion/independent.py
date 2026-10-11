"""Set-partition enumeration and full-state checking; no producer imports."""
import itertools, json, pathlib, sys

PARENT='0427e18aeae1625b7bd685e511038f769eef0c01'
SCOPE='477119113be8674a4b090a2056137d74553dd04fb44515b37a6c249523f13b0c'

def subsets(xs):
    xs=sorted(xs)
    for k in range(len(xs)+1):
        for choice in itertools.combinations(xs,k):yield set(choice)

def encode(state):return [sum(2**x for x in S) for S in state]

def admitted(state,palette):
    return state[0]==palette and all(state) and all(state[c]<=state[p] for c,p in ((1,0),(2,1),(3,1),(4,0),(5,0)))

def advance(state,op,palette):
    v,x,sign=op
    if (sign==1 and x in state[v]) or (sign==-1 and x not in state[v]):return None
    nxt=[s.copy() for s in state]
    if sign==1:nxt[v].add(x)
    else:nxt[v].remove(x)
    changes=[(i,y) for i,(s,t) in enumerate(zip(state,nxt)) for y in s^t]
    if changes!=[(v,x)] or not admitted(nxt,palette):return None
    return nxt

def heights(state):
    out=[]
    for children in ((1,4,5),(2,3)):
        for k in range(1,len(state[0])+1):
            if any(all(set(z)&state[c] for c in children) for z in itertools.combinations(sorted(state[0]),k)):
                out.append(k);break
        else:raise ValueError('empty or uncovered support')
    return out

def expected():
    commands=[[2,4,1],[2,0,-1],[2,1,1],[2,4,-1],[1,4,-1]];rows=[]
    for n in (0,1,2):
        palette=set(range(n+5));extras=palette-set(range(5))
        for Ae in subsets(extras):
            for We in subsets(Ae):
                for Be in subsets(extras-Ae):
                    for Ce in subsets(extras-Ae-Be):
                        A={0,1}|Ae;W={0,1}|We;B={2}|Be;C={3}|Ce
                        digits=[2 if x in We else 1 if x in Ae else 3 if x in Be else 4 if x in Ce else 0 for x in sorted(extras)]
                        for sigma in (0,1):
                            for mask in range(32):
                                state=[palette.copy(),A|({4} if sigma else set()),{0},W.copy(),B.copy(),C.copy()]
                                if not admitted(state,palette):raise ValueError('reconstructed initial state')
                                states=[encode(state)];ps=[heights(state)];executed=[];failure=None
                                for pos,op in enumerate(commands,1):
                                    if (mask//(2**(pos-1)))%2:
                                        nxt=advance(state,op,palette)
                                        if nxt is None:failure=pos;break
                                        state=nxt;executed.append(pos)
                                    states.append(encode(state));ps.append(heights(state))
                                rows.append({'id':[n,digits.copy(),sigma,mask],'status':'VALID' if failure is None else 'REJECTED',
                                             'states':states,'profiles':ps,'executed':executed,'failure':failure,'end':encode(state),
                                             'record_at_stop':int(0 not in state[2]),'source_erased_at_stop':state[1]==A,
                                             'peak':max(abs(a-3)+abs(b-1) for a,b in ps)})
    rows.sort(key=lambda r:r['id'])
    palette=set(range(5));state=[palette.copy(),{0,1},{0},{0,1},{2},{3}];states=[encode(state)];ps=[heights(state)]
    native=True;forgery_commands=[[2,1,1],[2,0,-1]]
    for op in forgery_commands:
        state=advance(state,op,palette)
        if state is None:native=False;break
        states.append(encode(state));ps.append(heights(state))
    if not native:raise ValueError('native counterhistory failed')
    cursor=0
    for op in commands:
        if cursor<len(forgery_commands) and op==forgery_commands[cursor]:cursor+=1
    forgery={'states':states,'profiles':ps,'native_valid':native,'protocol_valid':cursor==len(forgery_commands),
             'record':int(0 not in state[2]),'source_erased':state[1]=={0,1},'peak':max(abs(a-3)+abs(b-1) for a,b in ps)}
    return {'schema':'nested-record-conversion-v1','source_parent':PARENT,'scope_sha256':SCOPE,
            'commands':commands,'rows':rows,'forgery':forgery,
            'claims':{'protocol_sound':True,'native_access':False,'guaranteed_write':False,'optimality':False}}

def verify(doc):
    truth=expected()
    if json.dumps(doc,sort_keys=True,separators=(',',':'))!=json.dumps(truth,sort_keys=True,separators=(',',':')):
        raise ValueError('complete canonical reconstruction mismatch')
    rows=truth['rows'];valid=[r for r in rows if r['status']=='VALID']
    for r in valid:
        if r['peak']>1 or (r['record_at_stop'] and not r['id'][2]):raise ValueError('mathematical claim fails')
        if r['record_at_stop'] and r['source_erased_at_stop'] and (r['id'][3]!=31 or r['end'][2]!=2):raise ValueError('conversion endpoint fails')
    return {'status':'VERIFIED','requested':len(rows),'valid':len(valid),'rejected':len(rows)-len(valid),
            'positive_valid':sum(r['record_at_stop'] for r in valid),
            'source_erased_positive':sum(r['record_at_stop'] and r['source_erased_at_stop'] for r in valid),
            'saved_slice_occurrences':sum(len(r['states']) for r in rows),'complete_canonical_record_equality':True,
            'native_access_derived':False,'guaranteed_write':False}

if __name__=='__main__':
    doc=json.loads(pathlib.Path(sys.argv[1]).read_text());summary=verify(doc)
    if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
