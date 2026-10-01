"""Mutation RED: disabling verification must fail missing-state rejection."""
import unittest,verifier
from test_gate import Gate
verifier.verify=lambda *args,**kwargs: {}
suite=unittest.TestSuite([Gate('test_missing_state')]);result=unittest.TextTestRunner().run(suite)
raise SystemExit(not result.wasSuccessful())
