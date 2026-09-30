import tempfile,unittest,sys
from pathlib import Path
from core import fixture_cache,replace_directory,run_commands

class Infrastructure(unittest.TestCase):
    def test_fixture_generation_once_and_mutations_isolated(self):
        calls=[]
        def generate(bound):calls.append(bound);return {'nested':[bound]}
        cached=fixture_cache(generate)
        a=cached(3);a['nested'].append('poison')
        self.assertEqual(cached(3),{'nested':[3]})
        self.assertEqual(cached(4),{'nested':[4]})
        self.assertEqual(calls,[3,4])
    def test_publication_replacement_removes_stale_members(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);a=root/'fresh';b=root/'published';a.mkdir();b.mkdir()
            (a/'current').write_text('new');(b/'stale').write_text('old')
            replace_directory(a,b)
            self.assertEqual(sorted(p.name for p in b.iterdir()),['current'])
    def test_failed_command_preserves_peer_result(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);marker=root/'peer-finished'
            with self.assertRaises(RuntimeError):
                run_commands({'bad':[sys.executable,'-c','raise SystemExit(7)'],'peer':[sys.executable,'-c',f'from pathlib import Path;Path({str(marker)!r}).write_text("done")']},root/'logs')
            self.assertTrue(marker.exists(),'peer result must survive another command failure')

if __name__=='__main__':unittest.main(verbosity=2)
