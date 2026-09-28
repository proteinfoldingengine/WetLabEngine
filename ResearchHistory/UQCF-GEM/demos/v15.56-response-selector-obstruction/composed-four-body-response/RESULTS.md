# v15.98 — composition exposes four-body information; order is distinct

**COMPOSITION_ORDER_GEOMETRY_CONFIRMED** and **COMMUTING_COMPOSITION_ACTIVATION_CONFIRMED**. The archived result reports all_valid=true. All 48 state/source-pair/preparation rows passed the frozen hypotheses; there were no baseline, transformed or affine-check domain exits. No thresholds, states, amplitudes or criteria changed after preregistration.

The main lesson is that two source actions can expose four-body information that neither action exposes to a pair on its own. Noncommutation is not necessary for this exposure. With overlapping sources, however, their order can carry an additional frame-invariant geometric response.

## Measured response

Each row uses all 81 exact-weight-four probes, which initially vanish on every proper region. K is the 6x81 rotational response of the two based loops; J is the 3x81 response of (tr H1,tr H2,tr(H1 H2)). The derivative is taken at the two-source origin with respect to both source strengths and one hidden-state coordinate. It is not a baseline geometry statistic.

| Source pair and preparation | Cases | Forward K/J | Reverse K/J | Order contrast K/J |
|---|---:|---:|---:|---:|
| Overlapping 01,12; isotropic | 12 | 2 / 2 | 3 / 2 | 3 / 2 |
| Overlapping 01,12; planar | 12 | 1 / 1 | 1 / 1 | 1 / 1 |
| Disjoint 01,23; isotropic | 12 | 6 / 3 | 6 / 3 | 0 / 0 |
| Disjoint 01,23; planar | 12 | 2 / 2 | 2 / 2 | 0 / 0 |

Forward means the source on 01 acts first. The order contrast is forward minus reverse at a common baseline. All ranks hold at every preregistered threshold (1e-9,1e-10,1e-11 with reference1), in native and transformed frames. The forward/reverse overlapping ranks are descriptive measurements; the primary preregistered rank target concerned their contrast. Both ordered disjoint responses were the secondary target.

The smallest nonzero singular values are well separated from the cutoffs:

| Gate matrix | K range across 12 states | J range across 12 states |
|---|---:|---:|
| Overlap contrast, isotropic | 34.30516106590298–56.19067140095793 | 3.8937379672220813–56.73115300661969 |
| Overlap contrast, planar | 44.47291914165704–69.28793855256129 | 54.41345570489413–171.79779915059265 |
| Disjoint forward, isotropic | 19.458838185787588–34.99028846803835 | 3.6846372482526313–56.57226729187144 |
| Disjoint forward, planar | 12.380484126714975–39.12542136178855 | 20.961914872678683–72.10549140065376 |

These magnitudes use the frozen probe/source normalization and are not physical coupling constants.

## Mechanism and null controls

For the overlap pair, the first loop remains null because both sources act only on 012 while every hidden probe has a traceless factor on 3. The second loop supplies the order-dependent response. For h=YYXX/4, the exact forward two-body component is -IXIX/4 and the reverse two-body component is zero.

For the disjoint pair the two global channels commute exactly, but each can reduce Pauli support. For h=XXXX/4 the two-body component after both generators is ZIZI/4. Hence exposure survives even though the order contrast vanishes. The maximum measured disjoint K/J order-null norm is 1.32572096968145e-13, with rank zero at all thresholds.

All individual-source pair nulls remain valid (maximum residual 5.551115123125783e-17). Controls with one or both sources incoherent remain pair-null (maximum 1.1102230246251565e-16). The earlier v15.97 single-source weight-four null is unchanged: the nonzero object here is the twice-applied generator.

Edge 23 is explicitly recorded as correlation leakage outside the five-edge geometry atlas. In the forward overlap protocol its prepared correlation-leakage map has rank 6 in the isotropic arm and rank 2 in the planar arm; the reverse protocol has rank 0 there. These are ranks of a 9x81 moment-response map, not rotational tangent ranks. Edge 23 is no longer an unaffected spectator, and no polar geometry on that rank-deficient baseline edge was introduced.

