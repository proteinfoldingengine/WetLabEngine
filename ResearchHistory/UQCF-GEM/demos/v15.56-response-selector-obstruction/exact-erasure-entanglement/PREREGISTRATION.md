# v15.88 preregistration — exact erasure and entanglement

Branch research/v15.88-exact-erasure-entanglement from 38c675b1af1c9df6b926adc5d243d0a889d00f93. Freeze before implementation. The universal implication and its known provenance are in DERIVATION.md. No optimization, new ensemble, randomness, or fitted threshold.

## Inputs and arithmetic

Pin support-loop-composition/RESULT.json SHA-256 bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166 and cptp-erasure-cost/RESULT.json SHA-256 4167a743c5e2da6fa0de9a00e3a2cf56778286eb58dbee4e2cb31a807dbb5c66. Require all_valid and their respective three confirmed verdicts. Candidate 46, inherited loop L and P=L^T L, remain fixed. Reuse v15.84 complex channel helpers, v15.85 affine Choi routines and v15.86 cofactor helper. Python 3.11; numpy 2.3.5, SymPy 1.13.3, mpmath 1.3.0; 80 digits.

## Exact certificates

Implement input partial transpose by explicit tensor indices, not full transpose. Check the canonical J^Gamma=(X tensor I)J(X tensor I) exactly on ten coefficients: constant I tensor I/2; six sigma_j^T tensor sigma_i/2 with j=X,Y and i=X,Y,Z; three I tensor sigma_i/2. Separately construct the canonical soft-erasure Choi at T=diag(1/2,1/2,e), compute its input partial transpose, and verify all four Bell eigenvector equations for each matrix (eight equations). The eigenvalue multisets are in DERIVATION. No floating tolerance for these eighteen checks.

## Frozen native exact-erasure channels

Extract retained orthonormal v1,v2 from SVD of L, n=v1 cross v2, u1=L v1,u2=L v2,N=cof(L),u3=Nn. Use these six maps, in this order:

1. T=L/4, t=-u3/2.
2. T=L/4, t=0.
3. T=L/4, t=u3/2.
4. T=L/2, t=0 (v15.87 optimum).
5. T=(1/2)u1 v1^T, t=u2/4 (nonunital rank-one image).
6. T=0, t=e_Y/2 (complex replacement, rank-zero image).

For every row record unnormalized J and J^Gamma spectra, CP/PPT classifications, normalized Choi negativity=sum(max(0,-eig(J^Gamma)))/2, shift norm, singular values and kernel-pair output distance. Check Tn=0 numerically. Form H=I-2nn^T,F=diag(1,-1,1),A=HF; verify A^T A=I, det A=1, TA=TF, and direct J^Gamma equals J(TF,t). Verify J(TF,t)=J(TA,t) and J/J^Gamma isospectrality. No SVD-based modification of T is allowed.

## Frozen boundary and counterexample controls

Soft erasure epsilon in [0,0.01,0.0001,0.000001]: T=L/2+epsilon N,t=0. Record CP/PPT classifications, Choi/PT spectra, min singular value, ||Tn||, kernel antipodal output distance and normalized Choi negativity. Compare both spectra with DERIVATION formulas, all three erasure quantities with epsilon, and negativity with epsilon/4. Predicted CP all four; PPT only epsilon=0, other rows NOT_PPT. The nonzero cases are exact full-rank channels, not numerical rank failures.

Synthetic controls:
- Identity T=I,t=0: J spectrum (0,0,0,2); J^Gamma spectrum (-1,1,1,1); CPTP, NOT_PPT.
- Depolarizing T=I/4,t=0: J spectrum (3/8,3/8,3/8,7/8); J^Gamma spectrum (1/8,5/8,5/8,5/8); CPTP, PPT; min singular value 1/4. Thus EB does not imply exact erasure.
- Amplitude damping gamma=1/2: T=diag(1/sqrt(2),1/sqrt(2),1/2),t=(0,0,1/2). J spectrum (0,0,1/2,3/2); J^Gamma spectrum (-1/2,1/2,1,1); CPTP, NOT_PPT. Check Kraus construction using diag(1,1/sqrt(2)) and [[0,1/sqrt(2)],[0,0]].

## Frozen tolerances and verdicts

Parent reconstruction: L spectrum (1,1,0), P and inherited optimal matrix L/2 agree within 1e-60. All other formula/identity/action reconstruction/Hermiticity/TP/state trace tolerances 1e-45. State positivity and CP/PPT threshold min eigenvalue >=-1e-40; NON_CP/NOT_PPT threshold <=-1e-8; intermediate UNRESOLVED. No eigenvalue clipping for classification. Negativity uses the standard max(0,-eigenvalue), with residual zero tolerance 1e-40.

Validity requires pinned parents; finite data; eighteen exact checks; parent matching; synthetic formulas/classes, Kraus check and depolarizing singular value; native/kernel-state density diagnostics; direct partial-transpose reconstruction and affine/trace diagnostics; and proper A/reflection algebra <=1e-45. Native CP/PPT/isospectrality and soft-family formula/negativity results are scientific predicates, not silently promoted to validity failures.

Primary EXACT_ERASURE_ENTANGLEMENT_BREAKING_CONFIRMED iff valid and all six native rows are CPTP/PPT, J/J^Gamma spectra match <=1e-45, ||Tn|| and kernel-pair output distance <=1e-40, and normalized negativity <=1e-40. Otherwise EXACT_ERASURE_ENTANGLEMENT_BREAKING_NOT_CONFIRMED.

Secondary SOFT_ERASURE_ENTANGLEMENT_SURVIVES iff valid and all four soft rows are CPTP, their PPT classes are [PPT,NOT_PPT,NOT_PPT,NOT_PPT], both spectrum errors, erasure-quantity errors and negativity-formula errors <=1e-45. Otherwise SOFT_ERASURE_ENTANGLEMENT_NOT_CONFIRMED. The exact soft-family identities in DERIVATION establish the arbitrarily-small-positive statement; the finite ladder validates its implementation.

Any invalidity overrides both to INVALID. Tests accept valid scientific NOs. Numerical/coding exceptions are implementation failures. Never alter frozen amplitudes or gates after measurement.

## Execution plan

Publish this preregistration, derivation, tests and targeted workflow with gate.py absent; inspect exact RED logs and downloaded artifact. Implement only frozen gate, review, run CI, inspect actual JSON verdicts, exact logs and downloaded hashes/source bytes. Publish lossless RESULT.json, RESULTS.md and exact provenance. No merge to main, no old verdict changes, no claim of theorem novelty.
