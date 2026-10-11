"""Frozen-scope scientific contracts written before either implementation."""
import copy,gzip,json,pathlib,subprocess,sys,tempfile,unittest
import producer
import independent

class EscapeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=producer.build(fixture=True)
 def record(self,d,name='star'):return next(r for r in d['records'] if r['source'].get('name')==name)
 def mutate(self,fn):
  d=copy.deepcopy(self.data);fn(d)
  with self.assertRaises((AssertionError,ValueError)):independent.verify(d,fixture=True)
 def test_missing_implementation_contract(self):self.assertTrue(independent.verify(self.data,fixture=True))
 def test_complete_source_family(self):
  s=producer.sources();self.assertEqual(len(s),7360);self.assertEqual(len(set(map(lambda x:json.dumps(x,sort_keys=True),s))),7360)
  self.assertEqual({f:sum(x['family']==f for x in s) for f in {x['family'] for x in s}}, {'K4':1024,'C5':1024,'K5':288,'K6-minus45':576,'K5-minus34':224,'K4-leaf':4096,'K23-K2':128})
 def test_cover_pinned_static_unreachable(self):
  r=self.record(self.data,'pinned');self.assertFalse(r['escape']);self.assertTrue(r['cover_lock'])
  self.assertTrue(independent.validate_counts(r['source'],[1,2,2,1,0,0]));self.assertEqual(sum(r['source']['a'])-6,1)
 def test_duplicate_unpins(self):self.assertIn(0,self.record(self.data,'duplicate')['V'])
 def test_saturated_k2_has_no_outside_extension(self):
  r=self.record(self.data,'k2');self.assertFalse(r['escape']);self.assertFalse(r['cover_lock'])
  self.assertTrue(independent.validate_counts(r['source'],[3,3,1,1,1,2,2]))
 def test_nonminimum_upper_four_cover(self):self.assertIn([1,2,3,4],self.record(self.data,'nonminimum')['B'][0]);self.assertIn(0,self.record(self.data,'nonminimum')['V'])
 def test_leaf_and_equal_star_domain(self):
  self.assertTrue(self.record(self.data,'leaf_empty')['escape']);self.assertTrue(independent.validate_source(self.record(self.data,'k2')['source']))
 def test_actual_label_choices(self):
  r=self.record(self.data,'duplicate');vs=[c[0] for c in r['vacancies']];self.assertEqual(vs,list(range(sum(r['source']['a']))))
 def test_all_direct_candidates(self):
  r=self.record(self.data);s=r['source'];total=sum(a*((2**sum(v in e for e in s['H']))-1)*(len(s['H'])-sum(v in e for e in s['H'])) for v,a in enumerate(s['a']))
  self.assertEqual(len(r['candidates']),total);self.assertTrue(any(not c[-1] for c in r['candidates']))
 def test_first_event_routes(self):
  r=self.record(self.data);self.assertTrue(r['routes']);self.assertTrue(all(z['kind']=='X' for z in r['routes']))
 def test_original_hidden_masks(self):self.assertTrue(self.record(self.data)['protected_masks']);self.assertTrue(independent.verify(self.data,fixture=True))
 def test_omitted_carrier(self):self.mutate(lambda d:d['records'].pop())
 def test_omitted_saturation(self):self.mutate(lambda d:self.record(d)['source']['G'].pop())
 def test_omitted_profile(self):self.mutate(lambda d:self.record(d)['source']['a'].pop())
 def test_omitted_actual_label(self):self.mutate(lambda d:self.record(d)['vacancies'].pop())
 def test_omitted_subset(self):self.mutate(lambda d:self.record(d)['candidates'].pop(0))
 def test_omitted_root(self):self.mutate(lambda d:self.record(d)['candidates'].pop())
 def test_omitted_unsafe_candidate(self):
  def fn(d):
   r=self.record(d);i=next(i for i,c in enumerate(r['candidates']) if not c[-1]);r['candidates'].pop(i)
  self.mutate(fn)
 def test_omitted_verdict(self):self.mutate(lambda d:self.record(d)['evaluations'].pop())
 def test_omitted_cover(self):self.mutate(lambda d:self.record(d)['covers'].pop())
 def test_omitted_v_certificate(self):self.mutate(lambda d:self.record(d,'duplicate')['V'].pop())
 def test_omitted_x_certificate(self):self.mutate(lambda d:self.record(d)['X'].pop())
 def test_omitted_route(self):self.mutate(lambda d:self.record(d)['routes'].pop())
 def test_omitted_slice(self):self.mutate(lambda d:self.record(d)['routes'][0]['states'].pop())
 def test_omitted_hidden_mask(self):self.mutate(lambda d:self.record(d)['protected_masks'].pop())
 def test_shifted_floor(self):self.mutate(lambda d:self.record(d)['floors'].__setitem__(0,999))
 def test_wrong_label(self):self.mutate(lambda d:self.record(d)['routes'][0].__setitem__('label',999))
 def test_wrong_type(self):self.mutate(lambda d:self.record(d)['routes'][0].__setitem__('type',999))
 def test_early_vacancy(self):self.mutate(lambda d:self.record(d)['routes'][0]['states'][0].__setitem__(0,0))
 def test_early_outside_incidence(self):self.mutate(lambda d:self.record(d)['routes'][0]['states'].__setitem__(0,self.record(d)['routes'][0]['states'][-1]))
 def test_invalid_third_vertex(self):self.mutate(lambda d:self.record(d)['X'][0].__setitem__(2,self.record(d)['X'][0][0]))
 def test_missing_addition(self):self.mutate(lambda d:self.record(d)['routes'][0]['ops'].pop())
 def test_corrupted_cost(self):self.mutate(lambda d:self.record(d)['routes'][0].__setitem__('cost',999))
 def bad_source(self,fn):
  s=copy.deepcopy(self.record(self.data)['source']);fn(s)
  with self.assertRaises((AssertionError,ValueError)):independent.validate_source(s)
 def test_invalid_multiplicity(self):self.bad_source(lambda s:s['a'].__setitem__(0,0))
 def test_saturated_nonedge(self):self.bad_source(lambda s:s['G'].append([0,0]))
 def test_isolated_carrier_type(self):self.bad_source(lambda s:s.__setitem__('H',[e for e in s['H'] if 0 not in e]))
 def test_source_hitting_outside_domain(self):self.bad_source(lambda s:s.__setitem__('H',[[0,v] for v in range(1,5)]))
 def stream(self,kind):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/'ids.gz';rs=copy.deepcopy(self.data['records'])
   if kind=='truncated':rs.pop()
   if kind=='extra':rs.append(rs[-1])
   if kind=='corrupt':rs[0]['escape']=not rs[0]['escape']
   if kind!='missing':
    with gzip.open(p,'wt') as f:
     for r in rs:f.write(json.dumps(r)+'\n')
   with self.assertRaises((AssertionError,ValueError)):independent.verify(self.data,fixture=True,identity_path=str(p))
 def test_missing_stream(self):self.stream('missing')
 def test_truncated_stream(self):self.stream('truncated')
 def test_extra_stream(self):self.stream('extra')
 def test_corrupted_stream(self):self.stream('corrupt')
 def test_optimized_runtime_rejection(self):
  for module in ['producer','independent']:
   r=subprocess.run([sys.executable,'-O','-c','import '+module],cwd=pathlib.Path(__file__).parent,capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0);self.assertIn('requires assertions enabled',r.stderr)
if __name__=='__main__':unittest.main()
