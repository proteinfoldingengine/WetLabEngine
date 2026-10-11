"""Stage concrete audited closeout; does not itself publish or claim closure."""
import hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent;B='ResearchHistory/UQCF-GEM/research/physical-bridge/';E=B+'evidence/reserve-activation/'
binding=json.loads((P/'binding.json').read_text());audit=json.loads((P/'author_reconciliation.json').read_text());controls=json.loads((P/'author_audit_controls.json').read_text());assert audit['status']=='ACCEPTED_AUTHOR_RECONCILIATION' and controls['status']=='ACCEPTED'
m={n:B+'COUPLED_C3_RESERVE_ACTIVATION_'+n for n in ['CLOSEOUT.md','RECONCILIATION.md','PUBLICATION_AUDIT.md']}
for n in ['COUPLED_C3_C4_DEFICIT_CONTINUATION.md','POST_A12_THEOREM_FIRST_SYNTHESIS.md']:m[n]=B+n
names=['binding.json','freeze_binding.json','scientific_binding.json','scientific_readback.json','scientific_manifest.json','review_inputs.json','author_reconciliation.json','author_audit_controls.json','audit_originals.py','test_original_audit.py','reassemble_archives.py','audit_originals.log','audit_controls.log','PLAN_CURRENT.md','progress.md','CURRENT_STATUS.md','stage_publication.py','binary_entries.json','binary_upload_plan.json','source_readbacks.json','CODE_REVIEW.md','fresh_comparison.json','audit_originals_attempt1_failure.log','audit_controls_attempt1_failure.log','truncated_fresh_job.log','log_transport_failure.json']
for n in names:m[n]=E+n
for folder in ['originals','publication_evidence']:
 for f in sorted((P/folder).iterdir()):
  if f.suffix in ['.json','.log','.txt','.md']:m[folder+'/'+f.name]=E+folder+'/'+f.name
if (P/'immutable_readback.json').exists():m['immutable_readback.json']=E+'immutable_readback.json'
e=[dict(path=path,mode='100644',type='blob',content=(P/local).read_text()) for local,path in m.items()];binary=json.loads((P/'binary_entries.json').read_text());hashes={x['path']:hashlib.sha256(x['content'].encode()).hexdigest() for x in e}
for n,t in json.loads((P/'review_inputs.json').read_text())['documents'].items():hashes[B+n]=hashlib.sha256(t.encode()).hexdigest()
for row in binary:hashes[row['path']]=hashlib.sha256((P/'originals'/row['path'].split('/')[-1]).read_bytes()).hexdigest()
manifest={'scientific_commit':binding['scientific_commit'],'workflow_run':binding['workflow_run'],'sha256':hashes,'binary_git_blobs':{row['path']:row['sha'] for row in binary},'archive_representation':'Original unmodified ZIPs, no repacking'};text=json.dumps(manifest,indent=2,sort_keys=True)+'\n';(P/'publication_hash_manifest.json').write_text(text);e.append(dict(path=E+'publication_hash_manifest.json',mode='100644',type='blob',content=text));(P/'publication_entries.json').write_text(json.dumps(e)+'\n');print(len(e),'texts;',len(binary),'original ZIP blobs')
