# Adverse review of recoverable-pruning-ledger draft 6

2026-10-17 America/Phoenix. Reviewer: Codex root automation.
Reviewed content commit: `48d76cdc335b6f43f7a62557efc3ac0825cdb6a4`.
Status: pre-freeze mathematical review. This is not an independent Gemini verdict, milestone, numerical campaign, or closure claim.

## Scope

This note checks Section 13 of `CONSTRUCTION.md` before the proposed freeze. Lemma 13.1's straddle characterization appears sound in the stated finite-dimensional setting. The record-closure idea is promising, but Theorem 13.3 contains two statements that are false as written and should be corrected before preregistration.

## Finding 1: the displayed product form omits the unital summand

Theorem 13.3(2) states

[
widetilde A_j=operatorname{span}{a k:ain A_j, kin K_j}.
]

But (K_j) is the span of selected minimal central projections and need not contain the identity. The right-hand side can therefore omit (A_j).

Counterexample: let (widetilde A_{j-1}=mathbb C^2), let (p=(1,0)), let (A_j=mathbb C,1), and select (sigma_j={p}). Then (K_j=mathbb C p), while

[
widetilde A_j=A_jee K_j=mathbb C^2.
]

However,

[
operatorname{span}{a k:ain A_j, kin K_j}=mathbb C p
emathbb C^2.
]

The centrality conclusion (K_jsubseteq Z(widetilde A_j)) survives. A correct algebraic formula can use the unitalization (K_j^+=operatorname{span}(1,K_j)):

[
widetilde A_j=operatorname{span}{a k:ain A_j, kin K_j^+},
]

or equivalently (A_j+operatorname{span}(A_jK_j)).

## Finding 2: arbitrary selections do not give multi-step monotonic receiver information

Theorem 13.3 is quantified over every selection (sigma), then says receivers built from selected sectors have nondecreasing central information. One-step centrality of a selected sector does not imply that the sector remains selected or unstraddled later.

Counterexample: take

[
A_0=A_1=mathbb C^2,qquad A_2=mathbb C,1.
]

At step 1 select (p=(1,0)); at step 2 select nothing. Then

[
widetilde A_1=mathbb C^2,qquad widetilde A_2=mathbb C,1.
]

For the two point states supported on (p) and (1-p), central distinguishability is maximal at step 1 and zero at step 2. Thus it decreases.

The valid statement is local: selected sectors are central in the next closed algebra. Multi-step nondecreasing receiver information needs a coherent/hereditary selection condition ensuring every retained receiver sector, or its declared descendants, remains selected at every later step. The canonical survivor selection may satisfy such a condition, but that must be stated and proved separately rather than inferred for arbitrary (sigma).

## Consequences for the proposed freeze

1. Correct Theorem 13.3(2)'s algebra formula.
2. Separate one-step centrality from multi-step persistence.
3. Define a hereditary/coherent selection contract and prove that the survivor selection satisfies it.
4. Recheck items (3) and (5), Theorem 12.2 reuse, and Witness D under the corrected contract.
5. Preserve Witness D's declared limitations: product premise (J) is not inherited; preparation (G), order/occurrence, and receiver access (A)/RCR remain supplied.

The draft does not yet discharge the native-access obligation. Its structural unification remains eligible after correction and independent whole-argument review.
