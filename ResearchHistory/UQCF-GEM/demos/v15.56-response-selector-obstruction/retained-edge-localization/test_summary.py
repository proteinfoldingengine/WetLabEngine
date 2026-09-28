import copy,gzip,importlib.util,json,pathlib,subprocess,sys,tempfile,unittest
HERE=pathlib.Path(__file__).resolve().parent
class SummaryTests(unittest.TestCase):
 def need(self):
  self.assertTrue((HERE/'summarize.py').exists(),'16.05 reporter absent: expected RED')
  s=importlib.util.spec_from_file_location('summary1605',HERE/'summarize.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);return g
 def fixture(self,g):
  shards=[]
  for n in g.CANDIDATES:
   exact={arm:{'retained_zero':True,'omitted_zero':True,'edge_zero':[True]*6,'identity_middle_zero':True,'direction_polynomials':[[['0']*3 for _ in range(3)] for _ in range(6)]} for arm in ['plane','isotropic']}
   rows=[]
   for d in [50,80]:
    for a in [1.,1/3,1/6]:
     for arm in ['plane','isotropic']:
      frames=[{'frame':f,'directions':[[['0']*3 for _ in range(3)] for _ in range(6)],'norms':{'edges':['0']*6,'retained':'0','omitted':'0','complete':'0'},'T_D':{'matrix':[['0']*81 for _ in range(3)],'norm':'0','singular_values':['0']*3,'ranks':[0,0,0]},'classification':'null','localization':'RETAINED_EDGE_NULL'} for f in [0,1]]
      rows.append({'candidate_index':n,'a':a,'arm':arm,'precision':d,'frames':frames})
   controls=[{'precision':d,'all_valid':True,'ranks_and_localizations_agree':True,'metrics':{k:'0' for k in g.METRICS},'limits':{k:('1e-30' if k=='precision' else '1e-35') for k in g.METRICS},'laws':{'valid':True},'isotropic_laws':{'valid':True}} for d in [50,80]]
   shards.append({'version':'16.05','candidate_index':n,'execution_head':g.HEAD,'all_valid':True,'verdict':'EXACT_RETAINED_EDGE_LOCALIZATION_CONFIRMED','rows':rows,'controls':controls,'exact':exact,'support_certificate':{'basis_word_count':112,'confirmed':True,'failures':[],'exact_transfer_reconstruction':True},'excluded_state_coefficients':[],'excluded_sector_commutator_zero':True,'excluded_sector_commutator':[]})
  return shards
 def test_support_and_excluded_metadata_checked(self):
  g=self.need()
  shards=self.fixture(g)
  shards[0]['support_certificate']['basis_word_count']=0
  self.assertFalse(g.summarize(shards)['all_valid'])
  shards=self.fixture(g)
  shards[0]['support_certificate']['exact_transfer_reconstruction']=False
  self.assertFalse(g.summarize(shards)['all_valid'])
  shards=self.fixture(g)
  shards[0]['excluded_sector_commutator']=[[[0,0,1,1],'a-a**2']]
  with self.assertRaises(ValueError):g.summarize(shards)

 def test_complete_null_and_invalid_precedence(self):
  g=self.need();s=self.fixture(g);self.assertTrue(g.summarize(s)['all_valid'])
  s[0]['controls'][0]['metrics']['exact_direction']='1e-10'
  self.assertEqual(g.summarize(s)['verdict'],'INVALID')
 def test_incomplete_duplicate_and_wrong_head_rejected(self):
  g=self.need();s=self.fixture(g)
  with self.assertRaises(ValueError):g.summarize(s[:-1])
  s[0]['rows'][-1]=copy.deepcopy(s[0]['rows'][0])
  with self.assertRaises(ValueError):g.summarize(s)
  s=self.fixture(g);s[0]['execution_head']='wrong'
  with self.assertRaises(ValueError):g.summarize(s)
 def test_exact_nonzero_cannot_be_reported_zero(self):
  g=self.need();s=self.fixture(g);s[0]['exact']['plane']['direction_polynomials'][0][0][0]='a/2**80'
  with self.assertRaises(ValueError):g.summarize(s)
 def test_direction_norm_and_rank_metadata_checked(self):
  g=self.need();s=self.fixture(g);s[0]['rows'][0]['frames'][0]['directions'][0][0][0]='1'
  with self.assertRaises(ValueError):g.summarize(s)
  s=self.fixture(g);s[0]['rows'][0]['frames'][0]['T_D']['ranks']=[999,0,0]
  with self.assertRaises(ValueError):g.summarize(s)
 def test_cli_invalid_returns_failure(self):
  g=self.need();s=self.fixture(g);s[0]['all_valid']=False
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)
   for r in s:(p/f"result-{r['candidate_index']}.json.gz").write_bytes(gzip.compress(json.dumps(r).encode()))
   r=subprocess.run([sys.executable,str(HERE/'summarize.py'),str(p),'--output',str(p/'SUMMARY.json')],capture_output=True,text=True)
   self.assertEqual(r.returncode,2);self.assertEqual(json.loads((p/'SUMMARY.json').read_text())['verdict'],'INVALID')
if __name__=='__main__':unittest.main()
