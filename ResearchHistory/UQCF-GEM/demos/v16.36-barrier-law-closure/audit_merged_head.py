import json,pathlib,subprocess,sys
EXPECTED='ce4f0c0396fc4a763e5fac1826c180df599d9a00'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head==EXPECTED,(head,EXPECTED)
p=pathlib.Path('ResearchHistory/UQCF-GEM/demos/v16.36-barrier-law-closure')
for f in ['PROOFS.md','PUBLICATION_EVIDENCE.json','PROOF_CLOSURE_EVIDENCE.json','PAIR_COMPLETENESS_EVIDENCE.json','PRODUCTION.json','verifier.py','test_gate.py']:
 assert (p/f).exists(),f
d=json.loads((p/'PRODUCTION.json').read_text());assert d['gate_d']=='UNRESOLVED';assert d['gate_e']['tested_cases']==27 and d['gate_e']['excluded']==[] and d['gate_e']['ultrametric_violations']==0
pc=json.loads((p/'PAIR_COMPLETENESS_EVIDENCE.json').read_text());assert pc['full_inherited_stack'] is True
sys.path.insert(0,str(p.resolve()));import producer,verifier
fresh=producer.produce(4);r=verifier.verify_document(fresh)
assert r['execution_status']=='COMPLETED';assert len(fresh['pairs'])==18
print({'merged_head':head,'canonical_pairs':18,'gate_d':fresh['gate_d'],'gate_e':fresh['gate_e'],'audit':'PASS'})
