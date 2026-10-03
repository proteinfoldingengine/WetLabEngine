# A11.X3: target-three residual lifting with q-3 singleton-floor slots

Status: frozen candidate analytical proof for independent review. Scope parent: d6728a23537dcb59ae875ce9d0a62377e2c8c3bf. No enumeration, numerical campaign, implementation, tests or workflows. All earlier frozen scientific sources and receipts remain unchanged.

## 1. Result and inherited sources

Fix an original finite ordered palette P of size k, labelled root slots, positive floors a_i, and primitive one-incidence moves. Let A,C be permitted exact-q endpoints, q>=4.

**Theorem X3.** If at least q-3 ORIGINAL floors equal one, A and C are connected by a finite native primitive path with tau in {q-1,q}, with arbitrary positive floors elsewhere.

Set m=q-3>=1 and choose the SAME m floor-one slots J at both endpoints. No support in another slot is assumed compact or disjoint from the anchors. Feasibility gives k>=q and r>=q.

Inherited accepted dependencies at integrated baseline 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f:

- GENERAL_PARENT_CONNECTIVITY.md Theorem D: exact-three endpoints on ANY finite palette and positive floor vector, arbitrary feasible arity, have a finite primitive path in {2,3}.
- OVERLAPPING_CLIQUE_EXCHANGE.md Lemma L: a global palette transposition from exact hitting level t has a primitive path in {t-1,t}, preserving every floor and slot; concatenate transpositions for a permutation.
- GENERAL_PARENT_CONNECTIVITY.md Theorem A: a finite lower path tau>=q-1 between original exact-q endpoints can be converted to a finite path in {q-1,q} on the same carrier.

These theorems are not reproved or independently recertified here. Target-three connectivity is ALREADY accepted, not new X3 work. The new result is the common residual-carrier reduction and its higher-target consequence.

The construction allows temporary incidences, palette permutations implemented by primitive moves, and repeated toggles. It does NOT resolve A11's universal destination-directed question or minimal necessary anchor count. The original target-four uniform-floor-three diagnostic is outside its hypothesis.

## 2. Normalize distinct singleton anchors and align their labels

At either original endpoint contract each selected J support to a singleton, by individual deletions retaining any chosen label. Its original floor is one, and contraction cannot decrease tau, so completed and intermediate tuples have tau>=q.

If two selected singletons both contain p, change one by {p}->{p,t}->{t}, where t is outside the current selected-anchor label set. The other {p} singleton forces p, so the union step leaves all hitting requirements unchanged; deletion cannot lower tau. The number of distinct selected labels strictly increases. Duplicates and available labels exist until all m labels are distinct, because k>=q=m+3. The procedure is finite.

Fix canonical label set U consisting of the first m labels of P in the anchor-slot order. Extend the assignment from the normalized ordered anchor labels to U to a global palette permutation. Implement it using inherited Lemma L's primitive transposition paths on the WHOLE tuple.

If the normalized tuple has exact hitting number t>=q, each completed transposition retains t and each primitive has tau>=t-1>=q-1. It preserves root cardinalities and floors. At the completed permutation, the selected slots are the same canonical singleton anchors and tau=t>=q. Their labels are fixed from now until the residual connection has been made. The nonanchor supports need not be unchanged by this permutation; they retain their original floors and labelled indices.

Do this separately at A and C. A reverse of the entire construction for C will restore its original labels and supports exactly. No permutation is treated as a primitive, and no extra palette labels are introduced.

## 3. Exact anchored decomposition before inactive-root preparation

Let R=P minus U, n=|R|=k-m>=3. At a completed canonical-anchor tuple X with tau(X)>=q=m+3, let I_X be the nonanchor slots whose supports are disjoint from U. These supports lie in R. All other nonanchor roots meet U and are automatically hit by any set containing U.

Every transversal must contain the m singleton labels U. Conversely U plus any transversal of the I_X family hits every root. Thus, with tau(empty family)=0,

    tau(X)=m+tau_R((X_i)_{i in I_X}).

In particular the active family has residual transversal g>=3 and is nonempty. Its roots are the ACTUAL permitted supports at their original slots; no virtual roots or new support floors are used.

