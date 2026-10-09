import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('shared_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'intended RED: absent implementation')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):
  self.ready();self.mods['independent'].verify(self.cert)
  self.assertEqual(len(self.cert['sources_a']),7200);self.assertEqual(len(self.cert['sources_b']),108)
 def test_missing_source(self):self.reject(lambda c:c['sources_a'].pop())
 def test_duplicate_source(self):self.reject(lambda c:c['sources_b'].__setitem__(1,c['sources_b'][0]))
 def test_substituted_path(self):self.reject(lambda c:c['handoffs'].__setitem__(1,c['handoffs'][0]))
 def test_missing_goal(self):self.reject(lambda c:c['goals'].pop())
 def test_wrong_tau(self):self.reject(lambda c:c['sources_a'][0].__setitem__('tau',2))
 def test_false_admissibility(self):self.reject(lambda c:c['sources_a'][0].__setitem__('protected',False))
 def test_invalid_intermediate(self):self.reject(lambda c:c['handoffs'][0]['states'][2].__setitem__(5,0))
 def test_broken_substitution(self):self.reject(lambda c:c['handoffs'][0]['maps'][3].__setitem__(2,2))
 def test_wrong_floor(self):self.reject(lambda c:c['handoffs'][0]['minimum_sizes'].__setitem__(0,1))
 def test_wrong_target(self):self.reject(lambda c:c['goals'][1]['states'][-1].__setitem__(0,0))
 def test_marker_retained(self):self.reject(lambda c:c['handoffs'][0]['states'][-1].__setitem__(5,c['handoffs'][0]['states'][-1][4]|256))
 def test_changed_plan(self):self.reject(lambda c:c['goals'][1]['exchanges'].append([0,2]))
 def test_bound(self):self.reject(lambda c:c['claims'].__setitem__('edit_bound_factor',7))
 def test_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_observer(self):self.reject(lambda c:c['claims'].__setitem__('observer_origin',True))
 def test_progress(self):self.reject(lambda c:c['claims'].__setitem__('guaranteed_requests',True))
 def test_optimality(self):self.reject(lambda c:c['claims'].__setitem__('optimal',True))
 def test_type(self):self.reject(lambda c:c['sources_a'][0]['id'].__setitem__(0,False))
 def test_moving_cover(self):
  self.ready();self.assertEqual(self.cert['fixture']['source_tau'],4);self.assertEqual(self.cert['fixture']['alternating_taus'][4],5);self.assertEqual(self.cert['fixture']['persistent_cover_tau'],5)
 def test_false_fixed_cover(self):self.reject(lambda c:c['fixture'].__setitem__('persistent_cover_tau',4))
 def test_peak(self):self.reject(lambda c:c['handoffs'][0].__setitem__('peak',0))
 def test_one_incidence(self):self.reject(lambda c:c['claims'].__setitem__('one_excess_incidence',True))
if __name__=='__main__':unittest.main()
