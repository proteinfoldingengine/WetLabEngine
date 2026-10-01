"""Reject lost recursion, stacked defects, corpus corruption, and lost attempts."""
import unittest, copy
from unittest.mock import patch
import producer as p
import verifier as v

class Gate(unittest.TestCase):
 def check(self,t,k,q,start=None,order=None):
  start=p.canonical(t,k,q,order) if start is None else start
  trace=[];path=p.normalize(start,t,k,q,order,trace)
  v.path_check(t,k,q,path,start,p.canonical(t,k,q,order))
  for e in trace:
   if 'end' in e:self.assertEqual(v.profile_check(t,k,path[e['end']]),q)
  return path,trace
 def test_nested_ternary(self):
  path,trace=self.check(p.A,3,[2,3],p.initial(p.A,3,[2,3],'reversal','inflated'))
  self.assertGreater(len(path),1)
 def test_mixed_binary_parent(self):
  t=p.TREES['J'];q=[2]*6
  self.check(t,4,q,p.initial(t,4,q,'reversal','inflated'))
 def test_whole_palette_child_induced_order(self):
  path,trace=self.check(p.A,3,[2,3],p.initial(p.A,3,[2,3],'reversal','compact'))
  full=[e for e in trace if e['kind']=='whole_palette_child']
  self.assertEqual(len(full),1)
  anchor=next(e for e in trace if e['kind']=='anchor')
  self.assertEqual(anchor['label'],2);self.assertEqual(anchor['pair'],[0,1])
  self.assertFalse(any(e['kind']=='role_transport' and e['child']==full[0]['child'] for e in trace))
 def test_local_hole_with_other_child_occupied(self):
  t=p.TREES['G'];q=[2]*4;s=p.canonical(t,3,q);nodes=p.layout(t);c=nodes[0][0];trace=[]
  path=p.transport_child(s,t,c,[0,1],[1,0],[0,1,2],trace)
  region=sum(1<<vtx for vtx in p.vertices(nodes,c));end=s[:]
  end[0]=(s[0]&~region)|(s[1]&region);end[1]=(s[1]&~region)|(s[0]&region)
  v.path_check(t,3,q,path,s,end)
  self.assertTrue(any(e['kind']=='local_hole' and e['label']==2 for e in trace))
 def test_target_one_nested(self):self.check(p.A,3,[1,3],p.initial(p.A,3,[1,3],'reversal','inflated'))
 def test_target_three_nested(self):self.check(p.A,5,[3,3],p.initial(p.A,5,[3,3],'cyclic','inflated'))
 def test_spare_palette(self):self.check(p.A,4,[2,3],p.initial(p.A,4,[2,3],'cyclic','compact'))
 def test_leaf_fixed_root(self):self.assertEqual(p.normalize([1,1],(),2,[]),[[1,1]])
 def test_ordered_equivariance(self):
  t=p.A;q=[2,3];k=3;s=p.initial(t,k,q,'reversal','inflated');base=p.normalize(s,t,k,q);perm=[2,0,1]
  def relabel(s):
   out=[0]*k
   for j in range(k):out[perm[j]]=s[j]
   return out
  self.assertEqual(p.normalize(relabel(s),t,k,q,perm),[relabel(x) for x in base])
 def test_attached_contraction(self):
  t=(p.T,());q=[1,2];k=4;s=p.canonical(t,k,q);path,trace=self.check(t,k,q,s)
  end=p.canonical(t,k,q);self.assertEqual(path[-1],end)
  nodes=p.layout(t);child=nodes[0][0]
  self.assertEqual(sum(bool(z>>child&1) for z in end),2)
 def test_independent_case_universe(self):self.assertEqual(p.specs(),v.expected_specs());self.assertEqual(len(v.expected_specs()),7236)
 def test_shape_profile_counts(self):
  counts={name:sum(s['tree']==name for s in v.expected_specs()) for name in ('A','F','G','H','J')}
  self.assertEqual(counts,{'A':108,'F':324,'G':972,'H':1944,'J':3888})
 def test_independent_model(self):
  for s in v.expected_specs():
   t=p.TREES[s['tree']];M,start,end=v.model(t,s['q'],s['k'],s['permutation'],s['mode'])
   self.assertEqual(M,p.data(t,s['q'])[2][0]);self.assertEqual(start,p.initial(t,s['k'],s['q'],s['permutation'],s['mode']));self.assertEqual(end,p.canonical(t,s['k'],s['q']))
 def test_width_minimality(self):
  for widths,r,want in (((1,1),1,1),((2,3),2,5),((1,1,1),2,2),((2,2,2),2,3),((4,1,1),2,4),((2,3,4),2,5),((2,3,4),3,9)):
   self.assertTrue(v.root_feasible(widths,r,want));self.assertFalse(v.root_feasible(widths,r,want-1))
 def bad(self,change):
  t=p.TREES['G'];k=3;q=[2]*4;s=p.canonical(t,k,q);path=[s[:]];change(path)
  with self.assertRaises(ValueError):v.path_check(t,k,q,path,s,s)
 def test_empty_support(self):self.bad(lambda path:path.append([1,1,1]))
 def test_root_changed(self):self.bad(lambda path:path.append([path[0][0]^1,*path[0][1:]]))
 def test_nonprimitive(self):self.bad(lambda path:path.append(path[0][:]))
 def test_wrong_endpoint(self):
  t=p.A;q=[2,3];s=p.initial(t,3,q,'reversal','compact');path=p.normalize(s,t,3,q)
  self.assertNotEqual(path[-1],s)
  with self.assertRaisesRegex(ValueError,'exact canonical endpoint'):v.path_check(t,3,q,path,s,s)
 def test_unnested_support(self):
  def mutate(path):
   x=path[0][:];x[2]|=1<<2;path.append(x)
  self.bad(mutate)
 def test_bad_representation(self):self.bad(lambda path:path.append([True,0,0]))
 def test_root_and_nested_ternary_stacking(self):
  t=p.TREES['G'];q=[2]*4;s=p.canonical(t,3,q);nodes=p.layout(t);a,b,c=nodes[0]
  x=s[:];x[0]|=1<<c;y=x[:];y[0]|=1<<nodes[a][1]
  self.assertEqual(sum(abs(i-j) for i,j in zip(v.profile_check(t,3,y),q)),2)
  with self.assertRaisesRegex(ValueError,'total excursion'):v.path_check(t,3,q,[s,x,y],s,s)
 def test_two_ternary_children_stacking(self):
  t=p.TREES['G'];q=[2]*4;s=p.canonical(t,3,q);nodes=p.layout(t);a,b,c=nodes[0]
  x=s[:];x[0]|=1<<nodes[a][1];y=x[:];y[0]|=1<<nodes[b][1]
  self.assertEqual(sum(abs(i-j) for i,j in zip(v.profile_check(t,3,y),q)),2)
  with self.assertRaisesRegex(ValueError,'total excursion'):v.path_check(t,3,q,[s,x,y],s,s)
 def test_invalid_profile(self):
  with self.assertRaises(ValueError):v.model(p.A,[4,2],3)
 def test_small_palette(self):
  with self.assertRaises(ValueError):v.model(p.A,[2,3],2)
 def test_scope_rejected(self):
  with self.assertRaises(ValueError):v.verify({'schema':1,'scope':'all trees','kind':'campaign','cases':[]})

