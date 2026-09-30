"""Deliberately disable verification: the missing-state rejection MUST go RED.
This is mutation-control RED, not a claim of preimplementation TDD.
"""
import unittest,verifier
from test_gate import Gate
verifier.verify=lambda *args,**kwargs: {}
suite=unittest.TestSuite([Gate('test_missing_state')])
result=unittest.TextTestRunner().run(suite)
raise SystemExit(not result.wasSuccessful())
