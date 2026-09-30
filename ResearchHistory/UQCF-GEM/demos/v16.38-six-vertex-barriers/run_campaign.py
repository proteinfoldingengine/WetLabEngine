from pathlib import Path
import gzip,hashlib,json,sys,importlib.util
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'v16.37-certified-closure'
sys.path.insert(0,str(PARENT))
import producer,verifier
spec=importlib.util.spec_from_file_location('parent_runner',PARENT/'run_campaign.py')
parent_runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent_runner)
sys.path.pop(0)

def compare_parent(d,old,bound=5):
 def keyed(doc):
  graphs=[g for g in doc['graphs'] if len(g['parents'])<=bound]
  keys=[(tuple(g['parents']),g['views']) for g in graphs]
  if len(keys)!=len(set(keys)):raise ValueError('duplicate inherited graph')
  return dict(zip(keys,graphs))
 if keyed(d)!=keyed(old):raise ValueError('complete inherited graph records differ')

def validate_domain(d):
 if d.get('version')!='16.37' or type(d.get('bound')) is not int or d['bound']!=6 or d.get('view_counts')!=[1,2,3]:
  raise ValueError('campaign schema/domain')

def run(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 d=producer.produce(6);validate_domain(d)
 print('PRODUCTION_COMPLETE',flush=True)
 v=verifier.verify(d,6)
 if len(d['graphs'])!=111:raise ValueError('expected complete graph count')
 old=json.loads(gzip.decompress((PARENT/'evidence/science/scientific/CERTIFICATE.json.gz').read_bytes()))
 compare_parent(d,old)
 old18=json.loads((HERE.parent/'v16.36-barrier-law-closure/PRODUCTION.json').read_text())
 parent_runner.compare_historical(d,v,old18)
 v.update(campaign='16.38',complete_parent_graph_equality=True,inherited_exact_identity_equality=True,inherited_barrier_value_equality=True)
 raw=parent_runner.encoded(d)
 with (out/'CERTIFICATE.json.gz').open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as gz:gz.write(raw)
 summary={'campaign':'16.38','certificate_schema':'inherited-v16.37','bound':6,'outcome':d['outcome'],'summary':d['summary'],'universal_unit_law':d['universal_unit_law'],'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw)}
 (out/'SUMMARY.json').write_bytes(parent_runner.encoded(summary))
 (out/'VERIFY.json').write_bytes(parent_runner.encoded(v))
 print(json.dumps(summary,sort_keys=True),flush=True)

if __name__=='__main__':run(sys.argv[1])
