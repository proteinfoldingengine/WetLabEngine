"""Regression contracts for independent Task 1 provenance review."""
import copy
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from verifier import verify_protocol

class ProtocolReview(unittest.TestCase):
    def protocol(self):
        return json.loads((HERE/'protocol.json').read_text())

    def test_valid_frozen_protocol(self):
        self.assertEqual(verify_protocol(self.protocol(), HERE), [])

    def test_missing_preregistration_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(self.protocol(), HERE))

    def test_changed_plan_commit_rejected_without_binding(self):
        p = self.protocol()
        p['approved_plan_commit'] = '0'*40
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(p, HERE))

    def test_removed_inventories_rejected_without_binding(self):
        p = self.protocol()
        p['proofs'] = {}
        p['reviews'] = {}
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(verify_protocol(p, HERE))

    def test_nonimmutable_binding_rejected(self):
        with patch.dict(os.environ, {'PREREGISTRATION_SHA':'HEAD'}):
            self.assertTrue(verify_protocol(self.protocol(), HERE))

from universe import case,core,parts
from mechanisms import produce
from verifier import verify_record

class MechanismReview(unittest.TestCase):
    def cyclic(self):
        rows=core(parts((4,3,2)),3,True)
        return case('M5','balance',9,[3]*len(rows),6,rows,{},form='cyclic',h=3,sizes=[4,3,2],extras='P',d=0)

    def test_canonical_root_order_includes_duplicates(self):
        rows=core(parts((3,4)),3)+[list(range(7))]
        c=case('M5','balance',7,[3]*len(rows),3,rows,{},form='module',h=3,sizes=[3,4],extras='P',d=1)
        r=produce(c)
        self.assertEqual(r['path'][-1],sorted(r['path'][-1]))

    def test_false_star_slots_rejected(self):
        c=self.cyclic();r=produce(c);r['facts']['balancing'][0]['slots']=[]
        self.assertTrue(verify_record(c,r))

    def test_false_layer_peak_rejected(self):
        c=case('M1','layers',4,[1]*5,3,[[0],[1],[2],[3],[0,1]],{'peak':4})
        r=produce(c);r['facts']['layers'][0]['peak']=999
        self.assertTrue(verify_record(c,r))

    def test_unchecked_clone_preliminary_tail_rejected(self):
        p=json.loads((HERE/'protocol.json').read_text())
        c=case('M4','clone_sequence',6,[2]*4,3,[[0,1],[0,2],[1,3],[4,5]],{'operations':[[0,1]],'shift':0},tag='empty',source='PROSPECTIVE_VALIDATION_PLAN.md',source_sha256=p['approved_plan_sha256'])
        r=produce(c);r['facts']['preliminary_path'].append(copy.deepcopy(r['facts']['preliminary_path'][-1]))
        self.assertTrue(verify_record(c,r))

    def test_false_old_owner_category_rejected(self):
        c=case('M2','element',4,[0]*3,None,[[0],[1,2],[3]],{'target':[[1],[0,2],[3]]},capacities=[2,2,1],representation='blocks')
        r=produce(c);event=next(e for e in r['events'] if e['kind']=='element_buffer');event['old_owner']=2
        self.assertTrue(verify_record(c,r))

    def test_substituted_prescribed_cycle_pairing_rejected(self):
        rows=[[0,2],[1,3],[0,1,2,3]];target=[[1,3],[0,2],[0,1,2,3]]
        c=case('M2','forced_cycle',5,[2,2,4],None,rows,{'target':target,'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4})
        other=case('M2','degree2',5,[2,2,4],None,rows,{'target':target})
        r=produce(other);r['identity']=c['identity']
        self.assertTrue(verify_record(c,r))

    def test_direct_vacancy_lexicographic_pair(self):
        c=case('M2','degree2',4,[1,1,1],None,[[3],[0],[2]],{'target':[[2],[1],[2]]})
        r=produce(c)
        self.assertEqual((r['events'][0]['source'],r['events'][0]['target']),(0,1))

from model import state,plain,tau,clip
from universe import guard_case

class FollowupReview(unittest.TestCase):
    def test_module_pair_omitted_balancing_rejected(self):
        left,right=core(parts((3,5)),3),core(parts((4,4)),3)
        c=case('M5','module_pair',8,[3]*11,4,left,{'target':right+[right[0]]*3},h=3,sizes=[3,5],form='module')
        r=produce(c);r['facts']['balancing']=[]
        self.assertTrue(verify_record(c,r))

    def test_negative_guard_boundary_rejected(self):
        c=guard_case(2,3,6,1,1);r=produce(c)
        r['facts']['coexist_end']-=len(r['facts']['preliminary_path'])
        self.assertTrue(verify_record(c,r))

    def test_unprescribed_split_permutation_detour_rejected(self):
        c=case('M7','split_path',5,[1]*4,3,[[0],[0],[1],[2]],{},groups=[0,0,1,2])
        r=produce(c);f=r['facts'];left=f['left_path'];left.extend(copy.deepcopy([left[-2],left[-1]]))
        preliminary=left+list(reversed(f['right_path']))[1:]
        final,layers=clip([state(v) for v in preliminary],3)
        f['preliminary_path']=preliminary;f['layers']=layers
        f['active_labels']=[sorted(set().union(*v)) for v in final]
        r['path']=[plain(v) for v in final];r['tau']=[tau(v) for v in final]
        self.assertTrue(verify_record(c,r))

    def test_missing_native_clearance_trace_rejected(self):
        c=guard_case(2,3,6,1,1,'M9');r=produce(c);r['facts']['clearance']=[]
        self.assertTrue(verify_record(c,r))

    def test_unprescribed_cycle_rotation_rejected(self):
        from model import Path
        rows=[[0,2],[1,3],[0,1,2,3]];target=[[1,3],[0,2],[0,1,2,3]]
        c=case('M2','forced_cycle',5,[2,2,4],None,rows,{'target':target,'edges':[[0,1,0],[1,2,1],[2,3,0],[3,0,1]],'buffer':4})
        r=produce(c);event=r['events'][0];edges=event['edges'][1:]+event['edges'][:1];route=Path(rows)
        def move(i,x,y):route.toggle(i,y,True);route.toggle(i,x,False)
        x,y,i=edges[0];move(i,x,4)
        for a,b,j in reversed(edges[1:]):move(j,a,b)
        move(i,4,y)
        event['edges']=edges;r['path']=[plain(v) for v in route.vertices]
        self.assertTrue(verify_record(c,r))

from test_campaign import Campaign
