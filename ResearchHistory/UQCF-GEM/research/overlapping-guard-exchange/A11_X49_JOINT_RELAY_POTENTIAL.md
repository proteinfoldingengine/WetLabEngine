# A11.X49 - joint multi-cover ordering and repeated-root lifting

Analytical parent: d418097d51eea2886df397ca9e9785c07237278e.
Scope: ccc28ede4d4d9eaab47391ffcc89e42898e7c858.
Exact candidate for independent review. Analytical only.

## 1. Native carrier and typed conclusions

Fix finite ordered palette P, r labelled root slots, and SAME original positive floors a_i. Exact-four endpoints A and C obey those floors. Each primitive adds or removes one incidence in one root; larger temporary supports are permitted. No labels, slots or floor amendments occur.

Supply a finite nonempty family F of physical label sets K with |K| <= 4. These need not cover either endpoint individually. For each K define
    U_K = {i : K misses A_i},
    V_K = {i : K misses C_i}.
For completed-root set D let M(D) use C_i at i in D and A_i elsewhere.

X49I: K covers M(D) exactly if U_K is contained in D and D is disjoint from V_K. On a fixed total order sigma its valid prefix indices form the integer interval
    [L_K, R_K],
    L_K = max positions of U_K (zero if empty),
    R_K = min positions of V_K minus one (r if empty).
L_K > R_K means the interval is empty. All prefixes are covered by F exactly when the union of these intervals contains all integers 0 through r. This test includes multi-stage relays and arbitrary overlaps; it is exact only for the supplied cover family.

X49J: The explicit joint mean J below being strictly less than one guarantees a deterministic whole-root order with lower pair protection AND a cover from F at every mixed prefix. Processing roots add-before-delete gives a direct {3,4} path, every original floor legal, full labelled/noncompact restoration, and the endpoint-toggle minimum. The potential supplies an eligible next root at every generated prefix; no arbitrary-safe-prefix extension claim.

X49Q: Lower-safe distinct-type certificates lift to any positive labelled multiplicity. Direct upper protection additionally requires a four-cover of the mixed tuple with BOTH old and new supports of each active type, or a full partial-copy prefix certificate. Distinct types identify equal ordered pairs (A_i,C_i), not merely equal source supports. Original slots and individual floors remain fixed.

The scope's proposed unconditional duplicate-family extension X49F is not claimed. Section 5 pinpoints its failed upper step and gives the conditional replacement. This failure concerns the proposed method, not native repair.

## 2. Exact upper coverage and overlap counts

K hits M(D) exactly when it misses none of its remaining source roots and none of its completed destination roots. This is exactly U_K subset D and V_K disjoint D, proving X49I. If U_K intersects V_K, K cannot work at any mixed prefix, as the same root would have to be both completed and uncompleted.

For prefix size p, every p-subset D is equally likely under a uniform total root order. For a nonempty subfamily S of F put
    U_S = union of U_K over K in S,
    V_S = union of V_K over K in S.
Let
    n_p(S) = 0 if U_S intersects V_S;
    n_p(S) = C(r-|U_S|-|V_S|, p-|U_S|) otherwise.
The binomial coefficient is zero when its lower argument is outside 0 through its upper argument. n_p(S) counts completed sets of size p on which ALL covers in S work: mandatory U_S, forbidden V_S, and free remaining slots. Therefore inclusion-exclusion gives the exact number covered by at least one member of F:
    N_p = sum over nonempty S subset F of (-1)^(|S|+1) n_p(S).

Shared roots are combined by unions, not assigned independent capacities. Define the exact expected number of uncovered mixed prefixes:
    Theta = sum from p=0 to r of [1 - N_p/C(r,p)].
Each summand is nonnegative. Endpoints are included. If F omits all covers at an endpoint, Theta >= 1 and the strict joint condition cannot hold. Adding supplied covers can only decrease Theta; a small family is permitted.

This is a finite symbolic formula, not an executed enumeration protocol. It can be exponentially expensive and is not an efficiency result.

## 3. Lower pair-order events and the joint mean

For every physical palette pair B define actual old and new witness sets:
    O_B = {i : A_i misses B},
    T_B = {i : C_i misses B}.
Exact-four endpoints ensure both are nonempty. If their intersection is nonempty, that root's entire A_i union C_i misses B, giving a common witness throughout its edits.

Otherwise define the lower bad event E_B as
    every O_B root precedes every T_B root.
The sets are disjoint. In a uniform order their relative order is uniform, so
    Prob(E_B) = 1/C(|O_B|+|T_B|, |O_B|).
This is the accepted X34 event fraction, here applied on the SAME order domain used for upper prefix coverage.

Let Z(sigma) be the nonnegative integer
    number of lower bad pair events
    plus number of prefixes with no supplied cover.
Its exact mean is
    J = Psi + Theta,
    Psi = sum over pairs B with O_B intersect T_B empty
                 1/C(|O_B|+|T_B|, |O_B|).

Linearity does not require independent events, pairs, covers or capacities. If J < 1, some order has Z=0. More strongly, the following conditional construction supplies it.

For an ordered prefix h of distinct roots, define J(h) as the exact average of Z over all full labelled orders extending h. Initially J(empty)=J. If s roots remain, the extension domain splits into s equal-size classes by next root i. Hence
    J(h) = (1/s) sum over remaining i of J(h followed by i).
At least one next i has J(h,i) <= J(h). Choose the least such i in the fixed labelled order. J stays below one. At every unfinished generated prefix this next root exists. After r choices J(full order)=Z(full order), an integer below one, hence zero.

