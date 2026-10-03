# A10: a reachable renewal trap and complete local move certificates

Status: frozen analytical candidate for independent review. Scope parent: 69d0ec47822ba133ab4a6148c41f2a128b912fea. A10_SCOPE.md fixes two DISTINCT questions. No enumeration, tests, implementation or workflow. Original finite palettes, labelled slots and positive floors are retained.

## 1. Two relations, with different questions

Put L=q-1, q>=4. The recovery method M has all admissible tau>=L tuples as vertices. Its edges are A9 common-saturation exchanges in a two-label fiber whose actual inactive family has tau>=q-2, OR destination-compatible root transpositions certified by the common two-slot union tuple having tau>=L. These paths consist of actual single incidences. M does not include arbitrary critical-fiber paths or unrestricted primitive moves.

Question M: can every lower state reachable from an exact-q tuple by a primitive unit-band path recover to an exact-q tuple USING M? Section 4 gives a negative answer.

The secondary relation W permits SINGLE primitive incidence changes certified by a two-label fiber: either inactive tau>=q-2, or inactive tau=q-3 and every minimum inactive transversal retains both pure-role witnesses after the change. Section 5 defines its assumptions precisely and proves W equals the original lower primitive graph. This is a local expressiveness theorem, not a global path-selection algorithm.

Neither question silently alters A7, A8 or A9. Failure of M's recovery property does not disprove M-connectivity between every pair of exact endpoints. Equality of W to a primitive graph does not prove that graph connected.

## 2. Native exact-four source and repeated-triple destination

Use P={1,2,3,4,5,6,7}, q=4, 35 labelled root slots and uniform floor four. Describe supports by complements. Every admissible complementary block has size at most three.

Let E have one root for every three-element subset T of P, with support P minus T, in lexicographic triple order. Thus E has exactly binomial(7,3)=35 roots, all of size four. Every three-label set misses its own complementary root. Any set of four labels meets every root, since two four-element subsets of a seven-element palette must intersect. Hence tau(E)=4.

Use these seven triples:

    B_1=123, B_2=145, B_3=167, B_4=246,
    B_5=257, B_6=347, B_7=356.

Every pair lies in exactly one B_j, as verified by the displayed pair partition in A7; this can also be read directly from the seven triples. Their complementary roots have tau=3: every pair misses a root, while {1,2,4}, which is not a B_j, hits all seven size-four roots. No external design property is used.

Construct D with FIVE copies of each support P minus B_j. Keep one copy at the original E-slot of its triple B_j. Order the other 28 slots increasingly and fill them with four additional copies of B_1, then four of B_2, and so on through B_7 in complement notation. This defines the exact labelled D, not merely its multiset. Its 35 roots all have size four, and duplicates leave tau(D)=3=L.

## 3. A finite primitive unit-band path E to D

Hold the seven designated roots P minus B_j fixed. They form a lower guard with transversal three. Process each of the other 28 slots in its fixed order. Replace its current support U by its destination V through U -> U union V -> V, adding missing incidences then deleting excess incidences individually, in palette order. Every support contains its own starting or destination support, so floors four hold.

The fixed seven-root subfamily proves tau>=3 throughout. Independently, every intermediate support has size at least four, so ANY fixed four-label set hits every root, giving tau<=4 throughout. No upper normalization dependency is needed. Each replacement uses at most six incidences, since two four-subsets of seven differ in at most three labels in each direction. At most 168 primitive moves are used; some slots may need fewer or none.

Thus D is reachable from an exact-four endpoint by a floor-preserving primitive path with tau in {3,4}. The reverse path is an equally legal recovery to E. The construction uses the original palette and all original slots; no temporary root or label is created. The finite slot/incidence list supplies termination.

This is a diagnostic in a carrier already covered by the accepted uniform-slot sufficient bound, not a new universal primitive-connectivity class. The direct path above is self-contained and does not rely on that bound.

## 4. All certified M choices remain trapped at level three

At D, choose ANY distinct palette labels u,v. There is exactly one B_j containing their pair. A root is inactive for this pair precisely when its support contains neither u nor v, equivalently its complement contains both. Therefore the inactive family is exactly the five identical roots P minus B_j. These roots are nonempty and have common support, so their transversal is exactly one.

For q=4 the A9 common-saturation criterion requires inactive transversal at least two. It fails for EVERY label pair. Hence D has no certified saturation exchange in M, including pairs chosen adaptively rather than in any fixed schedule.

Root-slot transpositions cannot change D's multiset of supports. Every resulting tuple again has five copies of each displayed complement triple, tau=3, and inactive transversal one for every label pair. This argument applies inductively to every state reachable from D in M. No saturation edge can become eligible after arbitrarily many root swaps.

