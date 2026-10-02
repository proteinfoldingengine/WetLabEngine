"""Prospective two-failure controls; source remains frozen after RED."""
import copy
import importlib.util
import unittest
from unittest.mock import patch
from test_bootstrap import fixture
import verifier

class Prospective(unittest.TestCase):
    def test_four_child_implementation_missing(self):
        self.assertIsNotNone(importlib.util.find_spec('producer'), 'FOUR_CHILD_IMPLEMENTATION_MISSING')

    def test_actual_verifier_omission_red(self):
        complete=fixture()
        self.assertEqual(verifier.verify(complete)['status'],'VERIFIED')
        omitted=copy.deepcopy(complete);omitted['records']=[]
        with self.assertRaises(ValueError):verifier.verify(omitted)
        # Mutate only coverage equality, leaving all scientific checks intact.
        with patch.object(verifier,'verify_identities',lambda actual,expected: None):
            rejected=False
            try:verifier.verify(omitted)
            except ValueError:rejected=True
        self.assertTrue(rejected,'OMITTED_BOUNDARY_CONTROL_ACCEPTED')

if __name__=='__main__':unittest.main(verbosity=2)
