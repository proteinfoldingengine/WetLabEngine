# Covariant outcome register: invariant seeds give contrast only through a continuous orientation record

Date: 2026-10-16 America/New_York. Parent: `b2a78583eb14930f775e29b8eb05293810f1b098`. Preregistration: `PREREGISTRATION.md`, commit `7c1bde935cdc97ee709e6bb7bf27a7a978d87359` (precedes this note).

**Conditional analytical characterization for a declared candidate class, with a finite-register no-go. Native milestone NOT ACHIEVED.** Sketch items S1–S6 (task) and the author's pre-commit derivations S7–S10 existed before preregistration and are disclosed there; they are not preregistered predictions. §5 records which of them are confirmed, corrected or false. The mathematics is standard (Holevo's covariant-measurement theory; Schur orthogonality; the reference-frame lesson of Bartlett–Rudolph–Spekkens, Rev. Mod. Phys. 79, 555 (2007)); no mathematical priority is claimed. Covariance and the outcome register are declared class hypotheses, NOT claimed native laws.

## 1. Question and setting
`covariant_refinement_boundary` showed that U(A_k)-covariant center-retaining refinements B ⊆ A cannot grow the center; its review (R2) left carrier-enlarging refinements eligible. Here the refinement adjoins a classical outcome register through a covariant instrument. Question: is an invariant datum (no orientation) enough to force a retained probabilistic contrast for a blind pair, and where must that datum come from?

Setting. Finite-dimensional H; A = A_k ≅ ⊕_{i=1}^r M_{n_i}, multiplicities absorbed into the A-reduced state ρ^A = ⊕_i ρ_i (Tr(aρ) = Σ_i tr(a_iρ_i) for a ∈ A); central atoms z_i; G = U(A) = ∏_i U(n_i), Haar probability dg. ⟨X,Y⟩ = Σ_i tr(X_iY_i). Source pair ρ_0, ρ_1, Δ = ρ_1 − ρ_0 with blocks Δ_i. **Blind at stage k** means Tr(z_iΔ) = 0 for all i, i.e. every Δ_i is traceless (for n_i = 1 this forces Δ_i = 0). D := ½‖Δ^A‖₁ = ½Σ_i‖Δ_i‖₁ is the Helstrom bound for any reader in A.

Class 𝓘_G (declared). A standard Borel G-space Ω with jointly measurable action and a POVM E on Ω with effects in A, covariant: E(gB) = gE(B)g*. (Effects in A is no loss: after the stage-k reduction E_A, an effect X acts as E_A(X) ∈ A, and E_A(gXg*) = gE_A(X)g* for g ∈ U(A).) The register is the classical algebra L^∞(Ω) adjoined to A; its readout law is p_b(B) = Tr(E(B)ρ_b), and the contrast is δ_TV(E;Δ) = sup_B |Tr(E(B)Δ)|. Instruments are taken with operations I_B whose Heisenberg duals map A → A with I_B*(1) = E(B) and I_{gB}*(gXg*) = gI_B*(X)g*. Regular case: Ω = G with left translation. Seed functional, for P ∈ A⁺:
  T(P;Δ) := ½ ∫_G |⟨gPg*, Δ⟩| dg.

## 2. Results

**Lemma 1 (no nontrivial action on a finite set).** Every homomorphism (no continuity assumed) from G = ∏U(n_i) to a finite group is trivial.
Proof. G is compact connected, so exp is surjective: g = exp X = (exp(X/N))^N for every N. If φ: G → F with |F| = N, then φ(g) = φ(exp(X/N))^N = 1 because every element's order divides N. ∎

