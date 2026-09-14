# v15.20 — A CPTP predictor representation and its readout cost

**Result:** `EXECUTED_CONDITIONAL_CPTP_PREDICTOR_WITH_READOUT_COST`.

A positive quantum-channel representation of the v15.19 predictor exists on the **same four-qubit carrier**, provided the readout is explicitly rescaled. Exact direct readout and exact quantum-state recovery are different requirements and have a stronger obstruction. No new physical pruning, collapse, source, clock or entropy law is adopted.

## 1. The inherited problem

The frozen all-six-motion module for the fourteen target masks that pinch any of A1/A2/B1 is

\[
\mathcal S=\{A=A^\dagger:\operatorname{Tr}(\Gamma A)=0\},\qquad
\Gamma=Y^{\otimes4},\quad d=16.
\]

It has real Hermitian dimension 255, including the identity (254 free coordinates after normalization). The masks `0000` and `0001` instead require the full module and are not covered by this reduction. Every supplied motion commutes with Γ. The previous orthogonal projection

\[
\Pi(\rho)=\rho-\operatorname{Tr}(\Gamma\rho)\Gamma/16
\]

is not positive: a pure product of four +Y eigenstates produces minimum eigenvalue −1/16. v15.19 correctly did **not** conclude that every other physical representation is impossible.

The new baseline check regenerates the 255-dimensional module and compares its projector to Γ-perp. Error: approximately 9.09e−14. All inherited source hashes are checked. No original dynamics is rewritten.

## 2. Exact direct preservation has a general obstruction

Let Φ:M16→M16 be CPTP. Suppose

\[
\operatorname{Tr}[A\Phi(\rho)]=\operatorname{Tr}(A\rho)
\]

for every input state and every A∈S. Equivalently the unital completely positive adjoint Ψ=Φ* fixes S pointwise.

S contains each local Pauli X_i and Z_i. If a UCP map fixes a unitary W, then

\[
\Psi(W^\dagger W)=I=\Psi(W)^\dagger\Psi(W),\qquad
\Psi(WW^\dagger)=I=\Psi(W)\Psi(W)^\dagger.
\]

The multiplicative-domain theorem [1] therefore places W in the multiplicative domain: its products are preserved. The eight local X_i,Z_i generate M16, so Ψ and Φ must be identity. In particular Φ cannot erase Γ. An even shorter witness for the missing coordinate uses the two visible unitaries YIII and IYYY, whose product is Γ.

This is a finite proof, not a claim that testing a few channels exhausts all CPTP maps. The implementation verifies the generating words and product identities; the universal implication comes from the stated theorem.

### Common quantum encoder and decoder

For CPTP N:M16→Mm and R:Mm→M16, if the composition R∘N preserves all of S in the same exact all-input sense, the argument above gives R∘N=id on the full input algebra. Sixteen mutually orthogonal input states must remain perfectly distinguishable after N; their output supports must be mutually orthogonal. Hence m≥16.

This excludes a smaller carrier **under a common CPTP recovery contract**. It does not exclude feature coordinates, restrictions on allowed inputs, signed classical postprocessing, different observable encodings without a common quantum decoder, or approximate answers.

## 3. A valid noisy representation nevertheless exists

Consider the declared diagnostic family

\[
\Phi_{\lambda,t}(X)=\lambda X+(1-\lambda)\operatorname{Tr}(X)I/16
 +(t-\lambda)\operatorname{Tr}(\Gamma X)\Gamma/16.
\]

The implementation considers 0≤λ,t≤1. The identity gain is 1, the Γ gain is t, and the other 254 Pauli gains are λ. These are map parameters, **not time or a proposed physical decay law**.

In an orthonormal Pauli-Bell basis the normalized Choi eigenvalues (equivalently Pauli-mixture weights) are

\[
q_I=\frac{1+t+254\lambda}{256},
\]
\[
q_E=\frac{1+t-2\lambda}{256}
\quad(E\ne I,\ [E,\Gamma]=0;\ 127\text{ terms}),
\]
\[
q_E=\frac{1-t}{256}
\quad(\{E,\Gamma\}=0;\ 128\text{ terms}).
\]

They sum to 1. Within the specified unit square, complete positivity is equivalent to

\[
\boxed{\lambda\le(1+t)/2.}
\]

The Choi and Pauli-channel machinery is standard [2,3]. The displayed eigenvalues follow by the finite Pauli character transform and are checked independently by constructing the normalized Choi matrix from every matrix unit.

At the parity-erasing boundary t=0, λ=1/2,

