"""Behavioral controls for matched-input source response; all equalities exact."""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
import unittest

available = importlib.util.find_spec('matched_completion_response') is not None
if available:
    import matched_completion_response as m

class Availability(unittest.TestCase):
    def test_checker_exists(self):
        self.assertTrue(available, 'matched_completion_response checker is not implemented')

@unittest.skipUnless(available, 'checker is not implemented')
class MatchedResponseTests(unittest.TestCase):
    def test_faithful_normalized_states(self):
        for sign in (-1, 1):
            state=m.parity_state(3, F(1,5), sign)
            self.assertEqual(sum(state.probabilities), 1)
            self.assertEqual(min(state.probabilities), F(1,10))
            self.assertEqual(max(state.probabilities), F(3,20))

    def test_every_proper_marginal_matches(self):
        plus=m.parity_state(3, F(1,5), 1)
        minus=m.parity_state(3, F(1,5), -1)
        for support in ((0,),(1,),(2,),(0,1),(0,2),(1,2)):
            self.assertEqual(m.marginal(plus,support),m.marginal(minus,support))
            self.assertEqual(m.marginal(plus,support),(F(1,2**len(support)),)*(2**len(support)))

    def test_hidden_parity_is_the_only_changed_Z_moment(self):
        plus=m.parity_state(3, F(1,5), 1)
        minus=m.parity_state(3, F(1,5), -1)
        for support in m.subsets(3):
            delta=m.expectation(plus,m.z_observable(3,support))-m.expectation(minus,m.z_observable(3,support))
            self.assertEqual(delta, F(2,5) if len(support)==3 else 0)

    def test_fixed_source_fixed_observables_response(self):
        for sign in (-1,1):
            state=m.parity_state(3,F(1,5),sign)
            self.assertEqual(m.paired_response(state), (sign*F(1,5),F(1)))

    def test_projective_response_is_not_just_amplitude(self):
        plus=m.paired_response(m.parity_state(3,F(1,5),1))
        minus=m.paired_response(m.parity_state(3,F(1,5),-1))
        self.assertEqual(m.determinant(plus,minus),F(2,5))
        self.assertEqual(plus[0]/plus[1],F(1,5))
        self.assertEqual(minus[0]/minus[1],-F(1,5))

    def test_source_scaling_and_identity_shift(self):
        for sign in (-1,1):
            state=m.parity_state(3,F(1,5),sign)
            base=m.paired_response(state)
            for a in (F(2,7),F(1),F(3)):
                for b in (F(-5,2),F(0),F(11,3)):
                    self.assertEqual(m.paired_response(state,a,b), tuple(a*x for x in base))

    def test_identity_source_null(self):
        for sign in (-1,1):
            self.assertEqual(m.paired_response(m.parity_state(3,F(1,5),sign),0,7),(F(0),F(0)))

    def test_hidden_correlation_ablation(self):
        state=m.parity_state(3,F(0),1)
        self.assertEqual(m.paired_response(state),(F(0),F(1)))

    def test_exact_finite_tilts(self):
        for sign in (-1,1):
            state=m.parity_state(3,F(1,5),sign)
            for odds in (F(1,4),F(1,2),F(1),F(2),F(4)):
                t=m.tilt_odds(state,2,odds)
                response=(m.expectation(t,m.z_observable(3,(0,1))),m.expectation(t,m.z_observable(3,(2,))))
                h=(odds-1)/(odds+1)
                self.assertEqual(response,(sign*F(1,5)*h,h))
                self.assertEqual(sum(t.probabilities),1)

    def test_response_derivative_from_odds_formula(self):
        # d/du (u-1)/(u+1) at u=1 is 1/2; du/ds at 0 is 2.
        for sign in (-1,1):
            state=m.parity_state(3,F(1,5),sign)
            self.assertEqual(m.paired_response(state)[0],sign*F(1,5)*F(1,2)*2)

    def test_site_permutation_covariance(self):
        from itertools import permutations
        original=m.parity_state(3,F(1,5),1)
        for perm in permutations(range(3)):
            new=m.permute_sites(original,perm)
            source_site=perm.index(2)
            support=tuple(perm.index(i) for i in (0,1))
            P=m.z_observable(3,(source_site,))
            O=m.z_observable(3,support)
            self.assertEqual(m.susceptibility(new,O,P),F(1,5))

    def test_hierarchy_levels_and_lower_information(self):
        for k in range(1,7):
            r=m.quantum_case(k)
            self.assertEqual(r['proper_marginal_pairs_checked'],2**(k+1)-2)
            self.assertEqual(r['max_proper_marginal_difference'],'0')
            self.assertEqual(r['response_plus'],['1/5','1'])
            self.assertEqual(r['response_minus'],['-1/5','1'])
            self.assertEqual(r['absolute_determinant'],'2/5')

    def test_lawful_pruning_orders_and_final_operator_agree(self):
        for fine,coarse in m.baseline.CASES:
            r=m.graph_history_case(fine,coarse)
            self.assertTrue(r['orders_distinct'])
            self.assertEqual(r['history_count'],2)
            for key in ('source_composition_residual','restriction_composition_residual',
                        'boundary_response_residual','between_history_response_residual'):
                self.assertEqual(r[key],'0')

    def test_identity_pruning_null(self):
        keys=((),(0,),(1,))
        r=m.graph_history_case(keys,keys)
        self.assertFalse(r['orders_distinct'])
        self.assertEqual(r['boundary_response_residual'],'0')

    def test_singleton_retention_is_supported(self):
        r=m.graph_history_case(((),(0,),(0,0)),((),))
        self.assertEqual(r['boundary_response_residual'],'0')

    def test_invalid_inputs_fail_closed(self):
        for args in ((0,F(1,5),1),(3,F(1),1),(3,F(-1,5),1),(3,F(1,5),0),(3,0.2,1)):
            with self.assertRaises((TypeError,ValueError)): m.parity_state(*args)
        with self.assertRaises(ValueError): m.z_observable(3,(0,0))
        with self.assertRaises(ValueError): m.z_observable(3,(3,))
        state=m.parity_state(3,F(1,5),1)
        with self.assertRaises(ValueError): m.tilt_odds(state,2,0)
        with self.assertRaises(ValueError): m.expectation(state,(F(1),))
        with self.assertRaises(ValueError): m.permute_sites(state,(0,0,2))
        with self.assertRaises(ValueError): m.graph_history_case(((),(0,)),((),(1,)))

    def test_general_covariance_really_subtracts_both_means(self):
        state=m.DiagonalState(2,(F(1,2),F(1,4),F(1,8),F(1,8)))
        O=m.z_observable(2,(0,)); P=m.z_observable(2,(1,))
        self.assertEqual(m.susceptibility(state,O,P),F(1,8))
        self.assertEqual(m.susceptibility(state,O,tuple(x+7 for x in P)),F(1,8))
        self.assertEqual(m.tilt_odds(state,1,F(2)).probabilities,
                         (F(8,13),F(2,13),F(2,13),F(1,13)))

    def test_nonsymmetric_state_permutation_moves_data(self):
        state=m.DiagonalState(2,(F(1,2),F(1,4),F(1,8),F(1,8)))
        self.assertEqual(m.permute_sites(state,(1,0)).probabilities,
                         (F(1,2),F(1,8),F(1,4),F(1,8)))

    def test_epsilon_is_input_not_a_hardcoded_gap(self):
        for eps in (F(1,10),F(1,3),F(4,5)):
            for sign in (-1,1):
                state=m.parity_state(3,eps,sign)
                self.assertEqual(m.paired_response(state),(sign*eps,F(1)))
                self.assertEqual(m.marginal(state,(0,1)),(F(1,4),)*4)

    def test_saved_report_is_recomputed_not_trusted(self):
        path=Path(__file__).with_name('MATCHED_COMPLETION_RESULTS.json')
        self.assertTrue(path.exists(), 'Published exact results must be present')
        self.assertEqual(json.loads(path.read_text()),m.run())

    def test_scope_keeps_unearned_bridge_out(self):
        r=m.run()
        self.assertFalse(r['claims']['new_gravity_signal'])
        self.assertFalse(r['claims']['repair_history_generates_parity_states'])
        self.assertFalse(r['claims']['quantum_response_equals_lineage_curvature'])
        self.assertFalse(r['claims']['quantum_exclusive_or_novel_effect'])
        self.assertEqual(r['parameters_fit'],0)
        self.assertEqual(r['arithmetic'],'EXACT_RATIONAL')

if __name__=='__main__': unittest.main()
