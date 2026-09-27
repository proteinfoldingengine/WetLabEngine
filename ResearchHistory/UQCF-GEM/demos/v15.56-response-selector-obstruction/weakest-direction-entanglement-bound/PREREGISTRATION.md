# v15.89 preregistration — weakest-direction Choi-negativity bound

Branch research/v15.89-weakest-direction-entanglement-bound from parent 8419150d3a8309a247d29ae9cfac337ca0f87b6a. No new random states, fitting or optimizer. Freeze this protocol before implementation. DERIVATION.md contains the analytic universal bound and its interpretation limits.

## Inputs and numerical environment

Pin support-loop-composition/RESULT.json SHA-256 bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166 and exact-erasure-entanglement/RESULT.json SHA-256 06295e1705c9c38567ee8dc1bee10a737b0d9a8b260200867a68d01fc10130ab. Require all_valid and the three v15.83/two v15.88 confirmed verdicts. Candidate 46 and L are unchanged. Use v15.84/v15.85/v15.86/v15.88 helpers. Python 3.11, numpy 2.3.5, SymPy 1.13.3, mpmath 1.3.0; 80 digits, full complex arithmetic.

## Exact certificates

Thirteen canonical affine coefficient equations for J^Gamma-(X tensor I)J(X tensor I)=Z tensor (T e_Z).sigma, counting constant, nine T components and three shift components. One exact identity D^2=(w1^2+w2^2+w3^2)I4 for D=Z tensor w.sigma. Eight exact Bell eigenvector equations for the saturation family in DERIVATION (four J, four J^Gamma). Total 22 exact checks; immutable symbolic matrices must be converted to mutable before index assignment, preserving v15.88's implementation repair.

## Frozen 25-channel evaluation

1. Re-evaluate all six native and all four soft rows of v15.88 from their stored T and t. Compare reconstructed J/PT eigenvalues and normalized negativity with the stored values within 1e-60.
2. Seven saturation-family rows epsilon=[0,0.000001,0.0001,0.01,0.25,0.5,1], T=((1+epsilon)/2)L+epsilon cof(L),t=0.
3. Five amplitude-damping rows gamma=[0,0.25,0.5,0.75,1]. Let v1,v2 be a retained SVD basis, n=v1 cross v2,u1=L v1,u2=L v2,u3=cof(L)n. Evaluate T=sqrt(1-gamma)L+(1-gamma)cof(L), t=gamma u3. Validate the input/output frames are proper orthogonal. Compare J and PT spectra with DERIVATION, and delta with 1-gamma.
4. Three depolarizing controls alpha=[0.25,0.5,1], T=alpha(L+cof(L)),t=0. Expected J spectrum [(1-alpha)/2 three times,(1+3alpha)/2], PT spectrum [(1-3alpha)/2,(1+alpha)/2 three times]; negativity=max(0,(3alpha-1)/4), delta=alpha. The first two have strictly positive bound slack.

For every row recompute n as a weakest right singular vector of that row's T, rather than assuming its weakest direction equals the original loop kernel. Compute delta, H=I-2nn^T,F=diag(1,-1,1),A=HF, G=J^Gamma, B=J(TA,t), D=G-B, D_formula=((Fn).sigma)^T tensor (Tn).sigma. Record J,G,B eigenvalues, normalized Choi negativity, count of PT eigenvalues below -1e-40, bound delta/2, slack delta/2-negativity, minimum G eigenvalue+delta, ||D||op, and weakest-axis antipodal input/output trace distances (predicted 1,delta). No division by delta near zero.

Check A^T A=I,det A=1,||n||=1, ||Tn||=delta, D=D_formula and ||D||op=delta. B is an actual unitary precomposition, not a truncated surrogate; verify its spectrum matches J. Record T,t and all residuals. Numerical spectral norm of Hermitian complex D uses max absolute Hermitian eigenvalue, not real-only SVD.

## Tolerances, validity and verdicts

Parent/saved-result reconstruction tolerance 1e-60; generic identity/formula/trace/Hermiticity tolerance 1e-45. State and CP positivity tolerance -1e-40; count PT eigenvalues below -1e-40. No eigenvalue clipping for classification; negativity uses its standard max(0,-lambda)/2 definition. All 25 input channels and all comparison B matrices must be CPTP (Hermiticity/trace preservation and minimum eigenvalues >=-1e-40); otherwise the input/representation validity gate is INVALID, not evidence against a CPTP-only theorem.

Validity requires pinned parents and inherited data, all 22 exact checks, all finite values, parent L spectrum/projector checks <=1e-60, proper native frames, all channel/partial-transpose/affine diagnostics <=1e-45, physical weakest-axis input/output states, A and n geometry controls, D reconstruction/norm and B/J isospectrality <=1e-45. Saturation-family, amplitude-damping and depolarizing spectrum/delta formulas are validity controls. Distance predictions, bound slack and attained-negativity equations remain scientific predicates.

Primary WEAKEST_DIRECTION_NEGATIVITY_BOUND_CONFIRMED iff valid and all 25 rows have at most one negative PT eigenvalue, slack>=-1e-40, min(G)+delta>=-1e-40, and weakest-axis distance errors <=1e-45. Otherwise WEAKEST_DIRECTION_NEGATIVITY_BOUND_NOT_CONFIRMED.

Secondary NEGATIVITY_BOUND_SHARPNESS_CONFIRMED iff valid, primary confirmed, seven saturation and five amplitude-damping rows all satisfy |negativity-delta/2|<=1e-45, three depolarizing rows satisfy the stated negativity formula <=1e-45, and alpha=0.25,0.5 both have slack>=1e-4. Otherwise NEGATIVITY_BOUND_SHARPNESS_NOT_CONFIRMED. Invalidity overrides both verdicts to INVALID. Valid scientific NOs remain NO and are accepted by tests.

## Execution plan

Publish preregistration, derivation, tests and targeted workflow with gate.py absent; verify expected RED from exact logs and downloaded artifact. Implement only this protocol; review and run targeted CI; inspect exact logs, scientific JSON, artifact hashes and source bytes. Publish lossless RESULT.json, RESULTS.md and exact provenance. Preserve all historical verdicts and do not merge to main.
