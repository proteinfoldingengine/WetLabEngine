import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('deficit_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):
  self.ready();self.mods['independent'].verify(self.cert);self.assertEqual(len(self.cert['sources_a']),4096);self.assertEqual(len(self.cert['sources_b']),18)
 def test_fixtures(self):
  self.ready();self.assertEqual(self.cert['fixtures']['moving']['peak'],1);self.assertEqual(self.cert['fixtures']['moving']['persistent_cover_tau'],5);self.assertEqual(self.cert['fixtures']['rise']['taus'][0],3);self.assertEqual(self.cert['fixtures']['rise']['taus'][4],4)
 def test_missing_source(self):self.reject(lambda c:c['sources_a'].pop())
 def test_duplicate_source(self):self.reject(lambda c:c['sources_b'].__setitem__(1,c['sources_b'][0]))
 def test_substituted_handoff(self):self.reject(lambda c:c['handoffs'].__setitem__(1,c['handoffs'][0]))
 def test_missing_goal(self):self.reject(lambda c:c['goals'].pop())
 def test_tau(self):self.reject(lambda c:c['sources_a'][0].__setitem__('tau',1))
 def test_eligibility(self):self.reject(lambda c:c['sources_a'][0].__setitem__('protected',not c['sources_a'][0]['protected']))
 def test_slice(self):self.reject(lambda c:c['handoffs'][0]['states'][2].__setitem__(5,0))
 def test_map(self):self.reject(lambda c:c['handoffs'][0]['maps'][3].__setitem__(3,3))
 def test_floor(self):self.reject(lambda c:c['handoffs'][0]['minimum_sizes'].__setitem__(0,0))
 def test_target(self):self.reject(lambda c:c['goals'][1]['states'][-1].__setitem__(0,0))
 def test_marker(self):self.reject(lambda c:c['handoffs'][0]['states'][-1].__setitem__(5,c['handoffs'][0]['states'][-1][5]|32))
 def test_plan(self):self.reject(lambda c:c['goals'][1]['exchanges'].append([0,3]))
 def test_peak(self):self.reject(lambda c:c['handoffs'][0].__setitem__('peak',0))
 def test_certificate(self):self.reject(lambda c:c['handoffs'][0].__setitem__('certificate',[]))
 def test_partition(self):self.reject(lambda c:c['handoffs'][0]['covered'].append(0))
 def test_deficit(self):self.reject(lambda c:c['handoffs'][0]['deficit'].pop())
 def test_false_exact_tau(self):self.reject(lambda c:c['claims'].__setitem__('exact_tau',True))
 def test_band(self):self.reject(lambda c:c['claims'].__setitem__('band',[3,5]))
 def test_progress(self):self.reject(lambda c:c['claims'].__setitem__('guaranteed_requests',True))
 def test_observer(self):self.reject(lambda c:c['claims'].__setitem__('observer_origin',True))
 def test_optimality(self):self.reject(lambda c:c['claims'].__setitem__('path_optimal',True))
 def test_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['sources_a'][0]['id'].__setitem__(0,False))
 def test_fixed_cover(self):self.reject(lambda c:c['fixtures']['moving'].__setitem__('persistent_cover_tau',4))
if __name__=='__main__':unittest.main()