This is a constructive finite rule using exact extension averages; it is not a fast implementation or a new conditional-expectation principle. Prefix evaluation may use factorially many symbolic order terms. The descending measure is the number of unchosen roots, not J (which need not strictly decrease).

## 4. Every primitive and exact completion

Process each chosen root i by adding all absent C_i minus A_i labels, then deleting all A_i minus C_i labels, in palette order. Every edit is eligible and finite. During additions the active root contains A_i; during deletions it contains C_i, so size never falls below min(|A_i|,|C_i|) >= a_i.

For a palette pair with a common witness the full union at that root misses it. Otherwise Z=0 implies first(T_B) < last(O_B). Until the first new witness completes, there is an untouched old witness. During the first new witness's own edits, the later old witness still survives because the sets are disjoint. After completion that new witness persists. Thus every pair is missed by an actual support at every primitive, proving tau >= 3.

Z=0 also means every M_p has a supplied cover. Use that cover during additions and the next prefix cover during deletions, as proved in X48. Both cover the union midpoint; changing the cited witness requires no incidence edit. Thus tau <= 4 on the SAME path.

Every root completes once; common incidences stay fixed; every endpoint-differing incidence toggles once. The count is sum_i |A_i symmetric-difference C_i|, the unavoidable toggle lower bound, so it is minimum. All labelled full destination supports are restored.

For a finite supplied chain of exact-four endpoints, if each leg supplies a cover family satisfying its own J<1, repeat the construction. All roots and original floors persist; no witness reserve is consumed. The count is minimum per leg, not necessarily between outer endpoints. J is a sufficient condition, not necessary; failure gives no disconnection theorem.

## 5. Repeated-root lifting

Now assume a quotient certificate with q distinct ordered support pairs (A_t,C_t). Its type order is lower-safe at every add-before-delete primitive and its q+1 mixed type prefixes have physical covers of size at most four. For every type t declare n_t >= 1 actual labelled slots, all with source A_t and destination C_t. Each slot has its own original floor a_(t,s) <= min(|A_t|,|C_t|).

Process types in the certified order. Within a type block process its copies in labelled order, each add-before-delete. All copies of previously completed types are new; later types are old; the active type may have old, active and new copies.

Lower safety: at any active-copy primitive, collapse the other copies conceptually to one representative per type. For the active type use the active support; for other types use their certified endpoint support. This representative tuple is exactly a state on the lower-safe type path, so every pair misses a representative support. The corresponding actual slot exists; adding other actual copy constraints cannot destroy that avoiding witness. This proves tau >= 3 without claiming copy capacity independence.

Upper safety: let K_old cover the mixed type prefix before the active type, and K_new cover the one after it. K_old hits A_t and K_new hits C_t; both hit every other type's current endpoint.
- During the FIRST copy's additions, K_old hits all old copies and the active A_t-containing support; no new copy yet exists.
- During its deletions and after it completes, K_new hits that active/new C_t support, but might miss an untouched old A_t copy. Thus K_new alone is not enough for a partially completed block.

To avoid this issue we must use an upper certificate stronger than endpoint type-prefix covers alone: for each active type either one available four-set hits BOTH A_t and C_t while hitting all other current type supports, or every intermediate partial-copy tuple is separately covered. Type-prefix covers alone do NOT imply this. Accordingly the initially proposed X49Q/F lifting deduction is rejected as stated.

The lower lifting proof remains valid. The upper obstruction is exactly shared old/new copies: with one copy the cover switches at its union midpoint, while with multiple copies an old A_t and a new C_t coexist. Both must be hit simultaneously. Equal-copy grouping does not remove that constraint.

## 6. Corrected typed scope: X49Q is a conditional lifting lemma, not X49F

X49Q (conditional): lower type certificates always lift as above. A direct upper lift also holds if, for every type block, a four-label hitting set covers the mixed tuple with BOTH A_t and C_t constraints at that active type and the current endpoint constraints at every other type. That same set hits every copy's endpoint-containing support throughout the block. Alternatively a proved full partial-copy prefix cover certificate may be used. Such a certificate is an additional hypothesis.

The scope's proposed unconditional X49F deduction is NOT established and was withdrawn during self-review before candidate freeze. We do not claim d>1 direct-band or minimum-event completion for the alternating family. X40L plus Theorem A still provides its accepted complete native band repair, without schedule/minimum guarantee.

This failed lifting deduction is published transparently because it precisely identifies the missing upper obligation. It is not evidence of native disconnection. The valid new completion result is X49J with its openly stated joint mean condition; the exact multi-cover interval/count formulas and conditional copy lift supplement it.

## 7. Conclusion and limits

X49J goes beyond describing safe supplied moves: J<1 supplies an eligible next root at every certified ordered prefix and a complete exact destination path. It uses all supplied cover exception overlaps on the SAME ordering domain as lower pair events. This gives a multi-stage relay sufficient class at arbitrary positive original floors. No explicit new infinite family satisfying J<1 beyond previously covered cases is asserted in this packet; deriving economical structural bounds that force J<1 is the remaining research obligation.

The failed copy-lifting attempt teaches a distinct limit: old and new copies coexist, so a witness switch valid for a single root may fail inside a multiplicity block. Lower protection lifts, upper protection needs an additional coexistence cover.

No numerical execution, test campaign, implementation, benchmark, integration merge, numbered certification or physical interpretation. Preserve v16.55/v16.54 and all sources/evidence. Efficiency work remains unstarted. Arbitrary mixed/directed/higher-target/nested universality, arbitrary accessibility and necessity of J remain open.
