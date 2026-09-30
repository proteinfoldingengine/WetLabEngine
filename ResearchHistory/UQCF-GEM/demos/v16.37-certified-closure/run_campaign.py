from pathlib import Path
import gzip,hashlib,json,sys
import producer,verifier
HERE=Path(__file__).resolve().parent

def encoded(d):return (json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode()

def run(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 d=producer.produce(5);v=verifier.verify(d,5)
 old=json.loads((HERE.parent/'v16.36-barrier-law-closure'/'PRODUCTION.json').read_text())
 prior=[]
 for r in old['pairs']:
  ends=sorted([[sum(1<<v for v in view) for view in r[x]] for x in ('a','b')])
  prior.append([r['parents'],r['view_count'],r['q'],*ends])
 if len(prior)!=len({json.dumps(x) for x in prior}) or sorted(prior)!=v['canonical_inherited_endpoint_pairs']:
  raise ValueError('independently re-enumerated inherited identities disagree')
 v['inherited_exact_identity_equality']=True
 raw=encoded(d)
 with (out/'CERTIFICATE.json.gz').open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as gz:gz.write(raw)
 (out/'SUMMARY.json').write_bytes(encoded({'outcome':d['outcome'],'summary':d['summary'],'universal_unit_law':d['universal_unit_law'],'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw)}))
 (out/'VERIFY.json').write_bytes(encoded(v))
 print((out/'SUMMARY.json').read_text(),flush=True)

if __name__=='__main__':run(sys.argv[1])
