"""Prospective aggregate/reproduction rejection contracts."""
import copy
import sys
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from publication import check_partition,check_required_diagnostics,compare_reproduction
import publication

class Publication(unittest.TestCase):
    def shards(self):
        return [{'shard':i,'shards':8,'start':i*2,'stop':i*2+2,'total':16,'whole_universe_sha256':'a'*64,'identity_sha256':str(i)*64,'scope':'all'} for i in range(8)]

    def test_complete_partition(self):
        self.assertEqual(check_partition(self.shards()),[])

    def test_missing_shard_rejected(self):
        self.assertTrue(check_partition(self.shards()[:-1]))

    def test_duplicate_shard_rejected(self):
        s=self.shards();s[-1]=s[-2]
        self.assertTrue(check_partition(s))

    def test_overlapping_interval_rejected(self):
        s=self.shards();s[3]['start']-=1
        self.assertTrue(check_partition(s))

    def test_mismatched_universe_rejected(self):
        s=self.shards();s[3]['whole_universe_sha256']='b'*64
        self.assertTrue(check_partition(s))

    def test_empty_mechanism_category_rejected(self):
        self.assertTrue(check_required_diagnostics({}))

    def test_equal_scientific_reproduction(self):
        self.assertEqual(compare_reproduction({'a':'a'*64},{'a':'a'*64}),[])

    def test_scientific_byte_change_rejected(self):
        self.assertTrue(compare_reproduction({'a':'a'*64},{'a':'b'*64}))

    def test_missing_reproduction_file_rejected(self):
        self.assertTrue(compare_reproduction({'a':'a'*64},{}))

    def test_target_workflow_attempt_binding(self):
        check=getattr(publication,'check_run_binding',None)
        self.assertIsNotNone(check,'target workflow binding is required')
        good={'head_sha':'a'*40,'status':'completed','conclusion':'success','run_attempt':2,'id':19,'event':'push','path':'.github/workflows/v16.54-mechanism-validation.yml'}
        self.assertEqual(check(good,19,2,'a'*40),[])
        for key,value in [('path','another.yml'),('event','pull_request'),('run_attempt',1),('id',20)]:
            with self.subTest(key=key):
                self.assertTrue(check({**good,key:value},19,2,'a'*40))

    def test_executing_helpers_must_match_target(self):
        check=getattr(publication,'check_helper_binding',None)
        self.assertIsNotNone(check,'executing helpers must be bound')
        expected={'verifier.py':'a'*64,'campaign.py':'b'*64}
        self.assertEqual(check(expected,expected),[])
        self.assertTrue(check(expected,{'verifier.py':'c'*64,'campaign.py':'b'*64}))
        self.assertTrue(check(expected,{'verifier.py':'a'*64}))

    def test_inherited_package_uses_full_verifier(self):
        check=getattr(publication,'verify_inherited_package',None)
        self.assertIsNotNone(check,'full inherited package verification is required')
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);(p/'SOURCE_MANIFEST.json').write_text('{}')
            with self.assertRaises(ValueError):check(p,'a'*40)

    def test_unavailable_evidence_preserves_incomplete(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict('os.environ',{'GITHUB_ACTIONS':'true'}),patch.object(publication,'api',side_effect=OSError('evidence unavailable')):
                with self.assertRaises(Exception):publication.aggregate(19,1,'a'*40,directory)
            status=Path(directory)/'STATUS.json'
            self.assertTrue(status.exists(),'missing durable INCOMPLETE status')
            result=json.loads(status.read_text())
            self.assertEqual(result['status'],'INCOMPLETE')
            self.assertTrue(result['phase'])
            self.assertTrue(result['reason'])

    def test_actual_merge_requires_two_parents(self):
        check=getattr(publication,'check_merge_sources',None)
        self.assertIsNotNone(check,'actual merge needs source verification')
        source={'verifier.py':'a'*64,'protocol.json':'b'*64}
        self.assertEqual(check(['a'*40,'b'*40],source,source),[])
        self.assertTrue(check(['a'*40],source,source))

    def test_actual_merge_rejects_changed_or_missing_science(self):
        check=getattr(publication,'check_merge_sources',None)
        self.assertIsNotNone(check,'actual merge needs source verification')
        source={'verifier.py':'a'*64,'protocol.json':'b'*64}
        self.assertTrue(check(['a'*40,'b'*40],source,{'verifier.py':'c'*64,'protocol.json':'b'*64}))
        self.assertTrue(check(['a'*40,'b'*40],source,{'verifier.py':'a'*64}))

    def test_original_archive_parts_reconstruct_exact_bytes(self):
        import hashlib
        pack=getattr(publication,'archive_parts',None)
        self.assertIsNotNone(pack,'large original archives need exact-byte publication')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'original.zip';data=b'original archive bytes'*9;source.write_bytes(data)
            manifest=pack(source,root/'parts',hashlib.sha256(data).hexdigest(),chunk_bytes=31)
            rebuilt=b''.join((root/'parts'/row['name']).read_bytes() for row in manifest['parts'])
            self.assertEqual(rebuilt,data)
            self.assertEqual(manifest['archive_sha256'],hashlib.sha256(data).hexdigest())
            self.assertTrue(all(row['bytes']<=31 for row in manifest['parts']))

    def test_corrupt_original_archive_is_not_published(self):
        pack=getattr(publication,'archive_parts',None)
        self.assertIsNotNone(pack,'large original archives need exact-byte publication')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'original.zip';source.write_bytes(b'corrupt')
            with self.assertRaises(ValueError):pack(source,root/'parts','a'*64,chunk_bytes=31)

    def test_archive_destination_rejects_noninteger_run_before_writing(self):
        import preserve
        check=getattr(preserve,'validated_campaign',None)
        self.assertIsNotNone(check,'campaign destination must be validated before writes')
        good={'status':'PASS','run':19,'attempt':1,'scientific_sha':'a'*40,'workflow_sha':'a'*40}
        status={**good};run={'id':19,'run_attempt':1,'head_sha':'a'*40,'status':'completed','conclusion':'success'}
        self.assertEqual(check(good,status,run,{'target_head':'a'*40}),(19,1,'a'*40))
        for key,value in [('run','../../escape'),('run',True),('attempt',0),('scientific_sha','not-a-sha')]:
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):check({**good,key:value},status,run,{'target_head':'a'*40})

    def test_archive_campaign_cross_bindings_reject_substitution(self):
        import preserve
        check=getattr(preserve,'validated_campaign',None)
        self.assertIsNotNone(check,'campaign identities must agree across retained records')
        good={'status':'PASS','run':19,'attempt':1,'scientific_sha':'a'*40,'workflow_sha':'a'*40}
        run={'id':19,'run_attempt':1,'head_sha':'a'*40,'status':'completed','conclusion':'success'}
        for status,meta,prov in [({**good,'run':20},run,{'target_head':'a'*40}),(good,{**run,'run_attempt':2},{'target_head':'a'*40}),(good,run,{'target_head':'b'*40})]:
            with self.assertRaises(ValueError):check(good,status,meta,prov)

    def test_reproduction_rejects_equal_nonmanifest_values(self):
        self.assertTrue(compare_reproduction(['a'],['a']))
        self.assertTrue(compare_reproduction('same','same'))

    def test_explicit_null_comparison_rejected_before_evidence_access(self):
        import preserve
        with tempfile.TemporaryDirectory() as directory:
            request={'aggregate_run':19,'aggregate_attempt':1,'aggregate_head':'a'*40,'compare_to':None}
            with patch.dict('os.environ',{'GITHUB_ACTIONS':'true'}),patch.object(preserve,'api',side_effect=AssertionError('evidence accessed before request validation')):
                with self.assertRaisesRegex(ValueError,'invalid reproduction reference'):preserve.prepare(request,Path(directory)/'out')
