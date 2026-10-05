# A11.X43 — renewable four-cover transport with scarce representatives

Exact analytical candidate. Scope 2b462c72b6a4798149ae4ee81cad68248bee96ac; accepted parent 117ba4a8d1f7475269fe8958f80135682115d686.
No numerical execution or numbered certification.

## 1. Fixed carrier and typed statements

Use the native finite ordered palette P, original labelled roots and SAME ORIGINAL positive floors a_i. One primitive adds or removes ONE incidence in ONE root; larger temporary supports are allowed. No new labels/roots, weakened floors, simultaneous primitives or geometry.

Supply SAME nonempty actual masks Q_i on G=S disjoint-union R, with p=|S|>=1, n=|R|>=p+3, m=p+n. Supply source/destination partitions B_j,D_j with equal positive corresponding sizes b_j; A_i=union_{j in Q_i}B_j, C_i=union_{j in Q_i}D_j; N_i=sum_{j in Q_i}b_j and 0<a_i<=N_i. Require exact template transversal FOUR.

The NEW upper structural hypothesis is:
    EVERY I subset G with |I intersect S|=1 and |I intersect R|=3 covers all ACTUAL masks Q_i.
This is an openly sufficient property of actual incidences, not an imposed native rule. A given four-role cover need not remain fixed, and groups may be singletons.

**X43C (cover-transport lemma).** For ANY permutation pi of G there is a four-set I with one S-role and three R-roles such that pi(I) also has one S-role and three R-roles. Under the stated incidence property BOTH are minimum template covers. A deterministic eligible choice is derived.

**X43R (renewable direct repair).** In addition suppose an original root has actual mask S and let alpha=min actual pair avoidance over pairs meeting S and rho=min over all role pairs. If C(alpha+rho,alpha)>2p(m-3), inherited X42L supplies a complete cycle-based lower path. X43C gives FOUR SAME ACTUAL labels covering both adjacent endpoints of EVERY chosen simple cycle, including when all four selected owners move. That SAME physical path stays directly in{3,4}, preserves every original floor, renews another handover whenever unfinished, reaches FULL labelled/noncompact C and toggles exactly the original endpoint-differing incidences once. NO condition b_j>=2 in a cover is used.

**X43F (sparse family, all cardinalities).** The X42 family ONE S, ONE R co-pair mask per pair and p broad G-minus-s masks, for EVERY p>=2,n>=5p, satisfies both hypotheses. Therefore DIRECT minimum-event band repair now holds for EVERY positive equal corresponding group size b_j, including singletons. Controls with p>=3 give original floors>=3: (i) all b_j=1 with a full m-cycle and no unselected palette label; (ii) b_s=1 for all S and b_u=p+1 for all R, with p renewed long cycles. EVERY minimum cover in these controls necessarily uses a singleton S-group, so no minimum cover meets the old multiplicity hypothesis.

This strengthens upper protection of the supplied lower construction, not native connectivity classification. L already connects the same-floor equal-size-pattern endpoints. Arbitrary template access, unequal corresponding sizes, arbitrary mixed-floor/directed/higher-target/nested universality and efficiency implementation remain separate.

## 2. Derived cover transport for every role permutation

Let
    A={s in S: pi(s) in S},
    B={s in S: pi(s) in R},
    C={u in R: pi(u) in S},
    D={u in R: pi(u) in R}.
These are actual role sets, not independent root-capacity pools. Since pi is a bijection, |B|=|C|<=p and |D|=n-|C|>=n-p>=3.

If A is nonempty, choose its least role s and three least distinct roles of D. The resulting I has one S-role and three R-roles. Its images consist of pi(s) in S and three distinct R-images, so pi(I) has the same type.

If A is empty, ALL p S-roles lie in B, so B is nonempty, and |C|=p>=1. Choose least s in B, least u in C and two least distinct roles in D. Again I has one S-role and three R-roles. Its images consist of pi(u) in S and pi(s) plus two distinct D-images in R. Bijectivity guarantees all four images distinct. Both sets have the required type.

This provides an eligible finite deterministic choice for EVERY permutation, without assuming a convenient cycle arrangement. It is not merely the statement that some independent source and destination covers exist: the SAME selected role set I is transported by the prescribed pi.

Under the actual incidence property, I and pi(I) hit every mask. Exact template four makes them minimum covers. No additional labels, slots or floor slack are consumed. The condition n>=p+3 is sufficient; sharpness and converse are not asserted.

