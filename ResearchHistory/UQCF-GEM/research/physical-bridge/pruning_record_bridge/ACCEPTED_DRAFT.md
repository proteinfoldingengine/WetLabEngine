# Same-union pruning and protected incidence records

Date: 2026-10-11. Source parent: 95d0b2381f6006fb30c5fa7cd76ce80696bb3b2d.
Status: analytical candidate awaiting independent review. No numerical campaign, physical mechanism or numbered-stage certification is claimed.

## Question and status of the restriction

The previous native-control boundary permits every reversible native incidence path inside a total-unit band. Ordinary writable controls cannot then certify an original source bit from a terminal state. This probe examines a different, already defined mathematical relation: same-union pruning of indexed retained views (v16.25 and v16.26).

We first identify its exact representation on the nested-support carrier. We do NOT infer that every native toggle is physically oriented this way, or that a physical system selects these refinements. Same-union pruning is an inherited allowed comparison, not an inherited law selecting actual successive states. Restricting the considered histories to it is an explicit conditional premise. The phrase 'time is pruning' does not supply a transition selector, force a deletion, or identify every abstract tree with physically accessible records.

The result below has three parts: an exact representation and reachability criterion; a pruning-protected conditional record with an initially identical memory; and a limit on erasing the original source distinctions while retaining a universally sound positive record. This is a separately typed mathematical consumer, not satisfaction of the C3 restored-marker gate or its swapped-root test.

## 1. Literal transposition of the same supplied incidence carrier

Let T be a fixed finite rooted tree, P a fixed finite nonempty indexed palette, and S a native support state: S_root=P, every S_v is nonempty, and S_child is a subset of S_parent. For each label i define

    Y_i = {v in T : i belongs to S_v}.

Every Y_i contains the root and is prefix closed. Nonemptiness of every S_v says precisely that the indexed views cover T. Conversely, a P-indexed family of root-containing prefix-closed subsets Y_i whose union is T defines S_v={i:v in Y_i}; this is nonempty, nested and has fixed root P. These maps are mutually inverse. Redundant or identical indexed views are allowed and remain distinct indices; root-only views are allowed.

At an internal v, a label set I intersects every immediate child support iff the views indexed by I jointly contain every immediate child. Thus the native hitting number h_v equals the inherited local child-cover number tau_v. This identifies the same labeled incidence data, not just equal dimensions or a fitted relabeling. All maps commute with transport of the fixed tree and view indices.

Deleting incidence (v,i), v nonroot, preserves nesting iff no child of v contains i; in a prefix-closed view this means v is a leaf of Y_i. It preserves support nonemptiness iff another view still contains v. Thus native single-incidence deletion is exactly atomic leaf pruning of one view with the same union T. This is v16.26's atomic refinement on the same supplied carrier. No new palette, vertex, metric or comparison target is introduced.

This is a mathematical representation equivalence. It does not construct the actual Genesis/source-record binding of a physical tree, make all labeled incidences observer-accessible, or transport extensive source amounts into a physical record. Those are distinct obligations.

## 2. Exact directed reachability from an exact preparation

For two support states E and S, write E<=S when E_v is a subset of S_v at every vertex. Fix a feasible target profile q=h(S) at every internal vertex and a nonnegative integer band budget B. Let

    D_q(F) = sum over internal v of |h_v(F)-q_v|.

Allow only native deletions, with every intermediate state satisfying D_q<=B. Zero-length paths are permitted. There is no compulsory completion or stopping rule.

**Endpoint criterion.** A native state E is reachable from S by such a path iff E<=S and D_q(E)<=B.

Necessity follows from deletion-only evolution and the endpoint band. For sufficiency, keep E fixed and repeatedly choose a deepest incidence to remove from F\E: equivalently, prune a leaf of some current Y_i\Z_i, where Z is the view representation of E. Prefix closure is preserved because no retained E descendant can lie below a vertex absent from E's corresponding view. Some E-view still contains each removed vertex because E covers T. Hence each step preserves nonemptiness and the union. Finite repetition reaches E, exactly as in v16.26 atomic factorization.

Shrinking child supports cannot decrease any h_v: a hitting set for the smaller supports also hits the larger ones. Therefore throughout this factorization

    q_v = h_v(S) <= h_v(F) <= h_v(E).

