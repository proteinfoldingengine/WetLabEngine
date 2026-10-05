# A11.X46 — actual cycle-gap derivation of orbit-compatible protection

Exact analytical candidate. Scope 70aa5ecdb03e4d2d74429a66a8877b602823aed9; accepted analytical parent 02add6acaa56284cd21308990dce23a84a469d75.
No numerical execution, implementation, benchmark or numbered certification.

## 1. Native carrier and typed statements

Fix a finite ordered palette P, labelled original roots and their SAME ORIGINAL positive floors a_i. One primitive toggles ONE incidence in ONE root. Larger temporary supports are native; no label/root is added, no floor weakened and no simultaneous move, compactness or geometry is imposed.

Supply m>=5 nonempty role groups partitioning P and SAME nonempty actual masks Q_i subset G=[m]. A restored state has each actual root equal to the union of its role groups. The template transversal is EXACT FOUR, with all four-role covers denoted H4.

Let a lower mechanism select a directed simple ownership cycle

    C=(c_0,c_1,...,c_(ell-1)),  ell>=5,

and actual labels moving c_a to c_(a+1), indices modulo ell. Let pi be this forward rotation on C and the identity off C. Define cyclic four-windows

    W_a={c_a,c_(a+1),c_(a+2),c_(a+3)}.

For each actual root define

    g_i(C)=|{a: W_a intersect Q_i is empty}|,

and put Gamma(C)=sum_i g_i(C). These counts use actual masks and one actual cycle; duplicate labelled roots count separately because they are separate constraints.

**X46G (actual cycle-gap bound).** If

    Gamma(C)<ceil(ell/2),

then there is a deterministic start a for which BOTH W_a and W_(a+1) are actual four-role covers. Since W_(a+1)=pi(W_a), X45's exact representative criterion follows without enumerating H4 or assuming its global density. If Q_i meets C, g_i is the sum over cyclic complement gaps of max(0,d-3); if Q_i avoids C, g_i=ell.

**X46R (derived renewable upper interface).** Suppose a complete lower-protected repair theorem may choose, at every unfinished restored boundary, a lower-admissible simple cycle satisfying X46G, and edits roots by an endpoint-containing add-before-delete schedule. Choosing the least such cycle and least adjacent good windows makes the SAME physical lower path satisfy tau<=4. If the lower theorem separately supplies tau>=3, same-slot floors, eligible primitives, renewal, strict finite progress and FULL exact restoration, the combined path is direct {3,4}. X46 adds no primitive and preserves a proved endpoint-event minimum.

The gap bound is sufficient, not necessary. Its failure does not negate X45 compatibility or a path.

**X46F (zero-gap two-phase family).** For EVERY q>=2 and h>=2, put H=qh and m=4H. There is an exact-four actual template with every co-triple root plus TWO sparse residue roots of width H. Its full four-cover density is strictly BELOW one half, but each of q block cycles of length 4h has Gamma=0. With singleton groups and the q block rotations as destination, accepted X40L plus X46G/X45 give q renewable saturated long handovers, direct 3<=tau<=4, the endpoint-toggle minimum and FULL labelled/noncompact restoration.

The saturated floors have two grades H and m-3. The family lies outside X38, X39, X40U, X41, X43 and X44 sufficient inputs. L already connects the symmetry endpoints. The advance is derivation of upper compatibility from actual root gaps, not new connectivity or a universal lower theorem.

## 2. Bad windows, cyclic adjacency and exact orientation

For a start a, W_a fails to cover the template exactly when some actual mask Q_i is disjoint from it. Let

    B_i={a: W_a intersect Q_i is empty},
    B=union_i B_i.

Then |B_i|=g_i(C), B is precisely the set of bad starts, and the union bound gives

    |B|<=sum_i g_i(C)=Gamma(C).

No independence and no separate root capacity is assumed. The same root may contribute many bad windows and many roots may miss the same window; the union bound only overcounts.

Because all quantities are integers, Gamma(C)<ceil(ell/2) implies

    |{good starts}|=ell-|B|
      >=ell-ceil(ell/2)+1
      =floor(ell/2)+1.

