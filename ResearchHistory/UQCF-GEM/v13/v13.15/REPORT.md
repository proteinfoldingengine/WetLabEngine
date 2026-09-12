# UQCF-GEM v13.15 — Relational Locality / Sparse Source Closure Gate

**Date:** 2026-09-12

## Adjudication

Graph sparsity by itself does **not** make generic QMAR local.

But a sharply restricted positive sector does close exactly:

**commuting Markov graphical states + clique-compatible ETL sources** admit exact separator-message closure whose cost scales with treewidth rather than total Hilbert-space dimension.

This is the first exact locality compression in the v13 QMAR branch, but it is conditional on Markov/commuting structure that has not been derived from the ontology.

## 1. Generic path locality fails

Take a four-node path, so graph treewidth is only 1.

Construct two strictly positive global states

`rho_+` and `rho_-`

that differ only by a full four-body Pauli term.

Because that perturbation has nonidentity support on all four sites, tracing out **any** site kills it.

Fresh control:

maximum difference across **every proper subsystem marginal**:

`8.674e-19`.

So not only the target edge but every radius-limited neighborhood short of the entire system is identical.

Both states remain positive; minimum eigenvalue:

`0.00625315368525`.

Now apply the same site-local source

`sigma_x` on the first path node

and read the QMAR response of the first edge:
- BKM metric response at its two endpoints;
- polar-transport response on that edge.

The two edge-response vectors differ by

`0.00194759677484`.

Therefore:

**generic local ETL/QMAR response is not determined by any proper-neighborhood marginal, even on a treewidth-1 graph.**

The obstruction is hidden global completion, not graph degree.

## 2. Relation to v12.49

The older incidence-local exchange gate had already shown a different locality obstruction:

for isotropic exchange,
connected edge transpositions generate the full permutation action.

So a path, cycle, star, grid, or any other connected sparse graph has the same exact exchange algebra/module as the complete graph.

v13.15 does not merely repeat that result.

Here the source is site local and the target is a local QMAR edge response.

The new obstruction is:

**global hidden completion can influence a local source susceptibility even when every proper marginal is fixed.**

## 3. Exact positive sector: commuting Markov networks

There is nevertheless an exact locality theorem.

Suppose

`rho ∝ exp(sum_C Phi_C)`

where:
- the clique potentials `Phi_C` mutually commute;
- the graph is chordal or represented by a junction tree;
- the ETL source `P` belongs to the same commuting clique algebra.

Then

`rho_s ∝ exp(log rho + sP)`

simply changes one or more clique potentials.

The state remains in the same graphical exponential family exactly.

Therefore local marginals and their ETL derivatives can be computed by exact junction-tree message passing.

No approximation is involved.

## 4. Executed treewidth-1 controls

Binary Ising chains of sizes

`N = 4, 6, 8, 10, 12`

were tested.

For each chain:
- random local fields;
- random nearest-neighbor couplings;
- a distant site-local diagonal ETL source;
- an interior target edge.

Exact full-state enumeration was compared with two-state separator-message belief propagation.

Maximum finite-source pair-marginal error:

`1.302e-16`.

Maximum source-derivative error:

`8.151e-12`.

Thus the target edge response is recovered exactly from messages whose separator dimension is only

`2`

for every tested N.

The message size does not grow with total N.

## 5. Treewidth scaling

For a binary graphical state with treewidth `w`:

- separator message dimension is at most `2^w`;
- maximal clique tables have dimension `2^(w+1)`;
- junction-tree inference costs `O(N 2^(w+1))`.

So exact local response compression is exponential in separator width, **not** in total N.

That is the locality structure v13.15 was searching for.

But the positive theorem is conditional.

## 6. Why it does not yet solve generic QMAR

Apply instead a local noncommuting `sigma_x` source to a diagonal Markov state.

After finite ETL tilt, the off-diagonal state norm is

`0.0494983080399`.

So the flow immediately leaves the commuting graphical algebra.

Likewise the generic hidden-completion path counterexample shows that tree structure alone does not imply the Markov property required by separator closure.

Therefore:

`graph sparsity != quantum/Markov conditional independence`.

The latter is the real compression principle.

## 7. Architectural result

The hierarchy is now:

`connected graph sparsity alone`
-> **no exact compression**

but

`bounded treewidth + exact Markov factorization + source compatibility`
-> **exact separator closure**.

This sharply identifies the missing property.

It is not locality of edges by itself.

It is **conditional independence / recoverability across separators**.

## Status

- graph sparsity alone: **NO-GO**
- generic bounded-neighborhood QMAR: **NO-GO**
- treewidth-1 generic QMAR: **NO-GO**
- commuting Markov separator closure: **CLOSED EXACT / CONDITIONAL**
- exact state size at fixed treewidth: **LOCAL MESSAGE SIZE INDEPENDENT OF N**
- Markov/commuting structure from ontology: **NOT DERIVED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major no-go plus the first treewidth-controlled exact locality closure in the v13 QMAR branch**.

## Next — v13.16

### Quantum Markov / Conditional-Mutual-Information Selection Gate

The next question is whether the ontology itself selects the property that made v13.15 work.

Test across graph separators:

- conditional mutual information;
- exact/approximate quantum Markovity;
- Petz recoverability;
- source stability of recoverability.

If exact Markovity is not forced, ask whether a derived recoverability bound gives a certified approximate locality theorem.

That would be the first legitimate route from full pre-time quantum completion toward controlled local geometric dynamics without assuming a heuristic truncation.
