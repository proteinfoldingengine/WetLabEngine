# A contraction guard for higher-hyperedge cloning

Status: candidate analytical result for independent review. Parent analytical head 59b14ffbae1c8caaf665a4e90afeab89a146eff8. No implementation, numerical search or scientific execution. Earlier accepted proof files remain unchanged.

## 1. Objective and scope

Use the fixed-palette width-floor carrier and the clone construction of HYPEREDGE_CLONE_BOUNDARY.md. That construction edits only roots containing u but not v, copies every distinct v-only root with v replaced by u into compatible existing slots, and fills unused editable slots with P. All other roots stay fixed. Its sorted slot criterion is assumed satisfied. We do not assume a pair root or singleton guard exists.

We derive an exact formula for the completed clone's hitting number. The formula supplies a necessary-and-sufficient condition for that clone not to lower tau, and a sufficient condition for it to remain exactly at the original target. A symbolic all-floor-three family then shows an exact clone can move from a protected endpoint to one with no q disjoint root witnesses.

This is an exchange criterion and a demonstrated bridge, not a universal existence or termination theorem for arbitrary higher-floor endpoints. A contracted family below is an analytical object, not a new native root tuple; its smaller or empty supports are never introduced as native moves.

## 2. Two auxiliary covering problems

Let A have tau(A)=t>=3, and let A'=C_{u<-v}(A) be the slot-compatible clone. Define:

- F: the old roots not containing u, regarded on P\{u}. These roots are all retained.
- R=P\{u,v}.
- L: take every retained old root (all except the u-only roots) and remove u and v from its support. Regard the resulting supports as a family on R. Repeated supports may be deduplicated without changing its hitting number.

Write f=tau(F) and lambda=tau(L). An empty support in L makes it impossible to hit, and we set lambda=+infinity in that case. This extended convention is for the auxiliary covering problem only. If a family is empty its hitting number is 0, although F is not empty here: adding u to any hitting set of F hits A, so

    t-1 <= f <= t.

The upper bound holds because any old minimum hitting set can be restricted to P\{u} for purposes of hitting F. Every hitting set of L hits F, giving lambda>=f, including the infinite case. In particular any finite hitting set of L is nonempty.

## 3. Exact clone formula

