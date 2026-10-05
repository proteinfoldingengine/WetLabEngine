# A11.X60 - universal prescribed repair by shared exceptional color

Date: 2026-10-05 UTC.
Analytical parent: 625165b7f1befd06e7fd562c34d26daaa42b5c01.
Scope freeze: d398392c959406e2c5b0c22c0b5b2c3c6c5c4431.
Status: exact analytical candidate for fresh independent whole-argument review.
No numerical execution.

## 1. Fixed native carrier and theorem

Retain the EXACT X58/X59 colored carrier. G is a finite fixed labelled role set, A={0,1,2,3}, R=G minus A. For every a in A, Gamma_a is an actual simple graph on R. Declare precisely the root types Q={a} union e for e in Gamma_a, each with c_Q>=1 ORIGINAL labelled copies. Assume
(C) vc(union_{a in J} Gamma_a)>|J| for every nonempty J subset A.

Fix IN ADVANCE ANY prescribed permutation pi of G, with no later role/label/root relabeling. For t>=1 the physical palette contains distinct labels x_(s,h) for s in G,1<=h<=t and disjoint fixed padding sets Z_j. Source and destination role groups are
B_j=Z_j union {x_(j,h):h=1..t},
D_j=Z_j union {x_(pi^{-1}(j),h):h=1..t}.
Each original copy of type Q has source E_Q=union_{j in Q}B_j and exact destination C_Q=union_{j in Q}D_j. Its SAME original positive floor f_i may be any f_i<=N_Q=3t+sum_{j in Q}|Z_j|, including arbitrary unequal saturation.

X60U. EVERY prescribed pi admits an explicit finite native path from E to C with tau in {3,4} after EVERY one-incidence primitive. The path renews column by column, restores each original labelled full destination support, toggles every differing endpoint incidence exactly once and no other incidence. Its length
L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|
is the GLOBAL endpoint Hamming minimum.

This closes X59's direct-minimum single-column obligation WITHIN condition(C) and this one-anchor/two-outside representation. No common-hit seed-color hypothesis, disjoint upper exception family or supplied root order is required.

X60M. For every m>=24 there is a fixed private eight-type carrier with a prescribed SINGLE m-cycle containing two separated two-anchor runs. At t=1,no padding, one copy/type,floor3, its E_pi is nonempty while X59's B is empty. The constructed path uses exactly THREE physical four-cover identities. EVERY minimum-incidence direct-band native path between these exact endpoints requires at least THREE distinct upper-cover identities. This is an all-minimum-path separation, not an unrestricted temporary-incidence obstruction.

## 2. Inherited exact endpoints and pair localization

X58's equivalence of(C) supplies:
- A is the unique role cover of size at most four;
- every footprint F of size<=4 other than A has an ACTUAL avoiding type.

Brief verification: J=A minus F is nonempty when F!=A and |F|<=4; X=F intersect R has |X|<=|J|. Condition(C) supplies an actual edge of a color in J avoiding X. Its actual type avoids F. Conversely a small vertex cover of Gamma_J yields a different small role cover. Positive copies do not change covers.

Nonempty prepared role groups project physical hitting sets to owners; they have exact tau4 and minimum covers formed by one representative per anchor. This applies at both outer endpoints and every completed column for ANY pi.

In active column h, two active labels indexed by S have footprint S union pi(S). Any pair with at most one active label has footprint<=3. Thus the only pairs without an actual common column-union witness are
E_pi={S subset G: |S|=2 and S union pi(S)=A}.
Such S is a subset of A and pi(S)=A minus S. All other physical pairs have an actual original type avoiding BOTH full column endpoints, hence their union and every support within it.

For exceptional S, all OLD roots with color in A minus S avoid its physical pair; all NEW roots with color in S avoid it. This is actual support avoidance, not a fictitious color capacity. No complement closure is assumed.

## 3. Structural exceptional-family lemma

If pi(A)!=A and E_pi is nonempty, E_pi has at most TWO members and their intersection is nonempty.

Proof. Fix an actual exceptional S0. Write S0={a,b}, its complement={c,d}, naming the actual fixed roles so that pi(a)=c and pi(b)=d. These are proof names only; no physical relabeling or change of prescribed endpoints occurs.

A second exceptional pair cannot be {a,c}, since its footprint contains pi(a)=c already in the pair and cannot have four elements. Likewise {b,d} cannot be exceptional.

The remaining intersecting candidates are:
- {a,d}, exceptional only if pi(d)=b;
- {b,c}, exceptional only if pi(c)=a.
The disjoint candidate {c,d} would require pi({c,d})={a,b}; together with pi({a,b})={c,d} it would imply pi(A)=A, excluded.

