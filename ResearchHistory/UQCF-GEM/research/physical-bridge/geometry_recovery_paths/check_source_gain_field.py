"""Replay archived push, solve and fiber-mean field calls on a provenance-checked one-leaf P1 fiber."""
from contextlib import ExitStack
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
from check_receiver_command import hash_blob


DRIVER=Path("ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/pruning_response.py")
PIN="937325efc761d988d3cf34eb3378035a610e0773"
EPS=1e-8


def centered(seq):
    mean=sum(seq,F(0))/len(seq)
    return tuple(x-mean for x in seq)


def exact_solve(keys,source):
    """Rooted tree flow gives one potential; verify the defining linear equations at every vertex."""
    index={key:i for i,key in enumerate(keys)}
    j=centered(source)
    flow=list(j)
    ordered=sorted(range(1,len(keys)),key=lambda i:len(keys[i]),reverse=True)
    for i in ordered:
        flow[index[keys[i][:-1]]]+=flow[i]
    phi=[F(0)]*len(keys)
    for i in reversed(ordered):
        phi[i]=phi[index[keys[i][:-1]]]+flow[i]
    residual=[F(0)]*len(keys)
    for i in ordered:
        p=index[keys[i][:-1]]
        d=phi[i]-phi[p]
        residual[i]+=d
        residual[p]-=d
    assert tuple(residual)==j
    return centered(phi)


def exact_discrepancy(a,b):
    def decimal(v):
        return Decimal(v.numerator)/Decimal(v.denominator)
    ab=sum(x*y for x,y in zip(a,b,strict=True))
    aa=sum(x*x for x in a)
    bb=sum(y*y for y in b)
    with localcontext() as ctx:
        ctx.prec=70
        value=(2-2*decimal(ab)/(decimal(aa)*decimal(bb)).sqrt()).sqrt()
        return f"{value:.12f}"


def original_trace(m):
    refs={}
    passed=dict(push_into_coarse_solve=0,fine_solve_into_mean=0,mean_into_ray=0)
    push,solve,average,ray=m.push,m.solve,m.aggregate,m.ray
    def get_push(*a):
        refs["push"]=push(*a)
        return refs["push"]
    def get_solve(keys,j):
        answer=solve(keys,j)
        if j is refs.get("push"):
            passed["push_into_coarse_solve"]+=1
        else:
            refs["fine"]=answer
        return answer
    def get_mean(phi,*args):
        assert phi is refs["fine"]
        passed["fine_solve_into_mean"]+=1
        refs["average"]=average(phi,*args)
        return refs["average"]
    def get_ray(arr):
        if arr is refs.get("average"):
            passed["mean_into_ray"]+=1
        return ray(arr)
    with ExitStack() as stack:
        for key,fn in (("push",get_push),("solve",get_solve),("aggregate",get_mean),("ray",get_ray)):
            stack.enter_context(patch.object(m,key,fn))
        baseline=m.run()
    assert baseline["case_count"]==4 and all(v==4 for v in passed.values())
    return dict(routes=passed,cases=baseline["case_count"],verdict=baseline["verdict"])


def run(sources,science,universe,output,log):
    driver_path=sources/DRIVER
    assert hash_blob(driver_path.read_bytes())==PIN and np.__version__=="2.3.5"
    assert sha256(science.read_bytes()).hexdigest()=="b145501196e180109ed3a688b84fd5f8851e26e99fde1e3b074313cec455a2d5"
    reference=json.loads(science.read_bytes())
    payload=lzma.decompress(universe.read_bytes())
    assert sha256(payload).hexdigest()==reference["universe_sha256"]
    data=json.loads(payload)
    spec=importlib.util.spec_from_file_location("v1556_response",driver_path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    bundle=data["source_carriers"]
    fine,coarse=(tuple(map(tuple,bundle[k])) for k in ("before","after"))
    lost,=set(fine)-set(coarse)
    assert lost==(1,) and fine[0]==coarse[0]==()
    at={k:i for i,k in enumerate(fine)}
    retained=[at[k] for k in coarse]
    assert len(fine)==len(coarse)+1
    t=at[lost]
    out=dict(driver_blob=PIN,legacy_examples=original_trace(m),coarse_keys=len(coarse),
             fine_keys=len(fine),lost_key=lost,tolerance="1e-8",cases={})
    base=None
    logs={}
    for name in ("archive","low5","high5","low17","high17"):
        case=data["cases"][name]
        s=F(reference["cases"][name]["source_gain"])
        before,after=(tuple(map(F,case[k])) for k in ("before_p1","after_p1"))
        # Confirm exact carrier, ordering and all post-P1 coordinates from the main certificate.
        typed=sha256(json.dumps([bundle["genesis"],coarse,list(map(str,after))],
                                 separators=(",",":"),sort_keys=True).encode()).hexdigest()
        assert typed==reference["cases"][name]["typed_source_sha256"]
        pf=exact_solve(fine,before)
        pc=exact_solve(coarse,after)
        restrict=centered([pf[i] for i in retained])
        means=[pf[i] for i in retained]
        means[0]=(pf[0]+pf[t])/2
        pa=centered(means)
        if base is None:
            base=(pf,pc,restrict,pa)
        d=s-2
        assert tuple(x-y for x,y in zip(pf,base[0],strict=True))==centered([d if i==t else F(0) for i in range(len(fine))])
        assert pc==base[1] and restrict==base[2]
        assert tuple(x-y for x,y in zip(pa,base[3],strict=True))==centered([d/2]+[F(0)]*(len(coarse)-1))
        # An unequal pair of nonroot values rules out collinearity with the centered root basis.
        i=1
        j=next(k for k in range(2,len(coarse)) if base[3][k]!=base[3][i])
        ratio=pa[i]-pa[j]
        assert ratio==base[3][i]-base[3][j] and ratio
        j0=np.array(before,dtype=np.float64)
        n_pf=m.solve(fine,j0)
        j1=m.push(j0,fine,coarse)
        n_pc=m.solve(coarse,j1)
        n_pa=m.aggregate(n_pf,fine,coarse)
        n_restrict=n_pf[retained].copy()
        n_restrict-=n_restrict.mean()
        n_m=float(np.linalg.norm(m.ray(n_pa)-m.ray(n_pc)))
        exact_m=exact_discrepancy(pa,pc)
        errors={label:float(np.max(np.abs(n-np.array(q,dtype=np.float64)))) for label,n,q in (
            ("fine",n_pf,pf),("push",j1,after),("coarse",n_pc,pc),("mean",n_pa,pa),("restriction",n_restrict,restrict))}
        errors["discrepancy"]=abs(n_m-float(exact_m))
        assert all(v<EPS for v in errors.values()),(name,errors)
        logs[name]=dict(observed_discrepancy=n_m,maximum_absolute_errors=errors)
        out["cases"][name]=dict(source_gain=str(s),fine_leaf_contrast_change=str(d),
                         coarse_root_contrast_change="0",restricted_root_contrast_change="0",
                         mean_root_contrast_change=str(d/2),normalized_mean_changed=bool(d),
                         projective_discrepancy=exact_m)
    out["nonroot_witness_keys"]=[coarse[i],coarse[j]]
    assert len(set(v["projective_discrepancy"] for v in out["cases"].values()))==len(out["cases"])
    output.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    log.write_text(json.dumps(logs,sort_keys=True,indent=2)+"\n")
    return out


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Enable proof assertions")
    result=run(*(Path(a).resolve() for a in sys.argv[1:]))
    print(json.dumps({k:v["mean_root_contrast_change"] for k,v in result["cases"].items()}))
