from fractions import Fraction
from itertools import combinations
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
from hashlib import sha1,sha256
import json,os,sys

def main(reference):
    os.chdir(reference)
    p=Path('ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py')
    b=p.read_bytes()
    assert sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='3324c0b46e09120ae526338444a19070b692d049'
    spec=spec_from_file_location('original',p); h=module_from_spec(spec); spec.loader.exec_module(h)
    m=h.modules(); features,W0=h.fixture(); parent,g,_=map(tuple,zip(*features))
    grades=list(g)
    for v in reversed(range(1,len(grades))):grades[parent[v]]+=grades[v]
    q=[t*t for t in grades]; base=h.initial_state(features)
    assert W0==h.work_for(base,q)
    mu,edges=h.edges(W0); N={i:{j for j in h.LABELS if W0[i][j]==mu} for i in h.LABELS}
    def observe(w):
        return m['carriers'].build_carrier(m['projection'].Payload(h.SIDE,Fraction(1),h.LABELS,
            tuple(tuple(map(Fraction,row)) for row in w),h.edges(w)[1],()))
    def toggle(state,chart,v,sign):
        vsets=list(map(set,state)); assert (v in vsets[chart])==(sign<0); vsets[chart]^={v}
        end=tuple(tuple(sorted(row)) for row in vsets)
        hi,lo=(state,end) if sign<0 else (end,state)
        doc=m['atom'].atomic(parent,hi,chart,v); m['verify'].verify_atomic(doc)
        assert tuple(map(tuple,doc['after']))==lo
        return end
    def options(state,i,amount,low,high,first):
        r=set(state[i]); holders=[{j for j,row in enumerate(state) if v in row} for v in range(len(q))]
        result=[]
        for v in range(1,len(q)):
            if q[v]!=amount:continue
            hv=holders[v]
            if v in r:
                if len(hv)<2 or any(parent[w]==v for w in r):continue
                if high<=hv and not (low&hv):result.append((i,v,-1))
            elif not first and parent[v] in r and low<=hv and not (high&hv):
                result.append((i,v,1))
        return result
    labels=h.LABELS; observe(W0)
    pair_table=[]; far=0; signed=[]
    for i,j in combinations(labels,2):
        if j in N[i] or N[i]&N[j]:continue
        far+=1
        di={W0[i][k]-mu for k in N[j]}; dj={W0[j][k]-mu for k in N[i]}
        if len(di)==len(dj)==1:
            qi,qj=di.pop(),dj.pop()
            pair_table.append([i,j,qi,qj])
            if qi in q and qj in q:
                signed += [(i,j,qi,qj),(j,i,qj,qi)]
    keys=[()]
    for v in range(1,len(parent)): keys.append(keys[parent[v]]+(v,))
    lm=m['lineage']; full=lm.Carrier('same-endpoint-different-delivery',tuple(keys))
    def local_read(state,i,s):
        coarse=lm.Carrier(full.genesis,tuple(keys[v] for v in state[i]))
        result=dict(zip(state[i],lm.Pruning(full,coarse).aggregate(g)))
        return [str(result[0]),str(result.get(s,'absent'))]
    outcomes=[]; work_by_type={}; full_traces={}; null=[]
    for i,j,qi,qj in signed:
        for act in options(base,i,qi,N[j],N[i],False):
            split=toggle(base,*act)
            wfirst=h.work_for(split,q)
            try: observe(wfirst)
            except ValueError as err: assert str(err)=='degree_not_four'; null.append(list(act))
            else: raise AssertionError('one source edit repaired geometry')
            gets=[]
            for nxt in options(split,j,qj,N[i],N[j],False):
                end=toggle(split,*nxt); w=h.work_for(end,q)
                atlas=observe(w)
                swap={i:j,j:i}
                assert set(h.edges(w)[1])=={tuple(sorted(swap.get(x,x) for x in e)) for e in edges}
                typ='transfer' if act[-1]!=nxt[-1] else 'same_sign'
                full_traces[(act,nxt)]=(W0,wfirst,w)
                if typ in work_by_type: assert work_by_type[typ]==w
                else: work_by_type[typ]=w
                field=tuple(Fraction(k==0)-Fraction(1,len(labels)) for k in labels)
                ev=m['application'].evaluate_field(atlas,field)
                loop=str(next(x for face,_,x in ev.records if set(face)==set(h.FACE)))
                gets.append([list(nxt),local_read(base,j,act[1]),local_read(split,j,act[1]),local_read(end,j,act[1]),loop])
            outcomes.append([list(act),gets])
    distinct=[[i,j,work_by_type['transfer'][i][j],work_by_type['same_sign'][i][j]] for i,j in combinations(labels,2)
              if work_by_type['transfer'][i][j]!=work_by_type['same_sign'][i][j]]
    digest=lambda a:sha256(json.dumps(a,separators=(',',':')).encode()).hexdigest()
    traces=[]
    for (a,b),ws in sorted(full_traces.items()):
        involution=lambda r:(r[0],3-r[1],-r[2])
        assert (involution(a),involution(b)) in full_traces
        assert full_traces[(involution(a),involution(b))]==ws
        traces.append([list(a),list(b),[digest(w) for w in ws]])
    print(json.dumps({'initial':W0,'mu':mu,'far':far,'constant_pair_defects':pair_table,'outcomes':outcomes,
                      'null':null,'traces':traces,'directions_match_full_work':sorted(work_by_type),'type_matrix_diffs':distinct},
                      sort_keys=True,separators=(',',':')))
if __name__=='__main__': main(Path(sys.argv[1]).resolve())
