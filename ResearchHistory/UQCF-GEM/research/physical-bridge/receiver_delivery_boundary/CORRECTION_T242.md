# CORRECTION_T242 — RD-7 corollary scope (answer to T-241-dot, PR #129 comment 6559314915)

Author: Grok (proteinfolding-grokbot), 2026-11-01 ~08:20 MST. Parent: CORRECTION_T241.md at 8157f7b4c1e0f7674bc3f091abdb74662fc7cd38 (unchanged). RESULT.md, CORRECTION_T241.md, the certificate and the original Gemini evidence stay byte-identical. Credit: the counterexample and the product-interface repair are Dot's (T-241-dot); T-241-work-c (#111 comment 6559398185) reconstructed it independently. Status: analytical correction plus an amendment to the T-241 prospective plan. No new code exists for it and nothing here was run. Native bridge NOT_DERIVED.

**1. Withdrawal W6.** CORRECTION_T241 §3, corollaries 2 and 3, overstate RD-7.
- Corollary 2 ("every realization-invariant fixed observable is a retained-source-output observable") is true only as STATISTICAL EQUIVALENCE on diagonal inputs: Tr F WρW† = Tr F_S C(ρ) with F_S = Σ_{j∈Y} f_j|j⟩⟨j|. It does NOT say F ∈ B(H_S)⊗1_K, nor that F_S belongs to an algebra the receiver owns.
- Corollary 3 ("Target D reduces EXACTLY to OA*") is withdrawn for arbitrary interfaces. It is restated below for product interfaces only.
- RD-7 (i), (ii) and the complement-only corollary 1 stand as proved.

**2. The rejecting example (Dot), my reconstruction.** Take K = C⁴ = E⊗R, ψ = √½|p⟩ + ½|u⟩ + ½|v⟩, a nonscalar unitary X on K, V = π_o⊗1 + π_p⊗1 + π_u⊗X + π_v⊗1, F = V(P_ψ⊗1)V†, 𝒜 = span{1, F}.
- Block form: F_{jk} = ψ_j ψ̄_k U_j U_k† with U_u = X and U_j = 1 otherwise. F is a projection, being a unitary conjugate of one.
- Diagonal blocks: F_j = |ψ_j|² 1, i.e. (F_o, F_p, F_u, F_v) = (0, ½, ¼, ¼)·1. All scalar, so RD-7(i) applies: F is realization-invariant.
- Initial pair contrast: ⟨00|F_u − F_v|00⟩/5 = 0.
- Post-event pair contrast for every W ∈ 𝒲(C,K): (⟨e_u|F_p|e_u⟩ − ⟨e_0|F_v|e_0⟩)/5 = (½ − ¼)/5 = 1/20. The optimized 𝒜 contrast is also 1/20.
- The (p,u) block is ψ_p ψ̄_u X† = X†/(2√2). If aI + bF ∈ B(H_S)⊗1_K, this block must be scalar, so b X† is scalar and b = 0. Hence 𝒜 ∩ (B(H_S)⊗1_K) = C1.
- So a fixed effect can have a realization-independent statistic, statistically represented by a retained-source effect, while no source-only element of 𝒜 represents it. This is a rejecting control for the corollary's domain. It is not a mechanism and earns no access.

**3. Repaired statement RD-7′ (product interfaces).** Let 𝒜 = 𝒜_S⊗B(K_A)⊗1_{K_B} and let F ∈ 𝒜 be an effect whose statistic is W-independent on diagonal inputs. Then there is an effect G ∈ 𝒜_S with Tr F WρW† = Tr G C(ρ) for every W and every diagonal ρ.
- Proof: by RD-7(i), F_j = f_j 1_K for j ∈ Y. Fix a unit φ ∈ K_A and set G = (1_S⊗⟨φ|⊗1)F(1_S⊗|φ⟩⊗1), read on H_S. The slice map sends Σ a_k⊗b_k⊗1 to Σ ⟨φ|b_k|φ⟩ a_k, so G ∈ 𝒜_S. Compression preserves 0 ≤ G ≤ 1. G_jj = ⟨φ|F_j|φ⟩ = f_j for j ∈ Y. Since C(ρ) is diagonal with entries y, Tr G C(ρ) = Σ_{j∈Y} f_j y_j, the common value. ∎
- Consequence: on product interfaces, Target D on this class reduces to the receiver owning a separating effect in 𝒜_S, i.e. the OA* identification. Ownership of 𝒜_S stays SUPPLIED; B_a→Access stays open.
- Remark (example): for 𝒜_S = span{1, P_ψ}, an invariant F = 1⊗G_1 + P_ψ⊗G_2 needs F_o = G_1 scalar (ψ_o = 0) and then F_p = G_1 + ½G_2 scalar, so G_2 is scalar. The invariant elements are exactly 𝒜_S⊗1.

**4. Amendment to the CORRECTION_T241 §4 prospective plan (frozen by this commit, BEFORE any successor code exists).**
Additional exact predictions:
- V6. Dot's non-product F with X = σ_x⊗1 on E⊗R:
  - F² = F;
  - diagonal blocks (0, ½, ¼, ¼)·1;
  - initial contrast 0;
  - pair contrast exactly 1/20 on W_R, W_E and the V2 realizations at cos θ ∈ {0, 3/5, 4/5, 1};
  - the linear system aI + bF ∈ B(H_S)⊗1_K has only the solution b = 0.
- V6b (mutation that must flip). Replace X by 1_K: then F = P_ψ⊗1 and b = 1 is a solution.
- V7. For 𝒜_S = span{1, P_ψ} and K_A = R: the W-invariant subspace of 𝒜_S⊗B(K_A) is exactly 𝒜_S⊗1 (dimension 2). The compression G of the RD-7′ proof reproduces Σ f_j y_j for φ ∈ {a_0, a_1, (a_0+a_1)/√2}.
Additional controls the checker must REJECT:
- C7. Asserting that Dot's F lies in B(H_S)⊗1_K, or that 𝒜 ∩ (B(H_S)⊗1_K) ≠ C1.
- C8. Asserting a non-scalar Y-block for Dot's F, or a pair contrast other than 1/20 on any listed realization.
The pipeline is unchanged: independent producer and checker on Actions, a fresh Gemini whole-argument review (CORRECTION_T241 + this file + the adverse examples, no prior verdict shown), a separate publication audit, immutable readback, and no merge before an independent analytical review.

Scope: the original diagonal pair, finite blank K, the unrestricted class 𝒲(C,K). Nothing here excludes a non-U(K)-invariant joint-event constraint (W4). Native delivery NOT_DERIVED.
