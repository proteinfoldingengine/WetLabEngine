import unittest,copy,producer,independent
class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.actual=producer.build();cls.expected=independent.build()
    def test_complete_independent_identity(self):independent.validate(self.actual,self.expected)
    def test_exact_primary_coverage(self):self.assertEqual(self.actual['counts']['primary_identities'],8*len(self.actual['sources']))
    def test_multi_donor_without_backbone(self):
        r=self.actual['fixtures'][1];self.assertEqual(r['permutations'][0]['release'],[[0,3],[1,4],[0,0],[1,0]])
    def test_arbitrary_reserve_moving_permutations(self):
        for f in self.actual['fixtures']:self.assertEqual(len(f['permutations']),24);self.assertTrue(any(p['permutation'][f['reserve']]!=f['reserve'] for p in f['permutations']))
    def test_upper_cover_control(self):self.assertEqual(self.actual['upper_control']['candidate_tau'],5)
    def test_floor_demand_control(self):self.assertEqual(self.actual['floor_control']['candidate_admitted'],False);self.assertEqual(self.actual['floor_control']['candidate_tau'],3)
    def test_original_domination_control(self):self.assertEqual(self.actual['domination_control']['source_tau'],3);self.assertEqual(self.actual['domination_control']['candidate_tau'],2)
    def test_anchoring_control(self):self.assertEqual(self.actual['anchor_control']['candidate_admitted'],True);self.assertEqual(self.actual['anchor_control']['donor_inclusion'],False);self.assertIsNone(self.actual['anchor_control']['witness'])
    def test_old_obstructions_retained(self):
        for f in self.actual['negative']:self.assertTrue(all(v is None for v in f['witnesses']))
    def bad(self,change):
        d=copy.deepcopy(self.actual);change(d)
        with self.assertRaises(ValueError):independent.validate(d,self.expected)
    def test_missing_primary(self):self.bad(lambda d:d['primary'].pop())
    def test_duplicate_primary(self):self.bad(lambda d:d['primary'].__setitem__(1,d['primary'][0]))
    def test_substituted_source(self):self.bad(lambda d:d['sources'][0].__setitem__(0,0))
    def test_wrong_reserve(self):self.bad(lambda d:d['primary'][0].__setitem__(2,9))
    def test_wrong_witness(self):self.bad(lambda d:d['primary'][0].__setitem__(3,[1,1,1,1]))
    def test_wrong_script(self):self.bad(lambda d:d['fixtures'][0]['permutations'][0]['release'].pop())
    def test_wrong_endpoint(self):self.bad(lambda d:d['fixtures'][1]['permutations'][1]['endpoint'].__setitem__(0,1))
    def test_wrong_hidden_mask(self):self.bad(lambda d:d['fixtures'][0]['protected_masks'].pop())
    def test_false_coverage(self):self.bad(lambda d:d['counts'].__setitem__('primary_identities',0))
    def test_extra_field(self):self.bad(lambda d:d.__setitem__('heuristic',True))
    def test_bool_for_int(self):self.bad(lambda d:d['primary'][0].__setitem__(1,False))
if __name__=='__main__':unittest.main()
