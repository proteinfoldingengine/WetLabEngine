import copy,unittest
import producer as p
import independent as q

class Contracts(unittest.TestCase):
 def data(self):return p.build(True)
 def test_independent(self):self.assertTrue(q.verify(self.data(),True))
 def test_both_modes(self):self.assertEqual([c['mode'] for c in self.data()['cases']],['saturated','slack'])
 def test_positive(self):self.assertTrue(all(c['reachable'] for c in self.data()['cases']))
 def test_exact_tau(self):self.assertTrue(all(c['tau']==3 for c in self.data()['cases']))
 def test_all_anchor_choices(self):self.assertTrue(all(len(c['anchors'])>0 for c in self.data()['cases']))
 def test_shift_graph(self):self.assertTrue(all(c['graph_hash']==c['shifted_graph_hash'] for c in self.data()['cases']))
 def test_zero_residual_floors(self):self.assertIn(0,self.data()['cases'][1]['residual_floors'])
 def test_hidden_checked(self):self.assertGreater(self.data()['counts']['hidden_checks'],0)
 def test_negative(self):self.assertTrue(all(not x['reachable'] for x in self.data()['controls']))
 def test_no_private_rejected(self):
  self.assertFalse(p.private((3,5,6)))
  with self.assertRaises(ValueError):p.case((3,5,6),'saturated')
 def test_zero_original_floor_rejected(self):
  with self.assertRaises(ValueError):p.case((9,10,4,1,8),'invalid',(0,1,1,1))
 def reject(self,change):
  d=copy.deepcopy(self.data());change(d)
  with self.assertRaises(AssertionError):q.verify(d,True)
 def test_omitted_source(self):self.reject(lambda d:d['cases'].pop())
 def test_changed_mode(self):self.reject(lambda d:d['cases'][0].update(mode='other'))
 def test_omitted_anchor(self):self.reject(lambda d:d['cases'][0]['anchors'].pop())
 def test_expansion_corruption(self):self.reject(lambda d:d['cases'][0]['anchors'][0].update(expansions_hash='bad'))
 def test_vertex_corruption(self):self.reject(lambda d:d['cases'][0].update(vertices_hash='bad'))
 def test_edge_corruption(self):self.reject(lambda d:d['cases'][0].update(edges_hash='bad'))
 def test_component_corruption(self):self.reject(lambda d:d['cases'][0].update(components_hash='bad'))
 def test_lift_corruption(self):self.reject(lambda d:d['cases'][0]['anchors'][0].update(lifts_hash='bad'))
 def test_vacancy_corruption(self):self.reject(lambda d:d['cases'][0]['anchors'][0].update(vacancies_hash='bad'))
 def test_rename_corruption(self):self.reject(lambda d:d['cases'][0]['anchors'][0].update(renames_hash='bad'))
 def test_counts_corruption(self):self.reject(lambda d:d['counts'].update(hidden_checks=0))
 def test_positive_route(self):self.assertEqual([len(x['ops']) for x in self.data()['boundary']['positives']],[2,2])
 def test_positive_omission(self):self.reject(lambda d:d['boundary']['positives'].pop())
 def test_private_loss_rejected(self):self.assertTrue(all(x['rejected'] for x in self.data()['boundary']['private_loss']))
 def test_meet_corruption(self):self.reject(lambda d:d['boundary']['private_loss'][0].update(meet=[]))

if __name__=='__main__':unittest.main()
