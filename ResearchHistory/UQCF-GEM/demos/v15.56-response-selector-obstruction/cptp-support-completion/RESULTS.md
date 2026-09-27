# v15.86 — unique CPTP support completion requires the missing direction

The preregistered gate returned **UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED** and **DISCARDED_DIRECTION_RESTORATION_CONFIRMED**, with `all_valid: true`. Three tests passed. All eight exact symbolic checks passed. No thresholds, source data, or scientific criteria changed after preregistration.

## What was learned

For a real rank-two partial isometry L with singular values (1,1,0), let P=L^T L. Among all qubit trace-preserving affine maps r -> T r + t satisfying T P=L, the unique CPTP map has

    t=0,  T=R=L+cof(L).

Thus exact isometric preservation of two independent Bloch directions forces a unitary completion of the third. It cannot also erase that third direction. The cofactor is constructed directly from the retained operator; no rotation was fitted and no external alignment was used.

The universal uniqueness statement follows from the exact argument in [DERIVATION.md](DERIVATION.md), with independently constructed symbolic Choi coefficients checked in the implementation. Positivity of the two antipodal unit-length outputs first forces t=0. In proper input/output coordinates, the remaining column is (a,b,c). A Choi diagonal and the Bell-minus expectation force c=1; a principal minor then forces a=b=0. Finite parameter controls corroborate this proof but do not establish universal uniqueness on their own.

## Inherited-loop measurement

Candidate 46's certified rank-two loop was used unchanged at 80-digit precision. Its completion has determinant 1, orthogonality error 8.44e-81, and retained-plane agreement error 4.22e-81. Three representations of the same retained plane agree on the completion within 1.06e-80.

| Map | Unnormalized Choi spectrum, rounded | Verdict |
|---|---|---|
| Original zero extension L | (-0.5, 0.5, 0.5, 1.5) | NON_CP |
| Proper completion L+cof(L) | (0, 0, 0, 2) | CPTP |
| Improper completion L-cof(L) | (-1, 1, 1, 1) | NON_CP |

The completed map's smallest numerical Choi eigenvalue is -4.62e-81, within the frozen -1e-40 numerical tolerance; eigenvalues were not clipped. Its spectrum agrees with the unitary-channel spectrum within 4.62e-81.

For the antipodal pair on the missing input axis:

| Quantity | Trace distance |
|---|---|
| Input pair | 1 |
| Outputs under L | 1.97e-81 (numerical zero) |
| Outputs under R | 1 |

The change R-L has Frobenius norm 1 and vanishes on the retained plane within 3.57e-82. Its input and output normal-projector identities hold within 8.44e-81. The inverse channel induced by R^T recovers the action on all four matrix units within 4.22e-81.

“Restoration” names the action supplied by the alternative completion. It does **not** mean applying a recovery after L and recovering information already erased by L. The completed channel never performs that erasure. Its invertibility follows because the map itself has changed.

## Controls and validity

The frozen canonical ladder c=(-1,0,0.5,1,1.5) classified as (NON_CP,NON_CP,NON_CP,CPTP,NON_CP). Its spectra agree with the analytic formula within 2.11e-81. Identity and complete Z dephasing are distinct CPTP channels that agree on the single Z axis; their outputs for +X and +Y differ by trace distance 0.5. This confirms that one preserved axis does not force the same rigidity. The zero extension is positive on the Bloch ball but fails complete positivity.

Pinned-parent reconstruction error was 7.38e-81. Choi Hermiticity, trace preservation and action reconstruction errors were zero at working precision. Tested state trace errors were at most 1.06e-81; the minimum state eigenvalue -3.69e-81 is numerical roundoff within the frozen tolerance.

Preimplementation review caught a duplicated eigenvalue in the draft synthetic formula; it was corrected **before** preregistration commit and before any measurement. No frozen formula or criterion was subsequently changed. Implementation review found no important defects.

## Exact provenance

- Branch: `research/v15.86-cptp-support-completion`.
- Certified parent documentation: `c0adc88d4ef2b955a07d567b4cf2c3ab3d1fa24d`.
- Preregistration/tests commit: `cb99eb7b79044be8afbd7ce35a7abd27aaef3988`.
- Expected RED: [run 36354920501](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36354920501), job `108720633832`, artifact `10944035055`. Setup succeeded; tests stopped at the explicit absent-implementation assertion.
- RED ZIP SHA-256: `3fc60650da4ca8d006eb9e4d498d04f546e23e891938a1cf6540dee8580d8e4e`.
- Tested implementation commit: `6711b3f2b2ba89a66d8de811f7a705581ccf9073`.
- GREEN: [run 36355131725](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36355131725), job `108721247570`, [artifact 10942774856](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36355131725/artifacts/10942774856).
- GREEN ZIP SHA-256: `f61ccd8a89039a5c366f07c001551231e115eb3270e242d1786d607b60660bd4`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `7e0df41086ed226c90a22e09270f305e3de68abfe5d1d6a9e5811598c324090d`.

Exact job logs and downloaded artifacts were inspected. Both ZIP digests, execution heads and preregistered source bytes were verified; all GREEN SHA256SUMS entries matched. SHA256SUMS retains the artifact name `result.json`; identical bytes are committed here as `RESULT.json`. The subsequent documentation commit does not change the tested implementation.

## Scientific boundary

This is a rigidity result for exact isometric retention of a two-dimensional Bloch plane. It does not extend unchanged to arbitrary contracted planes, where physical lossy channels can exist. It also does not establish that retained geometric transport must itself be a qubit channel: that interpretation remains conditional.

v15.85's all-affine-shifts obstruction for the **fixed full** linear map remains true. This experiment allows a different full linear map. The source law has not been selected; no connection to gravity or alteration of admissible worlds has been derived. No fundamental time is introduced. Genesis Pin and all historical NOs remain intact.

The resulting constraint is precise: in this qubit interpretation, a physical channel cannot preserve the entire retained plane isometrically while genuinely erasing its missing direction. A model requiring erasure must relax exact retained-plane isometry or justify a different operational interpretation of the retained transport. No claim of continuous full polar transport across the v15.82 boundary follows.

No merge to main.
