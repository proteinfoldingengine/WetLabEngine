import importlib.util
from pathlib import Path
import tempfile
import unittest
import composition_gate as m
p=Path(__file__).with_name('replay.py');r=None
if p.exists():
    spec=importlib.util.spec_from_file_location('v1524_replay',p)
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class ViewTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'composition inspector absent')
    def test_all_fifteen_maps_and_contexts_exported(self):
        d=r.payload();self.assertEqual(len(d['partitions']),15);self.assertEqual(len(d['audit']['contexts']),105)
    def test_all_recipe_entries_reconstruct_the_map(self):
        import numpy as np
        for c in r.payload()['partitions']:
            if c['non_signalling']:
                np.testing.assert_allclose(m.recipe_correlation(c['phase_recipe']),c['matrix'],atol=1e-10)
            else:self.assertIsNone(c['phase_recipe'])
    def test_no_internet_or_physical_time(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.html';r.write_html(r.payload(),p);t=p.read_text()
            for phrase in ('Playback is not physical time','No actual outcome selected','non-signalling','independent'):
                self.assertIn(phrase,t)
            self.assertNotIn('<script src=',t);self.assertNotIn('fetch(',t)
    def test_story_uses_existing_maps(self):
        keys={c['partition'] for c in r.payload()['partitions']}
        self.assertTrue(set(r.STORY)<=keys)
    def test_fps_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_no_hidden_sampling_added_in_presentation(self):
        self.assertFalse(r.payload()['audit']['shared_random_outcome_sampled'])
        self.assertIsNone(r.payload()['audit']['actual_record_selected'])

if __name__=='__main__':unittest.main(verbosity=2)
