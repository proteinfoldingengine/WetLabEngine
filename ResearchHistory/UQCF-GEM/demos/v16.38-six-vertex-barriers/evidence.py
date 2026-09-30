"""Package source and execution evidence; verify durable manifests fail-closed."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tarfile,io,gzip
HERE=Path(__file__).resolve().parent
REPO=Path.cwd()

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,indent=2)+'\n'
def source_paths():
 paths=set((REPO/'ResearchHistory/UQCF-GEM').rglob('*.py'))|{p for p in HERE.glob('*.md') if p.name!='REPORT.md'}
 paths.add(REPO/'ResearchHistory/UQCF-GEM/AGENTS.md')
 paths.add(REPO/'docs/superpowers/plans/2026-09-30-v1638-certification.md')
 paths.add(REPO/'.github/workflows/uqcf-v1638-certification.yml')
 for line in (HERE/'inherited.txt').read_text().splitlines():
  if line.strip():
   root=REPO/line.strip();folder=root.parent.parent if root.parent.name=='tests' else root.parent;paths.update(folder.rglob('*.py'));paths.update(folder.rglob('*.json'))
 paths.update(p for p in (REPO/'ResearchHistory/UQCF-GEM').rglob('*.json') if HERE not in p.parents)
 paths.add(HERE/'inherited.txt')
 paths.add(HERE.parent/'v16.37-certified-closure/evidence/science/scientific/CERTIFICATE.json.gz')
 paths.add(HERE.parent/'v16.37-certified-closure/PROOFS.md')
 paths.add(HERE.parent/'v16.37-certified-closure/PREREGISTRATION.md')
 return sorted(p for p in paths if p.is_file())

def package(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 if head!=os.environ['GITHUB_SHA']:raise ValueError('checkout/trigger SHA mismatch')
 if os.environ['GITHUB_WORKFLOW_SHA']!=head:raise ValueError('workflow/source SHA mismatch')
 pre='53b20c929ee07ce732c2f8e3889c4dea0a8749c8';parent='694ed90ca853da205f83afb0ee60865a47477289'
 subprocess.run(['git','merge-base','--is-ancestor',pre,head],check=True)
 if subprocess.check_output(['git','show','-s','--format=%P',pre],text=True).strip()!=parent:raise ValueError('registration parent')
 if digest(HERE/'PREREGISTRATION.md')!='ffe75a69ddc2bde8b924684c4aa3fd0ea94680c6bf3a8868fc1ac6600e30bdf5':raise ValueError('registration content changed')
 metadata={'head':head,'trigger_sha':os.environ['GITHUB_SHA'],'workflow_sha':os.environ['GITHUB_WORKFLOW_SHA'],'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'python':sys.version,'platform':sys.platform,'phase':os.environ.get('PHASE','science'),'preregistration_commit':'53b20c929ee07ce732c2f8e3889c4dea0a8749c8','integrated_parent':'694ed90ca853da205f83afb0ee60865a47477289'}
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
