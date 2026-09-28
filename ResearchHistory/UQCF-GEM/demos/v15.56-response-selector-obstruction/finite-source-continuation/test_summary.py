"""Reporting tests: incomplete or invalid ensembles cannot look complete."""
import gzip
import importlib.util
import itertools
import json
import pathlib
import tempfile
import unittest

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('summary1603',HERE/'summarize.py')
S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)

class SummaryTests(unittest.TestCase):
    def fixture(self,folder):
        for idx in S.CANDIDATES:
            rows=[]
            for a,pair,arm,precision in itertools.product(S.AS,['overlap','disjoint'],['plane','isotropic'],[50,80]):
                row={'candidate_index':idx,'a':a,'pair':pair,'arm':arm,'precision':precision,'finite':[{'lambda_exponent':e,'orders':{'forward':[{},{}],'reverse':[{},{}]}} for e in [4,5,6,7,8]]}
                if pair=='disjoint':row.update(classification=['null','null'],cubic=[{'norm':'0','ranks':[0,0,0]}]*2)
                rows.append(row)
            r={'version':'16.03','candidate_index':idx,'all_valid':True,'finite_overlap_confirmed':False,'cubic_classes':['null']*4,'rows':rows,'controls':{'precisions':[{'precision':p,'metrics':{}} for p in [50,80]]},'execution_head':'fixture','verdict':'DISJOINT_CUBIC_NUMERICAL_NULL','continuation_verdict':'FINITE_GRID_OVERLAP_RESPONSE_NOT_CONFIRMED'}
            self.write(folder,idx,r)
    def write(self,folder,idx,r):
        (folder/f'result-{idx}.json.gz').write_bytes(gzip.compress(json.dumps(r).encode(),mtime=0))
    def test_valid_scientific_no_and_invalid_override(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);self.fixture(p);r=S.summarize(p)
            self.assertTrue(r['all_valid']);self.assertEqual(r['verdict'],'DISJOINT_CUBIC_NUMERICAL_NULL')
            f=p/'result-13.json.gz';q=json.loads(gzip.decompress(f.read_bytes()));q['all_valid']=False;self.write(p,13,q)
            self.assertEqual(S.summarize(p)['verdict'],'INVALID')
    def test_missing_candidate_and_duplicate_row_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);self.fixture(p);f=p/'result-77.json.gz';saved=f.read_bytes();f.unlink()
            with self.assertRaises(FileNotFoundError):S.summarize(p)
            f.write_bytes(saved);q=json.loads(gzip.decompress(saved));q['rows'][0]=q['rows'][1];self.write(p,77,q)
            with self.assertRaises(AssertionError):S.summarize(p)

if __name__=='__main__':unittest.main()
