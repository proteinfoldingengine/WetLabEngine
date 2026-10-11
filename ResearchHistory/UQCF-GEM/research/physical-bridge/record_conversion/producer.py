"""Bitset producer: independently reconstructable nested-record histories."""
import itertools, json, pathlib, sys

PARENT='0427e18aeae1625b7bd685e511038f769eef0c01'
SCOPE='477119113be8674a4b090a2056137d74553dd04fb44515b37a6c249523f13b0c'
COMMANDS=[[2,4,1],[2,0,-1],[2,1,1],[2,4,-1],[1,4,-1]]
PARENTS={1:0,2:1,3:1,4:0,5:0}
CHILDREN={0:[1,4,5],1:[2,3],2:[],3:[],4:[],5:[]}

def hitting(roots):
    union=0
    for s in roots: union |= s
    dp={0:0}
    for x in range(union.bit_length()):
        cover=sum(1<<i for i,s in enumerate(roots) if s&(1<<x))
        for old,cost in list(dp.items()):
            new=old|cover;dp[new]=min(dp.get(new,99),cost+1)
    return dp[(1<<len(roots))-1]

def profile(state): return [hitting([state[v] for v in CHILDREN[u]]) for u in (0,1)]

def step(state, command):
    v,x,sign=command;bit=1<<x
    if sign==1:
        if state[v]&bit or not state[PARENTS[v]]&bit:return None
        nxt=state.copy();nxt[v]|=bit
    else:
        if not state[v]&bit or state[v]==bit or any(state[c]&bit for c in CHILDREN[v]):return None
        nxt=state.copy();nxt[v]&=~bit
    return nxt

def initial(n,digits,sigma):
    A=W=3;B=4;C=8
    for j,k in enumerate(digits,5):
        if k in (1,2):A|=1<<j
        if k==2:W|=1<<j
        if k==3:B|=1<<j
        if k==4:C|=1<<j
    return [(1<<(5+n))-1,A|(16 if sigma else 0),1,W,B,C],A

def history(n,digits,sigma,mask):
    state,A=initial(n,digits,sigma);states=[state.copy()];executed=[];failure=None
    for pos,command in enumerate(COMMANDS,1):
        if mask&(1<<(pos-1)):
            nxt=step(state,command)
            if nxt is None:failure=pos;break
            state=nxt;executed.append(pos)
        states.append(state.copy())
    profiles=[profile(s) for s in states]
    return {'id':[n,list(digits),sigma,mask],'status':'VALID' if failure is None else 'REJECTED',
            'states':states,'profiles':profiles,'executed':executed,'failure':failure,'end':state.copy(),
            'record_at_stop':int(not(state[2]&1)),'source_erased_at_stop':state[1]==A,
            'peak':max(abs(h[0]-3)+abs(h[1]-1) for h in profiles)}

def produce():
    rows=[history(n,d,s,m) for n in range(3) for d in itertools.product(range(5),repeat=n) for s in (0,1) for m in range(32)]
    state,A=initial(0,(),0);states=[state.copy()]
    for cmd in ([2,1,1],[2,0,-1]):
        state=step(state,cmd)
        if state is None:raise ValueError('counterhistory unexpectedly illegal')
        states.append(state.copy())
    ps=[profile(s) for s in states]
    return {'schema':'nested-record-conversion-v1','source_parent':PARENT,'scope_sha256':SCOPE,
            'commands':COMMANDS,'rows':rows,
            'forgery':{'states':states,'profiles':ps,'native_valid':True,'protocol_valid':False,
                       'record':int(not(state[2]&1)),'source_erased':state[1]==A,'peak':max(abs(h[0]-3)+abs(h[1]-1) for h in ps)},
            'claims':{'protocol_sound':True,'native_access':False,'guaranteed_write':False,'optimality':False}}

if __name__=='__main__':
    doc=produce();pathlib.Path(sys.argv[1]).write_text(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'requested':len(doc['rows']),'valid':sum(r['status']=='VALID' for r in doc['rows'])}))
