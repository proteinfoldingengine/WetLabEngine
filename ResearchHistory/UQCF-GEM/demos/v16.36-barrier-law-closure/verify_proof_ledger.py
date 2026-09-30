import json,pathlib
p=pathlib.Path(__file__).parent
proof=(p/'PROOFS.md').read_text()
required=['P1 — Candidate signature','P2 — Exact meaning','P3 — Why bounded agreement','P4 — What would refute','P5 — What would establish','P6 — Five-vertex ultrametric','P7 — Evidence levels','P8 — Physical interpretation']
for x in required:
 if x not in proof: raise SystemExit('missing proof section: '+x)
d=json.loads((p/'PRODUCTION.json').read_text())
assert d['gate_d']=='UNRESOLVED'
assert d['gate_e']=={'excluded':[],'scope':'BOUNDED','tested_cases':27,'ultrametric_violations':0}
assert len(d['pairs'])==18
e=json.loads((p/'PUBLICATION_EVIDENCE.json').read_text())
assert e['closure']=='FINAL' and e['fresh_bytes_equal'] is True
assert e['scientific_run']==36665282860 and e['publication_run']=='36665735865'
print({'proof_sections':8,'pairs':18,'gate_d':d['gate_d'],'gate_e':d['gate_e'],'prior_publication_verified':True})
