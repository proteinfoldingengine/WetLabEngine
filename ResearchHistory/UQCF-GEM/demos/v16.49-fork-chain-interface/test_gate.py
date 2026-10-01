import unittest,copy
import producer,verifier
SMALL=(2,)
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
 def test_positive(self):self.assertEqual(self.check()['outcome'],'FORK_CHAIN_INTERFACE_VALIDATED')
 def test_missing_graph(self):self.doc['entries'].pop();self.reject()
 def test_duplicate_graph(self):self.doc['entries'].append(self.doc['entries'][0]);self.reject()
 def test_substitute_graph(self):self.doc['entries'][0]['k']=7;self.reject()
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
 def test_invalid_state(self):self.assertFalse(verifier.raw_path_valid([[0]],(2,2),(2,2),1,[1]*11,[2047],[2047]))
 def test_nonprimitive_move(self):
  l=r=(2,2);q=verifier.full_profile(l,r,[2,1,1,1,1]);x=list(verifier.canonical(l,r,2,q));y=list(reversed(x))
  self.assertFalse(verifier.raw_path_valid([x,y],l,r,2,q,x,y))
 def test_stacked_excursion(self):
  l=r=(2,2);k=6;q=verifier.full_profile(l,r,[2]*5);x=list(verifier.canonical(l,r,k,q));s=x[:];path=[s[:]]
  for v in range(1,11):
   for j in range(k):
    if not s[j]>>v&1:s[j]|=1<<v;path.append(s[:])
  path+=list(reversed(path[:-1]));costs=[[abs(a-b) for a,b in zip(verifier.raw_profile(z,l,r,k),q)] for z in path]
  self.assertTrue(all(max(c)<=1 for c in costs));self.assertTrue(any(sum(c)>1 for c in costs))
  self.assertFalse(verifier.raw_path_valid(path,l,r,k,q,x,x))
 def test_nonunit_priority(self):self.assertEqual(verifier.outcome(1,[{}]),'NONUNIT_WITNESS')
 def test_unknown_document(self):self.doc['extra']=True;self.reject()
 def test_unknown_entry(self):self.doc['entries'][0]['extra']=True;self.reject()
 def test_unknown_corpus(self):self.doc['corpus'][0]['extra']=True;self.reject()
 def test_scope(self):self.assertEqual(self.check()['universal_unit_barrier'],'UNRESOLVED')
 def direct(self,left,right,k,target,perm=None,transport=False):
  q=verifier.full_profile(left,right,target);end=list(verifier.canonical(left,right,k,q));perm=perm or list(reversed(range(k)));start=[0]*k
  for j,new in enumerate(perm):start[new]=end[j]
  if transport:
   a,b,M=verifier.requirements(left,right,q);path=producer.transport(start,left,right,k,[perm[j] for j in range(a)],[perm[j] for j in range(a,M)])
  else:path=producer.normalize(start,left,right,k,q)
  self.assertTrue(verifier.raw_path_valid(path,left,right,k,q,start,end))
 def test_singleton_children(self):self.direct((2,2),(2,2),1,[1]*5)
 def test_overlap_away_from_zero(self):self.direct((2,2),(2,2),3,[1,1,1,1,1])
 def test_disjoint_singletons(self):self.direct((2,2),(2,2),2,[2,1,1,1,1])
 def test_both_lower_saturated(self):self.direct((2,2),(2,2),6,[2]*5)
 def test_overlap_both_active(self):self.direct((2,2),(2,2),3,[1,2,2,2,2])
 def test_asymmetric_widths(self):self.direct((2,2),(2,2),4,[2,1,1,2,2])
 def test_asymmetric_lengths_degrees(self):self.direct((3,2),(2,2,2),5,[1,2,2,2,2,2])
 def test_asymmetric_disjoint(self):self.direct((3,2),(2,2,2),8,[2,2,2,2,2,2])
 def test_spare_palette(self):self.direct((2,2),(2,2),7,[2]*5)
 def test_cross_child_exchange(self):self.direct((2,2),(2,2),4,[2,1,2,1,2],[2,1,0,3],True)
 def test_within_left_pivot(self):self.direct((2,2),(2,2),4,[2,1,2,1,2],[1,0,2,3],True)
 def test_within_right_pivot(self):self.direct((2,2),(2,2),4,[2,1,2,1,2],[0,1,3,2],True)
 def test_unused_label(self):self.direct((2,2),(2,2),5,[2,1,2,1,2],[4,1,2,3,0],True)
 def test_width_laws(self):
  self.assertEqual(verifier.requirements((2,2),(2,2),verifier.full_profile((2,2),(2,2),[1,2,2,2,2])),(3,3,3))
  self.assertEqual(verifier.requirements((2,2),(2,2),verifier.full_profile((2,2),(2,2),[2,2,2,2,2])),(3,3,6))
 def test_undersized_palette(self):
  with self.assertRaises(ValueError):verifier.canonical((2,2),(2,2),5,verifier.full_profile((2,2),(2,2),[2]*5))
 def test_impossible_profile(self):
  with self.assertRaises(ValueError):verifier.requirements((2,2),(2,2),[3]*11)
 def test_frozen_corpus(self):self.assertEqual(len(verifier.corpus_specs()),192)
 def test_fork_contract_green(self):self.assertEqual(producer.normalize([2047],(2,2),(2,2),1,[1,1,1,0,0,0,1,1,0,0,0]),[[2047]])
if __name__=='__main__':unittest.main()
