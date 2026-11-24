"""Execute the historical cover guard, its two packet legs, and its path rewrite."""
from collections import Counter
import gzip
from hashlib import sha1, sha256
import importlib.util
from itertools import islice, permutations, product
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

from check_protected_work import DEMOS, modules, need
from cover_return_budget import budget_universe

HIST = "v16.54-parent-support-connectivity/"
PINS = {"model": ("model.py","a4a6407990c36084ab3b6e8e7da9022a4f9d63a8"),
        "m54": ("mechanisms.py","ab3541cba29d5e1ebd4fe6c56128daf020c1a81f"),
        "v54": ("verifier.py","e19999dfd46cd134d8191a59da7b8bf2cdb74b43"),
        "u54": ("universe.py","517ab8e20bc364c106e9a9b3ffaac23dc3a3b258")}


def historical(root):
    h = modules(root)
    for key,(file,digest) in PINS.items():
        p = root/DEMOS/HIST/file
        raw = p.read_bytes()
        need(sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()==digest,file)
        spec=importlib.util.spec_from_file_location(key,p)
        h[key]=sys.modules[key]=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(h[key])
    return h


def wire(rows):
    return [sum(1<<j for j in r) for r in rows]


def views(rows,k):
    return [[0]+[v for v,row in enumerate(rows,1) if j in row] for j in range(k)]


def commands(path,k):
    seq=[]
    for a,b in zip(path,path[1:]):
        (v,j),=[(v,j) for v,(x,y) in enumerate(zip(a,b)) for j in set(x)^set(y)]
        seq.append((1 if j in b[v] else -1)*(1+k*v+j))
    return seq


def push(h,rows,k,j):
    p=(-1,)+(0,)*len(rows)
    return list(map(int,h["refine"].push(p,views(rows,k)[j],[1]*len(p))))


def atom(h,rows,k,j,v):
    p=(-1,)+(0,)*len(rows)
    cert=h["atom"].atomic(p,views(rows,k),j,v)
    h["verify"].verify_atomic(cert)
    after=tuple(frozenset(i for i,view in enumerate(cert["after"]) if w in view) for w in range(1,len(p)))
    return after,[cert["tau_before"],cert["tau_after"],cert["trigger"]]


def layers(h,rows,k,q,case=None):
    model=h["model"]
    high=model.tau(rows)
    if case is None:
        case=h["u54"].case("M1","layers",k,[1]*len(rows),q,rows,{"peak":high})
    legs=[[],[]]
    current={}
    packet=model.Path.packet.__code__
    caller=h["m54"].packet_family.__code__
    def trace(frame,event,arg):
        if frame.f_code==packet and frame.f_back.f_code==caller:
            if event=="call":
                f=frame.f_locals
                current[id(frame)]=(int(frame.f_back.f_locals["reverse"]),f["x"],f["y"],len(f["self"].vertices)-1)
            elif event=="return":
                side,x,y,start=current.pop(id(frame))
                legs[side].append([x,y,commands(frame.f_locals["self"].vertices[start:],k)])
        return trace
    prev=sys.gettrace()
    try:
        sys.settrace(trace)
        result=h["m54"].produce(case)
    finally:
        sys.settrace(prev)
    need(not current and result["status"]=="PASS","incomplete layers execution")
    errors=h["v54"].verify_record(case,result)
    need(not errors,str(errors))
    original=result["facts"]["original_path"]
    final=result["path"]
    return dict(legs=legs,first=wire(final[0]),last=wire(final[-1]),original=commands(original,k),
                returned=commands(final,k),layers=result["facts"]["layers"],
                returned_tau=result["tau"],shadow=wire(model.shadow(rows)))


def shortest(h,rows,k,q):
    options=[]
    for v,row in enumerate(rows):
        for j in range(k):
            if row=={j}:
                continue
            trial=list(rows)
            trial[v]=row^{j}
            if h["model"].tau(trial)==q:
                options.append((1 if j not in row else -1)*(1+k*v+j))
    return sorted(options)


