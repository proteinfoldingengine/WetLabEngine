import copy,unittest
import producer as p
import independent as q
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=p.build(True)
 def test_independent(self):self.assertTrue(q.verify(self.d,True))
 def test_isolation(self):self.assertTrue(all(c['isolated']==c['fingerprint'] for c in self.d['graphs']))
 def test_locked_minimum(self):self.assertEqual(self.d['locked'][0]['minimum'],5)
 def test_star_minimum(self):self.assertEqual(self.d['stars'][0]['minimum'],7)
 def test_first_cost(self):self.assertTrue(all(len(r['ops'])==16 for r in self.d['routes']))
 def test_first_absence(self):self.assertTrue(all(r['first_absent']==16 for r in self.d['routes']))
 def test_batch_cost(self):self.assertEqual(len(self.d['batches'][0]['ops']),36)
 def test_upper5(self):self.assertEqual(self.d['controls']['upper5'],5)
 def test_join_optimal(self):self.assertEqual(self.d['controls']['join_cost'],4)
 def test_certificate_controls(self):self.assertTrue(all(self.d['controls']['rejections'].values()))
 def test_raw_connected(self):self.assertEqual(self.d['raw'][0]['components'],1)
 def test_hidden(self):self.assertGreater(self.d['counts']['hidden_checks'],0)
 def reject(self,f):
  d=copy.deepcopy(self.d);f(d)
  with self.assertRaises(AssertionError):q.verify(d,True)
 def test_graph_omission(self):self.reject(lambda d:d['graphs'].pop())
 def test_graph_identity(self):self.reject(lambda d:d['graphs'][0].update(G=999))
 def test_t_identity(self):self.reject(lambda d:d['graphs'][0].update(t=2))
 def test_source(self):self.reject(lambda d:d['graphs'][0].update(source=[]))
 def test_vertices(self):self.reject(lambda d:d['graphs'][0].update(vertices_hash='bad'))
 def test_edges(self):self.reject(lambda d:d['graphs'][0].update(edges_hash='bad'))
 def test_components(self):self.reject(lambda d:d['graphs'][0].update(components_hash='bad'))
 def test_static(self):self.reject(lambda d:d['locked'][0].update(minimum=0))
 def test_fingerprint(self):self.reject(lambda d:d['graphs'][0].update(fingerprint=True))
 def test_raw(self):self.reject(lambda d:d['raw'][0].update(vertices_hash='bad'))
 def test_lifts(self):self.reject(lambda d:d['raw'][0].update(lifts_hash='bad'))
 def test_hidden_omission(self):self.reject(lambda d:d['raw'][0].update(hidden_hash='bad'))
 def test_first_omission(self):self.reject(lambda d:d['routes'].pop())
 def test_batch_omission(self):self.reject(lambda d:d['batches'].pop())
 def test_count_corruption(self):self.reject(lambda d:d['counts'].update(hidden_checks=0))
 def test_floor_corruption(self):self.reject(lambda d:d['graphs'][0]['original_floors'].__setitem__(0,0))
 def test_identity_omission(self):self.reject(lambda d:d['identities'].pop(next(iter(d['identities']))))
 def test_canonical_vertex_corruption(self):
  def change(d):
   record=d['identities']['["count",0,1]'];record['vertices']=((99,0,0,0,0,0),)+record['vertices'][1:]
  self.reject(change)
 def test_join_hidden(self):self.assertGreater(self.d['controls']['join_hidden_checks'],0)
 def test_join_reverse(self):self.assertIn('join_reverse_hash',self.d['controls'])
 def test_actual_input_rejection(self):
  self.assertTrue(self.d['controls']['rejections']['fresh_label'])
  self.assertTrue(self.d['controls']['rejections']['floor_change'])
if __name__=='__main__':unittest.main()
