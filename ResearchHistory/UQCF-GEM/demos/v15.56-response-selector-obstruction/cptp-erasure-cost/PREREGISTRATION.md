# v15.87 preregistration — CPTP erasure cost

New additive branch research/v15.87-cptp-erasure-cost, parent 3b1c4d29db91b2bfac7f6fe447de131671fd9206. Freeze before implementation. DERIVATION.md supplies the universal argument and objective definitions. No new states, randomness, optimizer, or fitted law. Candidate 46's unchanged loop L is the sole inherited scientific input.

## Pinned inputs and arithmetic

Read support-loop-composition/RESULT.json SHA-256 bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166 and cptp-support-completion/RESULT.json SHA-256 7e0df41086ed226c90a22e09270f305e3de68abfe5d1d6a9e5811598c324090d. Require their all_valid flags and three v15.83 and two v15.86 confirmed verdicts. Use inherited v15.84 helpers plus v15.85 affine Choi and spin-flip certificate. Python 3.11, numpy 2.3.5, SymPy 1.13.3, mpmath 1.3.0; 80 digits, full complex arithmetic.

## Exact certificates

Independently construct the symbolic input-first Choi matrix for diag(s1,s2,0). Check its four normalized Bell eigenvector equations, with eigenvalues respectively (1+s1+s2)/2 for Phi+, (1-s1-s2)/2 for Phi-, (1+s1-s2)/2 for Psi+, (1-s1+s2)/2 for Psi-. At s1=s2=1/2, add an unrestricted real translation (t1,t2,t3). Check the Phi- expectation is identically zero and squared norm of its image is (t1^2+t2^2+t3^2)/4. Six exact checks. Re-run the inherited 13-coefficient exact full-transpose spin-flip certificate. These identities support the analytic inequalities and equality arguments in DERIVATION; no finite scan claims universal optimality.

## Frozen native measurements

Set P=L^T L,K=I-P. Compare L and P with v15.86/v15.83 data and singular values (1,1,0) within 1e-60. Define T*=L/2 directly. Extract a retained orthonormal basis v1,v2 from SVD and set ui=Lvi; v3=v1 cross v2.

Measure T*K, its nuclear norm, ||T*-L||op, ||T*-L||F, Choi eigenvalues and affine diagnostics. Reconstruct the optimal map as the equal mixture of the two measure-and-prepare maps on all four matrix units. Record positive normalized input/output states and trace distances for antipodal axes v1,v2,(v1+v2)/sqrt(2),v3. Frozen predicted output distances (1/2,1/2,1/2,0); all input distances 1. For the three retained-plane +axis states, compare the optimal output with the formal L output: predicted distance 1/4.

Frozen isotropic ladder T=alpha L with alpha in [0,1/4,1/2,3/4,1], t=0. Analytic sorted spectrum [(1-2alpha)/2,1/2,1/2,(1+2alpha)/2]; classifications CPTP,CPTP,CPTP,NON_CP,NON_CP.

Frozen anisotropic controls T=a u1 v1^T+b u2 v2^T with (a,b)=(3/4,1/4),(1,0),(1/4,1/4). All CPTP. Expected (operator error,Frobenius error) respectively (3/4,sqrt(10)/4),(1,1),(3/4,3sqrt(2)/4). These controls expose unequal retention and lower-norm loss; they do not search for an optimum.

At T*, freeze translations t=0 and +/-0.1 e_j for each of the three native coordinate axes j. Predict zero CPTP and every nonzero row NON_CP. This ladder checks implementation only; the exact kernel argument is the all-translations certificate. The axes are coordinate components for controls, not preferred source directions.

## Validity and scientific gates

Generic arithmetic/control tolerance 1e-45. Parent matching tolerance 1e-60. Density eigenvalue and CPTP tolerance -1e-40. NON_CP threshold <=-1e-8; otherwise UNRESOLVED. No eigenvalue clipping. Validity requires pinned parents, finite results, all six plus thirteen symbolic identities, parent matching, Choi Hermiticity/TP/affine identities <=1e-45, physical native tested states, isotropic formula errors <=1e-45 and listed classes, all anisotropic formulas/classes, and the inherited synthetic affine controls. Numerical exceptions are infrastructure failures.

Primary ERASURE_COST_BOUND_ATTAINED iff valid and T* is CPTP, spectrum agrees with (0,1/2,1/2,1) within 1e-45, ||T*K||<=1e-45, nuclear norm=1, operator error=1/2, Frobenius error=1/sqrt(2), and measure-and-prepare reconstruction <=1e-45. Otherwise ERASURE_COST_BOUND_NOT_ATTAINED.

Secondary OPTIMAL_ERASURE_TRANSLATION_RIGID iff valid, primary attained, and frozen translation classifications are [CPTP,NON_CP,NON_CP,NON_CP,NON_CP,NON_CP,NON_CP]. Otherwise OPTIMAL_ERASURE_TRANSLATION_RIGIDITY_NOT_CONFIRMED.

Third OPTIMAL_ERASURE_DISTINGUISHABILITY_CONFIRMED iff valid, primary attained and all input/output/target-output distance predictions hold within 1e-45 (kernel output <=1e-40). Otherwise OPTIMAL_ERASURE_DISTINGUISHABILITY_NOT_CONFIRMED. Invalidity overrides all verdicts to INVALID. Valid scientific NOs are retained and accepted by tests. No gate changes after measurement.

## Execution plan

Publish this document, DERIVATION.md, test_gate.py and targeted workflow with scientific gate.py absent. Verify expected RED in exact GitHub job logs and downloaded artifact. Implement only this frozen measurement; review code, run targeted CI, inspect actual verdicts, exact logs and artifact hashes/source bytes. Commit lossless RESULT.json, RESULTS.md and exact provenance. No merge to main. No revision of v15.85 or v15.86 verdicts.
