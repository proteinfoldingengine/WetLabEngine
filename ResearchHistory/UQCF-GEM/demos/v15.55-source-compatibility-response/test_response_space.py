"""v15.55 Task 3 RED: exact response-space parameterization."""
import json, unittest
from pathlib import Path
import response_space as rs
HERE=Path(__file__).resolve().parent

class ResponseSpaceTests(unittest.TestCase):
 def setUp(self): self.c=json.loads((HERE/"contract.json").read_text())
 def test_exact_system(self):
  s=rs.build_constraint_system(self.c)
  self.assertEqual(s["scalar_field"],"Q")
  self.assertGreater(s["variable_count"],0)
  self.assertGreater(s["constraint_count"],0)
 def test_all_frozen_axioms_represented(self):
  s=rs.build_constraint_system(self.c)
  self.assertEqual(set(s["axioms_encoded"]),set(self.c["axioms"]))
 def test_no_spectral_data(self):
  s=rs.build_constraint_system(self.c)
  blob=json.dumps(s,sort_keys=True).lower()
  for banned in ("eigenvalue","eigenvector","spectral_threshold","preferred_mode"):
   self.assertNotIn(banned,blob)
 def test_neutrality_homogeneous(self):
  s=rs.build_constraint_system(self.c); self.assertTrue(s["neutrality_homogeneous"])
 def test_classification_reports_dimension(self):
  r=rs.classify_exact(self.c)
  self.assertIn(r["primary_verdict"],self.c["allowed_verdicts"])
  self.assertIsInstance(r["solution_dimension"],int)
  self.assertGreaterEqual(r["solution_dimension"],0)
if __name__=="__main__": unittest.main()
