# v15.98 preregistration — composed four-body response

Parent903b72bc35f86533eab08e3de55b36b50fc96a70; branch research/v15.98-composed-four-body-response. Freeze before implementation/RED. No state selection, new randomness, fitting, threshold rescue or historical verdict change.

## Inputs and sources

Pin overlap-hidden-response/gate.py SHA256 a27a98a29c5dce4f286bd445072297228af903a348ee274a9c6bb7d15c986439, RESULT.json.gz 5d211fb43db6ddd101be6d31391554b4e6720f09626255e85cc01da76d3179bc, raw JSON a16af3868ed4a0d959dda97eaea9c79f02f2beb0aa996b175a233463b9381891. Require all_valid and both confirmed v15.97 verdicts. Also pin v15.96 raw JSON99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e and code56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52; read its exact hexadecimal complex input states. Indices[13,16,22,25,27,29,37,39,46,50,66,77]. Use all81 weight-four Pauli words in lexicographic X,Y,Z order, normalized /4. Verify orthonormality, Hermiticity and zero trace.

Three copies of the frozen source act on ordered site pairs A=(0,1), B=(1,2), D=(2,3). Coherent lambda=+1 for primary measurements. Compare A then B versus B then A, and A then D versus D then A. Incoherent controls use lambda pairs(0,1),(1,0),(0,0) for both source-pair types and orders. Preparation on all four sites follows both sources, using unchanged planar and isotropic v15.96 maps. Two source-pair types x two arms x12 states =48 rows. Baseline u=v=0 retains preparation. Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0, one BLAS thread.

## Exact certificate

Eight grouped checks using an independent exact local Pauli coefficient map and sparse global Pauli words: (1) reconstruction of local coherent/incoherent generator action on all16 two-qubit Pauli words; (2) individual-source proper-pair restrictions vanish for all81 probes for A,B,D; (3) all one-body components of twice-applied generators vanish for both pairs and orders; (4) the overlapping YYXX witness in DERIVATION, with both ordered two-body projections; (5) disjoint generator compositions commute on all256 four-qubit Pauli words; (6) the disjoint XXXX witness; (7) all incoherent-pair controls have zero two-body projection for all81 probes and both orders; (8) exact finite-channel polynomial pair identity in symbolic s,t for coherent compositions. Exact projection includes all six pairs, including23. Reuse v15.97's8 source checks, v15.96's13 frame/geometry checks and v15.92's45 preparation checks unchanged.

Compare the exact Pauli coefficients to independent complex16x16 nested-generator action on all81 probes and both source-pair types/orders. Tolerance1e-12 for max coefficient discrepancy. Check individual hidden pair nulls, single-body nulls, incoherent pair nulls, Gram/trace/Hermiticity and source unitarity at1e-12. Store retained pair-leakage ranks and norms for all six pairs, with23 separately labeled. Do not reuse the old unaffected-spectator check.

## Response and domain

For every row, extract the postprocessed baseline and the two ordered global Y arrays. Independently construct polar derivatives and loop products for all81 columns. Use the certified oriented rank-two completion for the planar arm, proper full polar for isotropic. Store both K6x81,J3x81, their difference, singular values, ranks, edge ranks, loop ranks and baseline loops. Absolute rank thresholds[1e-9,1e-10,1e-11], reference1. Primary observable is the order contrast of J; K is also required by the frozen rank hypotheses.

Baseline and affine-check domain: all five planar edges rank2, all five isotropic edges rank3 with positive full-polar determinant. Rank reference is each unprocessed correlation's leading singular value as in v15.96. No completion of another rank or full-rank determinant flip. Undefined domains yield null affected responses and scientific NOs, not INVALID when other controls pass.

Check proper polar/loop identities, Sylvester equations and skewness at1e-9. Check overlap first-loop response is null at1e-9. Disjoint order differences of both K,J have norm<=1e-9 and ranks0 at every threshold as a validity control. Compare independent response of Y_AB-Y_BA to difference of ordered responses within1e-9. This does not regard a generator commutator as a CPTP channel.

Covariance uses the same four frozen quaternion frames, transforming states, hidden probes and each source's unitaries. Conjugate the preparation map correctly. Independently recompute both orders and their contrast: K rotates by blockdiag(G0,G0), J is invariant; norms<=1e-9 and rank lists must match. No fitted alignment.

## Finite checks

Use physical hidden perturbations rho±epsilon h, epsilon=1e-4, and unchanged finite sources with u=v=0.1. Apply both orders and global preparation. Compare

(C_plus-C_minus)/(2 epsilon s(0.1)^2)

to the corresponding analytic connected mixed derivative, where s(u)=(1-exp(-2u))/2. Relative Frobenius error, denominator max(1,norm of analytic derivative array), must be<=1e-7. Store errors for both orders. This verifies exact finite retained channel action; it does not assert that origin loop ranks persist at u=v=0.1 or require a finite-source polar domain.

Independently evaluate the loop Frechet derivative on global affine probes rho±eta Y, eta=1e-6, after global preparation. Recompute loops and invariant scalars directly; central differences of each, divided by2eta, must match analytic K,J with relative Frobenius errors<=1e-5. Compare only in the baseline/affine rank domain. Record every affine domain exit and give the relevant row a scientific NO. These are physical nearby density matrices used for derivative verification, not a replacement source law. Check density positivity>=-1e-12 and trace/Hermiticity<=1e-12 for hidden inputs, each intermediate and final finite-source state, affine global inputs, and prepared outputs. Certify nonnegative normalized finite source weights plus unitarity and inherited preparation maps, with1e-12 tolerance. All data finite.

## Verdicts

Validity requires parent hashes/verdicts/indices/counts, all exact checks, all numeric algebra/null/physical/covariance/finite agreement controls and disjoint order null. INVALID overrides both verdicts if validity fails. Primary COMPOSITION_ORDER_GEOMETRY_CONFIRMED iff valid and every overlap row has all applicable domains and order-contrast K,J ranks[3,3,3],[2,2,2] for isotropic, or[1,1,1],[1,1,1] for planar, in both native and transformed frames. Otherwise COMPOSITION_ORDER_GEOMETRY_NOT_CONFIRMED.

Secondary COMMUTING_COMPOSITION_ACTIVATION_CONFIRMED iff valid and every disjoint row has all applicable domains and both orders have K,J ranks[6,6,6],[3,3,3] for isotropic, or[2,2,2],[2,2,2] for planar, in both native and transformed frames. Otherwise COMMUTING_COMPOSITION_ACTIVATION_NOT_CONFIRMED. Valid scientific NOs are accepted by tests. No post-measurement tuning.

## Execution and boundaries

Commit preregistration, derivation, tests and workflow without gate.py. Inspect expected GitHub RED and downloaded artifact. Implement only frozen measurement; inspect actual JSON/logs/downloaded artifact and hashes; publish RESULTS with exact provenance. No main merge. Source strengths are not fundamental time. This tests a specified compositional law, not physical source-law selection, complete six-edge geometry, continuous holonomy or gravity.
