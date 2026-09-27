"""v15.80: signed-source CPTP tangent lineality, with an even-source control."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('couplings79_signed',HERE.parent/'covariant-source-couplings'/'gate.py')
V79=importlib.util.module_from_spec(spec);spec.loader.exec_module(V79)
V78=V79.V78;V75=V79.V75;M=V79.M
BASIS=V78.BASIS;V=BASIS.reshape(64,64).T
OMEGA=np.eye(8).ravel()/np.sqrt(8);P=np.eye(64)-np.outer(OMEGA,OMEGA)
SUPPORTS=V79.SUPPORTS;ALL_SUPPORTS=[()]+SUPPORTS
ALLOWED={(0,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1)}
EPS=.1;THRESHOLDS=[1e-9,1e-10,1e-11]


def local_tensor(s,i,o):
    t=np.zeros((3 if o else 1,3 if s else 1,3 if i else 1))
    if (s,i,o)==(0,0,0):t[0,0,0]=1
    elif (s,i,o)==(0,1,1):t[:,0,:]=np.eye(3)
    elif (s,i,o)==(1,0,1):t[:,:,0]=np.eye(3)
    elif (s,i,o)==(1,1,0):t[0,:,:]=np.eye(3)
    elif (s,i,o)==(1,1,1):t=V79.local_tensor(True,True)
    return t


def enumerate_labels():
    labels=[]
    for s in SUPPORTS:
        for i in ALL_SUPPORTS:
            for o in ALL_SUPPORTS:
                if all((int(q in s),int(q in i),int(q in o)) in ALLOWED for q in range(3)):
                    k=len(set(s)&set(i)&set(o))
                    norm2=float(np.prod([np.linalg.norm(local_tensor(int(q in s),int(q in i),int(q in o)))**2 for q in range(3)]))
                    labels.append({'source':s,'input':i,'output':o,'crosses':k,'norm2':norm2})
    return labels


def ptm_tensor(label,source):
    factors=[]
    for q in range(3):
        s=int(q in label['source']);i=int(q in label['input']);o=int(q in label['output'])
        t=local_tensor(s,i,o);small=t[:,source[q]-1 if s else 0,:]
        a=np.zeros((4,4));outs=list(range(1,4)) if o else [0];ins=list(range(1,4)) if i else [0]
        a[np.ix_(outs,ins)]=small;factors.append(a)
    return np.kron(np.kron(factors[0],factors[1]),factors[2])


def choi_from_ptm(l):
    comp=V@l@V.conj().T
    return comp.reshape(8,8,8,8).transpose(2,0,3,1).reshape(64,64)


def spectrum(a):
    sv=np.linalg.svd(a,compute_uv=False)
    ref=float(sv[0]) if len(sv) else 0.
    return {'shape':list(a.shape),'singular_values':sv.tolist(),
            'ranks':[int(np.count_nonzero(sv>t*ref)) for t in THRESHOLDS],
            'norm':float(np.linalg.norm(a))}


def column_projector(a):
    if not a.shape[1]:return np.zeros((a.shape[0],a.shape[0]))
    u,sv,_=np.linalg.svd(a,full_matrices=False);keep=sv>1e-10*sv[0]
    return u[:,keep]@u[:,keep].T


def right_kernel(a):
    _,sv,vh=np.linalg.svd(a,full_matrices=False)
    return vh[sv<=1e-10*sv[0]].T


def local_dimensions():
    rows=[];res=0.;pe=0.
    for s,i,o in itertools.product((0,1),repeat=3):
        ds=3 if s else 1;di=3 if i else 1;do=3 if o else 1;blocks=[]
        for j in V79.generators():
            js=j if s else np.zeros((1,1));ji=j if i else np.zeros((1,1));jo=j if o else np.zeros((1,1))
            input_j=np.kron(js,np.eye(di))+np.kron(np.eye(ds),ji)
            blocks.append(np.kron(jo,np.eye(ds*di))-np.kron(np.eye(do),input_j.T))
        a=np.concatenate(blocks);_,sv,vh=np.linalg.svd(a,full_matrices=False);ref=float(sv[0])
        null=vh[sv<=1e-10*ref].T;res=max(res,float(np.linalg.norm(a@null)))
        t=local_tensor(s,i,o).ravel();expected=np.outer(t,t)/(t@t) if t@t else np.zeros((len(t),len(t)))
        pe=max(pe,float(np.linalg.norm(null@null.T-expected)))
        rows.append({'triple':[s,i,o],'nullities':[int(np.count_nonzero(sv<=z*ref)) for z in THRESHOLDS],'singular_values':sv.tolist()})
    return rows,res,pe


def adjudicate(valid,primary,secondary):
    if not valid:return 'INVALID','INVALID'
    return ('SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_CONFIRMED' if primary else 'SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_NOT_CONFIRMED',
            'SIGNED_CPTP_RETAINED_IMAGE_FOUR_CONFIRMED' if secondary else 'SIGNED_CPTP_RETAINED_IMAGE_FOUR_NOT_CONFIRMED')


def run_measurement():
    c={};mx=lambda k,v:V78.V77.maximize(c,k,v)
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    domain=M.domain([r['rho'] for r in selected]);local,lr,lp=local_dimensions()
    mx('local_kernel_residual',lr);mx('local_projector_error',lp)
    all_labels=enumerate_labels();labels=[x for x in all_labels if x['output']]
    nb=len(labels);b18,lab18=V79.build_tensors();projection=np.zeros((18,nb));hcoeff=np.zeros((nb,7))
    for ci,lab in enumerate(labels):
        si=SUPPORTS.index(lab['source']);k=lab['crosses']
        hcoeff[ci,si]=0 if k%2==0 else (1 if k==1 else -1)
        if lab['input']==(0,1,2):
            for j,t in enumerate(lab18):
                if tuple(t['source_support'])==lab['source'] and tuple(t['target_support'])==lab['output']:projection[j,ci]=1
    blocks=[];kernel_columns=[];unitary_cp=[];direct_hidden=np.zeros((63,27,36))
    for support in SUPPORTS:
        ci=[j for j,x in enumerate(labels) if x['source']==support];bl=[labels[j] for j in ci]
        full_bl=[x for x in all_labels if x['source']==support]
        admitted=[j for j,x in enumerate(full_bl) if x['output']]
        source_ids=[j for j,p in enumerate(V79.SLABELS) if tuple(q for q,x in enumerate(p) if x)==support]
        constraints=[];gram=np.zeros((len(full_bl),len(full_bl)));hs=hcoeff[ci,SUPPORTS.index(support)]
        for source_number,si in enumerate(source_ids):
            p=V79.SLABELS[si];source=M.F.op(*p)
            full_ls=np.array([ptm_tensor(x,p) for x in full_bl]);ls=full_ls[admitted]
            gram+=np.einsum('cij,dij->cd',full_ls,full_ls)
            mx('trace_row',np.max(np.abs(ls[:,0,:])))
            js=np.array([choi_from_ptm(l) for l in ls])
            for j,l in zip(js,ls):
                mx('Choi_hermiticity',np.linalg.norm(j-j.conj().T));mx('Choi_trace_annihilation',np.linalg.norm(V75.trace_output(j)))
                if source_number==0:mx('Choi_reshuffle',np.linalg.norm(j-V75.choi(lambda z:V78.apply_ptm(l,z))))
            ks=P@js@P
            constraints.append(np.concatenate([ks.real.reshape(len(ci),-1),ks.imag.reshape(len(ci),-1)],axis=1).T)
            combined=np.einsum('c,cij->ij',hs,ls)
            direct=V78.transfer(lambda z:-.5j*(source@z-z@source))
            mx('Hamiltonian_reconstruction',np.max(np.abs(combined-direct)))
            mx('Hamiltonian_conditional_Choi',np.linalg.norm(P@choi_from_ptm(combined)@P))
            direct_hidden[si]=combined[np.ix_(V79.RIDX,V79.HIDX)].T
            predicted=np.einsum('jc,jhr->crh',projection[:,ci],b18[:,si])
            mx('retained_projection',np.max(np.abs(ls[:,V79.RIDX][:,:,V79.HIDX]-predicted)))
            for sign in [1,-1]:
                u=np.cos(EPS/2)*np.eye(8)-1j*sign*np.sin(EPS/2)*source
                mx('unitarity',np.linalg.norm(u.conj().T@u-np.eye(8)))
                cp=V75.cp_diagnostics(V75.choi(lambda z:u@z@u.conj().T))
                unitary_cp.append({'source_label':list(p),'sign':sign,**cp})
        a=np.concatenate(constraints);info=spectrum(a);_,sv,vh=np.linalg.svd(a,full_matrices=False)
        null=vh[sv<=1e-10*sv[0]].T;projector=null@null.T;expected=np.outer(hs,hs)/(hs@hs)
        pe=float(np.linalg.norm(projector-expected));info.update(source_support=list(support),coefficient_indices=ci,
             nullities=[len(ci)-v for v in info['ranks']],kernel_projector=projector.tolist(),Hamiltonian_projector_error=pe)
        blocks.append(info)
        for col in null.T:
            z=np.zeros(nb);z[ci]=col;kernel_columns.append(z)
        mx('basis_Gram',np.linalg.norm(gram-np.diag([x['norm2'] for x in full_bl])))
    kernel=np.array(kernel_columns).T if kernel_columns else np.zeros((nb,0))
    image=projection@kernel;canonical=projection@hcoeff;image_info=spectrum(image)
    image_error=float(np.linalg.norm(column_projector(image)-column_projector(canonical)))
    projected_hidden=np.einsum('cj,cshr->jshr',canonical,b18,optimize=True)
    mx('Hamiltonian_hidden_reconstruction',np.max(np.abs(projected_hidden.sum(axis=0)-direct_hidden)))
    sw=np.array([(-1.)**j/(j+1) for j in range(63)]);hw=np.array([(-1.)**j/(j+1) for j in range(27)])
    states=[];qs=[];es=[]
    for rec in selected:
        q,e,sy,aq,ae=V79.maps(rec['rho'],b18,sw,hw)
        mx('sylvester',sy);mx('assembly_Q',aq);mx('assembly_E',ae)
        q=q@canonical;e=e@canonical;qs.append(q);es.append(e)
        states.append({'candidate_index':rec['candidate_index'],'Q':spectrum(q),'E':spectrum(e)})
    stacked={};expected_local=np.diag([1.,1.,1.,0.,0.,0.,0.])
    for key,rows in [('Q',qs),('E',es)]:
        a=np.concatenate(rows);k=right_kernel(a);d=spectrum(a)
        d['kernel_projector']=(k@k.T).tolist();d['local_kernel_projector_error']=float(np.linalg.norm(k@k.T-expected_local));stacked[key]=d
    # Physical quadratic/even-source control, separately labelled from -D.
    source=(M.F.op(3,0,0)+M.F.op(1,1,0))/np.sqrt(2)
    mx('D_source_hermiticity',np.linalg.norm(source-source.conj().T));mx('D_source_square',np.linalg.norm(source@source-np.eye(8)))
    def dissipator(z,a=source):return a@z@a-.5*(a@a@z+z@a@a)
    dl=V78.transfer(dissipator);dj=V75.choi(dissipator);dk=P@dj@P
    mx('D_Choi_reshuffle',np.linalg.norm(choi_from_ptm(dl)-dj))
    mx('D_trace_annihilation',np.linalg.norm(V75.trace_output(dj)));mx('D_Choi_hermiticity',np.linalg.norm(dj-dj.conj().T))
    for z in BASIS:mx('D_even_source',np.linalg.norm(dissipator(z)-dissipator(z,-source)))
    eig=np.linalg.eigvalsh((dk+dk.conj().T)/2);rev=np.linalg.eigvalsh(-(dk+dk.conj().T)/2)
    mx('D_conditional_spectrum',np.linalg.norm(eig-np.array([0.]*63+[8.])));mx('D_negative_conditional_min',abs(rev[0]+8))
    def channel(z,strength):
        p=(1+np.exp(-2*strength))/2
        return p*z+(1-p)*source@z@source
    cp=V75.cp_diagnostics(V75.choi(lambda z:channel(z,EPS)))
    reverse_cp=V75.cp_diagnostics(V75.choi(lambda z:channel(z,-EPS)))
    ys=np.array([dissipator(h) for h in M.HIDDEN]);coeff=np.einsum('hij,rji->rh',ys,V75.G)
    mx('D_tangent_trace',np.max(np.abs(np.trace(ys,axis1=-2,axis2=-1))))
    mx('D_tangent_hermiticity',np.max(np.linalg.norm(ys-ys.conj().transpose(0,2,1),axis=(-2,-1))))
    for hlabel,target in [((2,2,3),-M.F.op(0,3,3)/np.sqrt(8)),((1,1,1),M.F.op(3,0,1)/np.sqrt(8))]:
        j=M.LABELS.index(hlabel);expected=np.einsum('ij,rji->r',target,V75.G)
        mx('D_witness',np.linalg.norm(coeff[:,j]-expected))
    dr=spectrum(coeff);drows=[];d_geometry=dr['ranks']==[12]*3
    for rec in selected:
        q,e,sy=V78.V77.extract(rec['rho'],ys);mx('sylvester',sy)
        row={'candidate_index':rec['candidate_index'],'Q':spectrum(q),'E':spectrum(e),'edges':[]}
        d_geometry=d_geometry and row['Q']['ranks']==[6]*3 and row['E']['ranks']==[6]*3
        for edge in range(3):
            qe=q[3*edge:3*edge+3];ee=e[3*edge:3*edge+3]
            if edge==0:
                d_geometry=d_geometry and np.linalg.norm(qe)<=1e-12*np.linalg.norm(q) and np.linalg.norm(ee)<=1e-12*np.linalg.norm(e)
            else:d_geometry=d_geometry and spectrum(qe)['ranks']==[3]*3 and spectrum(ee)['ranks']==[3]*3
            row['edges'].append({'edge':list(M.EDGES[edge]),'Q':spectrum(qe),'E':spectrum(ee)})
        drows.append(row)
    d_valid=(d_geometry and cp['valid'] and reverse_cp['min_eigenvalue']<=-.1 and reverse_cp['hermiticity_error']<=1e-12 and reverse_cp['TP_error']<=1e-12)
    primary=(all(x['nullities']==[n]*3 for x,n in zip(local,[1,0,0,1,0,1,1,1])) and len(all_labels)==117 and nb==110
             and [len(x['coefficient_indices']) for x in blocks]==[11,11,11,17,17,17,26]
             and all(x['nullities']==[1]*3 and x['Hamiltonian_projector_error']<=1e-9 for x in blocks)
             and [sum(x['ranks'][i] for x in blocks) for i in range(3)]==[103]*3)
    secondary=(image_info['ranks']==[4]*3 and image_error<=1e-9 and all(d['ranks']==[4]*3 and d['local_kernel_projector_error']<=1e-9 for d in stacked.values()))
    limits={key:1e-12 for key in ['local_kernel_residual','trace_row','Choi_hermiticity','Choi_trace_annihilation','Choi_reshuffle','Hamiltonian_reconstruction','Hamiltonian_conditional_Choi','retained_projection','unitarity','Hamiltonian_hidden_reconstruction','D_source_hermiticity','D_source_square','D_Choi_reshuffle','D_trace_annihilation','D_Choi_hermiticity','D_even_source','D_tangent_trace','D_tangent_hermiticity','D_witness']}
    limits.update(local_projector_error=1e-10,basis_Gram=1e-10,sylvester=1e-11,assembly_Q=1e-10,assembly_E=1e-10,D_conditional_spectrum=1e-11,D_negative_conditional_min=1e-11)
    valid=(indices==M.EXPECTED and domain['valid'] and d_valid and all(x['valid'] for x in unitary_cp) and all(c[k]<=v for k,v in limits.items()))
    c['dissipator_control_valid']=bool(d_valid);c['unitary_CP_valid']=all(x['valid'] for x in unitary_cp)
    verdict,retained=adjudicate(valid,primary,secondary)
    report={'version':'15.80','candidate_indices':indices,'source_count':63,'all_valid':bool(valid),'verdict':verdict,'retained_verdict':retained,
            'controls':c,'domain':domain,'local':local,'full_dimension':len(all_labels),'trace_annihilating_dimension':nb,
            'coefficient_labels':[{k:list(v) if isinstance(v,tuple) else v for k,v in x.items()} for x in labels],
            'blocks':blocks,'total_constraint_ranks':[sum(x['ranks'][i] for x in blocks) for i in range(3)],
            'kernel_dimension':int(kernel.shape[1]),'retained_image':{**image_info,'projector_error':image_error,'canonical_coefficients':canonical.tolist()},
            'states':states,'stacked':stacked,'unitary_Choi':unitary_cp,
            'dissipator':{'conditional_eigenvalues':eig.tolist(),'negative_conditional_eigenvalues':rev.tolist(),'positive_strength_Choi':cp,'negative_strength_Choi':reverse_cp,'retained':dr,'states':drows}}
    report=M.V70.finalize_report(report)
    if not report['all_valid']:report['retained_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False))
    sys.exit(0 if result['all_valid'] else 2)
