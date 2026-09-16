import importlib.util, pathlib, unittest, tempfile
import selector_rank as m
r=None
p=pathlib.Path(__file__).with_name('replay.py')
if p.exists():
    spec=importlib.util.spec_from_file_location('v1526_replay',p);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'selector-rank presentation absent')
    def test_payload_has_three_selector_targets(self):
        d=r.payload();self.assertEqual(set(d['targets']),{'HODGE_TARGET','MICROSCOPIC_TARGET','CYCLE_SHIFT_TARGET'})
    def test_target_views_match_model(self):
        d=r.payload();a=m.audit()
        self.assertAlmostEqual(d['targets']['HODGE_TARGET']['remote_holonomy'],a['hodge_remote_holonomy'],places=12)
        self.assertAlmostEqual(d['targets']['MICROSCOPIC_TARGET']['remote_holonomy'],a['microscopic_target_remote_holonomy'],places=12)
    def test_self_contained_html_has_claim_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x.html';r.write_html(r.payload(),p);s=p.read_text()
            for text in ('No physical time','No gravity signal certified','same source q','target law'):
                self.assertIn(text,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_story_modes_are_valid(self):
        self.assertTrue(all(x in r.payload()['targets'] for x in r.STORY))
    def test_video_rate_guard(self):
        with self.assertRaises(ValueError):r.movie(pathlib.Path('unused.mp4'),0)
    def test_presentation_cannot_upgrade_canary(self):
        d=r.payload();self.assertFalse(d['audit']['signal_of_life']);self.assertFalse(d['audit']['gravity_canary_certified'])

if __name__=='__main__':unittest.main(verbosity=2)
