"""Literal boundary fixtures frozen before the routines exist."""
import importlib.util
import unittest

class Mechanisms(unittest.TestCase):
    def test_clearance_root_full_exact(self):
        spec=importlib.util.find_spec('producer')
        self.assertIsNotNone(spec,'CLEARANCE_IMPLEMENTATION_MISSING')
        import producer as p
        self.assertTrue(hasattr(p,'clear_role'),'CLEARANCE_IMPLEMENTATION_MISSING')
        import verifier as v
        tree=(((),()),(),(),());nodes=p.layout(tree)
        # Supports: root P; child0 P; leaves {0},{1}; other roots {0},{1},{2}.
        raw=[23,43,67,3];path=[raw[:]]
        p.clear_role(raw,nodes,1,0,2,path)
        self.assertEqual(raw,[19,43,71,3])
        self.assertEqual(len(path),3)
        for state in path:
            self.assertEqual([j for j,z in enumerate(state) if z&2],[0,1,2,3])
            self.assertEqual(v.profile_check(tree,4,state),[3,2])
        self.assertEqual(len({j for j,z in enumerate(raw) if z&12}),2)

    def test_cover_spare_current_bin(self):
        spec=importlib.util.find_spec('cover')
        self.assertIsNotNone(spec,'COVER_IMPLEMENTATION_MISSING')
        import cover
        actual=cover.reconfigure([{0},{1,2},set(),set()],[{1},{0,2},set(),set()],[2,2,2,0],[0,1,2])
        expected=[[{0},{1,2},set(),set()],[{0,1},{1,2},set(),set()],[{0,1},{2},set(),set()],[{0,1},{0,2},set(),set()],[{1},{0,2},set(),set()]]
        self.assertEqual(actual,expected)
        for step in actual:
            self.assertEqual(set.union(*step),{0,1,2})
            self.assertTrue(all(len(s)<=b for s,b in zip(step,[2,2,2,0])))

if __name__=='__main__':unittest.main(verbosity=2)
