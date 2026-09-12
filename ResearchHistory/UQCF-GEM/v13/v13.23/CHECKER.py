#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.23'
e=s['executed_pair']
assert e['coarse_recovery_error']<1e-14
assert abs(e['fine_state_trace_distance']-.2)<1e-12
assert e['ancilla_support_ranks']==[8,8]
assert e['preselection_descriptor_identical'] is True
assert e['fine_only_descriptor_different'] is True
for v in s['candidate_audit'].values():
    assert v['result']=='NO_SELECTOR'
a=s['adjudication']
assert a['QRSL_from_current_frozen_ontology'] is False
assert a['RATS_execution_authorized'] is False
assert s['status']['QRSL_ORIGIN_SEARCH']=='STOP'
assert s['status']['scientific_breakthrough'] is False
print('V13_23_CHECKER_PASS')
