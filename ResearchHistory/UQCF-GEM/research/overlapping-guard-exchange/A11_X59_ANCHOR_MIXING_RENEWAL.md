# A11.X59 - prescribed anchor-mixing with coordinated moving covers

Date: 2026-10-05 UTC.
Analytical parent: d955a6e884cba250eb0f2c8bcdaa393460fb7a4d.
Scope freeze: 8b55b187d3738b886f8450b40d246788109a7813.
Status: frozen candidate for fresh independent whole-argument review.
Analytical only; no numerical execution.

## 1. Native labelled objects

Use the exact X58 carrier: finite roles G, anchors A={0,1,2,3}, outside R; actual simple colored graphs Gamma_a on R; precisely the root types Q={a} union e for e in Gamma_a; c_Q>=1 ORIGINAL labelled copies. Assume
(C) vc(union_{a in J} Gamma_a)>|J| for every nonempty J subset A.

Fix an arbitrary prescribed role permutation pi BEFORE repair, now allowing pi(A)!=A. Fixed palette contains pairwise distinct x_(s,h), s in G, 1<=h<=t, and disjoint fixed padding Z_j. At source B_j=Z_j union {x_(j,h):h=1..t}; at destination D_j=Z_j union {x_(pi^{-1}(j),h):h=1..t}. Root Q has corresponding unions E_Q,C_Q. Each labelled copy i has its SAME original positive floor f_i<=N_Q=3t+sum_{j in Q}|Z_j|. Original unequal saturated floors are included.

No owner notation is an extra primitive: every actual move toggles ONE incidence in ONE original root. Role/label names, copies, palette and floors remain fixed. In particular no relabeling changes prescribed outer endpoints.

## 2. Statements

X59L (all prescribed permutations, complete lower renewal).
For EVERY pi, there is an explicit finite path from E to C maintaining tau>=3, with every differing endpoint incidence toggled exactly once and no common incidence changed. It renews over all columns and restores the exact labelled destination. Length
L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|
is the global endpoint Hamming minimum. This is initially a LOWER path, not a direct-band claim.

X59I (inactive-column upper protection).
For EVERY pi and t>=2, the SAME X59L path stays directly in {3,4}, by using an inactive column's physical labels at current anchor owners. Padding may be arbitrary. Its global minimum is retained.

X59Z (no exceptional pairs).
Define E_pi={S subset G:|S|=2 and S union pi(S)=A}.
If E_pi is empty, EVERY t>=1 admits a direct {3,4} global-minimum path, including t=1/no padding. Add ALL missing destination incidences to all roots, then delete ALL source-only incidences. The upper cover switches at the full-union boundary. This interleaves unfinished roots rather than completing root blocks.

X59R (derived compatible moving-cover relay).
Put B=A intersect pi(A) intersect pi^{-1}(A), and
U={Q:Q intersect pi^{-1}(A)=empty},
V={Q:Q intersect pi(A)=empty}.
Suppose
(R1) B meets every S in E_pi;
(R2) U intersect V is empty.
Then EVERY t>=1 admits a direct {3,4} global-minimum path constructed below, including t=1/no padding, arbitrary positive copies and unequal saturated floors. No compatible order is supplied as an input. A simpler purely role condition A subset pi(A) union pi^{-1}(A) implies R2, but actual R2 can be weaker.

For prescribed controls pi=(0 1 2 3 4 5) and pi=(0 1)(2 3 4 5), fixing unlisted roles, R1 and R2 are automatic on EVERY colored carrier satisfying(C). The latter has TWO simultaneous lower obligations and moves the unique endpoint upper cover. Neither requires favorable outside-edge labeling.

These are sufficient direct-minimum results. Universal direct-minimum SINGLE-column repair when E_pi nonempty and R1 or R2 fails remains open. Lower repair for that case is complete, and accepted maximum-layer theorem A can convert its complete original-ended lower path to a band path; the conversion does not preserve our schedule/minimum as a proved property.

## 3. Exact footprint and endpoint facts

Reuse X58's proved equivalence: A is the unique role cover of size at most four, and every footprint F of size at most four other than A has an actual avoiding type. For completeness, set J=A minus F, X=F intersect R. If F!=A, J nonempty and |X|<=|J|; (C) supplies an edge in Gamma_J avoiding X, hence its color/edge type avoids F. Conversely a vertex cover of Gamma_J of size<=|J| would yield a different small role cover.

Every prepared endpoint has nonempty role groups of sizes t+|Z_j|. Projection of any physical hitting set to owners implies tau>=4, and one physical representative per anchor implies tau<=4. This proves EXACT FOUR at both outer ends and completed columns, for arbitrary pi.

