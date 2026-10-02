"""Palette/reserve transformations and the whole native budget."""
import copy
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from universe import case,guard_case
from mechanisms import produce
from verifier import verify_record,verify_nested

class Task3(unittest.TestCase):
    def require(self,c,status='PASS'):
        record=produce(c)
        self.assertEqual(record.get('status'),status)
        self.assertEqual(verify_record(c,record),[])
        return record

    def test_palette_path_uses_exact_endpoints(self):
        self.require(case('M7','split_path',5,[1]*4,3,[[0],[0],[1],[2]],{},groups=[0,0,1,2]))

    def test_palette_boundary_refusal(self):
        r=self.require(case('M7','split_path',3,[1]*4,3,[[0],[0],[1],[2]],{},groups=[0,0,1,2]),'REFUSED')
        self.assertNotIn('barrier',r)

    def test_every_first_split_contract(self):
        self.require(case('M7','split_local',5,[1]*4,3,[[0],[0],[1],[2]],[0,0,3],groups=[0,0,1,2]))

    def test_reserve_reuse_and_fixed_endpoints(self):
        self.require(case('M8','support',25,[2]*4,3,[[0,1],[1,2],[0,2],[3,4]],
                          {'label':0,'length':11}))

    def test_native_parent_path_and_clearance(self):
        self.require(guard_case(2,3,6,1,1,'M9'))

    def test_global_budget_rejects_second_unit(self):
        nodes=[[1,4,7],[2,3],[],[],[5,6],[],[],[8,9],[],[]]
        targets={0:3,1:2,4:2,7:2}
        initial=[[0,1,2,3,4,5],[0,1],[0],[1],[2,3],[2],[3],[4,5],[4],[5]]
        parent=copy.deepcopy(initial);parent[1]=[0,1,2]
        two=copy.deepcopy(parent);two[3]=[0,1]
        self.assertEqual(verify_nested([initial,parent],nodes,targets,6),[])
        self.assertTrue(verify_nested([initial,parent,two],nodes,targets,6))

    def test_non_nested_state_rejected(self):
        nodes=[[1,2,3],[],[],[]];targets={0:3}
        self.assertTrue(verify_nested([[[0,1,2],[0],[1],[3]]],nodes,targets,3))

if __name__=='__main__':unittest.main(verbosity=2)
