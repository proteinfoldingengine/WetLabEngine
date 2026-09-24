"""v15.51 Task 1 RED: primitive lattice/output contract."""
from pathlib import Path
import unittest
import primitive_contract as pc
class PrimitiveContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(__file__).resolve().parents[4]; cls.c=pc.load_contract(cls.root)
 def test_sources_pinned(self):
  self.assertGreaterEqual(len(self.c["sources"]),3)
  self.assertTrue(all(len(v["git_blob_sha"])==40 for v in self.c["sources"].values()))
 def test_complete_lattice(self):
  self.assertEqual(set(self.c["packages"]),{"P0","P1","P2","P3","P12","P13","P23","P123","P4"})
 def test_strict_subpackages(self):
  self.assertEqual(set(self.c["strict_subpackages"]["P123"]),{"P0","P1","P2","P3","P12","P13","P23"})
  self.assertIn("P123",self.c["strict_subpackages"]["P4"])
 def test_required_outputs(self):
  self.assertEqual(set(self.c["required_outputs"]),{"carrier_representation_class","subsystem_composition",
    "recovery_capable_operations","typed_quantum_leg"})
 def test_no_quantum_smuggling(self):
  forbidden=set(self.c["forbidden_primitives"])
  for x in ("hilbert_space","matrix_algebra","qubit","born_rule","density_operator","CPTP_map","target_dimension"):
   self.assertIn(x,forbidden)
  for p in self.c["packages"].values():
   self.assertTrue(forbidden.isdisjoint(set(p["assumptions"])))
 def test_downstream_firewall(self):
  self.assertTrue(all(self.c["prohibited_inputs"].values()))
 def test_source_drift_fails_closed(self):
  with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
   pc.load_contract(self.root,overrides={"v1550_result":b"drift"})
if __name__=="__main__": unittest.main()
