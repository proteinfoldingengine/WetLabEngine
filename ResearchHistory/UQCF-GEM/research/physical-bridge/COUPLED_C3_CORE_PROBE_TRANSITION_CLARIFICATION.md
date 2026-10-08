# C3 core-probe transition relation — explicit clarification and review adjudication

Date: 2026-10-08. Status: CLARIFIED CANDIDATE; fresh independent review required.

Read with the unchanged COUPLED_C3_CORE_PROBE_SCOPE.md and COUPLED_C3_CORE_PROBE_RESULT.md. This document makes the bounded model's complete transition rule explicit. It does not assert that arbitrary other native systems obey this rule.

## Complete rule

A state X(P,Z) is admissible exactly when all four full supports have cardinality at least 2 and their exact hitting number lies in [3,4]. Core labels lie in C; Z is fixed, lies in the disjoint palette T, and occurs only in root 4. There are no additional state or transition predicates in this checkpoint.

For an admissible state X and command c=(i,s,x), where i is a fixed root slot, x is a core label, and s is + or -, define the syntactic membership predicate m_c(X): x is absent from root i for +, or present for -. If m_c(X) holds, let X^c be the state obtained by that one incidence toggle. Define

    L_c(X) iff m_c(X) and X^c is admissible.
    Outcomes_c(X) = {X} union ({X^c} if L_c(X), else the empty set).

The first element is the permitted rejected NO-OP, even for a legal command. No mandatory success, fairness, hidden capacity test, auxiliary filter, or spectator-dependent transition predicate is included. This is the exact interpretation of the frozen scope's one native-admissible incidence edit or rejected NO-OP. If a larger system imposes extra predicates, application to that system requires a separate proof that they are preserved. No such extension is claimed.

## Explicit substitution proof for Theorem 3, step 4

Fix a feasible observed history and a realizing Z_*. Take any Z' with |Z'|>=D_n. At a committed step, the observed projection toggles exactly the named core membership. Because C and T are disjoint, membership of that named core label depends only on P_i, so m_c has the same truth value under Z_* and Z'. Substitution commutes with the toggle: replacing Z_* by Z' before or after toggling a core incidence gives the same X(P',Z').

The history floor bound proves every substituted observed source and successor has all floors >=2. Lemma 1 applies when the fourth core projection is nonempty; Lemma 2 applies when it is empty and the floor requires |Z'|>=2. Thus the substituted successor has exactly the observed hitting number in [3,4]. Both conjuncts defining L_c hold. Therefore the committed successor is in Outcomes_c for Z'. At a rejected step the unchanged source belongs to Outcomes_c for every Z'. This establishes transition-by-transition sufficiency under the complete rule, not merely matching endpoint observations.

All other conclusions and limitations of the original proof are unchanged. In particular, observed successful deletion can certify positive hidden capacity; rejection cannot certify emptiness; accessibility of O_core and progress remain assumptions or open obligations.

## Adjudication of the actual review

Run 37852620648, workflow 0ffbd0574a59c687c49a59b221406a3e82945cd1, returned REVISE despite zero listed missing assumptions and zero counterexamples. Its extra actionable_mathematical_objection field asks whether unlisted spectator-dependent admissibility criteria exist. That field must not be discarded merely because the standard arrays are empty. The full response and original manifest are preserved in evidence/c3-core-probe-review-37852620648.json; response SHA256 92b1722e1f130a2dd4b09688064b5cc1376ee0d7ede3335225f719eb585ca151.

The concern is resolved for the stated model by explicitly specifying the complete transition relation above. It would be a genuine limitation for a broader relation with additional hidden predicates. The original frozen scope and executable relation use precisely membership, floors and band: no new transition restriction is being introduced to obtain acceptance. The theorem's scope is not broadened. Fresh independent review must assess the original proof together with this clarification; prior REVISE remains historical evidence.
