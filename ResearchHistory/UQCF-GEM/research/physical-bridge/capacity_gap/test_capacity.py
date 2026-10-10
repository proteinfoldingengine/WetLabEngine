import copy,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import producer,independent
class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.good=producer.build();cls.expected=independent.build()
    def test_complete(self): independent.validate(self.good,self.expected)
    def test_general_domain(self): self.assertEqual(len(self.good['cores']),2448)
    def test_family_capacity(self): self.assertEqual([r['capacity'] for r in self.good['family']],[5]*4)
    def test_unbounded_pattern(self):
        for r in self.good['family']:
            self.assertEqual(r['absent_labels'],list(range(5,r['n']+3)))
            self.assertTrue(all(x['source_admitted'] and not x['candidate_admitted'] for x in r['first_toggles']))
    def test_upper_native_control(self):
        c=self.good['upper_control'];self.assertEqual(c['taus'],[3,5]);self.assertTrue(c['floors'] and c['domination']);self.assertFalse(c['admitted'])
    def bad(self,fn):
        r=copy.deepcopy(self.good);fn(r)
        with self.assertRaises(ValueError):independent.validate(r,self.expected)
    def test_missing_core(self): self.bad(lambda r:r['cores'].pop())
    def test_duplicate_core(self): self.bad(lambda r:r['cores'].append(r['cores'][0]))
    def test_wrong_capacity(self): self.bad(lambda r:r['cores'][0]['capacity'].__setitem__(0,0))
    def test_missing_maximal(self): self.bad(lambda r:r['cores'][0]['maximal'].pop())
    def test_wrong_source(self): self.bad(lambda r:r['family'][0]['source'].__setitem__(0,0))
    def test_missing_family(self): self.bad(lambda r:r['family'].pop())
    def test_wrong_target(self): self.bad(lambda r:r['family'][0]['target'].__setitem__(0,0))
    def test_hidden_omission(self): self.bad(lambda r:r['family'][0]['protected_masks'].pop())
    def test_missing_toggle(self): self.bad(lambda r:r['family'][0]['first_toggles'].pop())
    def test_fake_witness(self): self.bad(lambda r:r['family'][0]['first_toggles'][0].__setitem__('source_admitted',False))
    def test_fake_absence(self): self.bad(lambda r:r['family'][1]['absent_labels'].append(0))
    def test_upper_forgery(self): self.bad(lambda r:r['upper_control'].__setitem__('admitted',True))
    def test_wrong_counts(self): self.bad(lambda r:r['counts'].__setitem__('core_sources',0))
    def test_extra(self): self.bad(lambda r:r.__setitem__('closed',True))
    def test_type(self): self.bad(lambda r:r['family'][0].__setitem__('capacity',True))
if __name__=='__main__':unittest.main()