\[
\boxed{\Phi_0(\rho)=\tfrac12\rho+\tfrac1{32}I
 -\tfrac1{32}\operatorname{Tr}(\Gamma\rho)\Gamma
 =\tfrac12\Pi(\rho)+\tfrac1{32}I.}
\]

This is a genuine CPTP map. A constructive Kraus representation has K0=I/√2 and KE=E/16 for each of the 128 Pauli operators anticommuting with Γ. Their K†K sum is exactly I. No random actual outcome is sampled in the simulator; a Kraus mixture describes a channel, not the program's RCR.

The two parity states (I±Γ)/16 both map to I/16. Γ is the channel's only erased linear direction. The channel has linear image dimension 255 and normalized-image affine dimension 254, but its output still lives in M16: it is **not a three-qubit or otherwise smaller carrier**.

The map is not idempotent. Applying it again shrinks the visible signals again. It is not silently substituted for a retained-algebra conditional expectation, RAS selector, or fundamental pruning event.

## 4. Exact prediction through an explicit readout

For A∈S, trace preservation and Γ-orthogonality give

\[
\operatorname{Tr}[A\Phi_{\lambda,t}(\rho)]
=\lambda\operatorname{Tr}(A\rho)+(1-\lambda)\operatorname{Tr}(A)/16.
\]

At positive λ the original expectation is therefore reconstructed from an ensemble estimate as

\[
\boxed{\langle A\rangle_\rho=
\frac{\langle A\rangle_{\Phi(\rho)}-(1-\lambda)\operatorname{Tr}(A)/16}{\lambda}.}
\]

For a traceless Pauli at the parity-erasing boundary this is simply twice the measured mean. For a balanced yes/no Pauli effect F=(I+P)/2 it is p=2p_out−1/2. The associated observable may have eigenvalues outside the original measurement range, so this is not a claim that a rescaled operator is itself a probability effect.

A nontraceless rank-one effect can have a larger direct probability change than a balanced Pauli effect: for an original |0000><0000| state/effect, the direct probability loss is 15/32, not 1/4. The 1/4 value applies to the balanced ±1 Pauli measurement witness. A review regression explicitly prevents advertising it as a universal bound on arbitrary yes/no observables.

### Sampling variance is real

For a Pauli observable with original mean a, measuring its ±1 output gives mean λa. The unbiased estimator X/λ has

\[
\operatorname{Var}(X/\lambda)=\lambda^{-2}-a^2.
\]

The ideal original measurement variance is 1−a². At λ=1/2 and a=0, these are 4 and 1 respectively. At a=1 they are 3 and 0, so there is **no universal constant variance ratio for every mean**. The inspector reports the chosen zero-mean example explicitly. No sampling experiment or finite-shot accuracy certificate is claimed; these are exact moment calculations.

This is not quantum-state recovery. Applying the affine signed reconstruction to the full matrix produces Π(ρ), which can still be nonpositive. Nor does the readout reconstruct Γ: that distinction is genuinely absent from this channel's retained output.

## 5. The half-signal cost is optimal for the stated direct-readout objective

Define, for any CPTP Φ on this same carrier,

\[
t=\operatorname{Tr}[\Gamma\Phi(\Gamma)]/16,
\quad
\delta=\max_{P\ne I,\Gamma}\|\Phi^*(P)-P\|_\infty.
\]

Exact erasure Φ(Γ)=0 implies t=0. The quantity δ is the largest worst-input **direct Pauli expectation error**, without re-encoding or gain correction.

Pauli twirling preserves all diagonal Pauli transfer coefficients and makes a Pauli channel with nonnegative probabilities q_E. For general Kraus operators Kj these probabilities are

\[
q_E=\sum_j|\operatorname{Tr}(EK_j)|^2/16^2.
\]

The original channel need not be unital or Pauli diagonal. This is an algebraic use of twirling, not a physical randomness assumption inserted into the ontology.

Let C be the 126 Pauli operators commuting with Γ other than I and Γ. Their character sum against an error E is 126 for E=I or Γ, −2 for the other commuting errors, and 0 for anticommuting errors. Therefore, writing c=(1+t)/2 for the total probability of commuting errors,

\[
\frac1{126}\sum_{P\in C}\frac{\operatorname{Tr}[P\Phi(P)]}{16}
=\frac{128(q_I+q_\Gamma)-2c}{126}\le c.
\]

For each P, \(|\operatorname{Tr}[P(\Phi^*(P)-P)]|/16\le\|\Phi^*(P)-P\|_\infty\). Consequently

