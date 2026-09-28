import copy,gzip,importlib.util,json,pathlib,subprocess,sys,tempfile,unittest
HERE=pathlib.Path(__file__).resolve().parent
class SummaryTests(unittest.TestCase):
    def need(self):
        self.assertTrue((HERE/'summarize.py').exists(),'16.04 reporter absent: expected RED')
        s=importlib.util.spec_from_file_location('summary1604',HERE/'summarize.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
    def fixture(self,g):
        # Literal shape has 12 candidates, 12 configurations each, two frames.
        shards=[]
        for n in [13,16,22,25,27,29,37,39,46,50,66,77]:
            rows=[]
            for d in [50,80]:
                for a in [1.,1/3,1/6]:
                    for arm in ['plane','isotropic']:
                        frames=[]
                        for f in [0,1]:
                            rec={'frame':f,'classifications':{'T_D':'null','T_A':'null','T':'null'},'cancellation_ratio':None,'direction_norms':{},'edges':[]}
                            for k in ['T_D','T_A','T']:rec[k]={'matrix':[['0']*81 for _ in range(3)],'norm':'0','ranks':[0,0,0],'singular_values':['0','0','0']}
                            frames.append(rec)
                        rows.append({'candidate_index':n,'precision':d,'a':a,'arm':arm,'frames':frames,'blocks':{}})
            controls=[{'precision':d,'all_valid':True,'ranks_and_classes_agree':True,'metrics':{k:'0' for k in g.METRICS},'limits':{k:('1e-30' if k=='precision' else '1e-35') for k in g.METRICS},'laws':{'valid':True},'isotropic_laws':{'valid':True}} for d in [50,80]]
            shards.append({'version':'16.04','candidate_index':n,'execution_head':g.HEAD,'all_valid':True,'verdict':'FACTORIZATION_CONFIRMED','factorization_confirmed':True,'rows':rows,'controls':controls})
        return shards
    def test_missing_candidate_or_duplicate_configuration_rejected(self):
        g=self.need();s=self.fixture(g)
        with self.assertRaises(ValueError):g.summarize(s[:-1])
        s[0]['rows'][-1]=copy.deepcopy(s[0]['rows'][0])
        with self.assertRaises(ValueError):g.summarize(s)
    def test_null_is_valid_but_control_failure_overrides(self):
        g=self.need();s=self.fixture(g)
        self.assertEqual(g.summarize(s)['verdict'],'FACTORIZATION_CONFIRMED')
        s[0]['controls'][0]['metrics']['parent_coefficient']='1e-10'
        self.assertEqual(g.summarize(s)['verdict'],'INVALID')
    def test_cli_invalid_result_returns_failure(self):
        g=self.need();shards=self.fixture(g);shards[0]['all_valid']=False
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)
            for s in shards:(p/f"result-{s['candidate_index']}.json.gz").write_bytes(gzip.compress(json.dumps(s).encode()))
            r=subprocess.run([sys.executable,str(HERE/'summarize.py'),str(p),'--output',str(p/'summary.json')],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
            self.assertEqual(json.loads((p/'summary.json').read_text())['verdict'],'INVALID')
    def test_rank_metadata_and_frame_disagreement_rejected(self):
        g=self.need();s=self.fixture(g)
        s[0]['rows'][0]['frames'][0]['T']['ranks']=[999,-1,0]
        with self.assertRaises(ValueError):g.summarize(s)
        s=self.fixture(g);f=s[0]['rows'][0]['frames'][0]
        f['T']['matrix'][0][0]='1';f['T']['norm']='1';f['T']['singular_values']=['1','0','0'];f['T']['ranks']=[1,1,1];f['classifications']['T']='active'
        with self.assertRaises(ValueError):g.summarize(s)
    def test_wrong_head_and_nonfinite_rejected(self):
        g=self.need();s=self.fixture(g);s[0]['execution_head']='wrong'
        with self.assertRaises(ValueError):g.summarize(s)
        s=self.fixture(g);s[0]['rows'][0]['frames'][0]['T']['matrix'][0][0]='NaN'
        with self.assertRaises(ValueError):g.summarize(s)
if __name__=='__main__':unittest.main()
