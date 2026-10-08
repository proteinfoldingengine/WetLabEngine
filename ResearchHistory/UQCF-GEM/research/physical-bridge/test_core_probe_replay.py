"""Read-only review tests; no independent-review or full-theorem certification."""
import copy
import unittest
import COUPLED_C3_CORE_PROBE_REPLAY as replay


class CoreProbeReplayTests(unittest.TestCase):
    def test_graph_is_constructed_from_all_hidden_worlds(self):
        report = replay.build_graph(2)
        self.assertEqual(len(report.get('nodes', [])), 8)
        self.assertEqual(len(report.get('edges', [])), 96)

    def test_one_spectator_boundary(self):
        report = replay.build_graph(1)
        self.assertEqual(len(report.get('nodes', [])), 4)
        self.assertEqual(len(report.get('edges', [])), 46)
        self.assertTrue(all(n['D'] <= 1 for n in report['nodes']))

    def test_every_node_compares_exact_labelled_completion_set(self):
        for n in (1, 2):
            for node in replay.build_graph(n)['nodes']:
                expected = sorted(z for z in replay.subsets('uv'[:n]) if len(z) >= node['D'])
                self.assertEqual(node['hidden_subsets'], expected)

    def test_restored_core_can_have_three_different_history_fibers(self):
        nodes = replay.build_graph(2)['nodes']
        restored = [node for node in nodes if node['core4'] == 'de']
        self.assertEqual(sorted(node['D'] for node in restored), [0, 1, 2])
        self.assertEqual(len({tuple(node['hidden_subsets']) for node in restored}), 3)

    def test_empty_projected_root_is_real_and_admissible(self):
        self.assertEqual(replay.full_tau('', 'uv'), 3)
        self.assertTrue(replay.admissible('', 'uv'))
        self.assertFalse(replay.admissible('', 'u'))

    def test_wrong_estimators_are_rejected(self):
        for mutant in ('attempt', 'forget', 'boolean', 'identity'):
            with self.subTest(mutant=mutant):
                with self.assertRaises(replay.ReplayError):
                    replay.build_graph(2, mutant)

    def test_omitted_node_is_rejected_by_fresh_enumeration(self):
        report = replay.build_graph(2)
        broken = copy.deepcopy(report)
        broken['nodes'].pop()
        with self.assertRaises(replay.ReplayError):
            replay.check_graph(broken)

    def test_omitted_outcome_edge_is_rejected_by_fresh_enumeration(self):
        report = replay.build_graph(2)
        broken = copy.deepcopy(report)
        broken['edges'].pop()
        with self.assertRaises(replay.ReplayError):
            replay.check_graph(broken)

    def test_changed_same_cardinality_identity_is_rejected(self):
        report = replay.build_graph(2)
        broken = copy.deepcopy(report)
        for node in broken['nodes']:
            if node['D'] == 1:
                node['hidden_subsets'] = ['u', 'uv', 'w']
                break
        with self.assertRaises(replay.ReplayError):
            replay.check_graph(broken)

    def test_each_command_has_an_unchanged_outcome(self):
        report = replay.build_graph(2)
        edges = {(e['source'], e['command'], e['target']) for e in report['edges']}
        for node in report['nodes']:
            for command in replay.COMMANDS:
                self.assertIn((node['id'], command, node['id']), edges)


if __name__ == '__main__':
    unittest.main(verbosity=2)
