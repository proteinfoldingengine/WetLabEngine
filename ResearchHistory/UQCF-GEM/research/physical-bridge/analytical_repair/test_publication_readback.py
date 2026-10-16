"""Offline rejecting controls for publication metadata; no scientific execution."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('publication_readback', Path(__file__).with_name('publication_readback.py'))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class PublicationReadbackTests(unittest.TestCase):
    def run_case(self, mutation=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            here = root / 'repair'
            here.mkdir()
            index = M.BASE + 'COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'
            paths = [index, 'repair/INDEX_APPEND.md', 'repair/source.txt']
            local = {index: b'old\nnew\n', paths[1]: b'new\n', paths[2]: b'source\n'}
            for path, data in local.items():
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(data)
            manifest = {'parent': M.PARENT, 'contract_commit': M.PARENT,
                        'source_parent': M.ORIGINAL, 'changed_paths': sorted(paths)}
            bound = {'files': {paths[2]: {'bytes': len(local[paths[2]]), 'sha256': M.sha(local[paths[2]])}}}
            state = {'manifest': manifest, 'bound': bound, 'remote': copy.deepcopy(local),
                     'commit': {'sha': 'a'*40, 'parents': [{'sha': M.PARENT}]},
                     'compare': {'status': 'ahead', 'total_commits': 1,
                                 'base_commit': {'sha': M.PARENT}, 'merge_base_commit': {'sha': M.PARENT},
                                 'commits': [{'sha': 'a'*40, 'parents': [{'sha': M.PARENT}]}],
                                 'files': [{'filename': p, 'status': 'modified'} for p in paths]},
                     'prior': b'old\n'}
            if mutation:
                mutation(state)
            (here/'publication_manifest.json').write_text(json.dumps(manifest))
            (here/'input_manifest.json').write_text(json.dumps(bound))
            def get(path):
                return state['commit'] if path.startswith('git/commits/') else state['compare']
            def contents(path, ref):
                return (state['prior'] if ref == M.ORIGINAL else state['remote'][path]), 'mock-blob'
            env = {'GITHUB_SHA': 'a'*40, 'UQCF_WORKFLOW_SHA': 'a'*40, 'GITHUB_RUN_ID': '1', 'GITHUB_RUN_ATTEMPT': '1'}
            with patch.object(M, 'ROOT', root), patch.object(M, 'HERE', here), patch.object(M, 'OUT', root/'out'), patch.object(M, 'get', get), patch.object(M, 'contents', contents), patch.object(M.subprocess, 'check_output', return_value='a'*40), patch.dict(M.os.environ, env):
                M.main()
            return json.loads((root/'out/remote_readback.json').read_text())

    def test_valid_readback(self):
        self.assertTrue(self.run_case()['verified'])

    def test_second_revision(self):
        def mutate(state):
            prior = '8f48da3e3c7f3165e27f64262c87f268cea64165'
            state['manifest']['prior_repair_commits'] = [prior]
            state['commit']['parents'] = [{'sha': prior}]
            state['compare']['total_commits'] = 2
            state['compare']['commits'] = [{'sha': prior, 'parents': [{'sha': M.PARENT}]}, {'sha': 'a'*40, 'parents': [{'sha': prior}]}]
        result = self.run_case(mutate)
        self.assertTrue(result['verified'])
        self.assertEqual(result['immediate_parent'], '8f48da3e3c7f3165e27f64262c87f268cea64165')

    def test_unexpected_revision_chain_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['manifest'].__setitem__('prior_repair_commits', ['b'*40]))

    def test_non_linear_chain_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['compare']['commits'][0].__setitem__('parents', [{'sha': M.PARENT}, {'sha': 'b'*40}]))

    def test_extra_path_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['compare']['files'].append({'filename': 'extra', 'status': 'added'}))

    def test_missing_path_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['compare']['files'].pop())

    def test_remote_source_change_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['remote'].__setitem__('repair/source.txt', b'changed'))

    def test_frozen_source_hash_change_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['bound']['files']['repair/source.txt'].__setitem__('sha256', '0'*64))

    def test_continuation_parent_change_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s.__setitem__('prior', b'wrong\n'))

    def test_source_parent_declaration_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['manifest'].__setitem__('source_parent', '0'*40))

    def test_contract_declaration_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['manifest'].__setitem__('contract_commit', '0'*40))

    def test_api_commit_identity_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_case(lambda s: s['commit'].__setitem__('sha', '0'*40))

    def test_bad_comparison_fields_rejected(self):
        for key, value in [('status', 'diverged'), ('total_commits', 2),
                           ('base_commit', {'sha': '0'*40}), ('merge_base_commit', {'sha': '0'*40}),
                           ('commits', [{'sha': '0'*40}])]:
            with self.subTest(field=key), self.assertRaises(SystemExit):
                self.run_case(lambda s: s['compare'].__setitem__(key, value))

    def test_absent_comparison_fields_rejected(self):
        for key in ['status', 'total_commits', 'base_commit', 'merge_base_commit', 'commits']:
            with self.subTest(field=key), self.assertRaises(SystemExit):
                self.run_case(lambda s: s['compare'].pop(key))

    def test_continuation_remote_bytes_always_checked(self):
        def mutate(state):
            path = M.BASE + 'COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md'
            state['manifest']['changed_paths'].remove(path)
            state['compare']['files'] = [x for x in state['compare']['files'] if x['filename'] != path]
            state['remote'][path] = b'wrong remote continuation'
        with self.assertRaises(SystemExit):
            self.run_case(mutate)


if __name__ == '__main__':
    unittest.main()
