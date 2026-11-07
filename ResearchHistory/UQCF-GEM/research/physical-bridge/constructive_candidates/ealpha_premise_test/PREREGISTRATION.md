# PREREGISTRATION (copy of thread entry T-269, agent-thread 742ee354; #111 notice 6586550350)

Committed before any execution of this test.

## T-269 (Grok) — PREREGISTRATION of one bounded, falsifiable test of a deliberately adopted NEW ASSUMPTION (sharp E-α). Nothing has been executed for this test at the time of this commit. Native bridge NOT_DERIVED; the premise can never be upgraded by this test.

Parents: agent-thread 0b3a479d (T-268a), research 750554de (verified unchanged at 12:25 PM MST). No new #111 entries after T-268a. Authorization: Aaron, 12:23 PM MST Nov 2, 2026, via Science Discovery X Bot (verbatim: "Yes, go ahead with the E-α test as proposed."), confirmed by reading that session. It overrides the T-264 no-adopt rule for this one test only and allows exactly one Gemini review. No merge, no claimStatus/Retained Atlas change.

### 0. Status tags (C9, T-263)

INHERITED: native tree, P1 contraction P(z_o,z_p,z_u,z_v)=(z_o,z_p+z_u,z_v), zero extension I, owner/address data. ACCEPTED-CONDITIONAL / SUPPLIED benchmark: H_S, encodings Π_X, reset channel C(ρ)=QρQ+ρ_uu|p⟩⟨p|, K=E⊗R, blank |0_E0_R⟩, receiver algebra, Stiefel realization class (frames (e_0,e_u)). SUPPLIED for this test only: the two-event carriers in §3. NEW ASSUMPTION: the premise in §1.

### 1. The premise (NEW ASSUMPTION, never DERIVED)

**E-α (sharp).** Under the P1 event the record of the erased branch is written isometrically into the designated receiver R and E is left untouched: e_0 = α⊗β, e_u = e^{iφ} α⊗β^⊥ (same E vector α, orthogonal R vectors). In the R basis with β=|0⟩, β^⊥=|1⟩ this is J_R W = W π_u (J_R = I_S⊗I_E⊗|1⟩⟨1|_R) together with "E untouched" (the E factor of W|j⟩ is the same fixed vector for every j). By Lemma Σ′ (T-262) the premise set equals H·W_R = {D_E = 0, D_R = 1/5}, H = U(E)⊗U(R).
Disclosed pre-run analytic note: J_R W = W π_u alone is not enough; the frame e_0=|00⟩, e_u=|11⟩ satisfies it but also writes E (D_E = 1/5). The E-untouched clause is load-bearing, so this frame is added as control W_ER.

**Why this one.** E-β (dual-marginal distinguishability) excludes W_R itself, so it is a different target. E-γ has no source: the P1 roles are fixed under E↔R swap. Weaker E-α targets (B_E∖B_R, or any R-contrast) give no lower bound on D_R (Σ′(ii)–(iii)), so they make no sharp predictions.

### 2. Admission controls (expected verdicts stated before running)

All share the P1 channel C. W_R (e_0=|00⟩, e_u=|01⟩): ADMIT. W_R^g = (a⊗b)·W_R for one fixed exact local unitary (orbit point): ADMIT. W_E (e_u=|10⟩): REJECT. W_Bell (e_0,e_u=(|00⟩±|11⟩)/√2): REJECT. W_W (e_0=|00⟩, e_u=(|01⟩+|10⟩)/√2): REJECT. W_ER (|00⟩,|11⟩): REJECT. W_θ (T-262, θ=π/8): REJECT. Admission is tested two ways that must agree: (i) the product/same-E-factor/orthogonal-R form of §1; (ii) (D_E, D_R) = (0, 1/5) on the benchmark pair z± = (1,1,2,1)/5, (1,1,1,2)/5.

### 3. Prediction P-a, compositional consistency (main test)

**Carriers (SUPPLIED).** Two P1 contractions P_1 (u_1→p_1) and P_2 (u_2→p_2) on disjoint addresses. Checked exactly: P_1P_2 = P_2P_1 natively, and C_1C_2 = C_2C_1 on the carrier.
- Carrier A, PRIMARY: one-hot address carrier H_S = span{o,p_1,u_1,p_2,u_2,v}, supplied tree o→p_1→{u_1,v}, o→p_2→u_2. This is the direct extension of the benchmark's grade-as-mixture encoding, with one grade vector on one tree.
- Carrier B, SECONDARY diagnostic: two benchmark copies S_1⊗S_2 (each span{o,p,u,v}), event k acting on S_k.

**How E-α extends to an already-written receiver.** Event k acts by an isometry V_k on the range of the other event's output. It has to (1) implement C_k on S for every operator supported on that domain, including operators correlated with R (Tr_R V_k ω V_k† = C_k(Tr_R ω)); (2) leave E untouched, with no extra output factor allowed (any added factor counts as E); and (3) write event k's erased-branch record into R isometrically. Three candidate extensions:
- X1 slot tensor: R = R_1⊗R_2, and event k does sharp E-α into a fresh slot R_k.
- X2 single shared R qubit: both events write into one qubit R (any write rule: OR, XOR or other). Well-posedness is decided rule-independently. If conditions (1)–(3) hold for both events, the composite is a Stinespring dilation of C_1C_2 whose environment is the qubit R with E pure, so it requires Choi rank(C_1C_2) ≤ 2. If that fails, X2 is FAIL (ill-posed).
- X3 isometric register-append: R = span of ordered event-label sequences (∅, [1], [2], [1,2], [2,1]); event k sends |u_k⟩|σ⟩ ↦ |p_k⟩|σ·k⟩ and acts as the identity elsewhere.

