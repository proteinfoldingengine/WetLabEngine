import unittest,cross_domain_homset_origin_audit as a
class T(unittest.TestCase):
 def test_retained_leg(self): self.assertTrue(a.run()['retained_leg_derived'])
 def test_quantum_leg(self): self.assertFalse(a.run()['quantum_leg_derived'])
 def test_nine_packages(self): self.assertEqual(len(a.run()['tested_packages']),9)
 def test_none_successful(self): self.assertEqual(a.run()['successful_packages'],[])
 def test_no_homset(self): self.assertFalse(a.run()['cross_domain_homset_derived'])
 def test_scope(self): self.assertIn('not a universal impossibility theorem',a.run()['logical_scope'])
 def test_no_new_primitive(self): self.assertFalse(a.run()['claims']['new_primitive_adopted'])
if __name__=='__main__': unittest.main()
