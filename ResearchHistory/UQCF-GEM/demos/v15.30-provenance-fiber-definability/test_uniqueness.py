import unittest
import uniqueness as uq


class UniquenessTests(unittest.TestCase):
    def test_label_renaming_does_not_create_new_relation(self):
        self.assertEqual(uq.canonical_partition_signature(('A', 'A', 'B')),
                         uq.canonical_partition_signature(('X', 'X', 'Y')))

    def test_two_distinct_partitions_prove_nonuniqueness(self):
        result = uq.classify_relation_family((('A', 'A', 'B'), ('A', 'B', 'B')))
        self.assertEqual(result.status, 'MULTIPLE')
        self.assertIsNotNone(result.witness_pair)

    def test_single_survivor_is_unique(self):
        result = uq.classify_relation_family((('A', 'A', 'B'), ('X', 'X', 'Y')))
        self.assertEqual(result.status, 'UNIQUE')
        self.assertEqual(len(result.signatures), 1)

    def test_empty_family_cannot_certify_uniqueness(self):
        result = uq.classify_relation_family(())
        self.assertEqual(result.status, 'NONE')


if __name__ == '__main__':
    unittest.main()
