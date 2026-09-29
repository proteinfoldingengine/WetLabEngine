"""Independent reconstruction: parent-stepping, Prüfer trees, rooted solves, SymPy.

Does not import producer, lineage, enumeration, or the inherited Fraction routines.
"""
from __future__ import annotations
import copy
import hashlib
import itertools
import json
import lzma
from pathlib import Path
import re
import traceback
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE='10e12fd2f178a03da5daedd4fb15af1cd94d1299'
HISTORICAL=(
    (((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)),((),(0,),(1,))),
    (((),(0,),(0,0),(0,1),(0,0,0),(0,0,1)),((),(0,),(0,0))),
    (((),(0,),(1,),(2,),(1,0),(1,1),(2,0)),((),(0,),(1,),(2,))),
    (((),(0,),(1,),(0,0),(0,0,0),(1,0),(1,0,0)),((),(0,),(1,),(0,0),(1,0))),
)

class VerificationError(ValueError): pass

def need(condition, why):
    if not condition: raise VerificationError(why)

def eq(left,right,why):
    need(left==right,why)

def fields(obj,names):
    need(isinstance(obj,dict) and set(names)<=set(obj),'missing required field: '+str(set(names)-set(obj) if isinstance(obj,dict) else names))

def keys(raw):
    need(isinstance(raw,(tuple,list)) and len(raw)>0,'empty or malformed carrier')
    out=[]
    for x in raw:
        need(isinstance(x,(tuple,list)) and all(type(t) is int and t>=0 for t in x),'malformed address')
        out.append(tuple(x))
    need(len(set(out))==len(out) and () in out,'duplicate address or missing root')
    need(all(not x or x[:-1] in out for x in out),'missing ancestor')
    return tuple(out)