## 3. Lift to FOUR SAME labels through every physical primitive

At a restored partition E, choose a simple ownership cycle i_1->...->i_l->i_1 and the actual selected labels x_t currently at i_t and destined for i_(t+1), as in X42. Let pi send i_t to i_(t+1) and fix every other role. Define ONE actual representative z_j per role:
- on the cycle use the selected label currently in that group;
- outside the cycle use the least current label of that nonempty group.

The z_j are distinct. At the next partition F, z_j has owner pi(j): cycle labels move to the next role and all others keep their owners. This remains valid for unequal sizes across DIFFERENT roles and for b_j=1; only equal corresponding endpoint sizes are needed by the lower cycle construction.

Apply X43C to this pi, choose I, and put K={z_j:j in I}. Then |K|=4. Its OLD owner set is I and its NEXT owner set is pi(I), each a cover of the ACTUAL masks. Thus the SAME four actual labels hit every E_i and every F_i. Selected labels may change owners; they need not be unselected or permanently attached to the same four roles.

During the existing one-root expansion/contraction handover, every active support contains its old endpoint during additions and its next endpoint during deletions; untouched roots are old and completed roots are new. Therefore K hits EVERY support at EVERY single-incidence prefix. This proves tau<=4 on that actual path. It neither freezes K's owner roles nor relies on a maximum-layer conversion.

Actual pair witnesses for tau>=3, original same-slot floor legality and eligible root/primitive choices remain the separate X42L obligations, not consequences of the four-cover. The transported cover does not replace the lower guard. It supplements the SAME physical path, so the event minimum survives directly.

## 4. Lower safety and renewal domain, restated without extending the source

For completeness identify inherited X42L's exact sufficient domain. Actual exact-four consistency forces every role pair to have at least two avoiding original slots. A common witness exists for any pair footprint using at most three roles. The actual S root supplies a common witness for any footprint avoiding S, even while that root changes. Only disjoint selected edges with at least one incident to S can remain noncommon, at most 2p(l-3), with allowed overcount.

For a noncommon pair, at least one old/new two-role owner set meets S, so its actual witness counts are at least alpha,rho in either orientation. Exact X34 fractions and conditional averaging on the SAME shared original indices give total mean<=2p(m-3)/C(alpha+rho,alpha)<1, and derive a complete root order with first(new witnesses)<last(old witnesses) for every pair simultaneously. No independence or invented separate capacity is assumed.

At each root, add literal absent next-only incidences before deleting literal source-only ones. An old support survives during expansion and a next support during contraction, each of size N_i>=SAME original floor a_i at that SAME slot, including saturation. Common incidences remain fixed, nominal already-present replacements are omitted. Actual common witnesses or untouched last-old witnesses through first-new completion miss every physical pair at every primitive. Literal finite lists and conditional choices derive each eligible next edit, rather than assuming arbitrary safe-prefix extension.

Equal current/destination group counts balance the misplaced-label graph. Every nonempty finite balanced loop-free graph has a simple cycle. Each completed exchange restores all b_j,N_i, actual masks,S,alpha,rho and template exactness, removes balanced arcs and fixes selected labels at their final owners. If unfinished another simple cycle exists, and the same strict bound handles it.

X43C applies afresh to ANY next cycle permutation. Nonempty group representatives always exist even if a previous singleton group's label has changed. No upper-cover label is spent; the next common cover may comprise different actual labels or owner roles. This gives a renewable upper interface rather than one fortunate cover at the first exchange.

Incorrect-owner count strictly decreases by the cycle length after each finite exchange and correct labels never move. The derived next cycle/order/primitive and well-founded measure prove termination at D_j and FULL labelled/noncompact C_i. Each original differing incidence toggles once; each common incidence stays fixed. Combining lower protection with Section 3 yields DIRECT3<=tau<=4 and exactly sum_i |A_i symmetric_difference C_i| primitives. Counts are per endpoint leg, not globally unique across chains revisiting states.

No use of A is needed for X43R. X42B remains separately valid for its other lower-class inputs without the new cover property. We do not infer event minima from an A-converted path or preservation of unfinished waypoints. Saturated floors and carrying level three within a handover remain permitted.

## 5. Sparse family: remove upper-cover multiplicity for all positive sizes

For EVERY p>=2,n>=5p take S={1,...,p}, R={p+1,...,p+n}, and the X42 original masks:
    ONE S;
    ONE R minus {u,v} for every R-pair;
    ONE G minus {s} for every s in S.
