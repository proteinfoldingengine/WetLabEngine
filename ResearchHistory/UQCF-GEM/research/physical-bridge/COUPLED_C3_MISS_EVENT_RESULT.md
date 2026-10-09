# C3 event inversion from miss-count increments
Status: analytical candidate; independent review/publication audit pending.
Scope commit: b5cdcd6a232b938437d1250b178afb47d41d5a22.
Inherited source: POST_A12_DYNAMIC_RESIDUAL_RESULT.md at 7c538e702e92a55beebcfc3f0f28bcd0bc7f00f7.
This is a conditional information theorem about the already defined count field, not a native acquisition or enforcement mechanism.

## 1. Objects and complete outcome premise
Let P be a finite declared palette and R a fixed finite collection of residual root slots. Each has a support S_r subset P. For every singleton and pair H define M(H)=#{r:S_r intersect H is empty}.

Between two consecutive observed resolved slices, either nothing changes, or exactly one root undergoes exactly one syntactically valid incidence addition/deletion. No other root or label changes; no root creation/removal or partition change occurs. Observations are exact. A skipped batch is not an atomic slice.

Write Delta(H)=M_after(H)-M_before(H). The decoder uses P and Delta only. It needs neither the number of residual roots nor their initial supports. Saying Delta is supplied does not derive its accessibility.

## 2. Exact inversion theorem
Under the premise above:
- Delta is identically zero iff the outcome is NOOP.
- Otherwise there is exactly one label x whose singleton difference is nonzero.
- Delta({x})=-1 means addition of x; +1 means deletion of x.
- For every y!=x, y belongs to the active support both before and after iff Delta({x,y})=0.
These facts uniquely reconstruct the full active support before and after the edit. They do not identify its root-slot address.

Proof. Only the active root contributes a changing miss indicator. A valid addition of x changes its singleton absence indicator from1 to0; deletion changes it from0 to1. Every other singleton is unchanged. Thus a committed toggle has one nonzero singleton, with the stated sign, while NOOP has none.

Put sigma=Delta({x}), which is -1 for addition and +1 for deletion. For y!=x, if y is present in the active root, the pair {x,y} hits that root both before and after, so its miss indicator remains zero. If y is absent, the pair's miss indicator equals the absence indicator of x and changes by sigma. Contributions from all other roots cancel. Hence
Delta({x,y}) = sigma * 1[y absent from the active root].
This determines every incidence other than x. The sign determines whether x was initially absent or present, and its final incidence is the opposite. QED.

Queries not containing x have zero difference. Higher-order coordinates are unnecessary. On a one-label palette the singleton alone suffices; on an empty palette only NOOP is possible. An empty residual family likewise has no toggle. Algebraic supports may be empty; imposing native floors merely restricts the admissible events, leaving the inversion valid.

## 3. Forward update and inverse observation are different
For a specified syntactically valid toggle c on the active root:
- given the old full miss field, the active support and c, the inherited exact update formula gives the new full field;
- given the old and new fields, singleton/pair inversion gives the active support, changed label and sign.

Consequently any exact prospective field updater must have sufficient input to determine that active support whenever its input would otherwise admit different active supports with different required updates. It may infer the support from other retained data; the theorem does not require a particular storage format.

A controller that only needs one legality Boolean or follows a uniformly safe restricted policy is not required by this theorem to maintain the entire field. An always-rejecting policy is also outside this exact-toggle-update requirement.

Crucially, observing the new field AFTER an edit cannot justify computing it or enforcing admissibility BEFORE the edit. Using the inferred support to explain how the same unknown field increment was generated would be circular. No retrospective formula removes that causal/ordered-update dependency.

## 4. Native swapped-root control and degree-one insufficiency
Take fixed roots {a,b},{b,c},{a,c}, residual slots r0,r1, common labels d,e, and further labels u,v,x, all distinct. All floors are2.

World A: (S_r0,S_r1)=({d,e,u},{d,e,v}).
World B: (S_r0,S_r1)=({d,e,v},{d,e,u}).
Issue the same valid committed addition +x at r0.

