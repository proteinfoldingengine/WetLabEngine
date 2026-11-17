#!/usr/bin/env python3
"""Fixed saved-main-score verification. Stdlib only; no scientific imports/replay.
Default: authenticate sibling data and emit JSON. --output PATH saves it.
--self-test adds in-memory mutation controls; never alters inputs.
"""
import argparse, csv, hashlib, io, json, math
from collections import Counter
from fractions import Fraction
from pathlib import Path

HASHES = {
 'v725_main_metrics.csv':'7a34ae50a613d3899c6ca2ce46457d6c91f57a170141badf43f5019bc2559f5b',
 'v725_results.json':'8c78148ef5aafc1aa76705381d789501245e753ed5b42ef2613c524c0f18a9b6',
 'v737_main_metrics.csv':'a5de3faac83acff2da4c87c10351d69102f2931972bf3f76a3b53bba74e3f2e7',
 'v737_results.json':'882a50f6ef6b3bed19bf02f3726e61e9e065a9ad89cc586bce8eb3de2a4dcb6d'}
# SHA256 above is an immutable input identity, not a historical lineage claim.
COLS={725:[('restoration_distance','restoration_distance_auc'),('adm_z','adm_z_auc'),('g_atrium_observable_only','g_atrium_observable_only_auc'),('g_atrium_with_k_oracle','g_atrium_with_k_oracle_auc'),('passive_mean','passive_mean_auc'),('passive_curvature','passive_curvature_auc')],737:[('atrium_scalar','atrium_auc'),('restoration_residual','restoration_residual_auc'),('passive_mean','passive_mean_auc'),('passive_curvature','passive_curvature_auc')]}

def require(ok, message):
 if not ok: raise ValueError(message)

def strict_json(b):
 def pairs(items):
  d={}
  for k,v in items:
   require(k not in d,'duplicate JSON key'); d[k]=v
  return d
 def bad(x): raise ValueError('nonfinite JSON constant '+x)
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)

def rows(b, version):
 reader=csv.DictReader(io.StringIO(b.decode('utf-8')))
 require(reader.fieldnames and len(set(reader.fieldnames))==len(reader.fieldnames),'malformed CSV header')
 out=[]
 for r in reader:
  require(None not in r and all(v is not None for v in r.values()),'malformed CSV row')
  require(r.get('label') in ('0','1'),'invalid label')
  require(r.get('pair_id','').isdigit(),'invalid pair id')
  for k,v in r.items():
   if k!='family': require(math.isfinite(float(v)),'nonfinite CSV value')
  out.append(r)
 n=240 if version==725 else 420
 require(len(out)==2*n,'row count')
 require(Counter((int(r['pair_id']),int(r['label'])) for r in out)==Counter((i,j) for i in range(n) for j in (0,1)),'pair/label multiplicity')
 ks=(.9,.25) if version==725 else (.82,.019999999999999907)
 require(all(float(r['k'])==ks[int(r['label'])] for r in out),'label/k association')
 return out

