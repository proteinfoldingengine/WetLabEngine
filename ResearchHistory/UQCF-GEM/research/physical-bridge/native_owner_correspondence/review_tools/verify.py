"""Independent reconstruction: Dyck words, atom predicates, no producer import."""
import itertools, json, sys
SCIENCE='20fedca0242791266e9851c1dc6cb4591888be15'

def require(ok, message):
    if not ok: raise ValueError(message)

def trees():
    found=set()
    for n in range(1,6):
        for word in itertools.product((1,-1), repeat=2*(n-1)):
            if sum(word): continue
            stack=[()]; counts={():0}; nodes=[()]; valid=True
            for direction in word:
                if direction==1:
                    parent=stack[-1]; child=parent+(counts[parent],)
                    counts[parent]+=1; counts[child]=0; nodes.append(child); stack.append(child)
                elif len(stack)==1: valid=False; break
                else: stack.pop()
            if valid and len(stack)==1: found.add(tuple(sorted(nodes)))
    require(len(found)==23,'Dyck tree universe is not 23')
    return sorted(found)

def subsets(x):
    return [tuple(v for v,bit in zip(x,mask) if bit) for mask in itertools.product((0,1),repeat=len(x))
            if mask[0] and all(not bit or not v or mask[x.index(v[:-1])] for v,bit in zip(x,mask))]

def expected(x,y):
    p=[[0]*len(x) for _ in y]; s=[[0]*len(x) for _ in y]
    for j,u in enumerate(x):
        ancestors=[v for v in y if u[:len(v)]==v]
        owner=max(ancestors,key=len)
        for i,v in enumerate(y): p[i][j]=int(v==owner); s[i][j]=int(v==u)
    return p,s

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def validate(c):
    require(set(c)=={'source_sha','n_max','records','witness'},'certificate schema')
    require(c['source_sha']==SCIENCE and c['n_max']==5,'source/domain provenance')
    expected_ids={(x,y) for x in trees() for y in subsets(x)}
    entries={}
    for row in c['records']:
        require(set(row)=={'X','Y','P','S'},'record schema')
        x=tuple(tuple(v) for v in row['X']); y=tuple(tuple(v) for v in row['Y']); key=(x,y)
        require(key not in entries,'duplicate identity')
        require(key in expected_ids,'invalid or substituted carrier')
        p,s=expected(x,y)
        require(row['P']==p and row['S']==s,'incorrect atom action')
        require(all(type(v) is int for a in (row['P'],row['S']) for rr in a for v in rr),'noninteger entry')
        entries[key]=(p,s)
    require(set(entries)==expected_ids,'incomplete canonical universe')
    chains=0; leaves=0
    for (x,y),(p,s) in entries.items():
        require(all(sum(p[i][j] for i in range(len(y)))==1 for j in range(len(x))),'native total')
        if x==y: require(p==s==[[int(i==j) for j in range(len(x))] for i in range(len(x))],'identity')
        for z in subsets(y):
            pyz,syz=expected(y,z); pxz,sxz=expected(x,z)
            require(mul(pyz,p)==pxz and mul(syz,s)==sxz,'composition')
            chains+=1
        # Independent renamed/reversed-storage construction, then permute back.
        rename=lambda v: tuple(2*t+3 for t in v)
        xr=tuple(rename(v) for v in reversed(x)); yr=tuple(rename(v) for v in reversed(y))
        pr,sr=expected(xr,yr)
        require(pr==[list(reversed(r)) for r in reversed(p)] and sr==[list(reversed(r)) for r in reversed(s)],'relabel covariance')
        removed=set(x)-set(y)
        if len(removed)==1:
            u=next(iter(removed)); a=u[:-1]
            require(a in y,'leaf parent missing')
            for i,v in enumerate(y):
                if v!=a: require(p[i]==s[i],'unrelated receiver changed')
            require(p[y.index(a)][x.index(u)]==1 and s[y.index(a)][x.index(u)]==0,'delivery/blind atom')
            leaves+=1
    x=((),(0,),(0,0)); y=((),(0,)); p,s=expected(x,y)
    inputs=([1,0,0],[1,0,1]); act=lambda a,v:[sum(t*b for t,b in zip(row,v)) for row in a]
    witness={'initial_R':[v[1] for v in inputs], 'native_outputs':[act(p,v) for v in inputs],
             'delivery_R':[act(p,v)[1] for v in inputs], 'blind_R':[act(s,v)[1] for v in inputs]}
    require(c['witness']==witness,'receiver witness mismatch')
    require(witness['initial_R']==[0,0] and witness['delivery_R']==[0,1] and witness['blind_R']==[0,0],'witness contrast')
    return {'status':'PASS','trees':23,'arrows':len(entries),'chains':chains,'leaf_prunings':leaves,
            'source_sha':SCIENCE,'native_bridge_status':'NOT_DERIVED'}

if __name__=='__main__':
    try: print(json.dumps(validate(json.load(open(sys.argv[1]))),sort_keys=True))
    except Exception as e:
        print(json.dumps({'status':'REJECTED','error':str(e)},sort_keys=True)); sys.exit(1)
