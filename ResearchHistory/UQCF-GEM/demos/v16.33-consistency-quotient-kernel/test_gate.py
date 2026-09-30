import unittest,importlib
class T(unittest.TestCase):
 def m(self):return importlib.import_module('producer'),importlib.import_module('verifier')
 def test_invisible_and_visible_controls(self):
  p,v=self.m();a,b=p.controls();v.verify_move(a,True);v.verify_move(b,False)
 def test_fake_unique_minimum_rejected(self):
  p,v=self.m();d=p.small_document();d['classes'][0]['unique_minimum']=True
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_changed_tau_move_rejected_as_invisible(self):
  p,v=self.m();_,b=p.controls()
  with self.assertRaises(ValueError):v.verify_move(b,True)
 def test_complete_small(self):
  p,v=self.m();r=v.verify_document(p.produce(3));self.assertEqual(r['execution_status'],'COMPLETED')
 def test_verifier_rejects_false_connectivity(self):
  p,v=self.m();d=p.produce(3)
  c=next(x for x in d['classes'] if len(x['members'])>1)
  c['connected']=not c['connected']
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_verifier_rejects_omitted_member(self):
  p,v=self.m();d=p.produce(3)
  c=next(x for x in d['classes'] if len(x['members'])>2)
  c['members'].pop()
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_verifier_rejects_false_bulk_counts(self):
  p,v=self.m();d=p.produce(3);d['disconnected_classes']+=1
  with self.assertRaises(ValueError):v.verify_document(d)
 def test_verifier_rejects_missing_class(self):
  p,v=self.m();d=p.produce(3);d['classes'].pop()
  with self.assertRaises(ValueError):v.verify_document(d)
if __name__=='__main__':unittest.main(verbosity=2)
