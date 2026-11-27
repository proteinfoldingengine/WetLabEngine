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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/RESULT.md": "c158c7f2c89674f6e21f5f2a320d281ffe4e5535",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/expected.json": "c8b17c474baedca362b37fda6abfac3f11f875b2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/replay.py": "e6375953bfba2a42ac796a57a4a76e6964e73bed",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/rows-0.json": "8a7e0804428539be75d104246ef310c8066de490",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/rows-1.json": "b04706d8994bc6e911b819d6add0776a42cbb9be",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43"
}
d.QUESTION="Adversarially adjudicate the complete scoped proof in RESULT.md. Independently reconstruct the archive pair, both exact root profiles and wrong-gain controls, from the supplied rows, unchanged producer and verifier, and observed guard-read replay. Verify actual in-call recomputation, equal remaining pending, alternate possible restoration, receiver own-row contrast versus equal final row, and whether either input plan supplies labels or receivers. Reject any claim that the incidence guard forces progress without the supplied loop and requests, or that M2 is a P1 event. Distinguish an existing central software continuation from a derived native operation, ownership/read access, and physical significance. Return JSON with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting, leave findings, missing_assumptions and counterexamples empty and state boundaries in limitations. Do not assess external scientific novelty."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
