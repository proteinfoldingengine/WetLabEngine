"""Targeted whole-source review controls, frozen before corrections."""
from pathlib import Path
import subprocess,unittest
from unittest.mock import patch
import producer as p
from test_integration import Integration

class ReviewFixes(unittest.TestCase):
    def test_one_unit_boundary_control_kills_permissive_guard(self):
        name='test_recursive_boundary_one_unit'
        self.assertTrue(hasattr(Integration,name),'ONE_UNIT_BOUNDARY_CONTROL_MISSING')
        def permissive(state,nodes,q):
            if abs(p.coordinate(state,nodes[0])-q)>1:raise ValueError('recursive call requires exact parent')
        result=unittest.TestResult()
        with patch.object(p,'require_exact_parent',side_effect=permissive):Integration(name).run(result)
        self.assertEqual(len(result.errors),0)
        self.assertEqual(len(result.failures),1,'ONE_UNIT_GUARD_MUTANT_SURVIVED')
    def test_generated_bytecode_is_ignored(self):
        stage=Path(__file__).resolve().parent
        names=[str(stage/'__pycache__'/'producer.cpython-311.pyc'),str(stage/'temporary.pyc')]
        result=subprocess.run(['git','check-ignore','--no-index','--stdin'],input='\n'.join(names)+'\n',capture_output=True,text=True)
        self.assertEqual(result.returncode,0,'GENERATED_BYTECODE_NOT_IGNORED')
        self.assertEqual(result.stdout.splitlines(),names)
    def test_hidden_source_retained_in_development_artifact(self):
        workflow=Path('.github/workflows/v16.53-red.yml').read_text()
        self.assertIn('include-hidden-files: true',workflow,'HIDDEN_SOURCE_ARTIFACT_RETENTION_MISSING')

if __name__=='__main__':unittest.main(verbosity=2)
