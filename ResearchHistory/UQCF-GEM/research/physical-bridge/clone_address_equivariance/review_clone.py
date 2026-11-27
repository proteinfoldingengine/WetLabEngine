from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import subprocess
import sys
root=Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())
path=root/"review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
data=path.read_bytes()
if sha1(b"blob "+str(len(data)).encode()+bytes(1)+data).hexdigest()!="0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Historical review driver identity mismatch")
spec=spec_from_file_location("pinned_review",path)
d=module_from_spec(spec)
spec.loader.exec_module(d)
d.ROOT=root
d.DOCUMENTS={
    "ResearchHistory/UQCF-GEM/research/physical-bridge/clone_address_equivariance/FINDING.md": "d275dfe599fcfc4a4b306cf9a5184fcb7851c0fc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/clone_address_equivariance/replay_clone.py": "b548d5e39e55e0fa9528c4ebd5713152b36cd3d6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/clone_address_equivariance/expected.json": "31cb937a2899ee0acf2b0bd70de0ef3e6d0da73f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43"
}
d.QUESTION="Independently verify the exact software claim in FINDING.md. Derive the two slot and demand lists for both stages and no-source control in each case. Check whether strict floor and demand-width inequalities make endpoints insensitive to both kinds of simultaneous relabeling while primitive order can change. Check disjoint rows and covering pair, signed cuts, receiver-only writes, no-source and identical-fresh-post aliases, equal-floor symmetry, allowed exact no-op and other supplied commands, and whether any feature of this case is archived occurrence rather than a constructed exact input. Identify any substantive error. Do not infer physical access, native generation, or novelty. Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. Separate scope limitations from errors in the scoped program-level argument; if accepting the scoped claim leave the last three arrays empty."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
