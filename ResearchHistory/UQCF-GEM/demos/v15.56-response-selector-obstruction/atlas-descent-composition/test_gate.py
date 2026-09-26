"""Frozen tests: partial trace, complex fidelity, composition, and adjudication."""
import importlib.util
import json
import pathlib
import unittest
import numpy as np


class GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = pathlib.Path(__file__).with_name('gate.py')
        if not path.exists():
            raise AssertionError('v15.70 scientific implementation absent: expected RED')
        spec = importlib.util.spec_from_file_location('atlas_gate', path)
        cls.g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.g)

    def test_partial_trace_preserves_imaginary_entries_and_region_order(self):
        # Catches real-only conversion and reversed (2,0) endpoint ordering.
        a = np.array([[.5, -.5j], [.5j, .5]])
        b = np.diag([1., 0.])
        c = np.diag([0., 1.])
        rho = np.kron(np.kron(a, b), c)
        np.testing.assert_allclose(self.g.restrict(rho, (2, 0)), np.kron(c, a), atol=1e-15)
        bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
        z = np.kron(np.outer(bell, bell), c)
        np.testing.assert_allclose(self.g.restrict(z, (0,)), np.eye(2)/2, atol=1e-15)

    def test_zero_hidden_marginals_and_nonzero_pair_tangent(self):
        # Catches retained projection selecting or averaging the wrong subsystem.
        x = np.array([[0, 1], [1, 0]])
        h = np.kron(np.kron(x, x), x)/np.sqrt(8)
        y = np.kron(np.kron(x, x), np.eye(2))/8
        np.testing.assert_allclose(self.g.restrict(h, (0, 1)), np.zeros((4, 4)), atol=1e-15)
        self.assertAlmostEqual(np.linalg.norm(self.g.restrict(y, (0, 1))), .5)

    def test_finite_source_composition_and_detectable_noncommutation(self):
        # Catches missing source amplitude, wrong order, or a hardcoded zero bracket.
        n = np.array([[0., 1.], [0., 0.]])
        m = n.T
        self.assertAlmostEqual(self.g.commutator_norm(n, m), np.sqrt(2))
        self.assertEqual(self.g.commutator_norm(n, n), 0.)
        rho = np.eye(2)/2
        h = np.array([[0., 1.], [1., 0.]])/np.sqrt(2)
        y = np.diag([1., -1.])/np.sqrt(2)
        sig = rho+.01*h
        out = self.g.source_step(sig, rho, h, y, .1)
        np.testing.assert_allclose(out, sig+.001*y, atol=1e-15)
        out2 = self.g.source_step(out, rho, h, y, -.03)
        np.testing.assert_allclose(out2, sig+.0007*y, atol=1e-15)

    def test_adjudication_preserves_negative_and_invalid_results(self):
        self.assertEqual(self.g.adjudicate(True, [0.]), 'ATLAS_NATURAL_NULL_CONFIRMED')
        self.assertEqual(self.g.adjudicate(True, [.5]), 'ATLAS_NATURAL_NULL_OBSTRUCTED')
        self.assertEqual(self.g.adjudicate(False, [.5]), 'INVALID')
        self.assertEqual(self.g.adjudicate(True, [float('nan')]), 'INVALID')
        self.assertEqual(self.g.adjudicate(True, []), 'INVALID')

    def test_nonfinite_diagnostics_emit_invalid_json_instead_of_crashing(self):
        # Catches nonfinite diagnostics surviving into strict JSON serialization.
        report = {'verdict': 'ATLAS_NATURAL_NULL_OBSTRUCTED', 'all_valid': True,
                  'composition_verdict': 'FIXED_BASE_NULL_COMPOSITION_CONFIRMED',
                  'rows': [{'lift_relative_residual': float('nan')} ]}
        cleaned = self.g.finalize_report(report)
        parsed = json.loads(json.dumps(cleaned, allow_nan=False))
        self.assertEqual(parsed['verdict'], 'INVALID')
        self.assertFalse(parsed['all_valid'])
        self.assertEqual(parsed['composition_verdict'], 'INVALID')
        self.assertIsNone(parsed['rows'][0]['lift_relative_residual'])
        negative = {'verdict': 'ATLAS_NATURAL_NULL_OBSTRUCTED', 'rows': []}
        self.assertEqual(self.g.finalize_report(negative), negative)

    def test_frozen_measurement_schema_controls_and_independent_norm_prediction(self):
        # Catches empty/skipped states, wrong normalization and invalid controls.
        r = self.g.run_measurement()
        self.assertEqual(r['candidate_indices'], [13,16,22,25,27,29,37,39,46,50,66,77])
        self.assertEqual(len(r['rows']), 12)
        self.assertEqual(r['n_descent_witnesses'], 972)
        self.assertTrue(r['all_valid'], r)
        self.assertIn(r['verdict'], ['ATLAS_NATURAL_NULL_CONFIRMED', 'ATLAS_NATURAL_NULL_OBSTRUCTED'])
        for row in r['rows']:
            self.assertEqual(len(row['descent_witnesses']), 81)
            self.assertAlmostEqual(row['Y_norm'], np.sqrt(3/8), places=10)
            for z in row['descent_witnesses']:
                self.assertAlmostEqual(z['derivative_gap'], .5, places=10)
                self.assertAlmostEqual(z['output_gap'], 1e-7, places=12)
            self.assertGreater(row['skew_control'], 1.)
            self.assertGreater(row['commutator_control'], 1.)


if __name__ == '__main__':
    unittest.main()
