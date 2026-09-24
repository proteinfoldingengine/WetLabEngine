"""Publication-integrity tests use real temporary Git repositories."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True,
                          text=True, capture_output=True).stdout.strip()


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('verify_publication'),
                             'publication verifier is absent')
        import verify_publication
        self.verify = verify_publication.verify
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        git(self.root, 'init', '-q')
        git(self.root, 'config', 'user.name', 'Fixture')
        git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        self.write('engine.py', 'unchanged engine\n')
        self.write('index.md', 'old index\n')
        self.commit('main baseline')
        base = git(self.root, 'rev-parse', 'HEAD')
        old = git(self.root, 'rev-parse', 'HEAD:index.md')
        self.write('versions/v44/model.py', 'x = 1\n')
        self.write('versions/v45/model.py', 'x = 2\n')
        self.write('deps/math.py', 'y = 3\n')
        self.write('old-index.md', 'old index\n')
        self.write('index.md', 'new index\n')
        self.write('pub/README.md', 'publication only\n')
        self.commit('publication')
        self.manifest = {
            'schema': 'uqcf-main-publication-v1', 'base_main': base,
            'source_head': 'a'*40,
            'snapshot_trees': {p: git(self.root, 'rev-parse', 'HEAD:'+p)
                               for p in ('versions/v44', 'versions/v45')},
            'pinned_files': {'deps/math.py': git(self.root, 'rev-parse', 'HEAD:deps/math.py')},
            'index_preservation': {'index.md': {'archive': 'old-index.md', 'blob': old}},
            'auxiliary_added': ['pub/README.md'],
        }

    def write(self, path, text):
        target = self.root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        git(self.root, 'add', '.')
        git(self.root, 'commit', '-qm', message)

    def test_exact_selective_copy_passes(self):
        receipt = self.verify(self.root, self.manifest, git(self.root, 'rev-parse', 'HEAD'))
        self.assertEqual(receipt['status'], 'PUBLICATION_INTEGRITY_VERIFIED')
        self.assertEqual(receipt['snapshot_files'], 2)
        self.assertEqual(receipt['pinned_files'], 1)

    def test_unrelated_main_modification_fails(self):
        self.write('engine.py', 'changed\n'); self.commit('bad engine edit')
        with self.assertRaisesRegex(ValueError, 'outside_publication_scope'):
            self.verify(self.root, self.manifest)

    def test_missing_snapshot_file_fails(self):
        (self.root/'versions/v44/model.py').unlink(); self.commit('missing file')
        with self.assertRaises(ValueError):
            self.verify(self.root, self.manifest)

    def test_altered_dependency_fails(self):
        self.write('deps/math.py', 'changed\n'); self.commit('bad dependency')
        with self.assertRaisesRegex(ValueError, 'pin_mismatch'):
            self.verify(self.root, self.manifest)

    def test_wrong_head_fails(self):
        with self.assertRaisesRegex(ValueError, 'head_mismatch'):
            self.verify(self.root, self.manifest, '0'*40)

    def test_unexpected_added_workflow_fails(self):
        self.write('.github/workflows/extra.yml', 'name: extra\n'); self.commit('extra workflow')
        with self.assertRaisesRegex(ValueError, 'outside_publication_scope'):
            self.verify(self.root, self.manifest)

    def test_uncommitted_change_fails(self):
        self.write('versions/v45/model.py', 'changed but not committed\n')
        with self.assertRaisesRegex(ValueError, 'tracked_worktree_changed'):
            self.verify(self.root, self.manifest)

    def test_old_index_must_be_preserved_exactly(self):
        self.write('old-index.md', 'truncated historical index\n'); self.commit('bad history')
        with self.assertRaisesRegex(ValueError, 'index_archive_mismatch'):
            self.verify(self.root, self.manifest)

    def test_unknown_schema_and_unsafe_paths_fail(self):
        for key, value in [('schema', 'other'), ('pinned_files', {'../escape':'b'*40})]:
            manifest = copy.deepcopy(self.manifest); manifest[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.verify(self.root, manifest)

    def test_pins_cannot_authorize_overwriting_existing_main(self):
        self.write('engine.py', 'replacement\n'); self.commit('bad overwrite')
        manifest = copy.deepcopy(self.manifest)
        manifest['pinned_files']['engine.py'] = git(self.root, 'rev-parse', 'HEAD:engine.py')
        with self.assertRaisesRegex(ValueError, 'existing_main_file_changed'):
            self.verify(self.root, manifest)


if __name__ == '__main__':
    unittest.main()
