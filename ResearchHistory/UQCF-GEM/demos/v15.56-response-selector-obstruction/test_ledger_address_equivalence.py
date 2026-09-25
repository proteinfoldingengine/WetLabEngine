"""v15.56 Task 19 RED: archived ledger vs full branch-address equivalence."""
import unittest
import ledger_address_equivalence as la
class LedgerAddressTests(unittest.TestCase):
 def test_archived_schema(self):
  r=la.audit(); self.assertEqual(r["archived_chain_key"],["prev_root","registry","ordered_slice","event","witnesses"])
 def test_full_branch_address_status(self):
  self.assertIn(la.audit()["primary_verdict"],(
   "PREFIX_STABLE_BRANCH_ADDRESS_EQUIVALENT",
   "HASH_CHAIN_IDENTITY_NOT_BRANCH_ADDRESS_EQUIVALENT"))
 def test_no_overclaim(self):
  r=la.audit()
  if r["primary_verdict"]=="PREFIX_STABLE_BRANCH_ADDRESS_EQUIVALENT":
   self.assertTrue(r["parent_recoverable_from_child_address"])
 def test_no_geometry(self):
  self.assertEqual(la.audit()["geometry_used"],[])
if __name__=="__main__": unittest.main()
