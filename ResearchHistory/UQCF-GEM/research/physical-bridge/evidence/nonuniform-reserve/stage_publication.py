import pathlib,json,hashlib
P=pathlib.Path(__file__).parent;BASE='ResearchHistory/UQCF-GEM/research/physical-bridge/';E=BASE+'evidence/nonuniform-reserve/'
mapping={
 'CLOSEOUT.md':BASE+'COUPLED_C3_NONUNIFORM_RESERVE_CLOSEOUT.md',
 'RECONCILIATION.md':BASE+'COUPLED_C3_NONUNIFORM_RESERVE_RECONCILIATION.md',
 'PUBLICATION_AUDIT.md':BASE+'COUPLED_C3_NONUNIFORM_RESERVE_PUBLICATION_AUDIT.md',
 'COUPLED_C3_C4_DEFICIT_CONTINUATION.md':BASE+'COUPLED_C3_C4_DEFICIT_CONTINUATION.md',
 'POST_A12_THEOREM_FIRST_SYNTHESIS.md':BASE+'POST_A12_THEOREM_FIRST_SYNTHESIS.md',
 'review_inputs.json':E+'review_input_readbacks.json'}
for n in ['binding.json','freeze_binding.json','scientific_binding.json','counts.json','author_reconciliation.json','author_audit_controls.json','audit_originals.py','test_original_audit.py','reassemble_archives.py','audit_originals.log','audit_controls.log','transport_failures.json','reassembly_verification.json','prepublication_evidence_check.json','roadmap_source_readbacks.json','PLAN.md','progress.md']:mapping[n]=E+n
for p in (P/'originals').iterdir():
 if p.suffix in ('.json','.log'):mapping['originals/'+p.name]=E+p.name
mapping['publication_runtime_observation.json']=E+'publication_runtime_observation.json'
if (P/'immutable_readback.json').exists():mapping['immutable_readback.json']=E+'immutable_readback.json'
for n in ['stage_publication.py','prepare_archive_segments.py','binary_entries.json','binary_upload_plan.json']:
 mapping[n]=E+n
for p in (P/'publication_evidence').iterdir():mapping['publication_evidence/'+p.name]=E+p.name
entries=[dict(path=target,mode='100644',type='blob',content=(P/local).read_text()) for local,target in mapping.items()]
binary=json.loads((P/'binary_entries.json').read_text())
hashes={e['path']:hashlib.sha256(e['content'].encode()).hexdigest() for e in entries}
# Bind the immutable scientific source/proof/report inputs as well as publication texts.
for n,txt in json.loads((P/'review_inputs.json').read_text())['documents'].items():hashes[BASE+n]=hashlib.sha256(txt.encode()).hexdigest()
for e in binary:hashes[e['path']]=hashlib.sha256((P/'originals'/e['path'].split('/')[-1]).read_bytes()).hexdigest()
manifest=dict(scientific_commit='72551789ce372e2bbe89916b41ec1f884c983aea',workflow_run=38092297156,sha256=hashes,binary_git_blobs={e['path']:e['sha'] for e in binary},archive_representation='Original ZIP bytes preserved by ordered segments described in archive_segments.json; small review ZIPs remain whole')
content=json.dumps(manifest,indent=2,sort_keys=True)+'\n';(P/'publication_hash_manifest.json').write_text(content);entries.append(dict(path=E+'publication_hash_manifest.json',mode='100644',type='blob',content=content))
(P/'publication_entries.json').write_text(json.dumps(entries,indent=2)+'\n');print('Publication texts',len(entries),'binary entries',len(binary))