Define a partition depending only on the ORIGINAL floor vector and canonical R:

    F={i not in J: a_i<=n},     Z={i not in J: a_i>n}.

Every active index belongs to F. A root in Z cannot be contained in R, since its required cardinality exceeds n, so it necessarily meets U at every allowed support. Such roots are redundant while the singleton anchors remain fixed.

The sets F,Z are the SAME for both endpoints. This is essential: I_X can vary between endpoints and cannot simply be passed to Theorem D as if its slots were identical.

## 4. Complete a common residual carrier without changing the hitting level

Keep all original active I_X supports fixed during this preparation.

For every inactive flexible slot h in F minus I_X, replace its support X_h by the WHOLE R using

    X_h -> X_h union R -> R,

adding missing labels individually and then deleting source-only labels individually. R respects a_h because a_h<=n. Floors hold by expansion from a permitted source and contraction to a permitted destination.

This replacement preserves tau EXACTLY at m+g. To prove the upper bound, choose a minimum transversal H of the unchanged original active family; H is a nonempty subset of R, since g>=3. U union H hits each intermediate support: the expansion segment contains the old X_h, which meets U; the contraction segment contains R, which meets H. All other unconverted inactive roots meet U, and previously converted flexible roots equal R and meet H. The original active roots and the fixed anchors give the matching lower bound m+g.

Expand each high-floor root h in Z to P by individual additions. It meets U throughout and remains redundant, so tau stays m+g. All floors hold. Neither a_h nor a high-floor root is lowered to fit R.

At completion the selected anchor slots are canonical singletons, EVERY flexible slot in F has a support inside R meeting its ORIGINAL floor a_i, and every slot in Z equals P. For ANY subsequent permitted tuple Y in this residual carrier,

    tau(full lifted Y)=m+tau_R(Y).

The equality is exact throughout every residual primitive: the anchors force U, all flexible roots lie entirely in R, and the full-palette roots are already hit by U. No union of root slots, relaxed support size or compact-only restriction is used. The residual vector consists of the SAME labelled F slots and the SAME original floors at both endpoints.

Because g>=3, |F|>=3 and n>=3. The residual floor bounds 1<=a_i<=n are built into F, so the eventual target-three call is in its native domain.

## 5. Higher residual levels can reach exact three safely

The prepared residual tuples at the two endpoints can have tau_R greater than three; applying Theorem D directly to them would be invalid. We explicitly reduce them first.

From any prepared residual tuple with g>=3, add its absent R-incidences in a fixed finite order, stopping at the FIRST tuple with tau_R=3. If g=3 initially, take the empty sequence.

Such a stopping point exists. At the end of the full addition list every flexible support would equal R, giving transversal one, since F is nonempty. A single support addition can lower transversal by at most one: a transversal for the expanded tuple can be repaired to hit the old nonempty support by appending one old support label. Transversal is an integer and cannot increase under additions. Thus descent from g>=3 to one must encounter three, without ever jumping from a level above three below it.

Before stopping every residual value is at least three. Hence the lifted tuple has tau>=m+3=q. All original floors are maintained by expansion. There is always another absent incidence while the level exceeds three; if none were absent, the level would be one. The number of absent incidences strictly decreases, so the step cannot continue indefinitely.

This is an exact finite construction, not a heuristic or a numerical execution. A hitting-number check defines its stopping state mathematically; no search outcome or claimed runtime is used. Apply it independently at the prepared A and C tuples, obtaining residual endpoints S,T with tau_R(S)=tau_R(T)=3.

## 6. Apply accepted target-three connectivity and lift every move

The two residual endpoints S,T share:

- palette R consisting of existing original labels;
- the SAME labelled root set F, of size at least three;
- the SAME positive original floors a_i<=n;
- exact transversal THREE.

All hypotheses of accepted Theorem D are therefore satisfied. It supplies a finite one-incidence residual path with transversal in {2,3}.

Hold the selected singleton anchors U and all high-floor supports P fixed. Perform each residual toggle at its ORIGINAL labelled root index and original palette label. This is a legal primitive in the original carrier, since the residual floors are the same a_i. By exact additivity,

    tau(full tuple) in {m+2,m+3}={q-1,q}

throughout this middle connection. R is only an analytical subpalette for the residual call; the full native palette remains P and no new roots are inserted.

