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
