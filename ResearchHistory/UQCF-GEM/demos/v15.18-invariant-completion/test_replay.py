"""Exports must expose completion as a requirement, not state recovery."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import completion as m
r=None
if importlib.util.find_spec('replay'):
    import replay as r

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'completion replay not implemented')
    def test_all_computed_cases_exported(self):
        p=r.payload();self.assertEqual(len(p['cases']),112)
        self.assertEqual(len({(x['family'],x['mask']) for x in p['cases']}),112)
    def test_display_matrices_match_the_algebra(self):
        for c in r.payload()['cases']:
            self.assertEqual(sum(map(sum,c['initial_matrix'])),c['initial_dimension'])
            self.assertEqual(sum(map(sum,c['completed_matrix'])),c['final_dimension'])
    def test_offline_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html';r.write_html(r.payload(),p);s=p.read_text()
            for t in ['not recovered information','Playback is not physical time','No actual record selected','multiplication']:
                self.assertIn(t,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_story_references_existing_cases(self):
        cases={(c['family'],c['mask']) for c in r.payload()['cases']}
        self.assertTrue(all(x in cases for x in r.STORY))
    def test_invalid_movie_rate_rejected(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_displayed_counts_come_from_computation(self):
        p=r.payload();self.assertEqual(p['summary'],m.audit()['classification_by_family'])
        self.assertFalse(p['physical_pruning_law_derived'])

if __name__=='__main__':unittest.main(verbosity=2)
