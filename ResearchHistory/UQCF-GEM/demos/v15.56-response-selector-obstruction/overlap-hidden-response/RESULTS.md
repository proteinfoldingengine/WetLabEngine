# v15.97 — hidden source response of overlapping loops

**OVERLAP_HIDDEN_RESPONSE_CONFIRMED** and **PLANAR_TWO_LOOP_RESPONSE_CONFIRMED**. The archived JSON reports all_valid=true. All 72 state/source/arm rows and every finite stencil remained inside the frozen rank domains. No threshold, amplitude, state, probe or criterion was changed after preregistration.

This gate measures the source-origin mixed derivative, rather than the baseline loop structure measured in v15.96. The specified source converts pair-invisible triple-body perturbations into independent changes of both loops, including changes of simultaneous-conjugation invariants.

| Frozen group | Cases | Rotational K rank | Invariant J rank |
|---|---:|---:|---:|
| Isotropic, coherent lambda=±1 | 24 | 6 | 3 |
| Planar, coherent lambda=±1 | 24 | 2 | 2 |
| Isotropic, incoherent lambda=0 | 12 | 0 | 0 |
| Planar, incoherent lambda=0 | 12 | 0 | 0 |

All ranks hold at thresholds 1e-9, 1e-10 and 1e-11, with fixed reference 1, in both native and independently transformed frames. K is a 6x54 mixed-response matrix in left-trivialized rotational coordinates. J is a 3x54 derivative matrix for (tr H1, tr H2, tr(H1 H2)); it measures frame-invariant changes. The 54 probe coordinates are orthonormal normalized four-qubit Pauli triples, not the earlier 243 hidden/source domain.

The smallest nonzero isotropic singular values ranged from 34.376252719312106 to 51.89588209861144 for K and from 4.570951983851757 to 74.31609070824598 for J. Planar ranges were 36.092743975206396–58.1704621814944 for K and 35.268496906061166–97.74340085077655 for J. These ranks are well separated from the frozen numerical cutoffs. Magnitudes depend on the explicitly frozen source/probe normalization and are not physical coupling constants.

## Mechanism and controls

The coherent isotropic cases have edge ranks (0,3,3,3,3) in order (01,12,20,13,30), with rank 3 in each loop. The planar cases have (0,1,1,1,1), with rank 1 per loop. Cross-loop blocks vanish: the 012 probes affect only the first loop and the 013 probes only the second. The 54 probes are invisible to every retained pair before the source; they are visible to their corresponding full three-site region.

All 81 weight-four directions remain pair-invisible under this source confined to sites 01. The largest measured generator pair-leakage residual for this null is 5.551115123125783e-17. The exact trace/support argument explains the null. The local-Hamiltonian control has exactly zero pair leakage. Incoherent K and J norms are at most 4.832612554610857e-14 and all their ranks are zero. Thus more globally hidden information is not automatically more geometrically responsive; the specified source's support and cross terms matter.

At u=0 the source is identity, while preparation remains present. All baseline hidden geometric finite differences have norm at most 5.6307061135791055e-11, below 1e-9. Lambda=0 at a positive source strength is an incoherent source, not a no-source reference. The source-origin mixed derivative removes the baseline-versus-response ambiguity in v15.96.

Eight new grouped exact checks, thirteen inherited frame/geometry checks, forty-five inherited preparation checks and all four unit tests passed. Independent global-matrix connected derivative extraction agrees with the endpoint formula within 1.6653345369377348e-16. Maximum derivative identity residual is 1.5826894870868467e-13; response covariance residual is 6.077676116077465e-12, below 1e-9. Native/transformed K and J rank lists agree explicitly.

## Finite-state check

Direct finite evaluation used all 54 probes per row, epsilon=1e-4, and the preregistered positive source ladder. Both the loop matrices and invariant scalars were recomputed from the finite states. Worst normalized errors across all 72 rows:

