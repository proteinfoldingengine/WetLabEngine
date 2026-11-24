"""Independent reconstruction by per-chart leaf masks and deficient covering teams."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys
from verify_cover_return_budget import verify_budget


def need(ok,why):
    if not ok:
        raise ValueError(why)


def same(a,b,msg):
    need(json.dumps(a,sort_keys=True,separators=(",",":"))==json.dumps(b,sort_keys=True,separators=(",",":")),msg)


def owners(rowmasks,k):
    return tuple(sum(1<<i for i,b in enumerate(rowmasks) if b&(1<<j)) for j in range(k))


def masks(s):
    return [sum(1<<j for j,a in enumerate(s) if a & (1<<v)) for v in range(max(s).bit_length())]


def union(xs):
    out=0
    for x in xs:
        out|=x
    return out


@lru_cache(None)
def team(s):
    return next(t for n in range(1,len(s)+1) for t in combinations(range(len(s)),n)
                if union(s[j] for j in t)==union(s))


def tau(s):
    return len(team(s))


def edit(s,n):
    leaf,j=divmod(abs(n)-1,len(s))
    need(leaf>=0 and j>=0 and bool(s[j] & (1<<leaf))==(n<0),"bad signed edge")
    return tuple(x^(1<<leaf) if i==j else x for i,x in enumerate(s))


def cmd(k,v,j):
    return (v-1)*k+j+1


def codes(path):
    out=[]
    for a,b in zip(path,path[1:]):
        (j,bit),=[(j,x^y) for j,(x,y) in enumerate(zip(a,b)) if x!=y]
        need(bit.bit_count()==1,"nonprimitive step")
        n=cmd(len(a),bit.bit_length(),j)
        out.append(n if b[j]&bit else -n)
    return out


def packet(s,x,y):
    p=[s]
    diff=s[y]&~s[x]
    while diff:
        lowest=diff & -diff
        p.append(edit(p[-1],cmd(len(s),lowest.bit_length(),x)))
        diff^=lowest
    return p


def join(p,target):
    start=p[-1]
    for add in (True,False):
        for v in range(1,max(max(start),max(target)).bit_length()+1):
            bit=1<<(v-1)
            for j in range(len(target)):
                if bool(target[j]&bit)==add and bool(p[-1][j]&bit)!=add:
                    p.append(edit(p[-1],(1 if add else -1)*cmd(len(target),v,j)))


def rewrite(path,q):
    meta=[]
    while max(map(tau,path))>q:
        peak=max(map(tau,path))
        need(max(tau(path[0]),tau(path[-1]))<peak,"raised endpoint")
        adapted=[packet(s,*team(s)[:2])[-1] if tau(s)==peak else s for s in path]
        new=[adapted[0]]
        for s in adapted[1:]:
            join(new,s)
        meta.append(dict(peak=peak,before=len(path),after=len(new)))
        need(max(map(tau,new))<peak,"peak retained")
        path=new
    return path,meta


def constructed(s,q):
    trajectories=[]
    logged=[]
    for reverse in (False,True):
        p=[s]
        calls=[]
        while tau(p[-1])>q:
            h=team(p[-1])
            x,y=(h[-1],h[-2]) if reverse else h[:2]
            new=packet(p[-1],x,y)
            need(tau(new[-1])==len(h)-1,"packet decrement")
            p.extend(new[1:])
            calls.append([x,y,codes(new)])
        trajectories.append(p)
        logged.append(calls)
    original=trajectories[0][::-1]+trajectories[1][1:]
    final,meta=rewrite(original,q)
    return dict(legs=logged,first=masks(final[0]),last=masks(final[-1]),original=codes(original),
                returned=codes(final),layers=meta,returned_tau=list(map(tau,final)),
                shadow=masks(packet(s,*team(s)[:2])[-1]))


def deficits(s,q):
    """A newly covering q-team missed exactly one leaf before the repair."""
    target=union(s)
    options=set()
    for t in combinations(range(len(s)),q):
        absent=target^union(s[j] for j in t)
        if absent.bit_count()==1:
            options.update(cmd(len(s),absent.bit_length(),j) for j in t)
    return sorted(options)


def arm(s,source,leaf,q):
    post=edit(s,-cmd(len(s),leaf,source))
    need(union(post)==union(s) and (tau(s),tau(post))==(q,q+1),"wrong source")
    original,meta=rewrite([s,post,s],q)
    return dict(trigger=[q,q+1,True],post=masks(post),repairs=deficits(post,q),run=constructed(post,q),
                cycle=codes(original),cycle_layers=meta)


def layout(q,counts,pi):
    k=q+2
    receiver,ua,va,source=pi[:4]
    s=[0]*k
    s[ua],s[va],s[source]=1,2,3
    pos=2
    for number,j in zip(counts,[source,receiver,*pi[4:]]):
        s[j] |= ((1<<number)-1)<<pos
        pos+=number
    return tuple(s)


def all_keys():
    keys=set()
    for q in (2,3):
        indices=set(range(q+2))
        for s,r in permutations(sorted(indices),2):
            remaining=indices-{s,r}
            for u,v in permutations(sorted(remaining),2):
                roles=(r,u,v,s,*sorted(remaining-{u,v}))
                for large in range(1<<q):
                    sizes=tuple(1+((large>>i)&1) for i in range(q))
                    keys.add((q,sizes,roles))
    return sorted(keys)


def numbers(s,j):
    size=union(s).bit_length()
    return [1+size-s[j].bit_count()]+[1]*s[j].bit_count()


def checks_named(q):
    k=q+2
    s=layout(q,(2,)*q,tuple(range(k)))
    out=dict(before=masks(s),prior_run=constructed(s,q),arms=[])
    for v in (1,2):
        case=arm(s,3,v,q)
        post=owners(case["post"],k)
        first=owners(case["run"]["first"],k)
        wanted=sorted(cmd(k,v,j) for j in (0,3,*range(4,k)))
        need(wanted==case["repairs"],"two-witness return theorem")
        nonundo=[n for n in wanted if n!=cmd(k,v,3)]
        trace=case["run"]
        need(trace["legs"][0]==[[0,v,[cmd(k,v,0)]]],"named receiver")
        cycle=[cmd(k,v,0),-cmd(k,v,3),cmd(k,v,3),-cmd(k,v,0)]
        need(case["cycle"]==cycle,"anticipating cover repair")
        double=[post]
        for w in (3-v,v):
            double.append(edit(double[-1],cmd(k,w,0)))
        bypass=[post]
        for w in (5,6):
            bypass.append(edit(bypass[-1],cmd(k,w,v)))
        need(list(map(tau,double))==list(map(tau,bypass))==[q+1,q+1,q] and
             bypass[-1][0]==s[0] and bypass[-1][3]==post[3],"two-step bypass")
        out["arms"].append(dict(leaf=v,source=case["trigger"],source_p1=[numbers(a,3) for a in (s,post)],
                  receiver_p1=[numbers(a,0) for a in (post,first)],forward=trace["legs"][0],
                  reverse=trace["legs"][1],original=trace["original"],returned=trace["returned"],
                  first=masks(first),end=trace["last"],cycle=cycle,all_one_step=wanted,cut_kept=nonundo,
                  idle=constructed(post,q+1),both=dict(seq=codes(double),q=list(map(tau,double)),end=masks(double[-1])),
                  bypass=dict(seq=codes(bypass),q=list(map(tau,bypass)),end=masks(bypass[-1]))))
    need(out["arms"][0]["both"]["end"]!=out["arms"][1]["both"]["end"] and
         owners(out["arms"][0]["both"]["end"],k)[0]==owners(out["arms"][1]["both"]["end"],k)[0],
         "receiver versus whole-state equality")
    return out


def six():
    original=(16,41,2,28)
    out={}
    for name,pi in (("original",(0,1,2,3)),("swap_0_2",(2,1,0,3))):
        prior=tuple(original[pi[j]] for j in range(4))
        moves=[(j,v) for j,owned in enumerate(original) for v in range(1,7) if owned&(1<<(v-1))
               and sum(bool(x&(1<<(v-1))) for x in original)>1]
        need(set(moves)=={(1,4),(3,4),(0,5),(3,5)},"original six event set")
        cuts=[]
        for source,leaf in ((1,4),(3,4),(0,5),(3,5)):
            j=pi[source]
            post=edit(prior,-cmd(4,leaf,j))
            cuts.append(dict(actor=j,v=leaf,source=[tau(prior),tau(post),tau(post)>tau(prior)],
                             post=masks(post),run=constructed(post,3)))
        out[name]=dict(prior=masks(prior),prior_run=constructed(prior,3),cuts=cuts)
    extras=[]
    for j in (1,3):
        source=edit(original,-cmd(4,4,j))
        for cut in (None,0,3):
            state=source if cut is None else edit(source,-cmd(4,5,cut))
            data=dict(actor=j,cut=cut,state=masks(state),run=constructed(state,3))
            if cut==3:
                trials=[]
                for v in (1,3,4,5,6):
                    donor,=[k for k,n in enumerate(state) if n&(1<<(v-1))]
                    change=state[donor].bit_count()==1
                    nxt=edit(state,cmd(4,v,2))
                    need(tau(nxt)==4-int(change),"sole private donor criterion")
                    trials.append([v,4-int(change),not change])
                data["receiver_trials"]=trials
            extras.append(data)
    out["protected_continuations"]=extras
    return out


def restore_count(cases):
    all_counts={}
    for q,sizes,roles,start,arms in cases:
        ident=str(q)+"_"+"".join(map(str,sizes))
        group=all_counts.setdefault(ident,Counter())
        group["preparations"]+=1
        for v,a in enumerate(arms,1):
            k=q+2
            with_source=[n for n in a["repairs"] if (n-1)%k!=roles[3] or (n-1)//k+1!=v]
            first=a["run"]["legs"][0][0][2]
            group.update(dict(arms=1,unique_with_cut_kept=int(len(with_source)==1),
                              all_spell_released_leaf=int(all((n-1)//k+1==v for n in a["repairs"])),
                              forward_one_edit=int(len(first)==1),
                              forward_single_to_designated_R=int(first==[cmd(k,v,roles[0])])))
    return all_counts


def key(row):
    return row[0],tuple(row[1]),tuple(row[2])


def reject(fn,*args):
    try:
        fn(*args)
    except ValueError:
        return
    raise ValueError("corruption did not fail")


def row_check(row,ident):
    q,sizes,pi=ident
    s=layout(q,sizes,pi)
    expected=[q,list(sizes),list(pi),masks(s),[arm(s,pi[3],v,q) for v in (1,2)]]
    same(row,expected,"complete endpoints, packets or chronology")


def main(directory):
    raw=lzma.decompress((directory/"cover_return_universe.json.xz").read_bytes())
    universe=json.loads(raw)
    same(sorted(universe),["budget","primary"],"universe sections")
    rows=universe["primary"]
    cert=json.loads((directory/"cover_return_certificate.json").read_bytes())
    keys=all_keys()
    def coverage(records):
        need(list(map(key,records))==keys,"prior identity/order")
    coverage(rows)
    for row,ident in zip(rows,keys):
        row_check(row,ident)
    z=owners([1,2,4,8,1],4)
    reg=dict(identity=["M1",dict(kind="layers",k=4,a=[1]*5,q=3),[[0],[1],[2],[3],[0]],{"peak":4}],
             run=constructed(z,3))
    archival=dict(archive="v16.54-parent-support-connectivity/evidence/validated/run-37075311542-attempt-1/shard-0/original.zip.part0000",
                  zip_sha256="ace5305518cf102ca15d8e48b0d7b8df4735672d311ad40bfccea339df205b97",line=56732,
                  record_sha256="5ceda0b05b2a8d1a00c14e6830c7f6c17817262278e5f20fa527aa48a94f4d25",
                  run=constructed(owners([1,2,4,8,16,32,1],6),3))
    for field,want in (("schema",1),("preparations",len(keys)),("arms",2*len(keys)),("counts",restore_count(rows)),
                       ("raw_sha256",sha256(raw).hexdigest()),("original_six",six()),("original_m1",reg),
                       ("archived_record",archival),("named",{str(q):checks_named(q) for q in (2,3)})):
        same(cert[field],want,field)
    need(len(keys)==1056,"finite domain")
    verify_budget(universe["budget"],cert["budget"])
    balls=universe["budget"]["balls"]
    def bad_prefix():
        data=dict(universe["budget"],balls=balls[1:])
        verify_budget(data,cert["budget"])
    reject(bad_prefix)
    balls[0][4]["marked_masks"][0].append(0)
    reject(verify_budget,universe["budget"],cert["budget"])
    balls[0][4]["marked_masks"][0].pop()
    reject(coverage,rows[:-1])
    reject(coverage,[rows[0]]+rows[:-1])
    bad=json.loads(json.dumps(rows[0]))
    bad[2][0],bad[2][1]=bad[2][1],bad[2][0]
    reject(row_check,bad,keys[0])
    for field in ("repairs","trigger","legs","cycle","returned","shadow"):
        bad=json.loads(json.dumps(rows[-1]))
        a=bad[4][0]
        if field=="repairs": a[field].append(-1)
        if field=="trigger": a[field][-1]=False
        if field=="legs": a["run"][field][0][0][0]=-1
        if field=="cycle": a[field][0]=-a[field][0]
        if field=="returned": a["run"][field].append(0)
        if field=="shadow": a["run"][field][0]=0
        reject(row_check,bad,keys[-1])
    reject(same,cert["original_six"]["original"]["cuts"][1]["run"],cert["original_six"]["original"]["cuts"][3]["run"],"crossing")
    return dict(status="PASS",complete_preparations=len(keys),complete_arms=len(keys)*2,
                exact_packets_and_paths=True,budget_arms=81,bounded_graphs=10,rejecting_controls=12)


if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[2])),sort_keys=True))
