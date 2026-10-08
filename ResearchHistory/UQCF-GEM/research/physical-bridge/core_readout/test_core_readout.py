import copy,importlib.util,json,pathlib,subprocess,sys,unittest
P=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 def setUp(self):
  f=P/'independent.py';self.assertTrue(f.exists(),'Expected RED: independent checker absent')
  s=importlib.util.spec_from_file_location('independent',f);self.v=importlib.util.module_from_spec(s);s.loader.exec_module(self.v)
 def report(self):return self.v.loads(subprocess.check_output([sys.executable,str(P/'producer.py')],text=True,timeout=30))
 def test_complete_identity(self):
  r=self.v.verify(self.report());self.assertEqual((r['states'],r['outcomes'],r['service_outcomes']),(14,110,6))
 def test_missing_duplicate_substitution(self):
  for field in ('states','outcomes','service'):
   for mode in ('missing','duplicate','substitute'):
    r=self.report()
    if mode=='missing':r[field].pop()
    elif mode=='duplicate':r[field].append(copy.deepcopy(r[field][0]))
    else:r[field][-1]=copy.deepcopy(r[field][0])
    with self.subTest(field=field,mode=mode),self.assertRaises(self.v.Error):self.v.verify(r)
 def test_corrupted_tau_type_and_guard(self):
  for val in (True,9):
   r=self.report();r['states'][0]['tau']=val
   with self.assertRaises(self.v.Error):self.v.verify(r)
  for edge in (['11000','+e4','11001'],['00000','-a1','00100']):
   r=self.report();r['outcomes'].append(edge)
   with self.assertRaises(self.v.Error):self.v.verify(r)
 def test_certificate_fibers(self):
  r=self.report()
  for obs,worlds in r['fibers'].items():
   if obs[:2]=='11':self.assertEqual({s[:2] for s in worlds},{'11'})
   if obs[2]=='1':self.assertNotIn('11',{s[:2] for s in worlds})
  self.assertEqual({s[:2] for s in r['fibers']['000']},{'00','01','10','11'})
 def test_paths_and_delayed_service(self):
  r=self.report();edges={tuple(e) for e in r['outcomes']}
  for path in r['restorations'].values():
   self.assertEqual(path[-1][-3:],'000')
   for a,b in zip(path,path[1:]):self.assertTrue(any(e[0]==a and e[2]==b for e in edges))
  for a,c,b in r['service']:self.assertEqual(a[-3:],b[-3:]);self.assertEqual(a[0],b[0])
  for key in ('restorations','certificates','fibers','controls'):
   bad=copy.deepcopy(r);bad[key]={}
   with self.assertRaises(self.v.Error):self.v.verify(bad)
 def test_false_claims_and_provenance(self):
  for key in ('tau_observed','uniformly_safe_attempts','guaranteed_completion','immediate_payload_decode','physical_origin_derived'):
   r=self.report();r['claims'][key]=True
   with self.assertRaises(self.v.Error):self.v.verify(r)
  r=self.report();r['proof_commit']='0'*40
  with self.assertRaises(self.v.Error):self.v.verify(r)
 def test_independent_without_producer_and_duplicate_json(self):
  self.assertEqual(len(self.v.reconstruct()['states']),14)
  with self.assertRaises(self.v.Error):self.v.loads('{"x":1,"x":2}')
if __name__=='__main__':unittest.main(verbosity=2)
