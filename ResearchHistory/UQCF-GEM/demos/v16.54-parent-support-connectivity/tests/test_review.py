"""Regression contracts for independent Task 1 provenance review."""
import copy
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from verifier import verify_protocol

class ProtocolReview(unittest.TestCase):
    def protocol(self):
        return json.loads((HERE/'protocol.json').read_text())

    def test_valid_frozen_protocol(self):
        self.assertEqual(verify_protocol(self.protocol(), HERE), [])

    def test_missing_preregistration_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(self.protocol(), HERE))

    def test_changed_plan_commit_rejected_without_binding(self):
        p = self.protocol()
        p['approved_plan_commit'] = '0'*40
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(p, HERE))

    def test_removed_inventories_rejected_without_binding(self):
        p = self.protocol()
        p['proofs'] = {}
        p['reviews'] = {}
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(p, HERE))

    def test_nonimmutable_binding_rejected(self):
        with patch.dict(os.environ, {'PREREGISTRATION_SHA':'HEAD'}):
            self.assertTrue(verify_protocol(self.protocol(), HERE))
