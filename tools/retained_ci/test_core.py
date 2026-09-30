import tempfile,unittest,sys
from pathlib import Path
from core import fixture_cache,replace_directory,run_commands,write_manifest,verify_manifest,compare_suites,unpack_zip,sha,anchored_file
import copy,io,zipfile
from publish import provenance,validate_merge
from core import PARENT
import subprocess

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

    def test_failed_generation_is_not_cached(self):
        calls=[]
        def generate(bound):
            calls.append(bound)
            if len(calls)==1:raise ValueError('generation failed')
            return {'bound':bound}
        fresh=fixture_cache(generate)
        with self.assertRaises(ValueError):fresh(3)
        self.assertEqual(fresh(3),{'bound':3})
    def test_missing_replacement_preserves_existing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);target=root/'existing';target.mkdir();(target/'kept').write_text('x')
            with self.assertRaises(ValueError):replace_directory(root/'absent',target)
            self.assertTrue((target/'kept').exists())
    def test_manifest_rejects_changed_extra_and_missing_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/'data';p.write_text('good');write_manifest(root);verify_manifest(root)
            p.write_text('bad')
            with self.assertRaises(ValueError):verify_manifest(root)
            p.write_text('good');(root/'extra').write_text('x')
            with self.assertRaises(ValueError):verify_manifest(root)
            (root/'extra').unlink();p.unlink()
            with self.assertRaises(ValueError):verify_manifest(root)
    def test_comparison_rejects_substituted_test_fixture_and_verifier(self):
        good={'success':True,'tests':[{'id':'case','outcome':'success'}],'fixture_hashes':{'3':'abc'},'verifier_calls':1,'verifier_uncached':True}
        compare_suites(good,copy.deepcopy(good))
        for key,value in [('tests',[{'id':'other','outcome':'success'}]),('fixture_hashes',{'3':'wrong'}),('verifier_calls',0),('verifier_uncached',False),('success',False)]:
            bad=copy.deepcopy(good);bad[key]=value
            with self.assertRaises(ValueError):compare_suites(good,bad)
    def test_artifact_rejects_digest_mismatch_and_path_escape(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:z.writestr('../escape','bad')
        raw=data.getvalue()
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):unpack_zip(raw,'sha256:wrong',td)
            with self.assertRaises(ValueError):unpack_zip(raw,'sha256:'+sha(raw),td)
    def test_provenance_rejects_wrong_run_head_attempt_and_phase(self):
        run={'id':7,'head_sha':'abc','run_attempt':2}
        artifact={'name':'retained-ci-science-abc','workflow_run':{'id':7,'head_sha':'abc'}}
        meta={'head':'abc','trigger_sha':'abc','workflow_sha':'abc','run_id':'7','run_attempt':'2','phase':'science'}
        provenance(run,artifact,meta,'abc',7,2,'science')
        for key in meta:
            bad=dict(meta);bad[key]='bad'
            with self.assertRaises(ValueError):provenance(run,artifact,bad,'abc',7,2,'science')
        for key,value in [('id',8),('head_sha','bad'),('run_attempt',1)]:
            bad=dict(run);bad[key]=value
            with self.assertRaises(ValueError):provenance(bad,artifact,meta,'abc',7,2,'science')

    def test_parent_anchor_rejects_coordinated_checkout_change(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/'reference.json';p.write_text('original')
            def git(*args):return subprocess.check_output(['git','-C',td,*args],stderr=subprocess.DEVNULL,text=True).strip()
            git('init');git('add','reference.json');git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','parent')
            parent=git('rev-parse','HEAD');self.assertEqual(anchored_file(root,parent,'reference.json'),b'original')
            p.write_text('changed');git('add','reference.json');git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','coordinated change')
            with self.assertRaises(ValueError):anchored_file(root,parent,'reference.json')
    def test_receipt_rejects_direct_push_and_wrong_merge_identity(self):
        run={'head_sha':'merge','event':'push','head_branch':'research/v16.34-fiber-component-invariant','path':'.github/workflows/retained-ci-optimization.yml'}
        pr={'merged':True,'merge_commit_sha':'merge','base':{'ref':'research/v16.34-fiber-component-invariant'},'head':{'sha':'pub'}}
        commit={'sha':'merge','parents':[{'sha':PARENT},{'sha':'pub'}],'tree':{'sha':'tree'}}
        publication={'sha':'pub','tree':{'sha':'tree'}}
        validate_merge(run,pr,commit,publication,'merge')
        for part,key,value in [(0,'event','workflow_dispatch'),(0,'path','wrong.yml'),(0,'head_branch','other'),(1,'merged',False),(1,'merge_commit_sha','other'),(2,'parents',[{'sha':PARENT}]),(3,'tree',{'sha':'changed'})]:
            args=copy.deepcopy([run,pr,commit,publication]);args[part][key]=value
            with self.assertRaises(ValueError):validate_merge(*args,'merge')

if __name__=='__main__':unittest.main(verbosity=2)
