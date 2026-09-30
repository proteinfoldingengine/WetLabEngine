"""Package source and execution evidence; verify durable manifests fail-closed."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tarfile,io,gzip
HERE=Path(__file__).resolve().parent
REPO=Path.cwd()

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,indent=2)+'\n'
def source_paths():
 paths=set(HERE.glob('*.py'))|set(HERE.glob('*.md'))
 paths.add(REPO/'ResearchHistory/UQCF-GEM/AGENTS.md')
 paths.add(REPO/'docs/superpowers/plans/2026-09-30-v1637-certification.md')
 paths.add(REPO/'.github/workflows/uqcf-v1637-certification.yml')
 for line in (HERE/'inherited.txt').read_text().splitlines():
  if line.strip():
   root=REPO/line.strip();paths.update(root.parent.rglob('*.py'));paths.update(root.parent.rglob('*.json'))
 paths.add(HERE/'inherited.txt')
 return sorted(p for p in paths if p.is_file())

def package(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 metadata={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'python':sys.version,'platform':sys.platform,'phase':os.environ.get('PHASE','science'),'preregistration_commit':'b5613ec948a4acdde3fcb5d8b1d5c00255170982','integrated_parent':'8941af1e0b4e0ff1bf575aa163f557bcb35f3a4b'}
 (out/'METADATA.json').write_text(canonical(metadata))
 src=source_paths();manifest={str(p.relative_to(REPO)):digest(p) for p in src}
 (out/'SOURCE_MANIFEST.json').write_text(canonical(manifest))
 with (out/'SOURCE.tar.gz').open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as gz:
   with tarfile.open(fileobj=gz,mode='w') as tf:
    for p in src:
     data=p.read_bytes();info=tarfile.TarInfo(str(p.relative_to(REPO)));info.size=len(data);info.mode=0o644;info.mtime=0;tf.addfile(info,io.BytesIO(data))
 manifest={str(p.relative_to(out)):digest(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
 (out/'MANIFEST.json').write_text(canonical(manifest));verify(out)

def verify(out):
 out=Path(out);d=json.loads((out/'MANIFEST.json').read_text())
 actual={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
 if set(d)!=actual:raise ValueError('manifest membership')
 for p,h in d.items():
  if digest(out/p)!=h:raise ValueError('manifest hash '+p)
 print(json.dumps({'manifest':'VERIFIED','members':len(d)}))

if __name__=='__main__':
 (package if sys.argv[1]=='package' else verify)(sys.argv[2])
