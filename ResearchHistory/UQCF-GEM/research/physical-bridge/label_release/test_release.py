import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
def module(name):
    p=HERE/(name+'.py')
    if not p.exists(): raise AssertionError('missing implementation: '+name)
    s=importlib.util.spec_from_file_location('release_'+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=module('producer');cls.v=module('independent');cls.good=cls.p.produce()
    def test_full_independent_reconstruction(self): self.assertTrue(self.v.validate(self.good))
    def test_first_progress_equivalence(self):
        self.assertTrue(all(bool(s['strict_pairs'])==bool(s['safe_first_toggles']) for s in self.good['sources']))
    def test_release_criterion(self):
        self.assertTrue(all(r[2]==(not r[3]) for s in self.good['sources'] for r in s['release']))
    def test_loan_renewal(self):
        for s in self.good['loans']:
            self.assertEqual(s['path'][0],s['path'][-1]);self.assertEqual(len(s['path']),2*s['cost']+1)
            self.assertTrue(all(3<=x<=4 for row in s['taus'] for x in row))
    def test_native_capacity_obstruction(self):
        self.assertTrue(self.good['controls']['nested_safe_first'])
        self.assertEqual(self.good['controls']['nested_absent_states'],[])
    def test_native_upper_control(self): self.assertEqual(self.good['controls']['upper_taus'],[4,5])
    def test_host_only_endpoint_cost(self): self.assertEqual(next(s['cost'] for s in self.good['loans'] if s['mask']==32),8)

def change(n,d):
    if n=='missing_source':d['sources'].pop()
    elif n=='source_core':d['sources'][0]['core'][0]=15
    elif n=='source_tau':d['sources'][0]['tau']=2
    elif n=='missing_mask':d['sources'][0]['source_masks'].pop()
    elif n=='first_toggles':d['sources'][0]['safe_first_toggles']=[[0,0]]
    elif n=='strict_pair':d['sources'][0]['strict_pairs']=[[0,0]]
    elif n=='release_value':d['sources'][0]['release'][0][2]=True
    elif n=='release_witness':d['sources'][0]['release'][0][3]=[]
    elif n=='missing_loan':d['loans'].pop()
    elif n=='loan_mask':d['loans'][0]['mask']=0
    elif n=='loan_cost':d['loans'][0]['cost']-=2
    elif n=='loan_slice':d['loans'][0]['path'].pop(1)
    elif n=='loan_tau':d['loans'][0]['taus'][0][0]=2
    elif n=='bad_mask':d['rejected_masks'].append(32)
    elif n=='capacity':d['controls']['nested_absent_states']=[0]
    elif n=='upper':d['controls']['upper_taus']=[4,4]
    elif n=='provenance':d['schema']='wrong'
    elif n=='type':d['sources'][0]['release'][0][2]=0
    elif n=='extra':d['unreviewed']=True
    return d
for n in ['missing_source','source_core','source_tau','missing_mask','first_toggles','strict_pair','release_value','release_witness','missing_loan','loan_mask','loan_cost','loan_slice','loan_tau','bad_mask','capacity','upper','provenance','type','extra']:
    def test(self,n=n):
        with self.assertRaises(ValueError): self.v.validate(change(n,copy.deepcopy(self.good)))
    setattr(Contracts,'test_reject_'+n,test)
if __name__=='__main__':unittest.main()