def pairwise_sum(a):
 """Binary64 NumPy contiguous double reduction ordering (128-block, 8 lanes).
 This reproduces this saved reduction; not a general NumPy emulation.
 """
 n=len(a)
 if n<8:
  s=-0.0
  for x in a:s+=x
  return s
 if n<=128:
  lanes=list(a[:8]); i=8
  while i<n-(n%8):
   for j in range(8):lanes[j]+=a[i+j]
   i+=8
  s=((lanes[0]+lanes[1])+(lanes[2]+lanes[3]))+((lanes[4]+lanes[5])+(lanes[6]+lanes[7]))
  while i<n:s+=a[i];i+=1
  return s
 m=(n//2)//8*8
 return pairwise_sum(a[:m])+pairwise_sum(a[m:])

def rank_auc(p,n):
 a=sorted([(x,1) for x in p]+[(x,0) for x in n]); rank=Fraction(0);i=0
 while i<len(a):
  j=i+1
  while j<len(a) and a[j][0]==a[i][0]:j+=1
  rank+=Fraction(i+1+j,2)*sum(label for _,label in a[i:j]);i=j
 return (rank-Fraction(len(p)*(len(p)+1),2))/(len(p)*len(n))

def scores(rs,col):
 p=[float(r[col]) for r in rs if r['label']=='1'];n=[float(r[col]) for r in rs if r['label']=='0']
 W=T=C=CW=CL=ASY=0;means=[]
 for x in p:
  w=t=0
  for y in n:
   win=x>y;tie=x==y;close=abs(x-y)<=1e-8+1e-5*abs(y)
   w+=win;t+=tie;C+=close;CW+=close and win;CL+=close and x<y
   ASY+=close!=(abs(x-y)<=1e-8+1e-5*abs(x))
  W+=w;T+=t;means.append(w/len(n)+.5*(t/len(n)))
 N=len(p)*len(n);exact=Fraction(2*W+T,2*N)
 require(exact==rank_auc(p,n),'independent average-rank disagreement')
 return {'comparisons':N,'wins':W,'exact_ties':T,'approx_ties':C,'close_wins':CW,'close_losses':CL,'asymmetric_classifications':ASY,'exact_fraction':str(exact),'exact_auc':float(exact),'v725_formula':(W+.5*C)/N,'v737_row_means_formula':pairwise_sum(means)/len(means),'rounding_difference':pairwise_sum(means)/len(means)-float(exact)}

def analyze(data,authenticate=True):
 identities={k:hashlib.sha256(data[k]).hexdigest() for k in HASHES}
 if authenticate: require(identities==HASHES,'input SHA256 identity mismatch')
 result={}
 for v in (725,737):
  rs=rows(data[f'v{v}_main_metrics.csv'],v); obj=strict_json(data[f'v{v}_results.json']); summary=obj['summary' if v==725 else 'main']
  require(summary['n_pairs' if v==725 else 'n']==(240 if v==725 else 840),'summary sample count')
  metrics={}
  for col,key in COLS[v]:
   s=scores(rs,col); saved=summary[key]
   require(type(saved) in (float,int) and math.isfinite(saved),'nonfinite/malformed summary')
   require(s['v725_formula' if v==725 else 'v737_row_means_formula']==saved,'saved AUC mismatch: '+col)
   s['archived_auc']=saved; metrics[col]=s
  pairs={}
  for r in rs:pairs.setdefault(r['pair_id'],[]).append(r)
  require(all(float(pair[0][c])==float(pair[1][c]) for pair in pairs.values() for c in ('passive_mean','passive_curvature')),'passive paired equality')
  result[str(v)]={'rows':len(rs),'pairs':len(pairs),'metrics':metrics}
 return {'scope':'Saved main rows only. No generators, gaps, scans, dynamics or physical certification. Stdlib binary64 reduction emulation is scoped to these arrays.','input_sha256':identities,'datasets':result}

def mutations(data):
 evidence=[]
 csvkey='v725_main_metrics.csv'; lines=data[csvkey].decode().splitlines();header=lines[0].split(',')
 def changed(cell,value):
  row=lines[1].split(',');row[header.index(cell)]=value
  return ('\n'.join([lines[0],','.join(row)]+lines[2:])+'\n').encode()
 cases=[('missing_row',('\n'.join(lines[:-1])+'\n').encode(),True),('duplicate_row',('\n'.join(lines+[lines[1]])+'\n').encode(),True),('substituted_pair',('\n'.join([lines[0],lines[3]]+lines[2:])+'\n').encode(),True),('wrong_label',changed('label','1'),True),('malformed_label',changed('label','0.0'),True),('nonfinite',changed('passive_mean','nan'),True),('malformed_numeric',changed('adm_z','not-a-number'),True),('finite_score_substitution',changed('adm_z','999'),True)]
 for name,b,semantic in cases:
  d=dict(data);d[csvkey]=b
  for auth in (True,False):
   try:analyze(d,auth)
   except (ValueError,KeyError,TypeError) as e:evidence.append({'case':name,'layer':'identity' if auth else 'semantic','result':'REJECTED','reason':str(e)})
   else:raise AssertionError('mutation escaped: '+name)
 for name,value in [('wrong_result',0.125),('nonfinite_result',float('nan'))]:
  d=dict(data);obj=json.loads(d['v725_results.json']);obj['summary']['adm_z_auc']=value;d['v725_results.json']=json.dumps(obj).encode()
  for auth in (True,False):
   try:analyze(d,auth)
   except (ValueError,KeyError,TypeError) as e:evidence.append({'case':name,'layer':'identity' if auth else 'semantic','result':'REJECTED','reason':str(e)})
   else:raise AssertionError('mutation escaped: '+name)
 # Deliberate rank-preserving mutation: semantic AUC is not byte identity.
 d=dict(data);d[csvkey]=changed('adm_z','-999')
 try:analyze(d,True)
 except ValueError as e:evidence.append({'case':'rank_preserving_substitution','layer':'identity','result':'REJECTED','reason':str(e)})
 else:raise AssertionError('identity accepted substituted bytes')
 analyze(d,False)
 evidence.append({'case':'rank_preserving_substitution','layer':'semantic','result':'ACCEPTED_AS_EXPECTED','reason':'rank invariance cannot authenticate bytes; mandatory identity gate does'})
 return evidence

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--data-dir',type=Path,default=Path(__file__).parent/'data');ap.add_argument('--output',type=Path);ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 data={k:(args.data_dir/k).read_bytes() for k in HASHES};out=analyze(data)
 if args.self_test:out['negative_controls']=mutations(data)
 out['result']='PASS';s=json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+'\n'
 if args.output:args.output.write_text(s)
 else:print(s,end='')
if __name__=='__main__':main()
