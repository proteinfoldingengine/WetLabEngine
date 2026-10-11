"""Publication controls, separate from the 23 scientific tests."""
import copy,importlib.util,json,pathlib,unittest
P=pathlib.Path(__file__).parent
class Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod=None;path=P/'audit_originals.py'
        if path.exists():
            spec=importlib.util.spec_from_file_location('conversion_audit',path);cls.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.mod)
    def ready(self):
        self.assertIsNotNone(self.mod,'expected RED: publication auditor absent')
        return self.mod.load(P)
    def reject(self,mutate):
        packet=self.ready();mutate(packet)
        with self.assertRaises((ValueError,KeyError)):self.mod.check(packet)
    def test_intact(self):
        packet=self.ready();self.assertEqual(self.mod.check(packet)['status'],'VERIFIED')
    def test_missing_member(self):self.reject(lambda p:p['archives']['conversion-verification'].pop('producer.py'))
    def test_corrupt_certificate(self):self.reject(lambda p:p['archives']['conversion-reproduction'].__setitem__('certificate.json',b'{}'))
    def test_wrong_scientific_commit(self):self.reject(lambda p:p['run'].__setitem__('head_sha','0'*40))
    def test_false_success(self):self.reject(lambda p:p['jobs']['jobs'][0].__setitem__('conclusion','failure'))
    def test_missing_suite(self):self.reject(lambda p:p['archives']['conversion-verification'].pop('star_carrier_tests.log'))
    def test_rewritten_raw_review(self):self.reject(lambda p:p['archives']['conversion-review'].__setitem__('review.txt',b'{"verdict":"ACCEPTED"}'))
    def test_false_review_input(self):
        def mutate(p):
            a=p['archives']['conversion-publication'];m=json.loads(a['manifest.json']);m['input_sha256'].pop(next(iter(m['input_sha256'])));a['manifest.json']=json.dumps(m).encode()
        self.reject(mutate)
    def test_truncated_job_log(self):self.reject(lambda p:p['logs'].__setitem__('verification_job.log',b'ACCEPTED'))
    def test_false_gate(self):
        def mutate(p):
            a=p['archives']['conversion-gate'];g=json.loads(a['publication_gate.json']);g['mathematical_inputs_verified']=0;a['publication_gate.json']=json.dumps(g).encode()
        self.reject(mutate)
if __name__=='__main__':unittest.main()
