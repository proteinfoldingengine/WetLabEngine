from pathlib import Path
import hashlib,json,os,shutil,sys,urllib.request,urllib.error,zipfile,subprocess
HERE=Path(__file__).resolve().parent
ROOT=Path.cwd()

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
def get(url,auth=True):
 headers={'Accept':'application/vnd.github+json'}
 if auth:headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args):return None
 try:return urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url,headers=headers)).read()
 except urllib.error.HTTPError as e:
  if e.code not in (301,302,303,307,308):raise
  return urllib.request.urlopen(e.headers['Location']).read()

def download(run,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 api='https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']
 artifacts=json.loads(get(api+'/actions/runs/'+run+'/artifacts'))['artifacts']
 wanted=[a for a in artifacts if a['name'].startswith('v1637-science-')]
 if len(wanted)!=1:raise ValueError('unique scientific artifact required')
 a=wanted[0];archive=out/'science-artifact.zip';archive.write_bytes(get(a['archive_download_url']))
 if a.get('digest')!='sha256:'+sha(archive):raise ValueError('artifact ZIP digest')
 dump(out/'ARTIFACT_METADATA.json',a)
 with zipfile.ZipFile(archive) as z:
  if z.testzip() is not None:raise ValueError('artifact ZIP CRC')
  for name in z.namelist():
   if Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('artifact path')
  z.extractall(out/'science')
 jobs=json.loads(get(api+'/actions/runs/'+run+'/jobs'))['jobs']
 science=[j for j in jobs if j['name']=='science']
 if len(science)!=1 or science[0]['conclusion']!='success':raise ValueError('science job success')
 dump(out/'SCIENCE_JOB.json',science[0]);(out/'SCIENCE_JOB.log').write_bytes(get(api+'/actions/jobs/'+str(science[0]['id'])+'/logs'))
 print(json.dumps({'artifact_id':a['id'],'zip_sha256':sha(archive),'digest_verified':True}))

def scientific_equal(a,b):
 expected={'CERTIFICATE.json.gz','SUMMARY.json','VERIFY.json'}
 if {x.name for x in Path(a).iterdir()}!=expected or {x.name for x in Path(b).iterdir()}!=expected:raise ValueError('scientific file membership')
 for name in sorted(expected):
  if (Path(a)/name).read_bytes()!=(Path(b)/name).read_bytes():raise ValueError('reproduction differs '+name)
 print('SCIENTIFIC_BYTES_IDENTICAL')

def members():
 files={p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=HERE/'MANIFEST.json'}
 files.update([ROOT/'ResearchHistory/UQCF-GEM/AGENTS.md',ROOT/'docs/superpowers/plans/2026-09-30-v1637-certification.md',ROOT/'.github/workflows/uqcf-v1637-certification.yml'])
 return sorted(files)

def finalize():
 e=HERE/'evidence';s=json.loads((e/'science/scientific/SUMMARY.json').read_text())
 report='# v16.37 prospective certification results\n\nPrimary outcome: **'+s['outcome']+'**. Universal unit law: **UNRESOLVED**.\n\n'+json.dumps(s['summary'],indent=2)+'\n\nAll declared cases and canonical component/endpoint identities were independently reconstructed. Three independent scalar barriers and LEX_BARRIER were checked with exact path/lower-threshold certificates. See PROOFS.md for general arguments and the finite/universal distinction.\n\nScientific artifact, API digest/CRC verification, raw certificate, source snapshots, execution logs, source manifests and fresh publication reproduction are committed under evidence/. Scientific bytes match exactly. Full inherited commands are listed in inherited.txt and their logs are in both execution packages.\n\nThis report records scientific/publication completion; numbered-stage closure additionally requires successful audit of the actual merge SHA. The final PR and audit receipt identify that merge and audit run.\n'
 (HERE/'REPORT.md').write_text(report)
 dump(HERE/'MANIFEST.json',{str(p.relative_to(ROOT)):sha(p) for p in members()})
 verify()

def verify():
 d=json.loads((HERE/'MANIFEST.json').read_text())
 if set(d)!={str(p.relative_to(ROOT)) for p in members()}:raise ValueError('publication manifest membership')
 for p,h in d.items():
  if sha(ROOT/p)!=h:raise ValueError('publication hash '+p)
 # Bind source manifests to the current executed source; documentation may have been added later.
 for phase in ('science','reproduction'):
  src=json.loads((HERE/'evidence'/phase/'SOURCE_MANIFEST.json').read_text())
  for p,h in src.items():
   if p.endswith('.py') and sha(ROOT/p)!=h:raise ValueError('executed source drift '+p)
 print(json.dumps({'publication_manifest':'VERIFIED','members':len(d)}))

if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='download':download(sys.argv[2],sys.argv[3])
 elif cmd=='equal':scientific_equal(sys.argv[2],sys.argv[3])
 elif cmd=='finalize':finalize()
 elif cmd=='verify':verify()
 else:raise ValueError(cmd)
