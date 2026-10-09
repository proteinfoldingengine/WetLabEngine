import copy
import importlib.util
import pathlib
import unittest

HERE=pathlib.Path(__file__).parent

def module(name):
    p=HERE/(name+'.py')
    if not p.exists():
        raise AssertionError('missing implementation: '+name)
    spec=importlib.util.spec_from_file_location('footprint_'+name,p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=module('producer'); cls.v=module('independent'); cls.good=cls.p.produce()

    def test_complete_independent_reconstruction(self):
        self.assertTrue(self.v.validate(self.good))

    def test_declared_universe(self):
        self.assertEqual([len(f['rows']) for f in self.good['fixtures']],[4096,4096,4096,625])

    def test_sharp_exchange(self):
        a=self.good['application']
        self.assertEqual(len(a['path']),11)
        self.assertEqual(a['no_spare_safe_neighbors'],[])
        self.assertEqual(a['spare_safe_neighbors'],[[0,5],[1,5],[2,5],[3,5],[4,5],[5,5]])
        self.assertTrue(all(3<=v<=4 for row in a['path_taus'] for v in row))

    def test_upper_control(self):
        self.assertEqual(self.good['upper_control']['candidate_tau'],5)
        self.assertEqual(self.good['upper_control']['conditions'],[True,False,True])

def corrupt(which,d):
    if which=='missing_fixture': d['fixtures'].pop()
    elif which=='missing_row': d['fixtures'][0]['rows'].pop()
    elif which=='duplicate_row': d['fixtures'][0]['rows'].append(d['fixtures'][0]['rows'][0])
    elif which=='protected_mask': d['fixtures'][0]['source_masks'].append(7)
    elif which=='source_core': d['fixtures'][0]['core'][0]=3
    elif which=='floor': d['fixtures'][0]['floors'][0]=0
    elif which=='classification': d['fixtures'][0]['rows'][0][2]=True
    elif which=='conditions': d['fixtures'][0]['rows'][0][1]=[True,True,True]
    elif which=='violations': d['fixtures'][0]['rows'][0][3]=[]
    elif which=='path': d['application']['path'].pop(2)
    elif which=='deadlock': d['application']['no_spare_safe_neighbors']=[[0,3]]
    elif which=='tau': d['application']['path_taus'][0][0]=2
    elif which=='upper': d['upper_control']['candidate_tau']=4
    elif which=='provenance': d['schema']='other'
    elif which=='boolean_type': d['fixtures'][0]['rows'][0][2]=0
    elif which=='unknown_field': d['unreviewed']=True
    return d

for name in ['missing_fixture','missing_row','duplicate_row','protected_mask','source_core','floor','classification','conditions','violations','path','deadlock','tau','upper','provenance','boolean_type','unknown_field']:
    def test(self,n=name):
        with self.assertRaises(ValueError): self.v.validate(corrupt(n,copy.deepcopy(self.good)))
    setattr(Contracts,'test_reject_'+name,test)

if __name__=='__main__': unittest.main()
