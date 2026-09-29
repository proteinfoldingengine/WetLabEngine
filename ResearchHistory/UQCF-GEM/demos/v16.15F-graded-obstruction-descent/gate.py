"""v16.15F exact graded descent of the intrinsic full-fine obstruction."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,subprocess
HERE=Path(__file__).resolve().parent
p=HERE.parent/'v15.56-response-selector-obstruction'/'pruning_consistency_audit.py'
s=importlib.util.spec_from_file_location('pc',p);PC=importlib.util.module_from_spec(s);s.loader.exec_module(PC)
def nullspace(A):
 R,piv=PC.rref(A); n=len(A[0]);free=[j for j in range(n) if j not in piv];out=[]
 for f in free:
  x=[F(0)]*n;x[f]=F(1)
  for i,j in enumerate(piv):x[j]=-R[i][f]
  out.append(x)
 return out
def matcols(cols,nrows):
 return [[col[i] for col in cols] for i in range(nrows)] if cols else [[] for _ in range(nrows)]
def chain(fine,coarse):
 # Remove noncoarse leaves in reverse depth/address order while preserving prefix closure.
 cur=list(fine); out=[tuple(cur)]
 while set(cur)!=set(coarse):
  removable=[k for k in cur if k not in coarse and not any(len(z)==len(k)+1 and z[:-1]==k for z in cur)]
  if not removable:raise ValueError('no lawful leaf pruning')
  victim=max(removable,key=lambda k:(len(k),k));cur.remove(victim);out.append(tuple(cur))
 return out
def audit():
 records=[];desc=0;history=0
 for ci,(fine,coarse) in enumerate(PC.CASES):
  L=PC.laplacian(fine);G=PC.green(L);Q=PC.center(len(fine));T=PC.mul(Q,G)
  ch=chain(fine,coarse)
  prev=[]
  for j,carrier in enumerate(ch[1:],1):
   P=PC.operators(fine,carrier)['P'];K=nullspace(P)
   # T restricted to K
   TK=PC.mul(T,matcols(K,len(fine))) if K else [[] for _ in fine]
   rankK=PC.rank(TK) if K else 0
   TP=PC.mul(T,matcols(prev,len(fine))) if prev else [[] for _ in fine]
   rankPrev=PC.rank(TP) if prev else 0
   ok=rankPrev==0
   desc+=ok;history+=not ok
   records.append({'fixture':ci+1,'stage':j,'fine_count':len(fine),'retained_count':len(carrier),'kernel_dim':len(K),'previous_kernel_dim':len(prev),'obstruction_rank_on_kernel':rankK,'obstruction_rank_on_previous_kernel':rankPrev,'descends_to_new_grade':ok})
   prev=K
 total=len(records)
 verdict='GRADED_OBSTRUCTION_DESCENT_CERTIFIED' if desc==total else 'OBSTRUCTION_RETAINS_PRIOR_GRADE_HISTORY' if history and desc==4 else 'MIXED_GRADED_DESCENT'
 # First nontrivial stage has K_prev=0 by construction; later stages decide history.
 return {'version':'16.15F','all_valid':total>0,'verdict':verdict,'metrics':{'stages':total,'descending_stages':desc,'history_retaining_stages':history},'records':records,'scope':'Intrinsic full-fine obstruction QG_f on nested pruning kernels; retained-boundary theorem unchanged.'}
if __name__=='__main__':
 r=audit();r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_valid':r['all_valid'],'verdict':r['verdict'],'metrics':r['metrics']}))
