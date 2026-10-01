"""Behavioral controls for ternary composition and independent total excursion."""
import unittest, copy
import producer as p
import verifier as v
from coverage import verify_identities

class Gate(unittest.TestCase):
 def check(self,t,k,q,start=None,order=None):
  start=p.canonical(t,k,q,order) if start is None else start
  trace=[];path=p.normalize(start,t,k,q,order,trace)
  endpoint=p.canonical(t,k,q,order)
  v.path_check(t,k,q,path,start,endpoint)
  for e in trace:
   if 'end' not in e:continue
   self.assertEqual(v.profile_check(t,k,path[e['end']]),q)
  return path,trace
 def test_triangle(self):
  path,trace=self.check(p.T,3,[2,2,2,2],p.initial(p.T,3,[2,2,2,2],'reversal','compact'))
  self.assertGreater(len(path),1)
  self.assertTrue(any(e['kind']=='role_transport' for e in trace))
 def test_all_shared_pairs(self):
  for pair in ((0,1),(0,2),(1,2)):
   state=p.canonical(p.T,2,[2,1,1,1]);nodes=p.layout(p.T)
   supports=[{0},{1},{1}]
   for i in range(3):supports[i]={1} if i in pair else {0}
   state=[1,1]
   for i,c in enumerate(nodes[0]):
    for vertex in p.vertices(nodes,c):
     for label in supports[i]:state[label]|=1<<vertex
   path,trace=self.check(p.T,2,[2,1,1,1],state)
   anchor=next(e for e in trace if e['kind']=='anchor')
   self.assertEqual(tuple(anchor['pair']),pair);self.assertEqual(anchor['label'],1)
 def test_whole_palette_child(self):
  q=[2,1,1,1,2,2,2]
  start=p.initial(p.U,4,q,'reversal','interface_and_binary_inflated')
  path,trace=self.check(p.U,4,q,start)
  full=[e for e in trace if e['kind']=='whole_palette_child']
  self.assertEqual(len(full),1)
  self.assertFalse(any(e['kind']=='role_transport' and e['child']==full[0]['child'] for e in trace))
 def test_local_hole_permutation(self):
  t=p.T;q=[2,2,2,2];s=p.canonical(t,3,q);nodes=p.layout(t);child=nodes[0][0];trace=[]
  path=p.transport_child(s,t,child,[0,1],[1,0],[0,1,2],trace)
  end=s[:];region=sum(1<<v for v in p.vertices(nodes,child))
  end[0]=(s[0]&~region)|(s[1]&region);end[1]=(s[1]&~region)|(s[0]&region)
  v.path_check(t,3,q,path,s,end)
  self.assertTrue(any(e['kind']=='local_hole' for e in trace))
 def test_asymmetric(self):
  self.check(p.U,6,[2,2,2,1,2,2,2],p.initial(p.U,6,[2,2,2,1,2,2,2],'cyclic','interface_and_binary_inflated'))
 def test_target_one(self):self.check(p.U,4,[1,2,2,1,2,2,2],p.initial(p.U,4,[1,2,2,1,2,2,2],'reversal','interface_and_binary_inflated'))
 def test_target_three(self):self.check(p.T,6,[3,2,2,2],p.initial(p.T,6,[3,2,2,2],'reversal','compact'))
 def test_spare_palette(self):self.check(p.T,4,[2,2,2,2],p.initial(p.T,4,[2,2,2,2],'cyclic','compact'))
 def test_ordered_equivariance(self):
  t=p.T;q=[2,2,2,2];k=3;s=p.initial(t,k,q,'reversal','compact');base=p.normalize(s,t,k,q)
  perm=[2,0,1]
  def relabel(s):
   out=[0]*k
   for j in range(k):out[perm[j]]=s[j]
   return out
  actual=p.normalize(relabel(s),t,k,q,perm)
  self.assertEqual(actual,[relabel(s) for s in base])
 def test_independent_case_universe(self):self.assertEqual(p.specs(),v.expected_specs());self.assertEqual(len(v.expected_specs()),2592)
 def test_root_two_count(self):self.assertEqual(sum(s['q'][0]==2 for s in v.expected_specs()),864)
 def test_independent_model(self):
  for s in v.expected_specs():
   t=p.TREES[s['tree']];M,start,end=v.model(t,s['q'],s['k'],s['permutation'],s['mode'])
   self.assertEqual(M,p.data(t,s['q'])[2][0]);self.assertEqual(start,p.initial(t,s['k'],s['q'],s['permutation'],s['mode']));self.assertEqual(end,p.canonical(t,s['k'],s['q']))
 def test_width_minimality(self):
  for a,b,c in ((1,1,1),(2,2,2),(4,1,1),(2,3,4)):
   for r in (1,2,3):
    M=max(a,b,c) if r==1 else (a+b+c if r==3 else max(a,b,c,(a+b+c+1)//2))
    self.assertTrue(v.root_feasible(a,b,c,r,M));self.assertFalse(v.root_feasible(a,b,c,r,M-1))
 def test_omitted_identity(self):
  with self.assertRaises(ValueError):verify_identities(['a'],['a','b'])
 def test_duplicate_identity(self):
  with self.assertRaises(ValueError):verify_identities(['a','a'],['a','b'])
 def test_substituted_identity(self):
  with self.assertRaises(ValueError):verify_identities(['a','c'],['a','b'])
 def test_extra_identity(self):
  with self.assertRaises(ValueError):verify_identities(['a','b','c'],['a','b'])
 def test_reordered_identity(self):
  with self.assertRaises(ValueError):verify_identities(['b','a'],['a','b'])
 def bad(self,change):
  t=p.T;k=3;q=[2,2,2,2];s=p.canonical(t,k,q);path=[s[:]];change(path)
  with self.assertRaises(ValueError):v.path_check(t,k,q,path,s,s)
 def test_empty_support(self):self.bad(lambda path:path.append([1,1,1]))
 def test_root_changed(self):self.bad(lambda path:path.append([path[0][0]^1,*path[0][1:]]))
 def test_nonprimitive(self):self.bad(lambda path:path.append(path[0][:]))
 def test_wrong_endpoint(self):
  t=p.T;k=3;q=[2,2,2,2];start=p.initial(t,k,q,'reversal','compact');path=p.normalize(start,t,k,q)
  self.assertNotEqual(path[-1],start)
  with self.assertRaisesRegex(ValueError,'exact canonical endpoint'):v.path_check(t,k,q,path,start,start)
 def test_unnested_support(self):
  def mutate(path):
   x=path[0][:];x[2]|=1<<2;path.append(x)
  self.bad(mutate)
 def test_bad_representation(self):self.bad(lambda path:path.append([True,0,0]))
 def test_root_plus_child_stacking(self):
  t=p.T;k=3;q=[2,2,2,2];s=p.canonical(t,k,q);nodes=p.layout(t);A,B,C=nodes[0]
  # At canonical supports {0,1},{0,2},{1,2}, add 0 to C then to A's second leaf.
  x=s[:];x[0]|=1<<C;y=x[:];y[0]|=1<<nodes[A][1]
  self.assertEqual(sum(abs(a-b) for a,b in zip(v.profile_check(t,k,y),q)),2)
  with self.assertRaisesRegex(ValueError,'total excursion'):v.path_check(t,k,q,[s,x,y],s,s)
 def test_two_child_stacking(self):
  t=p.T;k=3;q=[2,2,2,2];s=p.canonical(t,k,q);nodes=p.layout(t);A,B,C=nodes[0]
  x=s[:];x[0]|=1<<nodes[A][1];y=x[:];y[0]|=1<<nodes[B][1]
  self.assertEqual(sum(abs(a-b) for a,b in zip(v.profile_check(t,k,y),q)),2)
  with self.assertRaisesRegex(ValueError,'total excursion'):v.path_check(t,k,q,[s,x,y],s,s)
 def test_scope_rejected(self):
  with self.assertRaises(ValueError):v.verify({'schema':1,'scope':'all trees','cases':[]})
 def test_missing_case_rejected(self):
  with self.assertRaisesRegex(ValueError,'identities'):v.verify({'schema':1,'scope':v.SCOPE,'cases':[]})
 def test_invalid_profile(self):
  with self.assertRaises(ValueError):v.model(p.T,[4,2,2,2],3)
 def test_small_palette(self):
  with self.assertRaises(ValueError):v.model(p.T,[2,2,2,2],2)
if __name__=='__main__':unittest.main(verbosity=2)
