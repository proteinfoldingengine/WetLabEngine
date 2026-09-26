# Matched completion -> retained polar connection: a scoped exact witness

**Pinned baseline:** `8cf281ab1eb9cba2e2912abb5c12b043f215328d`.
**Verdict:** an existing supplied-source/connected-correlation/polar map carries
hidden three-body state information to a frame-invariant loop-response observable.
This is a conditional finite quantum-relational witness, not a gravity derivation.
All historical code, parity fixtures, and the corrected graph null are unchanged.

## 1. What is inherited, and what is new

The v13.09 report specifies a cyclic chiral three-body term and a collective
radial source; v13.10 reports initially matched local/pair data with different
polar response. The v13.09 CHECKER reads SUMMARY.json rather than generating
those states. The exact numerical seed needed to reproduce its quoted values
was not recovered from that version directory. We do not claim such a replay.

Instead we construct a **new rational member of the same algebraic family**.
Its parameters are supplied state data, not inferred coupling constants or
weights fitted to a desired response. The source, correlation extraction,
raw polar factor, and loop product are already specified in the archive.
The parameter-family proof below, not a search for favorable fixtures, explains
why it works. No graph weights or source law are modified to force a match.

The preceding diagonal parity example has zero initial 3x3 pair correlations.
After tilting its third site, C_01 has rank one, not three. It cannot provide a
unique full orthogonal link; we keep this as a rejection control, without
padding, choosing null-space bases, or regularizing it into a connection.

## 2. Explicit faithful matched states

Use the directed cycle E={(0,1),(1,2),(2,0)} and write k for the third site.
Let x=cos(theta), y=sin(theta), x^2+y^2=1. Define

    rho_h = (I + c sum_E [x(X_i X_j+Y_i Y_j)
                           + y(X_i Y_j-Y_i X_j)+Z_i Z_j]
               + h sum_E (X_i Y_j-Y_i X_j)Z_k)/8.

The frozen illustration uses c=1/20, x=3/5, y=4/5, and h=+/-1/100, with h=0
as a null. All these numbers are declared fixture choices, not physical laws.
Only three-body Pauli coefficients depend on h; consequently every one- and
two-body reduced density matrix matches exactly between the two states.
All local marginals are I/2, so their existing BKM metrics match as well.

A sufficient analytic positivity condition is

    3 c (2|x|+2|y|+1) + 6|h| < 1.

Every Pauli product has operator norm one, so the triangle inequality gives
lambda_min(rho_h) >= [1-3c(2|x|+2|y|+1)-6|h|]/8.
For the frozen nonzero pair the bound is **37/800**, not a near-zero edge.
The initial connected correlations are C_ij=cR, with

    R = [[x,y,0],[-y,x,0],[0,0,1]].

Their three singular values are exactly **1/20**. The raw polar is R with
determinant +1; no orientation-preserving projection or determinant flip is used.

## 3. Existing source law and exact derivative

Use P=Z_0+Z_1+Z_2, the archived collective source ray with its explicit scale.
The normalized family is exp(log(rho_h)+sP)/Tr exp(log(rho_h)+sP).
Here s is a source-deformation coordinate, not physical time.

The executable checks [rho_h,P]=0 with exact Pauli algebra. Hence
rho'_h=rho_h(P-<P>), and expectation derivatives are centered covariances.
The evaluator rejects noncommuting sources instead of applying this restricted
formula outside its domain. Identity shifts cancel and positive source scaling
multiplies both measured derivatives by the same factor.

At the matched base point, each edge has

    C'_ij = h J,  J=[[0,1,0],[-1,0,0],[0,0,0]].

For C=cR, the raw polar derivative is obtained from

    Omega = (R^T C' - C'^T R)/(2c),  R'=R Omega.

This is the full-rank polar Frechet derivative on the scaled-orthogonal base
stratum. Repeated nonzero singular values are allowed. Rank deficiency is not.

## 4. A gauge-invariant response, not just different coordinates

Fix H=O_01 O_12 O_20 and measure T=Tr(H). Independent endpoint frame changes
conjugate H, so T and its source derivative are invariant when states, source,
and observables are transformed consistently. No coordinate alignment is fitted.

