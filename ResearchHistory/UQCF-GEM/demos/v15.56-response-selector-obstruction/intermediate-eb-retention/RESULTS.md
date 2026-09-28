# v15.99 — intermediate EB retention: INVALID

Both preregistered verdicts are **INVALID**. The mandatory native/transformed rank-covariance control failed. There is no GREEN run, and no threshold, amplitude, state, source, or scientific predicate was changed to obtain one.

The native response-scaling predicate and complete-erasure predicate individually evaluate true. These do not override validity. This is an unresolved numerical validation failure, not a certified physical obstruction to retained response through an entanglement-breaking (EB) cut.

## Exact provenance

Repository: proteinfoldingengine/WetLabEngine. Branch: research/v15.99-intermediate-eb-retention. Main was not merged.

| Item | Exact identity |
|---|---|
| Certified parent | 3a3655a5c5bd263b8986a651b9c9ef23bda0c306 |
| Preregistration/tests | fad2d16aae746ed70e505a6902939591a9519922 |
| Initial implementation | 64e7ad9852d7c4fb3efe6acba19c29cdc76d839b |
| Tested diagnostic implementation | 00b1ba5c2dfdb47539c96004ded850c950dd7e0e |
| Expected RED run / job / artifact | 36375520791 / 108780443501 / 10950658108 |
| Initial measurement run / job / artifact | 36375832861 / 108781359058 / 10950982206 |
| Diagnostic measurement run / job / artifact | 36376165703 / 108782334443 / 10951660106 |

[Expected RED](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36375520791), [initial measurement](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36375832861), [complete diagnostic measurement](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36376165703).

The expected RED was the explicit absent-implementation assertion. The initial implementation completed its measurement inside the test, then failed the rank-covariance validity assertion. Its workflow stopped before emitting a standalone full JSON. That original artifact and INITIAL_TEST_LOG.txt are preserved; a full first-run JSON is not claimed.

The diagnostic commit changed only evidence capture: it archives already-computed transformed singular values and emits JSON/checksums even when tests fail, retaining a failing exit status. Its arithmetic and all frozen criteria are unchanged. The complete RESULT.json.gz belongs to this separate diagnostic execution. The four frozen tests report three passes and one failure in 68.955 seconds.

| SHA-256 object | Digest |
|---|---|
| Expected RED artifact ZIP | 1096caaa16054e42b001ae303e38028209e5e5a28f268c962736cbec65e77df1 |
| Initial measurement artifact ZIP | e998847cd1b26466200dcecd0026143d618cf45052f16e85d3837db9c6a5b832 |
| Diagnostic artifact ZIP | 040b467bd1fb04f7ddf75dfc89e7ff78e7404bbc0a815291385bd5a8fdf5013f |
| Diagnostic gate.py | ba44a36fbef8923baf0b2c274fadc1dcc6b65c4f6bff848ff6c8ce0f6d32a56c |
| Raw result JSON | 8107f3f6ac83b08ba9ff9490d56518a10ca823f9bd92a290adf418cc79d9ebbb |
| RESULT.json.gz | 84865667bf0a1987d919450eddf41751feb27ace640c99815592ebb65122eac9 |

All three downloaded archive digests, execution heads, and frozen source files were verified. Every diagnostic manifest checksum matches both the artifact and exact job log. The log explicitly prints both INVALID verdicts. Raw JSON is 18,789,502 bytes; deterministic gzip is 2,376,079 bytes. EVIDENCE.json, SUMMARY.json, SHA256SUMS, and test logs provide the compact audit trail.

## What was measured

The frozen 12 four-qubit states, all 81 weight-four hidden directions, overlapping/disjoint source pairs, both orders, and two final preparations give 192 rows. The intermediate channel is M_a = D_a tensor4 with a = 1, 1/3, 1/6, 0. There are 144 positive-a rows and 48 complete-erasure rows. Native responses were independently recomputed; parent matrices were predictions only.

