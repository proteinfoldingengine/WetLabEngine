# Post-A12: exact cover transfer and a retained-input handover policy

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT WITH COMPLETE ARGUMENTS BELOW; repository audit/readback tracked separately.
Attribution: ChatGPT author-side mathematical work. No independent peer review, formal proof-assistant certificate, numerical verification or physical validation is claimed.
Scope freeze: [POST_A12_HANDOVER_SCOPE.md](https://github.com/proteinfoldingengine/WetLabEngine/blob/906f38894df287944a6742ab2f3685e39976b7dc/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_HANDOVER_SCOPE.md), blob dcb9f4e654b1cf3baec3bbb4391c1661b25a470b.

This result concerns the prepared, fixed-residual, target-four class in that scope. It does not factor the whole A11.X2 arbitrary-endpoint construction, and it is not A12.6. The earlier A12 closeout and all certified sources remain unchanged.

## 1. Sources, carrier and retained record

The inherited six edits are Section 4 of [A11_RENEWABLE_SINGLETON_ANCHORS.md](https://github.com/proteinfoldingengine/WetLabEngine/blob/1cd572d2e90ba3880dc5598d260c14e8a92acc5c/ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_RENEWABLE_SINGLETON_ANCHORS.md), blob f4c295a21a545be746def65acb4fe38c781e3f14. That proof supplies a lower-band path and later uses maximum-layer removal. We derive the direct upper condition here; we do not assume the conversion preserves the six edits.

The certificate definitions are compatible with [A12 R1 Sections 1 and 4-5](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2085eb1fdca0bbe754743e6bd74ef6fda6bdbef/ResearchHistory/UQCF-GEM/research/physical-bridge/A12_CONSOLIDATED_PROOF_AND_AUDIT.md), blob f670e9a6687aec49b18429655285f937404e1a36. The proofs below use actual transversal sets directly, rather than finite A12 checks or an external verdict as a premise.

Let P be a finite ordered palette, k=card(P)>=4. Choose four distinct labelled root slots alpha,beta,i,j. The anchor floors are f_alpha=f_beta=1. Guard floors are fixed positive integers at most k-2. Every other labelled root belongs to a residual family R, which remains UNCHANGED throughout this item; its nonempty supports satisfy their original positive floors. An empty residual family is allowed and has transversal number zero.

For distinct u,v in P, the prepared state E_R(u,v) consists of anchors {u},{v}, both guards P minus {u,v}, and R. Different ordered pairs assign labels to the same alpha,beta slots, not to permuted roots. Its target E_R(u*,v*) preserves every residual labelled support and prescribes both final guard supports exactly. Initial and target states must have 3<=tau<=4.

For each unordered two-label set U define

    F_R(U)=1 iff some H subset P of size at most 4
                       hits every residual root,
                       contains U,
                       and has at least one label outside U.

It is a Boolean projection of the residual upper-cover field B_R(H). Once initialized correctly, it is stored, not queried from the hidden roots anew. Initialization may need global information; no efficient or observer-accessible initialization is proved.

Allowed policy data: P with its supplied order; distinguished slot identities and their immutable floors; F_R; current and target ordered anchor pairs; and phase memory identifying the moving anchor, its old/new labels, guard order (i,j) and phase. Intermediate controlled supports are defined by the six-edit table below. Neither the individual residual supports nor a full incidence-syntax table is supplied after initialization. The policy is promised that R remains unchanged and valid. It does not verify hidden residual modifications or invalid floors.

## 2. Exact cover-family identity for the six edits

At a prepared boundary let the changing anchor be {p}, the other anchor {w}, and choose t outside {p,w}. Let

    U={p,w}, U'={t,w}, G=P minus U, G'=P minus U'.

Write E_s for the state after s edits. R and the other anchor {w} are fixed. The changing anchor and guards are:

| s | Edit producing E_s | Changing anchor | Guard i | Guard j |
| --- | --- | --- | --- | --- |
| 0 | Start | {p} | G | G |
| 1 | Add p at j | {p} | G | G union {p} |
| 2 | Delete t at j | {p} | G | G' |
| 3 | Add t at anchor | {p,t} | G | G' |
| 4 | Delete p at anchor | {t} | G | G' |
| 5 | Add p at i | {t} | G union {p} | G' |
| 6 | Delete t at i | {t} | G' | G' |

All syntax is valid: p is absent from G, t belongs to G, and p,t are distinct. The changing anchor always has size one or two. Each guard has size k-2 or k-1, hence every original floor holds, including guard floors equal to k-2. The other roots never change.

Let T_s denote the family of ALL transversals H subset P of E_s, without imposing a size cutoff.

**Cover-transfer lemma.**

    T_0=T_1=T_2;
    T_3=T_0 union T_6;
    T_4=T_5=T_6.

Proof of the first equality: at phases 0,1,2 the anchors force p,w. Guard i requires an intersection with G. At phase 0 guard j repeats this same requirement; at phases 1 and 2 it contains p and is automatically hit by the forced p. The condition on R is the same at each phase. These are exactly the same transversal tests.

Proof of the last equality: at phases 4,5,6 the anchors force t,w. Guard j requires an intersection with G'. At phases 4 and 5 guard i contains t and is automatically hit; at phase 6 it repeats G'. Again R is unchanged.

Proof of the middle equality: at phase 3 a cover must contain w and at least one of p,t, and must hit both G and G'. If it contains p, G' is automatically hit and the remaining conditions are precisely those of T_0. If it contains t, G is automatically hit and the remaining conditions are precisely those of T_6. Conversely every T_0 cover hits G' through p and every T_6 cover hits G through t, so each is a phase-3 cover. Covers containing both p and t cause no exception: they may belong to both families. This proves the union identity.

The identity is about actual sets of covers, not just their counts. In particular for the size-at-most-four indicator C, C_3(H)=C_0(H) OR C_6(H). It is not a conservation equation for C or N4.

**Exact hitting-number corollary.** Put a=tau(E_0), b=tau(E_6). Since every support is nonempty, P is a cover and both values are finite. Taking minima of the displayed families gives

    (tau(E_0),...,tau(E_6))=(a,a,a,min(a,b),b,b,b).

Every prepared state requires its two anchor labels and at least one label in their complementary guard, so a,b>=3. The same is therefore true at every intermediate phase. This also reproves the lower-band claim for this prepared target-four handover without any conversion theorem.

Consequently ALL seven states lie in [3,4] if and only if BOTH prepared endpoint states lie in [3,4]. No assumption on the number or shape of residual roots is needed beyond the fixed valid carrier.

## 3. One-step sufficiency and an updateable record

For a prepared state, H hits both anchors and both guards exactly when U subset H and H minus U is nonempty. Therefore

    3<=tau(E_R(u,v))<=4 iff F_R({u,v})=1.

Together with the cover-transfer lemma, this proves a full handover is band-safe exactly when F_R(U)=F_R(U')=1. All syntax/floor information needed for the prescribed edits is already determined by the table and immutable floors.

There is a sharper next-move statement. From a protected prepared start, edits 1,2,3 are individually legal even when F_R(U')=0: their hitting numbers are a,a,min(a,b). Edit 4 is legal exactly when F_R(U')=1. If edit 4 is legal, edits 5,6 preserve its band status. The policy must therefore test the new endpoint bit BEFORE committing to the handover, rather than confuse a legal prefix with guaranteed completion.

At each edit the phase increments and the controlled supports follow the explicit table. F_R itself does not change, since R does not change. On completion update the ordered anchor pair and reset phase to zero; the guards now have the complementary supports required at the next boundary. This update uses no information about individual residual roots.

Thus the retained input suffices for (i) deciding the legality of a prescribed handover and its next edit, (ii) updating its own finite record, and (iii) renewing the same record format. This does NOT reconstruct arbitrary W multiplicities, the entire global C field, or arbitrary receiving-root margins. It provides the information required for this particular policy and its upper-band test; the lower guard is structural.

F_R has one Boolean coordinate per unordered pair, at most binomial(k,2) bits. Carrier and phase metadata are additional. This is independent of the number of residual supports, but not constant space as k grows and not an assertion that every instance is shorter than its full incidence description. Nor is F_R proved recoverable from current GLOBAL W/C alone: it was defined from the residual family.

## 4. Exact destination reachability for this policy model

Define a finite graph Gamma_R from F_R. Its vertices are the ordered pairs (u,v), u!=v, with F_R({u,v})=1. Two vertices are joined when they differ in exactly one coordinate and the replacement label is outside the old unordered pair. Each edge corresponds to one complete six-edit handover, with the appropriate anchor designated as changing. It can be traversed in either direction by the same construction with old/new roles exchanged.

**Retained-input scheduling theorem.** A finite concatenation of these complete handovers connects prepared source E_R(u,v) to prepared target E_R(u*,v*) inside the protected band if and only if the two ordered pairs lie in the same connected component of Gamma_R.

Sufficiency: lift every graph edge to its six edits. Both endpoint bits are one, so Section 2 keeps every primitive in the band and every floor intact. Each macro ends in precisely the prepared state represented by its next vertex. R is never edited. The final anchors, guards and all residual labelled roots therefore equal the exact prescribed target.

Necessity: the boundary of every successful complete handover is a prepared state, and Section 2 requires its endpoint bits to be one. Consecutive boundaries differ in one permitted coordinate. Hence any such repair concatenation projects to a graph path. This necessity is for COMPLETE CONCATENATIONS of the prescribed handover; it does not cover arbitrary active-root edits, interleaved handovers, or residual-root changes.

A deterministic terminating selection rule uses only the stored table. Calculate the minimum remaining number d(z) of graph edges from each reachable vertex z to the target. If the source is unreachable, report this policy restriction rather than declare the native destination impossible. Otherwise select a neighbor with d one smaller, using the supplied palette/slot ordering only to settle ties, and perform its six edits. This is a mathematical rule, not an executed graph search or a claimed autonomous physical selection law.

For a nonterminal boundary with d=d(z), phases s=0,...,5 have the nonnegative integer rank 6d-s. Each primitive lowers it by one; after edit 6 the new boundary has rank 6(d-1). Thus the procedure cannot stall or cycle. A simple graph path uses at most card(V(Gamma_R))-1 macros, so at most 6(k(k-1)-1) primitives suffice whenever source and target are connected. This is a nonoptimal analytical bound, not a benchmark.

The graph and existence statements are covariant under transported root/label permutations. A deterministic tie-break additionally transports the supplied order; arbitrary label-order choices are bookkeeping, not an intrinsic physical preference. The graph ranks count remaining handovers and introduce no physical geometry or fundamental time.

## 5. A sufficient class where every prepared target is reachable

The graph criterion is not left solely as a reformulation of the scheduling problem.

**Residual-three sufficient theorem.** If the fixed residual family has a transversal of size at most three, EVERY two protected prepared states are connected by the retained-input handover rule. A route of at most six handovers, hence at most 36 incidence edits, exists.

Proof. Extend a residual transversal, if needed, to a three-label set T={h1,h2,h3} subset P. This is possible since k>=4 and a superset of a transversal still hits R. For any two-label U intersecting T, the set H=T union U hits R, contains U, has size at most four, and has a label outside U because T has size three. Thus F_R(U)=1 whenever U intersects T.

Every feasible ordered pair (u,v) can reach the canonical pair (h1,h2) in at most three permitted coordinate changes:

- If v!=h1, change the first coordinate to h1, then the second to h2, omitting any change already satisfied. Every new pair contains h1.
- If v=h1 and u!=h2, change the second coordinate to h2, then the first to h1. Both changes use a label outside the current pair, and each new pair contains h1 or h2.
- If (u,v)=(h2,h1), use (h3,h1), then (h3,h2), then (h1,h2). All three intermediate pairs meet T and have distinct coordinates.

All these pairs are graph vertices and all listed transitions are edges. Do the same for the target and reverse its graph route. This yields at most six edges between any two feasible pairs. Lifting them proves the stated primitive bound and exact endpoint restoration.

The proof uses T as an existence witness, but the policy does not need an unrecorded oracle supplying T or reading R: its graph and shortest-edge ranking are computed from F_R alone. The witness proves the graph is connected and its needed routes have the asserted bound.

This is a sufficient condition, not a necessary one. For example, k=4 with four singleton residual roots has tau(R)=4, yet P is a four-cover containing every pair and meeting its complement, so F_R is identically one and the handover graph is connected. The new result does not classify every residual family.

## 6. Refutation: direct X2 handovers do not always connect valid endpoints

Let P be the disjoint union A union B, where

    A={a1,a2,a3,a4}, B={b1,b2,b3,b4}.

Use as residual roots ALL sixteen two-element sets {a,b} with a in A and b in B, each in its own fixed labelled slot. All original floors, including the four controlled slots, may be one. This is a k=8, twenty-root carrier satisfying the frozen domain.

Any residual transversal H contains all of A or all of B. Indeed, if a is absent from H and b is absent from H, root {a,b} is missed. Conversely containing all of either block hits every residual root. Hence tau(R)=4 and the ONLY residual covers of size at most four are A and B.

It follows that

    F_R(U)=1 iff U subset A OR U subset B.

The prepared states E_R(a1,a2) and E_R(b1,b2) both have exact tau=4: their respective block covers hit the anchors and complementary guards, while R forces the lower bound four. Both are admissible exact labelled endpoints.

Nevertheless Gamma_R separates pairs lying wholly in A from pairs lying wholly in B. Changing only one coordinate cannot cross between these sets without producing a mixed pair, whose F_R bit is zero. No concatenation of the prescribed band-safe handovers can connect these endpoints. This is an actual disconnected-policy obstruction, not merely two differently chosen successful schedules.

An explicit illegal continuation illustrates the upper-bound danger: starting at E_R(a1,a2), replace a2 by b1 while a1 stays fixed. The prepared new pair is mixed. A cover must contain a full block plus the missing anchor label from the other block, so its hitting number is at least five; A union {b1} is a five-cover also hitting the guards, so it is exactly five. The seven phases therefore have hitting numbers

    (4,4,4,4,5,5,5).

The first three edits are safe and the fourth fails. Endpoint preflight, not a prefix-only test, detects this.

Crucial rejecting interpretation: the obstruction does NOT refute X2 or even prove failure of all policies keeping R fixed. Here a different active-root path is immediate. First expand every controlled support to the union of its source and target support. The old block A remains a cover and R keeps tau>=4. Once all are expanded, the new block B covers them all; delete source-only incidences until the exact target is reached. B remains a cover, R still forces tau>=4, and union replacement preserves floors. Thus this alternative native path has tau=4 throughout. It is not a concatenation of the prescribed six-edit macros. The negative theorem is deliberately restricted to its actual policy model.

## 7. Information really is discarded, without losing the stated control task

Take P={a,b,c,d,e}, the four controlled slots, and three labelled residual slots. All original floors are one. Compare

    R_left=({d},{e},{d,a});
    R_right=({d},{e},{d,b}).

These are different full labelled incidence states on the SAME carrier and floor vector. In either case H hits every residual root exactly when it contains d and e. For every unordered pair U, U union {d,e} has size at most four; if it has no label outside U, append one existing palette label. This yields a permitted H of size three or four. Thus both residual families have exactly the same stored table, F_R(U)=1 for all U.

Choose the same current anchor pair (a,b), target (c,b), guard identities and phase zero. The allowed records agree completely, while the third residual support differs. Both source states and both target states have exact tau=4, forced by their four distinct singleton requirements and realized by the corresponding four-label sets. The same handover safely reaches each state's own exact prepared target while preserving its differing residual support.

This proves the retained-input map is non-injective even with fixed carrier, target anchor pair and floors. It has not smuggled the whole incidence state into a 'syntax' table. The omitted labelled residual distinction is irrelevant to this task because that residual root is never edited. This is not a claim of minimal encoding, universal compression, reconstruction of all certificate fields, or access by an internal observer.

## 8. Disposition and remaining frontier

Positive: the upper-cover family along an X2 prepared handover has an exact endpoint/union law; a derived fixed-residual Boolean table and explicit phase memory suffice to choose, execute and renew every allowed handover; graph connectivity exactly characterizes concatenated handover reachability; residual transversal at most three guarantees connectivity of all prepared targets with the stated finite bound.

Negative: safe source or safe prefix alone does not guarantee a safe complete handover. Even exact-four prepared endpoints on an X2 carrier need not be connected by this particular macro policy, as the sixteen-residual-root construction proves. Other native schedules can work, so no general repair impossibility is inferred.

The next unclosed obligation is changing or otherwise exploiting residual information without hiding a full-state read: factor a broader X2 schedule, or define and justify an updateable retained summary when a residual root may be edited. Preparation and arbitrary full labelled endpoint restoration outside the prepared class have not been solved by this result. No such extension or numerical campaign is launched here.

All results above are written analytical deductions and symbolic counterexamples. No code, tests, enumeration, external review, CI result, numerical PASS or new numbered certification is claimed. Whole-argument and publication audit must distinguish this evidence type from the previously closed A12 computational evidence. Closed A12.1-A12.5, issue #104, certified v16.54/v16.55 and accepted A11 sources are untouched. No physical force, energy, geometry, GR/ADM, dark-matter replacement, physical nonlocality, continuum, observer field or fundamental time follows from this work.
