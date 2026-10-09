import copy
import importlib.util
import pathlib
import unittest

HERE=pathlib.Path(__file__).parent

class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules={}
        for name in ('producer','independent'):
            path=HERE/(name+'.py')
            if path.exists():
                spec=importlib.util.spec_from_file_location('handoff_'+name,path)
                mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
                cls.modules[name]=mod
        cls.cert=cls.modules['producer'].produce() if 'producer' in cls.modules else None

    def ready(self):
        self.assertEqual(set(self.modules),{'producer','independent'},'intended RED: implementation absent')

    def reject(self,edit):
        self.ready(); c=copy.deepcopy(self.cert);edit(c)
        with self.assertRaises(ValueError):self.modules['independent'].verify(c)

    def test_full_independent_universe(self):
        self.ready();self.modules['independent'].verify(self.cert)
        self.assertEqual(len(self.cert['sources']),768)
        self.assertEqual(len(self.cert['paths']),384)
        self.assertEqual(len(self.cert['walks']),768)
    def test_missing_source(self):self.reject(lambda c:c['sources'].pop())
    def test_duplicate_source(self):self.reject(lambda c:c['sources'].__setitem__(1,c['sources'][0]))
    def test_substituted_path(self):self.reject(lambda c:c['paths'].__setitem__(1,c['paths'][0]))
    def test_missing_path(self):self.reject(lambda c:c['paths'].pop())
    def test_wrong_tau(self):self.reject(lambda c:c['sources'][0].__setitem__('tau',2))
    def test_invalid_spectator_classification(self):self.reject(lambda c:c['sources'][0].__setitem__('separated',False))
    def test_illegal_intermediate(self):self.reject(lambda c:c['paths'][0]['states'][2].__setitem__(3,0))
    def test_wrong_floor_minimum(self):self.reject(lambda c:c['paths'][0]['minimum_sizes'].__setitem__(0,1))
    def test_unremoved_marker(self):self.reject(lambda c:c['paths'][0]['states'][-1].__setitem__(3,c['paths'][0]['states'][-1][3]|32))
    def test_wrong_renewal(self):self.reject(lambda c:c['walks'][0]['states'][-1].__setitem__(0,0))
    def test_false_provenance(self):self.reject(lambda c:c.__setitem__('scope_commit','0'*40))
    def test_false_observer_claim(self):self.reject(lambda c:c['claims'].__setitem__('observer_origin',True))
    def test_false_progress_claim(self):self.reject(lambda c:c['claims'].__setitem__('guaranteed_request_completion',True))
    def test_false_optimality(self):self.reject(lambda c:c['claims'].__setitem__('optimal',True))
    def test_numeric_boolean_substitution(self):self.reject(lambda c:c['sources'][0]['id'].__setitem__(0,False))

if __name__=='__main__':unittest.main()
