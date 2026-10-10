import copy,unittest,producer as p,independent as v
class Construction(unittest.TestCase):
 def test_source(self):self.assertEqual(p.source(3),(11,19,35,13,21,37,126,128))
 def test_saturated(self):self.assertEqual(list(map(int.bit_count,p.source(3))),p.floors(3))
 def test_cost(self):self.assertEqual(len(p.release(3,0,1,2)),18)
 def test_first_vacancy(self):self.assertEqual(p.columns(p.route(p.source(3),p.release(3,0,1,2))[-1],8)[0],0)
 def test_static_positive(self):self.assertEqual(p.capacity(3)['minimum'],7)
 def test_static_negative(self):self.assertEqual(p.capacity(2)['minimum'],7)
 def test_bad_domination(self):
  s=list(p.source(3));s[4]|=8;self.assertFalse(p.safe(tuple(s),3))
 def test_native_hidden(self):
  s=list(p.source(3));s[4]|=8;self.assertEqual(p.fulltau(p.source(3),166),3);self.assertEqual(p.fulltau(tuple(s),166),2)
 def test_fresh_label(self):
  s=list(p.source(3));s[0]|=256;self.assertFalse(p.safe(tuple(s),3))
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=p.build(3)
 def test_independent(self):v.verify(self.c,3)
 def reject_list(self,key):
  c=copy.deepcopy(self.c);c[key].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_source_omission(self):self.reject_list('sources')
 def test_route_omission(self):self.reject_list('routes')
 def test_capacity_omission(self):self.reject_list('capacity')
 def test_graph_omission(self):self.reject_list('graphs')
 def test_permutation_omission(self):self.reject_list('permutations')
 def test_renewal_omission(self):self.reject_list('renewal')
 def test_vector_omission(self):
  c=copy.deepcopy(self.c);c['capacity'][0]['vectors'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_count_vertex_omission(self):
  c=copy.deepcopy(self.c);c['graphs'][1]['vertices'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_edge_omission(self):
  c=copy.deepcopy(self.c);c['graphs'][1]['edges'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_witness_omission(self):
  self.assertIn('vacancy_path',self.c['graphs'][1]);c=copy.deepcopy(self.c);c['graphs'][1]['vacancy_path'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_component_corruption(self):
  c=copy.deepcopy(self.c);c['graphs'][1]['components'][0].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_lift_omission(self):
  c=copy.deepcopy(self.c);c['graphs'][1]['edges'][0]['states'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_bad_floor(self):
  c=copy.deepcopy(self.c);c['sources'][0]['floors'][0]=2
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_bad_toggle(self):
  c=copy.deepcopy(self.c);c['routes'][0]['ops'][0][0]=6
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_renewal_bypass(self):
  c=copy.deepcopy(self.c);c['renewal'][0]['boundary']=18
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_equal_counts_do_not_decide_labelled_target(self):self.assertTrue(self.c['singleton_control']['same_counts']);self.assertEqual(self.c['singleton_control']['safe_first_toggles'],0)
if __name__=='__main__':unittest.main()
