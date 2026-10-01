import unittest,copy
from itertools import combinations
import producer,verifier
SMALL=((2,2,2),(2,2,3),(3,2,2))
class Gate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.fixture=producer.produce(SMALL)
 def setUp(self):self.doc=copy.deepcopy(self.fixture)
 def check(self):return verifier.verify(self.doc,SMALL)
 def reject(self):
  with self.assertRaises(ValueError):self.check()
 def graph(self):return self.doc['entries'][0]['graph']
 def pairs(self):return next(r['pairs'] for r in self.graph()['profiles'] if r['pairs'])
 def test_positive(self):self.assertEqual(self.check()['outcome'],'TWO_BRANCH_THEOREM_VALIDATED')
 def test_missing_state(self):self.graph()['states'].pop();self.reject()
 def test_duplicate_state(self):self.graph()['states'].append(self.graph()['states'][0]);self.reject()
 def test_missing_graph(self):self.doc['entries'].pop();self.reject()
 def test_duplicate_graph(self):self.doc['entries'].append(self.doc['entries'][0]);self.reject()
 def test_wrong_domain(self):self.doc['domain'][0][2]=4;self.reject()
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
 def direct(self,a,b,k,supports):
  start=tuple(sum(1<<v for v,S in enumerate(supports) if j in S) for j in range(k));parents=[-1,0]+[1]*b+[0]*(a-1)
  def profile(state):
   S=[{j for j in range(k) if state[j]>>v&1} for v in range(a+b+1)]
   self.assertEqual(S[0],set(range(k)))
   for v in range(1,len(S)):self.assertTrue(S[v] and S[v]<=S[parents[v]])
   def hit(vertices):
    return next(z for z in range(1,k+1) if any(all(set(H)&S[v] for v in vertices) for H in combinations(range(k),z)))
   return hit([1]+list(range(b+2,a+b+1))),hit(range(2,b+2))
  r,s=profile(start);path=producer.normalize(start,a,b,k,r,s)
  self.assertEqual(tuple(path[0]),start);self.assertEqual(tuple(path[-1]),verifier.canonical(a,b,k,r,s))
  for x,y in zip(path,path[1:]):self.assertEqual(sum((u^v).bit_count() for u,v in zip(x,y)),1)
  for x in path:self.assertLessEqual(sum(abs(u-v) for u,v in zip(profile(x),(r,s))),1)
 def test_single_side_leaf(self):self.direct(2,2,3,[{0,1,2},{1,2},{1},{2},{2}])
 def test_single_inner_label(self):self.direct(2,2,2,[{0,1},{1},{1},{1},{0}])
 def test_delayed_packed_inner(self):self.direct(3,2,2,[{0,1},{0,1},{1},{0},{1},{1}])
 def test_packed_side_downward(self):self.direct(3,2,2,[{0,1},{0},{0},{0},{1},{0}])
 def test_maximum_root_disjoint(self):self.direct(3,2,4,[{0,1,2,3},{0,2},{2},{0},{3},{1}])
 def test_overlap_both_levels(self):self.direct(3,3,3,[{0,1,2},{0,1},{0},{1},{0,1},{0},{2}])
 def test_spare_leaf_inner(self):self.direct(2,3,3,[{0,1,2},{0,1},{1},{0},{1},{2}])
 def test_spare_label_inner(self):self.direct(2,2,3,[{0,1,2},{0,1},{1},{0},{1,2}])
 def test_admitted_nonprimitive_path(self):
  g=self.graph();rec=next(r for r in g['profiles'] if r['pairs']);x,y=rec['pairs'][0]['endpoints']
  self.assertGreater(sum((u^v).bit_count() for u,v in zip(g['states'][x],g['states'][y])),1)
  self.assertFalse(verifier.path_valid([x,y],x,y,g,rec['q']))
 def test_admitted_wrong_endpoint(self):
  g=self.graph();rec=next(r for r in g['profiles'] if r['pairs']);x,y=rec['pairs'][0]['endpoints']
  self.assertNotEqual(x,y);self.assertFalse(verifier.path_valid([x],x,y,g,rec['q']))
 def test_admitted_overcost_path(self):
  g=self.doc['entries'][1]['graph'];rec=next(r for r in g['profiles'] if r['q'][:2]==[2,2]);x=rec['zero_components'][0][0]
  index={tuple(s):i for i,s in enumerate(g['states'])};state=list(g['states'][x]);path=[x]
  for v in range(1,len(g['parents'])):
   for j in range(g['k']):
    if not state[j]>>v&1:state[j]|=1<<v;path.append(index[tuple(state)])
  path+=list(reversed(path[:-1]))
  self.assertTrue(all(sum((u^v).bit_count() for u,v in zip(g['states'][i],g['states'][j]))==1 for i,j in zip(path,path[1:])))
  self.assertFalse(verifier.path_valid(path,x,x,g,rec['q']))
if __name__=='__main__':unittest.main()
