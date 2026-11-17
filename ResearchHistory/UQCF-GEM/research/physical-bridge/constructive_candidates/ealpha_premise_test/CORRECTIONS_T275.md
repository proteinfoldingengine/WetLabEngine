# CORRECTIONS_T275 — append-only analytic corrections to the E-α bounded test (PR #130)

- **Author:** proteinfolding-grokbot (Grok, UQCF Science Agent). **Date:** 2026-11-02, America/Phoenix.
- **Source of corrections:** T-273-dot (Dot, PR #111 comment 6587834812), accepted by the package author in T-275 (agent-thread 1e614355); ownership confirmed in T-283-dot / T-284 (PR #111 comments 6593485652, 6593580006).
- **Originals preserved, unedited:** `PREREGISTRATION.md` blob `cd005b2f27e921650168ab43f43cf9899d12e8f9`, `RESULT.md` blob `3745831acc4d72845b0455432e102acaf2665768` at branch head `0531fb5f12578ca2a5f23a626ab3d2c4701e2575`; all failed checker runs under `evidence/local-run-1/failed/`; raw Gemini review `evidence/gemini-review-41512469271/`. `SHA256SUMS` is left as it was and does not cover this file.
- **Review binding:** Gemini run 41512469271 reviewed the ORIGINAL text only. It does not certify these corrections or the amended whole argument.
- **Status:** POSTED analytic corrections (supporting mathematics inside the SUPPLIED benchmark plus the NEW premise sharp E-α). Package stays REVIEWED LOCAL EVIDENCE, open and unmerged. Native receiver delivery NOT_DERIVED.

## C1. Fixed versus fresh receiver capacity (supersedes RESULT §3 last two sentences of Proposition X2's commentary, RESULT §6 reading, and the "New derived consequence" bullet)

**Withdrawn:** "The receiver has to be a register whose capacity grows with the number of events", "The sharp premise is consistent only when each event gets fresh receiver capacity", and "a single fixed-dimension receiver cannot absorb two events … Sharp E-α composes only with fresh receiver capacity per event".

**Kept:** Proposition X2 for a single receiver *qubit* (Choi rank 3 on carrier A, 4 on carrier B, both > 2) stands, with its proof unchanged.

**Correct statement (standard Stinespring minimality).** For a channel Φ with Kraus rank r = rank J(Φ), an R-only realization (E untouched, R initially pure) exists iff dim R ≥ r. Necessity: the Kraus operators ⟨k|U|0_R⟩ number at most dim R. Sufficiency: the minimal isometry |ψ⟩ ↦ Σ_k K_k|ψ⟩⊗|k⟩ extends to a unitary on S⊗R. Hence a *preallocated fixed* receiver of dimension ≥ rank J(C_1C_2) (3 on carrier A, 4 on carrier B) absorbs both events at a fixed finite horizon; fresh capacity per event is not required. Explicit carrier-A witness (Dot): R a qutrit, U_i = swap(|u_i,0⟩, |p_i,i⟩); U_1, U_2 commute and ⟨k|U_1U_2|0⟩ = Q_1Q_2, |p_1⟩⟨u_1|, |p_2⟩⟨u_2|. For N disjoint one-hot erasures the Choi rank is N+1, so unbounded histories still need unbounded capacity. The E-writing mirror obeys the same bound, so the corrected statement is W_R/W_E-neutral and does not constrain delivery.

Check (local, not a campaign): `/workspace/uqcf_scratch/t275/t275_check.py`, sha256 `c849c2c48a0af5e65a2008d3d23eb39de46bed0d775386f365a2aa1acbc4ad6a` (sympy 1.14.0; N = 1,2,3 checked).

## C2. Entropy equality condition (supersedes PREREGISTRATION §4 "equality iff z_o+z_v=0 or z_pz_u=0")

**Withdrawn disjunct:** z_p z_u = 0. Counterexample: z = (z_o,z_p,z_u,z_v) = (0,0,½,½) has z_p z_u = 0, but h(z_u) = 1 while (z_p+z_u) h(z_u/(z_p+z_u)) = 0.

**Correct:** with A = 1_{u}, B = 1_{p,u}, the slack is I(A;B); since A ⊂ B, P(A∧B) − P(A)P(B) = z_u(z_o+z_v), so equality holds iff z_u = 0 or z_o + z_v = 0 (zero-weight convention). The inequality itself and P-b's DOWNGRADED status are unchanged. The reported W_R equality instance z = (0,½,½,0) satisfies the corrected condition.

## Remaining remediation (not done here; T-284 items 2–5)

1. Freeze a prospective GitHub producer and algorithmically independent checker with pinned dependencies, the inherited stack and every rejecting control (including corrupted-output rejection), disclosing all known local outcomes and the failed checker runs before execution.
2. Execute on GitHub Actions; separate publication, replay and immutable readback.
3. Fresh whole-argument review only for the corrected substantive claims (C1, C2); PR #132 does not cover them, and the old review is not rebound.
No scientific test is expanded and nothing is rerun by this file.
