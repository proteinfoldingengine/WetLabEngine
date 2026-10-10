import copy,unittest
import producer as p
import independent as q
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=p.build(True)
 def test_independent(self):self.assertTrue(q.verify(self.d,True))
 def test_t1_exception(self):self.assertTrue(all(c['reachable']==bool(c['isolated_types']) for c in self.d['cases'] if c['t']==1))
 def test_classification(self):self.assertTrue(all(c['reachable']==(c['static_spare'] and not c['fingerprint']) for c in self.d['cases']))
 def test_locked_spare(self):self.assertTrue(any(c['static_spare'] and not c['reachable'] for c in self.d['cases']))
 def test_isolated_cost(self):self.assertTrue(all(r['cost']==4 for r in self.d['routes'] if r['kind']=='isolated'))
 def test_cherry_cost(self):self.assertTrue(all(r['cost']==8 for r in self.d['routes'] if r['kind']=='cherry'))
 def test_triple_cost(self):self.assertTrue(all(r['cost']<=13 for r in self.d['routes'] if r['kind']=='triple'))
 def test_first_vacancy(self):self.assertTrue(all(r['first_absent']==r['cost'] for r in self.d['routes']))
 def test_anchors(self):self.assertTrue(all(len(r['anchors'])==4 for r in self.d['routes']))
 def test_lower_bound(self):self.assertEqual(self.d['lower_bound']['minimum_total'],8)
 def test_lower_universe(self):self.assertEqual(self.d['lower_bound']['witnesses'],480)
 def test_hidden(self):self.assertGreater(self.d['counts']['hidden_checks'],0)
 def test_controls(self):self.assertTrue(all(self.d['controls'].values()))
 def test_missing_compensation(self):self.assertTrue(all(r['omission_rejections'] for r in self.d['routes'] if r['kind']!='isolated'))
 def reject(self,f):
  d=copy.deepcopy(self.d);f(d)
  with self.assertRaises(AssertionError):q.verify(d,True)
 def test_graph_omission(self):self.reject(lambda d:d['structures'].pop())
 def test_t_omission(self):self.reject(lambda d:d['cases'].pop())
 def test_vertex(self):self.reject(lambda d:d['cases'][0]['graph'].update(vertices_hash='bad'))
 def test_edge(self):self.reject(lambda d:d['cases'][0]['graph'].update(edges_hash='bad'))
 def test_component(self):self.reject(lambda d:d['cases'][0]['graph'].update(components_hash='bad'))
 def test_static(self):self.reject(lambda d:d['cases'][0].update(static_spare=False))
 def test_certificate(self):self.reject(lambda d:d['structures'][0].update(independent=[]))
 def test_path(self):self.reject(lambda d:d['routes'][0]['ops'].pop())
 def test_anchor(self):self.reject(lambda d:d['routes'][0]['anchors'].pop())
 def test_hidden_omission(self):self.reject(lambda d:d['native'].pop())
 def test_lower_omission(self):self.reject(lambda d:d['lower_bound'].update(witnesses=0))
 def test_identity_omission(self):self.reject(lambda d:d['identities'].pop(next(iter(d['identities']))))
 def raw_reject(self,prefix,field):
  def mutate(d):
   import json
   key=next(k for k in d['identities'] if json.loads(k)[0]==prefix and d['identities'][k][field])
   d['identities'][key][field]=d['identities'][key][field][:-1]
  self.reject(mutate)
 def test_raw_vertex(self):self.raw_reject('count','vertices')
 def test_raw_edge(self):self.raw_reject('count','edges')
 def test_raw_component(self):self.raw_reject('count','components')
 def test_raw_hidden_mask(self):self.raw_reject('native','masks')
 def test_floor_change(self):self.reject(lambda d:d['cases'][0]['graph']['original_floors'].__setitem__(0,0))
 def test_count_change(self):self.reject(lambda d:d['counts'].update(hidden_checks=0))
if __name__=='__main__':unittest.main()