All masks are nonempty and original, without replicas. The base family forces one S-role and three R-roles into any four-role cover; conversely EVERY such one-plus-three set hits every high co-pair root. It hits each broad root too, because a four-set cannot fit in its singleton complement. Thus the new EVERY-cover property holds, and ALL minimum template covers have that type. Exact template four is unchanged.

Actual counts are alpha=n-1,rho=2, since broad roots avoid no role pair. Writing n=5p+d gives
    C(n+1,2)-2p(n+p-3)
      =[p^2+17p+(6p+1)d+d^2]/2 >0.
This inherited X42 margin holds for every d>=0. The upper size condition n>=p+3 also holds. Consequently X43R gives DIRECT band/minimum repair for ALL b_j>=1 and SAME original positive floors<=N_i, provided source/destination sizes correspond. This is the substantive extension of X42U: no cover's groups need two labels.

The profile argument remains valid for all positive group sizes. Broad roots distinguish S roles, S distinguishes S from R, and rest co-pair roots distinguish R roles. Every role profile is distinct; any partition-union cell for the SAME endpoint must be profile-homogeneous. Every original root contains at least two profiles, excluding a singleton-mask representation, as proved in X42. This is an input-representation obstruction, not native disconnection or inability to reach another state.

No new root or added palette representative is used to replace the old multiplicity assumption. The role-cover structure supplies a transported actual cover on every simple cycle.

## 6. No unselected label anywhere: singleton-group full-cycle control

Fix EVERY p>=3,n>=5p and set b_j=1 for ALL roles. Use one original label x_j per role and destination sending x_j to j+1 cyclically on ALL m=p+n roles. Source/destination group sizes are one. The misplaced graph is one directed m-cycle with no shorter simple cycle. Every palette label is selected and changes owner in the full cycle; NO unselected label exists anywhere.

Original floors are SATURATED:
    a_S=p, a_high=n-2, a_broad=m-1,
three distinct grades, all>=3. Every mask is a nonempty proper subset of the connected cycle, so every actual root changes. X43 supplies four SAME labels whose old and next owner sets both cover all roots despite all four selected labels changing owner. This gives complete direct band/minimum repair without an unchanged-owner representative and with no floor reserve.

EVERY minimum template cover uses singleton groups, so the former two-label condition fails. More strongly, ANY actual minimum four-label cover must use one S-label and three R-labels; ALL source groups are singleton. A partition cell cannot have two labels with different incidence profiles, and each profile has only one label here, so no regrouping creates any larger cell. Thus the old multiplicity hypothesis cannot be recovered by representing the SAME state differently.

Four disjoint floor-safe supports cannot fit ANYWHERE: at most one low slot exists, and any four original slots need at least p+3(n-2)>p+n=k labels since n>3 and n-2>p. The full cycle/original endpoint union is two-covered by x_p on p->p+1 and x_(p+2) on p+2->p+3: low is hit via p; the two labels expose three R roles to high masks, each excluding only two; broad masks exclude only one role and cannot miss a two-role footprint. Whole-union preparation is unsafe, not evidence of native disconnection or failure of every whole-root order.

This control is a symbolic all-parameter proof. One full cycle completes it; it is not claimed to demonstrate several unfinished cycles when all groups have size one. The repeated control below supplies that separate obligation.

## 7. Scarce required S representatives with repeated long handovers

Fix EVERY p>=3,n>=5p. Take original existing labels:
    z_s for each s in S;
    d_j for each j in R;
    y_(s,j) for every s in S and j in R.
All labels are distinct. Source groups:
    B_s={z_s};
    B_j={d_j} union {y_(s,j):s in S}.
Using ordered R roles j_1,...,j_n, destination groups are
    D_s={y_(s,j_n)};
    D_(j_1)={d_(j_1)} union {z_s:s in S};
    D_(j_q)={d_(j_q)} union {y_(s,j_(q-1)):s in S}, for q=2,...,n.
These are partitions of the SAME palette. Group sizes are one in S and p+1 in R, corresponding exactly at both endpoints. Palette k=p+n(p+1).

The misplaced graph has arcs s->j_1 and j_n->s once for each s in S, and p parallel copies of every j_q->j_(q+1). Diagonal d_j labels are correct. Every simple cycle passes through exactly ONE S role and ALL R roles, so has length n+1. Selecting a cycle fixes one S label, one incoming label at that S role and one label on each rest arc, removing one balanced copy. After q completed cycles, the graph has exactly p-q S branches and p-q copies of the rest chain. A next cycle exists whenever q<p; exactly p cycles restore FULL C.

