# PREREGISTRATION — thermal-bath / pure-receiver follow-up (T-271)

Byte-exact copy of thread entry T-271 (grok/agent-thread d37a3be5ed21309a945d6c1e1be284d483f9b0be), committed before any execution. Base: research 750554de. NEW ASSUMPTION; native bridge NOT_DERIVED.

## T-271 (Grok) — PREREGISTRATION of one bounded follow-up test: a physically motivated ingredient to break the R/E tie left open by T-270. Nothing has been executed for this test at the time of this commit. The ingredient is a NEW ASSUMPTION. Native bridge NOT_DERIVED.
Parents: T-270 (agent-thread a72bbfd9; PR #130 open, not merged, head 0531fb5f), T-268 (π_p/π_v owner falsifier), T-262 (Lemma Σ′). Base: research head 750554de; new branch grok/thermal-bath-purity-test (based on the research head, not on PR #130).
Authorization: Aaron, 12:49 PM MST 2026-11-02, "Yes, go ahead". This answered Science Discovery X Bot's question asking whether to have this agent design the next test, with predictions committed first and everything kept NOT_DERIVED. It covers one bounded test and one Gemini review.

### 0. The constraint (swap covariance)
By RD-9/RD-9′, Lemma E2 and Lemma Σ, swapping both the writer and the ingredient always reproduces a pass. That is unavoidable and is not a failure. The discriminating control therefore keeps the ingredient FIXED and swaps only the writer (W_R → W_E). An ingredient that simply forbids E from acting ("E is not coupled") restates the target and cannot count as a pass.

### 1. Requested candidate first: owner-local attachment. REJECTED by vetting, not run
INHERITED: owner/address data (owner(u)=p, y_p=z_p+z_u). NEW: each native address a carries a local carrier R_a, the erased-branch record is written into R_owner, and E is an unindexed common sink.
- **Q-b, owner coordinate y recoverable from the receiver family.** (iii) fails because W_R fails it as well. For every realization of C, W|p⟩=|p⟩e_p and W|v⟩=|v⟩e_v must satisfy ⟨e_v|e_p⟩=1, because C keeps the coherence |p⟩⟨v|. So π_p and π_v leave identical states on every receiver or environment factor, while y_p is 1 versus 0. The T-268 falsifier therefore survives any attachment rule. The weaker reading, "the owner of the erased branch is recoverable", is (i) forced: the complementary channel of C₁C₂ must hold orthogonal records of the decohered erasure branches, whichever system holds the record. Reading it "from the owner-indexed family" is (ii) tautological. With an adequately sized E register, the fixed-ingredient mirror also recovers it from E, so (iii) fails.
- **Q-a, per-carrier capacity pattern.** This is the Stinespring minimal-dilation bound localized by the ingredient's own placement rule, so it fails (i) and (ii). Side consequence, recorded: a shared owner with two decohered erased children needs dim R_p ≥ 3, so owner-local qubits are ill-posed there. The fixed-ingredient mirror either breaks the placement rule by definition (tautology), or with E of dimension ≥ the Choi rank it passes. If "unindexed" is read as one fixed-size cell, its failure is T-270's X2 obstruction applied to an asymmetrically sized sink, which the definition builds in.
- **Verdict.** No admissible discriminating prediction for owner-local attachment.

### 2. Other alternatives
- **Coupling, adjacency or locality** (event gates act only on (u, owner, local carrier)). If E is not adjacent, that is "E not coupled", the target restated. If E is adjacent everywhere, the setup is symmetric and the mirror passes.
- **Readout or accessibility** ("only R is read later"). The native consumer is exactly the open native obligation (T-270 Gemini next_native_obligation). Supplying it restates the target.
- **Thermal bath with a pure blank receiver (Landauer / third law). CHOSEN.** It constrains an initial state, not the writer or the coupling. E may still couple and be written.

### 3. Ingredient TB (NEW ASSUMPTION)
E is a finite-dimensional thermal bath at T > 0, so its initial state τ_E is full rank (a Gibbs state of a finite Hamiltonian; at positive temperature a bath has no pure component). R starts in the supplied pure blank |0⟩_R. The event dynamics is an ARBITRARY unitary U on S⊗E⊗R, with no coupling restriction.
- INHERITED: tree, P, I, owner/address data.
- ACCEPTED-CONDITIONAL / SUPPLIED: H_S, C(ρ)=QρQ+ρ_uu|p⟩⟨p|, K=E⊗R, the pure R blank, the dimensions (d_E=d_R=2 main; d_E=4 threshold), and the realization class.
- Test values: τ_q=diag(2/3,1/3) and τ_½=I/2.

A realization is a U with Φ_U(ρ)=Tr_ER U(ρ⊗τ_E⊗|0⟩⟨0|_R)U† = C(ρ) for all ρ. Classes:
- 𝓔₀ (E untouched): U=U_SR⊗I_E.
- 𝓡₀ (R untouched; the fixed-ingredient mirror of W_E): U=U_SE⊗I_R.

**Theorem L (Landauer rank bound; proof frozen here).** Let ρ* = (π_p+π_u)/2, so C(ρ*)=π_p. For U ∈ 𝓡₀, ⟨p|Φ_U(ρ*)|p⟩ = Tr[(π_p⊗I_E) U(ρ*⊗τ_E)U†] ≤ KF_{d_E}(ρ*⊗τ_E), the sum of the d_E largest eigenvalues (Ky Fan maximum principle; π_p⊗I_E has rank d_E). The bound is attained by a unitary that maps the top eigenvectors into ran(π_p⊗I_E).
- Hence 𝓡₀ contains an exact realization only if rank(τ_E) ≤ d_E/2.
- Conversely, if rank(τ_E) ≤ d_E/2 it does: map |u⟩⊗supp τ into |p⟩⊗(supp τ)^⊥ and act as the identity elsewhere. Every cross term then carries Tr|k′⟩⟨k| = 0 for k′ ⊥ k.
- A full-rank τ_E means no R-untouched realization exists.
- KF values: τ_q → 2/3; τ_½ → 1/2; d_E=4 with rank 2 → 1 (exists); d_E=4 with rank 3 → 2/3.

**Lemma PP (post-processing covariance).** If U realizes C, then so does (I_S⊗V)U for every unitary V on E⊗R, because the trace over E⊗R is unchanged. With V = SWAP_ER, W_R⊗I_E becomes "W_R;SWAP", which leaves R in τ_E independently of the input (D_R=0) and puts the record in E (D_E=1/5). Therefore **no ingredient that constrains only initial states can fix where the record ends up.** TB can only force R's purity to be consumed.

### 4. Predictions and PASS/FAIL criteria
- **Q-1 (counted).** Under τ_q and under τ_½:
  - (a) W_R⊗I_E realizes C exactly.
  - (b) The exact optimum of ⟨p|Φ_U(ρ*)|p⟩ over 𝓡₀ is KF: 2/3 and 1/2. It is attained exactly by the canonical W_E completion (the transposition |u,0⟩↔|p,1⟩ on S⊗E), and no 𝓡₀ unitary exceeds it. Supplementary check: 2000 Haar-random U_SE with numpy seed 271, max ≤ KF.
  - (c) Threshold "iff" at d_E=4: rank 2 gives an explicit exact 𝓡₀ realization; rank 3 gives optimum 2/3.
  - PASS iff (a)–(c) all hold. FAIL if W_R⊗I_E fails, or if any 𝓡₀ value exceeds KF (that would refute Theorem L, i.e. a proof or code error).
  - Vetting:
    - (i) Without TB (pure E), the R-untouched W_E realizes C exactly (T-262/T-270), so Q-1 is not forced by unitarity, Stinespring or subadditivity alone. It is a theorem of TB plus unitarity plus Ky Fan, predictable in advance; the run is a bounded exact check.
    - (ii) TB fixes an initial state, not the writer. E-touching realizations survive (see controls). It is not "E not coupled" restated, but the asymmetry is SUPPLIED: the tie-break is moved into the ingredient, not derived.
    - (iii) The fixed-ingredient mirror fails (2/3, 1/2 < 1) while W_R passes.
    - (iv) Two events, fresh slots: W_R per slot ⊗ I_E realizes C₁C₂ exactly on carriers A and B (T-270 dim R ≥ Choi rank is unchanged). The 𝓡₀ optimum is KF = 2/3 (A, ρ*=(π_{p1}+π_{u1})/2) and 1/3 (B, ρ* uniform on {p1,u1}⊗{p2,u2}). The existence threshold becomes rank τ_E ≤ d_E/f, where f is the fan-in.
- **Q-L (record location): NOT admissible as discriminating.** By Lemma PP, (iii) fails: the mirror "W_R;SWAP" passes with the ingredient fixed. Recorded as an expected negative.
- **Q-2 (consistency, not counted).** Under τ_½, every realization satisfies S(ω_R) ≥ S(ρ)−S(C(ρ)), by subadditivity plus TB (log d_E is already used up). It is forced, so it is P-b-like. Checked with mpmath at 50 digits, seed 271, 200 inputs plus diagonal specials.

### 5. Controls and expected verdicts (under τ_q and τ_½ unless stated)
| control | expected |
|---|---|
| W_R⊗I_E | realizes C; Q-1 PASS; D_E=0, D_R=1/5 |
| W_E, fixed-ingredient mirror (𝓡₀; canonical completion) | does not realize C; value 2/3 or 1/2 = KF; FAIL |
| W_E^c (W_E on the E=0 branch, completed on the E=1 branch by the rule below, which touches R) | realizes C; shows the W_E isometry survives only by consuming R's purity |
| W_Bell^c, W_W^c (T-269 frames on the E=0 branch, same completion rule) | realize C, so TB does not single out W_R |
| W_R;SWAP | realizes C; D_R=0, D_E=1/5 (record in E; Lemma PP) |
| jointly swapped mirror (τ on R, pure E; writer W_E⊗I_R) | realizes C; sanity PASS. In that swapped world W_R⊗I_E attains only KF=2/3 |
| threshold d_E=4 | rank 2: exact 𝓡₀ realization exists; rank 3: 2/3 |
| owner illustrations (not counted) | (1) for every control, π_p and π_v give equal K states; (2) carrier A with a 3-dim append E register realizes C₁C₂, and the erased address is recoverable from E |

Completion rule: on the E=|1⟩, R=|0⟩ input, e′_0 is the normalized projection of |10⟩ onto span{e_0,e_u}^⊥. If that projection is zero, use |11⟩, then |01⟩. e′_u is the next Gram–Schmidt vector from (|11⟩, |01⟩, |00⟩). The remaining inputs are completed by an exact orthonormal extension. Basis order is (E,R).

### 6. Expected outcome (analytic, disclosed)
Q-1 PASS: the T-270 tie between E-α and its R-untouched mirror is broken under TB. Q-L negative: TB does not fix record location, and no initial-state ingredient can. TB does not select W_R among E-touching writers. Q-2 consistency holds.

Plan: one local exact sympy run (script and SHA-256 under /workspace/uqcf_scratch/t271/), an optional independent numpy checker (failures kept), frozen files in constructive_candidates/thermal_bath_purity_test/ with SHA256SUMS, a PR into the research branch (no merge), one Gemini review via Actions, and the result in T-272. The criteria are frozen here. TB stays NEW, and the native bridge stays NOT_DERIVED.
