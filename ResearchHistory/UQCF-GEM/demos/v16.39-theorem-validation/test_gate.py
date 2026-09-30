import unittest,copy,sys
from pathlib import Path
import construct,check
class Construction(unittest.TestCase):
 def test_two_view_swap(self):
  p=[-1,0,0];a=[3,5];b=[5,3];q=[2,0,0]
  proof=construct.build(p,2,q,a,b)
  check.path_states(p,2,q,a,b,proof)
 def test_obstruction_classification(self):
  p=[-1,0,0,1,1];q=[2,2,0,0,0];a=[11,19,5];b=[19,11,5]
  c=construct.classify(p,3,q,a,b)
  self.assertFalse(c['sc']);self.assertFalse(c['endpoint_full'])
  self.assertEqual(c,check.classify(p,3,q,a,b))
 def test_reject_illegal_jump(self):
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],{'states':[[3,5],[5,3]],'zero_prefix':0,'zero_suffix':0})
 def test_reject_wrong_endpoint(self):
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],{'states':[[3,5]],'zero_prefix':0,'zero_suffix':0})
 def test_reject_false_zero_normalization(self):
  proof=construct.build([-1,0,0],2,[2,0,0],[3,5],[5,3])
  proof['zero_prefix']=len(proof['states'])-1
  with self.assertRaises(ValueError):check.path_states([-1,0,0],2,[2,0,0],[3,5],[5,3],proof)
 def test_palette_change_and_shrink(self):
  for a,b in [([3,5,1],[5,1,3]),([3,5,5],[3,3,5])]:
   check.path_states([-1,0,0],3,[2,0,0],a,b,construct.build([-1,0,0],3,[2,0,0],a,b))
 def test_subtree_lifting(self):
  p=[-1,0,0,1];q=[2,1,0,0];a=[11,5];b=[5,11]
  check.path_states(p,2,q,a,b,construct.build(p,2,q,a,b))
 def test_known_child_deficit_path(self):
  states=[[11,19,5],[11,27,5],[27,27,5],[19,27,5],[19,11,5]]
  check.path_states([-1,0,0,1,1],3,[2,2,0,0,0],states[0],states[-1],{'states':states,'zero_prefix':0,'zero_suffix':0})
 def test_known_parent_deficit_path(self):
  states=[[11,19,5],[11,19,7],[11,19,15],[3,19,15],[19,19,15],[19,3,15],[19,11,15],[19,11,7],[19,11,5]]
  check.path_states([-1,0,0,1,1],3,[2,2,0,0,0],states[0],states[-1],{'states':states,'zero_prefix':0,'zero_suffix':0})
 def test_reject_two_simultaneous_deviations(self):
  states=[[11,19,5],[11,19,7],[11,27,7],[11,19,7],[11,19,5],[11,27,5],[27,27,5],[19,27,5],[19,11,5]]
  with self.assertRaises(ValueError):check.path_states([-1,0,0,1,1],3,[2,2,0,0,0],states[0],states[-1],{'states':states,'zero_prefix':0,'zero_suffix':0})
class Certificate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v16.37-certified-closure'))
  import producer
  sys.path.pop(0)
  import campaign
  cls.c=campaign;cls.base=producer.produce(4);cls.doc=campaign.produce(cls.base)
  all5=producer.produce(5)
  cls.obase={'graphs':[g for g in all5['graphs'] if g['parents']==[-1,0,0,1,1] and g['views']==3]}
  cls.odoc=campaign.produce(cls.obase)
 def reject(self,change):
  d=copy.deepcopy(self.doc);change(d)
  with self.assertRaises(ValueError):self.c.verify(self.base,d)
 def test_valid_complete_records(self):self.assertEqual(self.c.verify(self.base,self.doc)['status'],'VERIFIED')
 def test_missing_record(self):self.reject(lambda d:d['records'].pop())
 def test_duplicate_record(self):self.reject(lambda d:d['records'].append(d['records'][0]))
 def test_same_count_substitution(self):self.reject(lambda d:d['records'].__setitem__(0,d['records'][1]))
 def test_false_sc(self):self.reject(lambda d:d['records'][0]['classification'].__setitem__('sc',False))
 def test_false_summary(self):self.reject(lambda d:d['summary'].__setitem__('component_pairs',0))
 def test_false_verdict(self):self.reject(lambda d:d.__setitem__('outcome','UNIT_THEOREM'))
 def test_wrong_schema(self):self.reject(lambda d:d.__setitem__('campaign','16.38'))
 def test_missing_field(self):self.reject(lambda d:d.pop('records'))
 def test_false_failed_coordinate_cut(self):
  d=copy.deepcopy(self.odoc)
  rec=next(r for r in d['records'] if r['static'])
  cut=next(z for z in rec['static'] if 'reachable' in z);cut['reachable']=[]
  with self.assertRaises(ValueError):self.c.verify(self.obase,d)
 def test_false_successful_coordinate(self):
  d=copy.deepcopy(self.odoc);rec=next(r for r in d['records'] if r['static'])
  cut=next(z for z in rec['static'] if 'reachable' in z);cut.pop('reachable');cut['path']=rec['full_unit_path']
  with self.assertRaises(ValueError):self.c.verify(self.obase,d)
 def test_obstruction_records_verified(self):self.assertEqual(self.c.verify(self.obase,self.odoc)['status'],'VERIFIED')
class Provenance(unittest.TestCase):
 def fixture(self):return ({'id':7,'head_sha':'abc','run_attempt':2},{'name':'v1639-science-abc','workflow_run':{'id':7,'head_sha':'abc'}},{'head':'abc','trigger_sha':'abc','workflow_sha':'abc','run_id':'7','run_attempt':'2','phase':'science'})
 def test_current_stage_provenance_accepts(self):
  import publication
  publication.validate_provenance(*self.fixture(),'abc','7','2')
 def test_stage_and_metadata_substitution_rejected(self):
  import publication
  for part,key,value in [(0,'id',8),(0,'head_sha','bad'),(0,'run_attempt',1),(1,'name','v1638-science-abc')]+[(2,k,'bad') for k in self.fixture()[2]]:
   args=list(copy.deepcopy(self.fixture()));args[part][key]=value
   with self.subTest(part=part,key=key),self.assertRaises(ValueError):publication.validate_provenance(*args,'abc','7','2')
 def test_source_membership_and_hash_rejected(self):
  import publication
  for actual in ({'code':'right'},{'code':'right','input':'bad'},{'code':'right','input':'right','extra':'x'}):
   with self.assertRaises(ValueError):publication.validate_source_map({'code':'right','input':'right'},actual)
if __name__=='__main__':unittest.main(verbosity=2)
