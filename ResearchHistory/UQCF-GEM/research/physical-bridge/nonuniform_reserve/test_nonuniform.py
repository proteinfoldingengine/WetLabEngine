import copy,json,unittest
import producer as p
import independent as q
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=p.build(True)
 def test_independent(self):self.assertTrue(q.verify(self.d,True))
 def test_profiles(self):self.assertGreater(len({tuple(c['profile']) for c in self.d['cases']}),1)
 def test_static(self):self.assertTrue(all(c['static_spare']==(bool(c['isolated_types']) or bool(c['eligible_cherries']) or bool(c['eligible_triples'])) for c in self.d['cases']))
 def test_reachable(self):self.assertTrue(all(c['reachable']==(c['static_spare'] and not c['fingerprint']) for c in self.d['cases']))
 def test_locked_spare(self):self.assertTrue(any(c['static_spare'] and not c['reachable'] for c in self.d['cases']))
 def test_static_obstructed_weak(self):self.assertTrue(any(not c['static_spare'] and not c['fingerprint'] for c in self.d['cases']))
 def test_singleton_donor(self):self.assertGreater(self.d['counts']['singleton_donor_routes'],0)
 def test_exclusion_differs_target(self):self.assertTrue(any(r['excluded_type']!=r['target_type'] for r in self.d['routes']))
 def test_isolated_cost(self):self.assertTrue(all(r['cost']==4 for r in self.d['routes'] if r['kind']=='isolated'))
 def test_cherry_cost(self):self.assertTrue(all(r['cost']==8 for r in self.d['routes'] if r['kind']=='cherry'))
 def test_triple_cost(self):self.assertTrue(all(r['cost']<=13 for r in self.d['routes'] if r['kind']=='triple'))
 def test_first_vacancy(self):self.assertTrue(all(r['first_absent']==r['cost'] for r in self.d['routes']))
 def test_anchor_count(self):self.assertTrue(all(len(r['anchors'])==4 for r in self.d['routes']))
 def test_lower_bound(self):self.assertEqual(self.d['lower_bound']['minimum_total'],8)
 def test_lower_witnesses(self):self.assertEqual(self.d['lower_bound']['witnesses'],480)
 def test_controls(self):self.assertTrue(all(self.d['controls'].values()))
 def test_hidden(self):self.assertGreater(self.d['counts']['hidden_checks'],0)
 def test_compensation(self):self.assertTrue(all(r['omission_rejections'] for r in self.d['routes'] if r['kind']!='isolated'))
 def reject(self,f):
  d=copy.deepcopy(self.d);f(d)
  with self.assertRaises(AssertionError):q.verify(d,True)
 def test_case_omission(self):self.reject(lambda d:d['cases'].pop())
 def test_profile(self):self.reject(lambda d:d['cases'][0]['profile'].__setitem__(0,3))
 def test_floor(self):self.reject(lambda d:d['cases'][0]['graph']['original_floors'].__setitem__(0,0))
 def test_source(self):self.reject(lambda d:d['cases'][0]['graph']['source'].__setitem__(0,1))
 def test_static_witness(self):self.reject(lambda d:d['cases'][0]['witnesses'].pop())
 def test_path(self):self.reject(lambda d:d['routes'][0]['ops'].pop())
 def test_anchor(self):self.reject(lambda d:d['routes'][0]['anchors'].pop())
 def test_exclusion(self):self.reject(lambda d:d['routes'][0].update(excluded_type=-1))
 def test_hidden_omission(self):self.reject(lambda d:d['native'].pop())
 def test_lower_omission(self):self.reject(lambda d:d['lower_bound'].update(witnesses=0))
 def test_count(self):self.reject(lambda d:d['counts'].update(hidden_checks=0))
 def raw(self,prefix,field):
  def mutate(d):
   key=next(k for k,v in d['identities'].items() if json.loads(k)[0]==prefix and v[field]);d['identities'][key][field]=d['identities'][key][field][:-1]
  self.reject(mutate)
 def test_raw_vertex(self):self.raw('universe','vertices')
 def test_raw_edge(self):self.raw('universe','edges')
 def test_raw_component(self):self.raw('universe','components')
 def test_raw_hidden(self):self.raw('native','masks')
 def test_raw_profile_omission(self):
  def mutate(d):d['identities'].pop(next(k for k in d['identities'] if json.loads(k)[0]=='count'))
  self.reject(mutate)
if __name__=='__main__':unittest.main()
