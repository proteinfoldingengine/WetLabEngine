import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
import simulation
if importlib.util.find_spec('render') is not None:
    import render
else:
    render=None
SCENARIO=json.loads((Path(__file__).parent/'scenario.json').read_text())
class PresentationTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(render,'presentation/export layer not implemented')
    def test_export_uses_computed_quantum_states(self):
        t=simulation.build_demo(SCENARIO,cadence=2); view=render.export_view(t)
        self.assertEqual(len(view['frames']),len(t.frames))
        for source,dst in zip(t.frames,view['frames']):
            self.assertAlmostEqual(sum(dst['probabilities']),1,places=7)
            self.assertEqual(dst['record'],source.record)
            self.assertEqual(dst['ordinal'],source.ordinal)
            self.assertAlmostEqual(dst['coherence'][1],abs(source.rho[0,2]),places=7)
    def test_eight_alternative_scenarios_are_explicit(self):
        b=render.make_bundle(SCENARIO,cadence=2)
        self.assertEqual(set(b['branches']),{f'{i:03b}' for i in range(8)})
        self.assertEqual(b['initial_branch'],'101')
    def test_html_is_self_contained(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'demo.html'; render.write_html(render.make_bundle(SCENARIO,2),p)
            s=p.read_text()
            self.assertIn('Playback is not physical time',s)
            self.assertIn('Supplied actual records',s)
            self.assertNotIn('<script src=',s)
            self.assertNotIn('fetch(',s)
    def test_phase_jumps_address_existing_frames(self):
        b=render.make_bundle(SCENARIO,2)
        for branch in b['branches'].values():
            for phase,idx in branch['phase_starts'].items():
                self.assertEqual(branch['frames'][idx]['phase'],phase)
    def test_export_does_not_recompute_collapse(self):
        t=simulation.build_demo(SCENARIO,2)
        self.assertEqual(render.export_view(t)['summary']['events'],t.events)
    def test_invalid_video_fps_is_rejected(self):
        with self.assertRaises(ValueError):
            render.render_movie(simulation.build_demo(SCENARIO,2),Path('unused.mp4'),fps=0)
if __name__=='__main__': unittest.main(verbosity=2)
