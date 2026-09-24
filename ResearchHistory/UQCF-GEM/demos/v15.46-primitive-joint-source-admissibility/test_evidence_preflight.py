"""Stage-A admission guards; real temporary files, no synthetic native success."""
import copy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


class EvidencePreflightTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('evidence_preflight'),
                             'Stage-A implementation is absent')
        self.p = importlib.import_module('evidence_preflight')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'source.txt').write_bytes(b'actual fixture bytes\n')
        self.pin = {'path':'source.txt', 'git_blob_sha':blob(b'actual fixture bytes\n')}
        self.inventory = {
            'schema':'uqcf-v1546-scoped-input-inventory-v1',
            'scope':'DECLARED_PINNED_SOURCE_REVIEW_NOT_EXHAUSTIVE_ARCHIVE_ABSENCE_PROOF',
            'repository_head':'a'*40,
            'authorship':'AUTHOR_REVIEW_NOT_INDEPENDENT_REVIEW',
            'joint_states_present':True,
            'native_input_status':'NATIVE_JOINT_INPUT_NOT_CERTIFIED_IN_SCOPED_INVENTORY',
            'coupling_status':'SOURCE_OPERATOR_DEFINED_BUT_INCIDENCE_COUPLING_UNSPECIFIED',
            'physical_source_law_adopted':False, 'source_correspondence':'NOT_EVALUATED',
            'Pillar_3':'OPEN',
            'sources':[dict(self.pin,key='fixture',inspection='TEST_FIXTURE',
                            interpretation='Explicitly supplied fixture; not native evidence.')],
        }
        self.packet = {'schema':'uqcf-v1546-source-interface-submissions-v1',
                       'scope':'SUBMITTED_WITNESSES_ONLY_NOT_EXHAUSTIVE_ARCHIVE_SCAN',
                       'submissions':[]}

    def audit(self, packet=None):
        raw=self.p.canonical_bytes(self.inventory)
        return self.p.preflight(self.root,raw,self.p.canonical_bytes(
            self.packet if packet is None else packet),inventory_pin=blob(raw))

    def complete(self,kind='native_claim'):
        return {'record_id':'fixture-R', 'provenance_kind':kind,
                'components':{k:dict(self.pin) for k in self.p.COMPONENTS}}

    def test_real_source_bytes_verified(self):
        result=self.audit()
        self.assertEqual(result['computed']['source_files_verified'],1)
        self.assertEqual(result['computed']['source_receipts'][0]['git_blob_sha'],self.pin['git_blob_sha'])

    def test_missing_source_fails_closed(self):
        (self.root/'source.txt').unlink()
        with self.assertRaisesRegex(ValueError,'missing_source'): self.audit()

    def test_changed_source_fails_closed(self):
        (self.root/'source.txt').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'source_blob_mismatch'): self.audit()

    def test_wrong_inventory_pin_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'inventory_pin_mismatch'):
            self.p.preflight(self.root,self.p.canonical_bytes(self.inventory),
                             self.p.canonical_bytes(self.packet),inventory_pin='0'*40)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate_json_key'):
            self.p.decode(b'{"x":1,"x":2}')

    def test_unknown_inventory_schema_and_fields_rejected(self):
        for key,value in [('schema','unrecognized'),('physical_source_law_adopted',True),('extra',0)]:
            bad=copy.deepcopy(self.inventory);bad[key]=value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.p.verify_sources(self.root,bad)

    def test_duplicate_source_keys_or_paths_rejected(self):
        for mode in ('key','path'):
            bad=copy.deepcopy(self.inventory)
            record=dict(bad['sources'][0])
            if mode=='key': record['path']='different.txt'
            else: record['key']='different'
            bad['sources'].append(record)
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError,'duplicate_source'):
                self.p.verify_sources(self.root,bad)

    def test_unsafe_source_paths_rejected(self):
        for path in ('../outside','/etc/passwd','a/../source.txt','./source.txt','a//b','a\\b',''):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError,'unsafe_path'):
                self.p.read_pin(self.root,dict(self.pin,path=path))

    def test_symlink_source_rejected(self):
        (self.root/'link.txt').symlink_to(self.root/'source.txt')
        with self.assertRaisesRegex(ValueError,'symlink_source'):
            self.p.read_pin(self.root,dict(self.pin,path='link.txt'))

    def test_malformed_hash_rejected(self):
        for sha in ('X'*40,'0'*39,None,True):
            with self.subTest(sha=sha), self.assertRaisesRegex(ValueError,'invalid_pin'):
                self.p.read_pin(self.root,dict(self.pin,git_blob_sha=sha))

    def test_empty_witness_set_is_not_a_zero_source(self):
        result=self.audit()
        self.assertEqual(result['computed']['submitted_records'],0)
        self.assertEqual(result['first_unmet_stage'],'A_NATIVE_INPUT_WITNESS')
        self.assertEqual(result['source_value'],'NOT_EVALUATED')
        self.assertFalse(result['interface_admitted'])
        self.assertEqual(result['later_stages'],'NOT_EXECUTED')

    def test_missing_components_reported_without_promotion(self):
        record={'record_id':'R','provenance_kind':'native_claim','components':{}}
        result=self.p.assess_submission(self.root,record)
        self.assertEqual(result['missing_components'],list(self.p.COMPONENTS))
        self.assertEqual(result['status'],'MISSING_REQUIRED_EVIDENCE')
        self.assertFalse(result['interface_admitted'])

    def test_self_declared_native_with_all_files_is_not_certified(self):
        result=self.p.assess_submission(self.root,self.complete())
        self.assertEqual(result['missing_components'],[])
        self.assertEqual(result['status'],'EVIDENCE_ATTACHED_SEMANTIC_VALIDATION_REQUIRED')
        self.assertFalse(result['native_provenance_certified'])
        self.assertFalse(result['interface_admitted'])

    def test_supplied_and_diagnostic_inputs_remain_distinct(self):
        for kind in ('supplied_hypothesis','diagnostic_fixture'):
            result=self.p.assess_submission(self.root,self.complete(kind))
            self.assertEqual(result['provenance_kind'],kind)
            self.assertFalse(result['native_provenance_certified'])

    def test_coupling_reference_cannot_point_at_changed_bytes(self):
        record=self.complete();record['components']['coupling_law']['git_blob_sha']='0'*40
        with self.assertRaisesRegex(ValueError,'source_blob_mismatch'):
            self.p.assess_submission(self.root,record)

    def test_unknown_component_and_provenance_kind_rejected(self):
        bad=self.complete();bad['components']['curvature_fit']=dict(self.pin)
        with self.assertRaises(ValueError): self.p.assess_submission(self.root,bad)
        bad=self.complete('native_certified')
        with self.assertRaises(ValueError): self.p.assess_submission(self.root,bad)

    def test_no_claim_from_witness_status_flags(self):
        bad=self.complete();bad['native_certified']=True
        with self.assertRaises(ValueError): self.p.assess_submission(self.root,bad)

    def test_duplicate_submission_ids_rejected(self):
        packet=copy.deepcopy(self.packet);packet['submissions']=[self.complete(),self.complete()]
        with self.assertRaisesRegex(ValueError,'duplicate_record_id'): self.audit(packet)

    def test_complete_refs_stop_before_semantic_or_geometry_validation(self):
        packet=copy.deepcopy(self.packet);packet['submissions']=[self.complete()]
        result=self.audit(packet)
        self.assertEqual(result['first_unmet_stage'],'B_OPERATOR_DOMAIN_AND_PROVENANCE')
        self.assertFalse(result['interface_admitted'])
        self.assertEqual(result['claims']['source_correspondence'],'NOT_EVALUATED')
        self.assertEqual(result['claims']['Pillar_3'],'OPEN')

    def test_deterministic_replay_and_review_claim_separation(self):
        first=self.audit();second=self.audit()
        self.assertEqual(self.p.canonical_bytes(first),self.p.canonical_bytes(second))
        self.assertTrue(self.p.canonical_bytes(first).endswith(b'\n'))
        self.assertEqual(first['reviewed_claims']['status'],'AUTHORED_INVENTORY_NOT_MACHINE_PROOF')
        self.assertFalse(first['claims']['physical_source_law_adopted'])
        self.assertFalse(first['claims']['full_v1546_certification'])


if __name__=='__main__': unittest.main()
