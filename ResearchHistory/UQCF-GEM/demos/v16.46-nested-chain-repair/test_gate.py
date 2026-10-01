import unittest,copy
from itertools import combinations
import producer,verifier
SMALL=((2,2,2,2),(2,2,2,3),(3,2,2,2))
class Gate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.fixture=producer.produce(SMALL)
 def setUp(self):self.doc=copy.deepcopy(self.fixture)
 def check(self):return verifier.verify(self.doc,SMALL)
 def reject(self):
  with self.assertRaises(ValueError):self.check()
 def graph(self):return self.doc['entries'][0]['graph']
 def pairs(self):return next(r['pairs'] for r in self.graph()['profiles'] if r['pairs'])
 def test_positive(self):self.assertEqual(self.check()['outcome'],'NON_SATURATED_CHAIN_LEMMA_VALIDATED')
 def test_missing_state(self):self.graph()['states'].pop();self.reject()
 def test_duplicate_state(self):self.graph()['states'].append(self.graph()['states'][0]);self.reject()
 def test_missing_graph(self):self.doc['entries'].pop();self.reject()
 def test_duplicate_graph(self):self.doc['entries'].append(self.doc['entries'][0]);self.reject()
 def test_wrong_domain(self):self.doc['domain'][0][3]=4;self.reject()
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
 def test_wrong_normalization_q(self):self.doc['entries'][0]['normalizations'][0]['q']=[-1];self.reject()
 def test_illegal_path_index(self):self.doc['entries'][0]['normalizations'][0]['path']=[-1];self.assertEqual(self.check()['outcome'],'CONSTRUCTION_REFUTED')
 def test_nonunit_priority(self):self.assertEqual(verifier.outcome(1,[{}]),'NONUNIT_WITNESS')
 def test_unknown_document_field(self):self.doc['extra']=True;self.reject()
 def test_unknown_entry_field(self):self.doc['entries'][0]['extra']=True;self.reject()
 def direct(self,a,b,c,k,S):
  start=tuple(sum(1<<v for v,z in enumerate(S) if j in z) for j in range(k))
  parents=[-1,0,1]+[2]*c+[1]*(b-1)+[0]*(a-1)
  def profile(state):
   T=[{j for j in range(k) if state[j]>>v&1} for v in range(len(parents))]
   self.assertEqual(T[0],set(range(k)))
   for v in range(1,len(T)):self.assertTrue(T[v] and T[v]<=T[parents[v]])
   q=[]
   for v in range(len(T)):
    children=[w for w in range(1,len(T)) if parents[w]==v]
    q.append(next(z for z in range(1,k+1) if any(all(set(H)&T[w] for w in children) for H in combinations(range(k),z))) if children else 0)
   return q
  q=profile(start);self.assertLess(q[0],a);path=producer.normalize(start,a,b,c,k,q)
  self.assertEqual(tuple(path[0]),start);self.assertEqual(tuple(path[-1]),verifier.canonical(a,b,c,k,q))
  for x,y in zip(path,path[1:]):self.assertEqual(sum((u^v).bit_count() for u,v in zip(x,y)),1)
  for x in path:self.assertLessEqual(sum(abs(u-v) for u,v in zip(profile(x),q)),1)
 def test_nested_adjacent_active(self):self.direct(2,2,2,3,[{0,1,2},{0,1,2},{0,1},{1},{0},{2},{0}])
 def test_inner_palette_saturation(self):self.direct(2,2,2,2,[{0,1},{0,1},{0,1},{1},{0},{1},{1}])
 def test_outer_raise(self):self.direct(3,2,2,3,[{0,1,2},{0,1},{0},{0},{0},{1},{2},{2}])
 def test_outer_already_exact(self):self.direct(3,2,2,3,[{0,1,2},{0,1},{0},{0},{0},{1},{0},{2}])
 def test_outer_packed_downward(self):self.direct(3,2,2,2,[{0,1},{0,1},{0,1},{1},{0},{0},{1},{0}])
 def test_middle_extra_leaf(self):self.direct(2,3,2,3,[{0,1,2},{0,1,2},{0,1},{1},{0},{2},{2},{1}])
 def test_bottom_extra_leaf(self):self.direct(2,2,3,3,[{0,1,2},{0,1,2},{0,1},{1},{0},{1},{2},{1}])
 def test_singleton_subtree(self):self.direct(2,2,2,3,[{0,1,2},{2},{2},{2},{2},{2},{2}])
 def test_saturated_scope_rejected(self):
  g=self.graph();rec=next(r for r in g['profiles'] if r['q'][0]==2);x=rec['zero_components'][0][0]
  with self.assertRaises(ValueError):producer.normalize(g['states'][x],2,2,2,2,rec['q'])
  with self.assertRaises(ValueError):verifier.canonical(2,2,2,2,rec['q'])
 def test_saturated_normalization_leak(self):
  e=self.doc['entries'][0];rec=next(r for r in e['graph']['profiles'] if r['q'][0]==2)
  e['normalizations'].append({'state':rec['zero_components'][0][0],'q':rec['q'],'path':None});self.reject()
 def test_saturated_cut_not_construction(self):
  self.assertEqual(verifier.outcome(1,[]),'NONUNIT_WITNESS')
  self.assertEqual(verifier.outcome(0,[{}]),'CONSTRUCTION_REFUTED')
 def test_partition_reporting(self):
  rows=self.check()['per_graph'];self.assertGreater(sum(r['saturated_profiles'] for r in rows),0)
  for r in rows:self.assertEqual(r['pairs'],r['saturated_pairs']+r['non_saturated_pairs'])
 def test_admitted_nonprimitive_path(self):
  g=self.graph();rec=next(r for r in g['profiles'] if r['pairs']);x,y=rec['pairs'][0]['endpoints']
  self.assertGreater(sum((u^v).bit_count() for u,v in zip(g['states'][x],g['states'][y])),1)
  self.assertFalse(verifier.path_valid([x,y],x,y,g,rec['q']))
 def test_admitted_wrong_endpoint(self):
  g=self.graph();rec=next(r for r in g['profiles'] if r['pairs']);x,y=rec['pairs'][0]['endpoints']
  self.assertFalse(verifier.path_valid([x],x,y,g,rec['q']))
 def test_admitted_stacked_path(self):
  g=self.doc['entries'][1]['graph'];rec=next(r for r in g['profiles'] if r['q'][1]==r['q'][2]==2);x=rec['zero_components'][0][0]
  index={tuple(s):i for i,s in enumerate(g['states'])};state=list(g['states'][x]);path=[x]
  for v in range(1,len(g['parents'])):
   for j in range(g['k']):
    if not state[j]>>v&1:state[j]|=1<<v;path.append(index[tuple(state)])
  path+=list(reversed(path[:-1]));costs=[[abs(u-v) for u,v in zip(g['attained_profiles'][g['profile_ids'][i]],rec['q'])] for i in path]
  self.assertTrue(all(max(d)<=1 for d in costs));self.assertTrue(any(sum(d)>1 for d in costs))
  self.assertTrue(all(sum((u^v).bit_count() for u,v in zip(g['states'][i],g['states'][j]))==1 for i,j in zip(path,path[1:])))
  self.assertFalse(verifier.path_valid(path,x,x,g,rec['q']))
 def test_false_general_claim(self):
  result=self.check();self.assertEqual(result['general_saturated_chain'],'UNRESOLVED');self.assertEqual(result['universal_unit_barrier'],'UNRESOLVED')
if __name__=='__main__':unittest.main()
