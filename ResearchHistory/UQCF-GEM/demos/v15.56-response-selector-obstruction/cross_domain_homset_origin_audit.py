"""Audit whether primitive composition/recovery structure derives the cross-domain morphism type."""
PACKAGES={
 'P0':[],
 'P1':['composition_with_interference'],
 'P2':['convex_operational_distinguishability'],
 'P3':['noncommutative_involutive_event_composition'],
 'P12':['composition_with_interference','convex_operational_distinguishability'],
 'P13':['composition_with_interference','noncommutative_involutive_event_composition'],
 'P23':['convex_operational_distinguishability','noncommutative_involutive_event_composition'],
 'P123':['composition_with_interference','convex_operational_distinguishability','noncommutative_involutive_event_composition'],
 'P4':['composition_with_interference','convex_operational_distinguishability','noncommutative_involutive_event_composition','purification','local_tomography']}
def run():
 return {'schema':'uqcf-cross-domain-homset-origin-audit-v1','baseline':'b6c32f7a3fd1bfc17fae3f849df7abfe2a10ff38',
 'primitive_baseline':'ORDERED_RECOVERABILITY_INCIDENCE',
 'retained_leg_derived':True,'quantum_leg_derived':False,
 'tested_packages':PACKAGES,'successful_packages':[],
 'forbidden_shortcuts':['hilbert_space','matrix_algebra','qubit','born_rule','density_operator','CPTP_map','target_dimension','tensor_factor'],
 'cross_domain_homset_derived':False,
 'verdict':'CROSS_DOMAIN_MORPHISM_TYPE_NOT_DERIVED_FROM_TESTED_PRIMITIVE_LATTICE',
 'logical_scope':'finite audited primitive lattice v15.49-v15.51; not a universal impossibility theorem',
 'minimal_missing_content':['quantum carrier representation class','subsystem composition law','recovery-capable operation class','typed relation from primitive events to quantum operational morphisms'],
 'next_research_choice':'either formulate a genuinely new predeclared primitive that supplies one missing typed item, or stop the bridge program; do not infer the Hom-set from downstream success',
 'claims':{'new_primitive_adopted':False,'quantum_theory_derived':False,'gravity_derived':False}}
if __name__=='__main__':
 import json; print(json.dumps(run(),indent=2,sort_keys=True))
