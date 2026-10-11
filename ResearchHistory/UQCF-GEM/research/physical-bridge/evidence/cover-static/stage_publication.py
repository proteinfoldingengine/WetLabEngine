"""Stage text and unchanged binary identities for leased publication."""
import pathlib,json,hashlib
P=pathlib.Path(__file__).parent;BASE='ResearchHistory/UQCF-GEM/research/physical-bridge/';E=BASE+'evidence/cover-static/'
mapping={n:BASE+'COUPLED_C3_COVER_STATIC_'+n for n in ['CLOSEOUT.md','RECONCILIATION.md','PUBLICATION_AUDIT.md']}
for n in ['COUPLED_C3_C4_DEFICIT_CONTINUATION.md','POST_A12_THEOREM_FIRST_SYNTHESIS.md']:mapping[n]=BASE+n
names=['binding.json','freeze_binding.json','scientific_binding.json','scientific_readback.json','running_readback.json','scientific_manifest.json','review_inputs.json','counts.json','author_reconciliation.json','author_audit_controls.json','audit_originals.py','test_original_audit.py','reassemble_archives.py','audit_originals.log','audit_controls.log','reassembly_verification.json','PLAN.md','progress.md','CURRENT_STATUS.md','stage_publication.py','prepare_archive_segments.py','binary_entries.json','binary_upload_plan.json','source_readbacks.json','verify_publication_readback.py']
for n in names:mapping[n]=E+n
for f in (P/'originals').iterdir():
 if f.suffix in ('.json','.log'):mapping['originals/'+f.name]=E+f.name
for f in (P/'publication_evidence').iterdir():mapping['publication_evidence/'+f.name]=E+f.name
if (P/'immutable_readback.json').exists():mapping['immutable_readback.json']=E+'immutable_readback.json'
entries=[dict(path=target,mode='100644',type='blob',content=(P/local).read_text()) for local,target in mapping.items()]
binary=json.loads((P/'binary_entries.json').read_text())
hashes={e['path']:hashlib.sha256(e['content'].encode()).hexdigest() for e in entries}
for name,txt in json.loads((P/'review_inputs.json').read_text())['documents'].items():hashes[BASE+name]=hashlib.sha256(txt.encode()).hexdigest()
for e in binary:hashes[e['path']]=hashlib.sha256((P/'originals'/e['path'].split('/')[-1]).read_bytes()).hexdigest()
manifest=dict(scientific_commit='6259573656b9a5fc6ed7b71c5fcede5c9047526a',workflow_run=38101841497,sha256=hashes,binary_git_blobs={e['path']:e['sha'] for e in binary},archive_representation='Original ZIP bytes; two larger ZIPs in ordered unchanged four-million-byte segments, small reviews whole')
content=json.dumps(manifest,indent=2,sort_keys=True)+'\n';(P/'publication_hash_manifest.json').write_text(content);entries.append(dict(path=E+'publication_hash_manifest.json',mode='100644',type='blob',content=content))
(P/'publication_entries.json').write_text(json.dumps(entries)+'\n');print('Publication texts',len(entries),'binary entries',len(binary))
