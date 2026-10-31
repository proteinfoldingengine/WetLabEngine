"""Reject archival corruption without executing a scientific program."""
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / '.github/scripts/uqcf_shift_integration_audit.py'

def packed(entries):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(out, 'w') as z:
            for name, value in entries:
                z.writestr(name, value)
    return out.getvalue()

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = None
        if SCRIPT.exists():
            spec=importlib.util.spec_from_file_location('audit', SCRIPT)
            cls.mod=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.mod)

    def test_a_audit_is_implemented(self):
        self.assertTrue(SCRIPT.is_file(), 'integration audit not implemented')

    def module(self):
        if self.mod is None:
            self.skipTest('waiting for implementation')
        return self.mod

    def test_original_archives_and_changed_bytes(self):
        m=self.module()
        for row in m.CONTRACT['archives']:
            raw=(ROOT/m.BASE/row['path']).read_bytes()
            got=m.verify_archive(raw,row['sha256'])
            self.assertEqual(len(got),row['members'])
            with self.assertRaises(ValueError):
                m.verify_archive(raw+b'changed',row['sha256'])

    def test_member_corruption_missing_and_extra(self):
        m=self.module()
        good=b'original'
        manifest={'a.txt':{'bytes':len(good),'sha256':hashlib.sha256(good).hexdigest()}}
        manifest_raw=json.dumps(manifest).encode()
        for entries in [
            [('a.txt',b'altered'),('artifact_manifest.json',manifest_raw)],
            [('artifact_manifest.json',manifest_raw)],
            [('a.txt',good),('extra.txt',b'extra'),('artifact_manifest.json',manifest_raw)],
            [('a.txt',good),('a.txt',good),('artifact_manifest.json',manifest_raw)],
            [('../a.txt',good),('artifact_manifest.json',manifest_raw)],
        ]:
            raw=packed(entries)
            with self.assertRaises(ValueError):
                m.verify_archive(raw,hashlib.sha256(raw).hexdigest())

    def test_complete_accepted_file_set(self):
        m=self.module()
        rows=m.verify_files(ROOT,m.CONTRACT['accepted_files'])
        self.assertEqual(len(rows),34)

    def test_missing_substituted_and_wrong_blob_files(self):
        m=self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'proof.md').write_bytes(b'proof')
            row={'path':'proof.md','git_blob':hashlib.sha1(b'blob 5\0proof').hexdigest()}
            self.assertEqual(len(m.verify_files(root,[row])),1)
            for changed in [{'path':'missing.md','git_blob':row['git_blob']},
                            {'path':'proof.md','git_blob':'0'*40}]:
                with self.assertRaises(ValueError):m.verify_files(root,[changed])
            (root/'proof.md').write_bytes(b'substituted')
            with self.assertRaises(ValueError):m.verify_files(root,[row])

    def test_scope_rejects_missing_unrelated_and_wrong_status(self):
        m=self.module()
        expected={'proof.md':'A','old.md':'M'}
        m.verify_diff(expected,expected)
        for actual in [{'proof.md':'A'},dict(expected,**{'unrelated.py':'M'}),
                       {'proof.md':'A','old.md':'A'}]:
            with self.assertRaises(ValueError):m.verify_diff(actual,expected)

if __name__=='__main__': unittest.main(verbosity=2)