A subset of cyclic ell positions with no two consecutive positions has size at most floor(ell/2): pair consecutive positions when ell is even; when ell is odd remove one position after choosing a hypothetical occupied start and pair the remaining path. Therefore two consecutive starts a,a+1 are good. Choose the lexicographically least such a.

The ownership orientation is literal:

    pi(c_t)=c_(t+1),

hence pi(W_a)=W_(a+1). Goodness means both windows hit every actual mask, so both lie in H4. Therefore

    W_a in H4 intersect pi^{-1}(H4).

X45 now supplies FOUR SAME physical representatives covering both restored endpoints and every endpoint-containing primitive. This derivation examines only ell actual windows and their root intersections; it does not assume or enumerate all binomial(m,4) covers.

## 3. Rootwise cyclic gap formula

Fix an actual root i. If Q_i intersect C is empty, every window W_a misses Q_i and g_i(C)=ell.

Otherwise remove the roles of Q_i intersect C from the cyclic order. The remaining roles split uniquely into maximal linear gaps of lengths d_1,...,d_t>=1. A four-window misses Q_i exactly when all four of its consecutive roles lie inside one gap. A linear gap of length d contains

    max(0,d-3)

four-consecutive windows. Different maximal gaps supply disjoint starts. Thus

    g_i(C)=sum_s max(0,d_s-3).

This makes Gamma an actual incidence statistic. Roots meeting the cycle at least once every four positions have g_i=0. Sparse roots may satisfy that condition; large mask width is not required.

The formula also shows why Gamma is only sufficient. Bad-window sets from different roots can overlap heavily, so their sum may reach half even while their union does not. X45's exact orbit intersection may also hold with only one adjacent good pair. X46 never promotes the union bound to necessity.

## 4. Renewal and division of proof duties

At a restored boundary, suppose the lower theorem can process a gap-admissible cycle. X46 deterministically chooses four physical representatives from W_a: selected labels on the cycle roles and fixed representatives elsewhere if needed. Here W_a is inside C, so all four are selected. Their old owner set is W_a and their next owner set W_(a+1), both covers.

During additions each active root contains its old endpoint; during deletions it contains its next endpoint; other roots are old or completed next. The SAME four labels hit every partial support, proving tau<=4.

Actual pair witnesses, tau>=3, floor legality, the actual root order, literal incidence availability and a next ownership cycle are not consequences of Gamma. They must be proved by the lower theorem on this SAME path. At handover completion, group sizes and masks restore, so every g_i for the next selected cycle is computed from the same actual template. No root or representative is consumed.

If an unfinished boundary always has a lower-admissible gap cycle, select the least one. A lower progress measure decreasing after each finite handover proves termination. Since X46 adds no edit, common incidences and endpoint-differing event counts remain exactly as established below. No maximum-layer conversion is used for the direct band.

## 5. The two-phase residue template

Fix q>=2,h>=2. Put H=qh>=4 and m=4H. Partition G into q disjoint cyclic blocks C^1,...,C^q, each of length 4h. Index positions in every block modulo four.

Declare the following labelled original masks:

1. Q_T=G minus T for EVERY three-role set T subset G;
2. D_0, the union of positions congruent to 0 modulo four in every block;
3. D_2, the union of positions congruent to 2 modulo four in every block.

The sparse roots D_0,D_2 are disjoint and each has width H=m/4. There are binomial(m,3)+2 original roots, with no duplicate masks.

Every at-most-three role set S is missed by Q_T for some three-set T containing S; in particular a three-set T misses its complementary root Q_T. Conversely every four-set hits every Q_T because it cannot be contained in a three-set. A four-set covers the full template exactly when it also meets D_0 and D_2.

A four-consecutive window inside any block contains one role in each residue class. It meets both sparse roots and hence is a four-cover. Therefore the template transversal is EXACT FOUR and

    H4={I subset G: |I|=4, I intersects D_0, I intersects D_2}.

This family is defined by actual masks. The compatible windows are consequences of those masks, not supplied members of an abstract cover family.

