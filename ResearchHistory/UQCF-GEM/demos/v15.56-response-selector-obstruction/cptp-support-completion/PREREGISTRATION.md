# v15.86 preregistration — frozen before implementation

Branch research/v15.86-cptp-support-completion starts at certified documentation head c0adc88d4ef2b955a07d567b4cf2c3ab3d1fa24d. The question and scope are in DERIVATION.md. No new states, sampling, optimizer, fitted parameter, or random seed is used. Candidate 46 and the root loop L are inherited unchanged.

## Inputs and precision

Read sibling support-loop-composition/RESULT.json, SHA-256 bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166; require all_valid and its three confirmed verdicts. Read affine-shift-obstruction/RESULT.json, SHA-256 a61ca58f52ca49e9a9f4186ded63a29b9cf84195f688ba00e77d05d15329370a; require all_valid and both confirmed verdicts. Use mpmath 1.3.0 at 80 digits, SymPy 1.13.3 and the inherited v15.84 channel helpers. Preserve complex entries. Freeze Python 3.11 and numpy 2.3.5 in CI.

## Exact certificate

Build the canonical general T with columns e1,e2,(a,b,c) and its complex-linear Pauli Choi matrix independently of the displayed target. SymPy real a,b,c and t1,t2,t3. Verify exactly: Choi matrix equals DERIVATION; norm-sum identity for unrestricted translations; diagonal (1-c)/2; normalized Bell-minus expectation (c-1)/2; principal minor at c=1 equal -(a^2+b^2)/4; the a=b=0,c=1 Choi equals the identity-channel Choi. Check Pauli commutator [X,Y]=2iZ and the independent matrix rank of I,X,Y,XY equals 4. All eight checks must pass. The positivity reasoning in DERIVATION converts these certificates into a universal uniqueness theorem; the finite controls alone do not.

## Frozen numerical measurement

Compute cof(L) by signed 2x2 minors, N=cof(L), R=L+N and Rminus=L-N directly, without replacing L by a fitted rotation. Compute P=L^T L,Q=L L^T and compare stored parent projectors within 1e-60. Inherited singular values must equal (1,1,0) within 1e-60. Other arithmetic/control residuals below use 1e-45; CPTP tolerance is minimum unnormalized Choi eigenvalue >=-1e-40, NON_CP <=-1e-8, otherwise UNRESOLVED. Never clip eigenvalues.

Record R,N,Rminus, orthogonality and determinant, RP-L and N P, N^T N-(I-P), N N^T-(I-Q), normF(N), all Choi eigenvalues and diagnostics. Reconstruct R from an SVD-derived retained basis rotated within its plane by frozen angles 0, pi/7, pi/3; use u_i=L v_i and oriented cross products. The maximum basis-independence residual must be <=1e-45. This is a representation control, not a random-frame replication.

For the missing input axis v3 and output axis N v3, record trace distances of the antipodal pair before mapping, under L, and under R. Check input/output states for the completed map are physical (Hermiticity/trace <=1e-45, minimum eigenvalue >=-1e-40). Record Phi_(R^T) composed with Phi_R on all four matrix units; error <=1e-45. Record input distance 1 and completed output distance 1 within 1e-45, while the zero extension's pair distance must be <=1e-40. Also verify R-L has Frobenius norm 1 within 1e-45. These observations comprise the restoration gate, not an inference from CP status alone.

## Controls, validity and verdicts

Synthetic canonical completion ladder T=diag(1,1,c), c in [-1,0,0.5,1,1.5]. Sorted Choi eigenvalues must match sorted [(c-1)/2,(1-c)/2,(1-c)/2,(3+c)/2] within 1e-45; classifications NON_CP,NON_CP,NON_CP,CPTP,NON_CP. Identity and rank-one complete Z dephasing both CPTP, agree on Z and differ by trace distance 1/2 between their outputs for the same +X input, since dephasing yields I/2. Check that value and include a +Y input to exercise complex transport. Verify the zero extension is Bloch-ball contractive (largest singular value <=1+1e-40) but NON_CP; improper completion has Choi spectrum (-1,1,1,1). Synthetic controls are validity requirements.

Validity requires pinned parents, exact certificates, finite numbers, synthetic controls, inherited projector/spectrum checks, Choi TP/Hermiticity/action reconstruction <=1e-45, basis independence, and density diagnostics. Numerical implementation exceptions are infrastructure failures. Native R orthogonality, determinant, CP spectrum and restoration properties are measured scientific predicates, not silently reclassified as infrastructure.

Primary confirmed iff valid, exact certificate true, R orthogonality error <=1e-45, |det R-1|<=1e-45, RP-L<=1e-45, N P<=1e-45, both normal-projector residuals<=1e-45, R classified CPTP with spectrum (0,0,0,2) within 1e-45, L and Rminus NON_CP with spectra (-.5,.5,.5,1.5) and (-1,1,1,1) within 1e-45. Verdict UNIQUE_CPTP_SUPPORT_COMPLETION_CONFIRMED; otherwise UNIQUE_CPTP_SUPPORT_COMPLETION_NOT_CONFIRMED.

Secondary confirmed iff valid, primary confirmed, normF(R-L)=1, the three pair-distance checks and full matrix-unit inverse check satisfy the frozen thresholds. Verdict DISCARDED_DIRECTION_RESTORATION_CONFIRMED; otherwise DISCARDED_DIRECTION_RESTORATION_NOT_CONFIRMED. Any invalidity overrides both verdicts to INVALID. Tests accept valid scientific NOs. No criterion changes after measurement.

## Execution plan

1. Publish this preregistration, derivation, tests and targeted workflow with gate.py absent. Inspect exact RED log/artifact for the missing-implementation assertion.
2. Implement only this protocol in additive gate.py; reviewer checks theorem and code. Run targeted CI. Inspect actual scientific JSON, exact logs and downloaded artifact hashes/source bytes.
3. Publish RESULTS.md, lossless RESULT.json and exact provenance on this branch. No merge to main and no reinterpretation of v15.85 as a pass for its unchanged maps.
