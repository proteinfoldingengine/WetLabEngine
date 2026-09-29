"""Behavioral and rejecting tests. Small fixtures are checker controls, not the campaign."""
from __future__ import annotations
import copy
import importlib
import json
from pathlib import Path
import sys
import unittest
from fractions import Fraction as F

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
MUTATIONS = []
PATH = ((), (0,), (0, 0))
STAR = ((), (0,), (1,))

class Tests(unittest.TestCase):
    def modules(self):
        for name in ('lineage', 'enumerate_cases', 'produce_certificates', 'verify_certificates'):
            self.assertTrue((HERE / (name + '.py')).is_file(), 'expected wiring RED: missing ' + name)
        return tuple(importlib.import_module(n) for n in ('lineage', 'enumerate_cases', 'produce_certificates', 'verify_certificates'))

    def instance(self, keys=PATH):
        return self.modules()[2].build_instance('checker-control', keys, max_arrows=3)

    def rejected(self, label, mutate):
        v = self.modules()[3]
        obj = self.instance()
        mutate(obj)
        with self.assertRaises(v.VerificationError) as caught:
            v.verify_instance(obj)
        MUTATIONS.append({'defect': label, 'rejected': True, 'reason': str(caught.exception)})

    def test_direct_fiber_sum_and_section(self):
        l, _, _, v = self.modules()
        a = l.Carrier('g', PATH); b = l.Carrier('g', PATH[:2])
        p = l.Pruning(a, b)
        self.assertEqual(p.aggregate((F(1, 3), F(-2, 3), F(4, 3))), (F(1, 3), F(2, 3)))
        self.assertEqual(p.ancestor((0, 0)), (0,))
        v.verify_instance(self.instance())

    def test_invalid_carriers_are_not_repaired(self):
        l, _, _, _ = self.modules()
        for keys in ((), ((0,),), ((), (0, 0)), ((), (0,), (0,)), ((), (-1,)), ((), (True,)), ((), ('x',))):
            with self.subTest(keys=keys), self.assertRaises(ValueError):
                l.Carrier('g', keys)

    def test_illegal_target_and_origin_rejected(self):
        l, _, _, _ = self.modules()
        a = l.Carrier('g', PATH)
        with self.assertRaises(ValueError): l.Pruning(a, l.Carrier('g', ((), (1,))))
        with self.assertRaises(ValueError): l.Pruning(a, l.Carrier('different-origin', PATH[:2]))

    def test_incompatible_composition_rejected(self):
        l, _, _, _ = self.modules()
        a = l.Pruning(l.Carrier('g', PATH), l.Carrier('g', PATH[:2]))
        b = l.Pruning(l.Carrier('g', STAR), l.Carrier('g', ((),)))
        with self.assertRaises(ValueError): a.then(b)
        c = l.Pruning(l.Carrier('g', tuple(reversed(PATH[:2]))), l.Carrier('g', ((),)))
        self.assertEqual(a.then(c).ancestor((0, 0)), ())

    def test_exact_input_no_float_or_truncation(self):
        l, _, _, _ = self.modules()
        p = l.Pruning(l.Carrier('g', PATH), l.Carrier('g', ((),)))
        for values in ((1, 2), (1.0, 2, 3), (1, 2, 3, 4)):
            with self.assertRaises(ValueError): p.aggregate(values)

    def test_constructive_and_negative_linear_descent(self):
        _, _, _, v = self.modules()
        s = v.sp; old = s.Matrix([1, 0])
        self.assertTrue(v.linear_descent(s.Matrix([[0, 1]]), old))
        self.assertFalse(v.linear_descent(s.Matrix([[1, 0]]), old))
        with self.assertRaises(v.VerificationError):
            v.check_descent(s.Matrix([[1, 0]]), old, True)

    def test_nonlinear_boundary_is_not_linear_test(self):
        _, _, _, v = self.modules()
        t = lambda x: x[0] * x[1]
        self.assertEqual(t((1, 0)), 0)
        self.assertNotEqual(t((0, 1)), t((1, 1)))
        with self.assertRaises((TypeError, ValueError)):
            v.linear_descent(t, v.sp.Matrix([1, 0]))

    def test_actual_old_kernel_witness(self):
        _, _, _, v = self.modules()
        obj = self.instance(); v.verify_instance(obj)
        steps = [z for c in obj['chains'] for z in c['steps'] if z['witness'] is not None]
        self.assertGreater(len(steps), 0)
        self.assertTrue(all(not z['descends'] for z in steps))
        s = v.sp
        L = s.Matrix([[1,-1,0],[-1,2,-1],[0,-1,1]])
        k = s.Matrix([0,-1,1]); phi = s.Matrix([s.Rational(-1,3),s.Rational(-1,3),s.Rational(2,3)])
        self.assertEqual(L*phi,k); self.assertEqual(sum(phi),0)
        self.assertEqual(s.Matrix([[1,0,0],[0,1,1]])*k,s.zeros(2,1))
        self.assertEqual(phi[2]-phi[0],1)

    def test_identity_and_root_zero_dimensional_cases(self):
        v = self.modules()[3]
        result = v.verify_instance(self.instance(((),)))
        self.assertEqual(result['non_descending_steps'],0)
        self.assertEqual(result['chains'],3)

    def test_response_quotient_and_supplied_complement(self):
        v = self.modules()[3]
        obj = self.instance(); v.verify_instance(obj)
        for ch in obj['chains']:
            for st in ch['steps']:
                rep=st['representatives']
                delta=v.sp.Matrix([v.sp.Rational(z) for z in rep['image_shifted']])-v.sp.Matrix([v.sp.Rational(z) for z in rep['image']])
                old=v.sp.Matrix([v.sp.Rational(z) for z in rep['old_image']])
                self.assertEqual(delta,old)

    def test_relabel_and_storage_naturality(self):
        l, _, p, v = self.modules()
        obj = self.instance(STAR)
        renamed = tuple(tuple(11-2*t for t in k) for k in reversed(STAR))
        other = p.build_instance('checker-control', renamed, max_arrows=3)
        self.assertEqual(v.verify_instance(obj),v.verify_instance(other))
        v.check_instance_naturality(obj,other,{k:tuple(11-2*t for t in k) for k in STAR})
        a=l.Carrier('g',STAR); b=l.Carrier('g',tuple(reversed(STAR)))
        self.assertEqual(a.identity,b.identity)

    def test_nonpermutation_coordinate_change(self):
        _, _, _, v = self.modules()
        v.check_basis_changes(self.instance())

    def test_bare_filtration_scaling_and_shear(self):
        s=self.modules()[3].sp
        scale=s.diag(2,1); tau=s.symbols('tau')
        self.assertEqual(s.solve([tau*scale[0,0]-scale[1,1]*tau],[tau]),{tau:0})
        a=s.symbols('a');section=s.Matrix([a,1]);shear=s.Matrix([[1,1],[0,1]])
        self.assertEqual(shear*section-section,s.Matrix([1,0]))

    def test_linear_right_inverse_can_fail_retained_naturality(self):
        v=self.modules()[3];s=v.sp
        P=s.Matrix([[1,1,1]]);biased=s.Matrix([0,1,0]);swap=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
        self.assertEqual(P*biased,s.ones(1,1))
        with self.assertRaises(v.VerificationError) as caught:
            v.check_naturality(swap,biased,s.eye(1),biased)
        MUTATIONS.append({'defect':'linear-but-nonnatural-section','rejected':True,'reason':str(caught.exception)})
        v.check_naturality(swap,s.Matrix([1,0,0]),s.eye(1),s.Matrix([1,0,0]))

    def test_mutated_pushforward_rejected(self):
        self.rejected('wrong-pushforward-coefficient',lambda o:o['prunings'][0]['P'][0].__setitem__(0,'2'))

    def test_mutated_section_rejected(self):
        self.rejected('wrong-section',lambda o:o['prunings'][0]['I'][0].__setitem__(0,'2'))

    def test_mutated_green_rejected(self):
        self.rejected('wrong-green',lambda o:o['carriers'][0]['G'][0].__setitem__(0,'7'))

    def test_foreign_domain_identity_rejected(self):
        self.rejected('illegal-domain-identification',lambda o:o['prunings'][0].__setitem__('genesis','foreign'))

    def test_false_descent_rejected(self):
        def change(o):
            st=next(z for ch in o['chains'] for z in ch['steps'] if z['witness'] is not None)
            st['descends']=True
        self.rejected('false-fixed-target-descent',change)

    def test_corrupted_witness_rejected(self):
        def change(o):
            st=next(z for ch in o['chains'] for z in ch['steps'] if z['witness'] is not None)
            st['witness']['image'][0]='99'
        self.rejected('corrupt-nonzero-image',change)

    def test_missing_check_and_coverage_rejected(self):
        self.rejected('missing-chain',lambda o:o['chains'].pop())
        self.rejected('missing-map-field',lambda o:o['prunings'][0].pop('I'))

    def test_shape_enumerators_agree_without_shared_implementation(self):
        _, e, _, v=self.modules()
        a=e.rooted_shapes(5);b=v.independent_shapes(5)
        self.assertEqual(set(a),set(b))
        self.assertEqual([sum(len(k)==n for k in a.values()) for n in range(1,6)],[1,1,2,4,9])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    out={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'passed':result.wasSuccessful(),'deliberate_defects':MUTATIONS}
    d=HERE/'evidence';d.mkdir(exist_ok=True)
    (d/'TEST_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
