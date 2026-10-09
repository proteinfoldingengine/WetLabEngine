import copy,importlib.util,pathlib,unittest
HERE=pathlib.Path(__file__).parent
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mods={}
  for n in ('producer','independent'):
   p=HERE/(n+'.py')
   if p.exists():
    s=importlib.util.spec_from_file_location('visible_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cls.mods[n]=m
  cls.cert=cls.mods['producer'].produce() if 'producer' in cls.mods else None
 def ready(self):self.assertEqual(set(self.mods),{'producer','independent'},'expected RED: implementation absent')
 def reject(self,f):
  self.ready();c=copy.deepcopy(self.cert);f(c)
  with self.assertRaises(ValueError):self.mods['independent'].verify(c)
 def test_complete(self):
  self.ready();self.mods['independent'].verify(self.cert);self.assertEqual(len(self.cert['sources']),256);self.assertEqual(len(self.cert['paths']),64)
 def test_observable_deterministic_endpoint(self):
  self.ready()
  for g in self.cert['graphs']:
   self.assertEqual(g['edges'],g['guarded_edges']);self.assertEqual(sum(n['target'] for n in g['nodes']),1)
   for n in g['nodes']:self.assertEqual(len(n['policy']),0 if n['target'] else 1);self.assertTrue(all(not v&32 for v in n['state']))
 def test_sharp_boundary(self):
  self.ready();self.assertEqual(self.cert['fixtures']['triangle']['taus'],[3,2]);self.assertEqual(self.cert['fixtures']['disjoint']['taus'],[4,3,4])
 def test_no_runtime_guard_query(self):
  self.ready();m=self.mods['producer'];s=(1,1,1,2,4,24);old=m.tau
  def forbidden(*a):raise AssertionError('runtime tau query')
  try:
   m.tau=forbidden;self.assertEqual(m.policy(s,0,0),[(5,0,1)]);self.assertEqual(m.syntax_outcomes(s,(5,0,1)),[s,(1,1,1,2,4,25)])
  finally:m.tau=old
 def test_missing_source(self):self.reject(lambda c:c['sources'].pop())
 def test_duplicate_source(self):self.reject(lambda c:c['sources'].__setitem__(1,c['sources'][0]))
 def test_substituted_graph(self):self.reject(lambda c:c['graphs'].__setitem__(1,c['graphs'][0]))
 def test_missing_graph(self):self.reject(lambda c:c['graphs'].pop())
 def test_source_tau(self):self.reject(lambda c:c['sources'][0].__setitem__('tau',3))
 def test_source_admission(self):self.reject(lambda c:c['sources'][0].__setitem__('eligible',False))
 def test_wrong_residual_tau(self):self.reject(lambda c:c['sources'][0].__setitem__('rho',1))
 def test_wrong_formula(self):self.reject(lambda c:c['sources'][0].__setitem__('prepared_tau',4))
 def test_missing_node(self):self.reject(lambda c:c['graphs'][0]['nodes'].pop())
 def test_duplicate_node(self):self.reject(lambda c:c['graphs'][0]['nodes'].__setitem__(1,c['graphs'][0]['nodes'][0]))
 def test_missing_edge(self):self.reject(lambda c:c['graphs'][0]['edges'].pop())
 def test_duplicate_edge(self):self.reject(lambda c:c['graphs'][0]['edges'].append(c['graphs'][0]['edges'][0]))
 def test_guarded_edge_mismatch(self):self.reject(lambda c:c['graphs'][0]['guarded_edges'].pop())
 def test_missing_noop(self):self.reject(lambda c:c['graphs'][0].__setitem__('edges',[e for e in c['graphs'][0]['edges'] if e[0]!=e[2]]))
 def test_illegal_host_delete(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('policy',[[5,3,0]]))
 def test_reverse_edge(self):
  def f(c):
   g=c['graphs'][0];e=next(e for e in g['edges'] if e[0]!=e[2]);g['edges'].append([e[2],e[1],e[0]])
  self.reject(f)
 def test_marker_insert(self):self.reject(lambda c:c['graphs'][0]['nodes'][0]['state'].__setitem__(5,c['graphs'][0]['nodes'][0]['state'][5]|32))
 def test_floor(self):self.reject(lambda c:c['graphs'][0]['floors'].__setitem__(5,0))
 def test_rank(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('rank',-1))
 def test_hidden_read(self):self.reject(lambda c:c['graphs'][0]['nodes'][0]['core'].__setitem__(0,127))
 def test_target(self):self.reject(lambda c:c['graphs'][0]['nodes'][0].__setitem__('target',not c['graphs'][0]['nodes'][0]['target']))
 def test_budget(self):self.reject(lambda c:c['paths'][0].__setitem__('beta',0))
 def test_missing_path(self):self.reject(lambda c:c['paths'].pop())
 def test_path_command(self):self.reject(lambda c:c['paths'][0]['commands'][0].__setitem__(1,5))
 def test_false_exact_tau(self):self.reject(lambda c:c['claims'].__setitem__('exact_tau_preserved',True))
 def test_false_progress(self):self.reject(lambda c:c['claims'].__setitem__('guaranteed_progress',True))
 def test_false_unobservable(self):self.reject(lambda c:c['claims'].__setitem__('observable_completion',False))
 def test_false_origin(self):self.reject(lambda c:c['claims'].__setitem__('observer_origin',True))
 def test_false_guard_needed(self):self.reject(lambda c:c['claims'].__setitem__('runtime_guard_required',True))
 def test_false_native_guard(self):self.reject(lambda c:c['claims'].__setitem__('universal_guard_derived',True))
 def test_false_uniform_safety(self):self.reject(lambda c:c['claims'].__setitem__('all_issued_commands_safe',False))
 def test_false_new_label(self):self.reject(lambda c:c['claims'].__setitem__('new_labels',1))
 def test_false_tau3_universal(self):self.reject(lambda c:c['claims'].__setitem__('all_tau3_sources_safe',True))
 def test_false_optimality(self):self.reject(lambda c:c['claims'].__setitem__('path_optimal',True))
 def test_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
 def test_type(self):self.reject(lambda c:c['sources'][0]['id'].__setitem__(0,False))
 def test_missing_triangle(self):self.reject(lambda c:c['fixtures'].pop('triangle'))
if __name__=='__main__':unittest.main()
