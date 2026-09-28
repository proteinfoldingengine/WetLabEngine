# v16.05 — Frozen retained-edge localization protocol

Parent publication: 9a79f85c5d3181471ccdbe4d7a2a8b5b3c82755a; parent scientific head: 1b14035ab727b1f07a40c01498f91ad7fd0f3aac. User approved the next localization step on 2026-09-28. This protocol is committed before implementation and any ensemble measurement.

## Question

Does D's v16.04 numerical-null cubic contribution disappear before the Hessian, when the six connected pair directions are projected onto the five loop-readout edges, or does a nonzero retained direction reach the readout and get annihilated?

The inherited ordered edges are (0,1),(1,2),(2,0),(1,3),(3,0),(2,3). Only the first five enter F. Source D acts on (2,3). Neither edges nor loops are changed here.

## Exact layer

Convert all archived state_hex matrix entries to exact binary rationals, without decimal rounding. Form all 256 normalized Pauli coefficients exactly. Use the inherited exact coherent source table to construct [L_D,M_a] for symbolic a, then apply the exact diagonal local preparation and connected differential including both one-body-product terms. Archive the complete six 3x3 polynomial matrices for both preparations, and exact zero predicates for the first five and sixth edge. Exact nonzero polynomials, however small, are never relabeled exact zero.

Separately certify the following conditional support statement on the complete 112-word Pauli basis with at least one identity at sites 2,3: [L_D,M_a] has no weight-one output, and its weight-two output is supported only on pair (2,3). Local diagonal preparations preserve Pauli support, so the connected differential on the first five edges vanishes for this class. Test the actual archived state's excluded 144-word sector separately: record exact nonzero coefficients and whether its entire commutator is zero. Do not assume that binary storage preserves the ideal mixture support exactly. The direct polynomial calculation on each archived state is authoritative even if the sufficient support criterion fails.

Exact symbolic certificate failure or a nonzero retained polynomial is a reportable scientific outcome; do not tune or discard a state. Transfer-table reconstruction, rational-to-numerical reconstruction, and exact-to-numerical agreement are validity controls.

## Numerical layer

Retain candidates 13,16,22,25,27,29,37,39,46,50,66,77; all 81 hidden probes; both preparations; native and transformed frames; archived binary attenuation values 1,1/3,1/6; 50 and 80 digits. There are 72 configurations per precision and two frames. No finite-lambda or new-state sweep.

Build the D global commutator by the v16.04 independent weight blocks; reconstruct both hidden tangents and compare their retained equality and one-body nulls. Archive full D connected direction matrices on all six edges, per-edge Frobenius norms, the first-five norm and omitted-edge norm, fresh T_D, ranks, spectra, and all six origin correlation matrices. Compare T_D with both frames of the archived v16.04 result. Reproduce the parent's complete connected-direction norm; evaluate the exact native polynomials at the same archived binary a and compare all six matrices.

Within-precision absolute Frobenius tolerances remain 1e-35; cross-precision 1e-30. Check parent hashes, head/version/candidate/unique rows, exact source reconstruction, source/preparation controls, numerical/exact state coefficients, direct/block commutators, global/prepared-direction covariance, retained covariance, full direction and T_D cross-precision agreement, hidden null/equality, Hessian arithmetic identities, parent norm/matrix agreement, rank/classification agreement and unchanged polar domains. Nonfinite values, domain failures, corrupted provenance, missing data, or failed validity controls produce INVALID.

## Localization labels and scope

For D, using absolute first-five direction norm r and T_D norm t: r<=1e-35 and t<=1e-35 gives RETAINED_EDGE_NULL; r>1e-9 and t<=1e-35 gives READOUT_ANNIHILATION; t>1e-9 gives READOUT_RESPONSE; all remaining finite cases give UNRESOLVED. A retained-null/response contradiction is INVALID. These labels are descriptive; the validity gate accepts either location and unresolved outcomes.

Exact polynomial zero is a separate predicate. Report all 24 state/preparation symbolic cases and all 48 EB numerical configurations, with identity-middle controls separately. A nonzero sixth-edge norm confirms a change outside the retained loop edges but does not define geometry on the sixth edge: its polar domain is not part of this experiment. Never insert that edge into the readout after observing the answer.

At a=1 the commutator and all direction matrices vanish. At a=0 polar geometry remains undefined and is not evaluated. Time is pruning / ordered recoverability update. This experiment localizes an existing specified-model signal; it does not derive a source law or gravity.

## Execution and publication

Observe absent-implementation RED, implement and review, pass new and parent controls, then execute all 12 candidate jobs. Preserve full exact and numerical outputs, SHA256SUMS, exact logs and execution identities. Publish the final report and permanent raw files on the research branch after verification, without merging main or running unrelated wet-lab workflows.