Concatenate:

    original A -> canonical prepared A -> lifted S
    -> lifted T -> reverse canonical preparation and normalization for C
    -> original C.

Endpoint anchor normalization preserves tau>=q; symmetry paths preserve tau>=q-1; inactive-root preparation preserves a completed level at least q; residual descent preserves tau>=q; the middle path is in {q-1,q}; reversed endpoint constructions have the same lower bounds. Therefore the complete finite path has tau>=q-1 and original exact-q endpoints.

Apply accepted Theorem A ONCE to this full path to remove any upward excursions from endpoint normalization or symmetry stages. It gives the stated fixed-palette, fixed-floor, fixed-slot path in {q-1,q}. This proves X3. The accepted conversion need not preserve the anchored form or the residual sequence.

## 7. Protection renewal and global termination

With m=q-3 anchors, a forbidden set of q-2=m+1 labels must consist of U plus ONE residual label x. It fails to hit the tuple exactly when x is missed by at least one flexible root. Thus the anchored lower problem is ORDINARY ELEMENT coverage by residual complementary blocks, not arbitrary pair coverage.

The accepted target-three construction maintains that coverage: its element-owner transfers establish a replacement occurrence before deleting the old occurrence, and its spare-capacity argument provides the next legal transfer. The exact-three residual endpoints supply the accepted capacity hypotheses. This inherited renewal mechanism is being lifted to the full tuple, not inferred from endpoint counts alone or newly recertified.

Global progress has explicit finite stages: selected-anchor distinctness increases; a finite permutation decomposition aligns anchor labels; finitely many inactive flexible and high-floor roots are prepared; residual additions strictly reduce absent incidences until exact three; accepted D supplies a finite residual path; the reverse endpoint word terminates and restores every labelled support. No arbitrary safe-prefix extension premise is used. X1's stranded-prefix counterexample remains valid.

## 8. General conditional lifting principle

The same argument proves an explicitly conditional reusable reduction:

**Anchor-lift principle.** Suppose exact-target-s native one-unit connectivity is established for EVERY finite palette and positive floor vector, with s>=2. Then for any q>s, at least q-s original floor-one slots suffice for native one-unit connectivity at exact target q, with arbitrary other floors.

Replace m=q-3 by m=q-s. The canonical residual construction gives g>=s. Expansion to all R-roots gives level one, so the one-incidence bound guarantees exact s can be reached before dropping below it. Invoke the ASSUMED exact-s theorem and lift its {s-1,s} path by the forced contribution m. Symmetry paths and final accepted upper removal are unchanged.

For X3 the premise is the already accepted s=3 Theorem D, so its conclusion is unconditional within the disclosed inherited dependencies. No premise of universal connectivity for s>=4 is assumed or proved. The principle cannot be used to declare those open targets closed.

## 9. New sufficient class and unchanged frontiers

**Corollary X3.4.** One ORIGINAL floor-one slot suffices for native one-unit connectivity of ALL feasible exact-four endpoint pairs on the same carrier, with arbitrary positive floors elsewhere. The selected root need not be singleton at either endpoint and need not share any label between them.

For general q>=4 this strengthens the independently accepted X2 sufficient count q-2 to q-3. X2 remains correct and supplies its separate direct six-move guard renewal. X3 uses the additional inherited target-three theorem and global symmetry paths to obtain the stronger class.

Sufficiency does not establish a minimal or necessary anchor count. Fewer than q-3 such slots remain outside X3 unless another accepted theorem applies. At q=4 this leaves the ZERO-singleton-capable case; exclude existing all-floor-two, protected, palette-room, slot-bound, symmetry and other solved classes before declaring any particular carrier unresolved. In particular uniform floor three remains OPEN outside applicable accepted classes.

This does NOT prove universal A11 destination-directed scheduling: endpoint permutations, preparation to R or P, helper labels, residual transfers and reversed normalization can use temporary incidences and repeated toggles. General unrestricted q>=4 root/nested universality remains OPEN, and native lifting retains its accepted child-interface conditions.

No physical geometry, primitive time, new external design property, numerical result, implementation certification, measured efficiency or originality claim is made. This is an analytical reduction using accepted lower-target connectivity, with all original floors and labelled slots preserved.

