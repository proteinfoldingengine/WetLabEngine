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

## Remaining work

A substantive state/support/provenance/occurrence/coupling witness must be provided and validated before source admission. Stages B–E of the full design are not completed by Stage A. No geometry-facing experiment, physical stress-energy, Einstein equation or continuum claim follows from a passed preflight. **Source correspondence remains NOT_EVALUATED; Pillar 3 remains OPEN.**
