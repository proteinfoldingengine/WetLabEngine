"""Substantive input-validation regression discovered during source review."""
import unittest
import engine
import verify
class Validation(unittest.TestCase):
    def test_all_parent_targets_checked_before_traversal(self):
        malformed = (-1, 2, 99)
        try:
            engine.threshold(malformed, [(0,1,2)])
        except Exception as exc:
            self.assertIsInstance(exc, ValueError, 'invalid target must be classified before following pointers')
        else:
            self.fail('malformed lineage accepted')
        with self.assertRaises(ValueError):
            verify.validate(malformed, [(0,1,2)])
    def test_reordered_valid_lineage_remains_accepted(self):
        self.assertEqual(engine.threshold((-1,2,0),[(0,2),(0,2,1)]),1)
if __name__ == '__main__':
    unittest.main(verbosity=2)
