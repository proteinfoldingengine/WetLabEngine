import copy
import unittest
try:
    import producer
    import independent
except ModuleNotFoundError:
    producer = independent = None

class Contracts(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(producer, 'implementation absent: intended local RED')
        self.data = producer.produce()

    def test_full_universe(self):
        result = independent.check(self.data)
        self.assertEqual(result['records'], 1980)
        self.assertEqual(result['families'], 495)
        self.assertEqual(result['minimum_collision_size'], {'0': 1, '1': 2, '2': 4, '3': None})

    def test_missing(self):
        self.data['records'].pop()
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_duplicate(self):
        self.data['records'].append(copy.deepcopy(self.data['records'][0]))
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_substitution(self):
        self.data['records'][0] = copy.deepcopy(self.data['records'][1])
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_wrong_value(self):
        self.data['records'][0]['moments'][0] += 1
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_invalid_support(self):
        self.data['records'][1]['supports'] = [8]
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_false_provenance(self):
        self.data['scope'] = '0'*40
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_native_fixture(self):
        r = independent.check(self.data)['native']
        self.assertEqual(r['tau'], [3, 3])
        self.assertEqual(r['residuals_per_world'], 16)
        self.data['parity']['even'][0] = 32
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_scope_controls(self):
        self.assertFalse(self.data['claims']['labelled_assignment_recovered'])
        self.assertFalse(self.data['claims']['initialization_derived'])
        self.data['claims']['labelled_assignment_recovered'] = True
        with self.assertRaises(ValueError): independent.check(self.data)

if __name__ == '__main__': unittest.main()
