"""v15.56 Task 13 RED: audit scalar-to-lineage attachment in prior stack."""
import unittest
import scalar_lineage_audit as sla
class AuditTests(unittest.TestCase):
 def test_v1545_scope(self):
  r=sla.audit(); self.assertEqual(r["v1545_scalar_domain"],"Z_LxZ_L_VERTEX_FIELD")
 def test_attachment_verdict(self):
  self.assertIn(sla.audit()["primary_verdict"],(
   "EARNED_SCALAR_LINEAGE_ATTACHMENT_FOUND","NO_EARNED_SCALAR_LINEAGE_ATTACHMENT"))
 def test_no_coordinate_identity_assumption(self):
  self.assertFalse(sla.audit()["lattice_vertex_equals_lineage_identity_assumed"])
 def test_evidence_paths(self):
  self.assertGreater(len(sla.audit()["evidence_paths"]),0)
if __name__=="__main__": unittest.main()
