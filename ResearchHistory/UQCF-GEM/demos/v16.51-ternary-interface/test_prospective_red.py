"""Genuine mechanism absence and verifier-reached exact-universe failures."""
import unittest, importlib.util
from pathlib import Path
from coverage import verify_identities
OLD=Path(__file__).resolve().parent.parent/'v16.50-recursive-binary-composition'
spec=importlib.util.spec_from_file_location('inherited_binary',OLD/'producer.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
class Red(unittest.TestCase):
    def test_missing_ternary_interface(self):
        self.assertTrue(callable(getattr(old,'normalize_ternary',None)), 'MISSING_TERNARY_INTERFACE')
    def test_verifier_reached_omission(self):
        expected=['otherwise-valid-a','otherwise-valid-b']
        self.assertTrue(verify_identities(expected, expected))
        with self.assertRaises(ValueError, msg='EXACT_UNIVERSE_OMISSION_ACCEPTED'):
            verify_identities(expected[:-1], expected)
if __name__=='__main__':unittest.main()
