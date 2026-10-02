"""Read-only binding to certified v16.53 fixed-root clearance."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys

PARENT='f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8'
BASE='ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/'
HERE=Path(__file__).resolve().parent
_loaded=None

def load_clearance():
    global _loaded
    if _loaded is not None:return _loaded
    directory=HERE.parent/'v16.53-four-child-boundary'
    hashes={}
    for name in ('producer.py','feasibility.py'):
        expected=subprocess.check_output(['git','show',PARENT+':'+BASE+name])
        actual=(directory/name).read_bytes()
        if actual!=expected:raise ValueError('certified inherited source changed: '+name)
        hashes[name]=hashlib.sha256(actual).hexdigest()
    # The inherited producer's sole local dependency has been byte-bound above.
    spec=importlib.util.spec_from_file_location('feasibility',directory/'feasibility.py')
    dependency=importlib.util.module_from_spec(spec);spec.loader.exec_module(dependency)
    previous=sys.modules.get('feasibility');sys.modules['feasibility']=dependency
    try:
        spec=importlib.util.spec_from_file_location('v1653_bound_producer',directory/'producer.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    finally:
        if previous is None:sys.modules.pop('feasibility',None)
        else:sys.modules['feasibility']=previous
    _loaded=(module.clear_role,hashes)
    return _loaded
