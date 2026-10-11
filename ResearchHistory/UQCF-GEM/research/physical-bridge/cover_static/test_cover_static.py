"""Prospective scientific controls, written before either implementation."""
import copy
import gzip
import json
import pathlib
import tempfile
import subprocess
import sys
import unittest
import producer
import independent

class CoverStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = producer.build(fixture=True)

    def changed(self, change):
        data = copy.deepcopy(self.data)
        change(data)
        with self.assertRaises((AssertionError, ValueError)):
            independent.verify(data, fixture=True)

    def record(self, data, name='duplicate0'):
        return next(r for r in data['records'] if r['name'] == name)

    def test_missing_implementation_contract(self):
        self.assertTrue(independent.verify(self.data, fixture=True))

    def test_optimized_runtime_rejects(self):
        code = "import independent; print(independent.verify({'schema':'wrong','fixture':True,'records':[{}]*6,'record_sha256':[],'counts':{}},fixture=True))"
        result = subprocess.run([sys.executable,'-O','-c',code],cwd=pathlib.Path(__file__).parent,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('requires assertions enabled',result.stderr)

    def test_complete_family_identity(self):
        rows = producer.sources()
        self.assertEqual(len(rows), 3072)
        self.assertEqual(len({json.dumps(r, sort_keys=True) for r in rows}), 3072)
        self.assertEqual({n:sum(r['family']==n for r in rows) for n in {r['family'] for r in rows}},
                         {'K4':1024,'C5':1024,'K5':288,'K6-minus45':512,'K5-minus34':224})

    def test_cover_condition_rejects_floor_only_spare(self):
        r = self.record(self.data, 'essential0')
        self.assertFalse(r['static'])
        s = r['source']
        stars = independent.original_stars(s)
        bad = [set()] + stars[1:]
        self.assertEqual(independent.hitting(bad, s['H']), 5)
        self.assertTrue(all(sum(tuple(e) in f for f in bad)>=b for e,b in zip(s['H'],r['floors'])))
        with self.assertRaises(AssertionError): independent.validate_endpoint(s,bad)

    def test_nonminimum_cover_required(self):
        r = self.record(self.data, 'nonminimum')
        cs = {tuple(c['C']):c for c in r['covers']}
        self.assertFalse(cs[(0,1,2)]['eligible'])
        self.assertTrue(cs[(1,2,3,4)]['eligible'])
        self.assertTrue(r['static'])

    def test_duplicate_restores_eligibility(self):
        self.assertTrue(self.record(self.data)['static'])

    def test_nonessential_isolates(self):
        for name in ('isolate4','isolate5'): self.assertTrue(self.record(self.data,name)['static'])

    def test_locked_static_boundary(self):
        r=self.record(self.data,'locked')
        self.assertTrue(r['static'])
        self.assertNotIn('reachable',r)

    def test_every_declared_count_and_cover(self):
        for r in self.data['records']:
            self.assertEqual(r['minimum'], min(map(sum,r['feasible'])))
            self.assertEqual(r['minimizers'],[n for n in r['feasible'] if sum(n)==r['minimum']])
        self.assertTrue(independent.verify(self.data, fixture=True))

    def test_actual_anchor_endpoints(self):
        r=self.record(self.data)
        self.assertEqual({e['choice'] for e in r['endpoints']},{'first','last'})
        self.assertTrue(independent.verify(self.data,fixture=True))

    def test_original_hidden_masks(self):
        self.assertTrue(self.record(self.data)['protected_masks'])
        self.assertTrue(independent.verify(self.data,fixture=True))

    def test_omitted_carrier(self): self.changed(lambda d:d['records'].pop())
    def test_omitted_saturation(self): self.changed(lambda d:self.record(d)['source']['G'].pop())
    def test_omitted_profile(self): self.changed(lambda d:self.record(d)['source']['a'].pop())
    def test_omitted_cover(self): self.changed(lambda d:self.record(d)['covers'].pop())
    def test_omitted_independent_set(self): self.changed(lambda d:self.record(d)['independent'].pop())
    def test_omitted_count(self): self.changed(lambda d:self.record(d)['feasible'].pop())
    def test_omitted_minimizer(self): self.changed(lambda d:self.record(d)['minimizers'].pop())
    def test_omitted_endpoint(self): self.changed(lambda d:self.record(d)['endpoints'].pop())
    def test_omitted_protected_mask(self): self.changed(lambda d:self.record(d)['protected_masks'].pop())
    def test_shifted_floor(self): self.changed(lambda d:self.record(d)['floors'].__setitem__(0,99))
    def test_singleton_cover_depletion(self):
        self.changed(lambda d:self.record(d,'nonminimum')['covers'][0]['eligible'].append([0]))
    def test_wrong_actual_anchor(self): self.changed(lambda d:self.record(d)['endpoints'][0]['anchors'].__setitem__(0,999))
    def test_fresh_label(self): self.changed(lambda d:self.record(d)['endpoints'][0]['state'].append(1))
    def test_wrong_deficiency(self): self.changed(lambda d:self.record(d)['endpoints'][0].__setitem__('empty',999))

    def invalid_source(self,change):
        s=copy.deepcopy(self.record(self.data)['source']);change(s)
        with self.assertRaises((AssertionError,ValueError)): independent.validate_source(s)
    def test_zero_multiplicity(self): self.invalid_source(lambda s:s['a'].__setitem__(0,0))
    def test_saturated_nonedge(self): self.invalid_source(lambda s:s['G'].append([4,5]))
    def test_isolated_carrier(self): self.invalid_source(lambda s:s.__setitem__('H',[e for e in s['H'] if 0 not in e]))
    def test_source_tau_outside(self):
        self.invalid_source(lambda s:s.__setitem__('H',[[0,v] for v in range(1,6)]))
    def test_invalid_cover(self):
        s=self.record(self.data)['source']
        with self.assertRaises(AssertionError): independent.validate_cover(s,[0])
    def test_oversized_cover(self):
        s=self.record(self.data)['source']
        with self.assertRaises(AssertionError): independent.validate_cover(s,list(range(6)))

    def stream_reject(self,kind):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'identities.gz'
            records=copy.deepcopy(self.data['records'])
            if kind=='truncated': records.pop()
            if kind=='extra': records.append(records[-1])
            if kind=='corrupt': records[0]['minimum']=-1
            if kind!='missing':
                with gzip.open(p,'wt') as f:
                    for r in records: f.write(json.dumps(r)+'\n')
            with self.assertRaises((AssertionError,ValueError)):
                independent.verify(self.data,fixture=True,identity_path=str(p))
    def test_missing_stream(self): self.stream_reject('missing')
    def test_truncated_stream(self): self.stream_reject('truncated')
    def test_extra_stream(self): self.stream_reject('extra')
    def test_corrupt_stream(self): self.stream_reject('corrupt')

if __name__=='__main__': unittest.main()
