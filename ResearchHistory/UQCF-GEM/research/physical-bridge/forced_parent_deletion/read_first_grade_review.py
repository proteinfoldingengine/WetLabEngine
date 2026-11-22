"""Read, hash, and export a failed review's raw evidence without reinterpreting it."""
import base64
import hashlib
import io
import json
import subprocess
from zipfile import ZipFile

ROOT = "repos/proteinfoldingengine/WetLabEngine/"
PINS = {
    "routed-grade-replay": [
        14716580159,
        1319,
        "e181a66fcadb035812f4b6a17a465e512aa3a5570f60f1ed3e36c8f7d136e21e"
    ],
    "routed-grade-review": [
        14716550451,
        90951,
        "e8815687d6577031f6930dcef2f999ddcd2fc69d31f286822e6505a0cf8acfc9"
    ]
}

for name,(number,size,pin) in PINS.items():
    raw = subprocess.run(["gh","api",ROOT+f"actions/artifacts/{number}/zip"],capture_output=True,check=True).stdout
    assert len(raw)==size and hashlib.sha256(raw).hexdigest()==pin
    with ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None
        if name.endswith("-review"):
            for f in ("review.txt", "response.json", "receipt.json"):
                if f in z.namelist():
                    print("FIRST_REVIEW_"+f+"_B64="+base64.b64encode(z.read(f)).decode())
    alias = name.split("-")[-1]
    for i in range(0,len(raw),6000):
        print(f"FIRST_GRADE_{alias}_{i//6000}="+base64.b64encode(raw[i:i+6000]).decode())
