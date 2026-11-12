# Q168 PREREG (2026-11-11 21:12 MST, written before analysis)
Question: does any inherited source define an attainable-state set / event domain on which the Q157 guard reference must be
nonnegative, deciding Q167's split between (a) positivity on all of F_X^+ (=> Lemma 166.1 => blind) and (b) positivity only at the
actual state on the event fiber (=> free α, either direction)?
Definitions: F_X=Q^X, F_X^+=Q_{>=0}^X (v16.23 TYPE_LEDGER row C); natural linear refs f=βT_0+Σα(d,j)E_{d,j} (Q166); carriers = T1 finite
rooted common-Genesis trees (v16.27 completion PROOFS T1); J(E) = predecessor-closed event sets = exactly reachable retained covers
(v16.28 T3/D1, used in v16.31).
Premises: INHERITED: T1, J(E)/D1, row C, P1 extensive pushforward. SUPPLIED (by Q157): the guard itself. No new assumption.
Novelty vs settled: Q167 named the domain choice as unsupplied after reading two ledgers only (its adversarial item iii); Q168 does the
source census for an attainable-state/domain clause and tests whether the one inherited reachable-state set (J(E)) decides it.
PASS (line closes as located obstruction): every inherited state-set clause either constrains covers/supports only, or has conic
hull F_X^+ on every carrier, so it is equivalent to (a) for linear refs; and the grade-level attainable set is explicitly OPEN in sources.
FAIL (revise Q165–Q167): a source clause restricting attainable grades to a proper subcone on some carrier, or typing the guard domain.
Counterexample strategy: (1) grep all UQCF-GEM sources at research 6b0ca26c for attainab/reachable/admissible state/domain/faithful;
(2) test J(E) and faithfulness restrictions against the Lemma 166.1 witnesses δ_a; (3) look for a P1-image restriction.
Analytic only; no numerical run.
