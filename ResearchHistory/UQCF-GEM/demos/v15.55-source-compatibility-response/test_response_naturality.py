"""v15.55 Task 4 RED: full naturality/composition freedom attack."""
import json, unittest
from pathlib import Path
import response_naturality as rn
HERE=Path(__file__).resolve().parent
class NaturalityTests(unittest.TestCase):
 def setUp(self): self.c=json.loads((HERE/"contract.json").read_text())
 def test_exact_refinement(self):
  r=rn.refine_response_space(self.c); self.assertEqual(r["scalar_field"],"Q")
 def test_starts_from_task3(self):
  r=rn.refine_response_space(self.c); self.assertEqual(r["initial_dimension"],4)
 def test_composition_and_naturality_explicit(self):
  r=rn.refine_response_space(self.c)
  self.assertTrue(r["composition_checked"]); self.assertTrue(r["full_naturality_checked"])
 def test_no_new_principle(self):
  r=rn.refine_response_space(self.c); self.assertEqual(r["extra_principles_added"],[])
 def test_dimension_monotone(self):
  r=rn.refine_response_space(self.c); self.assertLessEqual(r["refined_dimension"],r["initial_dimension"])
 def test_verdict_matches_dimension(self):
  r=rn.refine_response_space(self.c)
  if r["refined_dimension"]==0: self.assertEqual(r["primary_verdict"],"UNIQUE_CANONICAL_RESPONSE")
  else: self.assertEqual(r["primary_verdict"],"RESPONSE_NONUNIQUE")
if __name__=="__main__": unittest.main()
