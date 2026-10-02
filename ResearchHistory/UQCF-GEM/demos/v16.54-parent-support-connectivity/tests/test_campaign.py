"""Campaign rejection controls, before campaign implementation."""
import copy
import hashlib
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from campaign import verify_scientific_manifest,validate_campaign_summary

class Campaign(unittest.TestCase):
    def valid(self):
        return {'status':'PASS','expected':2,'checked':2,'failures':0,'incomplete':0,
                'identity_sha256':'a'*64,'verified_identity_sha256':'a'*64,
                'scientific_sha':'b'*40,'workflow_sha':'c'*40}

    def test_valid_manifest(self):
        self.assertEqual(verify_scientific_manifest({'a':b'abc'},{'a':hashlib.sha256(b'abc').hexdigest()}),[])

    def test_corrupted_scientific_bytes_rejected(self):
        self.assertTrue(verify_scientific_manifest({'a':b'abd'},{'a':hashlib.sha256(b'abc').hexdigest()}))

    def test_missing_scientific_file_rejected(self):
        self.assertTrue(verify_scientific_manifest({}, {'a':hashlib.sha256(b'abc').hexdigest()}))

    def test_invalid_provenance_rejected(self):
        s=self.valid();s['scientific_sha']='HEAD'
        self.assertTrue(validate_campaign_summary(s))

    def test_incomplete_cannot_pass(self):
        s=self.valid();s['checked']=1
        self.assertTrue(validate_campaign_summary(s))

    def test_equal_count_wrong_identity_digest_rejected(self):
        s=self.valid();s['verified_identity_sha256']='d'*64
        self.assertTrue(validate_campaign_summary(s))

    def test_failed_cannot_pass(self):
        s=self.valid();s['failures']=1
        self.assertTrue(validate_campaign_summary(s))

    def test_valid_summary(self):
        self.assertEqual(validate_campaign_summary(self.valid()),[])

class AttemptEvidence(unittest.TestCase):
    def run_failure(self,out):
        import json
        from unittest.mock import patch
        from campaign import run_shard
        rows=[{'identity':['M1',str(i).zfill(2),[],[]]} for i in range(16)]
        calls=[]
        def producer(case):
            calls.append(case)
            if len(calls)==2:raise RuntimeError('deliberate second-identity resource failure')
            return {'identity':case['identity'],'status':'PASS','events':[]}
        with patch('campaign.provenance',return_value={'scientific_sha':'b'*40,'workflow_sha':'c'*40}),patch('universe.generate_cases',side_effect=lambda protocol:iter(rows)),patch('verifier.reconstruct_cases',side_effect=lambda protocol:iter(rows)),patch('verifier.verify_protocol',return_value=[]),patch('verifier.verify_record',return_value=[]),patch('mechanisms.produce',side_effect=producer):
            with self.assertRaises(RuntimeError):run_shard('all',0,out)
        return rows

    def test_producer_exception_does_not_reuse_previous_record(self):
        import tempfile,json
        with tempfile.TemporaryDirectory() as out:
            rows=self.run_failure(out)
            failure=json.loads((Path(out)/'FIRST_FAILURE.json').read_text())
            self.assertEqual(failure['case'],rows[1])
            self.assertIsNone(failure['record'])

    def test_current_identity_checkpoint_precedes_production(self):
        import tempfile,json
        with tempfile.TemporaryDirectory() as out:
            rows=self.run_failure(out);checkpoint=Path(out)/'CURRENT_ATTEMPT.json'
            self.assertTrue(checkpoint.exists())
            self.assertEqual(json.loads(checkpoint.read_text())['case'],rows[1])
