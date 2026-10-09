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
        self.assertEqual(independent.check(self.data)['records'], 768)

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
        self.data['records'][0]['after'][0] += 1
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_invalid_support(self):
        self.data['records'][0]['id'][0] = 8
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_provenance(self):
        self.data['scope'] = '0'*40
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_native_controls(self):
        self.assertEqual(independent.check(self.data)['native_tau'], [3]*9)
        self.data['native']['a'][0] = 0
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_atomicity_and_scope(self):
        with self.assertRaises(ValueError): producer.decode([1,1,0,0,0,0], 3)
        self.data['claims']['root_address_decoded'] = True
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_coverage(self):
        self.assertEqual(independent.check(self.data)['coverage_final'], [5,3])
        self.data['coverage']['final'] = [3,5]
        with self.assertRaises(ValueError): independent.check(self.data)

if __name__ == '__main__': unittest.main()