Eight new grouped exact checks and 66 inherited exact checks passed. Independent complex 16x16 generator action agrees with exact sparse Pauli coefficients within 4.440892098500626e-16. Maximum polar/loop derivative identity residual is 1.0586975950405484e-13; linear order-contrast consistency residual is 1.5354079400326221e-13; frame covariance residual is 7.714884556435152e-12. Native/transformed K and J rank lists agree.

## Finite validation

The finite channel identity was checked on global states rho±1e-4 h with both source strengths 0.1, using the exact factor s(u)=(1-exp(-2u))/2. The worst relative connected-correlation error after division by 2 epsilon s(u)s(v) is 1.2557378287627656e-10, below the frozen 1e-7 bound.

The separate affine tangent check used global states rho±1e-6 Y and direct recomputation of loops and their invariant scalars. Worst relative errors are 1.2513132766560372e-9 for K and 4.53337585769691e-9 for J, below 1e-5. These nearby states verify the derivative; the affine probe is not an added source law.

All 79,704 density evaluations passed, including repeated inputs, intermediate/final source states and prepared outputs. Minimum eigenvalue is 0.023220735045541896; maximum trace and Hermiticity errors are 4.440892098500626e-16 and 7.084579703514581e-18. Finite sources use nonnegative normalized random-unitary weights; inherited local measure-and-prepare maps certify fully separable final outputs. No claim is made that the intermediate states are separable.

All four tests passed. Both the finite retained-channel identity and the local polar derivative are verified. This does not establish persistence of the origin loop ranks at source strengths 0.1; no finite-strength polar-domain claim was preregistered for that channel check.

## Interpretation boundary

This gate separates two properties: composition can expose previously pair-invisible global information even when the source maps commute; noncommuting overlapping sources can additionally encode order in loop invariants. CPTP composition remains associative. The order contrast is a difference of two physical protocols, not itself a CPTP source.

The result concerns the specified source law, fixed deterministic ensemble, 81 normalized probes and five-edge atlas. It does not prove that every compatible source must respond, remove the symmetric-null freedom for all source laws, select a physical source-to-admissible-world coupling, establish continuous SO(3) holonomy, or derive gravity. Source strengths and composition order introduce no fundamental time. Geometry is extracted from retained correlations; no fitted alignment is used. Genesis Pin and all historical verdicts remain intact.

## Exact provenance

- Certified parent: 903b72bc35f86533eab08e3de55b36b50fc96a70.
- Preregistration/tests: 03f9aafca328f4dc92155d50b654e5c27ab988ea.
- Expected RED: [run 36373498001](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36373498001), job 108774508235, artifact 10949993221; ZIP SHA256 d21e6ced1a3e589991a084977bf194e6e4c02e0bc5b51531414bc32e4de23f3a.
- Tested implementation: 0262836849e2bf1f34b4790b172e7bf29311a9c1.
- GREEN: [run 36373801764](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36373801764), job 108775402939, [artifact 10950207970](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36373801764/artifacts/10950207970); ZIP SHA256 317f68a1e7f4adb52044d7ba5a3505e28ef970f3cc487d2988a030fc6f44e085.
- gate.py SHA256 ddc0e59aee1db514e77728dd7788d43545f03cde40cb7a19b221e2e8b1733239.
- Raw JSON SHA256 044fa85ad44c2edf5e1d8e0fa4c2410f44498d5edc2456c99633706b4c251b0e; 8,680,602 bytes.
- RESULT.json.gz SHA256 20a117760c6f5a9ecac86e45c871411ab3ed64c59f48c42d79641202b6656c6d; 1,462,362 bytes; lossless gzip with mtime 0.

The RED archive and exact log confirm the expected absent-implementation assertion. Downloaded archive digests, execution heads, frozen source byte identity and every GREEN manifest checksum were verified. The complete timestamp-stripped scientific JSON in the exact job log has the same SHA256 as the downloaded artifact. The first scientific implementation passed; no post-measurement implementation repair or criterion change was needed.

See EVIDENCE.json, SUMMARY.json, TEST_LOG.txt, SHA256SUMS and RESULT.json.gz. SHA256SUMS preserves original artifact filenames; decompress RESULT.json.gz to result.json to check that entry. Reproduce with the committed targeted workflow under Python 3.11, numpy 2.3.5, sympy 1.13.3 and mpmath 1.3.0 with one BLAS thread. Documentation is an additive child of the tested implementation; its own SHA appears in Git history and the completion report. No merge to main.
