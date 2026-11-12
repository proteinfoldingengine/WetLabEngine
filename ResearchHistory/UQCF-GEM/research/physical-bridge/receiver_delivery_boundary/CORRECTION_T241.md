# CORRECTION T-241 to the T-240 receiver-delivery boundary (successor; RESULT.md unchanged)

Status: `CORRECTION_PENDING_PROSPECTIVE_VERIFICATION_AND_FRESH_REVIEW`. Native bridge `NOT_DERIVED`; scientific_breakthrough: false; no claimStatus change.

This file answers T-239-dot-c (PR #111 comment 6558980114), T-240-work-b (6559153316) and the REQUEST CHANGES review 5728521639 on PR #129. The frozen RESULT.md at science freeze 0c05b4e132ad18acd21f64ec1318d9fdb41e7fd4 (blob a04f23b6f667cf61c32149b1f3bb6e0316e60377), its certificate and the Gemini verdict of run 41313483346 are preserved unchanged as the original record, including the claims withdrawn below. That ACCEPTED verdict does NOT cover this correction. Thread entry: T-241 on grok/agent-thread at 35d5f12e91a46903c37671b7b2d97eeafc429528.

Credits: W1-W3 are Dot's counterchecks (T-239-dot-c). W4, W5 and the range theorem in §2 are from T-240-work-b and its review. RD-7 is new in T-241.

**1. Withdrawals (the frozen RESULT at 0c05b4e1 stays byte-identical; these are recorded as failed claims).**
- W1. RESULT §2 "and also C, exactly when OA* ∨ OC" is FALSE. Dot's coherent counterexample (ψ = √½|p⟩+½|u⟩+½|v⟩, 𝒜_S = span{1,P_ψ}, interface 𝒜_S⊗1_E⊗B(R)): initial contrast 0, W_E gives 1/20, W_R gives 1/5. OA* holds, B holds, C fails. RD-4 proves only B.
- W2. RD-5 "every S-interface is blind both before and after" for z'_± = (1,2,1,1)/5, (1,1,2,1)/5 is FALSE before the event (π_p: 2/5 vs 1/5). Correct statement: equal y gives C(ρ'_+) = C(ρ'_-), so every S-interface is blind AFTER the event. The ker P_XY versus owner-coordinate point is unaffected.
- W3. RESULT §5 "every effect on all of K gives the same statistics for both (RD-3)" is FALSE pointwise. F = 1_S⊗|01⟩⟨01| has pair contrast 1/5 under W_R and 0 under W_E. RD-3 is invariance of the OPTIMIZED contrast only. The 𝒜_S⊗1_K half of the sentence is correct.
- W4. RD-6 "a non-tautological minimal new premise can live only in identification language" is NOT PROVED and is withdrawn. RD-6 items 1-3 and 5 stand. Item 4 shows only that the weakest realization predicate is the target itself and that a forcing K cannot be U(K)-invariant. An independently sourced joint-event constraint that breaks U(K)-invariance is still eligible (Target B). Whether one is inherited is a provenance question, not settled by RD-6.
- W5. T-240 and the PR summary said "all ... plus I* admit both". RESULT row 9a (I* n/a, SUPPLIED) is the correct entry. Row 10 means "none found in the inspected sources", not "no K exists". RD-1's "every inherited constraint" means the typed and inspected rows of §4, with the nonempty admitted class. select_record covariance moves the supplied projectors and certifies nothing about a FIXED R-owned projector.

**2. Adopted repair (T-240-work-b), independently checked.** Take the original pair, the unrestricted class, and dim K_A, dim K_B ≥ 2. Write d_S = Δ_{𝒜_S}(C). Then {Δ_𝒜(W) : W ∈ 𝒲(C,K)} = [d_S, 1/5].
- My check of each step: (a) the lift F⊗1 gives the lower bound, which is RD-2 step 1. (b) e_u = a_0⊗b_1 gives C(ρ)⊗|a_0⟩⟨a_0|, and compression onto a_0 lands in 𝒜_S, which is RD-2 steps 2-4. (c) e_u = a_1⊗b_0 makes 1_S⊗|a_1⟩⟨a_1|⊗1 a z_u-flag with contrast 1/5 = ½‖Δρ‖₁, and isometries do not increase trace distance. (d) e_u(θ) = cos θ a_0⊗b_1 + sin θ a_1⊗b_0 is orthonormal to e_0 = a_0⊗b_0 for every θ. Δ_𝒜 is a maximum of a linear functional over a fixed compact set, so it is 1-Lipschitz in WΔρW† and continuous in θ.
- Consequences for the proper product case: uniform delivery B holds iff d_S > 0, and constant optimized contrast C holds iff d_S = 1/5 (plus initial blindness, still separate).
- Degenerate cases: if K_A is trivial, Δ ≡ d_S. If K_B is trivial, Δ ≡ 1/5.
- 𝒜_S = span{1,π_p} is initially blind with d_S = 1/5, so a proper complementary factor does not by itself make Δ vary (this corrects RESULT L111). 𝒜_S = C1 gives the full range [0,1/5].

**3. New: RD-7 (which FIXED observables are realization-invariant).** Let dim K ≥ 2. For F ∈ B(H_S⊗K) and j ∈ H_S basis, write F_j := (⟨j|⊗1)F(|j⟩⊗1) ∈ B(K).
- (i) Tr F WρW† is the same for every W ∈ 𝒲(C,K), for every diagonal input ρ, iff F_j = f_j 1_K for every j ∈ Y. The common value is then Σ_{j∈Y} f_j y_j, with y = P_XY z. So it is the statistic of the retained-source-output effect F_S = Σ_{j∈Y} f_j|j⟩⟨j| on C(ρ).
- (ii) For the original pair alone with dim K ≥ 3, the pair contrast of F is W-independent iff F_p and F_v are scalar. The value is then (f_p − f_v)/5.
- Proof:
  1. For diagonal ρ, WρW† = Σ_{j∈Y} z_j |j e_0⟩⟨j e_0| + z_u |p e_u⟩⟨p e_u|, so Tr F WρW† = Σ_{j∈Y} z_j ⟨e_0|F_j|e_0⟩ + z_u ⟨e_u|F_p|e_u⟩. (⇐) is immediate.
  2. (i ⇒) Put ρ = |j⟩⟨j|, j ∈ Y. Every unit vector is the e_0 of some W because dim K ≥ 2 (RD-0). A Hermitian F_j with a constant quadratic form on unit vectors is scalar.
  3. (ii ⇒) The contrast is (⟨e_u|F_p|e_u⟩ − ⟨e_0|F_v|e_0⟩)/5. Fix e_0 and vary e_u over e_0^⊥. Given unit x, y and dim K ≥ 3, choose e_0 ⊥ x, y, so ⟨x|F_p|x⟩ = ⟨y|F_p|y⟩ and F_p = f_p 1. Then varying e_0 gives F_v = f_v 1. ∎
  4. (For dim K = 2 the pair-only condition weakens to F_p + F_v scalar, since e_u is fixed by e_0 up to phase.)
- Corollaries:
  - A complement-only effect 1_S⊗G is realization-invariant iff G is scalar, i.e. trivial. No nontrivial fixed observable on the complement (R, E or any factor) has W-independent statistics.
  - On the diagonal benchmark, every realization-invariant fixed observable is a retained-source-output observable. T-240-work-b's F*⊗1 is the case F_S = F*.
  - Therefore Target D ("realization-invariant receiver observable") on this class reduces EXACTLY to the receiver owning a separating retained-source-output effect, which is the OA* identification. It does not reduce to any complement observable.
- This is a classification inside the supplied class. It does not supply or derive that ownership (B_a→Access stays open), and it does not exclude a non-U(K)-invariant joint-event constraint that changes the class (W4).

**4. Prospective verification plan for the successor (frozen by this commit, BEFORE any successor code exists).**

Exact predictions:
- V1. Dot interface 𝒜_S = span{1,P_ψ}, ψ = √½|p⟩+½|u⟩+½|v⟩, ⊗1_E⊗B(R):
  - pre-event contrast 0;
  - Δ(W_E) = 1/20, Δ(W_R) = 1/5;
  - d_S = 1/20.
  - All evaluated exactly (sympy rationals/radicals) through block-wise positive parts.
- V2. θ-family e_0 = a_0⊗b_0, e_u(θ) = cos θ a_0⊗b_1 + sin θ a_1⊗b_0 with K_A = R, K_B = E. The endpoints are exactly:
  - (d_S, 1/5) = (1/20, 1/5) for span{1,P_ψ};
  - (0, 1/5) for C1;
  - (1/5, 1/5) for span{1,π_p}.
  - Δ ≥ d_S and Δ ≤ 1/5 at every one of a fixed set of rational-cosine points (cos θ ∈ {0, 3/5, 4/5, 1}).
- V3. Dot-2: π_p pre-event 2/5 vs 1/5 for z'_±; post-event C(ρ'_+) = C(ρ'_-) exactly.
- V4. Dot-3: fixed F = 1_S⊗|01⟩⟨01| gives pair contrast 1/5 (W_R) and 0 (W_E).
- V5. RD-7 (i), on W_R, W_E and three fixed exact non-basis realizations from the V2 family:
  - an F with scalar Y-blocks f = (1/3, 1/2, ·, 1/4) and arbitrary fixed off-diagonal/u blocks gives W-independent statistics equal to Σ f_j y_j for z_±.
  - (ii) F with F_p = diag(1,0,0,0) on K, all else 0, gives different pair contrasts on two named realizations.

Controls that must be REJECTED by the checker:
- C1. Replacing 1/20 by 1/5 in V1 (the withdrawn "C" claim).
- C2. Asserting pre-event S-blindness for z'_± (the withdrawn RD-5 sentence).
- C3. Asserting equal W_R/W_E statistics for the fixed full-K effect (the withdrawn §5 sentence).
- C4. Perturbing one F_j (j ∈ Y) off scalar by a fixed rank-one term while claiming invariance.
- C5. A corrupted producer output (one altered rational).
- C6. Swapping W_R and W_E labels in V4.

Pipeline:
- Independent producer and checker (the checker rebuilds every operator from its definition). Run on GitHub Actions only; no local run before the workflow, or a disclosed one if needed.
- A fresh Gemini whole-argument review of this CORRECTION plus the adverse examples, without showing any prior verdict.
- A separate publication audit and immutable readback.
- No merge before all of these and an independent analytical review.

Scope: the original diagonal pair, finite blank K, and the unrestricted realization class 𝒲(C,K). Nothing here excludes an independently sourced joint-event constraint that is not U(K)-invariant (W4).
