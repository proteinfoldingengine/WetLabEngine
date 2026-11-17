# Bounded test of the NEW ASSUMPTION sharp E-α (T-269 preregistration → T-270 result)

Date: 2026-11-02 America/Phoenix (MST). Author: proteinfolding-grokbot (UQCF Science Agent).
Parents: research `750554de424a1e12e2d14c6665920bda31163dfc`, agent-thread `0b3a479d` (T-268a).
Preregistration: thread T-269 at agent-thread `742ee354578083bbcffa34cad5f7f9b3c4be6873` (#111 notice 6586550350), copied byte-for-byte below the header of `PREREGISTRATION.md`, committed on this branch at `21c1439e` **before** any execution.
Authorization: Aaron, 12:23 PM MST, "Yes, go ahead with the E-α test as proposed." (one bounded test, one Gemini review; T-264 no-adopt rule overridden for this test only).

**Status.** The premise is a NEW ASSUMPTION and stays NEW. Nothing here is DERIVED from native sources. Native bridge **NOT_DERIVED**. Class C (bounded benchmark mathematics). This is not a numbered retained stage. See §7 for which AGENTS.md closure items are not claimed.

## 1. Premise and tags

INHERITED: native tree, P1 contraction P, zero extension I, owner/address data. ACCEPTED-CONDITIONAL / SUPPLIED: H_S, Π_X, C(ρ)=QρQ+ρ_uu|p⟩⟨p|, K=E⊗R, blank state, receiver algebra, Stiefel realization class (frames e_0 ⊥ e_u with W|j⟩=|j⟩e_0, W|u⟩=|p⟩e_u). SUPPLIED for this test: the two-event carriers A and B.

**E-α (NEW ASSUMPTION).** e_0 = α⊗β and e_u = e^{iφ}α⊗β^⊥. Equivalently W ∈ H·W_R = {D_E=0, D_R=1/5} (Lemma Σ′, T-262). In the R basis adapted to β, this reads J_R W = Wπ_u plus "E untouched". J_R W = Wπ_u alone is not enough: W_ER (e_u=|11⟩) satisfies it and writes E.

## 2. Admission (exact; `t269_ealpha.py` → `admission`)

| realization | implements C | D_E | D_R | J_RW=Wπ_u | admitted | expected |
|---|---|---|---|---|---|---|
| W_R | yes | 0 | 1/5 | yes | **yes** | yes |
| W_R^g = (a⊗b)W_R, a=[[3/5,−4/5],[4/5,3/5]], b=[[3/5,4i/5],[4i/5,3/5]] | yes | 0 | 1/5 | no (rotated basis) | **yes** | yes |
| W_E | yes | 1/5 | 0 | no | no | no |
| W_Bell | yes | 0 | 0 | no | no | no |
| W_W | yes | 1/10 | 1/10 | no | no | no |
| W_ER | yes | 1/5 | 1/5 | **yes** | no | no |
| W_θ, θ=π/8 | yes | 0 | √2/10 | no | no | no |

The two admission tests (same pure E factor; (D_E,D_R)=(0,1/5)) agree on all seven. The premise admits exactly the W_R orbit among the controls.

## 3. P-a, compositional consistency (main test)

Native and channel commutation hold exactly: P_1P_2=P_2P_1 and C_1C_2=C_2C_1 on both carriers. Choi rank(C_1C_2) is 3 on carrier A (Kraus Q_{12}, |p_1⟩⟨u_1|, |p_2⟩⟨u_2|) and 4 on carrier B.

**Proposition X2 (rule-independent obstruction).** Suppose both events satisfy conditions (1)–(3) of the preregistration with a single receiver qubit R and E untouched. Then V_{12} = V_1V_2: S → S⊗R (⊗ fixed |0_E⟩) satisfies Tr_R V_{12}ρV_{12}^† = C_1C_2(ρ) for all ρ. Event 2's condition (1) holds on correlated operators, so the S-marginal after V_2 is C_2 of the S-marginal of V_1's output, which is C_1(ρ). The operators K_r = (I⊗⟨r|)V_{12}, r ∈ {0,1}, therefore form a Kraus representation of C_1C_2 with two elements, which forces Choi rank ≤ 2. That contradicts rank 3 (A) and rank 4 (B). ∎ The argument uses no write rule, so the explicit OR and XOR rules both fail the composite-channel check, as they must. More generally, E-α puts the whole Stinespring environment of the event history into R, so dim R ≥ Choi rank of the composite channel (n+1 for n disjoint events on carrier A, 2^n on carrier B). The receiver has to be a register whose capacity grows with the number of events. This is the standard minimal-dilation bound applied with E trivial. By E↔R symmetry it applies equally to E-writing realizations, so it is not destination-discriminating.

**X1 (slots).** V_k touches only addresses {p_k,u_k} and only slot R_k, so V_1V_2 = V_2V_1 exactly, with U_R = I. **X3 (append).** V_{12} = (I⊗U_swap)V_{21} with U_swap: [1,2]↔[2,1]. This is an exact operator identity on every basis input, and the only branch where the two orders differ is the doubly written branch (u_1,u_2) of carrier B.

| carrier | ext | W well-posed | O (S⊗E channel equal) | composite = C_1C_2 | B: E blind, D_E=0, D_R=1/5 per event | doubly-written branches | verdict |
|---|---|---|---|---|---|---|---|
| A (primary) | X1 | yes | yes (U_R=I) | yes | yes | 0 | PASS, non-discriminating ((a), (b)) |
| A | X2 | no (Choi 3 > 2) | — | OR/XOR: no | — | 0 | **FAIL (ill-posed)** |
| A | X3 | yes | yes (U_R=I suffices) | yes | yes | 0 | PASS, non-discriminating ((b)) |
| B (secondary) | X1 | yes | yes (U_R=I) | yes | yes | 1 | PASS, non-discriminating ((a)) |
| B | X2 | no (Choi 4 > 2) | — | OR/XOR: no | — | 1 | **FAIL (ill-posed)** |
| B | X3 | yes | yes (U_R=swap; identity fails) | yes | yes | 1 | **PASS** (non-trivial by the frozen definition) |

**Aggregate.** Headline, carrier A: **PASS, non-discriminating**. Secondary, carrier B: **PASS**. In both carriers, X2 (the only extension in which an event writes onto an already-written receiver of fixed dimension) is FAIL (ill-posed).

**Rejecting controls for the checker (all rejected as required).** Overwrite→E (carrier B): O fails and E is touched. X3 on carrier B with U_R forced to I: the explicit identity fails. The OR composite on carrier A fails C_1C_2 (it creates |p_1⟩⟨p_2| coherence from |u_1⟩⟨u_2|). **Mirror (E-writing) controls:** they get the same W/O/composite verdicts as E-α under X1 and X3 on both carriers, with (D_E, D_R) = (1/5, 0). So P-a checks that E-α is internally composable. It cannot tell destinations apart, as declared in advance.

Reading. P-a was a real chance to fail, and one natural reading (a single shared receiver qubit) did fail. The sharp premise is consistent only when each event gets fresh receiver capacity (a slot or a new register cell). In the primary carrier that makes commutation automatic. The one non-trivial pass (B-X3) depends on the preregistered allowance of a fixed relabeling of R, and the record keeps the event order up to that relabeling.

## 4. P-b, entropy ledger

**F1 (any Stinespring realization).** S(WρW^†) = S(ρ), and subadditivity gives S(ρ) ≤ S(C(ρ)) + S(ω_K). Hence S(ω_K) ≥ S(ρ_S) − S(C(ρ_S)) for every realization of C. **F2 (premise).** W|j⟩ = |s_j⟩⊗α⊗β_j, so ω_K = |α⟩⟨α| ⊗ ω_R. This was checked exactly on 20 random rational inputs for W_R and W_R^g. It gives S(ω_R) = S(ω_K) and S(ω_E) = 0. F1 and F2 both hold, so **P-b is DOWNGRADED to a consistency check** and does not count as a prediction. The diagonal grouping identity H(z) − H(z_o,z_p+z_u,z_v) = (z_p+z_u)h(z_u/(z_p+z_u)) is verified symbolically (residual 0).

Numerics: mpmath, 50 digits, seed 269, 200 random inputs of ranks 1–4 plus 3 diagonal specials. The independent numpy checker used 2001 inputs.

| realization | S(R) ≥ ΔS on all inputs | min slack | S(E)=0 | max S(E) bits | F1 min slack |
|---|---|---|---|---|---|
| W_R, W_R^g | yes | 0 (equality at z=(0,½,½,0)) | yes | ≤ 4e−51 | 0 |
| W_E | no (81/203) | −1 | no | 1 | 0 |
| W_Bell | yes | 0 | no | 1 | 0 |
| W_W | no (at z=(0,½,½,0)) | h(¼)−1 = −0.18872 | no | 0.936 | 0 |
| W_ER | yes | 0 | no | 1 | 0 |
| W_θ(π/8) | yes | 0 | no | 0.6009 (constant on diagonals; D_E=0) | 0 |

These match the preregistered expectations for every control. W_θ shows that E-blindness is not the same as zero exported entropy.

## 5. P-c (not counted)

R(π_p) = R(π_v) under W_R holds exactly (regression of T-268).

## 6. Directive categories

- **Native premises:** native tree, P1 contraction, I, owner/address data. Nothing new.
- **New derived consequence:** inside the supplied benchmark only. Under the NEW premise, a single fixed-dimension receiver cannot absorb two events (dim R ≥ Choi rank of the composite channel). Sharp E-α composes only with fresh receiver capacity per event (slot or register cell). P-b is a consequence of the premise plus Stinespring.
- **Still supplied:** the premise itself, the benchmark channel and factorization, the carriers, the receiver algebra, access, and the probability law.
- **Constrains delivery?** No. It constrains the premise's own composability (receiver capacity), not where delivery goes. Mirror controls pass identically.
- **Accessible observable?** None new.
- **Physical vs mathematical:** mathematical only.

## 7. Scope, deviations and disclosures

- Local run on the shared Grok box, not GitHub Actions. Main script `t269_ealpha.py` ran once (start 12:37:21 MST, exit 0, empty stderr). Independent checker `t269_verify_np.py`: run 1 crashed (checker Choi sizing bug), run 2 disagreed on carrier B because its reference channel dropped coherences that C⊗id keeps (checker bug, Choi rank 8 instead of 4), run 3 agreed on every verdict. The failed checker runs and their scripts are preserved under `evidence/local-run-1/failed/`.
- Two edits were made to the main script after it was written but **before** its single run: the mirror controls now check the untouched factor R, and the rational→mpf conversion was fixed. No main-script run preceded them.
- The analytic expectations in T-269 were disclosed before the run, and every outcome matched them. In that sense the test confirms a pre-run analysis.
- AGENTS.md closure items not claimed: a GitHub-run producer/verifier with pinned stack, a publication job with fresh reproduction, a merge audit, and CLOSED/CERTIFIED status. Only the single Gemini review runs on Actions. Finite exact checks are bounded evidence. The general statements are the proofs in §§3–4.
- Native bridge NOT_DERIVED. No claimStatus or Retained Atlas change.
