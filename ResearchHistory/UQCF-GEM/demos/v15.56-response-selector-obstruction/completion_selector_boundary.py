"""Bind the new matched-completion holonomy witness to frozen selector no-gos."""
import completion_connection_bridge as cb
from fractions import Fraction as F
CANDIDATES={
 'Genesis_Pin_provenance':False,
 'recoverability_order':False,
 'W1_W2_W3_certificates':False,
 'positivity_support':False,
 'coarse_quotient_naturality':False,
 'later_v14_v15_provenance_source_representation':False,
}
def run():
 p=cb.analyze(cb.state(h=F(1,100)),cb.source()); m=cb.analyze(cb.state(h=F(-1,100)),cb.source())
 return {'schema':'uqcf-completion-selector-boundary-v1','baseline':'d31f3049eba1ee3473b9bb647c25c7052ca15417',
 'matched_visible_initial_data':True,'opposite_hidden_completions_admissible':True,
 'response_ratios':[str(p['scale_free_ratio']),str(m['scale_free_ratio'])],
 'preselection_selector_candidates':CANDIDATES,
 'any_frozen_selector_available':any(CANDIDATES.values()),
 'v13_23_factorization_no_go_applies_in_type':'YES_PRESELECTION_DATA_CANNOT_SELECT_FROM_AN_UNDISTINGUISHED_COMPLETION_FIBER',
 'later_reopening':'NO_V14_V15_STILL_REQUIRE_NEW_REPRESENTATION_LINK_AND_STATE_DEPENDENT_SOURCE_LAWS_ARE_NONUNIQUE',
 'verdict':'HIDDEN_COMPLETION_SELECTION_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY',
 'forbidden_repairs':['choose sign from holonomy response','minimum curvature','maximum/minimum entropy or CMI','GR/ADM success','fine provenance consulted before fine state exists'],
 'next_legal_move':'new independently motivated preselection primitive/representation law, preregistered before downstream response testing',
 'posthoc_fit':False,'claims':{'generated_hidden_state':False,'generated_source_law':False,'gravity_signal':False}}
if __name__=='__main__':
 import json; print(json.dumps(run(),indent=2,sort_keys=True))