The complete initial miss field of any degree is identical because the two support multisets are equal. Root addresses, floors and the command also agree. After the edit, all singleton fields remain equal across the worlds: only the x singleton has decreased by one in each.

But the pair {x,u} changes by0 in A, because u is already in active r0, and by-1 in B, because u is absent from active r0. Thus the correct updated pair field differs. The active supports have been distinguished exactly as the theorem predicts.

Every listed source and successor is protected: the triangle requires two hits, every residual root is disjoint from triangle labels and contains d,e, so one further hit d suffices and is necessary. Hence tau=3, with all floors2. This is a native obstruction to exact field update from the old aggregate plus command/address alone. It also shows that even complete before/after singleton records generally fail to reconstruct the active support. Pair information adds something essential.

## 5. Address and atomicity controls
Address is not recovered: start instead with both residual supports {d,e,u}. Adding x to r0 or to r1 yields the same complete aggregate field before and after, at every degree, but different labelled successors. Even the recovered active before/after support cannot say which identical source slot changed.

Atomicity is essential: in World A add x at r0 and then delete it there. Both primitive states remain floor-two and tau-three. If the intermediate slice is skipped, the endpoint field difference is zero despite two actual edits. Zero difference certifies NOOP only under the explicit at-most-one-toggle premise. It does not certify no activity across an arbitrary interval.

These are controls on the declared interface, not universal no-observer theorems or new physical laws.

## 6. Seed-free labelled coverage corollary
Assume a complete ordered sequence of atomic field increments is available, and the correct root address of each actual edit is independently supplied. Maintain a table initially marked unknown for every root. On each nonzero increment, decode its active before/after support and store the latter at the supplied address. NOOP requires no update.

After a root's first actual edit its table entry is exact. Subsequently only edits at that root can change it; each is observed and replaces it with its newly decoded support. Therefore, by induction, once every root has undergone at least one observed actual edit, the table contains the complete current labelled residual state, for any finite number of roots and without an initial support seed.

This asserts neither guaranteed coverage nor that every untouched root must remain unknowable by all other means. Trusted addresses and complete increments remain premises. The result reconstructs an event channel from a count-difference channel; it does not derive the latter from native inputs.

## 7. Scientific significance and boundaries
The previous static theorem gives a sharp N<2^d bound for unordered reconstruction from a single field. Here a degree-two INCREMENT reconstructs the active support for arbitrary N, including families beyond that static threshold. Information hidden in a static aggregate can become visible through a native edit's exact count change.

The inherited update theorem assumed a supplied active support. This inversion proves why exact full-field updates are not generally a route around that information, while providing an explicit retrospective reconstruction if the increments are legitimately accessible.

Unknown fixed offsets in absolute field coordinates cancel algebraically in a difference, but this is not a construction that produces correct increments from uninitialized storage. No offset-tolerant sensor or new observation primitive is adopted.

The next useful target is a native available input or a genuinely smaller update-closed guard representation with independently established access. Merely exposing the full field after each edit trades an active-support read for an equivalent revealing record and does not close origin.

## 8. Verification scope
The preregistered algebraic domain has all 64 ordered two-root configurations on three labels, two root addresses, three toggled labels and two outcomes (NOOP/toggle): 768 records. It includes empty supports and is not a protected native state census. The four separate native controls above check protected carriers. A two-event coverage fixture ends at supports {0,2} and {0,1}, encoded [5,3].

Production uses direct disjointness and the closed-form inverse. Independent verification enumerates six incidence Booleans, computes fields by occupancy/co-occupancy and searches all candidate supports/toggles to invert each difference; it does not import the producer. Exact identities and values must match. Ten intended local RED failures precede implementation. General inversion and arbitrary finite coverage are proved analytically, not by the bounded fixture.

C3 origin/access/enforcement/progress and C4-C6 remain OPEN. No force, geometry, dark matter, fundamental time, GR derivation, efficient general-state reconstruction or full numbered-stage certification is claimed.
