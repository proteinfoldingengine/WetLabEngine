import importlib.util, unittest, numpy as np
m=None
if importlib.util.find_spec('pretime_gravity_canary'):
    import pretime_gravity_canary as m

class CanaryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(m, 'pre-time gravity canary implementation absent')

    def test_chain_complex_closes_exactly(self):
        c=m.torus_complex(7)
        self.assertLess(np.linalg.norm(c.B1@c.B2),1e-12)

    def test_single_incidence_defect_is_local_and_neutral(self):
        c=m.torus_complex(7)
        q,delta=m.incidence_defect(c,face=(0,0),edge_slot='bottom',amplitude=1.0)
        self.assertAlmostEqual(float(q.sum()),0.0,places=12)
        self.assertEqual(np.count_nonzero(np.abs(q)>1e-12),2)
        self.assertEqual(np.count_nonzero(np.abs(delta)>1e-12),1)

    def test_closed_face_multiplicity_is_null(self):
        c=m.torus_complex(7)
        q=m.closed_face_control(c,(0,0),amplitude=3.0)
        self.assertLess(np.linalg.norm(q),1e-12)
        r=m.compatibility_response(c.B1,q)
        self.assertLess(np.linalg.norm(r.current),1e-12)

    def test_response_restores_global_compatibility(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        r=m.compatibility_response(c.B1,q)
        self.assertLess(np.linalg.norm(c.B1@r.current+q),1e-11)
        self.assertLess(abs(float(r.current@c.B2[:,0])),1e-11)

    def test_response_is_global_not_only_source_edge(self):
        c=m.torus_complex(7);q,delta=m.incidence_defect(c,(0,0),'bottom',1.0)
        r=m.compatibility_response(c.B1,q)
        source_edge=int(np.flatnonzero(delta)[0])
        nonzero=np.flatnonzero(np.abs(r.current)>1e-10)
        self.assertGreater(len(nonzero),c.B1.shape[0])
        self.assertTrue(any(e!=source_edge for e in nonzero))

    def test_microscopic_closed_face_shift_same_source_same_response(self):
        c=m.torus_complex(7);q,d=m.incidence_defect(c,(0,0),'bottom',1.0)
        d2=d+2.75*c.B2[:,c.face_index[(3,4)]]
        q2=c.B1@d2
        np.testing.assert_allclose(q2,q,atol=1e-12)
        np.testing.assert_allclose(m.compatibility_response(c.B1,q2).current,
                                   m.compatibility_response(c.B1,q).current,atol=1e-11)

    def test_superposition_is_exact(self):
        c=m.torus_complex(7)
        q1,_=m.incidence_defect(c,(0,0),'bottom',.7)
        q2,_=m.incidence_defect(c,(3,3),'right',-.4)
        j=m.compatibility_response(c.B1,q1+q2).current
        expected=m.compatibility_response(c.B1,q1).current+m.compatibility_response(c.B1,q2).current
        np.testing.assert_allclose(j,expected,atol=1e-11)

    def test_permutation_covariance(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        r=m.compatibility_response(c.B1,q)
        rng=np.random.default_rng(140926)
        pv=rng.permutation(c.B1.shape[0]);pe=rng.permutation(c.B1.shape[1])
        B=c.B1[pv][:,pe];qp=q[pv]
        rp=m.compatibility_response(B,qp)
        expected=r.current[pe]
        np.testing.assert_allclose(rp.current,expected,atol=1e-10)

    def test_remote_face_scalar_circulation_is_zero(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        j=m.compatibility_response(c.B1,q).current
        far=m.farthest_face(c,(0,0))
        self.assertGreater(m.torus_face_distance(c,(0,0),far),1)
        self.assertLess(abs(m.face_circulation(c,j,far)),1e-11)

    def test_noncommuting_remote_holonomy_lives_while_commuting_control_dies(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        j=m.compatibility_response(c.B1,q).current
        far=m.farthest_face(c,(0,0))
        h=m.face_holonomy(c,j,far,epsilon=.2,commuting=False)
        hc=m.face_holonomy(c,j,far,epsilon=.2,commuting=True)
        self.assertGreater(m.holonomy_defect(h),1e-8)
        self.assertLess(m.holonomy_defect(hc),1e-10)

    def test_remote_face_holonomy_has_observed_linear_small_parameter_scaling(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        j=m.compatibility_response(c.B1,q).current
        far=m.farthest_face(c,(0,0))
        a=m.holonomy_defect(m.face_holonomy(c,j,far,epsilon=.01,commuting=False))
        b=m.holonomy_defect(m.face_holonomy(c,j,far,epsilon=.02,commuting=False))
        self.assertGreater(a,1e-12)
        self.assertAlmostEqual(b/a,2.0,delta=.08)

    def test_group_commutator_is_quadratic_nonabelian_control(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        j=m.compatibility_response(c.B1,q).current
        far=m.farthest_face(c,(0,0))
        a=m.holonomy_defect(m.response_commutator_holonomy(c,j,far,epsilon=.01,commuting=False))
        b=m.holonomy_defect(m.response_commutator_holonomy(c,j,far,epsilon=.02,commuting=False))
        z=m.holonomy_defect(m.response_commutator_holonomy(c,j,far,epsilon=.2,commuting=True))
        self.assertGreater(a,1e-12)
        self.assertAlmostEqual(b/a,4.0,delta=.15)
        self.assertLess(z,1e-10)

    def test_disconnected_component_gets_no_response(self):
        c=m.torus_complex(5);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        B=m.block_incidence(c.B1,c.B1)
        qq=np.concatenate([q,np.zeros_like(q)])
        j=m.compatibility_response(B,qq).current
        self.assertLess(np.linalg.norm(j[c.B1.shape[1]:]),1e-11)

    def test_remote_shell_signal_survives_all_four_incidence_orientations(self):
        c=m.torus_complex(7)
        for slot in ('bottom','right','top','left'):
            q,_=m.incidence_defect(c,(0,0),slot,1.0)
            j=m.compatibility_response(c.B1,q).current
            row=m.remote_shell_summary(c,j,(0,0),epsilon=.2)
            self.assertGreater(row['face_count'],20)
            self.assertGreater(row['noncommuting_rms'],1e-4)
            self.assertGreater(row['commutator_rms'],1e-6)
            self.assertLess(row['commuting_rms'],1e-10)

    def test_translation_equivalent_sources_have_same_aggregate_response(self):
        c=m.torus_complex(7);rows=[]
        for face in ((0,0),(1,2),(3,4)):
            q,_=m.incidence_defect(c,face,'bottom',1.0)
            r=m.compatibility_response(c.B1,q)
            rows.append((np.linalg.norm(r.current),m.remote_shell_summary(c,r.current,face)['noncommuting_rms']))
        for row in rows[1:]:np.testing.assert_allclose(row,rows[0],atol=1e-11)

    def test_source_amplitude_scaling_is_linear_for_response_quadratic_for_commutator(self):
        c=m.torus_complex(7);vals=[]
        for amp in (.5,1.0):
            q,_=m.incidence_defect(c,(0,0),'bottom',amp);j=m.compatibility_response(c.B1,q).current
            vals.append((np.linalg.norm(j),m.remote_shell_summary(c,j,(0,0),epsilon=.05)['commutator_rms']))
        self.assertAlmostEqual(vals[1][0]/vals[0][0],2.0,delta=1e-10)
        self.assertAlmostEqual(vals[1][1]/vals[0][1],4.0,delta=.05)

    def test_no_pruning_clock_or_gravity_fit_is_used(self):
        a=m.audit()
        self.assertFalse(a['uses_pruning'])
        self.assertFalse(a['uses_entropy'])
        self.assertFalse(a['uses_physical_time'])
        self.assertFalse(a['fits_newton_or_gr'])
        self.assertFalse(a['physical_gravity_derived'])
        self.assertEqual(a['candidate_law_status'],'SUPPLIED_PRETIME_HIGHER_INCIDENCE_CANARY')

    def test_cycle_freedom_changes_remote_holonomy_without_changing_closure(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        r=m.compatibility_response(c.B1,q);face=m.farthest_face(c,(0,0))
        shifted=r.current+0.25*c.B2[:,c.face_index[face]]
        self.assertLess(np.linalg.norm(c.B1@shifted+q),1e-10)
        h0=m.holonomy_defect(m.face_holonomy(c,r.current,face,.2,False))
        h1=m.holonomy_defect(m.face_holonomy(c,shifted,face,.2,False))
        self.assertGreater(abs(h1-h0),1e-4)

    def test_edge_inner_product_choice_changes_canonical_representative(self):
        c=m.torus_complex(7);q,_=m.incidence_defect(c,(0,0),'bottom',1.0)
        base=m.weighted_response(c.B1,q,np.ones(c.B1.shape[1])).current
        weights=np.linspace(.75,1.25,c.B1.shape[1])
        alt=m.weighted_response(c.B1,q,weights).current
        self.assertLess(np.linalg.norm(c.B1@alt+q),1e-10)
        self.assertGreater(np.linalg.norm(base-alt),1e-3)

    def test_canary_reports_signal_but_refuses_physical_gravity_certification(self):
        a=m.audit()
        self.assertTrue(a['global_compatibility_signal'])
        self.assertFalse(a['gravity_canary_certified'])
        self.assertFalse(a['canary_positive'])
        self.assertGreater(a['response_nonuniqueness_dimension'],0)
        self.assertEqual(a['selector_status'],'UNRESOLVED_CYCLE_COMPONENT_AND_EDGE_INNER_PRODUCT')
        self.assertLess(a['baseline_chain_error'],1e-12)
        self.assertLess(a['closure_residual'],1e-10)
        self.assertGreater(a['global_response_fraction'],.4)
        self.assertGreater(a['remote_noncommuting_holonomy'],1e-8)
        self.assertLess(a['remote_commuting_holonomy'],1e-10)
        self.assertLess(a['closed_face_control_response'],1e-12)
        self.assertLess(a['covariance_error'],1e-10)
        self.assertGreater(a['cycle_shift_holonomy_change'],1e-4)
        self.assertGreater(a['weighted_response_difference'],1e-3)

if __name__=='__main__': unittest.main(verbosity=2)
