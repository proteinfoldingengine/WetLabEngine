"""Identical fail-closed contract, selected historical or replacement verifier."""
import importlib.util
import json
import os
from pathlib import Path
import unittest
P=Path(__file__).resolve().parent
LEGACY=os.environ.get('V31_LEGACY')=='1'
PATH=(P.parent/'v16.30-interaction-component-closure'/'verifier.py') if LEGACY else P/'verifier.py'
VERSION='16.30' if LEGACY else '16.31'
class Contract(unittest.TestCase):
 def target(self):
  self.assertTrue(PATH.is_file(),'missing replacement verifier')
  s=importlib.util.spec_from_file_location('contract_target',PATH);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_no_sections_is_not_complete(self):
  m=self.target()
  with self.assertRaises(ValueError):m.verify_document({'version':VERSION})
 def test_fabricated_summary_is_not_complete(self):
  m=self.target()
  with self.assertRaises(ValueError):m.verify_document({'version':VERSION,'pairs':-1,'local_edges':999,'cross_parent_edges':5,'cases':[]})
 def test_untyped_empty_edges_are_not_a_certificate(self):
  m=self.target()
  with self.assertRaises(ValueError):m.verify_document({'version':VERSION,'cases':[{'parents':[-1,0,0],'events':[[0,1]],'views':[[0]],'edges':[]}]})
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
 e=P/'evidence';e.mkdir(exist_ok=True)
 (e/('LEGACY_CONTRACT.json' if LEGACY else 'CONTRACT.json')).write_text(json.dumps({'legacy':LEGACY,'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)},indent=2)+'\n')
 raise SystemExit(0 if r.wasSuccessful() else 1)
