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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/residue_controls/FINDING.md": "38688065fb896be34aa808d541a89edaab6fb890",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/residue_controls/expected_control.json": "1b17bee56f1070adcb7aad1bcc1ad116d7636cee",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/residue_controls/replay_residue_controls.py": "ad2a737f0fe193fb2e1a96f34f0b405f6584143d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/residue_controls/root-residue-fresh-original.json": "ba3bfe9aeb27d91bebf3ec808c57dd290d711a66",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/residue_controls/root-residue-mirror-original.json": "71dbccfd055b8a6d7bf34d4bfd29d3128bc9d6fe",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_buffer_local_word/buffer-rows-0.json": "5db794d6cc850b9ff2e34558ceeb3892dd9dbe95",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43"
}
d.QUESTION="Independently audit the exact finite software correction in FINDING.md, comparing all three original records. Check every condition of the replay, exact record identities, the extent of fresh equivalence including event interval offset, the fixed numerical order versus renaming of labels 2 and 3, and whether the fresh execution and reindexed buffer reject interpreting a four-edit path as proof of source occurrence or proof that the released label had to be buffered. Distinguish the bounded software finding from prior physical custody, historical unknown, or a claim that no such mechanism is possible. Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting the scoped argument, separate actual defects from declared scope limitations and leave the last three arrays empty. No physics or novelty claim."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
