import copy,unittest
import producer as P,independent as I
class MovingContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=P.build(True)
 def test_fixture_contains_both_floor_modes(self):self.assertEqual(len(self.data['cases']),2)
 def test_saturated_family_route(self):self.assertEqual(len(self.data['families']),1)
 def test_real_fixed_cover(self):self.assertTrue(P.covered((1,1,2,4,8),(0,2,3,4),4))
 def test_marked_target_absence(self):self.assertTrue(P.target_empty((1,0,2,3),(0,1),1))
 def test_unmarked_any_absence(self):self.assertTrue(P.target_empty((1,2,3,4),(1,0),None))
 def test_anonymous_absence_not_marked(self):self.assertFalse(P.target_empty((1,2,3,4),(1,0),2))
 def test_complete_fixture(self):self.assertTrue(I.verify(self.data,True))
 def test_omitted_cases(self):d=copy.deepcopy(self.data);d['cases']=[];self.assertRaises(AssertionError,I.verify,d,True)
 def test_omitted_family(self):d=copy.deepcopy(self.data);d['families']=[];self.assertRaises(AssertionError,I.verify,d,True)
 def corrupt(self,part,key,value):
  d=copy.deepcopy(self.data)
  if not d.get(part):self.fail('Missing required certificate section')
  d[part][0][key]=value;self.assertRaises(AssertionError,I.verify,d,True)
 def test_source_identity(self):self.corrupt('cases','source',[])
 def test_floor_identity(self):self.corrupt('cases','floors',[])
 def test_vertex_omission(self):self.corrupt('cases','vertices_hash','omitted')
 def test_edge_omission(self):self.corrupt('cases','edges_hash','omitted')
 def test_component_omission(self):self.corrupt('cases','components_hash','omitted')
 def test_native_lift_omission(self):self.corrupt('cases','lifts_hash','omitted')
 def test_cover_job_omission(self):self.corrupt('cases','covers',[])
 def test_source_component(self):self.corrupt('cases','reachable',[])
 def test_family_wrong_ops(self):self.corrupt('families','ops',[])
 def test_family_wrong_endpoint(self):self.corrupt('families','states',[])
 def test_family_fixed_cover_obstruction(self):self.corrupt('families','failed_source_covers',[])
 def test_family_anchored_omission(self):self.corrupt('families','anchored_failures',[])
 def test_family_capacity(self):self.corrupt('families','capacity_hash','omitted')

class AdditionalControls(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=P.build(True)
 def mutate_cover(self,key,value):
  d=copy.deepcopy(self.data);d['cases'][1]['covers'][0][key]=value;self.assertRaises(AssertionError,I.verify,d,True)
 def test_cover_vertex_omission(self):self.mutate_cover('vertices_hash','omitted')
 def test_cover_edge_omission(self):self.mutate_cover('edges_hash','omitted')
 def test_marked_identity_corruption(self):self.mutate_cover('D',[])
 def test_target_identity_corruption(self):self.mutate_cover('target',999)
 def test_one_cover_target_job_omission(self):
  d=copy.deepcopy(self.data);d['cases'][1]['covers'].pop();self.assertRaises(AssertionError,I.verify,d,True)
 def test_mandatory_target_requires_moving_cover(self):
  c=self.data['cases'][1];self.assertTrue(c['reachable'][5]);self.assertTrue(any(q['reachable'] for q in c['covers'] if q['target']==-1));self.assertTrue(all(not q['reachable'] for q in c['covers'] if q['target']==4))

if __name__=='__main__':unittest.main()
