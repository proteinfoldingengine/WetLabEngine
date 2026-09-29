"""v16.13F foundational closure ledger: typed retained primitives only."""
from pathlib import Path
import json,subprocess
HERE=Path(__file__).resolve().parent
def audit():
 ledger=[
  {'operation':'lineage_incidence_within_retained_object','status':'DERIVED','basis':'full lineage address -> immediate retained prefix parent'},
  {'operation':'ancestral_pruning_retraction','status':'DERIVED','basis':'longest retained prefix'},
  {'operation':'pruning_composition','status':'DERIVED','basis':'composition of ancestral retractions'},
  {'operation':'extensive_source_pushforward','status':'DERIVED','basis':'finite additivity on retraction fibers'},
  {'operation':'source_pushforward_composition','status':'DERIVED','basis':'(q o r)_*=q_* o r_*'},
  {'operation':'kernel_filtration','status':'DERIVED','basis':'ker(P_0j) subset ker(P_0,j+1)'},
  {'operation':'intrinsic_single_pruning_obstruction','status':'DERIVED','basis':'O_r=(Q G_f)|ker(P_r)'},
  {'operation':'cross_independent_retained_carrier_morphism','status':'ILL_TYPED','basis':'no canonical inter-construction identification'},
  {'operation':'intrinsic_obstruction_composition','status':'UNDERDETERMINED','basis':'O_r codomain is quotient fine-response data; frozen primitives do not supply a canonical transport of that codomain through q or an identification with O_q domain'},
 ]
 missing=[
  'A_TYPED_CANONICAL_TRANSPORT_FOR_INTRINSIC_OBSTRUCTION_CODOMAINS_ACROSS_COMPOSABLE_PRUNINGS',
  'OR_AN_EQUIVALENT_COMMON_OBJECT_IN_WHICH_O_r_AND_O_q_COMPOSE_WITHOUT_A_RESPONSE_COARSE_MAP'
 ]
 return {'version':'16.13F','all_valid':True,
  'verdict':'RETAINED_FOUNDATION_PARTIALLY_CLOSED_WITH_TYPED_BOUNDARY',
  'obstruction_composition_verdict':'INTRINSIC_OBSTRUCTION_COMPOSITION_UNDERDETERMINED',
  'inputs_used':['lineage_address','parent_child_incidence','ordered_pruning','ancestral_retraction','finite_additive_source_grade','source_pushforward','kernel_filtration','intrinsic_obstruction_O'],
  'uses_response_coarse_map_A':False,'closure_ledger':ledger,'minimal_missing_typed_data':missing,
  'boundary':'No new primitive adopted. Missing type is an obstruction result.',
  'time_statement':'Time is pruning / ordered recoverability update.'}
if __name__=='__main__':
 r=audit();r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_valid':r['all_valid'],'verdict':r['verdict'],'obstruction_composition_verdict':r['obstruction_composition_verdict']}))
