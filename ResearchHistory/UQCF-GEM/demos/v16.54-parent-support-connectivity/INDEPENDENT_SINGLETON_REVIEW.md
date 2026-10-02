# Independent review — singleton-anchor reduction

Reviewer: /root/v1654_singleton_review.
Verdict: ACCEPT the analytical proofs of Theorems P and Q.
Artifact: SINGLETON_ANCHOR_REDUCTION.md at 60a1b1da426858926dc6022f78de1f1d46e95a62.
Verified SHA256: 93eda3cc5c6f7904c5d88e6d99576d70892e638cda04e2414ad9bb2ea4fb932c.
Critical: none. Important: none. Minor: none.

## Essential checks

1. Exact compaction retains the chosen hitting set and all floors. Duplicate-singleton reassignment preserves the old constraint through another {x}; contraction cannot decrease hitting number.
2. P: q distinct singleton roots force the lower guard while all other roots expand. The destination is exact-q and protected, allowing J despite arbitrary other floors or different witness indices.
3. Q: canonical anchor relabeling uses L at current q', giving q'-1>=q-1. Pair roots touching anchors are redundant; replacing them retains the residual graph in fixed slots and stays exact at q'.
4. Additivity holds at every residual primitive state: forced labels are in T and all residual supports stay in its complement.
5. Graph normalization works from cover number at least ell. Clones maintain that bound, splitting stops at ell and balancing preserves ell. For ell=2 the frozen graph's cover number at least 1 supplies a surviving edge.
6. Slots, duplicate normalization and ordering are valid; residual swaps use only floor-2 slots. The separate ell=1 construction avoids a zero-edge issue in star editing.
7. Endpoint constructions reach the same ordered tuple. Theorem A is applied to the completed finite lower-guard path with exact-q original endpoints, not a residual path beginning above its target.

Relevant arguments in GENERAL_PARENT_CONNECTIVITY.md, PROTECTED_EXCHANGE.md, OVERLAPPING_CLIQUE_EXCHANGE.md and FLOOR_TWO_CONNECTIVITY.md were also checked. No mutations, numerical scripts, simulations, enumeration, tests or subagents were used.

## Declined-to-judge items and executor rulings

- Implementation correctness: unimplemented. Ruling: analytical theorem only, not validated code.
- Tests: not run in analytical scope. Ruling: no test-passing claim; future mechanism-focused protocol required.
- Numerical certification: not performed. Ruling: not CLOSED/CERTIFIED.
- Native lifting beyond child-interface assumptions: excluded. Ruling: retain conditional sufficient lifting and no native-necessity assertion.
- Efficiency: excluded. Ruling: finite constructions only, no runtime/path-length guarantee.
- Physical interpretation: excluded. Ruling: no physical claim.
- Repository/PR integration: outside review. Ruling: executor verifies exact bytes, ancestry/change scope and draft state separately; no merge inferred.

No outstanding findings remain.
