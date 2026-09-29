# UQCF-GEM v16.25 — Pruning/refinement closure

v16.25 continues foundational closure from v16.24.

## Main result

For componentwise legal ancestral pruning of an indexed retained cover with unchanged union carrier:

**h_after >= h_before.**

The complete bounded audit covered **488,307** same-union refinements across all **17** rooted tree shapes through five vertices. **318,719** strictly increased the order; **169,588** were unchanged; **none decreased it**.

For nested retained carriers, ancestral retractions and source pushforwards compose exactly, so direct and staged pruning are factorization-independent.

The theorem does not compare prunings that change the final union. It adds no response model or geometry.

Scientific GREEN: GitHub Actions run **36612979239**, execution SHA `a0064589cb491a68b35c575899e8fc718c41becb`.

Substantive verifier RED: run **36612453511** exposed acceptance of a non-prefix intermediate carrier before correction.

See [combined findings](demos/v16.25-pruning-refinement-closure/RESULTS.md), [proofs](demos/v16.25-pruning-refinement-closure/TYPE_AND_PROOF.md), and [reproduction](demos/v16.25-pruning-refinement-closure/REPRODUCE.md).

**Time is pruning / ordered recoverability update.**