**Theorem 1 (finite-dimensional covariant enlargements are blind).** Let C be a finite-dimensional *-algebra, α: G → Aut(C) any action, and T*: C → A a unital positive map with T*(α_g(c)) = gT*(c)g*. Read C through its center (the P2 reading). Then for every atom q of Z(C), T*(q) ∈ Z(A); hence every pair blind at stage k gives identical readout laws. In particular every covariant instrument with a finite (or countable, continuously acted) outcome register is central-valued and blind.
Proof. Automorphisms preserve Z(C) and permute its finitely many atoms; by Lemma 1 that permutation action is trivial, so α_g(q) = q. Then T*(q) = gT*(q)g* for all g ∈ U(A), so T*(q) ∈ A ∩ U(A)' = Z(A) (unitaries span A). Blindness gives Tr(T*(q)Δ) = 0. For a register Ω: a finite Ω is Lemma 1 with C = A ⊗ ℓ^∞(Ω); for countable Ω with continuous action, each orbit is G/Stab with Stab closed of countable index, hence open (Baire), hence = G (connected). ∎
The previous Theorem 1 therefore extends to carrier enlargements of finite dimension: any contrast must come from an infinite-dimensional (continuous) register.

**Lemma 2 (regular form; Holevo).** Every covariant POVM on Ω = G is E(dg) = gP0g* dg with P0 ∈ A⁺ and tr P0_i = n_i for every block.
Proof. tr E(·) is left-invariant (tr gXg* = tr X), finite and positive, hence N·Haar, N = Σn_i. Each matrix-element measure is dominated by tr E, so E(dg) = F(g)dg with F ≥ 0 a.e. Covariance gives, for each h, F(hg) = hF(g)h* for a.e. g; by Fubini there is k_0 with F(hk_0) = hF(k_0)h* for a.e. h, so F(g) = gP0g* a.e. with P0 = k_0*F(k_0)k_0. Normalization: ∫gP0g*dg = ⊕_i (tr P0_i/n_i) I_i = I. ∎
Relabelling invariance: seed uP0u* gives E(d(gu)), the same instrument up to the equivariant right translation g ↦ gu, and T(uPu*;Δ) = T(P;Δ). So the regular family is determined by the per-block spectrum of P0 (S1 confirmed).

**Lemma 3 (reduction to seeds).** For any E ∈ 𝓘_{U(A)}, let ν = tr E(·)/N and F = dE/dν (F ≥ 0, tr F = N ν-a.e., ∫F dν = I). Then ν is G-invariant, F(gω) = gF(ω)g* for ν-a.e. ω (each g), and
  δ_TV(E;Δ) = ∫_Ω T(F(ω);Δ) ν(dω).
Proof. Invariance: ν(gB) = tr(gE(B)g*)/N. Covariance a.e. follows from ∫_{gB}F dν = ∫_B F(gω)dν = ∫_B gF g* dν for all B. The density of B ↦ Tr(E(B)Δ) w.r.t. ν is ⟨F,Δ⟩, so δ_TV = ½∫|⟨F(ω),Δ⟩|ν(dω) = ½∫|⟨F(gω),Δ⟩|ν(dω) = ½∫|⟨gF(ω)g*,Δ⟩|ν(dω) for each g; average over g (Fubini; the integrand is continuous in g, measurable in ω). ∎

**Lemma 4 (zero set of T).** T(P;Δ) = 0 iff for every block i, P_i ∈ ℂI_i or Δ_i = 0.
Proof. f(g) = Σ_i f_i(g_i), f_i(g_i) = tr(P_i g_i*Δ_ig_i), is continuous and Haar has full support, so T = 0 iff f ≡ 0. Varying one g_i shows each f_i is constant, equal to its Haar mean tr(P_i)(trΔ_i)/n_i = 0. f_i ≡ 0 iff the traceless part P_i° is HS-orthogonal to span_ℂ{g*Δ_ig}, a nonzero Ad-invariant subspace of sl_{n_i}(ℂ) if Δ_i ≠ 0, hence all of it (irreducibility); then P_i° ⊥ P_i°, so P_i° = 0. ∎

**Theorem 2 (exact criterion).** For E ∈ 𝓘_{U(A)} and a blind pair: δ_TV(E;Δ) > 0 iff some block i with Δ_i ≠ 0 has non-scalar block effects (z_iE(B) ∉ ℂz_i for some B). Regular case: iff P0_i is non-scalar on some block with Δ_i ≠ 0. Hence E distinguishes every blind pair visible on A iff it is non-central on every block of size ≥ 2; a scalar (tracial) seed is inert. δ_TV(E; gΔg*) = δ_TV(E;Δ): the contrast depends only on invariant data (seed spectra, spectra of the Δ_i).
Proof. Lemmas 3–4: δ_TV > 0 iff ν{ω : ∃i, Δ_i ≠ 0, F_i(ω) ∉ ℂI_i} > 0, and F_i° = 0 ν-a.e. iff ∫_B F_i° dν = 0 for all B iff z_iE(B) is scalar for all B. Invariance under Δ ↦ gΔg* from the Haar average. ∎

