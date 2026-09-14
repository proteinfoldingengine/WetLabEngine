import importlib.util, tempfile, unittest
from pathlib import Path
import pretime_gravity_canary as m
r=None
path=Path(__file__).with_name('replay.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('v1525_replay',path)
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'v15.25 presentation absent')
    def test_payload_contains_all_four_source_orientations(self):
        p=r.payload();self.assertEqual(len(p['orientations']),4)
        self.assertEqual({x['slot'] for x in p['orientations']},{'bottom','right','top','left'})
    def test_payload_exposes_selector_nonuniqueness(self):
        p=r.payload();a=p['audit']
        self.assertFalse(a['global_compatibility_signal'])
        self.assertTrue(a['diagnostic_global_representative'])
        self.assertTrue(a['local_cancellation_exists'])
        self.assertFalse(a['gravity_canary_certified'])
        self.assertGreater(a['response_nonuniqueness_dimension'],0)
    def test_offline_html_has_claim_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'canary.html';r.write_html(r.payload(),path);s=path.read_text()
            for phrase in ['Playback is not physical time','No pruning','selector remains open','not certified gravity']:
                self.assertIn(phrase,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_story_modes_exist(self):
        p=r.payload();modes={x['mode'] for x in p['story']}
        self.assertTrue({'source','remote','null','nonuniqueness'}<=modes)
    def test_video_rate_guard(self):
        with self.assertRaises(ValueError):r.movie(Path('unused.mp4'),fps=0)
    def test_presentation_does_not_upgrade_claim(self):
        p=r.payload();self.assertFalse(p['audit']['canary_positive'])
        self.assertFalse(p['audit']['physical_gravity_derived'])
        self.assertFalse(p['audit']['global_compatibility_signal'])
        self.assertTrue(p['audit']['diagnostic_global_representative'])

if __name__=='__main__':unittest.main(verbosity=2)