All deviations have the same nonnegative sign. Summing gives D_q(F)<=D_q(E)<=B. This proves the band condition at every primitive, not just at the endpoint. The argument works for every finite tree arity; it does not extend the reversible arity-2/3/4 normalization theorem, which is not used here. Its ingredients are inherited refinement monotonicity and atomic factorization.

There are exactly sum_v |S_v\E_v| actual edits on any deletion-only path from S to E, since no incidence can be reinserted. In particular exact-to-exact pruning paths stay exact throughout. Excursions cannot rise and then fall during pure pruning.

## 3. Exact criterion and cost for deleting a designated incidence

Fix a nonroot vertex v and a label a initially in S_v. Let Desc(v) include v. Form C by removing a from every support in Desc(v), leaving all other incidences unchanged. Nesting forces this entire removal whenever a is absent at v.

**Pruning-cone criterion.** Some band-admitted deletion path reaches a state with a absent at v iff:

1. No vertex u in Desc(v) has initial support S_u={a}; and
2. D_q(C)<=B.

The first condition makes C nonempty everywhere. Nesting and the fixed root are then preserved, since v is nonroot and all affected descendants lose the same label. If both conditions hold, the endpoint criterion reaches C. Conversely, any endpoint E with a absent at v satisfies E<=C by nesting. Such an E cannot exist with an initial singleton {a} anywhere below v. Otherwise coordinatewise hitting-number monotonicity yields D_q(C)<=D_q(E)<=B. This proves necessity as well.

When attainable, the minimum number of actual deletions to this first absence is

    m(v,a) = number of u in Desc(v) with a in S_u.

Every one of these incidences must be deleted, giving the lower bound. Delete them in descendant-before-ancestor order, with (v,a) last, to attain C in exactly m(v,a) moves. No other incidence is removed. This is a global minimum within the declared deletion-only class, not a minimum in the reversible native graph or a physical duration.

For two exact preparations with the same T,P,q and an initially present designated incidence in both, this supplies an exact sound-positive test: a nonvacuous positive record 'a absent at v' is universally sound for original source one iff this criterion holds for S_1 and fails for S_0. Positivity persists under every subsequent legal deletion because deleted incidences cannot return. This does not imply that any path actually reaches positivity.

## 4. Five-vertex conditional record, with no exclusive supplied script

Use P={a,b,c}, rooted tree o with children u,C, and u with leaves r,w. Fix the same reference identities and q_o=2, q_u=1 in both preparations. The source bit is represented by the supplied singleton at r; the proposed memory is the initially identical support at u.

| Vertex | Source zero | Source one |
|---|---|---|
| o | {a,b,c} | {a,b,c} |
| u | {a,b} | {a,b} |
| r | {a} | {b} |
| w | {a,b} | {a,b} |
| C | {c} | {c} |

Both preparations are nonempty and nested. At o, u and C are disjoint, giving h_o=2. At u, w intersects the singleton r, giving h_u=1. Use B=1, the same numerical total band as the preceding native-control discussion.

For source one, the path -a(w), then -a(u), keeps (h_o,h_u)=(2,1) at all three states. The cone endpoint has u=r=w={b}, C={c}. The record R=1[a absent at u] begins at zero and becomes one after two actual deletions. It remains one under every subsequent pruning history. Two is optimal in the declared deletion class because both (w,a) and (u,a) must disappear.

For source zero, r={a} cannot change under native deletion: deleting its only incidence would violate nonemptiness. Nesting therefore forces a to remain in u on EVERY deletion history, irrespective of ordering or other allowed changes. R can never become one. In the cone criterion, source zero fails its singleton condition and source one passes with D_q(C)=0.

The ordering needed for the successful pair follows from the native child-inclusion rule, not an externally supplied exclusive five-step script. All legal band-limited pruning paths are admitted, and arbitrary stopping is allowed. There are also unsuccessful paths: source one may first delete b(w), giving h_u=2 and w={a}; this remains inside B=1 but the surviving singleton at w then prevents a's deletion at u. No universal success, probability, fairness, actual outcome or automatic commitment follows.