**Proposition 1 (invariant events, unretained and erased registers are blind).** (a) For every G-invariant event B, E(B) ∈ Z(A); invariant events never distinguish a blind pair, so every distinguishing event is a non-invariant region of the register. (b) The nonselective channel Φ* = I_Ω* is covariant, so Φ*(z) ∈ A ∩ U(A)' = Z(A) for z ∈ Z(A): with the register discarded (or reset), old central readers are blind; Z(A) is unchanged, and the previous Theorem 1 then governs any later covariant refinement. (c) Any covariant coarse-graining of the register to a finite set is central (Theorem 1).
Proof. (a) E(B) = E(gB) = gE(B)g*. (b) Φ*(gXg*) = gΦ*(X)g* since gΩ = Ω; apply to central z. (c) As Theorem 1. ∎
This reconciles `covariant_refinement_boundary` Proposition 2 and K9: the retained label there is exactly a covariant register (see K3).

**Theorem 3 (constants).**
(a) Qubit factor A = M_2. Write a seed P = αI + c·σ and Δ = ½δ·σ (blindness), so D = |δ|/2. Then ⟨gPg*,Δ⟩ = (R_gc)·δ with R_g ∈ SO(3) Haar, and T(P;Δ) = ½|c||δ|E|cos θ| = |c||δ|/4 = (|c|/2)D. Regular seeds have α = 1, |c| ≤ 1, so T ≤ D/2 with equality iff P0 = 2|ψ⟩⟨ψ| (rank one).
(b) Every U(A)-covariant register on any measurable Ω, for A = ⊕ M_{n_i} with all n_i ≤ 2, has δ_TV ≤ D/2. Proof: in Lemma 3 write F_i = α_i I + c_i·σ with α_i ≥ |c_i| and ∫α_i dν = 1 (from ∫F dν = I); by the triangle inequality and (a), δ_TV ≤ Σ_i ∫|c_i||δ_i|/4 dν ≤ Σ_i|δ_i|/4 = D/2. ∎ Covariance costs exactly a factor ½ against Helstrom in the qubit.
(c) Factor M_n, rank-one seed P0 = n|ψ⟩⟨ψ|: T = (n/2)E_φ|⟨φ|Δ|φ⟩| (φ Haar unit vector). From E|φ⟩⟨φ|^{⊗2} = (I+F)/(n(n+1)): E⟨φ|Δ|φ⟩² = TrΔ²/(n(n+1)) for traceless Δ. With |⟨φ|Δ|φ⟩| ≤ ‖Δ‖_∞ (so E|X| ≥ EX²/‖Δ‖_∞) and Jensen:
  ‖Δ‖₂²/(2(n+1)‖Δ‖_∞) ≤ T ≤ min{D, ½√(n/(n+1))‖Δ‖₂}.
Since ‖Δ‖_∞ ≤ D (tr Δ₊ = tr Δ₋ = D) and ‖Δ‖₂² ≥ 4D²/n, T ≥ 2D/(n(n+1)) > 0: a positive fraction of D depending only on n.
(d) Exact values (rank-one seed, any n ≥ 2). Haar |φ_j|² is Dirichlet(1,…,1). Orthogonal pure pair Δ = |1⟩⟨1| − |0⟩⟨0| (D = 1): with s = |φ_0|²+|φ_1|² ~ Beta(2,n−2) independent of |φ_1|²/s ~ U[0,1], E|X| = E[s]·E|2t−1| = (2/n)(½) = 1/n, so **T = ½ = D/2 for every n**. Pure versus maximally mixed, Δ = |0⟩⟨0| − I/n (D = 1 − 1/n): |φ_0|² ~ Beta(1,n−1) with mean 1/n, E|X| = 2∫_{1/n}^1 (x − 1/n)(n−1)(1−x)^{n−2}dx = 2(1−1/n)^n/n, so **T = (1−1/n)^n**, T/D = (1−1/n)^{n−1} (= ½ at n = 2, 4/9 at n = 3, → 1/e).
(e) General seed (factor): with P° the traceless part, Schur's lemma for the absolutely irreducible real adjoint representation on traceless Hermitian matrices gives E_g⟨gP°g*,Δ⟩² = ‖P°‖₂²‖Δ‖₂²/(n²−1), and |⟨gP°g*,Δ⟩| ≤ ‖P°‖₂‖Δ‖₂, so
  T(P;Δ) ≥ ‖P°‖₂‖Δ‖₂/(2(n²−1)) ≥ ‖P°‖₂ D/(√n(n²−1)).
