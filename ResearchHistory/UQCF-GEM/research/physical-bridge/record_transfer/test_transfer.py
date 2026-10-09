import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('transfer_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):self.ready();self.assertTrue(self.mods['independent'].verify(self.cert));self.assertEqual(len(self.cert['sources']),4096)
 def test_identity(self):
  self.ready()
  for s in self.cert['sources']:self.assertEqual(s['decoded'],s['outside_misses'])
 def test_fibers(self):
  self.ready();self.assertTrue(any(f['mixed'] for f in self.cert['fibers1']));self.assertFalse(any(f['mixed'] for f in self.cert['fibers2']))
 def test_analytic_pair(self):
  self.ready();d={tuple(s['id']):s for s in self.cert['sources']};a,b=d[0,0,3],d[0,0,24]
  self.assertEqual(a['moments'][:7],b['moments'][:7]);self.assertEqual([a['tau'],b['tau']],[4,3]);self.assertEqual([a['admitted'],b['admitted']],[True,False]);self.assertEqual([a['decoded'][6],b['decoded'][6]],[2,0])
 def test_missing_source(self):self.reject(lambda c:c['sources'].pop())
 def test_duplicate_source(self):self.reject(lambda c:c['sources'].__setitem__(1,c['sources'][0]))
 def test_wrong_state(self):self.reject(lambda c:c['sources'][0]['state'].__setitem__(0,127))
 def test_wrong_tau(self):self.reject(lambda c:c['sources'][0].__setitem__('tau',3))
 def test_wrong_protected(self):self.reject(lambda c:c['sources'][0].__setitem__('protected',False))
 def test_wrong_admission(self):self.reject(lambda c:c['sources'][0].__setitem__('admitted',False))
 def test_wrong_singleton(self):self.reject(lambda c:c['sources'][0]['moments'].__setitem__(0,0))
 def test_wrong_pair(self):self.reject(lambda c:c['sources'][0]['moments'].__setitem__(7,0))
 def test_wrong_decode(self):self.reject(lambda c:c['sources'][0]['decoded'].__setitem__(6,0))
 def test_wrong_outside(self):self.reject(lambda c:c['sources'][0]['outside_misses'].__setitem__(6,0))
 def test_missing_fiber1(self):self.reject(lambda c:c['fibers1'].pop())
 def test_missing_fiber2(self):self.reject(lambda c:c['fibers2'].pop())
 def test_duplicate_fiber(self):self.reject(lambda c:c['fibers2'].__setitem__(1,c['fibers2'][0]))
 def test_missing_member(self):self.reject(lambda c:c['fibers1'][0]['members'].pop())
 def test_substituted_member(self):self.reject(lambda c:c['fibers2'][0]['members'].__setitem__(0,[9,9,9]))
 def test_false_mixed(self):self.reject(lambda c:c['fibers2'][0].__setitem__('mixed',True))
 def test_false_fiber_record(self):self.reject(lambda c:c['fibers1'][0]['record'].__setitem__(0,99))
 def test_missing_query(self):self.reject(lambda c:c['queries'].pop())
 def test_wrong_witness(self):self.reject(lambda c:c['witness'].__setitem__(0,[0,0,0]))
 def test_false_access(self):self.reject(lambda c:c['claims'].__setitem__('native_access_derived',True))
 def test_false_minimal_bits(self):self.reject(lambda c:c['claims'].__setitem__('minimal_bits',True))
 def test_false_order(self):self.reject(lambda c:c['claims'].__setitem__('sufficient_global_order',1))
 def test_false_scope(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['sources'][0]['id'].__setitem__(0,False))
if __name__=='__main__':unittest.main()
