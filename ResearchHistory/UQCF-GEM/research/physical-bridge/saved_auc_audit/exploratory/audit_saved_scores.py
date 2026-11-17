"""Read-only scoring of saved labeled rows; never import/run scientific generators."""
from pathlib import Path
import ast, bisect, csv, hashlib, io, json, math, zipfile
import numpy as np

ROOT=Path(__file__).parent
DATA=ROOT/'library'
def sha(b): return hashlib.sha256(b).hexdigest()
def gitblob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def readcsv(b): return list(csv.DictReader(io.StringIO(b.decode())))
def score(rows,col):
    pos=[(r['pair_id'],float(r[col])) for r in rows if int(r['label'])==1]
    neg=[(r['pair_id'],float(r[col])) for r in rows if int(r['label'])==0]
    assert pos and neg and all(math.isfinite(x) for _,x in pos+neg)
    p=np.array([x for _,x in pos])[:,None];n=np.array([x for _,x in neg])[None,:]
    wins=p>n; equal=p==n; close=np.isclose(p,n)
    N=len(pos)*len(neg)
    W,T,C=map(lambda a:int(a.sum()),[wins,equal,close])
    # Independent rank/bisection comparator (no approximate equality).
    ns=sorted(x for _,x in neg)
    twice_rank=sum(bisect.bisect_left(ns,x)+bisect.bisect_right(ns,x) for _,x in pos)
    assert twice_rank==2*W+T
    # Independent scalar implementation of the documented NumPy default predicate.
    C_scalar=sum(abs(x-y)<=1e-8+1e-5*abs(y) for _,x in pos for _,y in neg)
    assert C_scalar==C
    examples=[]
    for i,j in np.argwhere(close & ~equal):
        examples.append({'positive_pair_id':pos[i][0],'negative_pair_id':neg[j][0],
                         'p':pos[i][1],'n':neg[j][1],'win':bool(wins[i,j]),
                         'difference':abs(pos[i][1]-neg[j][1]),
                         'threshold':1e-8+1e-5*abs(neg[j][1])})
    return {'comparisons':N,'wins':W,'exact_ties':T,'approx_ties':C,
            'close_wins':int((close&wins).sum()),'close_losses':int((close&(p<n)).sum()),
            'v725_formula_auc':(2*W+C)/(2*N),'exact_tie_auc':twice_rank/(2*N),
            'bias_fraction':[C-T,2*N],'bias':(C-T)/(2*N),
            'unequal_close_examples':examples}

v725_b=(DATA/'v725_observable_only_atrium_metric_paired_metrics.csv').read_bytes()
v725=readcsv(v725_b)
summary=json.loads((DATA/'v725_observable_only_atrium_metric_results.json').read_text())['summary']
assert len(v725)==480
assert {r['pair_id'] for r in v725}=={str(i) for i in range(240)}
assert all(sum(r['pair_id']==str(i) and int(r['label'])==j for r in v725)==1 for i in range(240) for j in [0,1])
assert {float(r['k']) for r in v725 if r['label']=='0'}=={.9}
assert {float(r['k']) for r in v725 if r['label']=='1'}=={.25}
cols=['restoration_distance','adm_z','g_atrium_observable_only','g_atrium_with_k_oracle','passive_mean','passive_curvature']
out={'scope':'One saved V725 main dataset and one saved V737 main dataset; no generators or sweeps executed.',
     'numpy_version':np.__version__,'v725_csv_sha256':sha(v725_b),'v725_rows':len(v725),'v725':{}}
for col in cols:
    d=score(v725,col);d['archived_summary_auc']=summary[col+'_auc']
    assert d['v725_formula_auc']==d['archived_summary_auc']
    out['v725'][col]=d
v725_source=(DATA/'v725_observable_only_atrium_metric_extraction.py').read_bytes()
assert gitblob(v725_source)=='cf8a1bd5937acde59586b6d42ae8979742fd4e89'
out['v725_source_git_blob']=gitblob(v725_source)

bundle=(DATA/'V737_atrium_reproducibility_bundle.zip').read_bytes()
with zipfile.ZipFile(io.BytesIO(bundle)) as z:
    prefix='V737_atrium_reproducibility_bundle/'
    src=z.read(prefix+'v737_reproduce_atrium_metric.py')
    assert gitblob(src)=='8b4f50b515603d978f8b2ca6e31c875314541c40'
    vb=z.read(prefix+'outputs/v737_main_metrics.csv'); rows=readcsv(vb)
    ss=json.loads(z.read(prefix+'outputs/v737_results.json'))['main']
    out['v737']={'bundle_sha256':sha(bundle),'source_git_blob':gitblob(src),
                 'main_csv_sha256':sha(vb),'rows':len(rows),'scores':{}}
    assert len(rows)==840
    assert all(sum(r['pair_id']==str(i) and int(r['label'])==j for r in rows)==1 for i in range(420) for j in [0,1])
    for col,key in [('atrium_scalar','atrium_auc'),('restoration_residual','restoration_residual_auc'),('passive_mean','passive_mean_auc'),('passive_curvature','passive_curvature_auc')]:
        d=score(rows,col);d['archived_summary_auc']=ss[key]
        assert math.isclose(d['exact_tie_auc'],ss[key],rel_tol=0,abs_tol=1e-15)
        pos=np.array([float(r[col]) for r in rows if int(r['label'])==1])
        neg=np.array([float(r[col]) for r in rows if int(r['label'])==0])
        d['v737_formula_auc']=float(np.mean([(v>neg).mean()+.5*(v==neg).mean() for v in pos]))
        assert d['v737_formula_auc']==ss[key]
        out['v737']['scores'][col]=d

(ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