Both intersecting candidates cannot occur together: pi(c)=a and pi(d)=b would again imply pi(A)=A. Hence there is at most one additional exceptional pair, and it shares a with S0 or b with S0. The claimed common anchor s exists.

Construction: compute E_pi from the six actual two-subsets of A as an exact finite definition, not an executed numerical campaign. If nonempty and anchor mixing, choose the least fixed anchor s in their intersection. The proof above guarantees this choice. Condition(C) on a singleton also ensures Gamma_s has at least one actual type and positive copies. No reserve-count bound is needed here.

The contrast is structural: anchor-preserving pi may have the four distributed exceptions of X58. Anchor mixing forces a common exceptional color.

## 4. Four native phases for a common exceptional color

Consider an anchor-mixing pi with nonempty E_pi and choose common s as above. Let F_s be the family of ALL original copies of color s. Keep every other original copy untouched until F_s is fully repaired for this column.

Use the following literal finite edit lists, with copies and labels in fixed original order:
I. In every copy of F_s, add ALL missing column-destination incidences. Do not delete any incidence anywhere.
II. In every copy of F_s, delete ALL old-only column incidences. Other colors remain untouched.
III. In every other original copy, add ALL missing column-destination incidences. Completed F_s stays fixed; no deletion in other colors yet.
IV. In every other original copy, delete ALL old-only column incidences. Completed F_s stays fixed.

No common incidence, padding label or other column is changed. Empty lists are skipped. Copy coexistence is literal: many original copies may be enlarged or partly repaired, and all the following witnesses refer to their ACTUAL supports.

### Actual lower protection through all phases

A nonexceptional pair retains an actual union-avoiding root through ALL four phases, even if its witness itself changes: every support remains within its column endpoint union.

For each exceptional S, s in S. Every color in A minus S differs from s and has actual original roots. Those roots remain at their OLD column supports throughout phases I/II, so they avoid the pair and protect the whole F_s preparation/deletion, including every partially enlarged seed.

After phase II, EVERY actual F_s copy is at its NEW column endpoint. Its anchor s lies in S, so it avoids that exceptional physical pair. Because s belongs to EVERY exceptional S, ANY one completed F_s copy now protects ALL such pairs simultaneously.

That same actual root stays untouched in phases III/IV. No protective resource is consumed; the roots formerly carrying old protection can now change under the installed common-color witness. This proves tau>=3 at every primitive, covering all mixed/ordinary/active pairs. The palette has at least four labels, so exclusion of two-label hitting sets excludes smaller hitting sets as well.

### Actual three-stage upper protection

Define physical sets for this column:
K0={x_(a,h):a in A},
Ks={x_(a,h):a in A minus {s}} union {x_(pi^{-1}(s),h)},
K1={x_(pi^{-1}(a),h):a in A}.

K0 and K1 have four distinct labels. Ks has at most four; if it has only three, it can be extended by any existing palette label to a four-set without losing coverage. No incidence edit implements an existential witness change.

During phase I every root contains its OLD column endpoint, hence K0 hits all roots.

After ALL F_s additions are complete, each F_s root contains its NEW column endpoint and therefore x_(pi^{-1}(s),h). Every other root is OLD and contains its own anchor label x_(a,h), a!=s. Thus Ks hits ALL original roots simultaneously at the phase-I boundary.

Use Ks through phase II: F_s roots retain their new endpoint, hence its new anchor label; other roots retain their old anchor. Use it through phase III: F_s stays new, and every other root retains its OLD endpoint throughout additions. All old, new, enlarged and partly changed copies remain hit.

After ALL remaining additions complete, every root contains its NEW column endpoint. K1 now hits all original copies. Use it through phase IV, when destination containment persists.

At both witness switches the adjacent sets are valid at the SAME boundary state. Every cover has size<=4, so tau<=4 on the SAME path already proved lower-safe. There is no independent upper/lower order selection, no unverified supplied DAG and no skipped active-copy state.

### Floors and next primitive

During additions an active root contains its old column endpoint; during deletions it contains its new endpoint. Both have size N_Q. Thus its OWN original floor f_i<=N_Q is preserved, including saturation. Every listed addition is absent; every listed deletion is present. All labels belong to the fixed palette; no extra copy or weakened floor occurs.

Finite phase/copy/incidence lists provide an eligible next primitive whenever edits remain. Their remaining scheduled incidence count decreases after every primitive; zero-edit copies and empty phases are skipped without fictitious moves. All four phases terminate at the exact column destination.

