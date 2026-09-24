"""v15.55 Task 6 RED: independent exact verifier."""
import json, unittest
from pathlib import Path
import verify_response as vr
HERE=Path(__file__).resolve().parent
class VerifyTests(unittest.TestCase):
 def setUp(self): self.c=json.loads((HERE/"contract.json").read_text())
 def test_independent_verdict(self):
  r=vr.verify(self.c); self.assertEqual(r["primary_verdict"],"RESPONSE_NONUNIQUE")
 def test_independent_dimension(self):
  r=vr.verify(self.c); self.assertEqual(r["solution_dimension"],4)
 def test_rank(self):
  r=vr.verify(self.c); self.assertEqual((r["variable_count"],r["constraint_rank"]),(7,3))
 def test_no_import_producer(self):
  self.assertTrue(vr.verify(self.c)["producer_semantics_used"] is False)
 def test_double_replay(self):
  self.assertEqual(vr.verify(self.c),vr.verify(json.loads(json.dumps(self.c))))
if __name__=="__main__": unittest.main()