In fact every root transposition of such a tuple is lower-certified. Its two-slot union path modifies at most two roots, leaving at least three copies of EVERY displayed root unchanged. Those unchanged roots keep transversal at least three. Each half contains its endpoint tuple of transversal three, so the entire swap path stays EXACTLY at level three and respects floors. Thus D's M-component is precisely all labelled reorderings of its multiset, with no hidden omitted slot choice.

Every vertex in that component has tau=3. No exact-four tuple belongs to it. This also excludes a route through higher completed levels: there is no eligible edge that leaves the component at all.

**Theorem T10-M.** A9-certified saturation exchanges plus certified root swaps cannot guarantee recovery from every legally reachable one-unit-defective state. The explicit D is primitive-reachable from exact-four E and primitive-recoverable to E, but its entire M-component has level three.

This is a rigorous method-recovery obstruction, not failure of one schedule. It is NOT a counterexample to primitive connectivity or to exact-endpoint-only connectivity of M. An exact-to-exact algorithm may avoid D; that possibility is not excluded. Adding more choices of the same certified pair exchanges or more root swaps cannot help after reaching D. A different mechanism, such as a critical-fiber witness handover or background-changing move, is required for recovery there.

## 5. Critical witness extension represents EVERY legal primitive move

We now define the distinct secondary local relation W on the lower carrier. Its candidate edge toggles exactly one incidence and must respect all original floors. It must lie in a two-label fiber of the exact A6 type. At its source X, use the actual background family, inactive family F, g=tau(F), and lambda_0 from A9. Since tau(X)>=L, the exact four-case formula implies lambda_0>=L and g>=q-3.

A candidate is certified if either:

- g>=q-2; or
- g=q-3 and, at its destination Y, EVERY minimum transversal H of F leaves an active pure-u root and an active pure-v root whose background it misses.

The first case certifies every admissible tuple in that fiber by A9. The second case is A9's exact critical-witness criterion. The invariant lambda_0>=L supplies its background hypothesis. Source witnesses in the critical case hold already because X is a lower vertex. Thus every W edge is a legal lower primitive move.

Conversely take ANY original lower primitive edge X to Y, toggling label u at root i. If the move adds u, choose any v in X_i. The old root is nonempty by its floor and lacks u, so v exists and v!=u. If the move deletes u, choose any v in Y_i; the new root is nonempty and lacks u. In either case v is retained in the changed root. Choosing the least such label in the existing palette order makes the choice deterministic.

Only incidences of u change, so backgrounds outside {u,v} are identical. Root i is active before and after because it contains v. Every other root is unchanged, so the active-slot union is fixed. Therefore X,Y lie in one permitted two-label fiber, on the original palette and slots.

The exact source formula implies g>=q-3. If g>=q-2 the move is certified in the first case. If g=q-3, Y's lower level implies the exact critical pure-role witnesses for EVERY minimum inactive cover, certifying it in the second case. These exhaust the possibilities. No enumeration or unproved pair-selection heuristic is used.

**Theorem T10-W.** The lower primitive graph and W have exactly the same SINGLE-INCIDENCE edges. Every legal lower move admits a two-label certificate with a retained companion label. Conversely every such certified, floor-valid move stays in the lower graph.

This is a local certificate-completeness statement. The certificate test can require all minimum transversals of F; no computational speedup or efficient witness procedure is claimed. It is not a proof of global connectivity, because all we have shown is another exact description of the graph whose connectivity remains the problem. The retained companion label gives pair selection for a supplied primitive move, not selection of an improving move.

The result prevents circular progress claims: adding arbitrary critical witness-certified primitive moves does remove an expressiveness restriction, but proving their global availability and well-founded use requires the original lower-connectivity argument. A supplied whole primitive path cannot be advertised as a new macro mechanism simply because its edges have these certificates.

## 6. Scientific decision and next obligation

A10 closes two declared analytical obligations: M's recovery-completeness claim is false, and W's local move expressiveness is exact. Both statements are self-contained given A9's accepted hitting-set identity/witness equivalence, whose mathematical uses are shown explicitly. No external perfect-design property is needed.

The remaining scientific problem is global. For q>=4, exact-target endpoints correspond in complement notation to covering every (q-1)-subset, while a lower path must keep covering every (q-2)-subset under each root's derived capacity. A proof must show this endpoint structure permits a finite progressing lower path, or produce a fully checked obstruction to that primitive connectivity. Local expressiveness alone cannot do so.

The original q=4/floor-three diagnostic remains open. A10 uses q=4/floor FOUR, with many duplicate supports; it neither resolves nor substitutes for that diagnostic. Universal higher-target primitive connectivity and full nested lifting remain OPEN or conditional on accepted child interfaces. Target-three arbitrary-arity connectivity remains the accepted baseline.

The next unit should target a genuinely global complementary-pair-cover argument at q=4, with admissibility, continued protection and a well-founded progress measure. More isolated local safety lemmas are not universal closure. No implementation, numerical campaign, efficiency, originality or physical-law claim is made.
