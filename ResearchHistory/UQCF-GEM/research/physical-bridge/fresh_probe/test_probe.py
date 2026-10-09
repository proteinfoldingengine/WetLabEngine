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
        self.data=producer.produce()

    def test_complete_domain(self):
        result=independent.check(self.data)
        self.assertEqual(result['records'],4536)
        self.assertEqual(result['probe_contexts'],1134)

    def test_missing(self):
        self.data['records'].pop()
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_duplicate(self):
        self.data['records'].append(copy.deepcopy(self.data['records'][0]))
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_substitution(self):
        self.data['records'][0]=copy.deepcopy(self.data['records'][1])
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_wrong_tau(self):
        self.data['records'][0]['tau'][0]+=1
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_wrong_count_or_floor(self):
        self.data['records'][0]['star_after'][0]+=1
        with self.assertRaises(ValueError): independent.check(self.data)
        self.data=producer.produce();self.data['records'][0]['floors'][0]+=1
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_invalid_support(self):
        self.data['records'][0]['family'][0]=0
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_provenance(self):
        self.data['scope']='0'*40
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_native_and_scan(self):
        result=independent.check(self.data)
        self.assertEqual(result['scan_commits'],8)
        self.assertEqual(result['native_tau'],[3,2,3,2,3,3,3,3])
        self.data['scan']['final'][0]+=1
        with self.assertRaises(ValueError): independent.check(self.data)

    def test_decoder(self):
        with self.assertRaises(ValueError): producer.decode([0,1,0,0])
        with self.assertRaises(ValueError): producer.decode([-1,1,0,0])

    def test_scope(self):
        self.data['claims']['guaranteed_completion']=True
        with self.assertRaises(ValueError): independent.check(self.data)

if __name__=='__main__': unittest.main()
