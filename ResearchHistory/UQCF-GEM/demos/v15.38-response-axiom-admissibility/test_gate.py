import json
from pathlib import Path
import unittest

from response_axiom_admissibility_gate import audit, canonical_json

class ResponseAxiomAdmissibilityGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_contract_structure(self):
        self.assertEqual(self.r['admissibility_requirement_count'],10)
        self.assertEqual(self.r['finite_size_controls'],[5,7,9])
        self.assertEqual(self.r['cycle_dimensions'],{'5':26,'7':50,'9':82})
        self.assertTrue(self.r['exact_multisize_structural_checks_pass'])

    def test_clean_candidates_survive(self):
        self.assertEqual(self.r['admissible_target_blind_control_count'],3)
        self.assertEqual(self.r['projectively_distinct_admissible_control_count'],3)
        self.assertEqual(self.r['accepted_candidate_spectrum_queries'],0)
        self.assertEqual(self.r['accepted_candidate_spectral_edge_parameters'],0)
        self.assertTrue(self.r['admissibility_contract_is_nonselective'])

    def test_bad_controls_rejected(self):
        self.assertEqual(self.r['rejected_control_count'],5)
        self.assertEqual(self.r['unresolved_check_count'],0)
        self.assertEqual(self.r['bad_control_primary_reasons'],{
            'L7_SECTOR_LOOKUP':'FINITE_SIZE_FAMILY_NATURALITY_FAILURE',
            'SPECTRAL_EDGE_TUNED':'SPECTRAL_EDGE_TUNING',
            'GR_FITTED_POLYNOMIAL':'DOWNSTREAM_TARGET_CIRCULARITY',
            'MINIMUM_NORM_HODGE_RESPONSE':'HIDDEN_METRIC_OR_MINIMUM_NORM_SELECTOR',
            'PRUNING_OR_TIME_RATE_RESPONSE':'PRETIME_ONTOLOGY_VIOLATION',
        })

    def test_falsifiability_and_scale(self):
        self.assertTrue(self.r['all_accepted_candidates_have_structural_falsifier'])
        self.assertTrue(self.r['all_accepted_candidates_have_locked_future_test'])
        self.assertTrue(self.r['projective_scale_discipline_enforced'])
        self.assertFalse(self.r['absolute_response_scale_derived'])

    def test_adjudication(self):
        self.assertEqual(self.r['status'],'PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE')
        self.assertFalse(self.r['response_function_selected'])
        self.assertEqual(self.r['next_required_object'],'PREREGISTERED_SMALL_SET_OF_NEW_PRETIME_RESPONSE_AXIOM_CANDIDATES_FOR_COMMON_ADVERSARIAL_CANARY')

    def test_committed_ledger_is_exact(self):
        committed=Path('docs/RESULTS.json').read_text()
        self.assertEqual(committed,canonical_json(self.r))
        self.assertEqual(json.loads(committed),self.r)

    def test_firewall(self):
        for key in ('new_response_function_axiom_adopted','response_function_selected','candidate_tested_against_gravity','gravity_observables_evaluated','new_metric_axiom_added','new_time_axiom_added','uses_holonomy_selector','uses_newton_or_gr_selector','uses_pruning_as_selector','uses_entropy_as_selector','uses_physical_time','physical_gravity_derived','scientific_breakthrough','signal_of_life'):
            self.assertFalse(self.r[key],key)
        self.assertEqual(self.r['Pillar_3'],'OPEN')

if __name__ == '__main__':
    unittest.main()