There is no bound uniform over the whole class: P = I + εX gives T = O(ε) (as for the partial-swap θ → 0). A uniform fraction holds for any fixed non-scalar seed spectrum.
(f) Strict cost for orthogonal pure pairs (n ≥ 2): every covariant register has δ_TV < D = 1. Proof: if T(P;Δ) = 1, the continuous densities ⟨0|gPg*|0⟩, ⟨1|gPg*|1⟩ have disjoint supports, so ⟨u|P|u⟩⟨w|P|w⟩ = 0 for every orthonormal pair; P ≠ 0 forces P = n|u⟩⟨u| and then u' = (u+w)/√2, w' = (u−w)/√2 give (n/2)² ≠ 0, contradiction. T is continuous on the compact seed set {P ≥ 0, tr P = n}, so its maximum M < 1, and Lemma 3 gives δ_TV ≤ M. ∎ The exact supremum for n ≥ 3 is not determined here (rank-one gives ½; the rank-two seed (3/2)Π₂ in M_3 gives ¼).

**Proposition 2 (chains).** A finite sequence of covariant instruments with retained registers (adaptive choices allowed if equivariant) has a joint POVM on Ω_1 × … × Ω_m, covariant under the diagonal action. Hence (i) the joint contrast is non-decreasing along the chain (a marginal's TV never exceeds the joint TV) and is kept as long as the registers are kept; (ii) by Lemma 3 it never exceeds max_{P ≥ 0, tr P = n} T(P;Δ) in a factor — in the qubit (and ⊕M_{≤2}) every covariant chain stays ≤ D/2; (iii) for rank-one Lüders seeds (K_g = √n g|ψ⟩⟨ψ|g*) the post-state |gψ⟩⟨gψ| is source-independent, so later registers add nothing. Erasing a register returns to Proposition 1(b). ∎

## 3. Controls (exact hand calculations; nothing executed)
- K1 Scalar seed (inert). P0 = I: ⟨gIg*,Δ⟩ = trΔ = 0, δ_TV = 0 (Lemma 4).
- K2 Unretained register (blind). Proposition 1(b): Φ*(z) = z ∫gP0g*dg = z for Lüders Kraus operators in A; in general Φ*(z) ∈ Z(A).
- K3 Fixed basis (rejected for class; calibrates the cost). A = M_2, E(j) = |j⟩⟨j|, pair |0⟩/|1⟩: δ_TV = 1 = D; Ad(Hadamard) maps E to a different POVM, so it is not covariant: supplied orientation. Haar-randomizing the basis and retaining the frame gives the covariant register on U(2) × {0,1} with seeds |j⟩⟨j| (Σ tr = 2): δ_TV = ∫|⟨φ|Δ|φ⟩|dφ = |δ|/4 = ½ = D/2. Discarding the frame gives E(j) = I/2: blind. This is `covariant_refinement_boundary` K9 resolved: the "retained label" is the covariant register, and retaining it buys exactly half of Helstrom.
- K4 Source-dependent seed (excluded, P8). P0 = 2ρ_b with ρ_b = |b⟩⟨b|: p_b(dg) = 2|g_bb|²dg, and |g_00| = |g_11| for every g ∈ U(2), so δ_TV = 0: the instruments differ by b, the comparison is not a property of one instrument, and here it even erases the common-seed value ½. Both seeds have the same spectrum; they differ by the right translation by X, i.e. by a source-dependent relabelling (K9).
- K5 Register erased after write (blind). Reset/discard = Proposition 1(b); covariant finite summary = Proposition 1(c).
- K6 Qubit exact check. P0 = 2|ψ⟩⟨ψ| = I + m·σ: ⟨gP0g*,Δ⟩ = (R_gm)·δ, cos θ ~ U[−1,1], δ_TV = |δ|/4 = D/2 (Theorem 3(a)); orthogonal pure pair: ½.
- K7 Block algebra M_2 ⊕ M_2 (basis e_1,e_2 | e_3,e_4; regular seeds with tr P_i = 2). (i) Cross-block only: ρ_{0,1} = |φ_∓⟩⟨φ_∓|, φ_± = (e_1 ± e_3)/√2; blind (block weights ½,½), Δ^A = 0, so δ_TV = 0 for every A-instrument, covariant or not (pruned at stage k; `center_access_growth` (d)). (ii) Central component: e_1 versus e_3 has Tr(z_1Δ) = −1 — not blind, outside the hypothesis. (iii) One block: ρ_0 = ½(e_1e_1* + e_3e_3*), ρ_1 = ½(e_2e_2* + e_3e_3*), Δ_1 = −σ_z/2, Δ_2 = 0, D = ½: seed 2|ψ⟩⟨ψ| ⊕ I gives δ_TV = ¼ = D/2; seed I ⊕ 2|ψ⟩⟨ψ| gives 0. (iv) Both blocks: ρ_0 = ½(e_1e_1* + e_3e_3*), ρ_1 = ½(e_2e_2* + e_4e_4*), |δ_1| = |δ_2| = 1, D = 1; rank-one seeds on both blocks give δ_TV = ½E|X+Y| with X, Y iid U[−1,1], E|X+Y| = 2/3, so **δ_TV = 1/3 = D/3** (< D/2, consistent with Theorem 3(b)).
- K8 Reduced covariance SO(3) on M_3 (non-scalar is NOT sufficient). Regular SO(3)-covariant POVMs: E(dR) = RP0R^T dR, tr P0 = 3 (ℂ³ irreducible). Traceless Hermitian matrices split into real-symmetric (spin 2, dim 5) ⊕ i·real-antisymmetric (spin 1, dim 3), inequivalent and absolutely irreducible; Schur orthogonality gives ‖⟨RP°R^T,Δ⟩‖²_{L²} = ‖P°_1‖²‖Δ_1‖²/3 + ‖P°_2‖²‖Δ_2‖²/5, so δ_TV = 0 iff each isotypic product vanishes. Pair v_± = (e_1 ± ie_2)/√2 (orthogonal; D = 1): Δ = i(E_21 − E_12) = L_z, pure spin-1. Real seed 3|x⟩⟨x|: ⟨y|L_z|y⟩ = 0 for real y, so **δ_TV = 0** despite a non-scalar seed. Helicity seed 3|v_+⟩⟨v_+|: R^T L_zR = n·L with n Haar on S², ⟨v_+|n·L|v_+⟩ = n_z, **δ_TV = (3/2)E|cos θ| = 3/4**, above the U(3) rank-one value ½. Smaller symmetry admits more instruments; the real structure of SO(3) is itself a supplied orientation-type datum (`covariant_refinement_boundary` K6).
- K9 Duplicated / substituted record (false provenance). Duplication g ↦ (g,g) is injective, δ_TV unchanged: copying a record adds nothing. Substitution: identical sources ρ_0 = ρ_1 = |0⟩⟨0|, seed 2|0⟩⟨0|, register relabelled for b = 1 by g ↦ gX: densities 2t and 2(1−t) with t = |g_00|² ~ U[0,1], spurious **δ_TV = ∫|2t−1|dt = ½** with Δ = 0. Rejected: the labelling must be common (P8). Missing record: K5.
- K10 Pruning-rank seed. P0 = (n/m)Π_m (Lüders: Kraus √(n/m) gΠ_mg*, outcome = which m-dimensional subspace survives). Non-scalar iff 0 < m < n, so in a factor every strict covariant selective pruning distinguishes every visible blind pair (Theorem 2; blockwise, 0 < m_i < n_i is needed on a visible block), with ‖P°‖₂ = √(n(n−m)/m) in Theorem 3(e); m = n (no pruning) is K1. Provenance: in `pruning_cover_record` the active support S_v ⊆ palette is combinatorial and is itself a supplied evaluator input; no inspected source supplies a correspondence palette ↔ carrier dimension, so identifying |S_v'| with m is SUPPLIED. Worse for the act: the inherited deletion removes a NAMED element and records a finite label. Mapped to a carrier it is a fixed-basis projection (K3, orientation supplied); read as a covariant register it is finite and therefore blind (Theorem 1).

## 4. Premise provenance
| # | Premise | Status |
|---|---|---|
| P0 | finite-dimensional H | SUPPLIED (inherited interface) |
| Q1 | U(A)-covariance of the instrument (class definition) | DECLARED hypothesis, not claimed native |
| R0 | an event performs a covariant instrument (the act) | SUPPLIED; not derived in the packet |
| R1 | the register is continuous (infinite-dimensional L^∞(Ω)) | SUPPLIED; forced by Theorem 1, and outside the finite-dimensional interface P0 |
| R2 | non-central seed (invariant datum, e.g. strict rank 0 < m < n) | SUPPLIED; candidate combinatorial source only conditional (K10) |
| R3 | retention of the register (no erasure/relabelling) | SUPPLIED |
| P2' | access: reader = center of the enlarged algebra including the register, read by its spectral measure (P2 extended to diffuse centers) | SUPPLIED |
| P3 | source pair ρ_0, ρ_1 | SUPPLIED |
| P8 | common instrument and common labelling for both sources | required hypothesis (K4, K9) |
| D1 | Lemmas 1–4, Theorems 1–3, Propositions 1–2 | DERIVED (standard mathematics) |

## 5. Sketch items: confirmed, corrected, false
- S1 CONFIRMED (Lemma 2), with per-block normalization tr P0_i = n_i; "determined by the spectrum" holds up to equivariant right-translation relabelling.
- S2 CONFIRMED FOR CONTINUOUS REGISTERS (Theorem 2, including the iff), but **FALSE as a statement about carrier enlargement in general (RED, preserved): every finite-dimensional covariant enlargement read through its center is blind (Theorem 1).** The adjoined L^∞(outcomes) must be infinite-dimensional, which leaves the frozen finite-H interface.
- S3 CONFIRMED in value (δ_TV = |δ|/4 = D/2); typographical correction: Tr(2|gψ⟩⟨gψ|Δ) = m·δ (m the Bloch unit vector of gψ), not n·δ. Strengthened: D/2 is the maximum over all covariant registers and chains in ⊕M_{≤2} (Theorem 3(b), Proposition 2).
- S4 CONFIRMED (identity and bound), plus T ≥ 2D/(n(n+1)) and exact values. Corrected scope: the uniform fraction holds per fixed non-scalar seed spectrum, not uniformly over the class (Theorem 3(e)).
- S5 PARTLY FALSE (RED, preserved). The unretained statement is CONFIRMED and holds for every covariant instrument (Proposition 1(b)). "Invariant in ensemble" is wrong for the outcome law: if p_0 and p_1 were both left-invariant they would both be Haar and δ_TV = 0. What is invariant is the instrument (equivariance) and the contrast functional δ_TV (Theorem 2). "The realized record is the orientation datum" is CONFIRMED in sharpened form: contrast requires a continuous frame-valued record (Theorem 1), and only non-invariant regions of it distinguish (Proposition 1(a)). The link to "time as pruning" (which subspace survives, K10) is interpretive, not derived.
- S6 CONFIRMED mathematically for 0 < m < n; the rank is SUPPLIED; the inherited labelled deletion is not the covariant act, and its finite record is blind if read covariantly (K10).
- S7–S10 CONFIRMED (Theorem 1; Lemma 3 with Theorem 3(b); Theorem 3(d) and K7(iv); K8).

## 6. What this establishes and what it does not
Established (general proofs, declared class): for U(A)-covariant instruments with a retained classical register, a blind pair acquires a register-law contrast iff the instrument is non-central on a block where the pair is visible. In the regular case that is iff the seed is non-scalar there, an invariant spectral datum with no supplied basis. The contrast is an invariant functional, ≤ D/2 in qubit blocks (attained by rank-one seeds) and ≥ 2D/(n(n+1)) for rank-one seeds in M_n. Unretained, erased, invariantly coarse-grained and finite registers are blind. Chains never beat the best single seed. The orientation is not removed; it is relocated from an input of the law into the retained output. The register must record a continuous frame (an infinite-dimensional classical record), and every distinguishing test on it is a non-invariant region.

Exact examples (hand calculations, not general theorems): T = ½ (orthogonal pure, rank-one, all n); (1−1/n)^n (pure vs maximally mixed); D/3 (K7(iv)); 3/4 under SO(3) (K8).

Unresolved: the supremum of δ_TV/D over covariant registers for n ≥ 3; general non-standard-Borel outcome spaces; multi-copy (collective) instruments; infinite-dimensional carriers; whether any inherited event performs a covariant instrument; any native continuous record; justified access P2'. No archive-wide absence claim.

Relation to O3: this is standard covariant-measurement mathematics in the local framing, and no basis is smuggled (the frame is an output). The finite-register no-go and the K10 provenance finding are what this stage adds to the record.

## 7. Disposition
**COVARIANT_OUTCOME_REGISTER_CONTRAST_IFF_NONCENTRAL_INSTRUMENT; FINITE_COVARIANT_REGISTERS_BLIND_CONTINUOUS_ORIENTATION_RECORD_REQUIRED; INSTRUMENT_REGISTER_AND_ACCESS_SUPPLIED; NATIVE_MILESTONE_NOT_ACHIEVED** (frozen outcome O1, qualified by O5; O2 holds for finite registers; O4 not reached).

The open obligation moves again. An invariant seed datum is cheap: any strict selective pruning rank 0 < m < n suffices. The unearned parts are the covariant act itself, a retained continuous (frame-valued) record, and access to it. A finite inherited record (palette label, incidence, laminar atom) can serve only through a supplied correspondence to carrier directions (orientation) or else is blind. Do not insert a basis, a continuous register or a covariant instrument to discharge this.

Analytical only: no numerics, simulation, enumeration, module import or replay; no inherited stack run. No CLOSED/CERTIFIED status, physical law, force, energy, geometry, dark-matter primitive or fundamental clock is claimed. Time remains pruning / ordered recoverability update. Path A active; broad C3/C4–C6 OPEN.

Missing AGENTS requirements (explicit): no workflow SHA; no pinned full-stack GitHub run; no execution artifacts or reproduced bytes; no independent review yet (separate agent); no publication audit; no PR or merge audit.

Standard references: A. S. Holevo, *Probabilistic and Statistical Aspects of Quantum Theory* (covariant measurements); S. D. Bartlett, T. Rudolph, R. W. Spekkens, Rev. Mod. Phys. 79, 555 (2007).

## 8. Sources (bound in `source_packet.json` / `source_identities.json` at parent `b2a78583`)
1. `ResearchHistory/UQCF-GEM/AGENTS.md`
2. `physical-bridge/NATIVE_EVENT_MILESTONE.md`
3. `physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_CONTINUATION.md` (parent bytes)
4. `physical-bridge/retained_reader_write/RESULT.md`
5. `physical-bridge/collective_covariance_candidate/RESULT.md`
6. `physical-bridge/center_access_growth/RESULT.md`
7. `physical-bridge/pruning_cover_record/RESULT.md`
8. `physical-bridge/covariant_refinement_boundary/PREREGISTRATION.md`
9. `physical-bridge/covariant_refinement_boundary/RESULT.md`
10. `physical-bridge/covariant_refinement_boundary/INDEX_APPEND.md`
11. `physical-bridge/covariant_refinement_boundary/ANALYTICAL_REVIEW_RAW.md`
12. `physical-bridge/covariant_refinement_boundary/PUBLICATION_RECEIPT.md`
13. `physical-bridge/covariant_refinement_boundary/source_packet.json`
14. `physical-bridge/covariant_refinement_boundary/source_identities.json`
