# Thermal-bath / pure-receiver follow-up (T-271 preregistration → T-272 result)

Date: 2026-11-02 America/Phoenix (MST). Author: proteinfolding-grokbot (UQCF Science Agent).
Preregistration: thread T-271 at agent-thread `d37a3be5ed21309a945d6c1e1be284d483f9b0be` (#111 notice 6587071140). It was copied to `PREREGISTRATION.md` at `5b125e8b` on `grok/thermal-bath-purity-test` (base research `750554de`) before execution.
Authorization: Aaron, 12:49 PM MST, "Yes, go ahead". One bounded test and one Gemini review.

**Status.** Ingredient TB is a NEW ASSUMPTION and stays NEW. Native bridge **NOT_DERIVED**. Class C (bounded benchmark mathematics). No claimStatus or Retained Atlas change.

## 1. Ingredient and tags
- **TB (NEW).** E is a finite thermal bath at T > 0, so its initial state τ_E is full rank. R starts in the supplied pure blank |0⟩. The dynamics is an arbitrary unitary on S⊗E⊗R.
- **INHERITED:** tree, P, I, owner/address data.
- **SUPPLIED:** H_S, C, K=E⊗R, the R blank, the dimensions, and the realization class.

The requested candidate, owner-local attachment, was rejected by vetting before execution (T-271 §1). For every realization of C, π_p and π_v leave identical K states, because C keeps |p⟩⟨v| and so ⟨e_v|e_p⟩=1. The owner coordinate y_p is therefore unrecoverable under every attachment rule. The erased-branch-owner reading is forced by the complementary channel and is tautological when read from the owner-indexed family. Q-a reduces to Stinespring's bound localized by the ingredient's own placement rule.

## 2. Theorem L and Lemma PP (proved in T-271; checked here)
- **Theorem L.** For U = U_SE⊗I_R (R untouched) and ρ* = (π_p+π_u)/2:
  ⟨p|Φ_U(ρ*)|p⟩ ≤ KF_{d_E}(ρ*⊗τ_E),
  by the Ky Fan maximum principle, since π_p⊗I_E has rank d_E. The bound is tight. So an exact R-untouched realization exists iff rank τ_E ≤ d_E/2, and none exists for a full-rank bath.
- **Lemma PP.** (I⊗V_ER)U realizes C whenever U does. So no initial-state ingredient fixes where the record ends up.

## 3. Results (`t271_tb.py`, one local run, exact sympy)
| control | τ_q=diag(2/3,1/3) | τ_½=I/2 | verdict |
|---|---|---|---|
| W_R⊗I_E | realizes C; p-value 1; D_E=0, D_R=1/5 | realizes C; D_E=0, D_R=1/5 | PASS |
| **W_E, fixed-ingredient mirror (R untouched)** | does not realize C; p-value 2/3 = KF | does not; 1/2 = KF | **FAIL** (as predicted) |
| W_E^c (W_E on the E=0 branch; on the E=1 branch, unerased→\|11⟩, erased→\|01⟩) | realizes C; D_E=1/15, D_R=0 | realizes C; D_E=0, D_R=0 | passes by consuming R's purity |
| W_Bell^c | realizes C; D_E=D_R=1/15 | realizes C; D_E=D_R=1/10 | passes (TB does not single out W_R) |
| W_W^c | realizes C; D_E=D_R=1/10 | realizes C; D_E=D_R=1/10 | passes |
| W_R;SWAP | realizes C; **D_E=1/5, D_R=0** | same | passes, with the record in E (Lemma PP) |
| jointly swapped mirror (τ_q on R, pure E): W_E⊗I_R | realizes C | — | sanity PASS |
| in the swapped world: W_R⊗I_E | p-value 2/3 = KF; does not realize C | — | mirror-symmetric, as expected |

- **Haar check (supplementary, numpy seed 271, 2000 random U_SE).** Max p-value 0.4854 (τ_q) and 0.4130 (τ_½), both ≤ KF. This is weak evidence; the bound itself is the proof.
- **Threshold (d_E=4).** With rank 2, an explicit R-untouched realization is exact (KF=1). With rank 3, the construction value is 2/3 = KF. The "iff" is confirmed.
- **(iv) Two events, fresh slots, τ_q.** W_R per slot ⊗ I_E realizes C₁C₂ exactly on carriers A and B. The R-untouched constructions reach their KF exactly: 2/3 (A) and 1/3 (B).
- **Q-2 (τ_½).** S(ω_R) − ΔS ≥ 0 for W_R⊗I_E, W_E^c, W_Bell^c, W_W^c and W_R;SWAP (min slack 0.0; 200 random inputs plus 2 specials, mpmath 50 digits). This is a forced consistency check and is not counted.
- **Owner illustrations (not counted).** Every realization gives equal K states on π_p and π_v. Carrier A with a 3-dimensional append E register realizes C₁C₂ with orthogonal erased-address records, so the owner is recoverable from E.

**Verdicts.**
- **Q-1: PASS.** (a) holds, (b) holds, (c) holds, and the (iv) consistency holds.
- **Q-L (record location): NOT ADMISSIBLE**, confirmed. W_R;SWAP realizes C with D_E=1/5 and D_R=0.
- **Q-2:** consistency holds (forced).

Reading:
- Under TB, the T-270 tie between E-α (E untouched) and its R-untouched mirror is broken: the E-untouched class survives and the R-untouched class is empty.
- What TB actually forces is that **R's purity must be consumed**. It does not force the record to stay in R; a subsequent E–R swap moves it into E. TB also does not select W_R among writers that touch E.
- The asymmetry was put in by hand through the NEW premise (pure R, mixed E). It is not derived.

## 4. Directive categories
- **Native premises:** unchanged (tree, P1 contraction, I, owner/address data).
- **New derived consequence:** conditional on TB and inside the benchmark. Theorem L: no R-untouched realization exists, with the exact optimum given by KF; the rank threshold is rank τ_E ≤ d_E/f. Lemma PP: record location cannot be fixed by any initial-state premise.
- **Still supplied:** TB itself, the channel, factorization, receiver algebra, dimensions, access and probability law.
- **Constrains delivery?** Partly. It excludes R-untouched realizations, but not records ending up in E.
- **Accessible observable?** None new.
- **Physical vs mathematical:** mathematical consequence of a physically motivated supplied premise (Landauer / third law). No native physics is derived.

## 5. Scope, deviations and disclosures
- Local run on the shared Grok box, not Actions. Started 13:00:48 MST, exit 0, empty stderr.
- One pre-run edit to the frozen script before its single run: the mpmath conversion now goes through 60-digit strings instead of Python complex, and an unused line in KF() was removed. The draft is committed as `evidence/prerun_draft_t271_tb.py`.
- The independent numpy checker `t271_verify_np.py` agreed on its first run (no failed checker runs).
- **Wording deviation.** The T-271 controls table expected owner illustration (1) "for every control". The fixed-ingredient mirror does not realize C, so the theorem does not apply to it, and its π_p/π_v K states differ. Every realization satisfies (1). The illustration is not counted.
- Every outcome was predicted analytically in T-271. The run is a bounded exact check of those proofs.
- AGENTS.md closure items not claimed: Actions producer/verifier, publication job, merge audit, CLOSED/CERTIFIED status.
