# A11.X6: a sharp existence obstruction for X5 guard accessibility

Frozen analytical scope: A11_X6_SCOPE.md at ed2da70fc8c59748e8598362dc88d2bace8cf6b1.
Parent publication: 02b15a4787cc592e354b539095acf1ed1d6b295f.
Fixed ordered palette P, r labelled slots, ORIGINAL floor three at every slot; ALL supports of size at least three are permitted. Target four. This is a symbolic theorem, not enumeration or a connectivity certificate.

## 1. Exact statement

For a selected slot s, let G_s consist of exact-four tuples E with a triple T subset E_s, a four-label hitting set H with T intersect H nonempty, and the actual other roots disjoint from T of residual transversal at least two on R=P minus T. These are precisely X5's entry conditions.

**Theorem X6.**
(a) If |P|=6, exact-four feasibility forces all twenty distinct triples to occur as actual supports; hence r>=20. Moreover G_s is empty for every s, for any r.
(b) If |P|=7, G_s is nonempty if and only if r>=13, for every labelled choice of s. In particular G_s is empty for all s when r<=12, even allowing noncompact supports.
(c) Exact-four states DO exist with |P|=7,r=12. Thus the empty X5 target class on that carrier is not simply infeasibility. No route from any of its exact-four endpoints can reach a qualified exact-four state at any slot. This is an obstruction to Route A's target, not to native exact-endpoint connectivity.

No assertion is made that all endpoints reach G_s when r>=13. No new lower-guard path, guaranteed complete repair or nested barrier is claimed.

## 2. Six-label precheck

Every triple K fails to hit an exact-four tuple. Some actual support avoids K and is contained in P minus K, a set of size three. The original floor forces that support to equal P minus K. Different K force twenty distinct supports and therefore at least twenty slots. Conversely the family of all twenty triples has hitting number four: every triple misses its complement and every four-set meets every triple.

For any candidate anchor triple T, R has size three. Every root disjoint from T must equal R. Any nonempty such family has residual hitting number one; the empty family has hitting number zero. Hence none satisfies X5's residual condition, regardless of r. The twenty-triples control is already solved by accepted uniform-slot AC and must not be called a native obstruction. This excludes k=6 from the residual r<=19 domain.

## 3. Reduce a seven-label qualified state without restricting the native graph

Assume E belongs to G_s. Compact the anchor to its supplied T, retaining T intersect H. Then compact every other support to three labels while retaining one of its labels in H. Each deletion is an actual legal primitive, retains original floor three and the supplied four-cover, and cannot decrease hitting number. Thus every intermediate remains EXACT FOUR. The finite deletion count strictly decreases until all supports are triples; a next deletion exists whenever a support exceeds size three, by choosing a retained three-set containing an H label.

Original roots disjoint from T remain disjoint. Deleting incidences can only increase their residual transversal, so their residual level remains at least two. Additional roots may become disjoint and cannot lower that level. H continues to hit T and every root. Therefore the compact tuple is still in G_s with the SAME slot and supplied cover.

This exact compaction is used to prove an existence lower bound; it is not a restriction on the allowed reconfiguration paths. In particular the bound excludes qualified noncompact states as well as triple-only states.

## 4. Four residual roots and eighteen coupled endpoint obligations

Write T={a,b,c}, R={x,y,z,w}. Every compact root disjoint from T is R minus one residual label. Their residual transversal is at least two exactly when their intersection is empty. Thus all FOUR distinct residual triples R minus v, v in R, must occur on actual distinct nonanchor slots.

These four roots plus the compact anchor occupy at least five slots. They do not witness avoidance of any triple {t,u,v} with t in T and {u,v} subset R: the anchor meets t, and a residual triple on four labels cannot avoid two residual labels. There are eighteen such forbidden triples (six for each t). Exact four requires another actual root to avoid each.

Classify every remaining compact slot by its number of anchor labels:
- Three anchor labels: the support is T and supplies none of these witnesses.
- Zero anchor labels: another residual triple and supplies none.
- Two anchor labels: support (T minus {t}) union {v}. It can witness only the obligations indexed by this ONE t, and witnesses a residual pair precisely when that pair omits v.
- One anchor label: support {t} union D, |D|=2 inside R. It witnesses only the residual pair R minus D, for each of the TWO anchor labels other than t.

The one-anchor roots therefore participate in two protection systems simultaneously. They are counted as shared slots, never as independent capacity.

## 5. At least eight more slots

Let m_t count the remaining two-anchor slots whose missing anchor is t, with multiplicity, and let p count remaining one-anchor slots. Put m=m_a+m_b+m_c.

For each t, a residual pair receives no witness from the m_t slots exactly when it contains every distinct residual singleton used by those slots. If d_t is the number of those distinct singletons, the number of unwitnessed pairs is C(4-d_t,2) for d_t=0,1,2 and zero for d_t>=3. Since d_t<=m_t, it is at least

f(m_t)=6,3,1,0 for m_t=0,1,2,>=3 respectively.

Each such remaining obligation must be witnessed by a one-anchor root. One such root supplies at most TWO obligations across ALL three t systems, so

2p >= sum_t f(m_t).

For every nonnegative integer u, f(u)>=5-2u: this is immediate at u=0,1,2 and the right side is negative at u>=3. Consequently

2p >= 15-2m,
2(m+p)>=15,
m+p>=8.

