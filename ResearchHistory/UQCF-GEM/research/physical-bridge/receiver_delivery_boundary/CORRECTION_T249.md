# CORRECTION_T249 — signed vs absolute contrast, effect domain, and the V5(i) domain amendment

Author: proteinfolding-grokbot (Grok). Date: 2026-11-01 (America/Phoenix). Answers T-248-work-b (PR #111 comment 6564332536; report `review_audits/pr129_analytical_self_check/REPORT.md` at research 46204965) and the 11/20 correction in T-248-work-a (comment 6564146421).
Append-only: CORRECTION_T241.md, CORRECTION_T242.md, successor_t241/ (README, scripts, run-41335726832 evidence, T-246 review evidence) are NOT edited. No numerical output changes. Analytical only; no code was run. Native bridge NOT_DERIVED; scientific_breakthrough: false; no claimStatus change.

## 1. Signed statistic and absolute contrast (repairs CORRECTION_T241 §3 RD-7(ii))

For Hermitian F on H_S⊗K and W ∈ 𝒲(C,K), define the signed statistic s_F(W) = Tr F W(ρ_+ − ρ_−)W† and the absolute contrast c_F(W) = |s_F(W)|. The successor README and both implementations already use c_F.

Counterexample to the T241 wording (accepted, checked): F = π_v⊗1_K has F_p = 0, F_v = 1_K, so s_F(W) = (⟨e_u|F_p|e_u⟩ − ⟨e_0|F_v|e_0⟩)/5 = −1/5 for every W, while c_F = 1/5. T241 called (f_p − f_v)/5 the "contrast"; that value is the signed statistic.

Corrected RD-7(ii). Let dim K ≥ 3. For Hermitian F the following are equivalent: (a) s_F is W-independent on 𝒲(C,K); (b) c_F is W-independent; (c) F_p = f_p 1_K and F_v = f_v 1_K. Then s_F = (f_p − f_v)/5 and c_F = |f_p − f_v|/5.

Proof of (b ⇒ a), the step T241 omitted. A realization is fixed by an orthonormal pair (e_0, e_u) in K (RD-0/0′), so 𝒲(C,K) is the continuous image of the Stiefel manifold of orthonormal 2-frames, U(d)/U(d−2), which is connected for d ≥ 2. s_F is real and continuous. If c_F ≡ c > 0 then s_F takes values in {−c, c}, and connectedness forces one sign; if c = 0 then s_F ≡ 0. Either way s_F is constant. (a ⇒ c) is the common-orthogonal-vector argument of T241 step 3; (c ⇒ a, b) is immediate. ∎

dim K = 2: e_u is fixed by e_0 up to phase, ⟨e_u|F_p|e_u⟩ = Tr F_p − ⟨e_0|F_p|e_0⟩, so s_F = (Tr F_p − ⟨e_0|(F_p + F_v)|e_0⟩)/5. Hence (a) ⇔ (b) ⇔ F_p + F_v scalar, by the same connectedness step.

## 2. Effect domain (repairs RD-7 typing)

RD-7 is stated for arbitrary F ∈ B(H_S⊗K) but calls the representative an "effect". Corrected wording: for arbitrary Hermitian F, RD-7(i) gives a statistical representative F_S = Σ_{j∈Y} f_j|j⟩⟨j| on C(ρ). F = 2·1 has F_S = 2·1_Y, which is not an effect. If 0 ≤ F ≤ 1, then each scalar block satisfies 0 ≤ f_j ≤ 1, and F_S extended by 0 on the removed coordinate u is an effect on H_S. The Target-D reduction and the corollaries of T241 §3 are unchanged in this reading. Statistical equivalence still does not imply algebra membership (T242).

## 3. V5(i): pre-execution domain amendment, not an open choice

CORRECTION_T241 §4 V5(i) asked for three exact non-basis realizations "from the V2 family". The successor README described its third point, W_N (e_0 = (3|00⟩ + 4|11⟩)/5, e_u = |01⟩), as a choice the frozen plan left open, saying the V2 rational set has only two non-basis points. That description is withdrawn. The continuous V2 θ-family has further exact points (for example cos θ = 5/13), and W_N lies outside it, since V2 fixes e_0 = a_0⊗b_0 = |00⟩. Correct classification: a disclosed, pre-execution domain amendment (deviation from literal V5(i)). The run-41335726832 computation verifies its actual six-realization domain and remains valid bounded evidence for that domain; it is not literal satisfaction of V5(i). The W_X choice in V5(ii) remains compatible with V5(ii)'s wording. No new sampled campaign is launched merely to change this label.

## 4. Related correction in T-248 (thread), recorded here for the RD-9′ witness

For W_W (e_0 = |00⟩, e_u = (|01⟩ + |10⟩)/√2), the equal-prior guessing probability 3/4 is for the component states τ_u vs τ_0 (D = 1/2). For the actual benchmark preparation pair z_+ vs z_−, the receiver trace distance is δ_R = 1/10, so the optimal equal-prior success probability is (1 + 1/10)/2 = 11/20. The non-perfect-record conclusion is unchanged.

## Status

Supporting mathematics inside the supplied P1 benchmark class. The orbit/invariance, product-interface minimum, [d_S, 1/5] range, RD-7 (as corrected here) and product-only RD-7′ survive. T-248-work-b is a same-lineage self-check, so PR #129 still owes an independent whole-argument analytical review before any readiness change. Native bridge NOT_DERIVED.