In active column h, active x_(s,h) has old owner s and new owner pi(s); every other label has one fixed current owner. A physical pair with at most one active label has footprint size at most three. Two active labels indexed by S have footprint S union pi(S), of size at most four. Thus precisely those S with S union pi(S)=A lack a common endpoint-union witness. This is an EXACT characterization: A hits every type, so for such S the physical pair hits every full column union.

If S is exceptional, S subset A and pi(S)=A minus S, even when pi(A)!=A. This follows because both two-element sets lie in A and their union has four elements. Complement closure of E_pi is NOT assumed.

Every other pair has an actual type avoiding its complete column endpoint union. Any original copy staying inside that union is a persistent actual witness, even while it changes.

For exceptional S, all old roots with anchor color in A minus S avoid the pair, and all completed new roots with anchor color in S avoid it. Their outside edges do not contain any anchor owner in S or pi(S). These identities supply the entire lower-witness transfer.

## 4. Universal lower constructor and all-color reserves

Singleton(C) forces vc(Gamma_a)>=2, hence two distinct actual edge types per color. Choose one original seed copy q_a and a distinct original reserve copy r_a in each of ALL FOUR colors. Choices exist independently of multiplicity. Retain all reserves untouched throughout the seed phase.

Choose T subset A meeting every exceptional S; T=A always works, and T=empty works when E_pi is empty. Complete the selected seeds for colors T first, in fixed color order. Within a copy add all destination-only labels of this column, then delete all source-only labels, in palette order.

Fix exceptional S. Until its first selected seed color in S completes, an untouched old reserve in A minus S protects it, including during that seed's edits. Such a reserve exists because reserves were retained in ALL colors; no complement-transversal deduction is needed. After the seed completes, it is an actual new witness and remains fixed through every remaining edit in this column. The same reserves/seeds can protect multiple obligations at once.

After all selected seeds complete, process all remaining original copies in any fixed order, including other copies of seed types and every reserve. Selected seed copies remain at destination, so each exceptional pair keeps a witness. Nonexceptional pairs retain their actual union witnesses irrespective of this order. Thus every physical pair is missed by an actual root after every primitive, proving tau>=3.

Floors are preserved: during additions the root contains its old column endpoint of size N_Q; during deletions its new endpoint of size N_Q. All primitives are absent additions/present deletions in the fixed palette. A zero-edit copy advances without a fictitious move. Finite seed/copy/incidence lists give an eligible next primitive whenever edits remain and terminate a column.

At a completed column, group sizes, actual type/copy identities, colored guard and original floors renew exactly. A later unresolved column still has source owners. Repeat with its own physical labels and the SAME actual seeds/reserves. Finite unresolved-column count strictly decreases at column completion. Ultimately every original labelled root equals C_Q, including fixed padding. This is full completion, not a supplied safe prefix.

## 5. Universal direct upper protection with an inactive column

If t>=2, choose any column g different from active h. It has fixed owners throughout active-column repair: identity if unresolved, pi if already completed. For each a in A choose the unique physical label in column g whose current owner is a. Their four-set hits every root at both column endpoints and through every intermediate edit because every root retains all inactive-column incidences.

Even an active seed/reserve root therefore has an actual upper hit. Together with Section4 this proves direct {3,4} on the SAME schedule, preserving global minimum. On the next column choose a different inactive column, whose current owner map remains a permutation. Witness switches introduce no incidence edit.

This explains why t>=2 can conceal the moving-cover challenge. No inactive-column argument is used for the t=1 controls below.

## 6. Empty exceptional family: an interleaved union bridge

When E_pi is empty, EVERY physical pair has an actual avoiding column-union root. Add every missing destination incidence across all original roots before deleting any source-only incidence. Every root stays within its column union, so all actual pair witnesses persist, including at the simultaneous full-union state.

During additions all roots contain their source column endpoints. K0={x_(a,h):a in A} hits all of them. At the full-union boundary, every root contains its destination endpoint. Thereafter use K1={x_(pi^{-1}(a),h):a in A}, whose new owner set is A. It hits all roots during deletions. Original floors and finite next primitives follow from endpoint containment.

Thus moving upper protection works without a common four-cover and without whole-root completion ordering. Each endpoint-differing incidence toggles once. This theorem covers calibration pi=(0 4): no two-start footprint can be A because the only nonfixed owners are 0 and4, while starts outside that pair have singleton owner footprints.

In that calibration, singleton(C) forces some color0 edge avoiding4, because vc(Gamma_0)>=2. Its type lies in BOTH U and V. Therefore the source/destination TWO-cover complete-root-block relay is impossible for these endpoint cover identities, despite our interleaved union bridge being legal and minimum. This is a precise METHOD obstruction and positive remedy, not native disconnection, nor an obstruction to every cover relay.

## 7. Derived joint relay when exceptions coexist