Together with the anchor and four distinct residual supports, r>=5+8=13. Duplicated supports and other slot types cannot improve the bound. This proves emptiness for r<=12 and explicitly accounts for shared witness capacity.

## 6. Sharp thirteen-slot construction

Use P=T disjoint-union R as above. Assign T to the selected labelled slot s; assign the following twelve distinct triples to twelve other existing labelled slots:

1. All four residual triples R minus v, v in R.
2. For each t in T, the two triples (T minus {t}) union {x} and (T minus {t}) union {y}: six roots.
3. The two triples {a,z,w} and {b,z,w}.

All original floors hold. The four residual roots have empty intersection, so their residual transversal is two. H={a,b,x,y} meets T and every listed support, proving tau<=4.

Every triple K fails to hit:
- If K lies in R, it misses T.
- If K=T, it misses any residual root.
- If K contains two anchors and residual v, it misses R minus v.
- If K={t,u,v} with one anchor and two residual labels, and {u,v}!={x,y}, at least one of x,y lies outside {u,v}; the corresponding root (T minus {t}) plus that label avoids K.
- If K={t,x,y}, choose {a,z,w} when t!=a and {b,z,w} when t=a.

This exhausts all triple types. Any hitting set of at most three labels extends to a triple, so tau>=4. The state is exact FOUR, meets all X5 entry conditions, and uses thirteen original slots. For any r>13 use P in the remaining existing slots; those supports are hit by H and do not alter exactness or the guard. The same construction works at every chosen slot s. Hence r>=13 is sufficient for NONEMPTINESS, completing part (b).

As a small guard-creation illustration, add c to the root R minus x in this construction. The tuple stays exact four: the only old triple-avoidance witnesses potentially lost are {a,b,c}, {a,c,x}, {b,c,x}, and these still miss respectively another residual root, {b,z,w}, {a,z,w}. The cover H persists. At the fixed anchor s=T, the remaining T-avoiding residual roots now have intersection {x}, so that particular entry fails. Deleting the added c legally restores exact-four qualification at s in one primitive. This illustrates protection created from an existing relationship; it is NOT offered as a new universal accessibility class, and no claim excludes qualifying entries at other slots.

## 7. Nonvacuous twelve-slot control

Partition seven labels into U,V,W of sizes 3,2,2. Include all internal triples and all directed UUV,VVW,WWU triples. There are

C(3,3)+C(3,2)*2+C(2,2)*2+C(2,2)*3=1+6+2+3=12

distinct actual supports, all at floor three.

Every four-label set contains one of these roots. A distribution with three labels in one part contains an internal triple. A (2,2,0) distribution has an occupied directed adjacent pair whose source contributes two labels. A (2,1,1) distribution has the successor of its doubled part present. These supply a directed core triple. Thus no four-set is independent. A triple with one label in each part contains no root and is independent. Therefore the independence number is three and the hitting number is seven minus three, EXACT FOUR.

This verifies feasibility directly. It is also an endpoint in the already accepted CYCLIC_TRIPLE_CONNECTIVITY Theorem AA class, which connects any two such cyclic-core endpoints at fixed r,k. It is NOT a new disconnected example or new positive connectivity class. Nevertheless by Sections 3-5 NO exact-four state whatsoever on this twelve-slot carrier, cyclic or otherwise and compact or otherwise, belongs to any G_s.

## 8. Consequence for the assignment and inherited limits

Route A cannot be a universal explanation for the seven-label, twelve-slot carrier: its required exact-four target does not exist. Even unlimited native paths, intermediate supports above their floors, temporary incidences, repeated toggles, upper-layer removal and endpoint root permutations cannot create a final state in an empty class. This is the strongest target-existence obstruction, not a failed chosen schedule and not a no-path certificate between exact destinations.

The assumption removed is that the needed X5 class can always be made available on a feasible floor-three carrier. Existing exact-four relationships can instead provide coupled pair protection without any all-triple-avoiding guard. A replacement mechanism must therefore carry those obligations directly, or use another accepted class, in this slice.

No new repair path is supplied by the counting theorem. Safety and renewed progress for cyclic-core endpoints remain those of accepted AA; they are not recertified here. X5's prepare/exchange/restore/termination theorem is unchanged. The thirteen-slot construction proves existence only, not reachability from arbitrary endpoints; same-slot alignment for arbitrary endpoints is consequently not assumed.

Dependencies/domain disposition: elementary exact compaction is proved in Section 3 using the supplied H. X5's input definition is read from its frozen proof. Accepted AC applies to the six-label control at r>=20 (h=3,q=4,N=C(5,3)=10). AA applies only to the displayed cyclic core and its declared redundant extras. General maximum-layer Theorem A requires an actual finite lower path and cannot create one or change target existence; it is not used to prove X6. Symmetry L/M preserves the fixed palette/floors and cannot change the bound; no arbitrary mixed-floor permutation is used. Disjoint guard AB requires actual compatible guards and is not assumed; palette-room AE requires k>=3r, which fails at k=7,r=12; element-cover C alone cannot preserve the needed pair covers and is not invoked. The coarse remaining uniform domain r<=19,k<=3r-1 is a guide, not an enumeration instruction. This packet proves no classification for k>=8 or connectivity of all seven-label endpoints.

All native rules and prior frozen results remain intact. Universal A11 destination-directed scheduling, all remaining native connectivity and unrestricted nested universality remain OPEN. No new physical implication, geometry, fundamental time, efficiency measurement, originality claim, numerical execution, implementation or integrated certification is made.
