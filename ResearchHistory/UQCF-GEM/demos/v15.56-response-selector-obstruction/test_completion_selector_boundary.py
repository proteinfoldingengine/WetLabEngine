import unittest
import completion_selector_boundary as s
class T(unittest.TestCase):
 def test_response_pair_is_opposite(self): self.assertEqual(s.run()['response_ratios'],['-144/625','144/625'])
 def test_no_frozen_selector(self): self.assertFalse(s.run()['any_frozen_selector_available'])
 def test_v13_no_go_bound(self): self.assertTrue(s.run()['v13_23_factorization_no_go_applies_in_type'].startswith('YES_'))
 def test_later_work_does_not_reopen(self): self.assertTrue(s.run()['later_reopening'].startswith('NO_'))
 def test_verdict(self): self.assertEqual(s.run()['verdict'],'HIDDEN_COMPLETION_SELECTION_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY')
 def test_no_overclaim(self): self.assertFalse(any(s.run()['claims'].values()))
if __name__=='__main__': unittest.main()