def make(sizes,pi):
    r,a,b,s=pi[:4]
    owners=[s,r,*pi[4:]]
    rows=[{s,a},{s,b}]
    for j,n in zip(owners,sizes):
        rows.extend([{j} for _ in range(n)])
    return tuple(map(frozenset,rows))


def finite_arm(h,before,k,source,v,q):
    post,trigger=atom(h,before,k,source,v)
    need(trigger==[q,q+1,True],"expected source increment")
    run=layers(h,post,k,q)
    cycle,meta=h["model"].clip([before,post,before],q)
    return dict(trigger=trigger,post=wire(post),repairs=shortest(h,post,k,q),run=run,
                cycle=commands(cycle,k),cycle_layers=meta)


def with_added(rows,leaf,chart):
    states=list(rows)
    need(chart not in states[leaf-1],"repeated addition")
    states[leaf-1]=states[leaf-1]|{chart}
    return tuple(states)


def family(h):
    records=[]
    for q in (2,3):
        k=q+2
        for sizes in product((1,2),repeat=q):
            for pi in permutations(range(k)):
                before=make(sizes,pi)
                arms=[finite_arm(h,before,k,pi[3],leaf,q) for leaf in (1,2)]
                records.append([q,list(sizes),list(pi),wire(before),arms])
    return records


def controls(h,q):
    model=h["model"]
    k=q+2
    before=make([2]*q,tuple(range(k)))
    ctrl=dict(before=wire(before),prior_run=layers(h,before,k,q),arms=[])
    for v in (1,2):
        post,source=atom(h,before,k,3,v)
        data=finite_arm(h,before,k,3,v,q)
        ones=[n for n in data["repairs"] if (n-1)%k!=3]
        # Common receiver endpoint with both contested leaves, source unchanged.
        other=3-v
        a=with_added(post,other,0)
        both=with_added(a,v,0)
        alt=[post,a,both]
        # Copy R's two private leaves to the helper which took sole ownership.
        bypass=[post]
        for private in views(before,k)[0][1:]:
            bypass.append(with_added(bypass[-1],private,v))
        first_state=model.shadow(post)
        ctrl["arms"].append(dict(leaf=v,source=source,source_p1=[push(h,y,k,3) for y in (before,post)],
                    receiver_p1=[push(h,y,k,0) for y in (post,first_state)],forward=data["run"]["legs"][0],
                    reverse=data["run"]["legs"][1],original=data["run"]["original"],
                    returned=data["run"]["returned"],first=wire(first_state),end=data["run"]["last"],
                    cycle=data["cycle"],all_one_step=data["repairs"],cut_kept=ones,
                    idle=layers(h,post,k,q+1),both=dict(seq=commands(alt,k),q=list(map(model.tau,alt)),end=wire(both)),
                    bypass=dict(seq=commands(bypass,k),q=list(map(model.tau,bypass)),end=wire(bypass[-1]))))
    return ctrl


def six(h):
    base=({1},{2},{3},{1,3},{0,3},{1})
    original=tuple(map(frozenset,base))
    doc={}
    for name,pi in (("original",(0,1,2,3)),("swap_0_2",(2,1,0,3))):
        prior=tuple(frozenset(pi[j] for j in group) for group in original)
        k=4
        record=dict(prior=wire(prior),prior_run=layers(h,prior,k,3),cuts=[])
        for j,v in ((1,4),(3,4),(0,5),(3,5)):
            post,src=atom(h,prior,k,pi[j],v)
            record["cuts"].append(dict(actor=pi[j],v=v,source=src,post=wire(post),run=layers(h,post,k,3)))
        doc[name]=record
    extras=[]
    for j in (1,3):
        base,_=atom(h,original,4,j,4)
        for cut in (None,0,3):
            state=base if cut is None else atom(h,base,4,cut,5)[0]
            item=dict(actor=j,cut=cut,state=wire(state),run=layers(h,state,4,3))
            if cut==3:
                p=(-1,)+(0,)*6
                tests=[]
                for v in range(1,7):
                    if 2 in state[v-1]:
                        continue
                    nxt=with_added(state,v,2)
                    equal=h["invisible"].adjacent(p,views(state,4),views(nxt,4))
                    cert=dict(parents=p,before=views(state,4),after=views(nxt,4))
                    h["invisible"].verify_move(cert,equal)
                    inverse,_=atom(h,nxt,4,2,v)
                    need(inverse==state,"addition not admitted")
                    tests.append([v,h["model"].tau(nxt),equal])
                item["receiver_trials"]=tests
            extras.append(item)
    doc["protected_continuations"]=extras
    return doc


