"""Review the P1 retained-grade versus B2 higher-incidence source boundary."""

import hashlib
from pathlib import Path

import review_common_field


BASE = "ResearchHistory/UQCF-GEM/"
PHYS = BASE + "research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    PHYS + "P1_B2_SOURCE_INTERFACE.md": "ff5a82b6eb575d94df794c7a1e897a528cf03c58",
    PHYS + "check_p1_b2_source_interface.py": "ade2ef4a6d8e408bb7438202a69fbaa3cc988f32",
    PHYS + "P1_WORK_CONNECTION.md": "c927a82fef384bdbc40bfa679cf2b2f404a98cb1",
    PHYS + "P1_WORK_CONNECTION_RESULT.md": "3a680f917bed6e9d4e9bea19ffc5bb05bc8a2765",
    BASE + "demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py":
        "620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a",
    BASE + "demos/v15.39-higher-incidence-source-axioms/docs/RESULTS.json":
        "ac8eb10ed90360fee6dcc0f170f19fffd0d74116",
    BASE + "demos/v15.40-global-balance-geometry-specificity/response_generation.py":
        "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5",
    BASE + "demos/v15.43-certified-response-geometry/acquire.py":
        "90f76146e7f6a875531a941290ad15679a8fb52f",
    BASE + "demos/v15.43-certified-response-geometry/README.md":
        "c939816a8b5b528fad2e82846e47dc7104cdc247",
    BASE + "foundational-closure-verification/PROOFS.md":
        "a21acad73c80cb748f2e42c244f6db53146c2bf2",
}
QUESTION = """Independently verify the scoped source-interface audit from the frozen documents and
exact replay. First give the strongest positive reading of the v15.39 closed-face source: check
that delta is a B2 face column, that B1 delta is zero, that the higher-incidence kappa channel is
nonnull, and that the archived ledger reports the stated additivity, reversal, covariance and
four-size coverage. Then challenge its use as the missing source for the reviewed P1 work-to-loop
chain. Inspect whether the v15.39 source axiom is derived or approved, whether it uses pruning,
whether its coarse vertex q channel carries a closed face, how v15.40 constructs centered face
sources, and what v15.43 acquisition actually imports and consumes. Check the published source-
correspondence status and the P1 proof's supplied periodic catalog, four-corner grades and label
association. Decide whether the inspected dependency closure contains an inherited provenance-
preserving map from a retained P1 vertex-grade record to the B2/periodic source. Do not claim a
universal no-go: noninspected or newly derived interfaces remain possible. Preserve the reviewed
conditional P1 work-to-connection result. Physical event binding, receiver ownership and access
remain open. Treat the exact replay as evidence and do not claim you executed it.
Return one JSON object with these exact field types: {"verdict":"ACCEPTED","findings":[],
"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},
"native_bridge_status":"OPEN"}. For ACCEPTED leave findings, missing_assumptions and
counterexamples empty and use substantive string values in proof_checks. Use REVISE or FAIL for
any actual defect."""
    

if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
