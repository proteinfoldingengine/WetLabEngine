"""Small declared two-leaf/two-label positive and rejecting controls."""
import unittest
from integrity import validate_summary
import producer,verifier
class Gate(unittest.TestCase):
    def setUp(self):
        self.doc=producer.produce(2,2);self.g=self.doc['graphs'][0];self.r=next(r for r in self.g['profiles'] if r['partition_profile']);self.pair=self.r['pairs'][0]
    def check(self):return verifier.verify(self.doc,2,2)
    def reject(self):
        with self.assertRaises(ValueError):self.check()
    def test_positive(self):self.assertEqual(self.check()['totals']['partition_pairs'],1)
    def test_missing_tree(self):self.doc['graphs'].pop();self.reject()
    def test_duplicate_tree(self):self.doc['graphs']*=2;self.reject()
    def test_substitute_tree(self):self.g['code']='()';self.reject()
    def test_wrong_domain(self):self.doc['domain']['labels']=3;self.reject()
    def test_wrong_parent(self):self.g['parents'][-1]=1;self.reject()
    def test_missing_state(self):self.g['states'].pop();self.reject()
    def test_duplicate_state(self):self.g['states'].append(self.g['states'][0]);self.reject()
    def test_substitute_state(self):self.g['states'][0]=self.g['states'][1];self.reject()
    def test_wrong_moves(self):self.g['forward_moves'][0]^=1;self.reject()
    def test_wrong_profile(self):self.g['profile_ids'][0]=99;self.reject()
    def test_missing_profile(self):self.g['profiles'].pop();self.reject()
    def test_wrong_classification(self):self.r['partition_profile']=False;self.reject()
    def test_wrong_active_class(self):self.r['adjacent_active']=not self.r['adjacent_active'];self.reject()
    def test_wrong_zero(self):self.r['zero_components']=[sum(self.r['zero_components'],[])];self.reject()
    def test_incomplete_unit(self):self.r['unit_components'][0].pop();self.reject()
    def test_false_unit_partition(self):self.r['unit_components']=[[i] for row in self.r['unit_components'] for i in row];self.reject()
    def test_missing_pair(self):self.r['pairs'].pop();self.reject()
    def test_duplicate_pair(self):self.r['pairs']*=2;self.reject()
    def test_substitute_pair(self):self.pair['components']=[0,0];self.reject()
    def test_wrong_endpoint(self):self.pair['endpoints'].reverse();self.reject()
    def test_invalid_unit_path(self):self.pair['unit_path']=self.pair['endpoints'];self.reject()
    def test_false_cut(self):self.pair['unit_cut']=[0,1];self.reject()
    def test_unsupported_unrestricted(self):self.pair['unrestricted_path']=self.pair['unit_path'];self.reject()
    def test_wrong_bounds(self):self.pair['primary_bounds']['B1']=[0,0];self.reject()
    def test_wrong_lex(self):self.pair['LEX']=[0,0,0];self.reject()
    def test_invalid_construction(self):self.pair['construction']=self.pair['endpoints'];self.reject()
    def abstract(self):
        # Cost-labelled graph only, NEVER an admitted retained counterexample.
        self.abstract_adj=[[1],[0,2],[1]];self.abstract_profiles=[(0,),(2,),(0,)]
        self.abstract_pair={'unit_path':None,'unit_cut':[0,1],'unrestricted_path':[0,1,2],'primary_bounds':{'B1':[2,2],'Binf':[1,2],'Bs':[1,1]},'LEX':None}
    def abstract_check(self):return verifier.check_connection(self.abstract_pair,0,2,(0,),self.abstract_profiles,self.abstract_adj,{0:0,2:1},{0,2})
    def test_abstract_finite_nonunit_cut(self):
        self.abstract();self.assertEqual(verifier.partition([0,2],self.abstract_adj),[[0],[2]]);self.assertEqual(verifier.partition(range(3),self.abstract_adj),[[0,1,2]]);self.assertTrue(self.abstract_check())
    def test_abstract_invalid_unrestricted(self):
        self.abstract();self.abstract_pair['unrestricted_path']=[0,2]
        with self.assertRaises(ValueError):self.abstract_check()
    def test_abstract_false_cut(self):
        self.abstract();self.abstract_pair['unit_cut']=[0,0]
        with self.assertRaises(ValueError):self.abstract_check()
    def test_abstract_false_support_bound(self):
        self.abstract();self.abstract_pair['primary_bounds']['Bs']=[1,2]
        with self.assertRaises(ValueError):self.abstract_check()
    def test_abstract_false_infinity_bound(self):
        self.abstract();self.abstract_pair['primary_bounds']['Binf']=[2,2]
        with self.assertRaises(ValueError):self.abstract_check()
    def test_outcome_binding(self):
        result=self.check()
        with self.assertRaises(ValueError):validate_summary({'finite_result':result,'preregistered_outcome':'NONUNIT_WITNESS'},result)
if __name__=='__main__':unittest.main()