## 5. Universal composition over pi and columns

There are three exhaustive prescribed cases:
1. pi(A)=A: accepted X58 supplies its direct-band minimum path. Its native labelled domain and colored hypothesis are exactly those here.
2. pi(A)!=A and E_pi empty: accepted X59Z supplies the all-add/all-delete union bridge, direct-band and minimum.
3. pi(A)!=A and E_pi nonempty: Section3 derives a common s, and Section4 supplies the four-phase direct-band minimum path.

No condition on X59's B or actual U/V is needed. In particular no inactive column is necessary, although multiple columns are allowed.

At a completed column, each role still contains t+|Z_j| labels, the original actual type/copy carrier and(C) remain, every root has size N_Q, and its original floor is unchanged. Later unresolved columns still have their source owner labels. Reuse the same prescribed case, common color if needed, and four-cover construction with the next column's physical labels.

Finite unresolved-column count decreases at each completed column; finite phase counts supply continuation inside it. Completion restores every ORIGINAL labelled full destination support exactly. Padding and common incidences were never altered. No claim is made about arbitrary safe unfinished prefixes.

The count is L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|: each column label belongs to source Q iff its role is in Q and to destination iff it is in pi^{-1}(Q). Each differing incidence toggles ONCE, every common incidence stays. Any native path must toggle each outer endpoint difference at least once, proving global minimum.

Repeated qualifying endpoint-to-endpoint legs renew the carrier/certificate at every exact boundary, but their concatenated counts are minimum PER LEG only. Revisiting incidences can prevent a global outer-chain minimum. No maximum-layer conversion is used for X60U.

## 6. Arbitrarily long control outside X59's common-hit relay

For every m>=24 let G={0,...,m-1}. Use precisely X58's private eight-type carrier:
Gamma_0={{8,10},{9,12}},
Gamma_1={{4,6},{11,14}},
Gamma_2={{5,7},{13,16}},
Gamma_3={{15,18},{17,m-1}}.
All eight outside edges are pairwise disjoint and private, so Gamma_J is a matching of 2|J| edges and vc(Gamma_J)=2|J|>|J|. Boundary roles19,20,21,22 occur in NONE of these edges.

Let L_out be the increasing list of ALL outside roles except19,20,21,22. Prescribe the SINGLE cycle
pi=(0,2,19,L_out,21,1,3,20,22),
where L_out means splice that list into the cycle. Every role occurs once; this is an actual fixed permutation for each m, declared before repair. It has two separated length-two anchor runs 0->2 and1->3, not the four-consecutive-anchor X59 control.

Then
pi(A)={2,3,19,20},
pi^{-1}(A)={0,1,21,22},
B=A intersect pi(A) intersect pi^{-1}(A)=empty,
E_pi={{0,1}}.
Indeed only active starts0,1 have images in A; they map to2,3.

All actual U={Q:Q avoids pi^{-1}(A)} types are exactly colors2/3, because edges avoid21,22. All V={Q:Q avoids pi(A)} types are exactly colors0/1, because edges avoid19,20. They are disjoint, but X59 R1 fails maximally. The strict source/destination block-stable relay requires every color2/3 copy before every color0/1 copy. At its boundary after colors2/3 have completed and before colors0/1 begin, the pair{x_(0,1),x_(1,1)} hits every actual root: new colors2/3 contain0/1, old colors0/1 contain0/1. Thus no such root order is lower-safe. This is a rigorously incompatible STRICT joint certificate, not arbitrary native disconnection.

Choose common s=0. At t=1,no padding use
K0={0,1,2,3},
Ks={22,1,2,3},
K1={0,1,21,22},
writing physical labels by role indices. Section4 completes ALL color0 roots first via additions and deletions, then all remaining additions/deletions. Color2/3 OLD roots protect pair{0,1} until color0 is NEW; color0 then jointly protects all remaining edits. Ks bridges the upper cover while the old complementary family changes.

This works on arbitrary positive original copies and floors; the discriminating control uses one copy/type and saturated floor3. Every type changes: a three-set cannot be invariant under a full m-cycle with m>=24. No unchanged background root exists.

The full outer endpoint-union tuple has tau EXACT TWO. The exceptional pair{0,1} hits every union; every singleton has footprint<=2 other than A and hence an actual union-avoiding root. There is no static union three-guard.

## 7. Three upper identities are necessary on EVERY minimum direct-band path