def archive_control(h):
    case=next(c for c in h["u54"].m1({}) if c["identity"][1]["kind"]=="layers")
    family,p,roots,ch=case["identity"]
    need(family=="M1" and p["k"]==4 and ch=={"peak":4} and roots==[[0],[1],[2],[3],[0]],"registered case")
    rows=tuple(map(frozenset,roots))
    return dict(identity=case["identity"],run=layers(h,rows,p["k"],p["q"],case))


def archived_record(root,h):
    rel=HIST+"evidence/validated/run-37075311542-attempt-1/shard-0/original.zip.part0000"
    path=root/DEMOS/rel
    archive_hash=sha256(path.read_bytes()).hexdigest()
    need(archive_hash=="ace5305518cf102ca15d8e48b0d7b8df4735672d311ad40bfccea339df205b97","historical ZIP")
    line=56732
    with ZipFile(path) as z, z.open("scientific/RECORDS.jsonl.gz") as source, gzip.GzipFile(fileobj=source) as stream:
        raw=next(islice(stream,line-1,line))
    record=json.loads(raw)
    rows=[[j] for j in range(6)]+[[0]]
    case=h["u54"].case("M1","layers",6,[1]*7,3,rows,{"peak":6})
    rebuilt=h["m54"].produce(case)
    need(h["v54"].verify_record(case,rebuilt)==[] and rebuilt==record,"archived row identity")
    need((json.dumps(rebuilt,sort_keys=True,separators=(",",":"))+"\n").encode()==raw,"archived record bytes")
    return dict(archive=rel,zip_sha256=archive_hash,line=line,record_sha256=sha256(raw).hexdigest(),
                run=layers(h,tuple(map(frozenset,rows)),6,3,case))


def summaries(records):
    ans={}
    for q,sizes,pi,prior,arms in records:
        key=str(q)+"_"+"".join(map(str,sizes))
        tally=ans.setdefault(key,Counter())
        tally["preparations"]+=1
        for v,arm in enumerate(arms,1):
            tally["arms"]+=1
            cmds=arm["repairs"]
            k=q+2
            cut_kept=[n for n in cmds if n!=(v-1)*k+pi[3]+1]
            tally["all_spell_released_leaf"]+=all((n-1)//k+1==v for n in cmds)
            tally["unique_with_cut_kept"]+=len(cut_kept)==1
            dst,donor,first=arm["run"]["legs"][0][0]
            tally["forward_one_edit"]+=len(first)==1
            tally["forward_single_to_designated_R"]+=first==[(v-1)*k+pi[0]+1]
    return ans


if __name__=="__main__":
    root,out=map(Path,sys.argv[1:])
    h=historical(root.resolve())
    cases=family(h)
    budget,stats=budget_universe(h,atom)
    raw=(json.dumps({"primary":cases,"budget":budget},separators=(",",":"))+"\n").encode()
    cert=dict(schema=1,preparations=len(cases),arms=2*len(cases),counts=summaries(cases),
              original_six=six(h),named={str(q):controls(h,q) for q in (2,3)},original_m1=archive_control(h),
              raw_sha256=sha256(raw).hexdigest(),archived_record=archived_record(root,h),budget=stats)
    out.mkdir(parents=True,exist_ok=True)
    (out/"cover_return_universe.json.xz").write_bytes(lzma.compress(raw))
    (out/"cover_return_certificate.json").write_text(json.dumps(cert,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:cert[k] for k in ("preparations","arms","raw_sha256")}))
