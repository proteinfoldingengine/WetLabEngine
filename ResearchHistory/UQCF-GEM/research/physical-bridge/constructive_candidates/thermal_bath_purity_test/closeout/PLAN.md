# Bounded thermal-bath closeout implementation plan

Date: 2026-11-02, America/Phoenix. GPT Work takes execution ownership in T-293.
Use the executing-plans workflow inline; preserve the existing independent Gemini requirement.

Goal: complete PR131 correction, GitHub verification and durable publication, without a new thermal research branch or changed physical claim.
Integrated reference: 1a18308a026c06882b428fbe201b4634c34dfd8f.
Original package: 23543a5b8c5f8938fe0d25c42be975296c8055fb; its 26 PR files are copied exactly.
Spec: original PREREGISTRATION.md and RESULT.md, superseded only by CORRECTIONS_T275.md and the bounded corrected-scope note. Original review 41515580146 is retained and never rebound.

## Authorization and limits
Aaron directly instructed this session to finish the currently authorized bounded thermal-bath test and preserve its result, then return to inherited structure. This is existing completion work. No new physics premise, dimension sweep, channel family or numerical discovery is admitted. Native delivery remains NOT_DERIVED. PR131's owner-review merge condition remains; this branch will supply the completed evidence for that review.

## Disclosed known outcomes
All original outcomes are known from local-run-1: Q1 PASS, fixed full-rank R-untouched mirror FAIL, SWAP delivers the distinction to E with D_R=0, and the entropy check holds. C1's Gibbs wording and C2's global-threshold counterexample are already accepted analytically by the author. We are verifying known claims, not preregistering discovery.

## Frozen scientific scope
1. Reproduce original t271_tb.py and independent t271_verify_np.py unchanged using Python 3.13.5, sympy 1.14.0, numpy 2.5.4, mpmath 1.3.0, matching the original environment. Compare all exact/rational/boolean scientific fields to the archived output. For the original supplementary Haar maxima only, retain the known fixed-seed values with an absolute 1e-10 comparison tolerance across platforms; no sample, seed or threshold changes. Compare the independent checker against every common output field. A fresh publication run must reproduce the new execution bytes exactly in the same pinned environment.
2. C2 only: carrier A with basis (o,p1,u1,p2,u2,v); channel with Q=diag(1,1,0,1,0,1), L1=|p1><u1|, L2=|p2><u2|. Pure E with dimension two meets each fan-in-two rank condition but cannot realize the full channel, whose Choi rank is three. Pure E dimension three has the already-known unitary witness swapping |u1,0> with |p1,1> and |u2,0> with |p2,2>. R is a spectator. No global mixed-bath sufficient criterion is asserted.
3. Producer uses exact sympy Gram rank of vectorized Kraus operators and explicitly constructs the permutation unitary. Independent checker uses numpy matrix-unit channel composition, Choi SVD, and partial trace of the permutation witness. It does not import producer decisions. Freeze exactly two cases (E2/E3) and all 36 matrix-unit actions for the E3 witness.
4. Reject seven mutations: missing case, duplicate case, substituted case, wrong Choi rank, false E2 sufficiency, wrong-slot witness, false provenance. Preserve rejection reasons. Also reject a corrupted original-output verdict in the comparison layer.
5. Run the unchanged inherited stack separately with Python 3.11, sympy 1.13.3 and mpmath 1.3.0: 22 FCV tests, 15 v15.56 parent tests, two historical tests, historical reproduction, FCV producer, independent verifier and inherited rejecting controls. Retain complete output.

## Tasks and interfaces
- [ ] Commit this contract and exact originals before scientific execution.
- [ ] Write independent C2 checker first; demonstrate rejection on corrupted certificates; write producer; require two complete case identities, rank and all-input witness agreement.
- [ ] Add the original-output comparison and its corrupted-verdict control; no producer or checker source modification.
- [ ] Freeze all new scripts, current scope note, original source blobs and workflow before dispatch. Source-integrity failure gates review.
- [ ] GitHub verification: original reproduction + C2 independent checks + inherited stack.
- [ ] One Gemini generation request on the exact corrected argument, originals/corrections, code and evidence context after verification passes. Independently reconstruct C2 and reject scope promotion. Return ACCEPTED/REVISE/FAIL, preserving adverse outcomes and raw request/response. The old review and PR132 are context, not acceptance of this package.
- [ ] Separate publication job repeats deterministic verification and compares bytes with the initial GitHub outputs; raw review identity and parse checked without a second model call.
- [ ] Download exact artifact ZIPs, validate API digests, inventories and all manifest members; preserve source, outputs, raw logs, model metadata and evidence in GitHub with immutable readback.
- [ ] Adjudicate findings, notify the bot thread and return PR131 to Grok for the recorded owner review. Do not merge around that condition.

## Review focus
Single-collision rank sufficiency must not become global sufficiency. Pure-bath Kraus-rank capacity is not a sufficient criterion for arbitrary mixed baths. Unitary construction is on the supported input subspace with a legitimate full-space extension; unused columns cannot be called a unitary without that extension. The SWAP conclusion is about the supplied equal-qubit benchmark, and purity loss must not be called source delivery. Fixed numerical or software verification does not supply native ownership/access.

## Resource and stopping rules
One scientific dispatch after freeze; jobs at most 30 minutes each, review at most 15 minutes. Retry only a documented infrastructure/software defect with failed evidence preserved and corrected bytes identified. Never adjust a scientific threshold or silently drop a control. A complete adverse review is archived and adjudicated, not retried for a favorable answer. Local construction/debug checks are disclosed and not counted as GitHub campaign evidence.

## Initial ledger
Pre-flight: original reproduction feeds comparison; C2 producer feeds independent checker/controls; both and inherited tests gate review; all initial deterministic outputs feed fresh publication. No schema conflict identified.
Ruling: isolated closeout branch begins at the current integrated reference and carries the exact PR131 packet; Grok's branch stays untouched to avoid conflicting ownership.
