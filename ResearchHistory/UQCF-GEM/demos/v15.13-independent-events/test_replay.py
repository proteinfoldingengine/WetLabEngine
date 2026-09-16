import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import event_model as m
if importlib.util.find_spec('replay'):
    import replay
else:
    replay=None

class ReplayTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(replay, 'independent-event replay not implemented')
    def test_compare_only_equal_completed_sets(self):
        fs=m.run(m.schedules()[0],'1001'); gs=m.run(m.schedules()[-1],'1001')
        self.assertFalse(replay.comparison(fs[1],gs[1])['comparable'])
        self.assertIsNone(replay.comparison(fs[1],gs[1])['state_distance'])
        self.assertTrue(replay.comparison(fs[-1],gs[-1])['comparable'])
        self.assertLess(replay.comparison(fs[-1],gs[-1])['state_distance'],1e-11)
    def test_html_has_no_external_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'replay.html'
            replay.write_html(m.build_payload(),p)
            s=p.read_text()
            self.assertIn('Playback is not physical time',s)
            self.assertIn('Independent operations',s)
            self.assertNotIn('<script src=',s)
            self.assertNotIn('fetch(',s)
    def test_replay_contains_all_supplied_data(self):
        p=m.build_payload()
        self.assertEqual(len(p['branches']),16)
        for trajectories in p['branches'].values():
            self.assertEqual(len(trajectories),6)
            for trajectory in trajectories:
                self.assertEqual(len(trajectory['snapshots']),5)
                for snap in trajectory['snapshots']:
                    self.assertAlmostEqual(sum(snap['probabilities']),1.,places=11)
    def test_bad_fps_rejected(self):
        with self.assertRaises(ValueError): replay.movie(Path('unused.mp4'),fps=0)

if __name__=='__main__': unittest.main(verbosity=2)
