"""v15.54 Task 1 RED: frozen operational nonclassicality contract."""
from pathlib import Path
import unittest
import nonclassicality_contract as nc

ROOT=Path(__file__).resolve().parents[4]
VERDICTS=("CERTIFIED_OPERATIONAL_NONCLASSICAL_OBSTRUCTION","OBSTRUCTION_PRESENT_BUT_CLASSICALLY_REPRODUCIBLE","NO_NONCLASSICAL_WITNESS_IN_FROZEN_FAMILY","FAMILY_INVALID","VERIFICATION_FAILED")

class ContractTests(unittest.TestCase):
 def setUp(self): self.c=nc.load_contract(ROOT)
 def test_schema(self): self.assertEqual(self.c["schema"],"uqcf-v1554-nonclassicality-contract-v1")
 def test_predecessor_pins(self):
  self.assertEqual(self.c["sources"]["v1553_results"]["git_blob_sha"],"dfe34bf7b98d708f2f706e293cd7b57d78ed2ea0")
  self.assertEqual(self.c["sources"]["v1553_contract"]["git_blob_sha"],"dc40cf64f857697a24169389af0ad7c1d9b617d9")
  self.assertEqual(nc.verify_sources(ROOT,self.c),self.c["sources"])
 def test_requires_certified_v1553(self): self.assertEqual(self.c["required_v1553_verdict"],"CERTIFIED_FAMILY_OBSTRUCTION_WITNESS")
 def test_ontic_bound_fixed_positive(self):
  self.assertIs(type(self.c["classical_ontic_bound"]),int); self.assertGreater(self.c["classical_ontic_bound"],0)
 def test_witness_frozen_exact(self):
  w=self.c["operational_witness"]; self.assertEqual(w["id"],"CHSH_EXACT")
  self.assertEqual(w["contexts"],["x0y0","x0y1","x1y0","x1y1"])
  self.assertEqual(w["outcomes"],["00","01","10","11"])
  self.assertEqual(w["classical_bound"],[2,1])
 def test_verdicts_exact(self): self.assertEqual(tuple(self.c["primary_verdicts"]),VERDICTS)
 def test_forbidden_fields(self):
  self.assertTrue({"nonclassical","target_class","E_observables","post_result_gauge","fixture_order_selector"}<=set(self.c["forbidden_fields"]))
 def test_firewall(self):
  self.assertEqual(self.c["source_correspondence"],"NOT_EVALUATED"); self.assertEqual(self.c["Pillar_3"],"OPEN")
  for k in ("physical_source_law","physical_gravity","geometry_or_curvature","continuum_limit","empirical_fit","fundamental_physical_time","dark_matter_primitive","universal_quantum_derivation"): self.assertFalse(self.c[k])
 def test_source_drift_fails(self):
  c=nc.load_contract(ROOT); c["sources"]["v1553_results"]["git_blob_sha"]="0"*40
  with self.assertRaises(ValueError): nc.verify_sources(ROOT,c)
if __name__=="__main__": unittest.main()
