import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('reactive_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):
  self.ready();self.mods['independent'].verify(self.cert);self.assertEqual(len(self.cert['sources']),256)
 def test_hidden_marker_alias(self):
  self.ready()
  for g in self.cert['graphs']:
   clean=next(n for n in g['nodes'] if n['target']);dirty=next(n for n in g['nodes'] if n['core']==clean['core'] and not n['target'])
   self.assertEqual(clean['policy'],dirty['policy']);self.assertNotEqual(clean['state'],dirty['state'])
 def test_missing_source(self):self.reject(lambda c:c['sources'].pop())
 def test_duplicate_source(self):self.reject(lambda c:c['sources'].__setitem__(1,c['sources'][0]))
 def test_substituted_graph(self):self.reject(lambda c:c['graphs'].__setitem__(1,c['graphs'][0]))
 def test_missing_graph(self):self.reject(lambda c:c['graphs'].pop())
 def test_tau(self):self.reject(lambda c:c['sources'][0].__setitem__('tau',1))
 def test_eligibility(self):self.reject(lambda c:c['sources'][0].__setitem__('protected',False))
 def test_missing_state(self):self.reject(lambda c:c['graphs'][0]['nodes'].pop())
 def test_duplicate_state(self):self.reject(lambda c:c['graphs'][0]['nodes'].__setitem__(1,c['graphs'][0]['nodes'][0]))
 def test_missing_edge(self):self.reject(lambda c:c['graphs'][0]['edges'].pop())
 def test_duplicate_edge(self):self.reject(lambda c:c['graphs'][0]['edges'].append(c['graphs'][0]['edges'][0]))
 def test_omitted_noop(self):self.reject(lambda c:c['graphs'][0].__setitem__('edges',[e for e in c['graphs'][0]['edges'] if e[0]!=e[2]]))
 def test_reverse_change(self):
  def f(c):
   g=c['graphs'][0];e=next(e for e in g['edges'] if e[0]!=e[2]);g['edges'].append([e[2],e[1],e[0]])
  self.reject(f)
 def test_illegal_direct_deletion(self):
  def f(c):
   g=c['graphs'][0];src=g['start'];s=g['nodes'][src]['state'][:];s[5]^=8
   g['nodes'].append({'state':s});g['edges'].append([src,[5,3,0],len(g['nodes'])-1])
  self.reject(f)
 def test_floor(self):self.reject(lambda c:c['graphs'][0]['floors'].__setitem__(5,0))
 def test_rank(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('rank',-1))
 def test_policy(self):self.reject(lambda c:c['graphs'][0]['nodes'][c['graphs'][0]['start']].__setitem__('policy',[[5,5,1]]))
 def test_marker_observation(self):self.reject(lambda c:c['graphs'][0]['nodes'][0]['core'].__setitem__(5,255))
 def test_target(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('target',not c['graphs'][0]['nodes'][0]['target']))
 def test_excess(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('excess',99))
 def test_false_progress(self):self.reject(lambda c:c['claims'].__setitem__('guaranteed_progress',True))
 def test_false_completion(self):self.reject(lambda c:c['claims'].__setitem__('observable_completion',True))
 def test_false_origin(self):self.reject(lambda c:c['claims'].__setitem__('observer_origin',True))
 def test_false_marker_read(self):self.reject(lambda c:c['claims'].__setitem__('marker_observed',True))
 def test_false_uniform_safety(self):self.reject(lambda c:c['claims'].__setitem__('all_issued_commands_safe',True))
 def test_false_composition(self):self.reject(lambda c:c['claims'].__setitem__('arbitrary_macro_composition',True))
 def test_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['sources'][0]['id'].__setitem__(0,False))
if __name__=='__main__':unittest.main()
