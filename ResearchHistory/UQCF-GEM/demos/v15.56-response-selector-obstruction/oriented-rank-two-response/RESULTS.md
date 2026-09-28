# v15.93 — oriented rank-two response

Both preregistered scientific verdicts are confirmed:

- **ORIENTED_RANK_TWO_READOUT_CONFIRMED**
- **PLANAR_ORIENTED_RESPONSE_CONFIRMED**

All four tests, 14 exact checks, 36 state/source cases, 108 retained edges and 2,916 edge/direction derivative checks passed. `all_valid=true`. No implementation fix, scientific criterion change, or domain exit occurred.

## Scientific result

Rank-two retained correlations support a unique proper rotational completion **once the endpoint Bloch SO(3) orientation is specified**. With V the support polar partial isometry,

\[
R=V+\operatorname{cof}(V)
\]

agrees with the observed support and lies in SO(3). It is covariant under independent proper endpoint frame changes. The rank-two Sylvester operator on skew matrices is invertible, despite the zero eigenvalue of P=R^T C.

Applying this explicitly specified extension to the same planar outputs that v15.92 excluded from its nonsingular readout gives:

| Source arm | Cases | Q rank | Rotational derivative E rank |
|---|---:|---:|---:|
| Coherent lambda=-1 | 12 | 2 | 2 |
| Incoherent lambda=0 | 12 | 0 | 0 |
| Coherent lambda=+1 | 12 | 2 | 2 |

All ranks agree at the three frozen thresholds. Coherent edge ranks are 0,1,1 on edges (0,1), (1,2), (2,0): one planar rotational direction survives on each active edge. Coherent E norms range from 1.2650251922767568 to 2.0850701109464533. Maximum incoherent E norm is 1.5367022269634117e-19; maximum incoherent Q norm is 8.11335436124542e-21.

Thus full three-dimensional preparation span is **not necessary for this oriented rotational readout**. The planar output remains fully separable and arises from the same entanglement-breaking preparation channel certified in v15.92. Source-law information remains visible in the retained skew sector. This is an existence result for the specified channel and readout, not universal sufficiency of noncommuting preparations.

## Relation to the earlier verdict

v15.92 remains correct within its frozen nonsingular domain. It stored no O/Q/E for singular cases; it did not measure a rotational null there. v15.93 adds a separately preregistered domain and readout. It neither revises that historical verdict nor claims uniqueness under arbitrary O(3) frames. At rank one, two distinct proper completions and a nonzero skew Sylvester kernel provide the exact ambiguity control.

The proper completion is a derived geometric readout, not recovery of an erased quantum degree of freedom. No inverse of the preparation channel has been constructed. Composition/naturality of this readout under successive retained restrictions remains open here.

## Numerical and exact evidence

- Smallest positive retained singular value: 0.002489524304201351.
- Smallest skew Sylvester denominator: 0.0024895243042013524.
- Worst completion residual: 2.7911101418675155e-15.
- Worst Sylvester residual: 1.7679157666498415e-16.
- Independent signed planar formula discrepancy: 2.1455863219007447e-15.
- Worst covariance residual: 1.7829638167186684e-14.
- Worst final-rung matrix finite-difference error: 6.09827784462965e-9, below the frozen 1e-6 limit.
- Minimum physical input eigenvalue: 0.038316212665944815; minimum source/output probe eigenvalue: 0.04182518541298883.

All 108 measured planar blocks have positive determinant. The reflected branch is covered by the exact negative-sign angle certificate and the hand-specified negative-determinant completion unit test, not by a claim that reflected physical cases were sampled.

The three finite-difference worst errors are 5.888939073521333e-10, 1.7214400746430536e-9, and 6.09827784462965e-9. The gate checks absolute derivative agreement, not monotonic asymptotic convergence; the small-step error increase is not converted into a scaling claim. These probes differentiate C+epsilon*dC in matrix space, separately from the physical density-operator checks.

Choi eigenvalues down to -1.7471890105403852e-15 are within the frozen -1e-12 numerical tolerance. No eigenvalue clipping or threshold adjustment was used. Independent derivative extraction agrees with T*dC_source*T^T to 2.7755575615628914e-17, and recomputed centers match the archived correlations exactly.

## Reproduction and immutable provenance

- Branch: `research/v15.93-oriented-rank-two-response`
- Certified parent: `59b40b60802b70b9cc57c3091e3d6deb9dc04cfb`
- Preregistration/tests: `c52c287c6208345611c058d11ba6e05f01757326`
- Tested implementation: `53e48385f863b5cc02444773ab8249764f537fb7`
- [Expected RED run 36365607262](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36365607262), job `108751285280`, artifact `10947191947`. Setup passed; the explicit absent-implementation assertion was the expected failure.
- RED ZIP SHA-256: `a9d5deff6cdfe12beb7149d4b61d43f9101131b3614e6e0840bb435c74dca676`.
- [GREEN run 36365855854](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36365855854), job `108751998058`, artifact `10947308100`.
- GREEN ZIP SHA-256: `7eab2076d6e556e9c5aff4662ac1689b7a95efc6317f14e7583a3a97251b5d41`.
- Full JSON SHA-256: `540f46f32bf8f74ad2c4283870d14f36427b16d0155444546e7113cedd26cd2a` (4,187,439 bytes).
- Lossless gzip SHA-256: `4c3e4d893c69f1a72a5409f905a1eafa81d4a0295b10439a0643ed21ba1dcc09` (169,051 bytes).
- Gzip Git blob: `d2e1d95fbc59e8377cd027698008979c3a49b74e`.

Both exact job logs and downloaded archives were inspected. Execution heads, frozen source bytes, implementation and all artifact SHA256SUMS entries were verified. The GREEN log's scientific JSON has the same SHA-256 as the artifact after removing timestamp headers and optional log-chunk BOM. RESULT.json.gz is a lossless copy; SUMMARY.json is derived. SHA256SUMS retains the artifact filename `result.json`. The dedicated workflow pins the numerical dependencies; run the four-test suite and gate.py from this directory in a complete repository checkout.

The documentation commit containing this file has the tested implementation as its sole parent. Its own SHA is recorded by Git history and the completion report, avoiding self-reference. No merge to main.

## Interpretation boundaries

This does not establish source-update composition, an identity-anchored preparation flow, a uniquely selected physical source law, universal geometry response, or gravity. It makes no novelty claim for polar/cofactor or Sylvester mathematics. Source-dependent effective measurement effects may be nonlocal. Genesis Pin and ordered recoverability framing are unchanged; no fundamental time or geometry primitive has been introduced. All earlier scientific NOs remain preserved.
