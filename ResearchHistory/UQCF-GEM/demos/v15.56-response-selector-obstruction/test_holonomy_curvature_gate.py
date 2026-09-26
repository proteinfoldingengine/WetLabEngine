import unittest
from fractions import Fraction as F
import holonomy_curvature_gate as g
class GateTests(unittest.TestCase):
 def test_holonomy_survives_but_curvature_not_identified(self):
  r=g.run(); self.assertTrue(r['finite_holonomy_response_certified']); self.assertFalse(r['curvature_density_identified'])
 def test_area_scale_changes_candidate_density_only(self):
  a=g.analyze_hidden(F(1,100)); self.assertEqual(a['holonomy_scale_free_ratio'],F(-144,625)); self.assertEqual(a['candidate_density_ratios'],[F(-144,625),F(-336,625),F(-144,1375)]); self.assertGreater(a['density_ratio_spread'],0)
 def test_hidden_sign_survives(self):
  p=g.analyze_hidden(F(1,100)); m=g.analyze_hidden(F(-1,100)); self.assertEqual(p['holonomy_scale_free_ratio'],-m['holonomy_scale_free_ratio'])
 def test_flat_trace_is_incomplete(self):
  c=g.flat_trace_control(); self.assertEqual(c['initial_loop_trace'],3); self.assertEqual(c['loop_trace_jet'],0); self.assertGreater(c['max_holonomy_matrix_jet_entry'],0); self.assertFalse(c['trace_observable_complete'])
 def test_no_fit(self): self.assertFalse(g.run()['posthoc_fit'])
 def test_claim_boundary(self):
  c=g.run()['claims']; self.assertTrue(c['holonomy_response_survives']); self.assertFalse(c['curvature_2form_derived']); self.assertFalse(c['gravity_signal'])
if __name__=='__main__': unittest.main()
