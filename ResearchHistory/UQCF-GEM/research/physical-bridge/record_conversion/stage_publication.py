"""Build reviewable publication entries; does not mutate GitHub."""
import hashlib,json,pathlib
P=pathlib.Path(__file__).parent;B='ResearchHistory/UQCF-GEM/research/physical-bridge/';D=B+'record_conversion/'
files={}
for n in ['CLOSEOUT.md','RECONCILIATION.md','PUBLICATION_REVIEW.md','binding.json','freeze_binding.json','freeze_manifest.json','freeze_recheck.json','scientific_manifest.json','scientific_readbacks.json','binary_entries.json','progress.md','author_reconciliation.json','audit_originals.py','test_original_audit.py','audit_originals.log','audit_controls.log','audit_red.log','audit_red_first.log','prepublish_tests.log','independent.json','native_check.json','certificate.json','stage_publication.py']:
 files[D+n]=P/n
for f in (P/'originals').iterdir():
 if f.suffix!='.zip':files[D+'originals/'+f.name]=f
for phase in ('conversion-review','conversion-publication'):
 for f in (P/'publication_evidence'/phase).iterdir():files[D+'publication_evidence/'+phase+'/'+f.name]=f
for name in ('publication_gate.json','file_manifest.json','reproduction.json','provenance.json'):
 files[D+'publication_evidence/conversion-gate/'+name]=P/'publication_evidence/conversion-gate'/name
files[B+'COUPLED_C3_RECORD_CONVERSION_CLOSEOUT.md']=P/'CLOSEOUT.md'
for f in (P/'indices_updated').iterdir():files[B+f.name]=f
entries=[];manifest=[]
for path,f in sorted(files.items()):
 data=f.read_bytes();git=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 entries.append({'path':path,'mode':'100644','type':'blob','content':data.decode()});manifest.append({'path':path,'local':str(f),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':git})
for x in json.loads((P/'binary_entries.json').read_text()):
 f=P/'originals'/x['file'];data=f.read_bytes();git=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if git!=x['git_blob']:raise ValueError('binary local identity changed')
 path=D+'originals/'+f.name;entries.append({'path':path,'mode':'100644','type':'blob','sha':git});manifest.append({'path':path,'local':str(f),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':git,'binary':True})
(P/'publication_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
entries.append({'path':D+'publication_manifest.json','mode':'100644','type':'blob','content':(P/'publication_manifest.json').read_text()})
(P/'publication_entries.json').write_text(json.dumps(entries))
# Bounded transport batches; no shell command embeds the entire packet.
for i in range(0,len(entries),5):(P/f'publish_batch_{i//5:02d}.json').write_text(json.dumps(entries[i:i+5]))
print(json.dumps({'text_files':sum('content' in e for e in entries),'binary_files':sum('sha' in e for e in entries),'bytes':sum(m['bytes'] for m in manifest),'batches':(len(entries)+4)//5}))