Assume R1,R2. Take T=B (or any subset of B meeting every exceptional S). Select seeds in these colors and distinct reserves in all four colors as in Section4.

A seed type with color a in B hits BOTH physical covers at BOTH column endpoints:
- K0 hits the source because a in A, and the destination because a in pi(A);
- K1 hits the source because a in pi^{-1}(A), and the destination because a in A.
Therefore no selected seed is in U or V. Its outside edge may be arbitrary; only its actual anchor incidence is used for these hits.

Derive the complete original-copy order:
1. selected seed copies, leaving all selected reserves untouched;
2. ALL original copies of types in U;
3. every remaining original copy in fixed order.

R2 ensures no U type is a V type, so ALL U copies complete strictly before the first V copy starts. If V is empty there is no switch requirement. This is the two-cover case of X51, applied to ORIGINAL copy identities; seed copies can be separated from the other copies of their types because neither endpoint of their type is an upper exception.

Use K0 until the first V copy would start. Before that point no completed or active root is a destination exception to K0, while every old root is source-covered by K0. It hits BOTH endpoints of each active copy and all simultaneously old/new copies.

At that first V copy, ALL U copies are already complete. Switch the witness to K1. Every completed root is destination-covered by K1; every remaining or active root is not in U and is therefore source-covered too. K1 hits BOTH endpoints of every active copy, every old/new copy coexisting in its type, and every endpoint-containing primitive support. If V is empty, K0 works throughout. If U is empty the switch may occur immediately after seeds or at the first V.

Lower protection is exactly Section4 on this SAME order: seeds first under untouched all-color reserves, then installed new seeds protecting all remaining changes. Actual common witnesses persist. Upper and lower orders are not chosen independently.

No supplied acyclic graph or manual root order is assumed. The actual anchor intersections produce seeds outside BOTH exception families; actual R2 separates all upper exceptions; these facts derive the precedence and its eligible next copy. All finite next-edit/floor/renewal/minimum proofs from Section4 remain.

A subset pi(A) union pi^{-1}(A) implies R2: the anchor of any type belongs to at least one of these images, so that type cannot avoid both. Actual R2 may hold even when this role condition fails, through actual outside incidences.

## 8. Proposed mixed controls, all colored carriers

All permutations below are prescribed on fixed labels with unlisted roles fixed, before constructing any repair.

(a) pi=(0 1)(2 3): X58 calibration. E_pi has four cross-block pairs, B=A, U=V=empty. Section7 reproduces the shared seed/reserve repair and fixed cover.

(b) pi=(0 4): E_pi empty. Section6 supplies the interleaved minimum bridge, and its U/V overlap demonstrates the stated whole-root two-cover limitation.

(c) pi=(0 1 2 3 4 5).
pi(A)={1,2,3,4}; pi^{-1}(A)={0,1,2,5}; B={1,2}.
Only starts0,1,2 have both old/new owners in A. Their two-start footprints give E_pi={{0,2}}. T={2} meets it.
U consists of color3 types whose outside edge avoids5.
V consists of color0 types whose outside edge avoids4.
They are disjoint; seed color2 lies outside both. Process seed2, ALL U copies, then remaining copies. This works for EVERY colored graph family satisfying(C), with arbitrary original positive copies.

(d) pi=(0 1)(2 3 4 5).
pi(A)={0,1,3,4}; pi^{-1}(A)={0,1,2,5}; B={0,1}.
Eligible starts are0,1,2; E_pi={{0,2},{1,2}}. This family is NOT complement-closed.
U consists of color3 types with edges avoiding5.
V consists of color2 types with edges avoiding4.
T={0,1} meets both exceptional pairs. Distinct all-color reserves protect both until their seed completes, then seeds0,1 jointly protect them. ALL U copies precede V. The SAME schedule has moving upper protection and two overlapping lower obligations.

For (c),(d), singleton(C) guarantees U,V are nonempty: a single outside vertex5 cannot cover Gamma_3, and4 cannot cover Gamma_0 or Gamma_2 respectively. Thus the relay is substantive on every valid carrier; outside favorable labeling is unnecessary.

At t=1/no padding, every source group is a singleton, and the unique physical four-cover is K0 indexed by A; destination's unique four-cover is K1 indexed by pi^{-1}(A). They differ for (b),(c),(d). No single four-set hits both endpoints. Our constructed paths use exactly TWO cover identities in these singleton controls: two are necessary by unique endpoints and two suffice above. This count is for the proved paths, and also a minimum count among paths admitting four-cover witnesses. It is not minimum number of primitive edits by itself; that is proved separately.

## 9. Structural carrier variation and precise count controls

No diagnostic enumeration was performed. The constructions apply to ALL colored carriers satisfying(C), not just private edges.

