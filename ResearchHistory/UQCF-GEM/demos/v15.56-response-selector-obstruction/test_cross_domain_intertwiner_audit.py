import unittest,cross_domain_intertwiner_audit as a
class T(unittest.TestCase):
 def test_no_existing(self): self.assertFalse(a.run()['existing_natural_intertwiner_found'])
 def test_v1547_nonselective(self): self.assertEqual(a.EVIDENCE['v15_47']['survivor_count'],120)
 def test_v1549_illtyped(self): self.assertEqual(a.EVIDENCE['v15_49']['verdict'],'BRIDGE_ILL_TYPED')
 def test_v1550_missing_quantum_leg(self): self.assertFalse(a.EVIDENCE['v15_50']['quantum_leg_derived'])
 def test_v1551_none_successful(self): self.assertEqual(a.EVIDENCE['v15_51']['successful_packages'],0)
 def test_verdict(self): self.assertEqual(a.run()['verdict'],'NO_FROZEN_OPERATIONAL_QUANTUM_TO_RETAINED_COMPATIBILITY_INTERTWINER')
 def test_not_adopted(self): self.assertFalse(a.run()['claims']['new_axiom_adopted'])
if __name__=='__main__': unittest.main()
