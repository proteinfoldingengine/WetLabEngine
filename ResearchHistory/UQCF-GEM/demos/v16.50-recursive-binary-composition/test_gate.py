"""Real rejection and recursive-interface controls; run only on GitHub."""
import unittest,copy
import producer as p,verifier as v
class Gate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.doc=p.produce()
 def test_complete(self):self.assertEqual(v.verify(self.doc)['cases'],1920)
 def test_missing(self):
  d=copy.deepcopy(self.doc);d['cases'].pop()
  with self.assertRaisesRegex(ValueError,'identities'):v.verify(d)
 def test_duplicate(self):
  d=copy.deepcopy(self.doc);d['cases'][-1]=d['cases'][0]
  with self.assertRaisesRegex(ValueError,'identities'):v.verify(d)
 def test_substitute(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['spec']['k']+=100
  with self.assertRaises(ValueError):v.verify(d)
 def test_false_width(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['width']+=1
  with self.assertRaises(ValueError):v.verify(d)
 def test_wrong_start(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['start'][0]^=2
  with self.assertRaises(ValueError):v.verify(d)
 def test_null_path(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['path']=None
  with self.assertRaises(ValueError):v.verify(d)
 def test_wrong_endpoint(self):
  d=copy.deepcopy(self.doc);r=next(r for r in d['cases'] if len(r['path'])>1);r['path']=r['path'][:-1]
  with self.assertRaises(ValueError):v.verify(d)
 def test_root_change(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['path'].append([x^1 for x in d['cases'][0]['start']])
  with self.assertRaises(ValueError):v.verify(d)
 def test_nonprimitive(self):
  d=copy.deepcopy(self.doc);r=next(r for r in d['cases'] if len(r['path'])>3);r['path'].pop(1)
  with self.assertRaises(ValueError):v.verify(d)
 def test_repeat_step(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['path'].append(d['cases'][0]['start'])
  with self.assertRaises(ValueError):v.verify(d)
 def test_invalid_state(self):
  d=copy.deepcopy(self.doc);d['cases'][0]['path'].append([1]*d['cases'][0]['spec']['k'])
  with self.assertRaises(ValueError):v.verify(d)
 def test_false_scope(self):
  d=copy.deepcopy(self.doc);d['scope']='arbitrary trees'
  with self.assertRaises(ValueError):v.verify(d)
 def test_false_schema(self):
  d=copy.deepcopy(self.doc);d['schema']=99
  with self.assertRaises(ValueError):v.verify(d)
 def test_total_stacking(self):
  s=p.canonical(p.F,4,[2,2,2]);a=s[:];a[0]|=1<<3;b=a[:];b[2]|=1<<6
  with self.assertRaisesRegex(ValueError,'total excursion'):v.path_check(p.F,4,[2,2,2],[s,a,b],s,s)
 def test_leaf_fixed_palette(self):self.assertEqual(p.normalize([1,1,1],p.L,3,[]),[[1,1,1]])
 def test_leaf_internal_join(self):
  t=(p.L,p.F);self.check_shape(t,[2,1,2,2],5)
 def test_mirrored_nested(self):self.check_shape((p.C,p.F),[2,2,1,2,2],5)
 def test_asymmetric_palette(self):self.check_shape((p.F,p.C),[2,2,2,1,2],6)
 def test_anchor_excluding_zero(self):self.check_shape(p.N,[1,1,1,1,1],3,'reversal','overlap_inflated')
 def test_minimal_palette(self):self.check_shape(p.D,[2]*7,8)
 def test_spare_palette(self):self.check_shape(p.D,[2]*7,9)
 def test_ordered_equivariance(self):
  t=p.N;q=[2,1,2,2,1];k=6;s=p.canonical(t,k,q);order=list(reversed(range(k)));permuted=list(reversed(s))
  path=p.normalize(permuted,t,k,q,order)
  self.assertEqual(path,[list(reversed(z)) for z in p.normalize(s,t,k,q)])
 def test_left_transport_pivot(self):
  self.direct_transport([1,0,2,3],[1,0],[2,3])
 def test_right_transport_pivot(self):
  self.direct_transport([0,1,3,2],[0,1],[3,2])
 def direct_transport(self,perm,left,right):
  q=[2,2,2];end=p.canonical(p.F,4,q);start=[0]*4
  for j,z in enumerate(end):start[perm[j]]=z
  path=p.transport_roles(start,p.F,1,4,list(range(4)),left,right)
  self.assertEqual(len(path)-1,24)
  v.path_check(p.F,4,q,path,start,end)
 def test_left_same_child_pivot(self):self.check_shape(p.N,[2,2,2,2,2],6,'reversal')
 def test_right_same_child_pivot(self):self.check_shape((p.C,p.F),[2]*5,6,'cyclic')
 def check_shape(self,t,q,k,perm='cyclic',mode='compact'):
  s=p.initial(t,k,q,perm,mode);path=p.normalize(s,t,k,q)
  v.path_check(t,k,q,path,s,p.canonical(t,k,q))
if __name__=='__main__':unittest.main()
