import unittest
from unittest.mock import patch
import producer as p
import verifier as v

class Lifting(unittest.TestCase):
    def test_zero_capacity_child(self):
        import cover
        a=[set(),{0,1},{1,2},{0,2}];b=[set(),{1,2},{0,2},{0,1}]
        path=cover.reconfigure(a,b,[0,2,2,2],[0,1,2])
        self.assertEqual(path[0],a);self.assertEqual(path[-1],b)
        self.assertTrue(all(not step[0] for step in path))
    def test_root_full_lift_and_leaf(self):
        t=(((),()),(),(),());state=[23,43,67,3]
        roots=[{0,1,2,3},{0},{1},{2}];target=[{1,2,3},{0},{1},{2}]
        path=p.lift_root_path(state,t,[3,2],[roots,target],[0,1,2,3],[])
        self.assertEqual(path,[[23,43,67,3],[23,43,71,3],[19,43,71,3],[17,43,71,3]])
        for raw in path:self.assertEqual(v.profile_check(t,4,raw),[3,2])
        leafroots=[{0,1},{0},{1},{2}];leafend=[{1},{0},{1},{2}]
        initial=v.raw_roots(3,leafroots)
        path=p.lift_root_path(initial,((),(),(),()),[3],[leafroots,leafend],[0,1,2],[])
        self.assertEqual(len(path),2);self.assertEqual(path[-1],v.raw_roots(3,leafend))
    def test_deletion_at_minimum_rejected(self):
        t=(((),()),(),(),());state=[23,41,65]
        roots=[{0,1},{0},{1},{2}];target=[{1},{0},{1},{2}]
        # Correctly nested exact interior with root size two.
        state=[23,43,65]
        with self.assertRaises(p.ConstructionFailure):p.lift_root_path(state,t,[3,2],[roots,target],[0,1,2],[])
    def test_invalid_root_step_rejected(self):
        roots=[{0},{0},{1},{2}];end=[{0,1},{0,2},{1},{2}]
        with self.assertRaises(p.ConstructionFailure):p.lift_root_path([7,9,17],((),(),(),()),[3],[roots,end],[0,1,2],[])
    def test_destination_properly_occupied_rejected(self):
        state=[23,43,67,3]
        with self.assertRaisesRegex(ValueError,'proper descendants'):
            p.clear_role(state,p.layout((((),()),(),(),())),1,0,1,[state[:]])
    def test_partial_clearance_retained(self):
        tree=(((),()),(),(),());start=[23,43,67,3]
        roots=[{0,1,2,3},{0},{1},{2}];target=[{1,2,3},{0},{1},{2}]
        original=p.clear_role;emitted=[]
        def fail(current,nodes,child,x,y,path):
            original(current,nodes,child,x,y,path);emitted[:]=[s[:] for s in path]
            raise ValueError('INJECTED_AFTER_REAL_CLEARANCE')
        with patch.object(p,'clear_role',side_effect=fail):
            with self.assertRaises(p.ConstructionFailure) as caught:
                p.lift_root_path(start,tree,[3,2],[roots,target],list(range(4)),[])
        self.assertGreater(len(emitted),1)
        self.assertEqual(caught.exception.path,emitted)
        self.assertIsInstance(caught.exception.original,ValueError)

if __name__=='__main__':unittest.main(verbosity=2)
