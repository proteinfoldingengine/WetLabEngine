from pathlib import Path
import sys,copy,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v16.37-certified-closure'))
import producer,verifier
sys.path.pop(0)
import run_campaign

class Extension(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.old=producer.produce(2)
 def test_identical_parent_accepted(self):run_campaign.compare_parent(self.old,self.old,2)
 def test_missing_graph_rejected(self):
  bad=copy.deepcopy(self.old);bad['graphs'].pop()
  with self.assertRaises(ValueError):run_campaign.compare_parent(bad,self.old,2)
 def test_duplicate_graph_rejected(self):
  bad=copy.deepcopy(self.old);bad['graphs'].append(bad['graphs'][0])
  with self.assertRaises(ValueError):run_campaign.compare_parent(bad,self.old,2)
 def test_same_count_substitution_rejected(self):
  bad=copy.deepcopy(self.old);bad['graphs'][-1]=bad['graphs'][0]
  with self.assertRaises(ValueError):run_campaign.compare_parent(bad,self.old,2)
 def test_changed_edges_rejected(self):
  bad=copy.deepcopy(self.old);bad['graphs'][0]['edges']=[[0,0]]
  with self.assertRaises(ValueError):run_campaign.compare_parent(bad,self.old,2)
 def test_reordered_graphs_accepted(self):
  bad=copy.deepcopy(self.old);bad['graphs'].reverse()
  run_campaign.compare_parent(bad,self.old,2)
 def test_six_vertex_domain(self):
  run_campaign.validate_domain({'version':'16.37','bound':6,'view_counts':[1,2,3]})
 def test_wrong_campaign_domain_rejected(self):
  for key,value in [('version','16.38'),('bound',5),('bound',6.0),('view_counts',[1,2])]:
   d={'version':'16.37','bound':6,'view_counts':[1,2,3]};d[key]=value
   with self.subTest(key=key,value=value),self.assertRaises(ValueError):run_campaign.validate_domain(d)

if __name__=='__main__':unittest.main(verbosity=2)
