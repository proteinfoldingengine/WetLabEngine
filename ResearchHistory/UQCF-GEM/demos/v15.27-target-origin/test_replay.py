import importlib.util,pathlib,tempfile,unittest
m=None;r=None
model=pathlib.Path(__file__).with_name('target_origin.py')
if model.exists():
    spec=importlib.util.spec_from_file_location('target_origin',model);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
view=pathlib.Path(__file__).with_name('replay.py')
if m is not None and view.exists():
    spec=importlib.util.spec_from_file_location('v1527_replay',view);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class ReplayTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(r,'target-origin presentation absent')
    def test_payload_has_five_candidate_classes(self):self.assertEqual(len(r.payload()['candidates']),5)
    def test_topology_family_exported(self):self.assertEqual([x['alpha'] for x in r.payload()['topology_family']],[-1.0,0.0,1.0])
    def test_self_contained_claim_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'x.html';r.write_html(r.payload(),p);s=p.read_text()
            for x in ('No gravity signal certified','does not factor through q','new law','No physical time'):self.assertIn(x,s)
            self.assertNotIn('<script src=',s);self.assertNotIn('fetch(',s)
    def test_story_modes_valid(self):self.assertTrue(all(x in r.payload()['views'] for x in r.STORY))
    def test_video_guard(self):
        with self.assertRaises(ValueError):r.movie(pathlib.Path('unused.mp4'),0)
    def test_presentation_cannot_upgrade_result(self):
        a=r.payload()['audit'];self.assertFalse(a['signal_of_life']);self.assertFalse(a['gravity_canary_certified'])
if __name__=='__main__':unittest.main(verbosity=2)
