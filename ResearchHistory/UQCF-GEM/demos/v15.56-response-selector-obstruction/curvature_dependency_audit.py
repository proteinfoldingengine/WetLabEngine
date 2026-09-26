"""Audit whether the existing archive supplies the objects needed to turn the
new finite matched-completion holonomy response into a curvature-density limit.
This is a dependency classifier, not a curvature construction.
"""
import holonomy_curvature_gate as hg
REQUIRED={
 'canonical_oriented_area_or_bivector':False,
 'lawful_shrinking_loop_family_bound_to_completion_fixture':False,
 'controlled_area_to_zero_limit':False,
 'compatible_log_holonomy_branch_across_refinement':False,
 'ontology_native_state_refinement_selecting_completion_tower':False,
}
ARCHIVE={
 'v13_04_CRCL_AVT':{'typed_object':'log(H)/A and vertical holonomy twists','status':'CONDITIONAL_CURVATURE_REGULARITY_STACK','supplies_missing_objects':False},
 'v13_06_LCM_refinement':{'typed_object':'metric/solder-compatible finite refinement','status':'EXISTS_BUT_NOT_SELECTED_BY_GENERIC_ARCHITECTURE','supplies_missing_objects':False},
 'v15_45_periodic_square':{'typed_object':'finite differentiated-holonomy operator on L5/L7','status':'FINITE_OPERATOR_ONLY_NO_CONTINUUM_TREND','supplies_missing_objects':False},
 'v13_27_peer_boundary':{'typed_object':'finite SO(3) loop diagnostic','status':'EXPLICITLY_REQUIRES_LOOP_AREA_AND_CONTROLLED_REFINEMENT_FOR_CURVATURE','supplies_missing_objects':False},
}
def run():
 h=hg.run()
 return {'schema':'uqcf-curvature-dependency-audit-v1','baseline':'9362454146c62b688bb25ce4ce8ed2f7f3b0caa0',
 'finite_holonomy_gate_passed':h['finite_holonomy_response_certified'],
 'required_objects':REQUIRED,'archive_candidates':ARCHIVE,
 'all_required_objects_earned':all(REQUIRED.values()),
 'verdict':'CURVATURE_LIMIT_BRIDGE_BLOCKED_BY_MISSING_NATIVE_AREA_AND_REFINEMENT',
 'next_legal_move':'derive an ontology-native area/bivector and completion-compatible shrinking-loop refinement, or stop this curvature branch',
 'posthoc_fit':False,'claims':{'curvature_density_derived':False,'continuum_limit_derived':False,'gravity_signal':False}}
if __name__=='__main__':
 import json; print(json.dumps(run(),indent=2,sort_keys=True))
