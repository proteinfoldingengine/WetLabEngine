"""Adversarial tests for the exact-head v15.44 CI boundary."""
import unittest
from pathlib import Path

import ci_verify


class Record:
    def __init__(self, code=0, out=b'', err=b''):
        self.returncode = code
        self.stdout = out
        self.stderr = err


class CITests(unittest.TestCase):
    def valid_result(self):
        carriers=[]
        for L,scale,rank in ((5,'1',24),(5,'7/3',24),(7,'1',48),(7,'7/3',48)):
            nullity=L*L-rank
            carriers.append({'L':L,'scale':scale,'certificate':{'rank':rank,'nullity':nullity,
                'null_basis':[[0]*nullity for _ in range(L*L)]},
                'control':{'rank':rank,'nullity':nullity,'exact':True},
                'constant_field_annihilated':True})
        return {'status':'INTRINSIC_CURVATURE_CHARACTERIZED','first_failed_stage':None,
                'failure':None,'completed_counts':{'cases':740,'controls':4,'pairs':592,'scale_pairs':370},
                'scientific_verdict':{'claims':dict(ci_verify.EXPECTED_CLAIMS),
                    'cases':[None]*740,'pairs':[None]*592,'scale_pairs':[None]*370,
                    'coverage':{'cases':740,'pairs':592,'scale_pairs':370,
                        'by_carrier':[{'L':5,'scale':'1','pairs':100},
                            {'L':5,'scale':'7/3','pairs':100},{'L':7,'scale':'1','pairs':196},
                            {'L':7,'scale':'7/3','pairs':196}],
                        'by_control':{str(i):148 for i in range(4)}},
                    'interpretation':'EXACT_FINITE_FOUR_CARRIER_CHARACTERIZATION_ONLY',
                    'carriers':carriers}}

    def test_additive_scope_only(self):
        ci_verify.validate_scope(['A\t' + ci_verify.DEMO + '/new.py'])
        for line in ('M\t' + ci_verify.DEMO + '/new.py',
                     'A\tREADME.md', 'R100\told\tnew'):
            with self.subTest(line=line), self.assertRaisesRegex(ValueError, 'nonadditive_scope'):
                ci_verify.validate_scope([line])

    def test_head_must_match_expected_at_start_and_finish(self):
        ci_verify.verify_head('abc', 'abc', 'initial')
        for stage in ('initial', 'final'):
            with self.subTest(stage=stage), self.assertRaisesRegex(ValueError, stage + '_head_mismatch'):
                ci_verify.verify_head('abc', 'def', stage)

    def test_approved_spec_blob_drift(self):
        with self.assertRaisesRegex(ValueError, 'approved_spec_mismatch'):
            ci_verify.verify_blob(b'drift', ci_verify.SPEC_BLOB, 'approved_spec')

    def test_incomplete_ledger_rejected(self):
        result = self.valid_result()
        result['completed_counts']['pairs'] -= 1
        with self.assertRaisesRegex(ValueError, 'incomplete_coverage'):
            ci_verify.verify_result(result)

    def test_false_physical_claim_rejected(self):
        result = self.valid_result()
        result['scientific_verdict']['claims']['physical_curvature'] = True
        with self.assertRaisesRegex(ValueError, 'claim_boundary'):
            ci_verify.verify_result(result)

    def test_runtime_is_exact(self):
        ci_verify.verify_runtime((3, 13, 5))
        with self.assertRaisesRegex(ValueError, 'official_python'):
            ci_verify.verify_runtime((3, 13, 6))

    def test_suite_rejects_skips_expected_failures_and_wrong_count(self):
        ci_verify.verify_suite_receipt(b'SUITE_COUNT 56 EXPECTED 56 SKIPS 0 EXPECTED_FAILURES 0 UNEXPECTED_SUCCESSES 0 ACCEPTED True\n', 56)
        for raw in (b'SUITE_COUNT 55 EXPECTED 56 SKIPS 0 EXPECTED_FAILURES 0 UNEXPECTED_SUCCESSES 0 ACCEPTED False\n',
                    b'SUITE_COUNT 56 EXPECTED 56 SKIPS 1 EXPECTED_FAILURES 0 UNEXPECTED_SUCCESSES 0 ACCEPTED False\n',
                    b'SUITE_COUNT 56 EXPECTED 56 SKIPS 0 EXPECTED_FAILURES 1 UNEXPECTED_SUCCESSES 0 ACCEPTED False\n'):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'suite_receipt'):
                ci_verify.verify_suite_receipt(raw, 56)

    def test_run_stage_uses_injected_subprocess_record(self):
        def runner(*args, **kwargs): return Record(7, b'out', b'err')
        with self.assertRaisesRegex(RuntimeError, 'probe: exit 7'):
            ci_verify.run_stage('probe', ['false'], Path('.'), 1, runner=runner)


if __name__ == '__main__':
    unittest.main()
