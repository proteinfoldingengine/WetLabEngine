import copy,gzip,json,os,pathlib,subprocess,sys,tempfile,unittest
import producer as P
import independent as Q

class Activation(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=P.build(fixture=True)
 def test_fixture_acceptance(self):self.assertTrue(Q.verify(self.data,fixture=True))
 def test_complete_source_universes(self):
  a=list(P.abstract_sources());n=list(P.native_sources());self.assertEqual(len(a),5054);self.assertEqual(len(n),8192)
  self.assertEqual(a,list(Q.abstract_sources()));self.assertEqual(n,list(Q.native_sources()));self.assertEqual(len({json.dumps(s,sort_keys=True) for s in a}),5054)
 def test_chain_eighteen(self):
  r=next(r for r in self.data['records'] if r.get('source',{}).get('name')=='chain');self.assertEqual(len(r['ops']),18);self.assertTrue(r['released']);self.assertEqual(len(r['macros']),4)
 def test_zero_edit_not_escape(self):
  r=next(r for r in self.data['records'] if r.get('source',{}).get('name')=='k2');self.assertEqual(r['ops'],[]);self.assertEqual(len(r['macros']),1);self.assertFalse(r['released']);self.assertEqual(len(r['states']),1)
 def test_forced_cherry(self):
  r=next(r for r in self.data['records'] if r.get('source',{}).get('name')=='cherry');self.assertEqual(len(r['ops']),8);self.assertEqual(r['macros'],[['T',0,4],['V',1,-1]])
 def test_saturated_lock(self):
  r=next(r for r in self.data['records'] if r.get('source',{}).get('name')=='full');self.assertFalse(r['released']);self.assertEqual(r['ops'],[])
 def test_native_closure_classification(self):
  for r in self.data['records']:
   if r['kind']=='native':self.assertEqual(r['released'],len(r['Z'])>len(r['closure']))
 def test_exact_reversal(self):
  for r in self.data['records']:
   if r['kind']=='native':self.assertEqual(r['reverse_states'],r['states'][::-1]);self.assertEqual(r['reverse_ops'],[[x,k,1-b] for x,k,b in r['ops'][::-1]])
 def test_ineligible_anchor(self):
  s=copy.deepcopy(next(P.native_sources()));s['C']=[0,1,2,3];s['a']=[1]*7
  for mod in [P,Q]:
   with self.assertRaises(AssertionError):mod.native_record(s)
 def mutate(self,kind,key,fn):
  d=copy.deepcopy(self.data);r=next(r for r in d['records'] if r['kind']==kind and r.get(key));fn(r)
  with self.assertRaises(AssertionError):Q.verify(d,fixture=True)
 def test_omitted_abstract_graph(self):
  d=copy.deepcopy(self.data);d['records'].pop(0)
  with self.assertRaises(AssertionError):Q.verify(d,fixture=True)
 def test_omitted_reachable_state(self):self.mutate('abstract','states',lambda r:r['states'].pop())
 def test_omitted_valid_edge(self):self.mutate('abstract','edges',lambda r:r['edges'].pop())
 def test_omitted_rejected_candidate(self):
  d=copy.deepcopy(self.data);r=next(r for r in d['records'] if r['kind']=='abstract' and any(not c[-1] for c in r['candidates']));r['candidates'].remove(next(c for c in r['candidates'] if not c[-1]))
  with self.assertRaises(AssertionError):Q.verify(d,fixture=True)
 def test_forged_closure(self):self.mutate('abstract','states',lambda r:r['closure'].append(99))
 def test_forged_surplus(self):self.mutate('abstract','states',lambda r:r.__setitem__('surplus',99))
 def test_repeated_donor(self):self.mutate('native','macros',lambda r:r['macros'].append(r['macros'][0]))
 def test_repeated_receiver(self):
  d=copy.deepcopy(self.data);r=next(r for r in d['records'] if r.get('source',{}).get('name')=='chain');r['macros'][1][2]=r['macros'][0][2]
  with self.assertRaises(AssertionError):Q.verify(d,fixture=True)
 def test_invalid_shared_root(self):self.mutate('native','ops',lambda r:r['ops'][0].__setitem__(1,99))
 def test_missing_compensation(self):self.mutate('native','states',lambda r:r['states'][-1].__setitem__(0,0))
 def test_original_floor_mutation(self):self.mutate('native','floors',lambda r:r['floors'].__setitem__(0,999))
 def test_anchor_mutation(self):self.mutate('native','anchors',lambda r:r['anchors'].__setitem__(0,0))
 def test_premature_vacancy(self):self.mutate('native','states',lambda r:r['states'][0].__setitem__(0,0))
 def test_hidden_mask_omission(self):self.mutate('native','protected_masks',lambda r:r['protected_masks'].pop())
 def test_reverse_label_corruption(self):self.mutate('native','reverse_ops',lambda r:r['reverse_ops'][0].__setitem__(0,99))
 def test_source_profile_omission(self):
  d=copy.deepcopy(self.data);r=next(r for r in d['records'] if r['kind']=='native' and r['source'].get('name')=='full');self.assertEqual(r['source']['a'],[2]*7);d['records'].remove(r)
  with self.assertRaises(AssertionError):Q.verify(d,fixture=True)
 def stream(self,mode):
  d=copy.deepcopy(self.data);rows=d.pop('records')
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'rows.gz'
   if mode!='missing':
    if mode=='truncated':rows=rows[:-1]
    if mode=='extra':rows.append(rows[-1])
    with gzip.open(p,'wt') as f:
     for r in rows:f.write(json.dumps(r)+'\n')
    if mode=='corrupt':p.write_bytes(p.read_bytes()[:-12])
   with self.assertRaises(AssertionError):Q.verify(d,fixture=True,identity_path=p)
 def test_missing_stream(self):self.stream('missing')
 def test_truncated_stream(self):self.stream('truncated')
 def test_extra_stream(self):self.stream('extra')
 def test_corrupt_stream(self):self.stream('corrupt')
 def test_optimized_runtime_rejection(self):
  for mod in ['producer','independent']:
   for flag in ['-O','-OO']:
    r=subprocess.run([sys.executable,flag,'-c','import '+mod],capture_output=True,text=True,cwd=pathlib.Path(__file__).parent);self.assertNotEqual(r.returncode,0);self.assertIn('requires assertions',r.stderr)
if __name__=='__main__':unittest.main()
