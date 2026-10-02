# v16.54 findings — the general parent-support principle

Status: independently accepted analytical results. No implementation or new numerical campaign has run. v16.54 is not CLOSED/CERTIFIED; the certified v16.53 predecessor remains unchanged.

## The general result

For any number of children, fixed palette and positive child-width floors, two exact-target-q root tuples (q>=2) have a one-unit connection if and only if they can be connected while keeping the hitting number at least q-1. Any such lower-guard connection can be rewritten so that the parent hitting number stays in {q-1,q}. Upper excursions are removable.

This is Theorem A in GENERAL_PARENT_CONNECTIVITY.md, accepted at proof SHA256 de144b98ee80c99510dc1eabb7318be11d67603f5f7337004019dc8372bc2751 by INDEPENDENT_PROOF_REVIEW.md. The submitted proof retains its candidate heading to preserve the reviewed bytes; the independent decision records its accepted status.

The structural explanation is explicit. Root supports may be expanded freely. Merging two label roles selected from a minimum hitting set lowers the hitting number exactly one. The union of two such local repairs lowers it by at most two relative to the removed high layer. Addition/deletion paths through those unions preserve width floors and the one-unit band. This argument does not depend on a branching number.

## What determines connectivity now

Write B_i=P\A_i and impose capacities |B_i|<=k-a_i. A hitting-number lower bound q-1 is exactly the requirement that every (q-2)-subset of the palette lies in some B_i. The remaining problem is therefore capacity-bounded subset-cover reconfiguration:

| Target | Required lower guard | Analytical outcome |
|---|---|---|
| q=1 or2, arbitrary arity | Elementary expansion/contraction | Connected |
| q=3, arbitrary arity | Cover every individual label | Connected; native exact admissibility supplies spare capacity |
| q=4, five children | Cover every pair of labels | Connected; degree-two incidence transfers plus an explicit saturated-hub argument |
| q>=3, arbitrary arity, saturated capacity sum b_i=(q-1)k | Cover every (q-2)-subset | Connected by the exact-endpoint normal form and partition exchanges |
| Positive-slack higher targets at arbitrary arity | Cover every (q-2)-subset | General connectivity remains OPEN beyond the proved cases |

Five-child target3 is now a consequence of the arbitrary-arity theorem. It does not require its own passing-case campaign. Five-child target4 tests a genuinely different lower guard: ordinary label coverage is insufficient. Its proof handles both spare incidence capacity and the no-spare-capacity case, rather than silently excluding saturated exact states.

## Native consequence and limit

The accepted fixed-root clearance mechanism lifts these root paths through arbitrary children already supplying the inherited interface. Child interiors stay exact during parent reconfiguration; child normalization occurs only at an exact parent. Thus the bound is on the global sum of deviations, not separate coordinate bounds.

The parent criterion is necessary and sufficient within the stated width-floor root graph, and sufficient for native nested repair. Its failure would not alone prove a native barrier: a native path may spend a unit inside a child and temporarily leave that child's minimum-exact-width carrier. A genuine obstruction must exclude those additional native paths too.

## The next mathematical question

Establish or refute a general exchange theorem for capacity-bounded pair and higher-subset covers, restricting endpoints to complementary tuples of exact-q native states. Such endpoints cover every (q-1)-subset and leave at least one q-subset uncovered. Total complementary capacity is at least (q-1)k, but that scalar slack has not been proved sufficient to preserve all pair/higher-subset constraints during reconfiguration.

The next useful deliverable is that exchange theorem or a precisely characterized obstruction to it. Another branching-number campaign or larger passing-case count would not resolve this question. No universal arbitrary-target connectivity, native nonunit obstruction, path-length efficiency or physical interpretation is claimed.

## Publication boundary

Native scope:3932248af7bb5c64bdd3d467fcd6d78ddf7adde5. Reviewed proof:26bdda935564ba828e89bb7879400285789f2d72. Parent:f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8. Draft PR102 holds this analytical work separately from the certified predecessor. Any later implementation has its own prospective protocol, written plan, independent producer/verifier, GitHub execution and full certification gates.

## Exact-endpoint extension: the capacity boundary is resolved

EXACT_ENDPOINT_CAPACITY.md (proof commit b1ebe5df4f534c8813797d5a3b2ccc430e757126, SHA256 37556dd879d80b1301395fbc89b8ec1ee442a0497459c659accbf776fa604ff8) is independently accepted in INDEPENDENT_CAPACITY_REVIEW.md with no findings.

At an exact-q endpoint every s-subset S, s<=q-1, lies in at least q-s complementary blocks. For s<=q-2, the capacities of precisely those blocks obey sum_{i:S subset B_i}(b_i-s)>=(q-s-1)(k-s). In particular every required lower-cover subset has at least two covering blocks. One whole block can therefore be replaced safely; this redundancy cannot be assumed to survive repeated replacements.

When total capacity attains its lower bound, every exact endpoint has r-q full-palette roots and q roots partitioning the palette. The same floor vector forces the same full-palette indices. Finite partition swaps give a one-unit path for every q>=3 and every arity, resolving pair and all higher-subset reconfiguration on this entire boundary.

For positive delta=sum b_i-(q-1)k, compaction leaves at most delta labels below maximum incidence degree r-q+1. Their deficits sum exactly to delta. This localizes the remaining structural problem without proving that these labels supply a safe exchange buffer. Universal positive-slack connectivity remains OPEN. No implementation or numerical campaign was initiated.
