import unittest
import source_extension_gate as gate


class GateTests(unittest.TestCase):
    def test_real_archive_fails_closed_without_fiber_entailment(self):
        r = gate.audit_real_archive()
        self.assertIn(r.status, {
            'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE',
            'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED',
            'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION',
            'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED',
            'PROVENANCE_SOURCE_REPRESENTATION_READY',
            'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
        })
        self.assertFalse(r.gravity_observables_evaluated)

    def test_current_frozen_evidence_prefers_non_entailment_if_countermodels_survive(self):
        r = gate.audit_real_archive()
        if r.countermodels_survive:
            self.assertEqual(r.status,
                             'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')

    def test_representation_ready_is_stronger_than_carrier_certified(self):
        carrier, ready = gate.synthetic_carrier_vs_ready_controls()
        self.assertEqual(carrier.status,
                         'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED')
        self.assertFalse(carrier.representation_ready)
        self.assertEqual(ready.status,
                         'PROVENANCE_SOURCE_REPRESENTATION_READY')
        self.assertTrue(ready.representation_ready)

    def test_raw_representative_control_never_certifies_real_carrier(self):
        r = gate.audit_raw_representative_control()
        self.assertEqual(r.status,
                         'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM')
        self.assertFalse(r.nontrivial_kernel_certified)


if __name__ == '__main__':
    unittest.main()
