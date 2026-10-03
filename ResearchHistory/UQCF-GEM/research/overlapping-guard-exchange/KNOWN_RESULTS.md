# Accepted starting results and the remaining obligation

Source baseline: `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, under `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`. Historical proof headers say candidate; their separate independent review records and final closeout govern acceptance. The original files are unchanged. This ledger summarizes scope, not a new certification of their implementations.

All statements concern fixed palette, labelled slots and positive floors. Unless stated otherwise, the output for two permitted exact-q endpoints is a primitive path with transversal in {q-1,q}.

| Accepted result / source | Required input | Output and boundary |
| --- | --- | --- |
| Targets 1 and 2; GENERAL_PARENT_CONNECTIVITY | Any feasible same-carrier endpoints | Direct expansion/contraction; target 1 stays exact |
| Upper-excursion removal; same source, A | A finite path maintaining tau>=q-1 between exact-q endpoints | Converts to the desired band; does not supply the lower-guard path |
| Arbitrary-arity target 3; same source, D | Exact target 3 | Element-cover buffering plus upper removal; not arbitrary pair-cover connectivity |
| Five-child target 4; same source, F | r=5, exact target 4 | Degree-two cycle buffering or saturated partition exchange |
| Saturated capacity; EXACT_ENDPOINT_CAPACITY, H/I | delta=sum_i(k-a_i)-(q-1)k=0, q>=3 | Classifies full roots plus a partition and connects all such endpoints; positive delta remains separate |
| All floors 2; FLOOR_TWO_CONNECTIVITY, O | a_i=2 for every slot | Graph star edits and renewed symmetrization reach a common form |
| Mixed floors 1/2; SINGLETON_ANCHOR_REDUCTION, Q | Every floor belongs to {1,2} | Anchor/residual-graph reduction; does not cover arbitrary higher floors |
| Enough singleton anchors; same source, P | At least q slots have floor 1 | Other floors may be arbitrary; reaches protected class |
| Protected roots; PROTECTED_EXCHANGE, J/K | Each endpoint has q pairwise disjoint roots | Connects that class; its existence requires sum of q smallest floors<=k, but accessibility from every endpoint is not proved |
| Safe symmetry exchanges; OVERLAPPING_CLIQUE_EXCHANGE, L/M | Label permutation, or root permutation with destination-compatible floors, at exact q | Connects symmetry-related endpoints, not arbitrary overlap types |
| Contraction clone guard; CONTRACTION_CLONE_GUARD, U/V/W | Slot-compatible prescribed clone; retained-family cover f and contraction cover lambda | Exact formula tau(new)=min(1+f,lambda); eligible clones or a globally terminating sequence are not guaranteed |
| Uniform modules; HYPEREDGE_STAR_RELOCATION, Y | Complete h-uniform cores on a partition, h>=3, q=k-m(h-1)>=3; extra roots contain core roots | Connects endpoints of this type at fixed r,k,h,q; not a universal normal form |
| Cyclic triples; CYCLIC_TRIPLE_CONNECTIVITY, AA | Three nonempty palette parts, all internal triples and directed AAB/BBC/CCA core triples, floor 3, redundant extras, k>=6 | Connects this class at fixed r,k and q=k-3; not all triple systems |
| Disjoint compatible guards; GUARD_BUFFER_CONNECTIVITY, AB | Actual t=q-1 guards on disjoint index sets | Two-phase handover for arbitrary floors; extended to one shared slot by the present candidate |
| Uniform slot bound; same source, AC | Uniform h, r>=2N with N=binomial(h+q-2,h) | Small guards can occupy disjoint existing slots; present candidate improves to 2N-1 |
| Palette room; PALETTE_SLACK_CONNECTIVITY, AE | k>=sum_i a_i | Split shared labels using currently unused labels already in P; does not follow from complementary capacity |
| Finite-support reduction; FINITE_SUPPORT_REDUCTION, AD | Compact endpoint pair, S=sum_i a_i | Preserves connectivity answer on a suitable subpalette of size<=3S+1; finiteness does not imply connectivity |

The exact-endpoint hierarchy supplies |N_A(X)|>=q-|X| and the local capacity inequalities. One-root replacement consumes at most one lower-guard unit, but the completed state need not renew exact redundancy. Complete-module normal forms are genuinely unavailable in some exact higher-floor carriers (MODULE_CAPACITY_OBSTRUCTION); those examples are not disconnection results and the cyclic class has its own successful method.

The present candidate targets a missing link: protection can transfer through one shared root, without requiring disjoint guards or palette room. The unresolved problem is a generally available, renewing exchange when multiple shared slots admit different missed-root sets. An exact characterization of one bridge's failure does not resolve general connectivity.
