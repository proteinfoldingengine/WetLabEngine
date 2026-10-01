import unittest,copy
from unittest.mock import patch
import producer,verifier
SMALL=((2,2),(3,2),(2,3))
class Gate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.fixture=producer.produce(SMALL)
 def setUp(self):self.doc=copy.deepcopy(self.fixture)
 def check(self):return verifier.verify(self.doc,SMALL)
 def reject(self):
  with self.assertRaises(ValueError):self.check()
 def graph(self):return self.doc['entries'][0]['graph']
 def pairs(self):return self.graph()['profiles'][-1]['pairs']
 def test_positive(self):self.assertEqual(self.check()['outcome'],'STAR_CLASSIFICATION_VALIDATED')
 def test_missing_state(self):self.graph()['states'].pop();self.reject()
 def test_duplicate_state(self):self.graph()['states'].append(self.graph()['states'][0]);self.reject()
 def test_missing_graph(self):self.doc['entries'].pop();self.reject()
 def test_duplicate_graph(self):self.doc['entries'].append(self.doc['entries'][0]);self.reject()
 def test_wrong_domain(self):self.doc['domain'][0][1]=4;self.reject()
 def test_wrong_tree(self):self.graph()['parents'][1]=1;self.reject()
 def test_wrong_edge(self):self.graph()['forward_moves'][0]^=1;self.reject()
 def test_wrong_profile(self):self.graph()['profile_ids'][0]=-1;self.reject()
 def test_missing_profile(self):self.graph()['attained_profiles'].pop();self.reject()
 def test_missing_component(self):self.graph()['profiles'][0]['zero_components'].pop();self.reject()
 def test_wrong_component(self):self.graph()['profiles'][0]['zero_components'][0].pop();self.reject()
 def test_wrong_unit_partition(self):self.graph()['profiles'][0]['unit_components'][0].pop();self.reject()
 def test_missing_pair(self):self.pairs().pop();self.reject()
 def test_duplicate_pair(self):self.pairs().append(self.pairs()[0]);self.reject()
 def test_wrong_pair_path(self):self.pairs()[0]['unit_path']=[];self.reject()
 def test_wrong_objective(self):self.pairs()[0]['primary_bounds']['Bs']=[0,1];self.reject()
 def test_missing_normalization(self):self.doc['entries'][0]['normalizations'].pop();self.reject()
 def test_duplicate_normalization(self):r=self.doc['entries'][0]['normalizations'];r.append(r[0]);self.reject()
 def test_wrong_normalization_identity(self):self.doc['entries'][0]['normalizations'][0]['state']=-1;self.reject()
 def test_normalization_refuted(self):self.doc['entries'][0]['normalizations'][0]['path']=[];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_wrong_normalization_q(self):self.doc['entries'][0]['normalizations'][0]['q']=-1;self.reject()
 def test_illegal_path_index(self):self.doc['entries'][0]['normalizations'][0]['path']=[-1];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_spare_leaf(self):self.assertEqual(self.check()['per_graph'][1]['components'],2)
 def test_spare_label(self):self.assertEqual(self.check()['per_graph'][2]['components'],2)
 def test_packed_boundary(self):self.assertEqual(self.check()['per_graph'][0]['components'],3)
 def test_nonunit_priority(self):self.assertEqual(verifier.outcome(1,[{}],[{}]),'NONUNIT_WITNESS')
 def test_classification_refuted(self):
  with patch.object(verifier,'factorial',return_value=999):self.assertEqual(self.check()['outcome'],'CLASSIFICATION_REFUTED')
 def test_unknown_document_field(self):self.doc['extra']=True;self.reject()
 def test_unknown_entry_field(self):self.doc['entries'][0]['extra']=True;self.reject()
if __name__=='__main__':unittest.main()
