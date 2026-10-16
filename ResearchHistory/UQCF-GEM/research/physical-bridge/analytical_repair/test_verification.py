"""Frozen exact examples and substantive certificate rejection controls."""
import copy
import importlib
import unittest

class VerificationTests(unittest.TestCase):
    def setUp(self):
        try:
            self.producer = importlib.import_module('producer')
            self.checker = importlib.import_module('independent')
        except ModuleNotFoundError as exc:
            self.fail('Required independently implemented component absent: ' + exc.name)

    def test_full_reconstruction(self):
        actual = self.producer.produce()
        self.assertEqual(actual, self.checker.reconstruct())
        self.assertTrue(self.checker.verify(actual))
        self.assertEqual(len(actual['records']), 26)

    def rejected(self, change):
        obj = copy.deepcopy(self.producer.produce())
        change(obj)
        with self.assertRaises(ValueError):
            self.checker.verify(obj)

    def test_missing(self):
        self.rejected(lambda o: o['records'].pop())

    def test_duplicate(self):
        self.rejected(lambda o: o['records'].append(o['records'][0]))

    def test_substitution(self):
        self.rejected(lambda o: o['records'][0].update(id='substituted'))

    def test_wrong_value(self):
        self.rejected(lambda o: o['records'][0].update(value='7/1'))

    def test_false_provenance(self):
        self.rejected(lambda o: o.update(source_parent='0'*40))

    def test_false_coverage(self):
        self.rejected(lambda o: o['domain'].update(n=[2,3]))

    def test_invalid_domain(self):
        self.rejected(lambda o: o['domain']['n'].append(1))

    def test_identical_state_false_contrast(self):
        def mutate(o):
            next(x for x in o['records'] if x['id']=='identical_centralizer')['value']['false_contrast']='1/2'
        self.rejected(mutate)

    def test_false_product_seed_attainment(self):
        def mutate(o):
            next(x for x in o['records'] if x['id']=='block_product')['value']='1/2'
        self.rejected(mutate)

if __name__ == '__main__':
    unittest.main()
