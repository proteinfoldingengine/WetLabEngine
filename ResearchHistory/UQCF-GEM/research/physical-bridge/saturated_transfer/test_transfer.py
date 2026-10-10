import copy
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import producer
import independent

class TransferContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = producer.build()
        cls.expected = independent.build()

    def test_entire_typed_domain(self):
        independent.validate(self.record, self.expected)

    def test_every_forward_reverse_exact(self):
        for row in self.record['cases']:
            p=row['partition']; m=len(p); r=row['reserve']
            self.assertEqual(len(row['forward'])-1, 2*m+4+4*p.count(r))
            self.assertEqual(row['reverse'][-1], row['forward'][0])
            self.assertEqual(len(set(map(tuple,row['forward']))),len(row['forward']))

    def test_empty_hidden_protected(self):
        for row in self.record['cases']:
            self.assertEqual(row['completions'][0]['q'],0)
            self.assertTrue(all(t==4 for t in row['completions'][0]['forward_tau']))

    def test_native_rejecting_controls(self):
        self.assertEqual(set(self.record['controls']),{'floor_release','mixed_reserve','split_apex','floor_cleanup'})
        for c in self.record['controls'].values():
            self.assertTrue(c['source_admitted'])
            self.assertFalse(c['candidate_admitted'])

    def test_one_block_isolation(self):
        self.assertEqual([r['m'] for r in self.record['isolated']], [2,3,4])
        for row in self.record['isolated']:
            self.assertEqual(len(row['rejecting_toggles']), (row['m']+3)*6)

    def bad(self, mutate):
        value=copy.deepcopy(self.record); mutate(value)
        with self.assertRaises(ValueError): independent.validate(value,self.expected)

    def test_missing_case(self): self.bad(lambda v:v['cases'].pop())
    def test_duplicate_case(self): self.bad(lambda v:v['cases'].append(v['cases'][0]))
    def test_missing_partition(self): self.bad(lambda v:v['cases'].__setitem__(0,v['cases'][1]))
    def test_wrong_donor(self): self.bad(lambda v:v['cases'][0].__setitem__('donor',v['cases'][0]['reserve']))
    def test_wrong_reserve(self): self.bad(lambda v:v['cases'][0].__setitem__('reserve',99))
    def test_missing_hidden(self): self.bad(lambda v:v['cases'][0]['completions'].pop())
    def test_hidden_change(self): self.bad(lambda v:v['cases'][0]['completions'][0].__setitem__('q',1))
    def test_wrong_hitting(self): self.bad(lambda v:v['cases'][0]['completions'][0]['forward_tau'].__setitem__(0,2))
    def test_wrong_reverse(self): self.bad(lambda v:v['cases'][0]['reverse'][-1].__setitem__(0,0))
    def test_private_cleanup_omitted(self): self.bad(lambda v:v['cases'][0]['forward'].pop())
    def test_floor_forged(self): self.bad(lambda v:v['cases'][0]['floors'].__setitem__(0,1))
    def test_missing_isolation(self): self.bad(lambda v:v['isolated'].pop())
    def test_missing_toggle(self): self.bad(lambda v:v['isolated'][0]['rejecting_toggles'].pop())
    def test_forged_control(self): self.bad(lambda v:v['controls']['mixed_reserve'].__setitem__('candidate_admitted',True))
    def test_forged_counts(self): self.bad(lambda v:v['counts'].__setitem__('cases',0))
    def test_extra_field(self): self.bad(lambda v:v.__setitem__('automatic_closeout',True))
    def test_bool_for_int(self): self.bad(lambda v:v['cases'][0].__setitem__('donor',False))

if __name__ == '__main__': unittest.main()
