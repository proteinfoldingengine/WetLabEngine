# v15.94 — oriented completion requires compatible intermediate supports

The frozen scientific verdicts are:

- **ORIENTED_COMPOSITION_OBSTRUCTED**
- **MATCHED_SUPPORT_COMPOSITION_CONFIRMED**

`all_valid=true`. Four tests, 12 exact checks and all three rational controls passed. The gate evaluated 108 planar pairs, 36 planar triples, and the single archived native loop composed with itself. No scientific threshold or frozen file changed after preregistration.

## What was learned

A unique, frame-covariant completion at each link does not ensure that completion commutes with composition. For rank-two partial-isometry factors A and B, let

\[
P_A=A^TA,\quad Q_B=BB^T,\quad
c=\sqrt{\operatorname{tr}[(I-P_A)(I-Q_B)]}.
\]

For c>0, AB remains rank two and the oriented completion F obeys

\[
\boxed{\|F(AB)-F(A)F(B)\|_F^2=4(1-c).}
\]

Therefore completion preserves composition exactly when the intermediate support planes match: P_A=Q_B. At c=0 the product has rank one and this prescription has no unique full rotation. Ordinary matrix multiplication remains associative in all cases.

This identifies a precise additional structural condition for this readout, rather than merely another example of nonclosure. The theorem concerns partial-isometry factors; arbitrary rank-two correlation matrices can also contain stretch effects and are outside this equivalence.

## Native obstruction and matched controls

The v15.83 loop L is retained as archived, with no factor normalization or support adjustment before multiplication. Its initial and final planes differ. For A=B=L:

| Quantity | Measured value |
|---|---:|
| Normal-overlap cosine c | 0.4854199762520051 |
| Product singular values | approximately (1, 0.48541997625200517, 0) |
| Intermediate projector gap | 1.2364201928596141 |
| Completion discrepancy | 1.4346846674415872 |
| Squared discrepancy | 2.0583200949919775 |
| Predicted squared discrepancy | 2.0583200949919798 |
| Formula error | 2.220446049250313e-15 |

The discrepancy is far above the frozen 1e-6 obstruction threshold. The product still has rank two at all three rank thresholds; this is a failure to preserve composition, not disappearance of the surviving support.

All 108 planar pairs and 36 triples inherited from v15.93 have matching intermediate planes and remain rank two. Their worst completion discrepancies are 1.7728839976828627e-15 for pairs and 1.7073627510943655e-15 for triples. Maximum support-plane gap is 2.249282079202031e-15, within the frozen 1e-9 tolerance.

The rational tilted-plane control gives c=3/5 and squared discrepancy 8/5. The matched control gives zero discrepancy. The orthogonal-normal control gives rank one and correctly retains null completion fields; the completion routine rejects that domain.

## Verification and interpretation

Worst residuals: factor partial-isometry condition 1.6911283707644368e-15; predicted spectrum 1.1102230246251565e-15; proper-completion identities 2.4547120262592922e-15; frame covariance 2.245469381366487e-15; raw associativity 2.2291027918243403e-16. The native squared loop agrees with its archived v15.83 power to 1.1897724610717036e-16.

This calculation converts the stored 80-digit v15.83 loop entries to float64 and validates their factor identities. It does not recertify the root at high precision. The v15.93 planar factors are also used exactly as archived before multiplication. Scalar normal-overlap squares alone may be bounded to [0,1] within the explicitly frozen roundoff allowance; no eigenvalues, factors or products are repaired.

Pre-run implementation review caught and corrected domain guards: rank-two-only formula checks now stay null outside their domain, and transformed products are checked before completion. Those corrections occurred before the first scientific run and changed no preregistered criterion. The published implementation passed its first scientific CI run. No unexpected scientific result required reinterpretation.

These are spatial retained-map compositions at a fixed ordered slice, not sequential quantum source updates. Physical-state and channel certifications are inherited through the pinned parents; this gate creates no new density operators or channels. The result does not falsify CPTP composition, recover erased quantum data, choose a physical source law, or derive gravity. Pointwise covariance and unique proper completion remain earned, but do not confer unrestricted compositional naturality. All prior verdicts, including scientific NOs, remain unchanged.

## Exact provenance and reproducibility

- Branch: `research/v15.94-oriented-composition-compatibility`
- Certified parent: `aee440c43996f9a14cc4973473aa403ed9eeb01e`
- Preregistration/tests: `d412b999134d598086bbeb639bd0cc75caaa6a49`
- Tested implementation: `9513de533d442d07400b3e6827f8a424cd4392ab`
- [Expected RED run 36366677105](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36366677105), job `108754359100`, artifact `10946913966`. Setup passed; only the explicit absent-implementation assertion failed as expected.
- RED archive SHA-256: `799ced164677876b4b4d5e68455d92d0385aefc339a2abe2689d4309941fb4db`.
- [GREEN run 36367019577](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36367019577), job `108755342941`, artifact `10947633397`.
- GREEN archive SHA-256: `f0eae55735875d371637a39b515294a58dc635505a7120d11268fb6a3d44067f`.
- Full JSON SHA-256: `7c9fc2bf42316e366d059e7b45d2aa8ebdeb11947a5b7593c4808de608a8e6b4` (691,755 bytes).
- Lossless gzip SHA-256: `627e9ac50b1ead13f76036965f020db19c85f5287f669e9a23f1a589118cc04a` (64,075 bytes).
- Gzip Git blob: `9f190177080b1193b24fb775fdda4086bfa89861`.

Exact job logs and downloaded artifacts were inspected. Archive digests, execution heads, frozen sources, implementation and every SHA256SUMS entry were verified. Scientific JSON extracted from the GREEN log has the artifact's exact SHA-256 after timestamp/optional log-chunk BOM removal. RESULT.json.gz preserves the raw result losslessly; SUMMARY.json is derived. SHA256SUMS retains the artifact filename `result.json`.

Reproduce using the pinned dependencies and commands in `.github/workflows/uqcf-oriented-composition-compatibility.yml` from a complete checkout. The additive documentation commit containing this file has the tested implementation as its sole parent; its own SHA is supplied by Git history and the completion report. No merge to main.

Geometry remains derived from retained structure. Genesis Pin and ordered recoverability framing remain unchanged. No external alignment, fitted support, fundamental time or dark-matter primitive is introduced. No novelty claim for the underlying polar/principal-angle mathematics is made.
