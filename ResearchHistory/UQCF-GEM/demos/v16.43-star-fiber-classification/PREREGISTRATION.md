# v16.43 prospective local-star obstruction classification
Status: PREREGISTERED / NOT EXECUTED / NOT CERTIFIED.
Exact verified parent: 4c8df6179496d8a5a6304443e4a5c7ade6a4ff6f, PR90, successful actual-merge run36793743498, durable receipt42523d3a72493bcafba3d6ef9a2083aede82372f.

## Question and disclosed analytical hypothesis
For an m-leaf rooted star with k indexed labels and target hitting number q, is the exact fiber connected unless m=k=q? The fully packed exception should have m! isolated exact states, with all three independent barriers1 between them; all other fibers should have one component and barriers0 between their states.
Proposed proof: shrink every leaf support onto a chosen minimum hitting set without changing q; then normalize the resulting surjective leaf coloring. A spare leaf (m>q) or spare label (k>q) should permit zero-cost rearrangements. This is an analytical hypothesis, not a measured result.
Prior v16.41 already tested m=k=4, all profiles; v16.42 tested the q=2 stars with k=2,m=3,4,5. Disclose these as prior threshold evidence. New normal-form certificates and the general proof are prospective. No claim of blinded replication.

## Frozen finite universe and objectives
Exactly all (m,k) in {2,3,4} x {2,3,4}, plus (5,2),(5,3). For EACH graph independently enumerate every admitted state, primitive move, all attained q profiles, exact/unit components and unordered component pairs. Require exact canonical domain/state/edge/profile/component/pair identity equality.
For EVERY admitted state retain a candidate path to the canonical singleton coloring for its q. Require cost0 except fully packed m=k=q, where cost<=1. Fully packed means all THREE equal; q=m alone with k>m is not the partition class. The inherited graph algorithms must explicitly respect this extended domain.
Primary B1,Binf,Bs remain independent scalar minima; LEX is separate.

## Competing outcomes
NONUNIT_WITNESS: independently complete unit cut and admitted unrestricted path; identify which scalar is nonunit.
CLASSIFICATION_REFUTED: independent complete exact components contradict the predicted one-component/fully-packed classification; do not conflate with nonunit.
CONSTRUCTION_REFUTED: candidate normalization path fails while the independently checked classification and threshold evidence are retained.
STAR_CLASSIFICATION_VALIDATED: independent mathematical review accepts the all-m,k,q proof and every frozen finite check passes.
INCOMPLETE: enumeration/provenance/resource failure. Preserve failed artifacts and report without certification.
A bounded numerical pass alone is not a general proof. No claim about physical gravity follows.

## Controls and stopping/closure rules
Missing/duplicated/substituted domain/state/edge/profile/component/pair/path records must be rejected. Include q=m,k>m spare-label and q=k,m>q spare-leaf positive controls, fully packed isolated-state negative control, invalid normalization adjudication, wrong provenance/objectives, abstract nonunit cut/path controls and genuine verifier-disabled RED.
GitHub-only numerical execution. Existing 431 inherited checks plus new controls; fresh v16.42 and nested parent science reconstruction; pinned Python3.11, Sympy1.13.3, mpmath1.3.0. Jobs: preflight<=5min, science/publication/post-merge<=45min each, receipt<=10min on ubuntu24.04. Any incomplete job blocks closure; no automatic domain relaxation or outcome-driven expansion.
Source/input snapshot and Git-blob bindings; run/attempt/workflow/head/prereg/parent metadata; complete artifact manifests; fresh publication byte equality; independent review; exact-head merge; actual-merge replay and durable audited receipt are mandatory. No CLOSED/CERTIFIED status before that chain.
