"""Review the finite-tree lost response and its full-cover controls at the frozen revision."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/COMMON_FIELD.md": "79f295f93bd4b35d6382ffa5280e948c348c9358",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_common_field.py": "5c249b8208fcc9b2cd77c1de0f5bd2535eb165c4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/common_field_results.json": "f247e9534c8ec3b3cc0400575bc7ef448b1efde0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_attached_contraction.py": "bd47c08eaf561bc4a6cbffa2f8a84ac9232c02ad",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/attached_contraction_results.json": "711811dbe996d3bde9c4b7a327d6d49564171807",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_passive_view.py": "ee3aec59f61b9525ed7d45e32dc55d91e824e993",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_original_atomic.py": "d9750d2cd672304be5342cc46d1eb4d50bd8eb6f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_root_trigger.py": "b9e5817a2a44c9b2010313d70f60a6d525c3e0b8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/PASSIVE_VIEW.md": "77d62e7b64bc6430842800114f9d0d93febb05d0",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/produce_certificates.py": "a056d636900db6ab8f9a7775dd75e7dd190e6fe8",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/verify_certificates.py": "d6d928982a65c1f72b4b9d3fc7e93c30653fed5f",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/PROOFS.md": "fd92415cc08e83858d4368047721c2bb27f9e500",
    "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/test_gate.py": "d3d762736290e3192333b12cf4277248010f2e32",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/producer.py": "90108c926299ca7cb66dca6acc4530bafcdb4a7e",
    "ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/verifier.py": "93fb1a7f40e304fc8fd05767a086b912cf4288a6",
    "ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/INTERFACE_LEMMA.md": "7f85ca3e9a7ca727ca2b03766872d0befe97a084",
    "ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/coverage.py": "973244d0eb8a48bcb2464870377139cf4e9870c6",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/FOUR_CHILD_INTERFACE.md": "7d903c609a94bdee960bc6c90c4a458f077ffcb9",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_move_interface/RESULT.md": "0371d4a8aa66ce02ffbda084ad5dde93f1ec1136"
}
QUESTION = """Independently reconstruct COMMON_FIELD.md from the supplied old code, exact proofs and the two replay files. Check each mathematical claim within its stated domain and attack any attempted inference to receiver delivery. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations and proof_checks, and native_bridge_status. For ACCEPTED the findings, missing_assumptions and counterexamples arrays must be empty. In proof_checks supply the actual equations or numbers you independently obtain, including the following.
1. For each event form the loss projector in the correct fine carrier, include it into X, and project onto the literal C view. Check sign, signed zero and negative cases, compatibility fixing the parent coefficient, and what would be an unjustified reinjection.
2. Derive the component potentials on all three endpoint views, state which view is logically obliged under O4 to match a realized nonzero op increment, what is optional outside the intersection, and which stronger claims require the literal injection. Recompute the unchanged passive field and shared-port blindness.
3. Derive both clamped dimensions and same-port test outcomes, both-free and both-clamped full-cover controls, fixed pw control, the one-bit information statement, and any hidden positivity/majority/grade/access assumptions. Check changes of representative and the two gauges.
4. Read the v16.52/53 contraction and FCV/O4 callers. Check whether either actually produces the stipulated immediate second event or publishes a local state change. Distinguish a loss component stored in a certificate from a field increment delivered to C, and the numerical counting preparation from arbitrary data.
A nonzero actual change of C cannot be inferred by decomposing a common old field. If you find a mathematically false or overbroad claim, quote the claim in context and give an explicit counterexample. Conditional declared inputs are limitations. A bare verdict is not an inspected review."""


def main():
    data = DRIVER.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Independent review driver changed")
    spec = importlib.util.spec_from_file_location("frozen_review_driver", DRIVER)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.DOCUMENTS = DOCUMENTS
    driver.QUESTION = QUESTION
    driver.main()


if __name__ == "__main__":
    main()
