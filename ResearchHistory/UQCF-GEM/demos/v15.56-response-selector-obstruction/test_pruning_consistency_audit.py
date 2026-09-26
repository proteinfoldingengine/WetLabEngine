"""Behavioural tests for the exact corrective pruning audit."""
import importlib.util
import unittest
from fractions import Fraction as F

SPEC = importlib.util.find_spec('pruning_consistency_audit')
if SPEC is not None:
    import pruning_consistency_audit as a

class Availability(unittest.TestCase):
    def test_checker_exists(self):
        self.assertIsNotNone(SPEC, 'Exact pruning consistency checker is not implemented')

@unittest.skipIf(SPEC is None, 'Waiting for the implementation after RED')
class ExactPruningTests(unittest.TestCase):
    def test_known_chain_laplacian_and_green(self):
        L = a.laplacian(((), (0,), (0, 0)))
        self.assertEqual(L, [[1,-1,0],[-1,2,-1],[0,-1,1]])
        self.assertEqual(a.green(L), [[F(5,9),F(-1,9),F(-4,9)],
                                    [F(-1,9),F(2,9),F(-1,9)],
                                    [F(-4,9),F(-1,9),F(5,9)]])

    def test_frozen_fiber_sizes_and_constant_source_witnesses(self):
        sizes = ([1,3,3], [1,2,3], [1,1,3,2], [1,1,1,2,2])
        witnesses = (['-4/9','2/9','2/9'], ['-1','0','1'],
                     ['-3/16','-15/16','17/16','1/16'],
                     ['-2/5','-1/5','-1/5','2/5','2/5'])
        r = a.run()
        for row, n, z in zip(r['cases'], sizes, witnesses):
            self.assertEqual(row['fiber_sizes'], n)
            self.assertEqual(row['raw_constant_source_coarse_response'], z)
            self.assertEqual(row['raw_operator_nullity'], 0)

    def test_exact_balanced_operator_identity_for_all_sources(self):
        for fine, coarse in a.CASES:
            d = a.operators(fine, coarse)
            self.assertEqual(a.mul(d['P'],d['Lf']), a.mul(d['Lc'],d['S']))
            self.assertEqual(a.mul(a.mul(d['Cc'],d['S']),d['Gf']),
                             a.mul(a.mul(d['Gc'],d['P']),d['Cf']))

    def test_centering_discrepancy_is_rank_one(self):
        for row in a.run()['cases']:
            self.assertEqual(row['centering_discrepancy_rank'], 1)
            self.assertEqual(row['centering_residual'], '0')
            self.assertEqual(row['balanced_naturality_residual'], '0')

    def test_only_normalized_fiber_local_solution_is_restriction(self):
        for row in a.run()['cases']:
            self.assertTrue(row['normalized_solution_unique'])
            self.assertEqual(row['projective_scale'], '1')
            self.assertEqual(row['solved_weights'], row['restriction_weights'])
            self.assertFalse(row['strictly_positive_solution'])
            self.assertTrue(row['nonnegative_solution'])

    def test_forgotten_contrast_invisible_only_after_correct_response_map(self):
        for row in a.run()['cases']:
            self.assertEqual(row['forgotten_source_pushforward'], '0')
            self.assertNotEqual(row['forgotten_fine_response'], '0')
            self.assertEqual(row['forgotten_restricted_response'], '0')

    def test_depth_measures_are_identical_not_independent_controls(self):
        for fine, coarse in a.CASES:
            d = a.operators(fine, coarse)
            self.assertEqual(a.aggregation(fine, coarse, 'ABS_DEPTH'),
                             a.aggregation(fine, coarse, 'FIBER_DEPTH'))
        self.assertEqual(a.run()['distinct_task31_aggregation_operators'], 2)

    def test_identity_pruning_has_no_constant_obstruction(self):
        keys = ((), (0,), (1,))
        d = a.operators(keys, keys)
        self.assertEqual(d['P'], a.eye(3))
        self.assertEqual(d['S'], a.eye(3))
        self.assertEqual(a.mul(d['Gc'], a.mul(d['P'], a.ones(3,1))), a.zeros(3,1))

    def test_equal_size_fibers_allow_original_full_source_equation(self):
        fine = ((),(0,),(1,),(0,0)); coarse = ((),(0,))
        d = a.operators(fine,coarse)
        self.assertEqual(a.mul(a.mul(d['Cc'],d['S']),d['Gf']), a.mul(d['Gc'],d['P']))

    def test_invalid_lineage_is_rejected(self):
        bad = (((),(0,0)), ((),()), ((0,),), ((),(-1,)))
        for keys in bad:
            with self.assertRaises(ValueError):
                a.laplacian(keys)
        with self.assertRaises(ValueError):
            a.operators(((),(0,)), ((),(1,)))

    def test_singleton_coarse_is_degenerate_not_strict_positive_nogo(self):
        d = a.operators(((),(0,),(0,0)), ((),))
        self.assertEqual(d['Gc'], [[0]])
        self.assertEqual(a.mul(d['Lc'],d['S']), a.zeros(1,3))
        with self.assertRaises(ValueError):
            a.analyze(((),(0,)), ((),))

    def test_exact_solver_rejects_inconsistent_system(self):
        rank, solution = a.unique_solution([[1],[1]], [1,2])
        self.assertEqual(rank, 1)
        self.assertIsNone(solution)

    def test_frozen_old_counting_defects_reproduce(self):
        expected = (0.0670206184335463,0.2478566204590682,
                    0.21951049458484495,0.08380894550612014)
        for row, x in zip(a.run()['cases'], expected):
            self.assertAlmostEqual(row['old_counting_ray_mismatch'], x, places=12)

    def test_serialized_result_is_deterministic(self):
        self.assertEqual(a.run(), a.run())

if __name__ == '__main__':
    unittest.main()