This section concerns t=1,no padding, the private control of Section6. Any positive multiplicities also retain the proof, but the declared control is one copy/type,floor3.

The source and destination have unique physical four-covers K0 and K1 by the colored exact-cover equivalence. A direct-band path has an upper four-cover at every state; a three-cover can be extended to four. If a witness family of at most TWO distinct four-sets sufficed over the path, they MUST be K0 and K1 because the exact endpoints have those unique covers.

Every minimum-incidence native path stays within each original root's endpoint union. To attain the Hamming lower bound, every differing incidence must toggle exactly once and no common or absent-at-both incidence can toggle; otherwise length exceeds the bound. Thus this support-union constraint is NECESSARY for every minimum path, without imposing it on unrestricted native admissibility.

For a color0/1 type Q={a} union e, its endpoint union intersects K0 in exactly {a}. Its source outside edge avoids all anchors; its destination anchor is21 or22. Its destination outside labels cannot be anchors: their successors would have to be2,3,19,20, and the edge contains neither anchors2,3 nor boundary roles19,20. Therefore K0 covering this root forces physical a in{0,1} to be present.

For a color2/3 type, its endpoint union intersects K1 in exactly its NEW anchor, respectively0 or1. Old outside edges avoid21,22; destination outside labels cannot equal any member of K1 because their successors are anchor roles0,1,2,3, absent from outside edges. Thus K1 covering this root forces a physical label in{0,1} to be present.

Consequently if BOTH K0 and K1 hit a state confined to endpoint unions, the pair{0,1} hits EVERY root, so tau<=2. Such a state is forbidden in a direct-band repair.

Suppose nevertheless only K0,K1 suffice. Initially K1 is not a cover (source has unique K0); finally K1 is a cover. Let the FIRST state covered by K1 follow its previous state by one primitive. Since that previous state has no K1 cover, the assumed two-witness family requires K0 to cover it. The primitive making a previously failing hitting set K1 become a cover MUST be an ADDITION: deleting an incidence cannot turn a root disjoint from K1 into one meeting it. An addition preserves every previously valid hitting set, so K0 also covers the new state. Both covers then hit that state, contradicting tau>=3 above.

Therefore no two-identity upper witness family exists on ANY minimum-incidence direct-band native path between these endpoints. At least THREE distinct physical four-sets are required. Section4's K0,Ks,K1 suffice and are distinct, proving the exact minimum of three.

This lower bound does not exclude nonminimum paths using temporary incidences outside unions. It does not bound primitive length beyond the independently attained Hamming minimum. It is stronger than a prescribed-order obstruction: it ranges over every minimum native ordering and every chosen four-cover family.

## 8. Advance, dependency domains and next obligation

X59 already proved universal LOWER minimum and multi-column direct minimum, plus several single-column sufficient relays. X60 discovers that anchor mixing forces all exceptional pair obligations onto one actual anchor color. Completing that color renews lower protection; interleaving whole-family addition/deletion phases transports upper coverage without requiring a common-hit seed or strict block-boundary root order.

This proves direct GLOBAL minimum completion for EVERY prescribed pi within the actual colored class, including the single-column no-padding saturated-floor case. The long private control has B empty, a forced conflict for the old strict two-cover certificate, no unchanged background, union tau2, and an exact all-minimum-path three-cover lower bound. It is an arbitrarily long structural family, not a root-count campaign.

Frozen X58/X59 sources are unchanged. Their(C), endpoint projection, common footprint, native floors and Hamming-count domains match this construction. X51's strict copy-coexistence relay is used only to classify the failed old certificate; Section4's ACTUAL phase covers prove copy safety directly and permit switches after family-wide additions. Symmetry connectivity was already known; this adds a prescribed direct-minimum mechanism and cover-complexity theorem, not a new unrestricted connectivity classification. Maximum-layer, exact-compaction, guard-buffer, palette-room and element-cover theorems are not invoked.

Remaining: weaken the unique small-cover/colored-footprint structure itself, such as carriers with several competing minimum covers or pairs whose union footprints have no actual avoiding root beyond this single exceptional anchor set. Derive a renewable interface for those actual obligations, rather than assume common-color availability. Arbitrary access to this representation, noncolored mixed/directed/higher-target/nested universality and physical interpretation remain open. Multiple role columns here each contain one moving label per role; arbitrary unequal owner transports are not claimed.

No numerical scientific commands, diagnostic enumeration, workflow, implementation, fixture, benchmark, integration merge, new numbered certification or physical claim. Certified v16.54/v16.55 and all original evidence remain preserved; separate efficiency implementation remains unstarted.
