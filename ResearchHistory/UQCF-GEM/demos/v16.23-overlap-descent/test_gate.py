"""Behavioral and deliberate-defect tests, frozen before implementation."""
import copy
import importlib
import json
from pathlib import Path
import unittest
from fractions import Fraction as F

HERE=Path(__file__).resolve().parent
REJECTED=[]

class Tests(unittest.TestCase):
    def modules(self):
        for name in ('engine','verify'):
            self.assertTrue((HERE/(name+'.py')).is_file(), 'expected wiring RED: missing '+name)
        return importlib.import_module('engine'),importlib.import_module('verify')

    def data(self):
        e,_=self.modules()
        if not hasattr(Tests,'cached'):
            Tests.cached=e.case((-1,0,0),'checker-star')
        return copy.deepcopy(Tests.cached)

    def rejection(self,name,change):
        _,v=self.modules();d=self.data();change(d)
        with self.assertRaises(ValueError) as cm:v.verify_case(d)
        REJECTED.append({'defect':name,'rejected':True,'reason':str(cm.exception)})

    def test_actual_signed_and_positive_pair_witness(self):
        e,_=self.modules();p=(-1,0,0)
        self.assertEqual(e.glue(p,(0,1),(0,2),(0,1),(0,1)),(F(-1),F(1),F(1)))
        with self.assertRaisesRegex(ValueError,'nonnegative'):
            e.glue(p,(0,1),(0,2),(0,1),(0,1),positive=True)

    def test_pairwise_positive_is_not_global(self):
        e,_=self.modules();p=(-1,0,0,0);ys=[(0,1),(0,2),(0,3)];xs=[(1,1)]*3
        for i in range(3):
            for j in range(i):self.assertEqual(e.glue(p,ys[i],ys[j],xs[i],xs[j],positive=True),(0,1,1))
        self.assertEqual(e.glue_many(p,ys,xs),(-1,1,1,1))
        with self.assertRaisesRegex(ValueError,'nonnegative'):e.glue_many(p,ys,xs,positive=True)

    def test_feasible_nonnegative_control(self):
        e,_=self.modules();self.assertEqual(e.glue((-1,0,0),(0,1),(0,2),(1,1),(1,1),positive=True),(0,1,1))

    def test_identity_root_and_repeated_views(self):
        e,_=self.modules();p=(-1,0,1)
        self.assertEqual(e.glue(p,(0,),(0,),(3,),(3,)),(3,))
        self.assertEqual(e.glue_many(p,[(0,1)]*3,[(2,3)]*3),(2,3))
        self.assertEqual(e.glue(p,(0,1),(0,1,2),(1,2),(1,1,1)),(1,1,1))

    def test_incompatible_overlap_rejected(self):
        e,_=self.modules()
        with self.assertRaisesRegex(ValueError,'compatible'):e.glue((-1,0,0),(0,1),(0,2),(0,1),(0,2))

    def test_source_shift_is_not_potential_gauge(self):
        e,_=self.modules();p=(-1,0,0)
        x=e.glue(p,(0,1),(0,2),(0,1),(0,1))
        self.assertNotEqual(e.push(p,(0,1,2),(0,1),tuple(a+1 for a in x)),(0,1))

    def test_response_representative_independence(self):
        e,_=self.modules();p=(-1,0,0)
        a=e.glue_response(p,(0,1),(0,2),(4,6),(-3,2))
        b=e.glue_response(p,(0,1),(0,2),(11,13),(5,10))
        self.assertEqual(a,(0,2,5));self.assertEqual(a,b)

    def test_nonnegative_false_input_rejected(self):
        e,_=self.modules()
        with self.assertRaisesRegex(ValueError,'nonnegative'):e.glue((-1,0),(0,1),(0,1),(-1,2),(-1,2),positive=True)

    def test_invalid_parent_and_retained_inputs(self):
        e,_=self.modules()
        for p in [(),(-1,True),(-1,0.0),(-1,2,1),(-1,7),(-1,-1)]:
            with self.subTest(p=p):
                with self.assertRaises(ValueError):e.validate(p)
        for keep in [(1,), (0,0), (0,2), (0,9), (0,True)]:
            with self.subTest(keep=keep):
                with self.assertRaises(ValueError):e.retained((-1,0,1),keep)

    def test_exact_scalars_and_lengths(self):
        e,_=self.modules()
        for vals in [(0.0,1),(False,1),(1,),('nan','1')]:
            with self.assertRaises(ValueError):e.glue((-1,0),(0,1),(0,1),vals,vals)
        vals=(F(1,10**30),F(-1,10**30))
        self.assertEqual(e.glue((-1,0),(0,1),(0,1),vals,vals),vals)

    def test_complete_small_certificate(self):
        _,v=self.modules();r=v.verify_case(self.data());self.assertGreater(r['pairs'],0);self.assertGreater(r['triples'],0)

    def test_changed_lineage_storage(self):
        e,v=self.modules()
        original=e.case((-1,0,1,1),'relabelling-test')
        changed=e.case((-1,3,3,0),'relabelling-test',reverse=True)
        a=v.verify_case(original);b=v.verify_case(changed)
        for key in ('pairs','triples','positive_compatible','positive_gluable','positive_obstructed'):
            self.assertEqual(a[key],b[key])

    def test_wrong_joint_readout_rejected(self):
        self.rejection('wrong-pushforward',lambda d:d['pairs'][0]['source']['A']['data'].__setitem__(0,'2'))

    def test_wrong_gluer_on_compatible_data_rejected(self):
        self.rejection('wrong-gluer',lambda d:d['pairs'][0]['source']['B']['data'].__setitem__(0,'9'))

    def test_wrong_overlap_rejected(self):
        self.rejection('wrong-overlap',lambda d:d['pairs'][-1].__setitem__('overlap',0))

    def test_foreign_origin_rejected(self):
        self.rejection('foreign-origin',lambda d:d['pairs'][0].__setitem__('genesis','foreign'))

    def test_false_positive_feasibility_rejected(self):
        def change(d):
            r=next(x for x in d['pairs'] if x['positive']['obstructed'])
            r['positive']['gluable']+=1;r['positive']['obstructed']-=1
        self.rejection('false-nonnegative-feasibility',change)

    def test_corrupt_negative_witness_rejected(self):
        def change(d):
            r=next(x for x in d['pairs'] if x['positive']['obstructed'])
            r['positive']['witness']['global'][0]='0'
        self.rejection('corrupt-negative-witness',change)

    def test_missing_coverage_rejected(self):
        self.rejection('missing-pair',lambda d:d['pairs'].pop())
        self.rejection('missing-triple',lambda d:d['triples'].pop())

    def test_missing_field_and_inexact_matrix_rejected(self):
        self.rejection('missing-required-map',lambda d:d['pairs'][0]['source'].pop('D'))
        self.rejection('inexact-coefficient',lambda d:d['pairs'][0]['source']['A']['data'].__setitem__(0,1.0))

    def test_off_domain_gluer_change_is_harmless(self):
        _,v=self.modules();d=self.data();r=next(x for x in d['pairs'] if x['source']['D']['rows']>0)
        B=v.decode(r['source']['B']);D=v.decode(r['source']['D']);K=v.sp.ones(B.rows,D.rows)
        r['source']['B']=v.encode(B+K*D)
        v.verify_case(d)

    def test_linear_but_nonnatural_section_rejected(self):
        _,v=self.modules();s=v.sp
        P=s.Matrix([[1,1,1]]);section=s.Matrix([0,1,0]);swap=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
        self.assertEqual(P*section,s.eye(1))
        with self.assertRaisesRegex(ValueError,'naturality'):
            v.check_section(P,section,swap,s.eye(1))
        v.check_section(P,s.Matrix([1,0,0]),swap,s.eye(1))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    out=HERE/'evidence';out.mkdir(exist_ok=True)
    (out/'TEST_RECEIPT.json').write_text(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'rejections':REJECTED},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