The exact family formula is

    T(0)=1+2 cos(3theta),
    T'(0)=-6 sin(3theta) (h cos(theta)/c).

The reference observable is M=(Z_0+Z_1+Z_2)/3. Its susceptibility is
M'(0)=1+2c, equal for both matched states. Normalize only by that explicitly
specified reference measurement; T'/M' is independent of positive source units.

| Hidden coefficient h | Initial loop trace | Loop-trace derivative | Reference derivative | Scale-free ratio |
|---|---:|---:|---:|---:|
| -1/100 | -109/125 | +792/3125 | 11/10 | +144/625 |
| 0 | -109/125 | 0 | 11/10 | 0 |
| +1/100 | -109/125 | -792/3125 | 11/10 | -144/625 |

Thus the matched nonzero states have scale-free response gap **288/625**.
Initial local/pair geometry and the source are the same. A predictor using only
those initial data cannot determine this response for both completions.

The trace observable is not universally informative: at a flat initial loop
its first derivative vanishes even when the matrix-valued loop derivative is
nonzero. That case is explicitly tested and not discarded as a failed fixture.

## 5. Verification

All state coefficients, Pauli products, initial marginals, source jets, polar
jets, gauge covariance, and reported fractions are computed with exact rational
arithmetic. The general derivative is checked at 18 declared (c,h,rotation)
combinations including zero and negative hidden coefficients.

An independent dense-matrix oracle constructs rho, computes exp(log rho+sP),
extracts connected Pauli correlations, and takes raw SVD polar factors. At
three fixed central-difference steps (1e-4,3e-5,1e-5), the maximum observed
loop-matrix derivative discrepancy over h=-1/100,0,+1/100 is below 1.8e-9.
The smallest sampled pair singular value exceeds 0.04999; the smallest sampled
state eigenvalue exceeds 0.0895. These floats validate the exact calculation;
they do not set the analytic result or its parameters.

The local RED receipt is one availability assertion failure and 19 skipped
tests. All 20 new tests then pass, along with the 15 existing exact-baseline
tests available locally. Three deliberate mutations were caught: removing a
hidden term, dropping covariance centering, and breaking the polar skew
projection. The full historical suite is run separately by GitHub CI.

Reproduce from the demo directory:

    python -m unittest -v test_completion_connection_bridge
    python completion_connection_bridge.py

The committed exact JSON is recomputed by the tests. Numerical-oracle results
are supplemental receipts, not values enforced bit-for-bit across machines.

## 6. Claims boundary and next gate

This closes a conditional arrow:

    supplied full state + supplied source
      -> pair-correlation derivative -> polar-connection derivative
      -> a loop-conjugacy response observable.

It does NOT derive which hidden completion or source is selected by Genesis,
repair history, or global consistency. It does not couple this loop response
to the separate v15.56 scalar lineage Laplacian. It establishes neither physical
curvature, gravitational universality, Einstein/ADM dynamics nor novelty. The
archived program already described this kind of hidden-completion effect.

The immediate next gate is state selection, not another fitted geometric map:
identify a provenance-supported repair/update rule that produces or constrains
h from common initial data, then compare the SAME gauge-invariant response
under that rule. Until such a rule is specified, this is a valid supplied-state
counterexample to static pair-data sufficiency, not a generated gravity signal.

## Provenance and mathematical prior art

- ../../v13/v13.09/REPORT.md and CHECKER.py: cyclic chiral completion/source,
  and the archived stored-summary validation scope.
- ../../v13/v13.10/REPORT.md: same initial pair data, different source response.
- ../v13.27-gravity-progress/MATH_AND_PHYSICS.md, sections 1-4: source family,
  connected covariance, raw polar factor and loop trace; its extra determinant
  projection is NOT used here.
- MATCHED_COMPLETION_RESPONSE.md and PRUNING_CONSISTENCY_AUDIT.md: unchanged
  parity control and exact scalar-graph baseline, kept as separate objects.
- E. S. Gawlik and M. Leok, Iterative Computation of the Frechet Derivative of
  the Polar Decomposition, SIAM J. Matrix Anal. Appl. 38(4), 1354-1379 (2017),
  DOI 10.1137/16M108971X, https://arxiv.org/abs/1608.04491 . Polar derivative
  calculus is established matrix analysis, not a new theorem claimed here.
