import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

module = None
if importlib.util.find_spec('archive_release'):
    import archive_release as module

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(module, 'archive tooling is not implemented')

    def test_inventory_hash_and_size(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample.txt';p.write_bytes(b'abc')
            self.assertEqual(module.metadata(p)['sha256'], 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
            self.assertEqual(module.metadata(p)['bytes'],3)

    def test_zip_preserves_member_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/'src';src.mkdir();(src/'result.bin').write_bytes(bytes(range(256)))
            z=root/'test.zip';module.package(src,z)
            with zipfile.ZipFile(z) as f:
                self.assertEqual(f.read('result.bin'),bytes(range(256)))
                manifest=json.loads(f.read('PACKAGE_MANIFEST.json'))
                self.assertEqual(manifest['files'][0]['bytes'],256)
                self.assertIsNone(f.testzip())

    def test_zip_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/'src';src.mkdir();(root/'secret').write_text('x');(src/'link').symlink_to(root/'secret')
            with self.assertRaises(ValueError):module.package(src,root/'test.zip')

    def test_same_input_same_zip(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/'src';src.mkdir();(src/'x').write_text('x')
            module.package(src,root/'a.zip');module.package(src,root/'b.zip')
            self.assertEqual((root/'a.zip').read_bytes(),(root/'b.zip').read_bytes())

    def test_remote_digest_and_size_required(self):
        local={'name':'x','bytes':3,'sha256':'a'*64}
        remote={'name':'x','size':3,'digest':'sha256:'+'a'*64,'state':'uploaded'}
        module.verify_remote(local,remote)
        for key,value in [('digest','sha256:'+'b'*64),('size',4),('state','starter'),('name','other')]:
            bad=dict(remote);bad[key]=value
            with self.assertRaises(ValueError):module.verify_remote(local,bad)
        remote.pop('digest')
        with self.assertRaises(ValueError):module.verify_remote(local,remote)

    def test_original_match_is_not_assumed(self):
        local={'name':'generated.mp4','bytes':3,'sha256':'a'*64}
        manifest={'files':[{'name':'original.mp4','bytes':3,'sha256':'b'*64}]}
        self.assertEqual(module.match_original(local,manifest),[])
        manifest['files'][0]['sha256']='a'*64
        self.assertEqual(module.match_original(local,manifest),['original.mp4'])

    def test_build_scope_has_exact_310_tests(self):
        self.assertEqual(sum(s['tests'] for s in module.SUITES),310)
        self.assertEqual(len(module.SUITES),10)
        self.assertEqual([s['version'] for s in module.SUITES],list(range(11,21)))

    def test_failure_log_preserved_and_raises(self):
        import sys
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);log=root/'failure.log'
            with self.assertRaises(RuntimeError):module.run_logged([sys.executable,'-c','print("expected failure");raise SystemExit(7)'],root,log)
            self.assertIn('expected failure',log.read_text())

    def test_logged_json_has_parseable_return_value(self):
        import sys
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);log=root/'output.log'
            output=module.run_logged([sys.executable,'-c','import json; print(json.dumps(dict(ok=True)))'],root,log)
            self.assertTrue(output.lstrip().startswith('{'), 'logged command header leaked into returned JSON')
            self.assertEqual(json.loads(output),{'ok':True})
            self.assertTrue(log.read_text().startswith('Command: '))

    def test_url_allowlist(self):
        module.validate_url('https://uploads.github.com/repos/proteinfoldingengine/WetLabEngine/releases/1/assets')
        for url in ['http://api.github.com/x','https://example.com/x','https://api.github.com.evil.invalid/x']:
            with self.assertRaises(ValueError):module.validate_url(url)

    def test_release_notes_do_not_claim_original_delivery(self):
        text=module.release_notes('source','builder',310)
        self.assertIn('regenerated',text)
        self.assertIn('not the original conversation',text)
        self.assertIn('unchanged',text)
        self.assertNotIn('all original artifacts are archived',text.lower())

if __name__=='__main__':unittest.main(verbosity=2)
