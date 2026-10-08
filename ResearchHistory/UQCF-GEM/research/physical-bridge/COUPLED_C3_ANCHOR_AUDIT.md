# C3 three-anchor lemma — author-side audit

Date: 2026-10-07.
Status: AUTHOR-SIDE AUDIT PASSED; independent review pending.

Scope: COUPLED_C3_ANCHOR_SCOPE.md at f12d6775214b827ede8e5a5248e9b8f92721c048.
Proof: COUPLED_C3_ANCHOR_RESULT.md at f99a7622a968d8a5ebdfebb4e43c76dc4e925fb0.

Checks:
1. Three distinct singleton supports force three distinct hitting labels a,b,c.
2. Any nonempty fourth support can be hit by at most one further label, so tau<=4.
3. All-additions-then-deletions keeps fourth support containing target T during deletion, hence above original floor f4.
4. If S differs from T, a legal endpoint-only first event exists.
5. The theorem does not imply full endpoint-only connectivity of the other three roots, and is not a no-go for all coupled four-root carriers.
6. C2 M4-first is a concrete consistency control: it is safe, but its completion can block later chosen macros.
7. No auxiliary necessity or physical interpretation is claimed.

Conclusion: the structural obstruction is valid as an author-side candidate. It narrows C3 carrier selection without claiming the entire C3 theorem.