## 6. Exact cover count and failure of global majority

The roles outside D_0 number 3H, as do those outside D_2; roles outside both number 2H. Inclusion-exclusion gives

    |H4|=binomial(4H,4)-2binomial(3H,4)+binomial(2H,4).

Twice the excess above half of all four-sets is

    2|H4|-binomial(4H,4)
      =binomial(4H,4)-4binomial(3H,4)+2binomial(2H,4)
      =H(-3H^3+14H^2-11H+2)/2.

Let f(H)=3H^3-14H^2+11H-2. Direct substitution gives f(4)=10. Its derivative is

    f'(H)=9H^2-28H+11,

which is positive at H=4 and strictly increasing thereafter because f''(H)=18H-28>0. Hence f(H)>0 for every H>=4, so the displayed excess is strictly negative. Thus

    |H4|<binomial(m,4)/2

throughout the declared family. X44's global-majority hypothesis genuinely fails.

## 7. Zero actual gap budget and q long handovers

For any block cycle C^s, every four-window meets D_0 and D_2. It also meets every co-triple Q_T because a four-set cannot lie inside T. Therefore

    g_i(C^s)=0 for EVERY actual root i,
    Gamma(C^s)=0<ceil(4h/2).

Give every role one actual label x_j. The source groups are singletons. Send x_j to the next role in its own block at the destination. The misplaced ownership graph is exactly q disjoint directed cycles, each of length 4h>=8, with no shorter cycle.

At an unfinished boundary, choose the least remaining block cycle. X46 supplies two consecutive covering windows. The four physical labels in the first window all move, and their new owner roles form the next window. There is no unselected label in any active group.

Completing one block cycle fixes its 4h labels and leaves the other block cycles unchanged. The actual masks, singleton group sizes, pair redundancy and zero gap budgets restore. The incorrect-owner count decreases by 4h. Exactly q finite handovers reach every destination singleton and every FULL labelled/noncompact destination root.

## 8. Lower protection, floors and exact event count

For a palette pair K, a co-triple root Q_T avoids K exactly when K subset T. There are m-2 choices for the third role of T. Thus every pair has at least m-2 actual avoiding roots. A pair with one role in D_0 and one in D_2 is avoided by neither sparse root, so the actual minimum redundancy is exactly

    rho=m-2.

Accepted X40L requires

    binomial(2rho,rho)>m(m-3)/2.

Here

    binomial(2rho,rho)
      =binomial(2m-4,m-2)
      >=binomial(2m-4,2)
      =(m-2)(2m-5),

and

    (m-2)(2m-5)-m(m-3)/2
      =(3m^2-15m+20)/2>0

for m>=16. Therefore X40L supplies the complete lower-protected path on the SAME selected block cycles: actual conditional root orders, every pair witness, tau>=3, literal add-before-delete primitives, same-slot floors, renewal, strict progress and exact restoration.

At singleton sizes, a co-triple root has cardinality m-3 and each sparse root cardinality H. Allow arbitrary SAME original positive floors up to those cardinalities. In particular the unequal saturated vector is

    a_(Q_T)=m-3,   a_(D_0)=a_(D_2)=H.

All floors are at least four. X40's endpoint-containing schedule preserves them without reserve. Combining X40L with Sections 2 and 7 gives a direct {3,4} path.

Each label moves in exactly one resolving block cycle, directly from its original to final owner. A mask containing both owners keeps the incidence; one containing neither stays absent; one containing exactly one toggles its endpoint-differing incidence once. X40L's preliminary path therefore has exactly

    sum_i |A_i symmetric_difference C_i|

primitives. X46 adds none. This is a mathematical minimum, not a runtime benchmark.

## 9. Separation from prior sufficient classes

**X38:** every nontrivial ownership cycle has length 4h>=8, outside its no-cycle-longer-than-three premise.

**X39:** the actual D_0,D_2 masks have width H=m/4<m-3, so the all-mask dense-width premise fails.

**X40U:** every role group is singleton, so no minimum four-cover has two unselected representatives per role. X40L is used only for lower safety.

