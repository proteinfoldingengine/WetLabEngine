"""Reject provenance, merge-binding and ZIP-integrity mutations."""
import unittest,copy,tempfile,io,zipfile
from integrity import PARENT,PREREG,WORKFLOW,sha,unpack_zip
from publish import provenance,validate_merge
class Integrity(unittest.TestCase):
    def setUp(self):
        self.head='a'*40
        self.run={'id':42,'head_sha':self.head,'run_attempt':1,'event':'push','path':WORKFLOW,'head_branch':'research/v16.40-coordinate-obstruction'}
        self.art={'name':'v1640-science-'+self.head,'workflow_run':{'id':42,'head_sha':self.head}}
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
if __name__=='__main__':unittest.main()