**Theorem U.** Under the stated slot-compatible construction,

    tau(A') = min(1+f, lambda).

Proof. Partition new hitting sets by whether they use at least one of u,v.

A hitting set containing u has minimum size exactly 1+f. The root constraints not containing u are precisely the retained F constraints. Every copied root contains u, every retained common root contains u, and every P filler contains u. Thus u together with a minimum F cover suffices and no smaller cover containing u is possible.

If a new hitting set H contains v but not u, replace v by u. Every retained v-only root E has a copy (E\{v}) union {u} in A'. Since H lacks u and hits that copy, H already contains a label of E\{v}. Removing v therefore does not lose coverage of E. Roots containing neither u nor v remain hit; roots containing u, including common roots, copies and P fillers, are hit by the new u. This produces an equal-sized new hitting set containing u. Consequently the minimum among all new covers using at least one of u,v is exactly 1+f.

A new cover avoiding both labels lies in R. On R the retained roots impose exactly L. The contraction of each copied u-only root equals the contraction of its corresponding retained v-only source, so the copies add no further condition. P fillers impose only that the cover be nonempty; that already follows from lambda>=f>=t-1. Thus the minimum among covers avoiding u,v is exactly lambda, or no such cover exists if lambda is infinite. Taking the better of the two classes proves the formula.

## 4. Safety, exactness and a failure certificate

**Corollary V (replacement guard).** The completed clone satisfies tau(A')>=t if and only if lambda>=t. The old pair-root guard is the special case lambda=+infinity because its contraction is empty. The new criterion also applies when every actual root has size at least 3.

Indeed 1+f>=t, so U makes lambda the only possible source of a decrease. Since lambda>=f>=t-1, an unsafe clone has lambda=t-1 and then tau(A')=t-1 exactly. A (t-1)-label cover of L is therefore a concrete failure certificate: viewed in the native palette it hits every new root while avoiding both clone labels. Such a cover cannot hit every old root, by old exactness. Absence of such a cover is the exact guard; we do not claim its verification is computationally cheap.

**Corollary W (exact exchange).** The clone remains exactly at t if and only if

    lambda>=t and [f=t-1 or lambda=t].

This follows immediately from f in {t-1,t} and U, including lambda=infinity. In particular f=t-1 plus lambda>=t is a reusable sufficient exactness condition.

The arbitrary-floor star lemma R implements each such clone with tau>=t-1, all original floors and one-incidence moves. If both endpoints are exact-t, upper-excursion removal turns that finite local path into a {t-1,t} path. A finite list of exchanges satisfying W at target q can therefore be concatenated without accumulating a lower deficit: every completed exchange returns to q. If only V is known, completed values may increase; their lower bound still protects subsequent star steps, and a final exact-q lower-guard connection can be clipped by Theorem A.

No universal list of guarded exchanges, accessibility theorem, or globally decreasing progress measure is supplied here. The criterion exposes the missing obligation instead of assuming that it follows from degree or capacity slack.

## 5. A genuine higher-floor bridge from protected to unprotected

Take nine distinct labels u,v,a,b,c,d,e,f,g, all root floors equal to 3, and roots

    {u,v,a}, {u,v,b}, {u,v,c},
    {u,d,e}, {v,f,g}, {a,b,c}.

The last three roots are disjoint, forcing tau>=3. The set {u,v,a} hits all six roots, so tau=3. There is one editable u-only slot, {u,d,e}, and one copied demand, {u,f,g}, from the v-only root {v,f,g}. The slot criterion holds exactly. Retain the other roots and replace {u,d,e} by {u,f,g}.

For this clone, F consists of {v,f,g} and {a,b,c}, so f=2. The contracted family L has singleton supports {a},{b},{c}, the pair {f,g}, and {a,b,c}; hence lambda=4. Formula U gives tau(new)=min(3,4)=3. Corollary W supplies an exact exchange with no pair or singleton root in the native tuple. Its smaller contracted supports are proof objects only.

The original endpoint has three disjoint root witnesses. The new endpoint has maximum disjoint-root family size 2: every retained fan root {u,v,a}, {u,v,b} or {u,v,c} intersects every new root. If a disjoint family contains no fan root, it is drawn from {u,f,g}, {v,f,g}, {a,b,c}; the first two intersect, and either can be paired with the third. Thus no three disjoint root witnesses exist at the destination.

For arbitrary g_0>=0 add g_0 further roots, each a triple on its own new palette disjoint from all previous labels and the other added triples. Put q=3+g_0. Hitting numbers add over these disjoint label sets. The same clone then has

    tau(old)=q, f=q-1, lambda=q+1, tau(new)=q.

All floors remain 3. The old tuple has q disjoint root witnesses; the new tuple has maximum disjoint-root family size q-1. There are no singleton or pair native roots. The exchange stays within one fixed palette and floor vector; unused old labels d,e are allowed at the destination.

This is an arbitrary-target symbolic example of the guard reaching beyond the protected endpoint class. It is not an enumeration campaign or a claim that all unprotected higher-floor endpoints are reachable. Combined with Theorem J, each such destination is connected to the protected component for its own palette and floor vector.

## 6. Relation to the earlier failed clone

For the four-root example in HYPEREDGE_CLONE_BOUNDARY.md, F consists of {v,c,d} and {w,e,f}, so f=2. The contracted family has {w}, {c,d}, and {w,e,f}, with lambda=2. Formula U gives min(3,2)=2, recovering the one-unit loss. The successful family above instead has enough contracted constraints to make lambda>=t while retaining f=t-1. The distinction is a covering property after contraction, not a degree count or an assumption that all hyperedges behave like graph edges.

## 7. Remaining question and review boundary

The next global obligation is whether arbitrary exact-q higher-floor endpoints admit a finite sequence of slot-compatible exchanges satisfying this guard, or an alternative exactness-restoring move when the guard fails. The contraction criterion is necessary and sufficient for this clone's endpoint safety, not a theorem that such clones suffice for all connectivity.

Conditional native lifting and the distinction from native necessity remain unchanged. No implementation, numerical execution, certification, efficiency bound or physical implication is claimed. Independent review must check the auxiliary empty-support convention, both cover classes in U, the exact equivalences in V/W, P fillers and duplicates, all symbolic hitting numbers, and the protected-to-unprotected distinction. Any later numerical campaign needs its own prospective protocol.