| Source step | K error | J error |
|---|---:|---:|
| 1e-3 | 1.0130988146484181e-6 | 2.6459204967661152e-6 |
| 3e-4 | 3.864930095491634e-7 | 6.726603818954419e-7 |
| 1e-4 | 9.378195712519803e-7 | 1.914680115670492e-6 |

The final-step criterion was <=1e-4 for each matrix. Errors do not decrease monotonically; no asymptotic scaling claim is made. The frozen analytic ranks, not ranks of noisy finite-difference matrices, adjudicate the scientific hypotheses.

There were 110,160 density evaluations including repeated states across the two arms and source stencils. Minimum eigenvalue was 0.023230389831364853, maximum trace error 4.440892098500626e-16 and Hermiticity error 5.860711981579306e-18. Nonnegative normalized source weights and unitary conjugations, followed by the inherited exact measure-and-prepare maps, certify finite CPTP action. Both preparation arms have fully separable outputs. This adds no negative-strength physical source extension.

## Interpretation boundary

For this frozen constructed ensemble and source law, pair-hidden information produces six independent two-loop rotational tangent directions and three independent invariant responses in the isotropic arm. Restricting the local preparation span to a plane reduces the response to two independent loop angles. Output entanglement is not necessary for either result.

This is a mixed derivative at a specified source origin, not a selected physical source-to-admissible-world law. The four-qubit ensemble is deterministic and inherited, not a new held-out sample; no claim that this construction is necessary or that the result holds for all states is earned. The five-edge atlas is not a complete nonsingular six-edge atlas. Response ranks do not establish continuous SO(3) holonomy, gravity, a fundamental time coordinate or an external alignment mechanism. Geometry is extracted from retained correlations within ordered recoverability. Genesis Pin and earlier historical verdicts remain unchanged.

## Exact provenance and reproduction

- Certified parent: c61de02241acac20c02b50a76469ba63224a7b3e.
- Preregistration/tests: 93c8321af2b5c482ffc7f52cb30581c8a6abfab5.
- Expected RED: [run 36370883538](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36370883538), job 108766794220, artifact 10949375911. ZIP SHA-256 c091296a2602796990f0127c0a47683299cf7449cc9d918b4d4f4b7fc91c4a33.
- Scientific implementation: 8e515756902647b6f2ae9e577ab146f0c2d1703e.
- GREEN: [run 36371243514](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36371243514), job 108767890096, [artifact 10949361749](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36371243514/artifacts/10949361749). ZIP SHA-256 f00c82961760338fa3717c3b5555b66fdc2dcafcde270f200746e1b27d7426fe.
- gate.py SHA-256 a27a98a29c5dce4f286bd445072297228af903a348ee274a9c6bb7d15c986439.
- Raw result SHA-256 a16af3868ed4a0d959dda97eaea9c79f02f2beb0aa996b175a233463b9381891, 3,858,159 bytes.
- RESULT.json.gz SHA-256 5d211fb43db6ddd101be6d31391554b4e6720f09626255e85cc01da76d3179bc, 680,588 bytes, lossless gzip with mtime 0.

Both downloaded artifacts were verified against their ZIP digests, execution heads and frozen sources. The RED log contains the expected absent-implementation assertion. GREEN manifest checksums all match. The full scientific JSON extracted from the exact job log has the same SHA-256 as the downloaded artifact. The first scientific implementation passed; no post-measurement code repair or gate change was needed.

See EVIDENCE.json, SUMMARY.json, TEST_LOG.txt, SHA256SUMS and RESULT.json.gz. SHA256SUMS preserves original artifact filenames: decompress RESULT.json.gz to result.json to check its entry. Run the committed targeted workflow, or its commands under Python3.11/numpy2.3.5/sympy1.13.3/mpmath1.3.0 with one BLAS thread. Pre-run review added the explicit already-preregistered covariance rank-list validity check. This documentation is an additive child of the tested implementation; its own SHA is recorded by Git history and the completion report. No merge to main.
