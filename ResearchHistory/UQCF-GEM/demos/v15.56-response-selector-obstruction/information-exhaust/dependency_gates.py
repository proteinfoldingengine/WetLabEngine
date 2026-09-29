"""16.17-16.18 fail-closed dependency adjudication."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def adjudicate_1617(added_dimension):
 return 'FORCED_STRUCTURE_NOT_IDENTIFIED' if added_dimension==0 else 'NONTRIVIAL_INFORMATION_REQUIRES_CLASSIFICATION'
def adjudicate_1618(v1617):
 return 'DEPENDENCY_BLOCKED_NO_NATIVE_STRUCTURE' if v1617=='FORCED_STRUCTURE_NOT_IDENTIFIED' else 'CURVATURE_CONTINUATION_NOT_YET_ADJUDICATED'
def audit():
 r=json.loads((HERE/'result.json').read_text()) if (HERE/'result.json').exists() else None
 if r is None or r.get('version')!='16.16' or not r.get('all_valid'): raise ValueError('valid 16.16 result required')
 d=r['metrics']['network_additional_pairs']
 v17=adjudicate_1617(d)
 v18=adjudicate_1618(v17)
 return {'version':'16.17-16.18','all_valid':True,'v16.16_verdict':r['verdict'],'v16.16_network_additional_pairs':d,'v16.17_verdict':v17,'v16.18_verdict':v18,'geometry_inserted':False}
if __name__=='__main__':
 out=audit();(HERE/'dependency-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
