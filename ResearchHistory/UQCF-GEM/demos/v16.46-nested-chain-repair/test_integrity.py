"""Reject provenance, merge-binding and ZIP-integrity mutations."""
import unittest,copy,tempfile,io,zipfile,json
from pathlib import Path
import archive,snapshot,tarfile,gzip
from integrity import PARENT,PREREG,WORKFLOW,sha,unpack_zip,validate_summary
from publish import provenance,validate_merge
class Integrity(unittest.TestCase):
    def setUp(self):
        self.head='a'*40
        self.run={'id':42,'head_sha':self.head,'run_attempt':1,'event':'push','path':WORKFLOW,'head_branch':'research/v16.46-nested-chain-repair'}
        self.art={'name':'v1646-science-'+self.head,'workflow_run':{'id':42,'head_sha':self.head}}
        self.meta={'head':self.head,'trigger_sha':self.head,'workflow_sha':self.head,'run_id':'42','run_attempt':'1','phase':'science','verified_parent':PARENT,'preregistration':PREREG}
    def check(self):provenance(self.run,self.art,self.meta,self.head,42,1,'science')
    def reject(self):
        with self.assertRaises(ValueError):self.check()
    def test_positive(self):self.check()
    def test_wrong_head(self):self.run['head_sha']='b'*40;self.reject()
    def test_wrong_attempt(self):self.run['run_attempt']=2;self.reject()
    def test_wrong_workflow(self):self.run['path']='other.yml';self.reject()
    def test_wrong_branch(self):self.run['head_branch']='main';self.reject()
    def test_wrong_artifact(self):self.art['workflow_run']['id']=43;self.reject()
    def test_wrong_embedded_sha(self):self.meta['workflow_sha']='b'*40;self.reject()
    def test_wrong_parent(self):self.meta['verified_parent']='b'*40;self.reject()
    def test_wrong_prereg(self):self.meta['preregistration']='b'*40;self.reject()
    def merge_objects(self):
        run=dict(self.run,head_branch='research/v16.34-fiber-component-invariant')
        pr={'merged':True,'merge_commit_sha':self.head,'base':{'ref':'research/v16.34-fiber-component-invariant'},'head':{'sha':'b'*40}}
        commit={'sha':self.head,'parents':[{'sha':PARENT},{'sha':'b'*40}],'tree':{'sha':'c'*40}}
        pub={'sha':'b'*40,'tree':{'sha':'c'*40}}
        return run,pr,commit,pub
    def test_merge_positive(self):validate_merge(*self.merge_objects(),self.head)
    def test_merge_parent(self):
        r,p,c,u=self.merge_objects();c['parents'][0]['sha']='d'*40
        with self.assertRaises(ValueError):validate_merge(r,p,c,u,self.head)
    def test_merge_tree(self):
        r,p,c,u=self.merge_objects();u['tree']['sha']='d'*40
        with self.assertRaises(ValueError):validate_merge(r,p,c,u,self.head)
    def test_zip_digest(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:z.writestr('a','x')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):unpack_zip(b.getvalue(),'sha256:wrong',d)
    def test_zip_traversal(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:z.writestr('../a','x')
        data=b.getvalue()
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):unpack_zip(data,'sha256:'+sha(data),d)
    def archive_case(self,mutation=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'artifact.zip';p.write_bytes(b'0123456789');folder=archive.retain(p,4)
            if mutation:mutation(folder)
            return archive.verify(folder,'sha256:'+sha(b'0123456789'))
    def test_archive_positive(self):self.assertEqual(self.archive_case(),b'0123456789')
    def test_archive_omission(self):
        with self.assertRaises(ValueError):self.archive_case(lambda p:(p/'00001.part').unlink())
    def test_archive_substitution(self):
        with self.assertRaises(ValueError):self.archive_case(lambda p:(p/'00000.part').write_bytes(b'abcd'))
    def test_archive_reordering(self):
        def mutate(p):
            f=p/'ARCHIVE.json';r=json.loads(f.read_text());r['chunks'].reverse();f.write_text(json.dumps(r))
        with self.assertRaises(ValueError):self.archive_case(mutate)
    def test_archive_extracted_binding(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:z.writestr('certificate','original')
        data=stream.getvalue();digest='sha256:'+sha(data)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'certificate';p.write_text('original');archive.verify_extracted(data,d,digest)
            p.write_text('substituted')
            with self.assertRaises(ValueError):archive.verify_extracted(data,d,digest)
    def test_publication_provenance(self):
        self.art['name']='v1646-publication-'+self.head;self.meta['phase']='publication'
        provenance(self.run,self.art,self.meta,self.head,42,1,'publication')
    def test_publication_wrong_head(self):
        self.art['name']='v1646-publication-'+self.head;self.meta['phase']='publication';self.meta['head']='b'*40
        with self.assertRaises(ValueError):provenance(self.run,self.art,self.meta,self.head,42,1,'publication')
    def source_case(self,mutation=None):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'a').write_bytes(b'same');(root/'b').write_bytes(b'same');expected={'a':sha(b'same'),'b':sha(b'same')};mapping=dict(expected);fmt=dict(snapshot.FORMAT);p=root/'SOURCE.tar.gz';snapshot.write(root,expected,p)
            with tarfile.open(p) as tf:rows=[(m.name,tf.extractfile(m).read()) for m in tf.getmembers()]
            if mutation:
                mutation(rows,mapping,fmt)
                with tarfile.open(p,'w:gz') as tf:
                    for name,data in rows:
                        info=tarfile.TarInfo(name);info.size=len(data);tf.addfile(info,io.BytesIO(data))
            result=snapshot.verify(p,mapping,expected,fmt)
            return rows,result
    def test_snapshot_positive_dedup(self):
        rows,result=self.source_case();self.assertEqual(len(rows),1);self.assertEqual(result,{'a':b'same','b':b'same'})
    def test_snapshot_missing_object(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:r.clear())
    def test_snapshot_extra_object(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:r.append(('objects/'+sha(b'extra'),b'extra')))
    def test_snapshot_duplicate_object(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:r.append(r[0]))
    def test_snapshot_substitution(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:r.__setitem__(0,(r[0][0],b'wrong')))
    def test_snapshot_missing_mapping(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:m.pop('b'))
    def test_snapshot_renamed_mapping(self):
        def mutate(r,m,f):m['other']=m.pop('b')
        with self.assertRaises(ValueError):self.source_case(mutate)
    def test_snapshot_wrong_format(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:f.update(schema=2))
    def test_snapshot_extra_mapping(self):
        with self.assertRaises(ValueError):self.source_case(lambda r,m,f:m.update(other=m['a']))
    def test_snapshot_duplicate_mapping_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'mapping.json';p.write_text('{"a":"x","a":"x"}')
            with self.assertRaises(ValueError):snapshot.read_json(p)
    def test_summary_false_universal_claim(self):
        result={'outcome':'NON_SATURATED_CHAIN_LEMMA_VALIDATED'}
        report={'finite_result':result,'preregistered_outcome':result['outcome'],'general_claim':'Universal unit barriers proved'}
        with self.assertRaises(ValueError):validate_summary(report,result)
    def test_summary_wrong_outcome(self):
        result={'outcome':'CONSTRUCTION_REFUTED'}
        report={'finite_result':result,'preregistered_outcome':'NON_SATURATED_CHAIN_LEMMA_VALIDATED','general_claim':'See independently reviewed THEOREM.md; finite results do not establish the universal unit-barrier claim.'}
        with self.assertRaises(ValueError):validate_summary(report,result)
if __name__=='__main__':unittest.main()
