import json
from pathlib import Path
import unittest

from sector_weight_constraint_gate import audit, canonical_json


class SectorWeightConstraintGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit()

    def test_inherited_weight_space(self):
        self.assertEqual(self.r['sector_count'], 10)
        self.assertEqual(self.r['affine_weight_dimension'], 10)
        self.assertEqual(self.r['inherited_projective_relative_weight_dimension'], 9)

    def test_frozen_constraint_ledger(self):
        self.assertEqual(self.r['automatic_constraint_count'], 5)
        self.assertEqual(self.r['type_blocked_constraint_count'], 5)
        self.assertEqual(self.r['projective_gauge_count'], 1)
        self.assertEqual(self.r['unresolved_constraint_count'], 0)
        self.assertEqual(self.r['frozen_actual_weight_equation_count'], 0)
        self.assertEqual(self.r['frozen_constraint_rank'], 0)

    def test_distinct_witnesses_survive(self):
        self.assertEqual(self.r['projectively_distinct_witness_count'], 5)
        self.assertTrue(self.r['all_witnesses_pass_automatic_constraints'])
        self.assertEqual(self.r['surviving_projective_weight_dimension'], 9)

    def test_stronger_controls_do_not_get_promoted(self):
        self.assertEqual(self.r['idempotent_total_choice_count'], 1024)
        self.assertEqual(self.r['idempotent_nonzero_choice_count'], 1023)
        self.assertFalse(self.r['idempotence_is_frozen_source_law'])
        self.assertEqual(self.r['equal_weight_control_projective_dimension'], 0)
        self.assertFalse(self.r['equal_weight_control_is_frozen'])
        self.assertEqual(self.r['positive_cone_projective_dimension'], 9)

    def test_adjudication(self):
        self.assertEqual(
            self.r['status'],
            'FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE',
        )
        self.assertEqual(
            self.r['next_required_object'],
            'NEW_TYPED_PRETIME_INVARIANT_OR_EXPLICIT_SECTOR_WEIGHT_AXIOM',
        )

    def test_committed_ledger_is_exact(self):
        committed = Path('docs/RESULTS.json').read_text()
        self.assertEqual(committed, canonical_json(self.r))
        self.assertEqual(json.loads(committed), self.r)

    def test_firewall(self):
        for key in (
            'new_source_semantics_axiom_added',
            'new_sector_weight_selector_added',
            'coupling_solver_reopened',
            'gravity_observables_evaluated',
            'uses_holonomy_selector',
            'uses_newton_or_gr',
            'uses_metric_selector',
            'uses_pruning_as_selector',
            'uses_entropy_as_selector',
            'uses_physical_time',
            'physical_gravity_derived',
            'scientific_breakthrough',
            'signal_of_life',
        ):
            self.assertFalse(self.r[key], key)
        self.assertEqual(self.r['Pillar_3'], 'OPEN')


if __name__ == '__main__':
    unittest.main()
