# Preregistration: independent reconstruction, controls and Gemini review of ADMISSION.md

Date: 2026-10-16 America/New_York (~21:30 ET). Author: proteinfolding-grokbot (UQCF Science Agent).
Frozen argument: `ADMISSION.md` blob `6debf31d…` as committed at `05b43cdabe3368784f5384d05d6fdec9cb4e7e94` (unchanged at `75054cf359b34c274366becc9850d0c6281f92ae`).
Source parent for pinned evidence: `8129e79ee00608b6fc760532eff6360019e5f43a`.

This file is committed and pushed **before** any reconstruction code is written or executed. No exploratory numerical run of Theorems A/B was performed before this commit; the only prior checks were the hand derivations in ADMISSION.md and an author self-check by reading (not a review). ADMISSION.md is not modified by this contract. If anything below fails, the failure is preserved and any correction to ADMISSION.md is a new commit with a fresh run.

## 1. Scope

Bounded finite-dimensional numerical reconstruction of the two mathematical statements in ADMISSION.md §2 (Theorem A (a)–(c), Theorem B, the self-reference Corollary) and the analytic controls K1–K7 of §3, followed by one Gemini review. No inherited replay, scientific stage, test-count change, native-mechanism claim or main merge. A finite no-counterexample result is bounded evidence, not a proof; the proofs are the text.

## 2. Producer and checker (algorithmically independent)

- **Producer** `.github/scripts/uqcf_relref_formula.py`: evaluates the claimed closed forms only: T_formula = ½Σ_i|Tr[Δ_iσ_i]| with σ_i = P_iσP_i, the reader E* = Σ_i (P_i⊗P_i)(I+s_iF_i)/2, the Corollary value ¼‖Δ‖₂², and the predicted commutant dimension Σ_i(2 if n_i≥2 else 1) + 4·C(m,2) (diagnostic).
- **Checker** `.github/scripts/uqcf_relref_checker.py`: does not import the producer and uses no block, swap or Schur–Weyl structure. It (i) builds the Lie-algebra representation of the declared symmetry group on the full tensor space from an orthonormal basis of block-diagonal anti-Hermitian generators, (ii) computes the commutant as the numerical null space of the stacked commutator maps (SVD, rank cutoff 1e-9 × largest singular value, recording the spectral gap), (iii) orthonormalises it in Hilbert–Schmidt inner product, (iv) for a contrast operator D (Hermitian, traceless) computes the HS projection E_C(D) onto the commutant and returns T_check = Tr[(E_C(D))_+], which equals max over invariant effects 0 ≤ E ≤ I of Tr[E D] because the commutant is a unital *-algebra and E_C is its trace-preserving conditional expectation. It also checks commutation of any supplied effect.
- **Comparator** `.github/scripts/uqcf_relref_reconstruct.py`: generates the declared universe, calls both, compares, runs rejecting controls, writes `certificate.json`.

## 3. Declared universe (complete; every record kept, including failures)

Block structures, in order: (2), (3), (1,2), (2,2), (1,3), (2,3), (1,1,2). Structure k uses `numpy.random.default_rng(20261016 + k)`. Random states are Ginibre-generated (G G†/Tr) restricted as stated. Central-blind pairs: ρ_0 random in A; ρ_1 = Σ_i p_i τ_i with p_i = Tr[P_iρ_0] and τ_i random block states. Unitarily related pairs: ρ_1 = uρ_0u*, u Haar-random in U(A) (block QR).

Per structure:
- **B-in**: 8 central-blind pairs with random σ ∈ A (identified copy). Require |T_check − T_formula| ≤ 1e-8 and that E* commutes with the representation and attains T_formula.
- **B-out**: 4 central-blind pairs with random σ on the full H (σ ∉ A). Same requirement (tests that only σ_i = P_iσP_i enters).
- **COR**: 4 unitarily related pairs, σ = ρ_0. Require T_check = ¼‖Δ‖₂² within 1e-8 and T > 0.
- **A-a**: 4 central-blind pairs with ω = I/N, 2 with random central ω = Σ_i c_i I_i/n_i (identified copy). Require T_check ≤ 1e-8.
- **A-b**: 4 central-blind pairs, unidentified copy (symmetry U(A)×U(A), independent actions), random noncentral ω. Require T_check ≤ 1e-8.
- **A-c**: 4 unitarily related pairs, two source copies, no rest; contrast ρ_1^{⊗2} − ρ_0^{⊗2} under the diagonal action. Require T_check ≤ 1e-8.
- **DIM** (diagnostic, not a pass gate for Theorems A/B): checker commutant dimension of the identified diagonal action versus the producer prediction. A mismatch is recorded and reported, and blocks review only if it coincides with a value mismatch.

Analytic controls (exact predicted values):
- **K3** qubit, ρ_0 = |1⟩⟨1|, ρ_1 = |0⟩⟨0|, σ = (I+X)/2: T = 0.
- **K4** structure (2), two copies, |0⟩⟨0| versus I/2, no rest: T = ¼ (outside single-copy scope; must be nonzero).
- **K5** qubit, same pair, σ = |0⟩⟨0|: T = ½; with identification twisted by Hadamard v (σ ↦ vσv*): T = 0.
- **K6** answer-bearing reference σ = ρ_b is excluded by premise; recorded only as the value the checker gives for σ = ρ_1 on the K3 pair (T = ½), labelled NOT_A_CONSEQUENCE.
- **K7** structure (1,2): changing σ's weight on the one-dimensional block (renormalised) leaves T_check/T_formula scaled only through the n=2 block term; recorded.
- **ORTH** orthogonal pure qubits, σ = ρ_0: T = ½.

## 4. Rejecting controls (each must be detected)

- W1 wrong closed form ½|Σ_iTr[Δ_iσ_i]| must mismatch T_check on at least one B-in record.
- W2 sign-flipped reader (s_i ↦ −s_i) must fail to attain T_check on every B-in record with T_check > 1e-6.
- W3 the non-invariant effect |0⟩⟨0|⊗|0⟩⟨0| must be rejected by the checker's commutation test.
- W4 a tampered certificate (one T value perturbed by 1e-3; one record deleted; one record duplicated; one record key substituted) must each be rejected by the comparator's universe/value validation.

## 5. Pass criteria, stopping rules, resources

GREEN iff every B-in, B-out, COR, A-a, A-b, A-c, K3–K5, ORTH requirement holds and W1–W4 are each detected. Otherwise RED: the certificate is preserved and uploaded, review does not run, and no tolerance, domain or seed is changed without a new recorded commit. Pinned: Python 3.12.12, numpy 2.1.3. One Gemini availability check and one generation request (gemini-3.1-pro-preview); on any HTTP failure the run stops with sanitized evidence and is not retried without Aaron's authorization or a fixed cause.

## 6. Jobs (GitHub Actions, gated in order)

integrity (exact input bytes and ancestry) → reconstruction-and-controls (producer, independent checker, comparator, rejecting controls) → gemini-review (frozen ADMISSION.md, this contract, the reconstruction certificate and a pinned source packet from `8129e79e`) → publication-audit (independent remote byte readback of the triggering commit, inputs, sources and review bytes). Durable evidence is then committed and an immutable author readback recorded.

## 7. Reviewer request

See `REVIEW_INSTRUCTIONS.txt` (frozen in this commit). ACCEPTED is analytical review of bounded admission bookkeeping, not native-physical validation. Native interaction milestone remains NOT ACHIEVED regardless of verdict.
