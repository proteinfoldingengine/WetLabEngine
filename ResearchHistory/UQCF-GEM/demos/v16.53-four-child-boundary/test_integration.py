import importlib.util
import unittest
import verifier as v

L=();B=(L,L);Q=(L,L,L,L)
class Integration(unittest.TestCase):
    def producer(self):
        self.assertIsNotNone(importlib.util.find_spec('producer'),'FOUR_CHILD_JOIN_MISSING')
        import producer as p
        self.assertTrue(callable(getattr(p,'normalize',None)),'FOUR_CHILD_JOIN_MISSING')
        return p
    def check(self,t,q,k,start=None,perm='reversal',mode='inflated'):
        p=self.producer();_,expected,end=v.model(t,q,k,perm,mode)
        if start is None:
            start=p.initial(t,k,q,perm,mode);self.assertEqual(start,expected)
        trace=[];path=p.normalize(start,t,k,q,trace=trace)
        self.assertLessEqual(v.path_check(t,k,q,path,start,end),1)
        self.assertEqual(path[-1],p.canonical(t,k,q))
        self.assertTrue(all(e['parent_exact'] for e in trace if e['kind']=='recursive_call'))
        return p,path,trace
    def test_q2_expand_contract_guard(self):
        _,path,trace=self.check(Q,[2],4,start=[7,25,1,1])
        self.assertTrue(all(v.profile_check(Q,4,s)[0] in (1,2) for s in path))
        self.assertIn('four_root_expand_contract',[e['kind'] for e in trace])
    def test_q3_cover_guard(self):
        _,path,trace=self.check(Q,[3],3,start=[7,9,17])
        self.assertTrue(all(v.profile_check(Q,3,s)[0] in (2,3,4) for s in path))
        self.assertIn('four_root_cover',[e['kind'] for e in trace])
    def test_q4_disjoint_exchange(self):
        self.check(Q,[4],4,start=[17,9,5,3])
    def test_four_child_under_binary_parent(self):
        self.check((Q,L),[2,3],5)
    def test_repeated_four_child(self):
        self.check((Q,L,L,L),[3,3],5)
    def test_recursive_call_requires_exact_parent(self):
        p=self.producer();nodes=p.layout(Q)
        with self.assertRaisesRegex(ValueError,'recursive call requires exact parent'):
            p.require_exact_parent([31,31,31],nodes,3)
    def test_stacked_defect_rejected(self):
        self.producer();t=(B,B);raw=[127,1]
        with self.assertRaisesRegex(v.InterfaceNotPreserved,'total excursion'):
            v.path_check(t,2,[1,2,2],[raw],raw,raw)
    def test_canonical_endpoint(self):
        p=self.producer()
        for t,q,k in [(Q,[2],4),(Q,[3],4),((Q,L),[2,3],5),((Q,L,L,L),[3,3],5)]:
            self.assertEqual(p.canonical(t,k,q),v.model(t,q,k)[2])
    def test_compact_contraction(self):
        p=self.producer();t=(Q,L);q=[2,3];k=6
        state=p.canonical(t,k,q);nodes,target,width=p.data(t,q)
        proper={j for j,z in enumerate(state) if z&~1}
        self.assertEqual(proper,set(range(width[0])))
        self.assertEqual(v.profile_check(t,width[0],state[:width[0]]),q)
    def test_transported_order_equivariance(self):
        p=self.producer();t=(Q,L,L,L);q=[3,3];k=5
        start=p.initial(t,k,q,'cyclic','inflated');path=p.normalize(start,t,k,q)
        permutation=[2,4,1,0,3]
        def relabel(raw):
            out=[0]*k
            for j,z in enumerate(raw):out[permutation[j]]=z
            return out
        self.assertEqual(p.normalize(relabel(start),t,k,q,order=permutation),[relabel(s) for s in path])

if __name__=='__main__':unittest.main(verbosity=2)
