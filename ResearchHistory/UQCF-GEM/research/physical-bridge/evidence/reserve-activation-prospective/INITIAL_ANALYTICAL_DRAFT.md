# Reserve activation through successive saturated-neighbor compensation

Status: OPEN analytical candidate, hand-derived before new enumeration. Parent c31f5313486be2be25ff1d32d01b507d2de2e313 closes source escape. This campaign addresses escape to a usable absent label within a specified monotone template, not complete native reachability.

## Domain

Retain finite simple isolate-free H with source vertex-cover number three or four, positive original multiplicities a, original palette and star footprints M_v. G is a saturated subgraph; original floor on uv is a_u+a_v in G, otherwise one. All current footprints must be contained in some original star. Original protected hidden completions stay fixed; upper-four is required.

Choose a nonempty G-independent set I of donor types. Put N=N_G(I), disjoint from I. Fix any original H vertex cover C of size at most four with a_i>=2 for each i in I intersect C. Choose one actual original anchor at each C type, and one actual original non-anchor donor x_i at each i in I. Such labels exist. All other original labels stay unchanged. Different choices give the same analytical construction.

A receiver w in N becomes activated when a donor is transferred to the full original star M_w. Exactly one additional label is retained there and is never moved again during the forward construction. A donor is used at most once. Each transfer shrinks its donor from M_i to {iw}, then expands it to M_w; all deletions precede additions. A release deletes an unused donor's entire M_i and ends the construction at its first vacancy. This deliberately specified template does not include arbitrary partial-star interactions or return transfers.

## Saturated-neighbor activation closure

Starting R=empty, repeatedly add any w outside R for which some i in I has N_G(i) minus R = {w}. Let R* be the resulting least fixed point, equivalently the least set closed under all implications N_G(i) minus {w} subset R => w in R for i in I and w in N_G(i). Define Z(R)={i in I:N_G(i) subset R}.

**Candidate theorem.** A first vacancy is reachable by this monotone full-star activation template iff |Z(R*)|>|R*|. Every positive instance admits unchanged actual C anchors, all original floors, original domination and uniform safety for every original protected hidden completion. The closure and the criterion are independent of rule order. This is an exact classification of the template, only a sufficient criterion for unrestricted native reachability.

## Construction and safety

Track activated receivers R and used donors J, with a bijection from J to R recording transfers. Initially both empty. At macro boundaries each used donor occupies its assigned full receiver star; each unused donor remains original. Thus counts are a-1_J+1_R. Every used donor has all saturated neighbors in R.

If unused i has N_G(i) subset R, release x_i. Every original saturated loss at iw is compensated by the extra full receiver label at w. Nonsaturated floors and upper-four follow from the unchanged actual C anchors. Domination holds during deletion. Other labels are nonempty; the final deletion is the first vacancy.

Otherwise choose unused i with N_G(i) minus R={w}. Shrink x_i to iw. Every other saturated root incident to i has its extra receiver support already present. Root iw retains x_i through the entire transfer. Expand to M_w, creating a new extra receiver label; no floor is decreased by expansion. All nonsaturated roots and upper-four are protected by the unchanged C anchors. The donor remains nonempty throughout. Since w is new, this extends the J-to-R bijection. The root iw exists in H because it is saturated. No source type is invented or missing from the original source; current counts may become zero at non-anchor donor types.

Every slice is dominated by original stars. If a protected full system acquired a two-label cover, replacing current core labels by their original containing stars would contradict original lower-three protection. The unchanged C anchors supply upper-four independently of hidden incidences. This establishes universal safety, not observation or actual-successor enforcement.

## Closure, exactness and order

The implication operator is monotone on finite receiver sets, so asynchronous saturation reaches its unique least fixed point R*. A donor that has fired has all its neighbors activated thereafter and can never fire again. Hence a closure run realizes an injective assignment of one distinct donor to every activated receiver, and J subset Z(R), |J|=|R|.

If no unused zero-neighbor donor exists, every member of Z(R) is used. If R is not closed, any applicable donor with exactly one missing neighbor cannot already be used, so the next closure rule is realizable as a safe transfer. Therefore either a release becomes available, or one reaches R*. At R*, an unused releasable donor exists exactly when |Z(R*)|>|R*|.

An early release also implies the final inequality. Under a subsequent closure rule adding one receiver, its firing donor was not in Z(R) and newly enters Z; hence |Z(R)|-|R| never decreases. Thus an early positive surplus persists to R*. Conversely if final surplus is positive, executing closure transfers without releasing early leaves an unused donor in Z(R*) that can be deleted. Necessity applies only to the defined template: a transfer to a new receiver must leave all other saturated neighbors already compensated, since its full-star donor loses those incidences and no other labels have changed except previous completed receiver transfers. A release similarly requires all its saturated neighbors activated. No arbitrary-native-path normalization is asserted.

## Reversal and costs

The reverse of any constructed route restores the exact original labelled source, provided the reserve and all other labels have not been altered in between. Every reversed state is one of the already safe forward states. This is an exact release-and-reversal construction, not permission to insert arbitrary repair in the middle, nor a general exchange/restoration theorem.

A transfer i->w costs deg_H(i)+deg_H(w)-2 actual edits; release of t costs deg_H(t). The retained saturated edge prevents early emptiness. The constructed cost is the sum over chosen transfers plus final release; no shortest-path claim. Equal stars in a K2 component need care: the prospective anchor eligibility and fixed cover exclude using its two singleton endpoints as an unprotected reserve; the formula can give a zero-edit relabelling of its container. Such a macro changes the bookkeeping assignment, not the actual state. It must not be counted as a committed incidence edit or a source escape. The canonical certificate must explicitly retain this distinction.

## Hand-derived controls

On H=K_{4,3} with I={0,1,2,3}, N={4,5,6}, original anchors C={4,5,6}, all multiplicities one, take saturated edges 04,14,15,25,26,36. Activate 4 using donor0, then5 using donor1, then6 using donor2, and release donor3. There is no original saturated cherry: the degree-one donors have different neighbors. This yields three genuine cross-star transfers and a first vacancy in18 actual edits (each transfer costs5, release costs3), with three original anchors unchanged. It generalizes the one-step cherry mechanism to a compensation chain.

On the same carrier with G=H, closure is empty and Z(empty) is empty: the donor deficiency4>3 gives a static reserve but no template release. All saturated degrees exceed one, so the inherited source-escape theorem also rules out unrestricted release here.

With G empty, any donor releases directly. A two-donor common-neighbor pattern recovers the inherited cherry construction as a special case, without claiming a new five-type result. Fixed-cover eligibility remains essential; an unanchored numerical success cannot establish the theorem for an excluded singleton donor.

## Open boundaries

The choice of I and C is supplied and exact. No assertion that every reachable reserve has such an activation witness. Native acquisition, retained record origin, enforcement, actual-successor selection, guaranteed progress, broad C3/C4-C6 and physical derivation remain OPEN. Optional NOOPs can stall forever. No new primitive, full-state sensor, hidden-dependent outcome, compulsory commitment, fundamental time, dark-matter variable or geometry is introduced. No numerical campaign has yet run.
