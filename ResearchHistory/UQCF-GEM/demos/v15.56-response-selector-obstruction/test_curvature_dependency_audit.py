import unittest
import curvature_dependency_audit as a
class T(unittest.TestCase):
 def test_finite_holonomy_is_input(self): self.assertTrue(a.run()['finite_holonomy_gate_passed'])
 def test_missing_objects_explicit(self):
  r=a.run(); self.assertFalse(r['all_required_objects_earned']); self.assertEqual(sum(r['required_objects'].values()),0)
 def test_old_stacks_not_silently_promoted(self):
  self.assertTrue(all(not x['supplies_missing_objects'] for x in a.run()['archive_candidates'].values()))
 def test_verdict(self): self.assertEqual(a.run()['verdict'],'CURVATURE_LIMIT_BRIDGE_BLOCKED_BY_MISSING_NATIVE_AREA_AND_REFINEMENT')
 def test_no_overclaim(self):
  c=a.run()['claims']; self.assertFalse(c['curvature_density_derived']); self.assertFalse(c['continuum_limit_derived']); self.assertFalse(c['gravity_signal'])
 def test_no_fit(self): self.assertFalse(a.run()['posthoc_fit'])
if __name__=='__main__': unittest.main()