All eight new exact checks and 74 inherited checks passed. The six-outcome local measure-and-prepare representation, tensorized to 1296 outcomes, matches the intermediate map on all 256 matrix units at each EB value. All 108 unique finite intermediate centers reconstruct with maximum error 9.71445e-17. Physicality checks cover 344,604 density evaluations, minimum eigenvalue 0.023220735045541896.

The sparse Pauli calculation establishes that only first-source weight-three terms contribute to the eventual retained pair derivative. Thus the pair derivative scales as a cubed, while baseline connected correlations scale as a squared. The analytic positive-a prediction is K_a = a K_parent and J_a = a J_parent. Across native responses, maximum normalized residuals are 2.35364e-13 for K and 2.93320e-13 for J. All native rank lists match the parent. No positive-a domain exit occurred.

Complete-erasure errors are at most 4.16334e-17. All 48 erasure rows correctly keep the polar responses undefined; they do not manufacture rank-zero K/J.

## Failed control and interpretation

Eight of the 432 native/transformed response comparisons disagree at the strictest frozen rank threshold, 1e-11. They occupy four of the 144 positive-a rows. All disagreements concern planar K; all J rank lists agree. The other frozen thresholds, 1e-9 and 1e-10, agree in these cases.

| Candidate | a | Pair | Responses | Native K rank | Transformed K rank at 1e-11 | Extra singular value |
|---|---|---|---|---|---|---|
| 66 | 1 | overlapping | reverse, contrast | 1 | 2 | 1.32779e-11, 1.32370e-11 |
| 66 | 1/3 | overlapping | reverse, contrast | 1 | 2 | 1.08614e-11, 1.08594e-11 |
| 66 | 1/6 | overlapping | reverse, contrast | 1 | 2 | 1.57882e-11, 1.57970e-11 |
| 77 | 1/6 | disjoint | forward, reverse | 2 | 3 | 1.89480e-11, 1.89507e-11 |

The extra singular values are tiny compared with the order-units/tens active singular values. Absolute covariance residuals still satisfy their separate 1e-9 bound: maximum 2.41587e-11. Every scalar validity tolerance passes. Finite channel agreement is 2.40148e-10; affine derivative errors are at most 1.22026e-8 for K and 1.67948e-8 for J.

This pattern is consistent with numerical leakage into planar null directions, but does not identify or certify its computational cause. Candidate 66 also fails for the identity middle channel (a=1), so the failure cannot be interpreted as an EB-induced physical obstruction. Passing a looser covariance norm does not waive the independently frozen rank criterion. Both final verdicts remain INVALID.

The global disjoint mixed order contrast is nonzero with insertion (norm 0.2793508271 at a=1/3 and 0.0436485667 at a=1/6), although the retained contrast remains null within its frozen controls. Original disjoint-source commutation therefore must not be promoted to commutation of the inserted protocols.

## Boundary and next research step

The exact channel/algebra results and observed native scaling narrow the numerical issue, but this run does not certify the complete EB response gate. A separately preregistered precision/identity audit of the eight failing comparisons is the next appropriate step. It must retain this INVALID history and avoid tuning rank thresholds.

The intermediate EB map removes entanglement with an arbitrary reference and gives fully separable intermediate states; positive a still preserves attenuated operator coefficients. The second source may recreate internal entanglement. No fully classical process, universal physical source law, or gravity derivation is claimed. Source strengths and composition order introduce no fundamental time; geometry remains extracted from retained correlations. Genesis Pin and earlier verdicts are unchanged.

## Reproduction

Check out tested commit 00b1ba5c2dfdb47539c96004ded850c950dd7e0e, install the versions in the dedicated workflow, set OPENBLAS_NUM_THREADS=1, and run test_gate.py or gate.py in this directory. The frozen test suite and gate intentionally return nonzero for this recorded INVALID outcome. gate.py writes complete JSON before returning status 2. RESULT.json.gz can be decompressed independently and checked against the raw hash above.
