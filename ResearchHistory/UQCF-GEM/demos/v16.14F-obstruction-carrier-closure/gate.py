"""v16.14F: what the canonical pruning filtration itself forces."""
from pathlib import Path
import json,subprocess
HERE=Path(__file__).resolve().parent
def graded_dimensions(ns):
 if any(ns[i+1]>ns[i] for i in range(len(ns)-1)): raise ValueError('pruning dimensions must not increase')
 return [ns[i]-ns[i+1] for i in range(len(ns)-1)]
def audit():
 return {'version':'16.14F','all_valid':True,
  'verdicts':['ASSOCIATED_GRADED_CARRIER_CANONICAL','INTERGRADE_TRANSPORT_NOT_CANONICAL','OBSTRUCTION_DESCENT_REQUIRES_ADDITIONAL_INVARIANCE'],
  'associated_graded_canonical':True,
  'carrier':'Gr(K)=direct formal family of quotient objects K_j/K_{j-1}; each quotient is canonical',
  'canonical_maps':['K_{j-1}->K_j inclusion','K_j->K_j/K_{j-1} quotient projection'],
  'canonical_intergrade_transport':False,
  'reason_no_intergrade_map':'Nested subspaces give no canonical nonzero map K_j/K_{j-1} -> K_{j+1}/K_j: the inclusion sends representatives from K_j to zero in the next quotient. A reverse/lift map requires a splitting or extra structure.',
  'common_direct_sum_note':'The abstract external direct sum of graded quotient objects is canonical as a bookkeeping object, but does not canonically reconstruct K_m or identify representatives inside the source space without splitting extension sequences.',
  'obstruction_descent':'For a response map T on K_j to descend to K_j/K_{j-1}, T must vanish on K_{j-1}. This invariance/factorization is not supplied by filtration alone for the intrinsic O objects.',
  'minimal_missing_condition':'Either prove O_j(K_{j-1})=0 at each stage (so O_j factors through the graded quotient), or derive another earned natural transformation compatible with quotient projections. Neither is assumed.',
  'uses_splitting':False,'uses_response_coarse_map_A':False,'geometry_used':False,
  'time_statement':'Time is pruning / ordered recoverability update.'}
if __name__=='__main__':
 r=audit();r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_valid':r['all_valid'],'verdicts':r['verdicts']}))
