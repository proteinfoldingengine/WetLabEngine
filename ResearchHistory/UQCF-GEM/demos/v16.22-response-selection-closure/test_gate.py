"""Behavior, rejecting certificates and metamorphic controls for v16.22."""
import copy
import importlib
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent

class Tests(unittest.TestCase):
    _certificate = None

    def modules(self):
        for name in ('engine', 'verify'):
            self.assertTrue((HERE / (name + '.py')).is_file(), 'expected wiring RED: missing ' + name)
        return importlib.import_module('engine'), importlib.import_module('verify')

    def cert(self):
        e, _ = self.modules()
        if Tests._certificate is None:
            Tests._certificate = e.produce(3)
        return copy.deepcopy(Tests._certificate)

    def reject(self, mutate):
        _, v = self.modules()
        c = self.cert()
        mutate(c)
        with self.assertRaises(v.VerificationError):
            v.verify(c)

    def test_independent_enumeration(self):
        e, v = self.modules()
        self.assertEqual(e.shapes(5), v.independent_shapes(5))
        self.assertEqual([sum(len(t)==n for t in e.shapes(5)) for n in range(1,6)], [1,1,2,4,9])

    def test_actual_source_and_potential_maps(self):
        e, _ = self.modules()
        P,I,R,H = e.maps((-1,0,1), (-1,0), (0,1))
        self.assertEqual(P.tolist(), [[1,1]])
        self.assertEqual(I.tolist(), [[1],[0]])
        self.assertEqual(R.tolist(), [[1,0]])
        self.assertEqual(H.tolist(), [[1],[1]])
        self.assertEqual(P*I,e.sp.eye(1))
        self.assertEqual(R*H,e.sp.eye(1))

    def test_invalid_parents_and_embeddings_rejected(self):
        e, _ = self.modules()
        for p in ((), (0,), (-1,2,1), (-1,-1), (-1,True)):
            with self.assertRaises(ValueError): e.validate(p)
        for f in ((1,0),(0,0),(0,2),(0,8)):
            with self.assertRaises(ValueError): e.maps((-1,0,1),(-1,0),f)

    def test_root_and_small_universes(self):
        e,v = self.modules()
        for n in (1,2,3):
            r=v.verify(e.produce(n))
            self.assertEqual(r['comparison_dimension'],n-1)
            self.assertEqual(r['inverse_affine_dimension'],0)

    def test_unrestricted_solver_and_complete_verification(self):
        _,v = self.modules()
        r=v.verify(self.cert())
        self.assertEqual(r['comparison_dimension'],2)
        self.assertGreater(r['checks_executed'],0)
        self.assertEqual(r['first_edge_normalized_dimension'],1)

    def test_nonproportional_witness_is_not_new_inverse(self):
        e,v = self.modules()
        c=self.cert(); idx=c['parents'].index([-1,0,1])
        a=v.matrix(c['families']['unit'][idx]); b=v.matrix(c['families']['depth'][idx])
        self.assertEqual(a,e.sp.Matrix([[1,1],[1,2]]))
        self.assertEqual(b,e.sp.Matrix([[1,1],[1,3]]))
        self.assertNotEqual(a,b); self.assertEqual(a[0,0],b[0,0])
        self.assertEqual(e.root_laplacian((-1,0,1))*a,e.sp.eye(2))
        self.assertNotEqual(e.root_laplacian((-1,0,1))*b,e.sp.eye(2))
        v.check_family(c,c['families']['unit']); v.check_family(c,c['families']['depth'])

    def test_false_nullity_rejected(self):
        self.reject(lambda c:c['stats'].__setitem__('nullity',777))

    def test_corrupted_basis_rejected(self):
        def bad(c): c['basis'][0][0]=str(int(c['basis'][0][0])+1)
        self.reject(bad)

    def test_incomplete_basis_rejected(self):
        self.reject(lambda c:c['basis'].pop())

    def test_missing_embedding_rejected(self):
        self.reject(lambda c:c['arrows'].pop())

    def test_missing_constraint_rejected(self):
        self.reject(lambda c:c['rows'].pop())

    def test_wrong_original_inverse_rejected(self):
        def bad(c):
            i=c['parents'].index([-1,0,1]); c['green'][i]=copy.deepcopy(c['families']['depth'][i])
        self.reject(bad)

    def test_wrong_domain_and_scalar_rejected(self):
        self.reject(lambda c:c.__setitem__('genesis','foreign-origin'))
        self.reject(lambda c:c.__setitem__('scalar','unearned-real-physical-source'))
        self.reject(lambda c:c['basis'][0].__setitem__(0,0.25))

    def test_missing_required_field_rejected(self):
        self.reject(lambda c:c.pop('rows'))

    def test_linear_but_label_selected_response_rejected(self):
        _,v=self.modules(); c=self.cert()
        f=copy.deepcopy(c['families']['unit']); i=c['parents'].index([-1,0,0])
        f[i]=[['1','0'],['0','2']]
        with self.assertRaises(v.VerificationError): v.check_family(c,f)

    def test_arbitrary_overall_scale_is_not_fixed_inverse(self):
        _,v=self.modules(); c=self.cert()
        f=[[[str(2*v.rational(z)) for z in row] for row in m] for m in c['families']['unit']]
        v.check_family(c,f)
        c['green']=f
        with self.assertRaises(v.VerificationError): v.verify(c)

    def test_storage_order_and_nullspace_basis_change(self):
        _,v=self.modules(); c=self.cert()
        c['arrows'].reverse(); c['rows'].reverse(); c['basis'].reverse()
        c['basis'][0]=[str(3*v.rational(z)) for z in c['basis'][0]]
        self.assertEqual(v.verify(c)['comparison_dimension'],2)

    def test_nonpermutation_coordinates(self):
        _,v=self.modules(); c=self.cert()
        r=v.check_coordinate_changes(c)
        self.assertGreater(r,0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
