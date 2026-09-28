# v15.96 — overlapping loops and the common-line obstruction

**OVERLAP_COMMON_LINE_OBSTRUCTION_CONFIRMED** and **PLANAR_COMMON_LINE_PRESERVED**. The archived JSON reports `all_valid: true`. All 72 cases remained in their original and transformed rank domains. No scientific criterion, state, source amplitude or tolerance changed after preregistration.

The 36 isotropic cases all have rank 5 for the stacked action on symmetric traceless tensors at each frozen threshold (1e-9, 1e-10, 1e-11). Thus their two based loops have no common invariant unoriented line. The 36 planar cases all have rank 4 and preserve their common normal line. The independently transformed output states reproduce these ranks.

| Original-frame measurement | Planar (36) | Isotropic (36) |
|---|---:|---:|
| Smallest singular value of B | 4.0438352948831645e-16–2.7304036353034662e-15 | 0.4979815452380838–1.6195926693152003 |
| Loop commutator norm | 5.862072599596872e-17–1.4547584839936504e-15 | 0.4526709849440536–2.5751129754113 |
| Rank at all three thresholds | 4 | 5 |

Noncommutation alone was not used to infer absence of a common line: the exact normal-flip control is noncommuting yet has rank 4. The quarter-turn control has rank 5. All 13 new grouped exact checks and 45 inherited exact checks passed, as did four unit tests, including scientific NO and INVALID adjudication controls.

## Physical and numerical evidence

Twelve deterministic four-qubit mixtures were constructed from cyclic pairs of the frozen states. These are globally positive mixtures, not cloned states or a new held-out ensemble. Their reduced regions 012 and 013 share edge 01 consistently. Five declared edges enter the two loops; the separately recorded spectator edge 23 has rank at most one and is not silently admitted into a nonsingular complete atlas.

Both local measure-and-prepare channels give explicitly fully separable four-qubit outputs. The plane arm has 256 product outcomes and the isotropic arm 1296; all center probabilities are archived. Pauli action and independent measure-and-prepare reconstruction agree on all 256 computational matrix units and all 72 centers. Nine dimension-16 Choi certificates passed. Minimum input/source/output eigenvalues are respectively 0.023238820210108396, 0.02688447081995684 and 0.054413329035132914. The smallest Choi eigenvalue is -7.616025668786442e-15, inside the frozen -1e-12 numerical bound; no threshold was adjusted.

Worst residuals: overlap 8.326758711027992e-17; regional correlation 9.71445146547012e-17; spectator formula 5.65170366985209e-17; geometry 1.519393075441413e-14; covariance 4.8533006107844434e-14; planar normal tensor 3.0432134437411643e-14. All satisfy their preregistered limits.

## What this earns

The fixed-plane common-line reduction established in v15.95 does not apply to every fully separable retained output: the isotropic preparation channel here supports two overlapping loop rotations with no shared invariant line. Entanglement of the output is therefore not necessary for this finite-loop obstruction. The links are extracted from retained correlations, not supplied as explanatory geometry primitives.

Rank 5 does **not** establish continuous SO(3) holonomy: a finite irreducible rotation group can also lack a common line, including the quarter-turn positive control. The gate measures baseline loop structure, not a hidden/source mixed derivative or a causal change relative to zero source. Lambda=0 is not a no-source reference at the fixed nonzero source amplitude. This is a deterministic constructed ensemble and a five-edge overlapping-region atlas, not a universal theorem about all states or a complete six-edge atlas. It selects no physical source law and derives no gravity. Ordered recoverability remains the framework; no fundamental time was introduced. Historical verdicts remain unchanged.

## Reproducibility and exact provenance

- Certified parent: `0bb9d708f1a793dc0020000426ede5391b8e76f9`.
- Preregistration/tests: `0e60d6b867e3b54898746983925e325513f9fbb4`.
- Expected RED: run [36369357144](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36369357144), job `108762175925`, artifact `10948498099`; ZIP SHA-256 `73f602d63c54b4840fe108b1c0e7bd128e73e709b1329f956582007cb90e4f21`. Downloaded archive confirmed the expected missing-implementation assertion, absent gate.py and frozen sources.
- Tested implementation: `d296c43f7ae7c807b092e2d2e0eee36b1ee44e3f`.
- GREEN: run [36369815339](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36369815339), job `108763557485`, artifact [10948054942](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36369815339/artifacts/10948054942); ZIP SHA-256 `cf02f6d9758212f9b8c702dfc87bcc64524c1a89de49413e7564b64ea3e84b5b`.
- gate.py SHA-256: `56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52`.
- Raw result SHA-256: `99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e` (3,160,359 bytes).
- RESULT.json.gz SHA-256: `1102dd9da14f82cc44d958de15effe9b0553e3b6cf396deb1791f98a88527550` (783,390 bytes, lossless gzip with mtime 0).

Exact job logs and downloaded artifact were inspected. Archive digest, execution head, every manifest checksum, and byte identity of preregistration/derivation/tests/implementation were verified. Timestamp-stripped result JSON in the job log has the same SHA-256 as the artifact JSON. The only pre-run review changes were enforcing the already specified SU(2) determinant condition and using the specified per-effect Frobenius Hermiticity check; neither changed the frozen scientific gate.

See EVIDENCE.json, SUMMARY.json, TEST_LOG.txt, SHA256SUMS and RESULT.json.gz. SHA256SUMS retains the CI artifact's original filenames; decompress RESULT.json.gz to result.json when checking that entry. Reproduce under Python 3.11 with numpy 2.3.5, sympy 1.13.3 and mpmath 1.3.0 using the committed workflow. This documentation is an additive child of the tested commit; its own SHA is recorded in Git history and the completion report. No merge to main.
