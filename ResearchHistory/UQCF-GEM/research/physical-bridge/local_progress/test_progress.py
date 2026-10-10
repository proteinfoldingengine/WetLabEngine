import copy,unittest
import producer,independent
class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.actual=producer.build();cls.expected=independent.build()
    def test_exact_independent_universe(self):independent.validate(self.actual,self.expected)
    def test_nonisolated_seven_state_component(self):
        for r in self.actual['families']:
            self.assertEqual(len(r['states']),7);self.assertEqual(len(r['edges']),18)
            self.assertNotIn(r['target'],r['states'])
    def test_no_reachable_absent_label(self):
        for r in self.actual['families']:
            for s in r['states']:self.assertEqual(__import__('functools').reduce(int.__or__,s),(1<<(r['n']+5))-1)
    def test_static_reserve_grows(self):
        for r in self.actual['families']:self.assertEqual(len(r['absent_target_labels']),r['n']-2);self.assertEqual(r['capacity'],7)
    def rejected(self,change):
        bad=copy.deepcopy(self.actual);change(bad)
        with self.assertRaises(ValueError):independent.validate(bad,self.expected)
    def test_missing_family(self):self.rejected(lambda d:d['families'].pop())
    def test_duplicate_family(self):self.rejected(lambda d:d['families'].__setitem__(1,copy.deepcopy(d['families'][0])))
    def test_missing_state(self):self.rejected(lambda d:d['families'][0]['states'].pop())
    def test_duplicate_state(self):self.rejected(lambda d:d['families'][0]['states'].__setitem__(1,d['families'][0]['states'][0]))
    def test_missing_edge(self):self.rejected(lambda d:d['families'][0]['edges'].pop())
    def test_substituted_edge(self):self.rejected(lambda d:d['families'][0]['edges'][0].__setitem__(1,0))
    def test_missing_witness(self):self.rejected(lambda d:d['families'][0]['rejecting_toggles'].pop())
    def test_wrong_witness(self):self.rejected(lambda d:d['families'][0]['rejecting_toggles'][0].__setitem__(3,-1))
    def test_wrong_floor(self):self.rejected(lambda d:d['families'][0]['floors'].__setitem__(0,1))
    def test_wrong_target(self):self.rejected(lambda d:d['families'][0]['target'].__setitem__(0,1))
    def test_wrong_capacity(self):self.rejected(lambda d:d['families'][0].__setitem__('capacity',6))
    def test_extra_field(self):self.rejected(lambda d:d.__setitem__('invented',True))
    def test_boolean_integer(self):self.rejected(lambda d:d['families'][0]['floors'].__setitem__(-1,True))
if __name__=='__main__':unittest.main()
