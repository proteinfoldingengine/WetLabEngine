"""v15.52 Task 2 RED: complete finite source automorphism action."""
from pathlib import Path
import unittest
import obstruction_contract as oc
import source_automorphisms as sa
class AutomorphismTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=oc.load_contract(root); cls.f=sa.frozen_fixture(cls.c); cls.a=sa.enumerate_automorphisms(cls.c,cls.f)
 def test_identity_present(self):
  self.assertIn(tuple(range(len(self.f["objects"]))),self.a)
 def test_complete_against_bruteforce(self):
  self.assertEqual(self.a,sa.bruteforce_preserving_permutations(self.c,self.f))
 def test_every_map_preserves_all_relations(self):
  self.assertTrue(all(sa.preserves(self.c,self.f,p) for p in self.a))
 def test_no_duplicates(self):
  self.assertEqual(len(self.a),len(set(self.a)))
 def test_orbits_partition_objects(self):
  o=sa.object_orbits(self.f,self.a)
  flat=[x for orbit in o for x in orbit]
  self.assertEqual(sorted(flat),list(range(len(self.f["objects"]))))
  self.assertEqual(len(flat),len(set(flat)))
if __name__=="__main__": unittest.main()
