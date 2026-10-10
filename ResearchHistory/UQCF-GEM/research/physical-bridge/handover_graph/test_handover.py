import unittest,producer as p
class Contract(unittest.TestCase):
 def test_actual_nonmonotone_handover_toggles(self):
  self.assertEqual(p.lift((3,1,6,8),(6,1,6,8)),[[0,0],[2,0]])
 def test_upper_four_meet_accepted(self):
  self.assertTrue(p.gate((2,1,6,8),[1]*4,4))
 def test_zero_bridge_lift(self):
  self.assertEqual(p.lift((0,3,6,8),(3,3,6,8)),[[0,0],[1,0]])
class GraphContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import independent as q
  cls.q=q;M=(3,6,8);f=(1,1,1,1);F,FE,FC=p.region(M,f,4);V,E,C=p.graph(M,f,4)
  cls.record={'maxima':list(M),'floors':list(f),'full_vertices':[list(v) for v in F],'full_components':[[list(v) for v in c] for c in FC],'vertices':[list(v) for v in V],'edges':[[list(a),list(b)] for a,b in E],'components':[[list(v) for v in c] for c in C],'component_map':p.equality(FC,C,M)}
 def test_full_component_equivalence(self):self.q.verify_region(self.record)
 def test_omitted_full_vertex_rejected(self):
  import copy
  r=copy.deepcopy(self.record);r['full_vertices'].pop()
  with self.assertRaisesRegex(AssertionError,'full vertex'):self.q.verify_region(r)
 def test_omitted_compressed_vertex_rejected(self):
  import copy
  r=copy.deepcopy(self.record);r['vertices'].pop()
  with self.assertRaisesRegex(AssertionError,'compressed vertex'):self.q.verify_region(r)
 def test_omitted_edge_rejected(self):
  import copy
  r=copy.deepcopy(self.record);r['edges'].pop()
  with self.assertRaisesRegex(AssertionError,'edge identities'):self.q.verify_region(r)
 def test_corrupted_full_partition_rejected(self):
  import copy
  r=copy.deepcopy(self.record);r['full_components'][0].pop()
  with self.assertRaisesRegex(AssertionError,'full components'):self.q.verify_region(r)
 def test_corrupted_compressed_partition_rejected(self):
  import copy
  r=copy.deepcopy(self.record);r['components'][0].pop()
  with self.assertRaisesRegex(AssertionError,'compressed components'):self.q.verify_region(r)
 def test_source_omission_rejected(self):
  with self.assertRaisesRegex(AssertionError,'source universe'):self.q.verify({'sources':self.q.source_universe()[:-1]})
 def test_true_upper_cover_handover_obstruction(self):
  # All A,D,J_i are original inclusion-maximal footprints; original tau3.
  original=(3,12,33,34,36,40,48);self.assertEqual(p.tau(p.roots(original,6)),3)
  a=(3,33,34,36,40,48,48);b=(12,33,34,36,40,48,48);meet=(0,33,34,36,40,48,48)
  self.assertTrue(p.gate(a,[1]*6,6));self.assertTrue(p.gate(b,[1]*6,6));self.assertEqual(p.tau(p.roots(meet,6)),5);self.assertFalse(p.gate(meet,[1]*6,6))
  self.assertEqual(p.maxima(p.roots(original,6),7),tuple(sorted(original)))
 def test_floor_rejects_vertex(self):self.assertFalse(p.gate((0,1,6,8),[2,1,1,1],4))
 def test_multiple_coordinates_are_not_an_edge_lift(self):
  with self.assertRaises(AssertionError):p.lift((3,1,6,8),(6,3,6,8))
 def test_empty_coordinate_retained_in_expansion(self):self.assertEqual(p.expand((0,1,2,8),(3,6,8)),(0,3,3,8))
 def test_nonmonotone_lift_restores_exact_labelled_source(self):
  a=(3,1,6,8);b=(6,1,6,8);ops=p.lift(a,b);self.assertEqual(p.path_states(b,ops[::-1])[-1],a)
class InheritedBoundaryContracts(unittest.TestCase):
 def test_isolated_obstruction_has_singleton_assignment_component(self):
  s=(9,17,33,10,18,34,4);f=[2]*6+[1];M=p.maxima(s,6);a=p.expand(p.columns(s,6),M)
  self.assertEqual(p.reachable(M,f,a),[a]);self.assertNotIn(0,a)
 def test_local_motion_collapses_without_reserve(self):
  s=(5,9,17,6,10,18,224,32);f=[2]*6+[3,1];M=p.maxima(s,8);a=p.expand(p.columns(s,8),M)
  self.assertEqual(p.reachable(M,f,a),[a]);self.assertNotIn(0,a)
 def test_all_expansion_choices_share_a_component(self):
  M=(3,6,8);f=[1]*4;source=(2,1,6,8);V,E,C=p.graph(M,f,4)
  expansions=[v for v in V if all(J&~K==0 for J,K in zip(source,v))]
  hit={i for i,c in enumerate(C) if any(v in c for v in expansions)};self.assertEqual(len(hit),1)
 def test_hidden_upper_control_rejects_empty_meet(self):
  v=(0,33,34,36,40,48,48);self.assertEqual(p.fulltau(v,0,6),5)
 def test_lift_cost_is_symmetric_difference(self):
  a=(3,1,6,8);b=(6,1,6,8);self.assertEqual(len(p.lift(a,b)),(a[0]^b[0]).bit_count())

if __name__=='__main__':unittest.main()
