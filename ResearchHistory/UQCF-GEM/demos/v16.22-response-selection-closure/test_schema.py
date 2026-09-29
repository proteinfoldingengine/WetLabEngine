"""Substantive RED: malformed parent scalars must fail explicitly.

Self-review found bool/int list equality could accept a malformed certificate.
These controls are not alterations to the mathematical universe or equations.
"""
import unittest
import engine
import verify

class ParentScalarTests(unittest.TestCase):
    def check_parent(self,value):
        c=engine.produce(3)
        i=c['parents'].index([-1,0,1]);c['parents'][i][2]=value
        with self.assertRaisesRegex(verify.VerificationError,'parent identifiers'):
            verify.verify(c)

    def test_boolean_parent_is_not_an_integer_identifier(self):
        self.check_parent(True)

    def test_float_parent_is_not_an_integer_identifier(self):
        self.check_parent(1.0)
