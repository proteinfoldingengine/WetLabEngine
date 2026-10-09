import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('family_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):self.ready();self.assertTrue(self.mods['independent'].verify(self.cert));self.assertEqual(len(self.cert['states']),4096);self.assertEqual(len(self.cert['fibers']),4032)
 def test_all_categories(self):
  self.ready();d={tuple(f['id']):f for f in self.cert['fibers']};self.assertEqual(d[0,0,1]['category'],'forced_false');self.assertEqual(d[0,0,24]['category'],'mixed');self.assertEqual(d[0,0,62]['category'],'forced_true')
 def test_sharp_preparation(self):
  self.ready()
  for f in self.cert['fibers']:
   self.assertEqual(f['preparation_possible'],f['complement_tau']<=1)
   if not f['preparation_possible']:self.assertTrue(f['witness']['protected']);self.assertIn(f['id'][2],f['no_masks'])
 def test_full_partition(self):
  self.ready()
  for f in self.cert['fibers']:self.assertEqual(sorted(f['yes_masks']+f['no_masks']),f['admissible_masks']);self.assertFalse(set(f['yes_masks'])&set(f['no_masks']))
 def test_missing_state(self):self.reject(lambda c:c['states'].pop())
 def test_duplicate_state(self):self.reject(lambda c:c['states'].__setitem__(1,c['states'][0]))
 def test_tau(self):self.reject(lambda c:c['states'][0].__setitem__('tau',2))
 def test_state(self):self.reject(lambda c:c['states'][0]['supports'].__setitem__(0,0))
 def test_floor(self):self.reject(lambda c:c['states'][0]['floors'].__setitem__(0,9))
 def test_protected(self):self.reject(lambda c:c['states'][0].__setitem__('protected',False))
 def test_missing_fiber(self):self.reject(lambda c:c['fibers'].pop())
 def test_substitute_fiber(self):self.reject(lambda c:c['fibers'].__setitem__(1,c['fibers'][0]))
 def test_missing_completion(self):self.reject(lambda c:c['fibers'][0]['admissible_masks'].pop())
 def test_duplicate_completion(self):self.reject(lambda c:c['fibers'][0]['admissible_masks'].append(0))
 def test_missing_false_member(self):self.reject(lambda c:c['fibers'][0]['no_masks'].pop())
 def test_substituted_truth(self):self.reject(lambda c:c['fibers'][0]['yes_masks'].append(0))
 def test_core_intersection(self):self.reject(lambda c:c['fibers'][0].__setitem__('core_intersection',[]))
 def test_complement_tau(self):self.reject(lambda c:c['fibers'][0].__setitem__('complement_tau',1))
 def test_category(self):self.reject(lambda c:c['fibers'][0].__setitem__('category','forced_true'))
 def test_preparation(self):self.reject(lambda c:c['fibers'][0].__setitem__('preparation_possible',True))
 def test_witness_tau(self):self.reject(lambda c:c['fibers'][0]['witness'].__setitem__('tau',2))
 def test_witness_protected(self):self.reject(lambda c:c['fibers'][0]['witness'].__setitem__('protected',False))
 def test_false_hidden_control(self):self.reject(lambda c:c['claims'].__setitem__('hidden_edits_covered',True))
 def test_false_retarget(self):self.reject(lambda c:c['claims'].__setitem__('retargeting_covered',True))
 def test_false_native_access(self):self.reject(lambda c:c['claims'].__setitem__('native_access_derived',True))
 def test_false_floor_extension(self):self.reject(lambda c:c['claims'].__setitem__('floors_above_core_covered',True))
 def test_scope(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['fibers'][0]['id'].__setitem__(0,False))
if __name__=='__main__':unittest.main()
