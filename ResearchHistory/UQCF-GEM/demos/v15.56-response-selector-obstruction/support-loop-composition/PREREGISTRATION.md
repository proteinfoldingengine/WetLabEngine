# v15.83 preregistration — support loop composition

Frozen before gate.py exists or new measurement. Branch
research/v15.83-support-loop-composition, parent
b7e472378b907c7ff95a44cd8611d11c7fdaa2f5.

## Frozen input and extraction

Read the parent polar-boundary-obstruction/RESULT.json, SHA-256
 a60feb6ab4506e8049d72c6a4e85627ae6f9137e3509aa9da44e14f6f151df56.
It must retain all_valid=true and POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED.
Use candidate 46, lambda=-1, Psource=ZII, Qsource=XXI and its complete complex
input_hex matrix, without normalization or symmetrization. Verify equality
with the inherited selector and its unchanged 12 candidate indices. Use the
midpoint of the stored exact rational isolating interval, not the rounded
printed strength. Precision is 80 decimal digits. No random seeds.

Independently extract connected matrices for edges (0,1),(1,2),(2,0) from
the exact rational state/channel. Use the first two singular terms for V_01
at the root approximation, full polar factors for the other two edges, and
L=V_01 O_12 O_20. Define P=L^T L, Q=L L^T. No extra alignment or polar
correction. Re-evaluate full regular loops at the unchanged side distances
[1e-3,1e-5,1e-7] in ordered strength; keep their improper orientation after
the root as a diagnostic, without changing v15.81's proper-domain gate.
Measure L_side P-L and (L_before-L_after)P.

Compute raw matrix powers L^n for n=[1,2,3,4], singular spectra,
partial-isometry defects ||A_n^2-A_n||_F with A_n=(L^n)^T L^n, G_n=I-A_n,
and its independent telescoping reconstruction. Report lossless dimensions
at thresholds [1e-9,1e-10,1e-11] against fixed identity scale 1. Do not use
an all-noise leading singular value as the reference. Report ||L^3||_2.

## Validity (failure gives INVALID for all verdicts)

- Parent file hash, verdict and selector match exactly. Matrix roundtrip
  error <=1e-16. No imaginary component discarded.
- Original source-edge root matrix agrees with stored v15.82 matrix <=1e-60
  max entry. Rank-two guard s_min<=1e-45, s_next>=1e-4. Other two root edges
  min singular values >=1e-4, proper determinants within1e-40 of +1.
- Original/root/side quantum matrices normalized and Hermitian within1e-12,
  min eigenvalue >=-1e-12. Convex-unitary formula remains the same.
- Every evaluated full polar orthogonality/reconstruction error <=1e-50.
  Initial/final projector symmetry and idempotence, L L^T L=L and
  tr(P)=tr(Q)=2 residuals <=1e-50.
- Every power's direct/telescoping G_n difference <=1e-50; G_n eigenvalues
  >=-1e-50 and <=1+1e-50. Kernel dimension from G_n agrees with the nullity
  of the stacked constraints (I-P)L^k using the squared singular values
  and the same thresholds. This tests energy loss, not raw matrix rank.
- L^2 spectrum agrees with (1,sqrt(c^2),0), and the defect/commutator formula
  in DERIVATION.md agrees within1e-45. c^2 may be clipped to [0,1] only for
  sqrt after validating membership to1e-50; record its raw value.
- Synthetic controls: L=diag(1,1,0) remains partial-isometric for all four
  powers, with lossless dimension2. For L=diag(1,1,0) R_y, where cos=3/5,
  sin=4/5, L^2 singular values (1,3/5,0) and defect144/625 within1e-45.
  For L=diag(1,1,0) times the cycle matrix [[0,1,0],[0,0,1],[1,0,0]],
  the lossless dimensions are [2,1,0,0] and L^3=0 within1e-45.
- All output finite. Unexpected exceptions are implementation failures.

## Separate scientific verdicts

Crossing: at the smallest frozen delta, both ||L_side P-L||_F and
||(L_before-L_after)P||_F <=1e-5, while the uncompressed loop difference
has Frobenius norm >=1.9.
YES SUPPORT_RESTRICTED_CROSSING_CONFIRMED;
NO SUPPORT_RESTRICTED_CROSSING_NOT_CONFIRMED.

Composition through the four frozen traversals:
- Any n in[2,3,4] with partial-isometry defect >=1e-8:
  SUPPORT_LOOP_COMPOSITION_OBSTRUCTED.
- Otherwise if every such defect <=1e-40:
  SUPPORT_LOOP_COMPOSITION_CLOSED.
- Otherwise SUPPORT_LOOP_COMPOSITION_UNRESOLVED.
CLOSED is scoped to these powers; matrix multiplication is associative
regardless of this verdict. Do not interpret OBSTRUCTED as nonassociativity.

Invariant lossless core: use ker G_3, justified by Cayley-Hamilton.
- Dimension0 at all three thresholds: LOSSLESS_LOOP_CORE_TRIVIAL.
- The same positive dimension at all thresholds: LOSSLESS_LOOP_CORE_NONTRIVIAL.
- Threshold disagreement: LOSSLESS_LOOP_CORE_UNRESOLVED.
All are valid scientific outcomes; tests must not require an anticipated one.
A trivial core implies strict contraction after three traversals, not a zero
map. Publish all spectra and residuals, not just verdict labels.

## Workflow

Publish this preregistration, derivation, tests and dedicated workflow with
gate.py absent. Verify GitHub expected RED before implementation. Then run
only the targeted research workflow, inspect exact job logs and downloaded
artifacts with hashes/execution SHA, review interpretation and publish
lossless JSON and RESULTS.md. No changes to old files, criteria, amplitudes
or historical verdicts; no merge to main. Documentation uses [skip ci].