def rational(s):
    need(isinstance(s,str) and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?',s) is not None,'non-exact scalar encoding')
    return sp.Rational(s)

def matrix(raw,n,m):
    need(isinstance(raw,list) and len(raw)==n and all(isinstance(r,list) and len(r)==m for r in raw),'matrix dimensions')
    return sp.Matrix(n,m,[rational(v) for row in raw for v in row])

def vec(raw,n):
    need(isinstance(raw,list) and len(raw)==n,'vector dimension')
    return sp.Matrix(n,1,[rational(x) for x in raw])

def parent_image(x, target):
    while x not in target:
        need(bool(x),'no retained ancestor')
        x=x[:-1]
    return x

def model(ks):
    n=len(ks); L=sp.zeros(n)
    for child in ks:
        if child:
            i,j=ks.index(child[:-1]),ks.index(child)
            L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
    Z=sp.eye(n)-sp.ones(n)/n
    indices=[i for i,k in enumerate(ks) if k]
    rooted=sp.zeros(n)
    if indices:
        inv=L.extract(indices,indices).inv()
        for i,u in enumerate(indices):
            for j,v in enumerate(indices): rooted[u,v]=inv[i,j]
    G=Z*rooted*Z
    eq(L*G,Z,'rooted Green left inverse');eq(G*L,Z,'rooted Green right inverse')
    return L,Z,G

def all_masks(ks):
    result=[]
    for n in range(1,len(ks)+1):
        for chosen in itertools.combinations(range(len(ks)),n):
            subset={ks[i] for i in chosen}
            if () in subset and all(not k or k[:-1] in subset for k in subset):
                result.append(sum(1<<i for i in chosen))
    return tuple(sorted(result))

def all_chains(masks,full,bound):
    result=set()
    for n in range(1,bound+1):
        for targets in itertools.product(masks,repeat=n):
            seq=(full,)+targets
            if all(a&b==b for a,b in zip(seq,seq[1:])):result.add(seq)
    return result

def independent_shapes(bound=5):
    found={}
    for n in range(1,bound+1):
        words=[()] if n<=2 else itertools.product(range(n),repeat=n-2)
        for word in words:
            adjacency=[set() for _ in range(n)]
            if n>1:
                degree=[1]*n
                for x in word:degree[x]+=1
                for x in word:
                    leaf=next(i for i in range(n) if degree[i]==1)
                    adjacency[leaf].add(x);adjacency[x].add(leaf)
                    degree[leaf]-=1;degree[x]-=1
                a,b=[i for i in range(n) if degree[i]==1]
                adjacency[a].add(b);adjacency[b].add(a)
            for root in range(n):
                def code(v,parent=-1):
                    return '('+''.join(sorted(code(c,v) for c in adjacency[v] if c!=parent))+')'
                signature=code(root)
                if signature in found:continue
                out=[]
                def walk(v,parent,path):
                    out.append(path)
                    for i,c in enumerate(sorted((c for c in adjacency[v] if c!=parent),key=lambda c:code(c,v))):
                        walk(c,v,path+(i,))
                walk(root,-1,());found[signature]=tuple(out)
    return dict(sorted(found.items()))

def linear_descent(T,old):
    if not isinstance(T,sp.MatrixBase) or not isinstance(old,sp.MatrixBase):
        raise TypeError('matrix-linear maps required; nonlinear representative test is different')
    need(T.cols==old.rows,'descent domain dimensions')
    return T*old==sp.zeros(T.rows,old.cols)

def check_descent(T,old,claimed):
    need(type(claimed) is bool,'descent claim must be Boolean')
    eq(linear_descent(T,old),claimed,'false fixed-target descent claim')

def check_naturality(target_change,original,source_change,relabeled):
    eq(target_change*original,relabeled*source_change,'retained naturality square fails')

def _verify_instance(obj):
    fields(obj,('tag','genesis','keys','max_arrows','carriers','prunings','chains'))
    need(isinstance(obj['genesis'],str) and bool(obj['genesis']),'Genesis identifier')
    eq(obj['genesis'],obj['tag'],'instance origin label')
    ks=keys(obj['keys']); n=len(ks);full=(1<<n)-1;bound=obj['max_arrows']
    need(type(bound) is int and 1<=bound<=3,'arrow bound')
    masks=all_masks(ks);carriers={}; maps={}
    need(isinstance(obj['carriers'],list),'carrier records required')
    eq(len(obj['carriers']),len(masks),'carrier coverage count')
    for c in obj['carriers']:
        fields(c,('mask','genesis','keys','L','Z','G'))
        mask=c['mask'];need(type(mask) is int and mask in masks and mask not in carriers,'duplicate/illegal carrier mask')
        eq(c['genesis'],obj['genesis'],'carrier origin')
        expected=tuple(k for i,k in enumerate(ks) if mask&(1<<i));ck=keys(c['keys'])
        eq(ck,expected,'retained identity/array order mismatch')
        L,Z,G=model(ck); size=len(ck)
        eq(matrix(c['L'],size,size),L,'wrong incidence Laplacian')
        eq(matrix(c['Z'],size,size),Z,'wrong centering representative')
        eq(matrix(c['G'],size,size),G,'wrong Green operator')
        carriers[mask]=(ck,L,Z,G)
    expected_maps={(a,b) for a in masks for b in masks if a&b==b}
    eq(len(obj['prunings']),len(expected_maps),'pruning coverage count')
    for p in obj['prunings']:
        fields(p,('genesis','src','dst','images','P','I','S','h','K','fiber_input','fiber_output'))
        ab=p['src'],p['dst'];need(ab in expected_maps and ab not in maps,'duplicate/illegal pruning domain')
        eq(p['genesis'],obj['genesis'],'illegal domain identification')
        fk,Lf,Zf,Gf=carriers[ab[0]];ck,Lc,Zc,Gc=carriers[ab[1]]; nf,nc=len(fk),len(ck)
        images=[parent_image(k,set(ck)) for k in fk]
        eq(p['images'],[list(k) for k in images],'wrong ancestral retraction')
        P=sp.Matrix(nc,nf,lambda i,j:int(images[j]==ck[i]))
        I=sp.Matrix(nf,nc,lambda i,j:int(fk[i]==ck[j]));S=I.T;h=P.T
        for name,expected in (('P',P),('I',I),('S',S),('h',h)):
            eq(matrix(p[name],expected.rows,expected.cols),expected,'wrong '+name+' defining map')
        K=matrix(p['K'],nf,nf-nc)
        eq(P*K,sp.zeros(nc,K.cols),'kernel basis membership')
        eq(K.rank(),nf-nc,'kernel basis completeness')
        eq(len(P.nullspace()),nf-nc,'independent kernel dimension')
        eq(P*I,sp.eye(nc),'source section identity')
        eq(S*h,sp.eye(nc),'response section identity')
        eq(P*Lf,Lc*S,'fiber boundary identity')
        eq(Lf*h,I*Lc,'pullback harmonic identity')
        eq(Zc*S*Gf,Gc*P*Zf,'balanced response restriction')
        eq(Gf*I*Zc,Zf*h*Gc,'response lift compatibility')
        probe=vec(p['fiber_input'],nf);reported=vec(p['fiber_output'],nc)
        summed=sp.Matrix([sum(probe[j] for j,x in enumerate(images) if x==c) for c in ck])
        eq(reported,summed,'direct fiber sum');eq(P*probe,summed,'matrix/fiber comparison')
        eq(sum(reported),sum(probe),'total grade')
        maps[ab]={'P':P,'I':I,'S':S,'h':h,'K':K}
    G0=carriers[full][3];Z0=carriers[full][2];L0=carriers[full][1]
    expected_chains=all_chains(masks,full,bound)
    eq(len(obj['chains']),len(expected_chains),'chain coverage count')
    seen=set();stage_cache={};total_steps=non_desc=rank_old_sum=triples=nonempty_old=0
    for chain in obj['chains']:
        fields(chain,('masks','steps'));seq=tuple(chain['masks'])
        need(seq in expected_chains and seq not in seen,'chain identity coverage');seen.add(seq)
        eq(len(chain['steps']),len(seq)-1,'stage coverage')
        ds=[]
        for (prev,cur),st in zip(zip(seq,seq[1:]),chain['steps']):
            fields(st,('previous','current','E','D','kernel_dim','old_kernel_dim','rank_current','rank_old','descends','witness','section','cumulative_images','old_images','new_images','representatives'))
            eq((st['previous'],st['current']),(prev,cur),'stage endpoint identity')
            signature=json.dumps(st,sort_keys=True)
            if (prev,cur) not in stage_cache:
                before,now,step=maps[full,prev],maps[full,cur],maps[prev,cur]
                Kprev,K=before['K'],now['K']; Eprev=before['I']*before['P'];E=now['I']*now['P'];D=Eprev-E
                eq(matrix(st['E'],n,n),E,'cumulative source projector')
                eq(matrix(st['D'],n,n),D,'source layer projector')
                eq(E*E,E,'source idempotence');eq(D*D,D,'layer idempotence')
                eq(now['P']*Kprev,sp.zeros(len(carriers[cur][0]),Kprev.cols),'kernel nesting')
                eq(st['kernel_dim'],K.cols,'kernel dimension');eq(st['old_kernel_dim'],Kprev.cols,'old kernel dimension')
                current_image=G0*K;old_full=G0*Kprev
                eq(st['rank_current'],current_image.rank(),'current obstruction rank')
                eq(st['rank_old'],old_full.rank(),'old obstruction rank')
                check_descent(G0,Kprev,st['descends'])
                section=before['I']*step['K']
                eq(matrix(st['section'],n,step['K'].cols),section,'supplied exact-sequence section')
                eq(before['P']*section,step['K'],'section right inverse on step kernel')
                eq(now['P']*section,sp.zeros(now['P'].rows,section.cols),'section cumulative membership')
                eq(Kprev.row_join(section).rank(),K.cols,'split sequence spans cumulative kernel')
                eq(Kprev.cols+section.cols,K.cols,'split sequence dimensions')
                old_image=G0*(sp.eye(n)-Eprev)*K
                lifted=Z0*before['h']*carriers[prev][3]*before['P']*K
                eq(matrix(st['cumulative_images'],n,K.cols),current_image,'cumulative image certificate')
                eq(matrix(st['old_images'],n,K.cols),old_image,'old response certificate')
                eq(matrix(st['new_images'],n,K.cols),lifted,'stage lift certificate')
                eq(old_image+lifted,current_image,'cumulative/stage response identity')
                responseD=Z0*before['h']*before['S']-Z0*now['h']*now['S']
                eq(responseD*G0,G0*D*Z0,'source/response layer intertwining')
                if st['descends']:
                    need(st['witness'] is None,'unexpected non-descent witness')
                    eq(old_full,sp.zeros(n,Kprev.cols),'positive descent annihilation')
                else:
                    w=st['witness'];fields(w,('k','image'));k=vec(w['k'],n);image=vec(w['image'],n)
                    eq(before['P']*k,sp.zeros(before['P'].rows,1),'witness old-kernel membership')
                    eq(now['P']*k,sp.zeros(now['P'].rows,1),'witness cumulative membership')
                    eq(sum(k),0,'witness source balance');eq(G0*k,image,'witness image')
                    eq(L0*image,k,'witness defining response equation');eq(sum(image),0,'witness centered representation')
                    need(any(image[i]!=image[ks.index(())] for i in range(n)),'witness nonzero quotient image')
                rep=st['representatives'];fields(rep,('x','old_k','image','image_shifted','old_image'))
                x,k=vec(rep['x'],n),vec(rep['old_k'],n)
                eq(now['P']*x,sp.zeros(now['P'].rows,1),'representative in K_j')
                eq(before['P']*k,sp.zeros(before['P'].rows,1),'representative shift in old kernel')
                phi,shift,previous=vec(rep['image'],n),vec(rep['image_shifted'],n),vec(rep['old_image'],n)
                eq(phi,G0*x,'representative response');eq(shift,G0*(x+k),'shifted response');eq(previous,G0*k,'old response')
                eq(shift-phi,previous,'response quotient representative difference')
                eq(old_full.row_join(previous).rank(),old_full.rank(),'difference in discarded response subspace')
                eq(Eprev*(x+k),Eprev*x,'supplied representative selector independence')
                eq(current_image.row_join(old_full).rank()-old_full.rank(),K.cols-Kprev.cols,'graded response quotient image dimension')
                stage_cache[prev,cur]=(signature,D,st['descends'],st['rank_old'])
            cached,D,desc,rko=stage_cache[prev,cur]
            eq(signature,cached,'inconsistent duplicate stage certificate')
            ds.append(D);total_steps+=1;non_desc+=int(not desc);rank_old_sum+=rko;nonempty_old+=int(st['old_kernel_dim']>0)
        for x,y,z in zip(seq,seq[1:],seq[2:]):
            a,b,c=maps[x,y],maps[y,z],maps[x,z]
            eq(b['P']*a['P'],c['P'],'two/three-stage pushforward composition')
            eq(a['I']*b['I'],c['I'],'source inclusion composition')
            eq(b['S']*a['S'],c['S'],'response restriction composition')
            eq(a['h']*b['h'],c['h'],'response lift composition');triples+=1
        summed=sum(ds,sp.zeros(n));final=maps[full,seq[-1]]
        eq(summed,sp.eye(n)-final['I']*final['P'],'refinement telescoping')
        eq(G0*summed,G0*(sp.eye(n)-final['I']*final['P']),'endpoint loss response')
        for i in range(len(ds)):
            for j in range(i):eq(ds[i]*ds[j],sp.zeros(n),'different layer product')
    eq(seen,expected_chains,'complete chain keys')
    return {'vertices':n,'carriers':len(carriers),'prunings':len(maps),'chains':len(seen),'steps':total_steps,
            'non_descending_steps':non_desc,'descending_steps':total_steps-non_desc,'nonempty_old_kernel_steps':nonempty_old,
            'old_kernel_rank_sum':rank_old_sum,'composition_triples':triples,'distinct_stage_certificates':len(stage_cache)}

def verify_instance(obj):
    try:return _verify_instance(obj)
    except VerificationError:raise
    except Exception as exc:raise VerificationError('malformed certificate: '+repr(exc)) from exc

def check_instance_naturality(original,changed,rename):
    ka,kb=keys(original['keys']),keys(changed['keys'])
    need(set(rename)==set(ka) and set(rename.values())==set(kb),'relabel bijection')
    eq(rename[()],(),'relabel root')
    need(all(not k or rename[k][:-1]==rename[k[:-1]] for k in ka),'relabel ancestry')
    eq(original['genesis'],changed['genesis'],'relabel Genesis')
    ca={c['mask']:c for c in original['carriers']};cb={c['mask']:c for c in changed['carriers']}
    matching={}; permutations={}
    for mask,c in ca.items():
        akeys=keys(c['keys']);wanted={rename[k] for k in akeys}
        other=next((d for d in cb.values() if set(keys(d['keys']))==wanted),None)
        need(other is not None,'missing relabeled carrier');matching[mask]=other['mask']
        bkeys=keys(other['keys']);n=len(akeys)
        T=sp.Matrix(n,n,lambda i,j:int(bkeys[i]==rename[akeys[j]]));permutations[mask]=T
        for name in ('L','Z','G'):
            eq(matrix(other[name],n,n),T*matrix(c[name],n,n)*T.T,'carrier covariance '+name)
    mb={(p['src'],p['dst']):p for p in changed['prunings']}
    for p in original['prunings']:
        src,dst=p['src'],p['dst'];other=mb[matching[src],matching[dst]]
        Tf,Tc=permutations[src],permutations[dst];nf,nc=Tf.rows,Tc.rows
        for name in ('P','S'):
            check_naturality(Tc,matrix(p[name],nc,nf),Tf,matrix(other[name],nc,nf))
        for name in ('I','h'):
            check_naturality(Tf,matrix(p[name],nf,nc),Tc,matrix(other[name],nf,nc))
        A=Tf*matrix(p['K'],nf,nf-nc);B=matrix(other['K'],nf,nf-nc)
        eq(A.row_join(B).rank(),nf-nc,'kernel subspace covariance')
    changed_chains={tuple(c['masks']):c for c in changed['chains']};T0=permutations[(1<<len(ka))-1]
    for c in original['chains']:
        other=changed_chains[tuple(matching[m] for m in c['masks'])]
        for a,b in zip(c['steps'],other['steps']):
            for name in ('E','D'):
                eq(matrix(b[name],len(kb),len(kb)),T0*matrix(a[name],len(ka),len(ka))*T0.T,'layer covariance '+name)
            eq(a['descends'],b['descends'],'descent covariance')
    return len(original['prunings'])

def check_basis_changes(obj):
    cs={c['mask']:c for c in obj['carriers']};count=0
    def change(n,lower=False):
        M=sp.eye(n)
        for i in range(n-1):
            if lower:M[i+1,i]=i+2
            else:M[i,i+1]=i+1
        return M
    for p in obj['prunings']:
        f,c=cs[p['src']],cs[p['dst']];n,m=len(f['keys']),len(c['keys'])
        A,B=change(n),change(m);U,V=change(n,True),change(m,True)
        Ai,Bi,Ui,Vi=A.inv(),B.inv(),U.inv(),V.inv()
        Zf,Zc=matrix(f['Z'],n,n),matrix(c['Z'],m,m)
        Gf,Gc=U*matrix(f['G'],n,n)*Ai,V*matrix(c['G'],m,m)*Bi
        P=B*matrix(p['P'],m,n)*Ai;I=A*matrix(p['I'],n,m)*Bi
        R=V*Zc*matrix(p['S'],m,n)*Ui;H=U*Zf*matrix(p['h'],n,m)*Vi
        eq(P*I,sp.eye(m),'basis-changed source section')
        eq(R*H,V*Zc*Vi,'basis-changed quotient response section')
        eq(R*Gf,Gc*P*(A*Zf*Ai),'basis-changed balanced comparison')
        eq(Gf*I*(B*Zc*Bi),H*Gc,'basis-changed lift comparison');count+=1
    return count

def challenge_verifier(instance):
    receipts=[]
    def challenge(name,mutator,expected_reason):
        obj=copy.deepcopy(instance);mutator(obj)
        try:verify_instance(obj)
        except VerificationError as exc:
            need(expected_reason in str(exc),'defect rejected for unintended reason: '+name+': '+str(exc))
            receipts.append({'defect':name,'rejected':True,'reason':str(exc)})
        else:raise VerificationError('verifier accepted deliberately corrupted '+name)
    challenge('P-coefficient',lambda o:o['prunings'][0]['P'][0].__setitem__(0,'2'),'wrong P')
    challenge('section',lambda o:o['prunings'][0]['I'][0].__setitem__(0,'2'),'wrong I')
    challenge('Green',lambda o:o['carriers'][0]['G'][0].__setitem__(0,'7'),'wrong Green')
    challenge('domain',lambda o:o['prunings'][0].__setitem__('genesis','foreign'),'illegal domain')
    def step(o):return next(z for c in o['chains'] for z in c['steps'] if z['witness'] is not None)
    challenge('descent',lambda o:step(o).__setitem__('descends',True),'false fixed-target')
    challenge('witness',lambda o:step(o)['witness']['image'].__setitem__(0,'99'),'witness image')
    challenge('coverage',lambda o:o['chains'].pop(),'chain coverage')
    challenge('missing-field',lambda o:o['prunings'][0].pop('I'),'missing required field')
    P=sp.Matrix([[1,1,1]]);biased=sp.Matrix([0,1,0]);swap=sp.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    eq(P*biased,sp.ones(1,1),'control is a linear right inverse')
    try:check_naturality(swap,biased,sp.eye(1),biased)
    except VerificationError as exc:receipts.append({'defect':'linear-but-nonnatural-section','rejected':True,'reason':str(exc)})
    else:raise VerificationError('biased section incorrectly accepted as natural')
    return receipts

def verify_bundle(bundle):
    fields(bundle,('schema','base_sha','scalar_domain','max_vertices','max_arrows','instances','relabeled_instances'))
    eq(bundle['schema'],'fcv-1-certificates-v1','schema');eq(bundle['base_sha'],BASE,'parent binding')
    eq(bundle['scalar_domain'],'Q formal signed diagnostic','scalar scope');eq(bundle['max_vertices'],5,'vertex bound');eq(bundle['max_arrows'],3,'arrow bound')
    expected={'U1:'+c:k for c,k in independent_shapes(5).items()}
    expected.update({'U2:'+str(i+1):f for i,(f,_) in enumerate(HISTORICAL)})
    actual={i['tag']:i for i in bundle['instances']};renamed={i['tag']:i for i in bundle['relabeled_instances']}
    eq(len(actual),len(bundle['instances']),'duplicate instance');eq(set(actual),set(expected),'complete instance coverage')
    eq(len(renamed),len(bundle['relabeled_instances']),'duplicate renamed instance');eq(set(renamed),set(expected),'renamed coverage')
    rows=[];basis_checks=naturality_checks=0
    for tag,ks in expected.items():
        original,changed=actual[tag],renamed[tag]
        eq(keys(original['keys']),ks,'raw universe lineage');eq(original['max_arrows'],3,'full arrow coverage')
        result=verify_instance(original);other=verify_instance(changed);eq(result,other,'metamorphic classification')
        rename={k:tuple(20-3*t for t in k) for k in ks}
        eq(keys(changed['keys']),tuple(rename[k] for k in reversed(ks)),'frozen relabel/storage control')
        naturality_checks+=check_instance_naturality(original,changed,rename)
        basis_checks+=check_basis_changes(original)
        rows.append({'tag':tag,**result})
        print('Verified',tag,'chains',result['chains'],flush=True)
    control=next(i for i in actual.values() if len(i['keys'])==3)
    mutations=challenge_verifier(control)
    totals={k:sum(r[k] for r in rows) for k in rows[0] if k!='tag'}
    coverage={'instances':len(rows),'shape_counts':{str(n):sum(len(k)==n for k in independent_shapes(5).values()) for n in range(1,6)},
              'original':totals,'relabeled':totals.copy(),'basis_changed_prunings':basis_checks,'naturality_prunings':naturality_checks}
    coverage_hash=hashlib.sha256(json.dumps([(r['tag'],r['chains'],r['steps']) for r in rows],separators=(',',':')).encode()).hexdigest()
    return {'execution_status':'completed','input_validity':'all reconstructed inputs and coverage validated',
            'all_valid':len(rows)==len(expected) and len(mutations)==9 and all(m['rejected'] for m in mutations),
            'proof_status':'general arguments P0-P7 in PROOFS.md; code provides bounded exact certificates; self-reviewed',
            'scientific_verdicts':{'fixed_target_descent':'OLD_KERNEL_OBSTRUCTION_WITNESSED' if totals['non_descending_steps'] else 'NO_OLD_KERNEL_OBSTRUCTION_OBSERVED',
                'old_kernel_condition_matches':totals['non_descending_steps']==totals['nonempty_old_kernel_steps'],
                'source_sections_verified':totals['prunings'], 'response_comparisons_verified':totals['prunings'],
                'stage_composition_diagrams_verified':totals['composition_triples']},
            'coverage':coverage,'coverage_count_sha256':coverage_hash,'instances':rows,'deliberate_defects':mutations,
            'scope':'finite prefix-tree retained structures and the inherited rational Green-response diagnostic; no physical source realization or geometry claim'}

def verify_historical(raw):
    need(raw.get('version')=='16.15F','historical reproduction version')
    expected=[]
    for i,(fine,coarse) in enumerate(HISTORICAL,1):
        current=list(fine);L,Z,G=model(fine);prevP=sp.eye(len(fine));j=0
        while set(current)!=set(coarse):
            candidates=[k for k in current if k not in coarse and not any(z and z[:-1]==k for z in current)]
            victim=max(candidates,key=lambda k:(len(k),k));current.remove(victim);j+=1
            images=[parent_image(k,set(current)) for k in fine]
            P=sp.Matrix(len(current),len(fine),lambda a,b:int(current[a]==images[b]))
            K=P.nullspace();U=prevP.nullspace()
            B=sp.Matrix.hstack(*K) if K else sp.zeros(len(fine),0)
            A=sp.Matrix.hstack(*U) if U else sp.zeros(len(fine),0)
            expected.append({'fixture':i,'stage':j,'fine_count':len(fine),'retained_count':len(current),
              'kernel_dim':len(K),'previous_kernel_dim':len(U),'obstruction_rank_on_kernel':(G*B).rank(),
              'obstruction_rank_on_previous_kernel':(G*A).rank(),'descends_to_new_grade':G*A==sp.zeros(len(fine),A.cols)})
            prevP=P
    eq(raw['records'],expected,'historical exact records');need(len(expected)>0,'empty historical verification')
    return {'stages':len(expected),'descending_stages':sum(x['descends_to_new_grade'] for x in expected),
            'non_descending_stages':sum(not x['descends_to_new_grade'] for x in expected),
            'scope':'new independent reconstruction of the historical selected chains, not an old-run upgrade'}

if __name__=='__main__':
    d=HERE/'evidence'
    (d/'VERIFICATION.json').unlink(missing_ok=True)
    (d/'INVALID_VERIFICATION.json').unlink(missing_ok=True)
    try:
        raw=lzma.decompress((d/'certificates.json.xz').read_bytes());bundle=json.loads(raw)
        result=verify_bundle(bundle)
        result['historical_reproduction']=verify_historical(json.loads((d/'REPRODUCED_1615F.json').read_text()))
        result['raw_certificate_sha256']=hashlib.sha256(raw).hexdigest()
        (d/'VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'all_valid':result['all_valid'],'coverage':result['coverage'],'historical_reproduction':result['historical_reproduction']}))
        if not result['all_valid']:raise VerificationError('required check count mismatch')
    except Exception:
        d.mkdir(exist_ok=True)
        (d/'INVALID_VERIFICATION.json').write_text(json.dumps({'execution_status':'invalid','all_valid':False,'error':traceback.format_exc()},indent=2)+'\n')
        raise
