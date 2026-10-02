"""Proof-mechanism paths and deliberately invalid certificates."""
import copy
import json
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from mechanisms import produce
from universe import case, guard_case, core, parts
from verifier import verify_record

def simple_case():
    return case('M1','packet',4,[1]*5,4,[[0],[1],[2],[3],[0,1]],[0,1])

def reference():
    c=simple_case()
    # Two roots containing the original source role 1 acquire role 0.
    return {'identity':c['identity'],'status':'PASS',
            'path':[[[0],[1],[2],[3],[0,1]],[[0],[0,1],[2],[3],[0,1]]],
            'tau':[4,3], 'facts':{'source_rows':[1,4]},'events':[]}

class Task2(unittest.TestCase):
    def require(self,c,status='PASS'):
        r=produce(c)
        self.assertEqual(r.get('status'),status)
        self.assertEqual(verify_record(c,r),[])
        return r

    def test_original_packet_membership(self):
        c=case('M1','double_packet',4,[1]*5,4,[[0],[1],[2],[3],[0,1]],[[0,1],[2,0]])
        self.require(c)

    def test_both_maximum_layer_neighbors(self):
        roots=[[0],[1],[2],[3],[0,1]]
        for edge,right in (([4,2],[2,3]),([0,1],None)):
            self.require(case('M1','neighbor',4,[1]*5,4,roots,
                              {'edge':edge,'left':[0,1],'right':right,'reverse':False}))

    def test_repeated_layer_removal(self):
        self.require(case('M1','layers',6,[1]*7,3,[[x] for x in range(6)]+[[0,1]],{'peak':6}))

    def test_repeated_color_cycle(self):
        self.require(case('M2','forced_cycle',5,[2,2,4],None,[[0,2],[1,3],[0,1,2,3]],
                          {'target':[[1,3],[0,2],[0,1,2,3]],
                           'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4}))

    def test_element_old_owner_buffer(self):
        self.require(case('M2','element',4,[0]*3,None,[[0],[1,2],[3]],
                          {'target':[[1],[0,2],[3]]},capacities=[2,2,1],representation='blocks'))

    def test_saturated_swap(self):
        self.require(case('M3','saturated',4,[2,1,1,4],3,[[0,1],[2],[3],[0,1,2,3]],
                          {'target':[[0,2],[1],[3],[0,1,2,3]]},hubs=1))

    def test_empty_contraction(self):
        protocol=json.loads((HERE/'protocol.json').read_text())
        self.require(case('M4','clone_sequence',6,[2]*4,3,[[0,1],[0,2],[1,3],[4,5]],
                          {'operations':[[0,1]],'shift':0},tag='empty',
                          source='PROSPECTIVE_VALIDATION_PLAN.md',
                          source_sha256=protocol['approved_plan_sha256']))

    def test_cyclic_exceptional_move(self):
        rows=core(parts((4,3,2)),3,True)
        self.require(case('M5','balance',9,[3]*len(rows),6,rows,{},
                          form='cyclic',h=3,sizes=[4,3,2],extras='P',d=0))

    def test_guard_transfer(self):
        self.require(guard_case(3,4,20,1,1))

    def test_slot_boundary_refusal(self):
        self.require(guard_case(3,4,19,1,1),'REFUSED')

    def test_valid_reference(self):
        self.assertEqual(verify_record(simple_case(),reference()),[])

    def test_wrong_tau_rejected(self):
        r=reference();r['tau'][-1]=4
        self.assertTrue(verify_record(simple_case(),r))

    def test_wrong_floor_rejected(self):
        r=reference();r['path'][1][0]=[]
        self.assertTrue(verify_record(simple_case(),r))

    def test_external_label_rejected(self):
        r=reference();r['path'][1][1]=[0,1,4]
        self.assertTrue(verify_record(simple_case(),r))

    def test_simultaneous_move_rejected(self):
        r=reference();r['path'][1][2]=[0,2]
        self.assertTrue(verify_record(simple_case(),r))

    def test_false_packet_source_rejected(self):
        r=reference();r['facts']['source_rows']=[0,1,4]
        self.assertTrue(verify_record(simple_case(),r))

    def test_substituted_identity_rejected(self):
        r=reference();r['identity']=copy.deepcopy(r['identity']);r['identity'][3]=[1,0]
        self.assertTrue(verify_record(simple_case(),r))

    def test_false_coverage_rejected(self):
        r=reference();r['events']=[{'kind':'buffered_cycle','source':'fabricated'}]
        self.assertTrue(verify_record(simple_case(),r))

if __name__=='__main__':unittest.main(verbosity=2)

class SpecificRejections(unittest.TestCase):
    def test_empty_contracted_edge_cannot_be_finite(self):
        protocol=json.loads((HERE/'protocol.json').read_text())
        c=case('M4','clone_sequence',6,[2]*4,3,[[0,1],[0,2],[1,3],[4,5]],{'operations':[[0,1]],'shift':0},tag='empty',source='PROSPECTIVE_VALIDATION_PLAN.md',source_sha256=protocol['approved_plan_sha256'])
        r=produce(c);r['facts']['clones'][0]['contraction']=3
        self.assertTrue(verify_record(c,r))

    def test_below_floor_cycle_buffer_rejected(self):
        c=case('M2','forced_cycle',5,[2,2,4],None,[[0,2],[1,3],[0,1,2,3]],{'target':[[1,3],[0,2],[0,1,2,3]],'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4})
        r=produce(c);r['path'][1][0]=[2]
        self.assertTrue(verify_record(c,r))
