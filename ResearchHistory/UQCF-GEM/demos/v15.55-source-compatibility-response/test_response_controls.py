"""v15.55 Task 5 RED: adversarial controls."""
import json, unittest
from pathlib import Path
import response_controls as rc
HERE=Path(__file__).resolve().parent
class ControlTests(unittest.TestCase):
 def setUp(self): self.c=json.loads((HERE/"contract.json").read_text())
 def test_zero_defect_zero_response(self): self.assertTrue(rc.run_controls(self.c)["zero_defect"])
 def test_relabeling(self): self.assertTrue(rc.run_controls(self.c)["relabeling"])
 def test_noncommuting_classical(self): self.assertTrue(rc.run_controls(self.c)["noncommuting_classical_zero"])
 def test_duplicate_presentation(self): self.assertTrue(rc.run_controls(self.c)["duplicate_presentation"])
 def test_operation_order(self): self.assertTrue(rc.run_controls(self.c)["operation_order"])
 def test_spectral_edge_firewall(self): self.assertTrue(rc.run_controls(self.c)["spectral_edge_firewall"])
 def test_dimension_preserved(self): self.assertEqual(rc.run_controls(self.c)["surviving_dimension"],4)
if __name__=="__main__": unittest.main()
