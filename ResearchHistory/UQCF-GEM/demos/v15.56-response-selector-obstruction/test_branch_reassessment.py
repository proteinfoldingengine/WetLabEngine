import unittest,branch_reassessment as b
class T(unittest.TestCase):
 def test_one_live_route(self): self.assertEqual(b.run()['live_routes'],['operational_recoverability_defect_to_compatibility'])
 def test_stops_preserved(self): self.assertTrue(all(v['status']=='STOP' for k,v in b.ROUTES.items() if k!='operational_recoverability_defect_to_compatibility'))
 def test_gate(self): self.assertEqual(b.run()['selected_next_gate'],'OPERATIONAL_DEFECT_TO_RETAINED_COMPATIBILITY_NATURAL_TRANSFORMATION_CLASSIFICATION')
 def test_no_physical_claim(self): self.assertFalse(b.run()['physical_claim'])
if __name__=='__main__': unittest.main()
