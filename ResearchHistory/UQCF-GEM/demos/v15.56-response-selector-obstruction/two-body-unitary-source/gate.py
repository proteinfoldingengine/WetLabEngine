"""Frozen v15.73: specified unitary support transfer, not derived interaction."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('memory71_unitary',HERE.parent/'memory-enriched-null'/'gate.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
S,ETA,P_MIX=1e-3,1e-4,.37
THRESHOLDS=[1e-9,1e-10,1e-11]
SOURCE_LABELS={w:[x for x in itertools.product(range(4),repeat=3) if sum(a!=0 for a in x)==w] for w in [1,2]}

def response(p,h):return -.5j*(p@h-h@p)
def unitary(p,s):return np.cos(s/2)*np.eye(8)-1j*np.sin(s/2)*p
def channel(u,z):return u@z@u.conj().T
def skew_coords(q):return np.array([q[0,1]-q[1,0],q[0,2]-q[2,0],q[1,2]-q[2,1]])/np.sqrt(2)
def ranks(a,reference):
    sv=np.linalg.svd(a,compute_uv=False)
    return [int(np.sum(sv>r*reference)) for r in THRESHOLDS]
def spectrum(a,ref):return {'singular_values':np.linalg.svd(a,compute_uv=False).tolist(),'ranks':ranks(a,ref)}
def adjudicate(valid,passed):
    if not valid:return 'INVALID'
    return 'TWO_BODY_UNITARY_HIDDEN_ROTATION_'+('CONFIRMED' if passed else 'NOT_CONFIRMED')

def run_measurement():
    controls={k:0. for k in ['unitarity','mixture_affinity','centered_identity','centered_truncation','sylvester','exterior_invariance','trace_error','hermiticity_error']}
    controls.update({k:float('inf') for k in ['min_activity','min_density_eigenvalue','min_edge_singular','min_positive_polar']})
    rows=[];cases=0;domain_ok=True;scientific=True
    try:
        selected=M.V70.V64.ASYM.select_states()
        indices=[r['candidate_index'] for r in selected]
        if indices!=M.EXPECTED:raise ValueError('frozen selection mismatch')
        for state in selected:
            rho=state['rho'];one=M.moments(rho,M.ONE).reshape(3,3)
            cs=M.correlations(rho);ops=[M.polar(c) for c in cs]
            maps={};details=[]
            for weight in [2,1]:
                matrices=[[],[],[]]
                for label in SOURCE_LABELS[weight]:
                    p=M.F.op(*label);up=unitary(p,S);um=unitary(p,-S)
                    controls['min_activity']=min(controls['min_activity'],float(np.linalg.norm(response(p,rho))))
                    controls['unitarity']=max(controls['unitarity'],*(float(np.linalg.norm(u.conj().T@u-np.eye(8))) for u in [up,um]))
                    block=[[],[],[]];norms=[];edge_leak=0.
                    support=[i for i,a in enumerate(label) if a]
                    source_edge=next((e for e,ij in enumerate(M.EDGES) if set(ij)==set(support)),None)
                    for h in M.HIDDEN:
                        y=response(p,h);yn=float(np.linalg.norm(y));norms.append(yn)
                        finite=(channel(up,h)-channel(um,h))/(2*S)
                        controls['centered_identity']=max(controls['centered_identity'],float(np.linalg.norm(finite-np.sin(S)/S*y)))
                        controls['centered_truncation']=max(controls['centered_truncation'],float(np.linalg.norm(finite-y))/max(1.,yn))
                        dyone=M.moments(y,M.ONE).reshape(3,3)
                        leak=M.moments(y,M.PAIR);pair=leak.reshape(3,3,3)
                        qs=[];es=[]
                        for e,(i,j) in enumerate(M.EDGES):
                            dc=pair[e]-np.outer(dyone[i],one[j])-np.outer(one[i],dyone[j])
                            o,pos,_=ops[e];q=o.T@dc-dc.T@o
                            w=o.T@M.polar_derivative(cs[e],dc)
                            controls['sylvester']=max(controls['sylvester'],float(np.linalg.norm(pos@w+w@pos-q)))
                            qs.extend(skew_coords(q));es.extend(skew_coords(w))
                        for dest,value in zip(block,[leak,qs,es]):dest.append(value)
                        if weight==2:edge_leak=max(edge_leak,float(np.linalg.norm(M.V70.restrict(y,M.EDGES[source_edge]))))
                        a=rho+ETA*h;b=rho-ETA*h
                        evolved=[channel(u,z) for u in [up,um] for z in [a,b]]
                        dm=M.domain([a,b]+evolved);domain_ok=domain_ok and dm['valid']
                        for key in ['min_density_eigenvalue','min_edge_singular','min_positive_polar']:controls[key]=min(controls[key],dm[key])
                        for key in ['trace_error','hermiticity_error']:controls[key]=max(controls[key],dm[key])
                        for u in [up,um]:
                            defect=channel(u,P_MIX*a+(1-P_MIX)*b)-P_MIX*channel(u,a)-(1-P_MIX)*channel(u,b)
                            controls['mixture_affinity']=max(controls['mixture_affinity'],float(np.linalg.norm(defect)))
                            if weight==2:
                                exterior=[i for i in range(3) if i not in support]
                                for z in [a,b]:controls['exterior_invariance']=max(controls['exterior_invariance'],float(np.linalg.norm(M.V70.restrict(channel(u,z)-z,exterior))))
                        cases+=1
                    block=[np.array(a).T for a in block]
                    for dest,value in zip(matrices,block):dest.append(value)
                    if weight==2:details.append({'label':list(label),'source_edge':source_edge,'Y_norms':norms,'source_edge_marginal_max':edge_leak,'blocks':block})
                maps[weight]=[np.concatenate(a,axis=1) for a in matrices]
            refs=[float(np.linalg.svd(a,compute_uv=False)[0]) for a in maps[2]]
            aggregate={name:spectrum(a,ref) for name,a,ref in zip(['leakage','Q','E'],maps[2],refs)}
            local={name:dict(spectrum(a,ref),relative_norm=float(np.linalg.norm(a)/np.linalg.norm(b))) for name,a,b,ref in zip(['leakage','Q','E'],maps[1],maps[2],refs)}
            scientific=scientific and all(aggregate[k]['ranks']==[n]*3 for k,n in [('leakage',27),('Q',9),('E',9)])
            scientific=scientific and all(x['ranks']==[0]*3 and x['relative_norm']<=1e-10 for x in local.values())
            for d in details:
                block=d.pop('blocks')
                d['maps']={name:spectrum(a,ref) for name,a,ref in zip(['leakage','Q','E'],block,refs)}
                d['edge_Q_ranks']=[ranks(block[1][3*e:3*e+3],refs[1]) for e in range(3)]
                d['edge_E_ranks']=[ranks(block[2][3*e:3*e+3],refs[2]) for e in range(3)]
                active=[n for n in d['Y_norms'] if n>1e-10]
                ok=len(active)==12 and all(abs(n-1)<=1e-12 for n in active) and d['source_edge_marginal_max']<=1e-12
                ok=ok and all(d['maps'][k]['ranks']==[n]*3 for k,n in [('leakage',12),('Q',6),('E',6)])
                ok=ok and all(d[k][e]==[0 if e==d['source_edge'] else 3]*3 for k in ['edge_Q_ranks','edge_E_ranks'] for e in range(3))
                d['pass']=bool(ok);scientific=scientific and ok
            rows.append({'candidate_index':state['candidate_index'],'aggregate':aggregate,'local':local,'sources':details,'aggregate_Q':maps[2][1].tolist(),'aggregate_E':maps[2][2].tolist()})
        valid=domain_ok and cases==11664 and len(rows)==12 and controls['min_activity']>1e-8
        valid=valid and all(controls[k]<=t for k,t in [('unitarity',1e-12),('mixture_affinity',1e-12),('centered_identity',1e-10),('centered_truncation',1e-6),('sylvester',1e-10),('exterior_invariance',1e-12)])
        report={'candidate_indices':indices,'probe_cases':cases,'states':rows,'controls':controls,'all_valid':bool(valid),'scientific_pass':bool(scientific),'verdict':adjudicate(valid,scientific),'s':S,'eta':ETA,'mixture_weight':P_MIX,'rank_thresholds':THRESHOLDS,'source_labels':SOURCE_LABELS,'hidden_labels':M.LABELS}
        return M.V70.finalize_report(report)
    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
        return M.V70.finalize_report({'verdict':'INVALID','all_valid':False,'error':str(exc),'controls':controls,'states':rows,'probe_cases':cases})

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(2 if result['verdict']=='INVALID' else 0)
