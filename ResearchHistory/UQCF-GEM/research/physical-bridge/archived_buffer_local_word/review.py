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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/RESULT.md": "943755480c0929f9a4dc5912ed94192267d9c214",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/expected.json": "0abea04b043ed039e8492a7b2b7b284b42d6af51",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/replay.py": "e098ecd0255bd8e9a3e9f048fa759407d2c571b5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/buffer-rows-0.json": "5db794d6cc850b9ff2e34558ceeb3892dd9dbe95",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/buffer-rows-1.json": "bedb15f6d651d89e820bf8c2c0ce5cad58e01985",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43"
}
d.QUESTION="Independently reconstruct and adjudicate the scoped program-level and finite combinatorial claims in RESULT.md. Audit the archive rows, source release event, exact shared pre-release state, source and both peer plans, the common post-release menu and when occupancy invokes the stock direct versus buffered route. Check all support profiles and own-state projected words, including that label erasure preserves the size-word difference, both terminal receiver rows match, and the archive projector is not an original receiver-owned reader. Derive or refute the six-versus-four lower bounds with source frozen and peers' targets supplied, and check the symmetric buffer control. Distinguish a provable existing software operation, the program-supplied choice of buffer owner, and the still unestablished native bridge. Return exactly one JSON object, not an array or prose, with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting the scoped argument, separate actual defects from declared scope limitations, and leave findings, missing_assumptions, counterexamples empty; otherwise identify a concrete repair. No physics claim."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