The singleton source is protected here by nonemptiness AND the pruning-only premise. It is not an independently inserted immutable nonroot anchor within the reversible grammar. If additions are again admitted, it is mutable: source zero can take +b(r), -a(r), -a(w), -a(u), with all targets exact, and reach the same full positive endpoint. This explicit four-edit counterhistory reinstates the previous boundary. It is a hand-derived example, not a new numerical run.

The output R is a mathematical projection, not an earned observer read. The positive endpoint and both initial preparations have the same h profile, so those profile values alone do not read the record. The initial memory at u is common; the complete initial preparations differ at r. No physical readout, request resolution or source initialization has been derived. This is a persistent conditional record relation under actual same-union pruning, not a completed physical sensor.

## 5. Why pruning-only sound records cannot erase every original source distinction

Let S_0 and S_1 be arbitrary exact native preparations with common T,P,q, not necessarily comparable. Use the same budget B and the same endpoint readout R. By the endpoint criterion, a native band endpoint E is reachable from both exactly when E<=S_0 and E<=S_1.

Consequently, if E is reachable from S_1 but not from S_0, then E contains at least one incidence belonging initially to S_1 but not S_0. For if every incidence of E also belonged to S_0, E<=S_0 and the criterion would make it reachable from S_0. Thus every positive endpoint of a universally sound, nonvacuous source-one readout must retain at least one originally source-one-exclusive incidence at its ORIGINAL coordinate.

This is a necessary condition, not a sufficiency statement for any supplied projection. It applies even if all initial memory coordinates are identical and the reported memory is elsewhere: some original distinguishing incidence must still survive in the full state. Pruning cannot relocate all original source differences into initially common coordinates and then erase them all while preserving such universal historical soundness. A same-union endpoint that erases all those differences is also reachable from source zero.

The example retains (r,b), which was absent in source zero. It therefore respects this limit. It achieves persistence without source erasure. This differs from the five-edit conversion's source-erasing record, whose soundness depends on an exclusive protocol and whose route includes additions. The old conversion is not claimed achievable under pruning alone.

## 6. What has changed, and what is still supplied

The mathematical advance in this probe is an exact conditional classification: the directed reachable set, the criterion and optimal deletion cost for a specified missing incidence, and the necessary retained-source distinction. The two-edit witness exhibits a record protected against ALL histories in this pruning class, not merely against departures from one script. These are direct consequences/applications of inherited refinement structure; no novelty is claimed for general order theory, monotonicity, or the incidence transposition.

This answers a limited re-entry question left by the reversible control boundary: an inherited mathematical history restriction can protect a conditional record, and the point at which the restriction matters is explicit. It does not earn that restriction as a physical update law. A formal comparison relation does not enforce itself. The carrier, source preparation, reference identities, profile/budget and prospective readout are supplied. Neither an inaccessible verifier nor a terminal flag is substituted for enforcement or access.

Disposition sought: CONDITIONAL_PRUNING_RECORD_BRIDGE; PHYSICAL_REALIZATION_AND_ACCESS_OPEN. There is no new numbered scientific campaign, new scientific test count, Gemini review, main merge or CLOSED/CERTIFIED status. The prior 527 scientific tests are historical record-conversion evidence, not verification of this note, and are not rerun or increased here.

The next physical obligation is to justify that a real retained-input interaction lies in this pruning relation and to derive an accessible use of its retained record. Merely choosing deletion-only dynamics because the example works would add the missing premise. A new numerical campaign cannot establish that missing physical premise; if a separate verification campaign for this scoped mathematical result is proposed, its universe and controls must first be prospectively frozen. Broad C3/C4-C6, source correspondence and physical derivation remain OPEN. Ordered pruning supplies no fundamental duration, inserted geometry, force or dark-matter primitive.

## Immutable dependencies

source_readbacks.json binds exact source bytes at the parent. Essential mathematical sources are v16.24 TYPE_AND_PROOF (indexed views and child-cover number), v16.25 TYPE_AND_PROOF (coordinatewise monotonicity and actual retained subviews), v16.26 TYPE_AND_PROOF (same-union atomic factorization), and v16.53 NATIVE_ADMISSIBILITY (support carrier and toggles). The v16.32 noninjectivity result, native-control boundary, record-conversion result and physical-frontier/gate sources constrain interpretation. The inherited source documents' own historical prospective/closure status is retained; this note does not recertify earlier stages.
