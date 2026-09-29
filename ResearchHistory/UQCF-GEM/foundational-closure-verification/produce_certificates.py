"""Produce raw finite-tree certificates. No scientific success is hardcoded."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, lzma, os, subprocess, traceback
from lineage import Carrier, Pruning
from enumerate_cases import rooted_shapes, legal_masks, chains
import exact_algebra as a
HERE=Path(__file__).resolve().parent
BASE='10e12fd2f178a03da5daedd4fb15af1cd94d1299'

def pruning_data(fine, coarse, src, dst):
    r=Pruning(fine,coarse); n,m=len(fine.keys),len(coarse.keys)
    P=[[F(r.ancestor(x)==y) for x in fine.keys] for y in coarse.keys]
    I=[[F(x==y) for y in coarse.keys] for x in fine.keys]
    lost=[x for x in fine.keys if x not in coarse.keys]
    K=[[F(x==v)-F(x==r.ancestor(v)) for v in lost] for x in fine.keys]
    values=tuple(F(i+1,i+2) for i in range(n)); summed=r.aggregate(values)
    return {'genesis':fine.genesis,'src':src,'dst':dst,
            'images':[list(r.ancestor(k)) for k in fine.keys],
            'P':P,'I':I,'S':a.transpose(I),'h':a.transpose(P),'K':K,
            'fiber_input':values,'fiber_output':summed}

def build_instance(tag, keys, max_arrows=3):
    keys=tuple(tuple(k) for k in keys); full_carrier=Carrier(tag,keys)
    if type(max_arrows) is not int or not 1<=max_arrows<=3: raise ValueError('arrow bound')
    masks=legal_masks(keys); full=(1<<len(keys))-1; n=len(keys)
    carriers={}; carrier_records=[]
    for mask in masks:
        c=Carrier(tag,tuple(k for i,k in enumerate(keys) if mask&(1<<i)))
        L=a.pc.laplacian(c.keys); Z=a.pc.center(len(c.keys)); G=a.pc.green(L)
        carriers[mask]=(c,L,Z,G)
        carrier_records.append({'mask':mask,'genesis':tag,'keys':[list(k) for k in c.keys],
                                'L':a.encode(L),'Z':a.encode(Z),'G':a.encode(G)})
    maps={}; map_records=[]
    for src in masks:
        for dst in masks:
            if src&dst != dst: continue
            d=pruning_data(carriers[src][0],carriers[dst][0],src,dst); maps[src,dst]=d
            map_records.append({k:(a.encode(v) if k in ('P','I','S','h','K') else list(map(str,v)) if k in ('fiber_input','fiber_output') else v) for k,v in d.items()})
    Z0,G0=carriers[full][2:]; identity=a.eye(n)
    stage_cache={}
    def stage(prev,cur):
        if (prev,cur) in stage_cache: return stage_cache[prev,cur]
        before,now,step=maps[full,prev],maps[full,cur],maps[prev,cur]
        Kprev,K=before['K'],now['K']; Eprev=a.mul(before['I'],before['P']); E=a.mul(now['I'],now['P']);D=a.sub(Eprev,E)
        cumulative=a.mul(G0,K); old=a.mul(G0,a.mul(a.sub(identity,Eprev),K))
        new=a.mul(a.mul(a.mul(a.mul(Z0,before['h']),carriers[prev][3]),before['P']),K)
        oldfull=a.mul(G0,Kprev); rankold=a.rank(oldfull); ranknow=a.rank(cumulative)
        witness=None
        for j in range(len(Kprev[0])):
            im=a.col(oldfull,j)
            if any(x[0] for x in im):
                witness={'k':a.vector(a.col(Kprev,j)),'image':a.vector(im)}; break
        x=a.col(K,len(K[0])-1) if K[0] else a.zero_col(n)
        k=a.col(Kprev,0) if Kprev[0] else a.zero_col(n)
        rec={'previous':prev,'current':cur,'E':a.encode(E),'D':a.encode(D),
             'kernel_dim':len(K[0]),'old_kernel_dim':len(Kprev[0]),
             'rank_current':ranknow,'rank_old':rankold,'descends':rankold==0,'witness':witness,
             'section':a.encode(a.mul(before['I'],step['K'])),
             'cumulative_images':a.encode(cumulative),'old_images':a.encode(old),'new_images':a.encode(new),
             'representatives':{'x':a.vector(x),'old_k':a.vector(k),'image':a.vector(a.mul(G0,x)),
                'image_shifted':a.vector(a.mul(G0,a.add(x,k))),'old_image':a.vector(a.mul(G0,k))}}
        stage_cache[prev,cur]=rec; return rec
    chain_records=[]
    for seq in chains(masks,full,max_arrows):
        chain_records.append({'masks':list(seq),'steps':[stage(u,v) for u,v in zip(seq,seq[1:])]})
    return {'tag':tag,'genesis':tag,'keys':[list(k) for k in keys],'max_arrows':max_arrows,
            'carriers':carrier_records,'prunings':map_records,'chains':chain_records}

def main():
    instances=[]; transformed=[]
    sources=[('U1:'+code, keys) for code,keys in rooted_shapes(5).items()]
    sources += [('U2:'+str(i+1),fine) for i,(fine,_) in enumerate(a.pc.CASES)]
    for tag,keys in sources:
        base=build_instance(tag,keys)
        rename={k:tuple(20-3*t for t in k) for k in keys}
        changed=build_instance(tag,tuple(rename[k] for k in reversed(keys)))
        instances.append(base); transformed.append(changed)
        print('Produced',tag,'vertices',len(keys),'chains',len(base['chains']),flush=True)
    bundle={'schema':'fcv-1-certificates-v1','base_sha':BASE,'scalar_domain':'Q formal signed diagnostic',
            'max_vertices':5,'max_arrows':3,'instances':instances,'relabeled_instances':transformed}
    raw=json.dumps(bundle,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    out=HERE/'evidence';out.mkdir(exist_ok=True)
    (out/'certificates.json.xz').write_bytes(lzma.compress(raw))
    receipt={'execution_status':'completed','input_validity':'producer validation executed; independent verification pending',
             'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw),
             'xz_sha256':hashlib.sha256((out/'certificates.json.xz').read_bytes()).hexdigest(),
             'instances':len(instances),'relabeled_instances':len(transformed)}
    (out/'PRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)

if __name__=='__main__':
    try: main()
    except Exception:
        (HERE/'evidence').mkdir(exist_ok=True)
        (HERE/'evidence/INVALID_PRODUCTION.json').write_text(json.dumps({'execution_status':'invalid','error':traceback.format_exc()},indent=2)+'\n')
        raise
