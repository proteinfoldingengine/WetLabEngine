# Before implementation: expose the inherited runner to the new tests.
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent.parent/'v16.37-certified-closure'/'run_campaign.py'
spec=importlib.util.spec_from_file_location('inherited_run',p)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
