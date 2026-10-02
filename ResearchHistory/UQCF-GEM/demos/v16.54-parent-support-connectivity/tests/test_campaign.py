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
