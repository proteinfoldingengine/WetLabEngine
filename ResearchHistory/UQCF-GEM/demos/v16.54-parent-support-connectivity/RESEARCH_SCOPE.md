# v16.54 — general parent-support connectivity, proof first

The user's objective is to discover the structural reason one-unit repair is possible, ending progression by branching number. Five-child targets3 and4 are focused tests of what the current mechanism does not explain. The deliverable is an arity-independent principle or a precisely characterized obstruction, with those tests used to discriminate mechanisms.

This is an architectural analytical investigation, not implementation. The written brief carries forward the user's supplied purpose and constraints. Existing source, evidence and the v16.53 certified claim remain unchanged. No new numerical execution has occurred. Implementation/specification approval gates apply before a later code campaign.

## Approach

1. State the general width-floor root graph and its exact relation to native lifting.
2. Rewrite the hitting-number band as capacity-bounded covering of label subsets by complementary blocks. Separate lower and upper band obligations.
3. Test structural sufficient conditions: spare incidence capacity, controlled temporary overlap and local replacement of forbidden high-transversal states. Keep all assumptions explicit and determine which follow from exact admissibility.
4. Use (r,q)=(5,3) and (5,4) to expose missing guards, not to accumulate examples. Require finite constructive arguments for all feasible widths/palettes in any claimed subcase.
5. Obtain independent analytical review of candidate lemmas before calling them accepted. Report the remaining general conjecture separately. Any implementation/certification requires its own written plan and full closure chain.

Alternatives considered: another branching-number implementation campaign would not meet the user's goal; an unguided finite search would provide bounded evidence without explaining the mechanism. The recommended route is the abstract connectivity problem, with exact five-child boundary analysis and later narrowly specified computational probes only if a concrete unresolved obligation needs them.

## Analytical leads already known before this commit

- Transversal number changes by at most one when one admitted incidence changes. Monotonicity alone does not prove band connectivity because row width floors can block deletions.
- Fixed-root clearance from v16.53 is independent of the number of sibling roots. It suggests a general sufficient lifting theorem, but not automatic necessity for the width-floor graph.
- Complementary blocks turn the lower band guard into coverage of all (q-2)-subsets. Ordinary element coverage is therefore insufficient for five-child target4, which requires pair coverage.
- At any exact-q state, a label occurs in at most r-q+1 child roots: that label and one label from each uncovered child would otherwise give a smaller hitting set.
- Five-child target3 might use the existing element-cover path plus a local detour around the forbidden pairwise-disjoint states of transversal5. A candidate detour adds one overlap and uses unions of neighboring augmented states; its lower-band bound still needs a complete proof.
- Five-child target4 exact endpoints have label incidence degree at most2. A candidate route compacts roots to their width floors and reconfigures a binary incidence matrix with column capacity2. Spare-capacity cycle exchanges and the saturated case need explicit justification.
- In the saturated degree2 case, the graph of shared child pairs may force a common hub when the transversal is4 on five nonempty roots. A star-versus-triangle argument is a lead, not yet an accepted theorem.

These leads arose while framing the problem. This commit prospectively freezes admissibility and research scope before new execution; it does not claim that the leads were preregistered before thought or independently proved already.

## Success and honest incomplete outcomes

A useful positive result is an explicit general connectivity/lifting criterion whose hypotheses can be checked from native exact states, with all intermediate guards proved. Five-child success alone must not be described as an arbitrary-arity theorem. A negative result must identify the exact failed condition and whether it obstructs this construction, the width-floor graph, or all native unit paths. If the universal principle remains open, publish the proven reductions and the precise remaining connectivity question.
