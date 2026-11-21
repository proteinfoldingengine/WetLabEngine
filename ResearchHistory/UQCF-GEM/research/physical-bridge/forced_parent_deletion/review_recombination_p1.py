"""Independent review of a literal ancestry-to-recombination binding."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECOMBINATION_P1.md": "dfdf1edda8b23946dd8d78cdeaaa2ee84b7e7104",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECOMBINATION_P1_PROTOCOL.md": "9ce35e703e1501405dbfa70cadbc5457937287cb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECORD_NATIVE_LIMIT.md": "f4372d0e919a8da8ccfc5123c9b973db9cb45412",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_bracket_pruning.py": "274a37c61009da3dce5ad533ed43e0970f4a6a5b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/recombination_p1/summary.json": "bcddaa4fbb2aebc9275f004978ff91e53a656b15",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_bracket_ports.py": "80e74e11ef3af58ff41d49e1838091342b5ac6bf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/SAME_PORT_RESPONSE.md": "215e94d3ab8609c235b2103084358cb105690092",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/H4_rock_test/v1687_16.py": "090a03bf665b97d7784f688c8294a348ad20507f",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v15.14-record-dependencies/adaptive.py": "44a87e4cc5bcf531ef7798aadab5d9dbba3482cb",
    "ResearchHistory/UQCF-GEM/demos/v15.15-coherent-records/coherent_records.py": "fdf5367b11729fc1e2bfccd8d8daa2a0c7209049",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/recoverability.py": "0a01d2eea4f0114b119fbb7beaf4619775c0f9f6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/exponential_operation_bridge/RESULT.md": "27426646e87aa9aafd4ec3e80612bf4380df280d"
}
QUESTION = "Independently challenge the full RECOMBINATION_P1.md and RECORD_NATIVE_LIMIT.md. Reconstruct the directed-cycle columns and rank, elementary P1 support, two-step expansion bound with mixed orientations, the no-monotone-sequence result for both actual operands, and the difference between a direct event hypothesis and a changed grouping. Verify exact one-merge conditions for arbitrary left-factorization and same-law coarse cyclic identity including n=3; classify all 132 possible pairs from zeros; verify fine and coarse contrasts, absolute mismatch on the two exceptional cases, and fixed site3 observations. The summary binds the full machine result by SHA. The local finite-reading negatives apply only to fixed archived fields and parameters, not arbitrary calibrated amplitude. Challenge the general two-free-input nonfactorization and minimum linear additions for one merger with both input variations. Independently reconstruct why every original adaptive prefix/next record law is unchanged by the pullback pinch using the sharp code, and the state-independent bounded-copy rational obstruction for the unknown affine family, including conditional means, a derivative with merely pointwise finite limits, coefficient subsequence, continuation and logarithmic endpoint. Do not conflate a fixed read with unobserved intermediate states, a generated amplitude with an actual physical activation, or a bounded no-go with universal impossibility. No execution claim. Return JSON with verdict ACCEPTED/REVISE/FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks and native_bridge_status. Include separate calculations and exact figures. ACCEPTED requires empty findings, missing_assumptions and counterexamples."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
