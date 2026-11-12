import copy
import importlib.util
import json
from pathlib import Path
import unittest

module = Path(__file__).with_name('uqcf_owner_integration.py')
if not module.exists():
    module = Path(__file__).with_name('integration_audit.py')
spec = importlib.util.spec_from_file_location('audit', module)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class HistoryReplay(unittest.TestCase):
    def setUp(self):
        self.old = {'execution_head': 'old', 'records': [{'rank': 2}], 'all_valid': True}
        self.new = copy.deepcopy(self.old)
        self.new['execution_head'] = 'new'
    def test_changed_execution_identity_preserves_science(self):
        audit.compare_history(json.dumps(self.new).encode(), json.dumps(self.old).encode(), 'new', 'old')
    def test_changed_scientific_record_is_rejected(self):
        self.new['records'][0]['rank'] = 3
        with self.assertRaises(ValueError):
            audit.compare_history(json.dumps(self.new).encode(), json.dumps(self.old).encode(), 'new', 'old')
    def test_forged_execution_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            audit.compare_history(json.dumps(self.new).encode(), json.dumps(self.old).encode(), 'forged', 'old')

if __name__ == '__main__':
    unittest.main()
