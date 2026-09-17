import unittest
import typed_carrier_graph as tc


class CommonCarrierTests(unittest.TestCase):
    def test_common_words_create_no_edge(self):
        graph = tc.CarrierGraph()
        graph.add_untyped_note('source provenance site origin')
        self.assertFalse(graph.has_certified_path('A', 'B'))

    def test_supplied_embedding_is_not_real_evidence(self):
        graph = tc.synthetic_supplied_embedding_graph()
        result = tc.find_typed_connection(
            graph, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE', real_only=True)
        self.assertFalse(result.real_certified)

    def test_synthetic_common_parent_is_detected(self):
        graph = tc.synthetic_common_parent_graph()
        result = tc.find_typed_connection(
            graph, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE', real_only=False)
        self.assertEqual(result.common_node, 'SYNTHETIC_PARENT')
        self.assertEqual(result.common_node_kind, 'PARENT')

    def test_real_graph_has_exactly_four_candidate_roots(self):
        graph, candidates = tc.build_real_graph()
        self.assertEqual(len(candidates), 4)
        self.assertIn('TORUS_EDGE_REPRESENTATIVE', graph.nodes())

    def test_untyped_relation_classes_never_promote(self):
        for name in ('NO_TYPED_RELATION', 'ARCHIVE_EVIDENCE_ONLY',
                     'CONDITIONAL_ON_SUPPLIED_MAP'):
            self.assertFalse(tc.relation_class_is_certifying(name))


if __name__ == '__main__':
    unittest.main()
