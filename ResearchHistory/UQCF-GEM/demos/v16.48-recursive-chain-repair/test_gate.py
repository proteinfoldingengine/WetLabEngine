import unittest,copy
import producer,verifier
SMALL=(((2,2,2,2),2),)
CASES=verifier.corpus_specs()[:6]
class Gate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.fixture=producer.produce(SMALL,CASES)
 def setUp(self):self.doc=copy.deepcopy(self.fixture)
 def check(self):return verifier.verify(self.doc,SMALL,CASES)
 def reject(self):
  with self.assertRaises(ValueError):self.check()
 def graph(self):return self.doc['entries'][0]['graph']
 def pairs(self):return next(r['pairs'] for r in self.graph()['profiles'] if r['pairs'])
 def test_positive(self):self.assertEqual(self.check()['outcome'],'CHAIN_INDUCTION_VALIDATED')
 def test_missing_graph(self):self.doc['entries'].pop();self.reject()
 def test_duplicate_graph(self):self.doc['entries'].append(self.doc['entries'][0]);self.reject()
 def test_substitute_graph(self):self.doc['entries'][0]['degrees']=[3]*4;self.reject()
 def test_missing_state(self):self.graph()['states'].pop();self.reject()
 def test_duplicate_state(self):self.graph()['states'].append(self.graph()['states'][0]);self.reject()
 def test_substitute_state(self):self.graph()['states'][0]=[0,0];self.reject()
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
 def test_substitute_normalization(self):self.doc['entries'][0]['normalizations'][0]['state']=-1;self.reject()
 def test_wrong_normalization_q(self):self.doc['entries'][0]['normalizations'][0]['q']=[-1];self.reject()
 def test_empty_normalization(self):self.doc['entries'][0]['normalizations'][0]['path']=[];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_missing_corpus(self):self.doc['corpus'].pop();self.reject()
 def test_duplicate_corpus(self):self.doc['corpus'].append(self.doc['corpus'][0]);self.reject()
 def test_substitute_corpus(self):self.doc['corpus'][0]['spec']['permutation']='wrong';self.reject()
 def test_wrong_palette_bound(self):self.doc['corpus'][0]['palette_requirement']+=1;self.reject()
 def test_wrong_corpus_start(self):self.doc['corpus'][0]['start'][0]=0;self.reject()
 def test_empty_corpus_path(self):self.doc['corpus'][0]['path']=[];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_wrong_corpus_endpoint(self):self.doc['corpus'][4]['path']=[self.doc['corpus'][4]['start']];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_invalid_state(self):self.assertFalse(verifier.raw_path_valid([[0]],(2,),1,[1,0,0],[7],[7]))
 def test_nonprimitive_move(self):self.assertFalse(verifier.raw_path_valid([[3,5],[5,3]],(2,),2,[2,0,0],[3,5],[5,3]))
 def test_stacked_excursion(self):
  d=(2,2,2,2);k=5;q=[2]*4+[0]*5;x=list(verifier.canonical(d,k,q));s=x[:];path=[s[:]]
  for v in range(1,9):
   for j in range(k):
    if not s[j]>>v&1:s[j]|=1<<v;path.append(s[:])
  path+=list(reversed(path[:-1]));costs=[[abs(a-b) for a,b in zip(verifier.raw_profile(z,d,k),q)] for z in path]
  self.assertTrue(all(max(c)<=1 for c in costs));self.assertTrue(any(sum(c)>1 for c in costs))
  self.assertFalse(verifier.raw_path_valid(path,d,k,q,x,x))
 def test_nonunit_priority(self):self.assertEqual(verifier.outcome(1,[{}]),'NONUNIT_WITNESS')
 def test_unknown_document(self):self.doc['extra']=True;self.reject()
 def test_unknown_entry(self):self.doc['entries'][0]['extra']=True;self.reject()
 def test_unknown_corpus(self):self.doc['corpus'][0]['extra']=True;self.reject()
 def test_scope(self):self.assertEqual(self.check()['universal_unit_barrier'],'UNRESOLVED')
 def direct(self,d,k,q,permutation=None):
  q=list(q)+[0]*(sum(d)+1-len(d));end=list(verifier.canonical(d,k,q));permutation=permutation or list(reversed(range(k)));start=[0]*k
  for j,new in enumerate(permutation):start[new]=end[j]
  path=producer.normalize(start,d,k,q)
  self.assertTrue(verifier.raw_path_valid(path,d,k,q,start,end))
  self.assertTrue(all(z[j]&1 for z in path for j in range(k)))
 def test_singleton_depth4(self):self.direct((2,2,2,2),1,[1]*4)
 def test_singleton_depth8(self):self.direct((2,)*8,1,[1]*8)
 def test_base_packed_star(self):self.direct((3,),3,[3])
 def test_base_spare_star(self):self.direct((3,),4,[3])
 def test_deep_all_saturated(self):self.direct((2,)*8,9,[2]*8)
 def test_deep_alternating(self):self.direct((2,)*8,7,[1,2]*4)
 def test_unequal_degrees(self):self.direct((3,2,3,2),6,[2]*4)
 def test_spare_palette(self):self.direct((2,)*4,7,[2]*4)
 def test_saturated_outer_outer_exchange(self):self.direct((3,2),3,[3,1],[1,0,2])
 def test_compact_bound(self):
  self.assertEqual(verifier.requirements((2,)*8,[2]*8),list(range(9,1,-1)))
  self.assertEqual(verifier.requirements((2,)*4,[1]*4),[1]*4)
 def test_frozen_corpus_identities(self):self.assertEqual(len(verifier.corpus_specs()),210)
 def test_recursive_contract_green(self):self.assertEqual(producer.normalize([511],(2,2,2,2),1,[1]*4+[0]*5),[[511]])
if __name__=='__main__':unittest.main()
