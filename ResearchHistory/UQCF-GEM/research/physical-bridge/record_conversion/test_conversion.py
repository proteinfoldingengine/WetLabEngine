import copy, importlib.util, pathlib, unittest
HERE = pathlib.Path(__file__).parent

class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mods = {}
        for name in ('producer', 'independent'):
            path = HERE / (name + '.py')
            if path.exists():
                spec = importlib.util.spec_from_file_location('conversion_' + name, path)
                mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
                cls.mods[name] = mod
        cls.cert = cls.mods['producer'].produce() if 'producer' in cls.mods else None

    def ready(self):
        self.assertEqual(set(self.mods), {'producer', 'independent'}, 'expected RED: implementation absent')

    def reject(self, mutate):
        self.ready(); doc = copy.deepcopy(self.cert); mutate(doc)
        with self.assertRaises(ValueError): self.mods['independent'].verify(doc)

    def row(self, sigma, mask):
        self.ready(); return next(r for r in self.cert['rows'] if r['id'] == [0, [], sigma, mask])

    def test_complete_reconstruction(self):
        self.ready(); summary = self.mods['independent'].verify(self.cert)
        self.assertEqual((summary['requested'], summary['valid'], summary['rejected']), (1984, 496, 1488))
        self.assertEqual(summary['source_erased_positive'], 31)

    def test_full_positive_path(self):
        r = self.row(1, 31)
        self.assertEqual(r['states'], [[31,19,1,3,4,8], [31,19,17,3,4,8], [31,19,16,3,4,8], [31,19,18,3,4,8], [31,19,2,3,4,8], [31,3,2,3,4,8]])
        self.assertEqual(r['profiles'], [[3,1],[3,1],[3,2],[3,1],[3,1],[3,1]])
        self.assertEqual(r['executed'], [1,2,3,4,5]); self.assertEqual(r['peak'], 1)

    def test_one_sided_soundness(self):
        self.ready()
        for r in self.cert['rows']:
            if r['status'] == 'VALID':
                if r['record_at_stop']: self.assertEqual(r['id'][2], 1)
                if r['record_at_stop'] and r['source_erased_at_stop']:
                    self.assertEqual(r['id'][3], 31); self.assertEqual(r['end'][2], 2)
                self.assertLessEqual(r['peak'], 1)

    def test_skips_do_not_guarantee_write(self):
        r = self.row(1, 0); self.assertEqual(r['status'], 'VALID'); self.assertEqual(r['record_at_stop'], 0); self.assertEqual(r['executed'], [])

    def test_absent_deletions_are_rejected(self):
        for mask, step in [(8,4), (16,5)]:
            r = self.row(0,mask); self.assertEqual(r['status'], 'REJECTED'); self.assertEqual(r['failure'], step); self.assertEqual(r['executed'], [])

    def test_forgery_native_valid_but_outside_protocol(self):
        self.ready(); f = self.cert['forgery']
        self.assertEqual(f['states'], [[31,3,1,3,4,8],[31,3,3,3,4,8],[31,3,2,3,4,8]])
        self.assertTrue(f['native_valid']); self.assertFalse(f['protocol_valid']); self.assertEqual(f['record'],1); self.assertTrue(f['source_erased']); self.assertEqual(f['peak'],0)

    def test_missing(self): self.reject(lambda d: d['rows'].pop())
    def test_duplicate(self): self.reject(lambda d: d['rows'].__setitem__(1,copy.deepcopy(d['rows'][0])))
    def test_substitution(self): self.reject(lambda d: d['rows'][0]['id'].__setitem__(1,[4]))
    def test_wrong_source_bit(self): self.reject(lambda d: d['rows'][0]['id'].__setitem__(2,1))
    def test_false_record(self): self.reject(lambda d: d['rows'][0].__setitem__('record_at_stop',1))
    def test_illegal_state(self): self.reject(lambda d: d['rows'][0]['states'][0].__setitem__(2,16))
    def test_omitted_transient(self): self.reject(lambda d: next(r for r in d['rows'] if r['id']==[0,[],1,31])['states'].pop(2))
    def test_false_zero_peak(self): self.reject(lambda d: next(r for r in d['rows'] if r['id']==[0,[],1,31]).__setitem__('peak',0))
    def test_wrong_order(self): self.reject(lambda d: d['commands'].__setitem__(1,[2,1,1]))
    def test_false_access(self): self.reject(lambda d: d['claims'].__setitem__('native_access',True))
    def test_false_guarantee(self): self.reject(lambda d: d['claims'].__setitem__('guaranteed_write',True))
    def test_wrong_parent(self): self.reject(lambda d: d.__setitem__('source_parent','0'*40))
    def test_wrong_scope(self): self.reject(lambda d: d.__setitem__('scope_sha256','0'*64))
    def test_bool_identity(self): self.reject(lambda d: d['rows'][0]['id'].__setitem__(0,False))
    def test_forgery_native_rejection(self): self.reject(lambda d: d['forgery'].__setitem__('native_valid',False))
    def test_forgery_protocol_acceptance(self): self.reject(lambda d: d['forgery'].__setitem__('protocol_valid',True))
    def test_syntax_laundered_as_skip(self):
        def mutate(d):
            r=next(r for r in d['rows'] if r['id']==[0,[],0,16]); r['status']='VALID';r['failure']=None
        self.reject(mutate)

if __name__ == '__main__': unittest.main()