The SAME X42 lower counts and X43 cover-transport property persist at every boundary. Literal primitives and conditional orders preserve original floors and every pair, and transported four-label covers guarantee the upper bound for EVERY next cycle. The next cover may use an unchanged S representative outside the chosen cycle; this control is not claimed to require moving all four representatives at each step. Section 6 independently proves the stronger no-unselected control.

EVERY minimum cover has one S role and three R roles, but ALL S groups have size one. Thus NO minimum cover can satisfy b_j>=2 for every cover group, at either original endpoint or restored intermediate partition. Distinct S incidence profiles prevent regrouping their labels into one larger cell. More formally, any profile-homogeneous union-partition cell containing an S-label has only that ONE label. Any actual four-label hitting set must hit S and the high family, requiring one S label and three distinct R-role representatives. Therefore changing the SAME-state representation cannot remove this scarce necessary cover group.

Saturated original floors are
    a_S=p,
    a_high=(n-2)(p+1),
    a_broad=k-1,
distinct and>=3. Only the S slot is low. Any four disjoint floor-safe supports require at least p+3(n-2)(p+1)>k, since n>3. There is no original root-floor reserve and no carrier-wide disjoint-four placement.

For every q with 0<q<p, the low root and ALL high roots remain unfinished relative to BOTH original endpoints while all protective conditions renew. Low has lost/gained selected S/R labels but retains an unresolved z_s. Each high mask is a nonempty proper subset of every chosen cycle (which includes one S role outside it and every R role); it loses/gains crossing labels on the first handover. A high-to-excluded-R crossing arc, or an included last-R->S arc, still has p-q unresolved source labels, so it differs from C until the last cycle. Broad roots differ: the one omitting s changes only when s's branch is selected, then reaches its destination. They may be unchanged or already completed; this control does NOT assert ALL roots unfinished.

For an individual cycle, selected labels on s->j_1 and j_2->j_3 two-cover the cycle union: low via s, highs via three R roles j_1,j_2,j_3, broad roots via two-role footprints. Hence simultaneous whole-cycle union preparation is unsafe. All cycle unions are inside the full original endpoint union because labels move only once directly to final owners; that same pair therefore two-covers the full original union as well. This is a method obstruction, not a no-path or every-order impossibility claim.

The control proves actual repeated renewal when every minimum cover has a scarce group, rather than merely one successful upper cover. It is symbolic, without scientific execution, sampling or benchmarking.

## 8. Advance, inherited domains and remaining questions

X43C derives compatible minimum-cover transport from an actual one-plus-three cover structure. It is not the tautology that two endpoint covers exist: one actual four-label set simultaneously covers both, with a supplied construction for ANY cycle. X43R supplements the SAME event-unique X42 lower schedule and so proves direct band/minimum without the previous unchanged-representative multiplicity condition.

Inherited X34 supplies shared-root conditional handover, X40 cycle/event accounting and X42 multi-role lower localization/constructor/profile distinction. X39 already had a different common-cover argument in its dense class; X43 does not claim common-cover transport as a new general principle. Here it is structurally derived for the sparse class with necessary singleton-sized cover groups. Certified L already gives native symmetry connectivity. No A conversion is invoked for the new direct result.

Same supplied exact-four masks, equal positive corresponding group sizes, actual S and strict lower count margin remain inputs, now joined by the EVERY one-plus-three cover property and n>=p+3. The old two-label-per-cover-group hypothesis is removed WITHIN this class, not universally. Arbitrary template access, templates lacking the cover property, unlocalized/below-bound lower repair, unequal group sizes, arbitrary mixed/directed/higher-target/nested universality and sharper compatible-grade work remain open.

No scientific commands/tests/enumeration/numerical workflows, implementation, benchmark, integration merge, new numbered certificate, literature-originality or physical/fundamental-time claim. v16.55/v16.54, inherited analytical sources and ALL original evidence remain unchanged. Separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped. Minimum incidence count is a mathematical result, not measured runtime.

Fresh independent whole review must check BOTH the permutation cover construction and the coupled actual lower/upper path: same-label identity/distinctness, arbitrary cycle eligibility and scarce group legality, every pair/original floor, renewed cover and balanced continuation, exact event minimum and full destination, singleton full-cycle/no-unselected control, repeated p-cycle/exhaustive minimum-cover and profile restriction, unfinished-root qualification, union/private-root method obstructions and inherited domains.
