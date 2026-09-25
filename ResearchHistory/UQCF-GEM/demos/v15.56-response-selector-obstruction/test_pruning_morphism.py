"""v15.56 Task 28 RED: classify lawful retained pruning morphism."""
import unittest
import pruning_morphism as pm
class T(unittest.TestCase):
 def test_domain(self): self.assertEqual(pm.classify()["domain"],"PREFIX_CLOSED_RETAINED_LINEAGE_SETS")
 def test_map(self): self.assertEqual(pm.classify()["canonical_map"],"ANCESTOR_RETRACTION_TO_NEAREST_RETAINED_PREFIX")
 def test_idempotent(self): self.assertTrue(pm.classify()["idempotent"])
 def test_source_cases(self): self.assertEqual(set(pm.classify()["source_cases"]),{"SOURCE_SURVIVES","SOURCE_PRUNED_TO_RETAINED_ANCESTOR"})
 def test_no_geometry(self): self.assertEqual(pm.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
