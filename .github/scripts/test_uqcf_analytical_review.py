"""Offline infrastructure rejection tests; never contact Gemini."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('repair_review_client', Path(__file__).with_name('uqcf_analytical_repair_review.py'))
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewInfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.verdict = {'verdict': 'ACCEPTED', 'findings': [], 'missing_assumptions': [], 'counterexamples': [], 'limitations': []}
        self.response = {'candidates': [{'finishReason': 'STOP', 'content': {'role': 'model', 'parts': [{'text': json.dumps(self.verdict)}]}}]}
        self.identity = {'scientific_sha': 'a'*40, 'workflow_sha': 'a'*40, 'run_id': '123', 'run_attempt': '1'}

    def test_strict_json(self):
        for raw in ['[]', 'null', '{"a":1,"a":2}', '{"x":NaN}', '{"x":Infinity}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                review.strict_object(raw)

    def test_unresolved_findings_block_acceptance(self):
        self.assertTrue(review.accepted(self.verdict))
        for key in ('findings', 'missing_assumptions', 'counterexamples'):
            obj = copy.deepcopy(self.verdict)
            obj[key] = ['unresolved']
            with self.subTest(key=key):
                self.assertFalse(review.accepted(obj))
        for verdict in ('REVISE', 'FAIL'):
            self.assertFalse(review.accepted({**self.verdict, 'verdict': verdict}))

    def test_candidate_must_be_complete_single_text(self):
        self.assertEqual(review.strict_object(review.response_text(self.response)), self.verdict)
        invalid = [{}, {'candidates': []}, {'candidates': self.response['candidates']*2},
                   {'candidates': [{'finishReason': 'MAX_TOKENS', 'content': self.response['candidates'][0]['content']}]},
                   {'candidates': [{'finishReason': 'STOP', 'content': {'role': 'model', 'parts': [{'functionCall': {}}]}}]}]
        for obj in invalid:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                review.response_text(obj)

    def test_artifact_membership_hash_and_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repair_verification'
            root.mkdir()
            provenance = {**self.identity, **review.FROZEN}
            def put(obj):
                (root / 'provenance.json').write_text(json.dumps(obj))
            def seal():
                (root / 'file_manifest.json').write_text(json.dumps({str(p.relative_to(root)): {'bytes': len(p.read_bytes()), 'sha256': review.sha(p.read_bytes())} for p in root.rglob('*') if p.is_file() and p != root / 'file_manifest.json'}))
            put(provenance)
            nested = root / 'nested'
            nested.mkdir()
            (nested / 'file_manifest.json').write_text('{}')
            seal()
            review.validate_artifact(root, {'provenance.json'}, self.identity)
            (root / 'extra.txt').write_text('unexpected')
            with self.assertRaises(ValueError):
                review.validate_artifact(root, {'provenance.json'}, self.identity)
            (root / 'extra.txt').unlink()
            for key in provenance:
                put({**provenance, key: 'wrong'})
                seal()
                with self.subTest(key=key), self.assertRaises(ValueError):
                    review.validate_artifact(root, {'provenance.json'}, self.identity)
            put(provenance)
            seal()
            (root / 'provenance.json').write_text('{}')
            with self.assertRaises(ValueError):
                review.validate_artifact(root, {'provenance.json'}, self.identity)
            put(provenance)
            seal()
            with self.assertRaises(ValueError):
                review.validate_artifact(root, {'required.json'}, self.identity)

    def test_bad_workflow_fails_before_network(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as temporary:
            try:
                os.chdir(temporary)
                environment = {'REVIEW_PHASE': 'mathematical', 'GITHUB_SHA': 'a'*40, 'UQCF_WORKFLOW_SHA': 'b'*40, 'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '1'}
                with patch.dict(os.environ, environment, clear=True), patch.object(review.subprocess, 'check_output', return_value='a'*40), patch.object(review.urllib.request, 'urlopen') as api:
                    with self.assertRaises(SystemExit):
                        review.main()
                    api.assert_not_called()
                error = review.read_object(Path('repair_review/infrastructure_failure.json'))
                self.assertEqual(error['kind'], 'INPUT_VALIDATION')
                self.assertTrue(Path('repair_review/file_manifest.json').is_file())
            finally:
                os.chdir(previous)


if __name__ == '__main__':
    unittest.main()
