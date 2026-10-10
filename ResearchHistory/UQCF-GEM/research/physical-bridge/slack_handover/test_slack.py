import copy,unittest,producer as p,independent as v
class SlackContracts(unittest.TestCase):
 def test_source(self):self.assertEqual(p.source(3),(3,5,9,14,16))
 def test_positive(self):self.assertEqual(len(p.release(3,0,[1])),4)
 def test_first_vacancy(self):self.assertTrue(p.route(p.source(3),p.release(3,0,[1]))[-1][1]&4==0)
 def test_capacity(self):self.assertEqual(p.capacity(3,1)['minimum'],4)
 def test_one_slack(self):self.assertEqual(p.capacity(3,2)['minimum'],5)
 def test_no_slack(self):self.assertEqual(p.capacity(3,3)['minimum'],5)
 def test_bfs_allows_upper_four(self):self.assertEqual(p.tau((3,5,9,18,12,32)),4);self.assertTrue(p.safe((3,5,9,18,12,32),4,1));p.build(4)
 def test_bfs_minimum(self):self.assertEqual(p.bfs(3,1)['first_vacancy'],4)
 def test_fresh_label_rejected(self):
  s=(35,5,9,14,16);self.assertFalse(p.safe(s,3,1));self.assertFalse(v.gate(v.supports(s),3,1))
 def test_bad_domination(self):self.assertFalse(p.safe((3,7,9,14,16),3,1))
 def test_hidden_witness(self):self.assertEqual(p.fulltau((3,7,9,14,16),20),2)
 def test_source_hidden(self):self.assertEqual(p.fulltau(p.source(3),20),3)
class CertificateContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=p.build(3)
 def test_independent(self):v.verify(self.c,3)
 def reject(self,key):
  c=copy.deepcopy(self.c);c[key].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_omitted_source(self):self.reject('sources')
 def test_omitted_route(self):self.reject('primary')
 def test_omitted_batch(self):self.reject('batch')
 def test_omitted_capacity(self):self.reject('capacity')
 def test_omitted_permutation(self):self.reject('permutations')
 def test_omitted_bfs(self):self.reject('bfs')
 def test_omitted_vector(self):
  c=copy.deepcopy(self.c);c['capacity'][0]['vectors'].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_omitted_layer_state(self):
  c=copy.deepcopy(self.c);c['bfs'][0]['layers'][1].pop()
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_renewal_bypass_rejected(self):
  c=copy.deepcopy(self.c);c['renewal'][0]['boundary']=4
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_altered_floor(self):
  c=copy.deepcopy(self.c);c['sources'][0]['floors'][0]=1
  with self.assertRaises(AssertionError):v.verify(c,3)
 def test_altered_toggle(self):
  c=copy.deepcopy(self.c);c['primary'][-1]['ops'][0][0]=0
  with self.assertRaises(AssertionError):v.verify(c,3)
if __name__=='__main__':unittest.main()
