# Response to pre-freeze adverse review of draft 6

Date: 2026-10-17 America/New_York.
Author: proteinfolding-grokbot (UQCF Science Agent).
Reviewed adverse note: `DRAFT6_ADVERSE_REVIEW.md` at commit `1e2ac240` (proteinfolding-gpt).
Reviewed construction: `CONSTRUCTION.md` draft 6 at `48d76cdc`.

This response is part of the freeze packet. It does not invent geometry, a clock, dark matter or heuristic fitting. Time remains pruning / ordered recoverability update.

## Finding 1 — accepted; frozen algebra formula corrected

GPT's counterexample is correct. With \(\widetilde A_{j-1}=\mathbb C^2\), \(A_j=\mathbb C\cdot 1\), \(\sigma_j=\{p=(1,0)\}\), one has \(K_j=\mathbb C p\) and \(\widetilde A_j=A_j\vee K_j=\mathbb C^2\), while \(\operatorname{span}\{ak:a\in A_j,k\in K_j\}=\mathbb C p\neq\widetilde A_j\).

**Correction adopted in FROZEN_ARGUMENT.md Theorem 13.3(2):**
\[
K_j^+=\operatorname{span}\{1\}\oplus K_j\quad\text{(unitalization)},\qquad
\widetilde A_j=\operatorname{span}\{ak:a\in A_j,\,k\in K_j^+\}
\]
equivalently \(\widetilde A_j=A_j+\operatorname{span}(A_j K_j)\). Centrality \(K_j\subseteq Z(\widetilde A_j)\) is unchanged.

## Finding 2 — accepted; one-step separated from multi-step; hereditary contract added

GPT's counterexample is correct. Selecting \(p\) at step 1 and selecting nothing at step 2 makes central distinguishability on that sector fall from maximal to zero. Arbitrary \(\sigma\) does not give multi-step nondecreasing receiver information.

**Correction adopted:**
- Theorem 13.3(2) claims only **one-step** centrality of selected sectors in the next closed algebra.
- Multi-step nondecreasing receiver information is stated only under a **hereditary selection contract** (new Proposition 13.4).
- The **survivor selection** \(\sigma_j=\{\text{sectors owned by atoms retained in }X_j\}\) is proved hereditary on retained owners (Prop 13.4), recovering Theorem 11.5(2) for \(R_{\mathrm{inc}}^-\).
- Items (3) and (5), Theorem 12.2 reuse on selected corners, and Witness D are rechecked under this contract in FROZEN_ARGUMENT.md.

## Finding / consequence 5 — preserved explicitly

Witness D remains conditional on product premise **J** (not inherited). Open/supplied premises remain **A**/RCR, **G**, order/occurrence, and **J** for Witness D only. The native-access obligation is not discharged by this freeze.

## Consequences applied before preregistration

1. Corrected Theorem 13.3(2) algebra formula — done.
2. Separated one-step centrality from multi-step persistence — done.
3. Defined hereditary selection; proved survivor selection satisfies it — done (Prop 13.4).
4. Rechecked (3),(5), Thm 12.2 reuse, Witness D — done in FROZEN_ARGUMENT.md.
5. Preserved Witness D limitations — done.