\[
\boxed{\delta\ge(1-t)/2.}
\]

The displayed boundary family λ=(1+t)/2 attains equality: every visible traceless Pauli is scaled by λ. At t=0, the minimax direct-expectation error is therefore 1/2. This means some balanced Pauli yes/no probability has worst-input error at least 1/4. It does not mean all probabilities shift by 50%, or that gain-corrected ensemble estimates cannot be exact.

The finite proof supplies the universal bound. Code checks the exact integer character table, the saturating channels, a non-Pauli unitary, and a nonunital amplitude-damping comparison channel. The latter is a negative/generalization control, not a newly adopted physical process.

## 6. Integration with the unchanged simulation

Because every supplied U commutes with Γ,

\[
\Phi_{\lambda,t}(U\rho U^\dagger)=U\Phi_{\lambda,t}(\rho)U^\dagger.
\]

The noisy representation therefore uses the exact same finite motions. It introduces no replacement dynamics. The code checks 912 original observables from the fourteen eligible masks, at thirteen finite-word checkpoints on two input states: **23,712 decoded predictions**.

Largest decoded error: 6.591949208711867e−16. Largest direct, uncorrected target error in those fixtures: 0.13377729868937857. Maximum channel/motion covariance error: 4.650370270965911e−16. These sampled checks illustrate the exact all-input expectation identity; they are not its proof.

Maximum Kraus/formula discrepancy: 5.50e−16. Maximum independently constructed Choi-spectrum discrepancy: 4.44e−16. The computed boundary Choi minimum is −7.20e−17, numerical roundoff around the exact zero eigenvalue. The rejected raw predictor projection has the genuinely negative minimum −1/256 and 127 negative Choi directions.

## 7. What this establishes—and what it does not

The successful construction closes a **mathematical representation question** for this particular predictor: a valid same-carrier CPTP map can erase Γ while retaining all selected predictions after explicit ensemble readout scaling. A common noiseless CPTP decoder would instead force full-state recovery. Those statements are compatible.

The noisy map, its parameter family, and the minimax objective are declared diagnostic constructions. They are not accepted fundamental laws selecting physical pruning. There is no automatic actual outcome, entropy-production objective, calibrated time, new source coupling, change to the quantum carrier's origin, or gravitational fit. Coherent pre-time motion remains allowed; RAS and RCR retain their earlier separate conditional status. No universal destruction across every possible enlarged environment is inferred. Pillar 3 remains OPEN. No scientific novelty priority or physical breakthrough is claimed.

## 8. Reproducibility and delivery

The portable source includes the exact inherited v15.19 model and eight baseline Python files under SHA-256 verification. Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.10.8 were used locally. No baseline source was altered.

Tests were written and run before their implementations: thirty absent-model assertions and six absent-replay assertions were recorded. Review then added two failing scope tests, corrected the overly broad probability label, and strengthened rejection of an unsupported entropy claim. Final total: **38 new tests plus 272 selected prior tests = 310 local checks**. An aggregate regression command reached the container call limit after the earlier suites; the v15.19 suite was rerun separately and passed. No incomplete run is counted as a pass.

The 24-second 1280×720 H.264 movie is rendered from computed data. The offline inspector contains 441 parameter points; system Chromium/Playwright checks cover all 441, four preset controls, no external requests or JavaScript errors, and no horizontal overflow at widths 1280, 820 and 390. Native iPad/Safari attachment handling is untested. The MP4 was visually inspected and fully decoded locally.

This is a local delivery. No GitHub write or CI run was attempted in this step; no alternate write path was used to bypass the preceding upload blocks. There is no v15.20 branch or CI success claimed here. The work received self-review, not independent peer review, a formal proof-checker certificate, empirical validation, or a full-repository regression.

## Primary mathematical references

[1] M.-D. Choi, N. Johnston and D. W. Kribs, *The multiplicative domain in quantum error correction*, arXiv:0811.0947, https://arxiv.org/abs/0811.0947. The unitary-fixed-point implication is also explained by the coauthor at https://njohnston.ca/2009/07/a-brief-introduction-to-the-multiplicative-domain-and-its-role-in-quantum-error-correction/.

[2] S. T. Flammia and J. J. Wallman, *Efficient estimation of Pauli channels*, arXiv:1907.12976, https://arxiv.org/abs/1907.12976. Used for the standard Pauli-channel/twirling context, not the program's physical interpretation.

[3] IBM Quantum Learning, *Representations of channels*, https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels. Our Choi matrices are normalized to trace 1; some references instead use the unnormalized trace-d convention.