**PASS/FAIL criteria for each extension and carrier (frozen).**
(W) Well-posed: some V_k satisfying (1)–(3) exists for both events, checked exactly on all matrix units of the domain. If none exists: FAIL (ill-posed).
(O) Order-independent up to a fixed relabeling of R: the S⊗E channels of V_{12}=V_1V_2 and V_{21}=V_2V_1 (R traced out) are equal on every matrix unit. By Stinespring uniqueness this is equivalent to V_{12} = (I⊗U_R)V_{21} for a partial isometry U_R on R. U_R is also exhibited explicitly and checked as an exact operator identity. The composite must implement C_1C_2.
(B) Stays inside the E-blind orbit: E is exactly |0⟩ on every output, and for each event's benchmark pair (other event's coordinates fixed and active) D_E = 0 and D_R = 1/5. Carrier A pairs: event 1 (1,1,4,1,1,2)/10 vs (1,1,2,1,1,4)/10, event 2 (1,1,1,1,4,2)/10 vs (1,1,1,1,2,4)/10. Carrier B pairs: z±⊗z+ for event 1 and z+⊗z± for event 2.
An extension PASSES iff W, O and B all hold. It FAILS on any O or B violation and is FAIL (ill-posed) if W fails.
**Trivial commutation (declared in advance).** A pass is non-discriminating if order-independence follows by construction from (a) the two writes acting on disjoint tensor factors of R (X1), or (b) no source branch ever receives two writes (the two erased branches are mutually orthogonal, so no write onto an already-written receiver is exercised).
**Aggregate P-a verdict for each carrier:** FAIL if no extension passes. PASS if some extension passes non-trivially. "PASS, non-discriminating" if every passing extension is trivial. The per-extension verdicts are always reported, including FAIL (ill-posed). The headline is carrier A, and carrier B is reported alongside it as a secondary verdict, not merged into the headline. These criteria will not be changed after the results are seen.
**Rejecting controls for the P-a checker:** an isometric overwrite register (the qutrit R gets the latest label, and the old content goes to E): O must fail, and it violates E-untouched. X3 with U_R forced to the identity: the explicit-U check must fail in carrier B. The X2 OR-rule composite: the channel equality with C_1C_2 must fail on a u_1–u_2 coherent input in carrier A. The mirror control (E-writing W_E-type events under each extension) gets the same W/O verdicts by E↔R symmetry, so P-a cannot discriminate destination. That limitation is declared now.
**Expected (analytic, pre-run, disclosed):** X1 PASS non-discriminating in both carriers. X2 FAIL (ill-posed) in both carriers (Choi rank 3 in A and 4 in B, both > 2). X3 PASS non-discriminating in A (by (b)) and PASS in B (non-trivial, U_R = swap of [1,2]↔[2,1]). So headline A = "PASS, non-discriminating", and B = PASS.

### 4. Prediction P-b, entropy ledger

For all inputs ρ: S(ρ_R) ≥ S(ρ_S) − S(C(ρ_S)), with zero exported entropy on E (S(ρ_E)=0). On diagonal inputs this is h(z_u) ≥ (z_p+z_u)·h(z_u/(z_p+z_u)).
**Forcing check (preregistered).** (F1) For every Stinespring realization, does S(ρ_K) ≥ S(ρ_S) − S(C ρ_S) follow from isometric invariance plus subadditivity? (F2) For premise realizations, is ω_K = |α⟩⟨α|_E ⊗ ω_R exactly, so that S(ρ_R) = S(ρ_K) and S(ρ_E) = 0? If F1 and F2 both hold, P-b follows from the premise plus Stinespring and the channel. It is then DOWNGRADED to a consistency check and not counted as a prediction. Expected: downgraded.
Checks: exact diagonal identities (sympy), plus a fixed-seed high-precision random check (seed 269, mpmath 50 digits, 200 random density matrices of rank 1–4) over all controls. Expected control results: W_R satisfies (on diagonal inputs, equality iff z_o+z_v=0 or z_pz_u=0); W_E fails the R inequality whenever ΔS>0; W_Bell satisfies it on diagonal inputs (S(R)=1 bit) and fails S(E)=0; W_W fails both (e.g. z=(0,½,½,0): h(¼) < 1); W_θ fails S(E)=0 while D_E=0 (blindness is not zero entropy).

### 5. P-c (known, not counted)

Owner unrecoverable from R: R(π_p) = R(π_v) under W_R (T-268). It is recomputed only as a regression check.

### 6. Procedure and scope

One exact sympy script plus an algorithmically independent numpy checker. Local run on the shared box, with seed, raw stdout and SHA-256 saved under /workspace/uqcf_scratch/t269/, then frozen with RESULT.md under physical-bridge/constructive_candidates/ealpha_premise_test/ on a new branch, with a PR into the research branch (no merge). One Gemini referee review through an Actions workflow (one model call, no retry). Results go in T-270. Disclosed now: this is a bounded thread test, not a numbered retained stage. The AGENTS.md closure chain (GitHub-run producer/verifier, publication job, merge audit) is not claimed. A finite exact check is bounded evidence, and the general statements in §3 (W) and §4 (F1) are proved analytically in RESULT.md. Native bridge NOT_DERIVED. The premise stays NEW ASSUMPTION whatever the outcome.