class Corpus(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.corpus=p.produce()
 def reject(self,mutate,pattern):
  doc=copy.deepcopy(self.corpus);mutate(doc)
  with self.assertRaisesRegex(ValueError,pattern):v.verify(doc)
 def test_valid_full_corpus(self):
  result=v.verify(self.corpus);self.assertEqual(result['cases'],7236);self.assertEqual(result['kind'],'campaign')
 def test_omitted_full_case(self):self.reject(lambda d:d['cases'].pop(),'identities')
 def test_duplicate_full_case(self):self.reject(lambda d:d['cases'].__setitem__(-1,d['cases'][0]),'identities')
 def test_substituted_full_case(self):self.reject(lambda d:d['cases'][0]['spec'].update(mode='wrong'),'identities')
 def test_wrong_target(self):self.reject(lambda d:d['cases'][0]['spec'].update(q=[2]),'identities')
 def test_wrong_palette_identity(self):self.reject(lambda d:d['cases'][0]['spec'].update(k=999),'identities')
 def test_wrong_width(self):self.reject(lambda d:d['cases'][0].update(width=999),'width/start')
 def test_wrong_start(self):self.reject(lambda d:d['cases'][0].update(start=[]),'width/start')
 def test_claimed_failure(self):self.reject(lambda d:d['cases'][0].update(failure={'message':'failed','category':'construction'}),'construction failure')
 def test_false_schema(self):self.reject(lambda d:d.update(schema=9),'schema/scope')
 def test_extra_record_field(self):self.reject(lambda d:d['cases'][0].update(claimed_total=0),'record keys')
 def test_campaign_not_control(self):self.reject(lambda d:d.update(kind='canonical_coverage_control'),'width/start|control singleton path')

class FailureHandling(unittest.TestCase):
 def test_start_failure_retained(self):
  with patch.object(p,'initial',side_effect=ValueError('INJECTED_START_FAILURE')):doc=p.produce()
  self.assertEqual(len(doc['cases']),7236)
  self.assertTrue(all(row['start'] is None and row['failure']['phase']=='start' for row in doc['cases']))
 def test_construction_failure_retained(self):
  with patch.object(p,'normalize',side_effect=p.ConstructionFailure(ValueError('INJECTED_PATH_FAILURE'),[[1]])):doc=p.produce()
  self.assertEqual(len(doc['cases']),7236)
  self.assertTrue(all(row['path']==[[1]] and row['failure']['phase']=='normalization' for row in doc['cases']))
 def test_scientific_failure_outcome(self):
  import run_campaign
  self.assertEqual(run_campaign.failure_outcome(v.InterfaceNotPreserved('illegal repair')),'INTERFACE_NOT_PRESERVED')
 def test_execution_failure_outcome(self):
  import run_campaign
  self.assertEqual(run_campaign.failure_outcome(ValueError('coverage gap')),'INCOMPLETE')

if __name__=='__main__':unittest.main(verbosity=2)
