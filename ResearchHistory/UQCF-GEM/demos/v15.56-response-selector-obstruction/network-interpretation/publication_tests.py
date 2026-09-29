"""Fail-closed tests for publication of the pinned original v16.15 evidence."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent

class PublicationTests(unittest.TestCase):
    def module(self):
        path = HERE / 'publish_evidence.py'
        self.assertTrue(path.is_file(), 'publication verifier absent: expected RED')
        spec = importlib.util.spec_from_file_location('publication1615', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def archive(self):
        return (HERE / 'evidence/original-actions-artifact.zip').read_bytes()

    def test_original_archive_and_all_counts(self):
        m = self.module()
        _, result, summary = m.verify_archive(self.archive())
        self.assertEqual(result['execution_head'], m.SOURCE_SHA)
        self.assertEqual(summary['records'], {'exact': 144, 'local_scalars': 1728, 'pairs': 72, 'independent_loop_checks': 504})
        self.assertEqual(summary['reference_ranks'], {'1': 126, '4': 18})
        self.assertEqual(summary['network_beyond_chosen_local_scalars'], 0)

    def test_tampered_archive_rejected(self):
        m = self.module()
        with self.assertRaises(ValueError):
            m.verify_archive(self.archive() + b'tamper')

    def test_missing_record_rejected(self):
        m = self.module()
        _, result, _ = m.verify_archive(self.archive())
        result['pairs'].pop()
        with self.assertRaises(ValueError):
            m.summarize(result)

    def test_invalid_verdict_rejected(self):
        m = self.module()
        _, result, _ = m.verify_archive(self.archive())
        result['all_valid'] = False
        with self.assertRaises(ValueError):
            m.summarize(result)

    def test_changed_reproduction_rejected(self):
        m = self.module()
        _, original, _ = m.verify_archive(self.archive())
        import copy
        fresh = copy.deepcopy(original)
        fresh['execution_head'] = 'a' * 40
        m.compare_reproduction(original, fresh)
        fresh['pairs'][0]['network_distinguishes'] = True
        with self.assertRaises(ValueError):
            m.compare_reproduction(original, fresh)

if __name__ == '__main__':
    unittest.main()
