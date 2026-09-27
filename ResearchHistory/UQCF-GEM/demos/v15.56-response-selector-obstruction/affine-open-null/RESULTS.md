# v15.75 — Affine robustness and a physical pointwise null

Primary verdict: **AFFINE_OPEN_NULL_RETAINED_CLOSED_CONFIRMED**.

Secondary verdict: **CPTP_POINTWISE_NULL_ONLY_CONFIRMED**.

The fixed-affine extension passed. Across the twelve frozen states, the retained-output tangent map has rank 36 for both pre-Sylvester skew Q and rotation E. No common nonzero retained tangent lies in their kernels. An explicitly CPTP, affine channel nevertheless realizes nonzero symmetric retained leakage with null rotation at its frozen reference state. The same channel is visible on the non-reference ensemble. Operational admissibility therefore permits pointwise invisibility; open-state robustness is the additional condition that rules out retained leakage for a fixed affine law.

## Classification result

Each state supplies a 9-by-36 map from the nine one-body and 27 pair tangent coefficients to nine retained rotational coordinates. The stack is 108-by-36. At every frozen relative cutoff (1e-9, 1e-10, 1e-11):

| Map | Rank | Smallest retained singular value | Largest singular value |
| --- | --- | --- | --- |
| Stacked Q | 36 | 0.6039023948443148 | 18.4548375507729 |
| Stacked E | 36 | 2.902360260112841 | 113.70417299250616 |

Appending the 27 independently evaluated hidden-output columns preserves rank 36. Those columns are exactly zero in this computation. The resulting 63-column null-projector agrees exactly, at recorded precision, with the hidden-sector coordinate projector.

For 27 independent hidden input columns, the unrestricted linear hidden-response operator therefore has observation rank 972 and kernel dimension 729 by tensor multiplicity. These numbers count source-operator coefficients, not rotational dimensions or parameters of the CPTP cone. The retained edge rotation observable remains nine-dimensional per probe and state.

## Physical pointwise counterexample

The channel is fixed once, using the v15.71 symmetric lift Y_ref at candidate 13:

Phi(z)=Tr(z)I/8+.01 Tr(XXX z)Y_ref.

It is explicitly measure-and-prepare, with POVM elements (I±XXX)/2 and output states I/8±.01Y_ref. These output states have minimum eigenvalue 0.12199117994021896. The source family T_s=(1-s)id+sPhi is CPTP for 0<=s<=1; numerical finite checks use s=.1. The construction deliberately uses the reference geometry to exhibit a counterexample, and is not proposed as a source law derived from recoverability.

Its hidden derivative has retained HS coefficient norm **0.01732050807568877**. At the frozen anchor:

- Q norm: 5.068185584016187e-18.
- E norm: 1.859307323100497e-17.

On the other eleven states, keeping exactly the same channel and Y_ref:

- Combined Q norm: 0.1890185638354506.
- Combined E norm: 1.0005796027341056.
- Individual Q norms range from 0.03662040834485292 to 0.07059412437063628.
- Individual E norms range from 0.17881632250141244 to 0.5244094521112953.

The secondary gate required aggregate non-anchor visibility; all eleven happened to be visible individually. The verdict's word ONLY denotes the distinction between pointwise nullity and nullity across this ensemble. It does not claim the anchor is the unique null state in the full quantum state space. Nor does an infinitesimal null imply finite-strength rotational invariance.

The depolarizing reset control had analytic retained closure (numerical retained coefficient norm 8.326672684688674e-17), and the entangling channel control had hidden-response Q/E rank six on every state.

## Numerical and channel validity

All 972 channel/state/hidden-probe finite cases passed. Each Phi and its T_.1 update passed the frozen Choi and trace-preservation tests. The pointwise channel's Choi minimum eigenvalue was 0.12199117994021896, and T_.1's was 0.012199117994021512. The entangling channel had Choi eigenvalues as low as -1.9230160511781253e-15 across Phi/T, consistent with roundoff around its exact zero eigenvalues and within the preregistered -1e-12 tolerance; this is not a scientific failure.

