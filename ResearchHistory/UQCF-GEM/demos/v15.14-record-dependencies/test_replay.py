import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import adaptive as m

if importlib.util.find_spec('replay'):
    import replay as r
else:
    r=None

class ReplayTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(r, 'record-aware replay not implemented')

    def test_payload_has_all_80_valid_runs(self):
        p=m.payload()
        self.assertEqual(len(p['branches']),16)
        self.assertEqual(len(p['schedules']),5)
        self.assertTrue(all(len(x)==5 for x in p['branches'].values()))

    def test_realized_records_not_full_script_exported_as_available(self):
        p=m.payload()
        for runs in p['branches'].values():
            for run in runs:
                for f in run['snapshots']:
                    self.assertEqual(set(f['records']),set(f['done']))
                    for e in f['enabled']:
                        self.assertTrue(set(m.READS[e])<=set(f['done']))

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'demo.html'; r.write_html(m.payload(),path)
            t=path.read_text()
            for phrase in ['Playback is not physical time','A1 record required','Supplied records']:
                self.assertIn(phrase,t)
            self.assertNotIn('<script src=',t)
            self.assertNotIn('fetch(',t)

    def test_story_shows_block_before_resolution(self):
        story=r.movie_story('1001')
        self.assertTrue(any(x['blocked_attempt']=='B2' and x['snapshot'].done==('B1',) for x in story))
        self.assertEqual(story[-1]['snapshot'].done,m.EVENTS)
        other=r.movie_story('0000')
        self.assertIn('A1=0',next(row['message'] for row in other if row['snapshot'].event=='B2'))

    def test_fps_guard(self):
        with self.assertRaises(ValueError): r.movie(Path('unused.mp4'),fps=0)

    def test_all_frontier_snapshots_agree_with_model(self):
        p=m.payload()
        for outcome,runs in p['branches'].items():
            for s,t in zip(m.schedules(),runs):
                for f,v in zip(m.run(s,outcome),t['snapshots']):
                    self.assertEqual(v['blocked'],{e:list(m.missing(f,e)) for e in m.EVENTS if e not in f.done and m.missing(f,e)})
                    self.assertAlmostEqual(sum(v['probabilities']),1,places=11)

if __name__=='__main__': unittest.main(verbosity=2)