Private control: for every m>=20 use X58's eight private pairwise-disjoint outside edges
Gamma_0={{8,10},{9,12}},
Gamma_1={{4,6},{11,14}},
Gamma_2={{5,7},{13,16}},
Gamma_3={{15,18},{17,m-1}}.
For every J, the union is a matching of 2|J| edges, so its cover number is 2|J|>|J|.

Shared control: for every m>=14 put ALL four Gamma_a equal to the same five-edge outside matching
{{4,5},{6,7},{8,9},{10,11},{12,13}}.
Its cover number is five, hence(C) for all |J|<=4. There are twenty distinct color/edge types; the SAME outside edge participates in several colors. The proofs account for these actual overlaps, not independent capacity per pair. Either control permits arbitrary unequal positive labelled copies and floors.

For t=1, no padding and one copy/type, every root is a saturated triple. For the private carrier:
- control(c) has four types containing outside4 or5 and four containing neither. The former have |Q intersect pi^{-1}(Q)|=1 and difference4; the latter difference6. No edge containing5 is in color3 and no edge containing4 in color0. Thus exact global length is 4*4+4*6=40.
- control(d) has four color0/1 types with no moved outside labels, difference2; two color2 types and one color3 type outside the moved outside roles have difference4; the remaining color3 type contains5 and has difference6. Thus exact global length is 4*2+3*4+6=26.
These counts scale by t with one copy/type; arbitrary copies use the weighted formula. They are analytical identities, not benchmarks.

For controls(c),(d), any exceptional physical pair hits ALL endpoint unions. No singleton hits all unions, since its footprint has size<=2 and differs from A, providing an actual avoiding type. Hence actual endpoint-union transversal is EXACT TWO. All root types in these private mixed controls change; there is no unchanged background root. The direct path is therefore protected by the changing actual witness arrangement, not a permanent union three-guard.

## 10. Minimum, continuation, reuse and inherited boundaries

In column h, selected label x_(s,h) belongs to Q at source iff s in Q and at destination iff s in pi^{-1}(Q). Every listed construction toggles exactly differing incidences once; all common incidences, padding and other columns are fixed during that column. Thus total count equals the OUTER endpoint Hamming distance L. Any native path requires at least that many single-incidence changes, proving global minimum. This includes X59L's LOWER minimum and each stated direct-band minimum, but not the maximum-layer-converted path.

Finite column/copy/incidence lists supply a next edit when unfinished; the pending scheduled edit count decreases at primitives, with zero-edit copies skipped. Completed columns renew exact-four role partitions, original floors and actual seed/reserve/relay eligibility. No label, copy or guard resource is consumed. Hence all t columns finish at original exact labelled destinations.

Any finite succession of qualifying prescribed legs can be repaired by recomputing its actual pi, exceptional family and upper conditions at its exact restored boundary. Counts are minimum PER LEG; such concatenation need not be globally shortest between its outermost ends. No arbitrary unfinished safe-prefix completion is claimed.

For universal SINGLE-column pi beyond Sections6/7, Section4 supplies a COMPLETE lower path between original exact-four ends. Only then does accepted maximum-layer A give some band path to the exact destination. Inexact waypoint preservation, original schedule and minimum length are not guaranteed by this conversion.

Dependencies: X58 supplies colored footprint/endpoints and seed/reserve ideas; X51 supplies the copy-coexistence discipline and two-cover exception interface; X52 supplies the transferring-lower/moving-upper comparison. The actual joint construction here is proved directly. Applicable symmetry connectivity is already known: this is a direct prescribed minimum repair mechanism, not a new native connectivity classification. No frozen source is rewritten or recertified.

## 11. Rejecting boundaries and next obligation

The certificates reject losing a last old witness before its seed completes, a fictitious missed root, a cover missing an active endpoint or coexisting old copy, deletion below a labelled floor, endpoint relabeling and repeated toggles under a minimum claim. No executed numerical rejection suite is claimed.

R1 failure rejects the chosen common-hit seed-color certificate; R2 failure rejects this endpoint-two-cover whole-copy relay, as control(b) shows. Neither rejects other seeds, extra covers, partial-root interleaving or native paths. The supplied controls establish absence of a COMMON endpoint cover and presence of a moving-cover path, not impossibility of all whole-root orders.

The remaining analytical objective is direct-minimum single-column repair with E_pi nonempty when the compatible common-hit anchor set fails to meet it or actual U,V overlap. Derive another relay/interleaving or characterize the chosen-method obstruction. General lower renewal and t>=2 direct minimum are now complete in this colored class.

No numerical execution, new implementation, fixture, benchmark, workflow, integration merge, numbered certification or physical claim. v16.54/v16.55 and all original evidence remain preserved. Separate efficiency work remains unstarted.
