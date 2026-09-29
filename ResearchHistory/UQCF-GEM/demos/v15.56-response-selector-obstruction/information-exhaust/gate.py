"""16.16 exact information-exhaust classifier. No geometric target."""
from pathlib import Path
import hashlib,json,lzma,subprocess
import sympy as sp
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'network-interpretation'
PARENT_XZ='3b3f5e075ef129640f135b76780544ea268bd22bbc2efb17cd4d3b3dbebe2b81'
def ranks(local,network):
 L=sp.Matrix(local);R=sp.Matrix(network);S=L.col_join(R)
 rl,rr,rs=L.rank(),R.rank(),S.rank(); n=L.cols
 return int(rl),int(rr),int(rs),int(n-rl),int(n-rs),bool(rs>rl)
def k(x): return (x['candidate'],x['a'],x['arm'])
def audit():
 raw=(PARENT/'result.json.xz').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PARENT_XZ: raise ValueError('16.15 compressed parent hash mismatch')
 p=json.loads(lzma.decompress(raw))
 if not(p['version']=='16.15' and p['all_valid'] and len(p['pairs'])==72 and len(p['local_scalars'])==1728 and len(p['independent_loop_checks'])==504): raise ValueError('parent completeness')
 local={};loops={}
 for x in p['local_scalars']: local.setdefault(k(x),[]).append(x)
 for x in p['independent_loop_checks']: loops.setdefault(k(x),[]).append(x)
 out=[]
 for ident in sorted(local):
  ls=sorted(local[ident],key=lambda x:(x['edge'],x['observable']))
  rs=sorted(loops[ident],key=lambda x:x['cycle'])
  if len(ls)!=24 or len(rs)!=7: raise ValueError('pair coverage')
  L=[[sp.Rational(v) for v in x['contrast']] for x in ls]
  R=[[sp.Rational(v) for v in x['total']] for x in rs]
  N=[[sp.Rational(v) for v in x['normal']] for x in rs]
  a=ranks(L,R); b=ranks(L,N)
  if ident[1]==1.0 and any(a[:3]): raise ValueError('identity null')
  if any(row[0]!=0 for row in L+R+N): raise ValueError('zero-coherence coefficient')
  out.append({'candidate':ident[0],'a':ident[1],'arm':ident[2],
   'local_rank':a[0],'network_rank':a[1],'combined_rank':a[2],
   'local_kernel_dim':a[3],'combined_kernel_dim':a[4],
   'network_adds_quotient_direction':a[5],
   'normal_network_rank':b[1],'local_plus_normal_rank':b[2],
   'normal_adds_quotient_direction':b[5]})
 adds=sum(x['network_adds_quotient_direction'] for x in out)
 verdict='NETWORK_ADDS_QUOTIENT_DIRECTION' if adds==72 else 'LOCAL_DIFFERENTIAL_SPANS_FROZEN_RESPONSE' if adds==0 else 'MIXED_INFORMATION_EXHAUST'
 return {'version':'16.16','all_valid':True,'verdict':verdict,'parent_version':'16.15','parent_xz_sha256':PARENT_XZ,
  'counts':{'pairs':72,'local_records':1728,'loop_records':504},
  'metrics':{'network_additional_pairs':adds,'normal_additional_pairs':sum(x['normal_adds_quotient_direction'] for x in out),
   'local_rank_counts':{str(i):sum(x['local_rank']==i for x in out) for i in range(3)},
   'network_rank_counts':{str(i):sum(x['network_rank']==i for x in out) for i in range(3)},
   'combined_rank_counts':{str(i):sum(x['combined_rank']==i for x in out) for i in range(3)}},
  'pairs':out,
  'interpretation':'Exact first-order information classification in the frozen two-coefficient family; no geometry inferred.'}
if __name__=='__main__':
 try:r=audit()
 except Exception as e:r={'version':'16.16','all_valid':False,'verdict':'INVALID','error':repr(e)}
 r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
 (HERE/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 print(json.dumps({x:r.get(x) for x in ['all_valid','verdict','metrics']}))
 raise SystemExit(0 if r['all_valid'] else 2)
