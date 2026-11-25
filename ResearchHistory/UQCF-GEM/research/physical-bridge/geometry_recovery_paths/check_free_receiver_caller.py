"""Trace the actual single-state v16.44 normalizer and its original campaign separately."""
import ast
from hashlib import sha1
import importlib
from itertools import permutations
from pathlib import Path
import sys
from free_receiver_io import ATOM, DEMOS, P1, TWO, module, require, write_xz


def audit_sources(root):
    files={}
    sites=[]
    for directory in sorted((root/DEMOS).glob("v16.*-*")):
        if not 22<=int(directory.name.split("-")[0].split(".")[1])<=54:
            continue
        for path in sorted(directory.glob("*.py")):
            rel=path.relative_to(root/DEMOS).as_posix()
            raw=path.read_bytes()
            files[rel]=sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
            for fn in ast.walk(ast.parse(raw)):
                if not isinstance(fn,ast.FunctionDef):
                    continue
                # Limit traversal to calls whose nearest enclosing function is fn.
                queue=list(fn.body)
                while queue:
                    node=queue.pop()
                    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.Lambda,ast.ClassDef)):
                        continue
                    if isinstance(node,ast.Call):
                        head=node.func
                        name=getattr(head,"id",getattr(head,"attr",""))
                        if name=="atomic":
                            sites.append([rel,node.lineno,fn.name])
                    queue.extend(ast.iter_child_nodes(node))
    return dict(files=files,atomic_named_calls=sorted(sites))


def source_event(atom,p,before,cut,j):
    calls=set()
    def observe(frame,event,arg):
        if event=="call" and frame.f_back is not None and frame.f_back.f_code is atom.__code__:
            code=frame.f_code
            if not code.co_name.startswith("<"):
                calls.add((Path(code.co_filename).name,code.co_name))
    old=sys.getprofile()
    try:
        sys.setprofile(observe)
        result=atom(p,before,j,cut)
    finally:
        sys.setprofile(old)
    return result,sorted([list(x) for x in calls])


def trace_inner(producer, star, post, q):
    raw=Path(star.__file__).read_text().splitlines()
    point=next(i for i,line in enumerate(raw,1) if line.strip()=="for j in support(v):")
    clearing=next(i for i,line in enumerate(raw,1) if line.strip()=="if j!=keep:change(j,v,False)")
    original=star.normalize.__code__
    entry=[]
    supports=[]
    edits=[]
    def observe(frame,event,arg):
        parent=frame.f_back
        if event=="call" and frame.f_code.co_name=="local" and parent and parent.f_code is producer.normalize.__code__:
            a=frame.f_locals
            if len(a["leaves"])==len(a["palette"])==3:
                entry.append(len(a["path"])-1)
        if not parent or parent.f_code is not original or parent.f_locals["m"]!=3 or parent.f_locals["k"]!=3:
            return
        if event=="return" and frame.f_code.co_name=="support" and parent.f_lineno==point:
            require(frame.f_locals["s"] is parent.f_locals["s"],"support read from a copied chart list")
            supports.append(dict(tip=parent.f_locals["v"]+1,holders=arg,keeper=parent.f_locals["keep"]))
        if event=="call" and frame.f_code.co_name=="change" and parent.f_lineno==clearing:
            a=frame.f_locals
            edits.append([a["j"],a["v"]+1,a["add"]])
    old=sys.getprofile()
    try:
        sys.setprofile(observe)
        path=producer.normalize(post,2,3,3,q[0],q[1])
    finally:
        sys.setprofile(old)
    require(len(entry)==1 and len(supports)==3 and len(edits)==1,"actual cleanup trace")
    return path,dict(start=entry[0],supports=supports,edits=edits)


def produce(root,out):
    root=root.resolve()
    sys.path.insert(0,str(root/TWO))
    producer,star,verifier=(importlib.import_module(name) for name in ("producer","star_normalize","verifier"))
    atom=module(root,ATOM,"caller_atom","c10ac57f988a439144e21898bd2b33ece0838a9b").atomic
    push=module(root,P1,"caller_p1","b18f52109ccff9c7dc77542d3b8f3e5d5989102a").push
    campaign=[]
    def observer(frame,event,arg):
        if event=="call" and frame.f_code is producer.normalize.__code__:
            outer=frame.f_back
            require(outer.f_code is producer.produce.__code__,"unexpected campaign caller")
            a=outer.f_locals
            require(frame.f_locals["state"] is a["g"]["states"][a["i"]],"representative origin")
            campaign.append(a["i"])
    old=sys.getprofile()
    try:
        sys.setprofile(observer)
        doc=producer.produce(((2,3,3),))
    finally:
        sys.setprofile(old)
    receipt=verifier.verify(doc,((2,3,3),))
    g=doc["entries"][0]["graph"]
    p=tuple(g["parents"])
    require(p==(-1,0,1,1,1,0),"anchored tree")
    nodes=tuple(range(6))
    states={tuple(x):i for i,x in enumerate(g["states"])}
    reps=sorted(campaign)
    rows=[]
    for order in permutations("SHR"):
        S,H,R=map(order.index,"SHR")
        for a,b,c in permutations((2,3,4)):
            grades=[5,3,0,0,0,4]
            grades[a]=grades[b]=2
            grades[c]=1
            original=[{0,1} for j in order]
            original[S].update((a,b,c))
            original[H].update((a,5))
            original[R].add(b)
            for cut in (a,b):
                event,calls=source_event(atom,p,[sorted(x) for x in original],cut,S)
                post=tuple(sum(1<<v for v in y) for y in event["after"])
                start=states[post]
                q=g["attained_profiles"][g["profile_ids"][start]]
                path,log=trace_inner(producer,star,post,q)
                sequence=[states[tuple(v)] for v in path]
                end=states[verifier.canonical(2,3,3,q[0],q[1])]
                require(verifier.path_valid(sequence,start,end,g,q),"historical full path validation")
                component=next(comp for rec in g["profiles"] if list(rec["q"])==list(q)
                               for comp in rec["zero_components"] if start in comp)
                require(component[0] in reps,"missing original component entry")
                point=path[log["start"]+len(log["edits"])]
                retained=tuple(v for v in nodes if point[R]>>v&1)
                grade=int(push(p,nodes,retained,grades)[retained.index(1)])
                rows.append(dict(order="".join(order),abc=[a,b,c],cut="a" if cut==a else "b",
                    source_start=start,representative=component[0],actually_called=start in reps,
                    source_calls=calls,q=q,trace=log,path=path,p=grade))
    pdead=(-1,0,0,1,0)
    before=((0,1,2,3,4),(0,1),(0,2,4))
    dead=[]
    for cut in (2,4):
        first=atom(pdead,before,0,cut)
        second=atom(pdead,first["after"],1,1)
        g=(5,3,2,1,2)
        dead.append(dict(cut=cut,receiver_move=[1,1],p1_prior=list(map(int,push(pdead,tuple(range(5)),before[1],g))),
                         p1_after=list(map(int,push(pdead,tuple(range(5)),second["after"][1],g)))))
    output=dict(cases=rows,states=len(states),campaign_calls=reps,campaign_receipt=receipt,stub=dead,
                audit=audit_sources(root))
    write_xz(out/"free_receiver_caller.json.xz",output)
    print("Archived graph states",len(states),"campaign calls",len(reps),"experimental arms",len(rows),
          "selected arms",sum(r["actually_called"] for r in rows),"audited files",len(output["audit"]["files"]))


if __name__=="__main__":
    produce(Path(sys.argv[1]),Path(sys.argv[2]))
