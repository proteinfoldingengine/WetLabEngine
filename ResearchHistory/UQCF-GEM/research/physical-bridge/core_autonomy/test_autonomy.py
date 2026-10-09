import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('autonomy_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):self.ready();self.assertTrue(self.mods['independent'].verify(self.cert));self.assertEqual(len(self.cert['states']),128)
 def test_all_commit_not_noop_only(self):
  self.ready();trace=self.cert['scratch_trace'];self.assertEqual(len(trace),5);self.assertNotEqual(trace[0],trace[1]);self.assertEqual(trace[0],trace[-1])
  for g in self.cert['pairs']:
   self.assertTrue(any(e[2]==1 for e in g['edges']))
 def test_nonuniform_guard_boundary(self):
  self.ready();self.assertTrue(any(r['left_legal']!=r['right_legal'] for r in self.cert['nonuniform']));self.assertIn({'pair':[0,3],'core':[0,0,0,0,0],'command':[3,4,1],'left_legal':True,'right_legal':False},self.cert['nonuniform'])
 def test_admission_application(self):
  self.ready();f=self.cert['admission'];self.assertEqual(f['taus'],[[4,4],[3,3]]);self.assertEqual(f['admission'],[True,False]);self.assertEqual(f['cores'][0],f['cores'][1])
 def test_missing_state(self):self.reject(lambda c:c['states'].pop())
 def test_duplicate_state(self):self.reject(lambda c:c['states'].__setitem__(1,c['states'][0]))
 def test_tau(self):self.reject(lambda c:c['states'][0].__setitem__('tau',2))
 def test_floor(self):self.reject(lambda c:c['states'][0].__setitem__('floor_valid',False))
 def test_admissible(self):self.reject(lambda c:c['states'][0].__setitem__('admissible',False))
 def test_support(self):self.reject(lambda c:c['states'][0]['supports'].__setitem__(0,0))
 def test_missing_guarded_edge(self):self.reject(lambda c:c['guarded_edges'].pop())
 def test_duplicate_guarded_edge(self):self.reject(lambda c:c['guarded_edges'].append(c['guarded_edges'][0]))
 def test_missing_pair(self):self.reject(lambda c:c['pairs'].pop())
 def test_substituted_pair(self):self.reject(lambda c:c['pairs'].__setitem__(1,c['pairs'][0]))
 def test_missing_pair_node(self):self.reject(lambda c:c['pairs'][0]['nodes'].pop())
 def test_missing_pair_edge(self):self.reject(lambda c:c['pairs'][0]['edges'].pop())
 def test_duplicate_pair_edge(self):self.reject(lambda c:c['pairs'][0]['edges'].append(c['pairs'][0]['edges'][0]))
 def test_wrong_resolution_mask(self):self.reject(lambda c:c['pairs'][0]['edges'][0].__setitem__(2,9))
 def test_wrong_core_effect(self):self.reject(lambda c:c['pairs'][0]['edges'][0][3].__setitem__(0,9))
 def test_admit_nonuniform(self):self.reject(lambda c:c['pairs'][3]['edges'].append([[0,0,0,0,0],[3,4,1],1,[0,0,1,0,0]]))
 def test_missing_nonuniform(self):self.reject(lambda c:c['nonuniform'].pop())
 def test_false_nonuniform(self):self.reject(lambda c:c['nonuniform'][0].__setitem__('left_legal',not c['nonuniform'][0]['left_legal']))
 def test_constant_scratch(self):self.reject(lambda c:c['scratch_trace'].__setitem__(1,c['scratch_trace'][0]))
 def test_false_distribution_claim(self):self.reject(lambda c:c['claims'].__setitem__('arbitrary_kernel_distribution_equality',True))
 def test_false_universal_observer(self):self.reject(lambda c:c['claims'].__setitem__('universal_no_observer',True))
 def test_false_noop_dependency(self):self.reject(lambda c:c['claims'].__setitem__('relies_on_all_noop',True))
 def test_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['states'][0]['id'].__setitem__(0,False))
if __name__=='__main__':unittest.main()
