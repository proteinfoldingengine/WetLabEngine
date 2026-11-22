"""Export GitHub-verified archive bytes for both historical child-call reviews."""
import base64
import hashlib
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

REPO = "proteinfoldingengine/WetLabEngine"
PREVIOUS_HASHES = {"ternary-child-replay":"d5d83e224e39c5e4dfa49a0bca1a1b9d91bb98c57cfa2cd51f8d37cd2dbf68f1","ternary-child-review":"25ac1314f58b38840cf28b74f8b449443c3bd7666e4c2f7fc1dbecc2bafd79b3","ternary-child-publication":"cf3cd0e8471a5e0b16034efa4c10e2a54565d7c5f70fe3406374023b9a9829d4"}
def get(rest):
    return subprocess.run(["gh","api","repos/" + REPO + "/" + rest],check=True,capture_output=True).stdout
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def main():
    now = int(os.environ["GITHUB_RUN_ID"])
    for label,run,head,prefix,result in (
        ("ternary",44921891822,"d46470c8d572bf995b47703018e2c312ba6d211d","ternary-child","ternary.json"),
        ("chain",now,os.environ["GITHUB_SHA"],"chain-child","chain.json")):
        response = json.loads(get(f"actions/runs/{run}/artifacts?per_page=100"))
        arts = {a["name"].removeprefix(prefix+"-"):a for a in response["artifacts"] if a["name"].startswith(prefix+"-")}
        assert set(arts) == {"review","replay","publication"}
        contents, binaries, manifest = {}, {}, {}
        with TemporaryDirectory() as tmp:
            for name,a in sorted(arts.items()):
                raw=get(f'actions/artifacts/{a["id"]}/zip')
                assert a["digest"]=="sha256:"+sha(raw) and len(raw)==a["size_in_bytes"]
                if label=="ternary":
                    assert PREVIOUS_HASHES[a["name"]]==sha(raw)
                path=Path(tmp)/(name+".zip")
                path.write_bytes(raw)
                with ZipFile(path) as z:
                    assert z.testzip() is None and all(Path(n).name==n for n in z.namelist())
                    docs={n:z.read(n) for n in z.namelist()}
                binaries[name]=raw
                contents[name]=docs
                manifest[name]={"artifact_id":a["id"],"bytes":len(raw),"sha256":sha(raw),
                                "entries":{n:{"bytes":len(v),"sha256":sha(v)} for n,v in docs.items()}}
        docs=contents["review"]
        audit=json.loads(contents["publication"]["publication_audit.json"])
        assert audit["audit"]=="PASS" and audit["verdict"]=="ACCEPTED"
        assert int(audit["run_id"])==run and head==audit["workflow_sha"]==audit["checkout_sha"]
        for key in ("response","prompt","request"):
            filename="prompt.txt" if key=="prompt" else key+".json"
            assert sha(docs[filename])==audit[key+"_sha256"]
        verdict=json.loads(docs["review.txt"])
        assert verdict["verdict"]=="ACCEPTED" and not any(verdict[k] for k in ("findings","missing_assumptions","counterexamples"))
        output=contents["replay"][result]
        parsed=json.loads(output)
        if label=="ternary":
            assert parsed["archive_rows"]==7236 and parsed["runs"]["delete_A_v5"]["untouched_leaf_v6"]["raw"]==[1]
        else:
            assert parsed["unchanged_default_producer_matches_full_archive"] and parsed["common_field"]["nonzero_common_field_residuals"]==0
        for name,raw in binaries.items():
            for i in range(0,len(raw),6000):
                print(f"CHILD_ARCHIVE_{label}_{name}_{i//6000}="+base64.b64encode(raw[i:i+6000]).decode())
        print("CHILD_MANIFEST_"+label+"="+json.dumps(manifest,sort_keys=True))
if __name__=="__main__":
    main()
