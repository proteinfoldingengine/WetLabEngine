#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/'SUMMARY.json').read_text())
assert s['version']=='v13.24'
d=s['deletion_audit']
assert d['total_claims']==24
assert d['qrsl_independent_count']==21
assert d['qrsl_dependent_count']==3
a=s['adjudication']
assert a['QRSL_failure_invalidates_finite_scale_QMAR'] is False
assert a['QRSL_failure_invalidates_internal_PathA_ADM_assembly'] is False
assert a['QRSL_failure_blocks_native_quantum_continuum_refinement_interpretation'] is True
assert a['RATS_remains_sealed'] is True
p=s['pathA_after_qrsl']
assert p['internal_ADM_like_Hamiltonian']=='PRESERVED_CLOSED_INTERNAL'
assert p['physical_stress_energy_identification']=='OPEN'
n=s['highest_leverage_independent_bridge']
assert n['name'].startswith('RSLB') and n['requires_qrsl'] is False
assert s['status']['Pillar_3']=='OPEN'
assert s['status']['scientific_breakthrough'] is False
print('V13_24_CHECKER_PASS')
