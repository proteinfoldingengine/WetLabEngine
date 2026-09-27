# v15.90 preregistration — arbitrary-input negativity

Branch research/v15.90-arbitrary-input-negativity, exact certified parent 44ca8cf73e39ef1e66fda684ddabdf0ce6a1d5bf. Freeze before gate.py exists. DERIVATION.md states the universal proof, counterexample family and interpretation limits. No new randomness, fitting or numerical optimization.

## Inputs and precision

Pin weakest-direction-entanglement-bound/RESULT.json SHA-256 760442f2d460af344aa9b1d6d8b1a0305894d301c1e1fddfd90d1cc478fb373c; require all_valid and both confirmed verdicts. Use all 25 stored matrices/shifts and inherited v15.84-v15.89 helpers. Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0, 80 digits and full complex numbers. Recompute inherited 22 exact checks.

## New exact certificate: eight checks

Use real a,b,z,g with formal Kraus matrices K0=diag(1,z), K1=[[0,g],[0,0]], and input (a,0,0,b). Verify (1) explicit output matrix, (2) its input PT, (3) the characteristic polynomial (lambda-a^2)(lambda-z^2 b^2)(lambda^2-g^2 b^2 lambda-a^2 b^2 z^2), (4) trace preservation after substituting g^2=1-z^2. For q=z^2 and d=1-z^2+2z, verify (5) the negativity quadratic at p*=z/d,N*=z^2/d, (6) stationary equation, (7) strict-ceiling-gap identity 2-d=(1-z)^2, and (8) limit as z->0+ of N*/q is 1. Proof of concavity is in DERIVATION; do not infer global optimization from a finite scan.

## Frozen 114 state/channel rows

For each of the 25 inherited channels evaluate four inputs (100 rows): three pure states psi_p=sqrt(1-p)|00>+i sqrt(p)|11>, p=[0,0.25,0.5], and the mixed state (|psi_0.25><psi_0.25|+|10><10|)/2. Phase i is a complex-transport control. Apply id tensor Phi independently by 2x2 block action. For pure rows also reconstruct the output from (A tensor I)J(A^dagger tensor I)/2 with A=diag(sqrt(2(1-p)),i sqrt(2p)); verify PT reconstruction and operator lower bound using A* A^T. For mixed rows check linear output reconstruction and negativity convexity against its two component outputs.

Add 14 canonical amplitude-damping rows: q=[1,0.5,0.25,0.01,0.0001,0.000001,0], each with p=1/2 and the exact p* above (real Schmidt amplitudes). At q=0 use p*=0. Independently construct outputs using Kraus action and affine block action. Compare output negativity to N_q(p) and at p* to q/(1-q+2sqrt(q)); compare p=1/2 to q/2. Record both the old Choi ceiling and new uniform bound. The input-family optimizer is an analytic expression, not a tuned parameter.

All rows record T,t,delta,input/output/PT eigenvalues, input Schmidt maximum for pure rows, negativity, min(delta,1/2), signed slack, excess over delta/2, and physicality/identity residuals. Pure rows additionally record slack delta*lambda_max-N and min eigenvalue of rho_out^Gamma+(delta/2)(A* A^T tensor I). Mixed rows record the convexity slack. Do not divide normalized-state negativity by two. Do not clip eigenvalues for positivity classification.

## Validity and frozen scientific predicates

Pin/hash/parent verdict checks, all inherited 22 and new eight exact checks, all finite data, all 32 evaluated channel occurrences CPTP (25 inherited plus seven damping channels), all prepared inputs/outputs physical. Density/Choi minimum eigenvalue >=-1e-40; Hermiticity, trace, TP, block/filter/PT/Kraus reconstruction <=1e-45. Recomputed inherited Choi spectra, delta and negativity match archive <=1e-60. Damping delta equals q <=1e-45. These are input and implementation controls; failure gives INVALID.

Primary UNIVERSAL_INPUT_NEGATIVITY_BOUND_CONFIRMED iff valid and all 114 rows have uniform slack>=-1e-40 and at most one PT eigenvalue below -1e-40; every pure-row Schmidt slack and operator-bound minimum >=-1e-40; all mixed-row convexity slacks>=-1e-40. Otherwise UNIVERSAL_INPUT_NEGATIVITY_BOUND_NOT_CONFIRMED.

Secondary CHOI_CEILING_EXTENSION_FALSIFIED iff valid and the p* rows at q=0.5 and q=0.25 each exceed q/2 by >=1e-4, all 14 damping negativity formulas agree <=1e-45, and all inherited p=0.5 rows match their Choi negativity <=1e-45. Otherwise CHOI_CEILING_EXTENSION_NOT_FALSIFIED. This falsifies only the proposed extension, never v15.89.

Third OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_CONFIRMED iff valid, primary confirmed, damping formulas pass, the six positive-q p* ratios N/q increase strictly as q decreases through the frozen list, and the ratio at q=1e-6 is >=0.99. Exact limiting certificate supplies the universal optimal-coefficient argument, not the finite threshold. Otherwise OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_NOT_CONFIRMED. Never divide by q=0. INVALID overrides all verdicts. Tests accept valid scientific NOs and exercise negative adjudication.

## Execution

Publish these documents, test_gate.py and dedicated workflow with gate.py absent; inspect GitHub expected RED logs and artifact before implementation. Implement only this frozen measurement; run CI and inspect logs, JSON, downloaded artifact digest, execution SHA and source hashes. Publish unchanged artifact result as RESULT.json and exact provenance as RESULTS.md/EVIDENCE.json. No merging to main and no retrospective gate changes.