- Largest channel TP error: 5.978733960281817e-16.
- Engineered Choi versus analytic formula: exactly zero discrepancy.
- Measure-and-prepare reconstruction error: 9.813077866773595e-18.
- Mixture-affinity error: 6.284194755995331e-17.
- Positive-strength hidden secant versus Lh: 2.2051352654711234e-12.
- Direct global versus retained-map response error: Q 1.3322676295501878e-15; E 1.0658141036401503e-14.
- Maximum Sylvester residual: 1.4802072481531892e-14.
- Minimum finite density eigenvalue: 0.03831621266594478.

No negative source strength was treated as a physical channel. No finite-output polar domain was needed, because the scientific observable is the analytic derivative at the frozen base states.

## Analytic statement and boundaries

The preregistered proof in DERIVATION.md removes the Hamiltonian assumption from v15.74's first argument. For fixed affine X(rho)=L(rho)+b, Y_h=L(h) is independent of rho. Requiring O^T D to remain symmetric while independently varying polar factors and Bloch vectors in a full-dimensional physical neighborhood forces all one-body and pair moments of Y_h to vanish. Thus open-state rotational nullity is equivalent to L preserving the hidden tangent sector.

The open-state theorem is analytic; the finite stack is a numerical witness that these particular states suffice. Neither substitutes for the other. Affinity alone does not remove pointwise symmetric-null freedom, as the fully CPTP counterexample shows. The theorem does not classify CP constraints inside the hidden-preserving class, select a physical interaction, apply automatically to a lower-dimensional admissible-state manifold, or cover state-dependent nonlinear/conditioned laws as fixed affine maps.

This narrows the source question but derives no gravity, fundamental time, source-to-admissible-world law, external alignment, fitted explanation, or new matter primitive. Genesis Pin remains foundational. All historical verdicts remain intact. The next operational question is whether a physical pointwise-null assignment can survive composition with the source data held fixed; this gate does not claim finite-composition invariance.

## Exact execution evidence

Parent certified head: `7d6f4cf42cc7165da7861aae4b0a4ee8184927a2`.

Preregistration, theorem and tests: `f4ae0ef48cb49ce95287bc47062b4b1b0715b18e`.
[Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36322638158): job `108629296358`, artifact `10931974620`, SHA-256 `3649defe504f6ec1d9eac7618a0e3af0430760026870adbddf2f09241dd8c8d9`. Setup passed; the sole error was the intended missing-implementation assertion. Downloaded archive, execution head and frozen source bytes were verified.

Tested implementation: `379675777abdd72361da001812f49f4febe822e9`.
[GREEN run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36322874417): job `108629965102`, artifact `10932906971`, SHA-256 `71a2f6692146af9075afde36744ac7dc16f41f9f22ef53275cb5ccd545be9251`. All three tests passed. The standalone result explicitly contains both scientific verdicts above and all_valid=true. Exact job logs were retrieved and inspected. The downloaded artifact digest, execution SHA, source byte identities, and all SHA256SUMS entries were verified. Independent read-only review checked the proof and implementation before publication. No implementation correction or criterion change was required.

Raw result SHA-256: `e9128668f7c48c127e92de6484ffef1fa1b551824363f8c654d58b25703b5710`.

RESULT.json.gz preserves the exact raw CI result, including retained maps, spectra, projectors, reference lift, channel retained maps, Choi spectra and channel responses. SUMMARY.json is a readable reduction. EVIDENCE.json records the compressed digest and Git blob, and TEST_LOG.txt and SHA256SUMS preserve CI validation. Decompress with `gzip -dc RESULT.json.gz > result.json` and verify the raw digest.

Reproduce at the tested SHA with Python 3.11, numpy==2.3.5 and OPENBLAS_NUM_THREADS=1 using `.github/workflows/uqcf-affine-open-null.yml`. Documentation is published in an additive later commit, identified by its containing Git commit rather than a circular self-hash. No merge to main.
