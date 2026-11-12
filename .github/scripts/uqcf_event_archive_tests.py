import importlib.util
from pathlib import Path
import unittest
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[2]

class ArchiveAuditTest(unittest.TestCase):
    def test_archives_and_tampering(self):
        script=ROOT/'.github/scripts/uqcf_event_archive_audit.py'
        spec=importlib.util.spec_from_file_location('audit',script)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for name,expected in module.ARCHIVES.items():
            raw=(ROOT/module.BASE/'evidence/archives'/name).read_bytes()
            module.verify_archive(raw,expected,ROOT/module.BASE/'evidence'/name.removesuffix('.zip'))
            with self.assertRaises(ValueError):
                module.verify_archive(raw+b'changed',expected,ROOT/module.BASE/'evidence'/name.removesuffix('.zip'))
            with self.assertRaises(ValueError):
                module.verify_archive(raw,expected,ROOT/'missing-extraction')
            with tempfile.TemporaryDirectory() as directory:
                altered=Path(directory)/'extracted'
                shutil.copytree(ROOT/module.BASE/'evidence'/name.removesuffix('.zip'),altered)
                member=next(p for p in altered.iterdir() if p.is_file())
                member.write_bytes(member.read_bytes()+b'changed')
                with self.assertRaises(ValueError):
                    module.verify_archive(raw,expected,altered)

if __name__=='__main__':unittest.main()
