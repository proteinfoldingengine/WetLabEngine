from pathlib import Path
import gzip,hashlib,json,subprocess,sys,tempfile
import campaign
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'v16.38-six-vertex-barriers'
def enc(d):return (json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode()
def run(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as fresh:
  subprocess.run([sys.executable,str(PARENT/'run_campaign.py'),fresh],check=True)
  for name in ('CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json'):
   if (Path(fresh)/name).read_bytes()!=(PARENT/'evidence/science/scientific'/name).read_bytes():raise ValueError('parent scientific bytes differ '+name)
  base=json.loads(gzip.decompress((Path(fresh)/'CERTIFICATE.json.gz').read_bytes()))
 if base['bound']!=6 or base['view_counts']!=[1,2,3] or len(base['graphs'])!=111:raise ValueError('frozen canonical domain')
 print('PARENT_SCIENTIFIC_BYTES_IDENTICAL',flush=True)
 doc=campaign.produce(base);checked=campaign.verify(base,doc)
 checked['parent_scientific_bytes_identical']=True
 raw=enc({'canonical':base,'experiment':doc})
 with (out/'CERTIFICATE.json.gz').open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as z:z.write(raw)
 summary={key:doc[key] for key in ('campaign','summary','outcome','obstruction_outcome','universal_unit_law')}
 summary.update(raw_sha256=hashlib.sha256(raw).hexdigest(),raw_bytes=len(raw))
 (out/'SUMMARY.json').write_bytes(enc(summary));(out/'VERIFY.json').write_bytes(enc(checked))
 print(json.dumps(summary,sort_keys=True),flush=True)
if __name__=='__main__':run(sys.argv[1])
