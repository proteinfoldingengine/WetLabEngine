"""Create the exact compact review view of the complete retained-state census."""
import hashlib
import json
import sys
from pathlib import Path

data=Path(sys.argv[1]).read_bytes()
result=json.loads(data)
for domain in result["domains"].values():
    assert len(domain["states"])==domain["state_count"]
    del domain["states"]
result["full_result_sha256"]=hashlib.sha256(data).hexdigest()
result["full_result_bytes"]=len(data)
print(json.dumps(result,sort_keys=True,indent=2))
