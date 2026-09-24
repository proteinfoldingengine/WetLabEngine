# v15.46 — Primitive Joint-State Source Admissibility / Incidence Typing

## Current scope

This is an ongoing source-admissibility investigation, not an adopted physical source law or a full v15.46 certification. The certified v15.44 and v15.45 snapshots have been published to main through [PR #58](https://github.com/proteinfoldingengine/WetLabEngine/pull/58); this v15.46 work remains separate on [PR #57](https://github.com/proteinfoldingengine/WetLabEngine/pull/57).

The known conditional modular operator is mathematically defined on a supplied faithful joint state. The existing [research decision](RESEARCH_DECISION.md) records its prior art, exact pairwise-descent counterexample and noncommuting example. The [admissibility review](ADMISSIBILITY_REVIEW.md) identifies missing native provenance and incidence coupling, with conditional trace-only and unaddressed-boundary-source constraints. These results do not assert the absence of all possible future source laws.

## Implemented continuation: Stage-A evidence preflight

`evidence_preflight.py` verifies the exact ten-source inventory and reads the referenced bytes. A separate submitted-witness packet declares evidence for the joint state, overlap inclusions, support treatment, oriented occurrence link, coupling, linearity and provenance derivation. No complete witness is submitted by the current study.

The important distinction is enforced in code: even all seven file references plus a self-declared native label cannot certify a native source. File presence is not semantic validation. The empty submitted-witness list is not an exhaustive repository absence proof and does not imply that the source value is zero.

[Execution record and limitations](docs/STAGE_A_EXECUTION.md) separates local tests from GitHub checkout verification. The narrow workflow checks the current 28-test preflight/exploratory set, original 195-check mathematical result replay, typing-result replay, actual inventory pins and canonical Stage-A output. Final run receipts are attached to PR #57.

From the repository root, with CPython 3.13.5:

```sh
D=ResearchHistory/UQCF-GEM/demos/v15.46-primitive-joint-source-admissibility
python "$D/evidence_preflight.py" --root . --out /tmp/v1546-stage-a.json
python "$D/evidence_preflight.py" --root . --check /tmp/v1546-stage-a.json
```

The source research checkout is needed because the inventory includes historical files not copied into the selective main publication. No archived pin is relaxed to accommodate a different checkout.

## Implemented continuation: Stage-B native record trace

Stage B selected the strongest scoped existing joint-state candidate, the frozen v13.27 six-qubit thermal demo, because it supplies an explicit joint state, graph, source operator and source-node labels. The trace verifies the exact source blob and stops at the first unearned native interface rather than inventing missing types.

The machine result is:

`SUPPLIED_JOINT_STATE_PRESENT_NATIVE_PROVENANCE_UNESTABLISHED`

The first unmet interface is `B1_NATIVE_JOINT_STATE_PROVENANCE`: the file constructs a supplied demo state with normalized `exp(-beta H)`, but does not derive that state from primitive retained records. Consequently overlap inclusions, support treatment, occurrence addressing and coupling are marked `NOT_EXECUTED_AFTER_FIRST_FAILURE`.

[Stage-B result](docs/STAGE_B_RESULTS.json) and [CI receipt](docs/STAGE_B_CI_RECEIPT.md) record the exact RED→GREEN evidence. Complete run `35946791128` passed 35/35 current v15.46 tests and replayed the prior exact controls on executed head `1211968aa97fd9b52476dfebbae419fb74df8ff4`.

## Remaining work

The next research problem is upstream of geometry: either identify a genuinely primitive-derived joint record, or prove within a bounded declared archive scope that no candidate in that scope supplies the required native provenance. Only after native provenance is earned should overlap/support/occurrence/coupling stages execute. No geometry-facing experiment, physical stress-energy, Einstein equation or continuum claim follows from Stage A or B. **Source correspondence remains NOT_EVALUATED; Pillar 3 remains OPEN.**
