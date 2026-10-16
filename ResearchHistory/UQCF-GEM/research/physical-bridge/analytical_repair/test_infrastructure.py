"""Infrastructure rejection regressions; no scientific producer/checker imports."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import campaign as c


class InfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {
            'GITHUB_SHA': 'a' * 40, 'UQCF_WORKFLOW_SHA': 'a' * 40,
            'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '2'})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_workflow_sha_is_actual_workflow_identity(self):
        with patch.dict(os.environ, {'UQCF_WORKFLOW_SHA': 'b' * 40}):
            with self.assertRaisesRegex(ValueError, 'actual workflow'):
                c.expected_provenance()

    def test_every_provenance_field_is_required(self):
        expected = c.expected_provenance()
        c.validate_provenance(expected)
        for field in expected:
            with self.subTest(field=field):
                obj = dict(expected)
                obj.pop(field)
                with self.assertRaises(ValueError):
                    c.validate_provenance(obj)

    def test_run_attempt_is_bound(self):
        obj = c.expected_provenance()
        obj['run_attempt'] = '1'
        with self.assertRaisesRegex(ValueError, 'run_attempt'):
            c.validate_provenance(obj)

    def test_nested_manifest_bytes_are_bound(self):
        nested = self.directory / 'nested'
        nested.mkdir()
        (nested / 'file_manifest.json').write_text('{}')
        c.manifest(self.directory)
        c.check_manifest(self.directory)
        (nested / 'file_manifest.json').write_text('{"changed":true}')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            c.check_manifest(self.directory)

    def test_artifact_manifest_rejects_unsafe_paths(self):
        c.dump(self.directory / 'file_manifest.json', {'../outside': {}})
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            c.check_manifest(self.directory)

    def test_intact_artifact_from_wrong_run_rejected(self):
        provenance = c.expected_provenance()
        provenance['run_id'] = 'another-run'
        c.dump(self.directory / 'provenance.json', provenance)
        c.manifest(self.directory)
        with self.assertRaisesRegex(ValueError, 'run_id'):
            c.upstream(self.directory)

    def test_accepted_review_with_findings_is_rejected(self):
        obj = {'verdict': 'ACCEPTED', 'findings': [], 'missing_assumptions': [], 'counterexamples': []}
        c.validate_review_verdict(obj)
        obj['findings'] = ['substantive unresolved finding']
        with self.assertRaisesRegex(ValueError, 'review unresolved'):
            c.validate_review_verdict(obj)
        del obj['findings']
        with self.assertRaisesRegex(ValueError, 'review unresolved'):
            c.validate_review_verdict(obj)

    def test_remote_readback_requires_exact_path_universe(self):
        c.dump(self.directory / 'input_manifest.json', {'files': {'expected.md': {}}})
        c.dump(self.directory / 'remote_readback.json', {
            'verified': True, 'scientific_sha': 'a' * 40,
            'parent': c.CONTRACT_COMMIT, 'continuation_parent': c.SOURCE_PARENT,
            'files': {'substitute.md': {}}})
        with patch.object(c, 'HERE', self.directory), patch.object(c, 'validate_inputs'), patch.object(c, 'publication_paths', return_value={'expected.md'}):
            with self.assertRaisesRegex(ValueError, 'path set mismatch'):
                c.validate_remote(self.directory)

    def revision_fixture(self):
        prior = '8f48da3e3c7f3165e27f64262c87f268cea64165'
        head = 'a' * 40
        first = {'sha': prior, 'parents': [{'sha': c.CONTRACT_COMMIT}]}
        current = {'sha': head, 'parents': [{'sha': prior}]}
        compare = {'total_commits': 2, 'commits': [first, current]}
        publication = {'prior_repair_commits': [prior]}
        return current, compare, publication

    def test_second_revision_preserves_cumulative_commit_identity(self):
        commit, compare, publication = self.revision_fixture()
        c.validate_remote_commits(commit, compare, publication)
        commit['parents'] = [{'sha': c.CONTRACT_COMMIT}]
        with self.assertRaisesRegex(ValueError, 'remote commit parent'):
            c.validate_remote_commits(commit, compare, publication)

    def test_second_revision_rejects_substituted_or_omitted_prior_commit(self):
        for mutation in ('substitute', 'omit', 'wrong_total', 'merge_parent'):
            commit, compare, publication = self.revision_fixture()
            if mutation == 'substitute':
                compare['commits'][0]['sha'] = 'b' * 40
            elif mutation == 'omit':
                compare['commits'].pop(0)
            elif mutation == 'wrong_total':
                compare['total_commits'] = 1
            else:
                compare['commits'][0]['parents'].append({'sha': 'b' * 40})
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                c.validate_remote_commits(commit, compare, publication)

    def test_first_revision_remains_bound_to_contract(self):
        head = 'a' * 40
        commit = {'sha': head, 'parents': [{'sha': c.CONTRACT_COMMIT}]}
        c.validate_remote_commits(commit, {'total_commits': 1, 'commits': [commit]}, {})

    def input_fixture(self):
        (self.directory / 'CONTRACT.md').write_bytes((c.HERE / 'CONTRACT.md').read_bytes())
        changed = sorted([c.REPAIR + 'input_manifest.json', c.REPAIR + 'new_source.md'])
        c.dump(self.directory / 'publication_manifest.json', {
            'source_parent': c.SOURCE_PARENT, 'contract_commit': c.CONTRACT_COMMIT,
            'changed_paths': changed})
        files = {name: {} for name in c.MANDATORY_PATHS}
        files[c.REPAIR + 'new_source.md'] = {}
        files[c.REPAIR + 'CONTRACT.md'] = {'sha256': c.CONTRACT_SHA256}
        return {'source_parent': c.SOURCE_PARENT, 'contract_commit': c.CONTRACT_COMMIT, 'files': files}

    def test_each_mandatory_source_path_is_required(self):
        bound = self.input_fixture()
        with patch.object(c, 'HERE', self.directory):
            c.validate_inputs(bound)
            for path in c.MANDATORY_PATHS:
                with self.subTest(path=path):
                    obj = copy.deepcopy(bound)
                    del obj['files'][path]
                    with self.assertRaisesRegex(ValueError, 'missing required'):
                        c.validate_inputs(obj)

    def test_publication_changed_paths_require_input_binding(self):
        bound = self.input_fixture()
        del bound['files'][c.REPAIR + 'new_source.md']
        with patch.object(c, 'HERE', self.directory):
            with self.assertRaisesRegex(ValueError, 'missing required'):
                c.validate_inputs(bound)

    def test_contract_bytes_and_frozen_parent_are_required(self):
        bound = self.input_fixture()
        with patch.object(c, 'HERE', self.directory):
            obj = copy.deepcopy(bound)
            obj['source_parent'] = 'b' * 40
            with self.assertRaisesRegex(ValueError, 'frozen source'):
                c.validate_inputs(obj)
            (self.directory / 'CONTRACT.md').write_text('replacement')
            with self.assertRaisesRegex(ValueError, 'contract bytes changed'):
                c.validate_inputs(bound)

    def test_same_count_substituted_inherited_suite_rejected_before_execution(self):
        folder = self.directory / 'record_conversion'
        folder.mkdir()
        suites = list(c.SUITES)
        suites[0] = ('substituted', 'test_fake.py')
        (folder / 'ci_campaign.py').write_text('SUITES=' + repr(suites))
        with patch.object(c, 'BASE', self.directory), patch.object(c, 'run') as runner:
            with self.assertRaisesRegex(ValueError, 'exact suite identities'):
                c.regression(self.directory)
            runner.assert_not_called()


if __name__ == '__main__':
    unittest.main()
