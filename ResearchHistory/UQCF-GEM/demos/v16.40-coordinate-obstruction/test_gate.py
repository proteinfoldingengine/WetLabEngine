"""Fast independent mutation controls on a declared two-leaf, two-view fixture."""
import unittest,copy
import producer,verifier
D={'parents':[-1,0,0],'k':2,'q0':[2,0,0]}
W=[[3,5],[3,7],[7,7],[5,7],[5,3]]
class Gate(unittest.TestCase):
    def setUp(self):self.doc=producer.build(D['parents'],D['k'],D['q0'],W)
    def check(self):return verifier.verify(self.doc,D,W)
    def reject(self):
        with self.assertRaises(ValueError):self.check()
    def test_positive_static(self):
        r=self.check();self.assertEqual(r['classifications'],{'static_sufficient':1});self.assertTrue(r['named']['candidate_valid']);self.assertEqual(r['named']['static_success_coordinates'],[0])
    def test_missing_state(self):self.doc['admitted'].pop();self.reject()
    def test_duplicate_state(self):self.doc['admitted'].append(self.doc['admitted'][0]);self.reject()
    def test_substitute_state(self):self.doc['admitted'][0]=self.doc['admitted'][1];self.reject()
    def test_wrong_domain(self):self.doc['domain']['q0']=[1,0,0];self.reject()
    def test_missing_unit(self):self.doc['unit'].pop();self.reject()
    def test_missing_edge(self):self.doc['unit_edges'].pop();self.reject()
    def test_false_edge(self):self.doc['unit_edges'][0]=[0,0];self.reject()
    def test_missing_pair(self):self.doc['pairs'].pop();self.reject()
    def test_duplicate_pair(self):self.doc['pairs']*=2;self.reject()
    def test_substitute_pair(self):self.doc['pairs'][0]['components']=[0,0];self.reject()
    def test_wrong_endpoint(self):self.doc['pairs'][0]['endpoints'].reverse();self.reject()
    def test_wrong_barrier(self):self.doc['pairs'][0]['primary']=[0,1,1];self.reject()
    def test_wrong_lex(self):self.doc['pairs'][0]['LEX']=[1,0,1];self.reject()
    def test_invalid_move(self):self.doc['pairs'][0]['paths']['0']=self.doc['pairs'][0]['endpoints'];self.reject()
    def test_missing_success(self):self.doc['pairs'][0]['paths'].pop('1');self.reject()
    def test_false_static_success(self):self.doc['pairs'][0]['paths']['2']=self.doc['pairs'][0]['paths']['0'];self.reject()
    def test_incomplete_partition(self):self.doc['partitions']['static'][0][0].pop();self.reject()
    def test_false_partition(self):self.doc['partitions']['zero']=[sum(self.doc['partitions']['zero'],[])];self.reject()
    def test_false_cut(self):self.doc['pairs'][0]['cuts']['2']=[0,0];self.reject()
    def test_false_sc(self):self.doc['pairs'][0]['SC']=not self.doc['pairs'][0]['SC'];self.reject()
    def test_false_endpoint_full(self):self.doc['pairs'][0]['endpoint_full']=not self.doc['pairs'][0]['endpoint_full'];self.reject()
    def test_false_classification(self):self.doc['pairs'][0]['classification']='moving_required';self.reject()
    def test_matching_but_illegal_candidate(self):
        bad=W[:2]+W[-1:];self.doc['named_path']=bad
        r=verifier.verify(self.doc,D,bad);self.assertFalse(r['named']['candidate_valid']);self.assertFalse(r['named']['shortest_if_valid'])
    def test_wrong_candidate(self):self.doc['named_path']=W[:2]+W[-1:];self.reject()
if __name__=='__main__':unittest.main()