**X43:** choosing actual S=D_0 gives p=H and a sufficiently large complement, but its EVERY one-S/three-complement cover property fails: take one D_0 role and three distinct roles in G minus (D_0 union D_2), which has size 2H>=8; that four-set misses D_2. Choosing D_2 fails symmetrically. Choosing a co-triple root gives p=m-3 and complement size three, violating n>=p+3. These exhaust all actual roots.

**X44:** Section 6 proves strict global majority false.

**No singleton representation:** the co-triple roots distinguish every pair of roles. For a!=b choose a three-set T containing a but not b; Q_T omits a and contains b. Hence all role incidence profiles are distinct. Any cell in any union-partition representation of the SAME endpoint must be profile-homogeneous. D_0,D_2 each contain H>=4 distinct profiles and each Q_T contains m-3 distinct profiles, so no actual root can be one cell. X41's singleton direct input is unavailable in every same-endpoint representation.

X45 remains the inherited exact upper criterion that X46 satisfies; X46 does not claim to supersede it. All separations above concern accepted sufficient inputs, not impossibility of other mechanisms. L already supplies symmetry connectivity.

## 10. Saturated controls and unsafe whole union

Only two original roots have the low saturated floor H. Any four pairwise disjoint floor-safe supports require total size at least

    2H+2(m-3)=5m/2-6>m=|P|.

Thus four private/disjoint saturated supports cannot fit anywhere. This is a method obstruction, not native disconnection.

In one block choose labels x_a and x_(a+2). Their source/destination footprints are

    {a,a+1} and {a+2,a+3}.

Their combined footprint is one four-window, which covers every actual mask. Therefore at least one of the two labels occurs in every rootwise whole endpoint union. The pair hits the entire union tuple, so its hitting number is at most two. Simultaneous whole-union preparation is unsafe.

Every original root changes. D_0 rotates to residue class one and D_2 to residue class three. If a co-triple Q_T were invariant under the product of block rotations, its three-role complement T would be invariant. Each role orbit is a full block of length 4h>=8, so a nonempty invariant set is a union of full blocks and cannot have size three.

X40 transfers lower pair protection root by root while X46 derives a moving upper cover from zero actual gaps. Neither uses private guards or the unsafe whole union.

## 11. Advance and exact remaining obligation

X46 converts actual root incidence along a lower-selected cycle into orbit-compatible upper protection. The maintainable quantity is a cyclic gap budget: root omissions may overlap, but if their total cannot occupy half the starts, two consecutive actual covers must exist. Sparse roots can have zero gap budget, so the theorem is not a disguised dense-width requirement.

The condition is sufficient, not necessary. Gamma may overcount overlapping bad windows; X45 may succeed beyond it. X46 does not prove an arbitrary endpoint has a qualifying representation or a gap-admissible next cycle. It assumes a lower theorem can process the chosen cycle and that such a cycle exists at each restored boundary. X46 supplies neither pair protection nor floor legality.

Same supplied exact-four masks, equal positive corresponding group sizes, a typed endpoint-containing lower handover and derived gap-cycle availability remain inputs. Unequal corresponding sizes, below-X40 lower repair, universal derivation of a qualifying cycle, arbitrary mixed-floor/directed/higher-target/nested connectivity and physical interpretation remain OPEN. Stronger compatible-grade availability remains parallel.

No scientific commands, enumeration, numerical workflow, implementation, benchmark, integration merge, numbered certificate, literature-originality or physical energy/metric/gravity/fundamental-time claim. v16.55/v16.54, frozen prior sources and all original evidence remain unchanged. Separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped.

Fresh independent whole review must check X46G/R/F together: exact bad-window union and gap formula; cyclic adjacency/orientation; endpoint-containing lift; lower/upper separation; exact template and cover count; below-half polynomial; zero gaps; pair redundancy/X40 inequality; unequal saturated floors; q-cycle renewal/progress/event minimum/full restoration; exhaustive method/profile separations; private/whole-union controls; and all domain limits.
