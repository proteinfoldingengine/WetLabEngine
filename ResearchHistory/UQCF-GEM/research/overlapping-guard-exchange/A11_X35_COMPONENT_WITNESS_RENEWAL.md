# A11.X35 — component-wise coupled witness renewal beyond the global count

Scope freeze: c003ea6c3d26d43c656358f4ee4559e6b84846fb.
Analytical parent: a287ed73db909eaf254ceece2d3d0cbb736b105e.
Status: exact candidate for fresh independent whole-argument review. Analytical only.
Completed bounded v16.55 and certified v16.54 are unchanged.

## 1. Exact statements and domain

Fix an ordered palette P with k>=4, r labelled slots, and ORIGINAL positive floors a_i<=k. Every root E_i subset P has |E_i|>=a_i. A native primitive toggles ONE incidence in ONE root. All permitted larger supports, repeated changes and arbitrary temporary incidences remain available. The theorem chooses a sufficient one-pass method without imposing it on native admissibility.

Let A,C satisfy tau(A),tau(C)>=3. For every pair K subset P define ACTUAL sets

    U_K={i:A_i intersect K empty},
    V_K={i:C_i intersect K empty}.

They are nonempty. Let B be the pairs with U_K intersect V_K empty. Construct a graph on the ORIGINAL root indices by connecting all indices in U_K union V_K for EACH K in B. Isolated indices are included. Let J range over its connected components. Each noncommon pair belongs to a UNIQUE component containing its ENTIRE witness union. Define

    Phi_J = sum over K in B with U_K union V_K subset J
                            1/binomial(|U_K|+|V_K|,|U_K|).

**X35D — exact decomposition of the chosen method.** A globally safe whole-root add-then-delete order exists if and only if EVERY interaction component has a local order in which first(V_K)<last(U_K) for all its noncommon pairs. Local orders can be concatenated in any component order.

**X35C — derived component completion.** If Phi_J<1 for EVERY J, there is a deterministic finite native A -> C path with tau>=3, respecting every ORIGINAL floor and restoring the FULL labelled/noncompact destination. Local conditional averaging supplies an eligible next root at every certified local prefix. The preliminary path has exactly sum_i |A_i symmetric_difference C_i| primitives.

**X35R — renewal.** Any finite specified chain on the SAME original carrier whose adjacent pairs satisfy X35C has complete finite lower repair through its full labelled waypoints. The next interaction graph/counts are rebuilt from restored ACTUAL endpoints; no slot or reserve is consumed. A certificate may persist at level three inside a handover.

**X35B — exact-four band.** For original exact-four outer ends, first finish the ENTIRE lower path and then apply accepted maximum-layer theorem A. This yields tau in {3,4} and the exact labelled outer destination. Conversion need not preserve the preliminary schedule, length or inexact internal waypoints. If each intended waypoint is exact four, conversion can instead be applied separately to completed adjacent lower segments.

**X35F — strict nonvacuous improvement.** For every even m>=6, Section 5 gives exact-four endpoints on k=2m and unequal original floors m-1/m. X34's GLOBAL count is exactly m/6, hence fails its strict condition and grows without bound. The distinct pair events also number m; eliminating duplicate events does not fix that bound. EVERY interaction component has weight1/3. A specified native {3,4} handover has a critical tau3 state where neither old nor new roots independently protect, even with the fixed background included in both families. That background has tau2; the full endpoint UNION also has tau2. Repeated module handovers have an eligible decreasing assignment measure and reach any specified assignment in the declared family.

This strengthens a DERIVED sufficient bound, not the native rule set. The symbolic family's symmetry-related endpoint connectivity is already covered by accepted M; it is not claimed outside all earlier connectivity results. The new claim is component availability/renewal with unbounded global failure weight and actual combined protection.

## 2. Why the interaction graph is the right object

For any chosen root order, process slot i by adding C_i minus A_i individually, then removing A_i minus C_i individually, using the palette order. During additions the support contains A_i; during deletions it contains C_i. Its own ORIGINAL floor holds throughout, and every intermediate support is contained in A_i union C_i.

For K with a common witness i, both endpoint supports avoid K. That actual root's union and all its intermediate supports avoid K, regardless of when it changes. It is not necessary to hold its support unchanged.

For a noncommon pair, the inherited A2/X34 order criterion is

    first(V_K)<last(U_K).

Before that first destination root completes, the last source root remains untouched and misses K, including during the first new root's active union. Afterward the completed new root misses K for the remainder. Thus actual protection holds for EVERY primitive.

If all U_K indices occur before all V_K indices, the visited union of the last U_K root meets K, as its index is not in V_K. All other roots meet K too: every old witness has changed, no new witness is installed, and no common witness exists. So the chosen method loses the lower guard.

Ordering constraints for this pair depend ONLY on its actual U_K union V_K. By graph construction all those indices lie in one component. Restricting a safe global order to each component preserves the same relative constraints. Conversely, concatenate safe local orders. Within each component all relevant relative positions are unchanged; each common witness continues to work regardless of the concatenation. This proves X35D.

The graph is not an extra geometric structure or a partition of independent capacities. It is derived from actual support avoidance. Labels can occur across all components. A root shared by different noncommon obligations joins those obligations into the SAME component. Shared capacity is therefore accounted for, not assigned separately.

## 3. Local counting gives next-move availability

In any component J count ALL permutations of its actual labelled indices. For a noncommon pair with u=|U_K|,v=|V_K|, relative order on those u+v indices has exactly binomial(u+v,u) old/new patterns. Exactly one places every old witness before every new witness. Its fraction is

    1/binomial(u+v,u).

Thus Phi_J is the mean NUMBER of bad events in that local order. Linearity needs NO independence between events inside J. We do not multiply event probabilities or assume different pairs have separate root resources.

For an EXACT ordered prefix D inside J, define Phi_J(D) as the mean bad-event count over all local orders extending D. Its per-pair contributions are the same exact finite counts as X34:

- If no V_K index has been chosen, put u'=|U_K minus D| and v=|V_K|. Contribution is 1/binomial(u'+v,u'), including value1 when u'=0.
- If a V_K index has been chosen, contribution is zero if an old witness remains outside D or an old witness appears after the first chosen new witness. Otherwise every old witness preceded that first new witness, making contribution one.
- Common-index pairs impose no ordering event and need no count.

With n=|J minus D|>0, local completion permutations split equally by next index, so

    Phi_J(D)=(1/n) sum_{i in J minus D} Phi_J(D followed by i).

An eligible next index with nonincreasing mean EXISTS. Choose its least index. From Phi_J(empty)<1 this constructs a local order while retaining Phi_J(D)<1. The remaining local-slot count decreases at each choice. At completion Phi is an integer, hence ZERO.

A certified local prefix therefore has a full safe extension. Safety alone is not asserted to imply extension. One may build the full local orders first and then execute the primitive list. Section 2 proves each resulting actual pair witness throughout every active union, including across component boundaries.

Inside an unfinished root, a missing destination addition exists until all such additions are done; then an old-only deletion exists until the root equals C_i. Each primitive decreases the remaining endpoint symmetric difference by one. Roots already equal their destinations require no move. The finite outer list and primitive count prove termination. No previously processed root is subsequently perturbed by this preliminary construction. EVERY labelled destination incidence is restored.

A convenient derived corollary is: if component J has at most d_J noncommon pair obligations, every one with u,v>=rho_J>=1, and

    d_J < binomial(2rho_J,rho_J),

then Phi_J<1. Binomial(u+v,u) increases when either u or v increases, so this follows directly. Bounds can differ across components. There is NO bound on the sum of d_J or global Phi imposed here.

## 4. Renewal, band conversion and exact dependency limits

For a finite specified chain E^0,...,E^s, restore E^j fully before constructing the next adjacent interaction graph. X35C supplies every next edit and complete next destination whenever its actual component inequalities hold. No fixed disjoint guard is required; the protected obligations can migrate within each component. Within a component the retained certificate is the conditional count below one, even if the current hitting number is only three.

For original exact-four outer ends, concatenate all finite lower segments FIRST, then invoke A. Its required carrier has positive floors, arbitrary incidence additions and componentwise unions, fixed labels/slots, and complete exact-q endpoints. All match here at q4. r>=4 is forced by exact4, so A's arity requirement is satisfied. There is no compactness or destination-monotonicity assumption in A. Its resulting path retains original outer endpoints and floors but may alter internal waypoints/schedule/length. Complete separate exact-four segments may instead each be converted, then concatenated if preserving those exact waypoints matters.

No compact preparation, minimum-cover compaction, same-floor token placement, palette slack, element cover or grade permutation is an INPUT to X35C. Their hypotheses are not silently inferred. X35 uses the accepted actual order criterion and the X34 finite count/conditional averaging, plus A ONLY for the completed lower-to-band conversion. Those frozen sources are not rewritten or recertified.

This remains a one-active-root chosen method. The unbounded participation theorem still prevents claiming universal completeness for bounded-participation architectures. Phi_J>=1 is merely failure of this sufficient count. A safe local order can still exist; lack of every whole-root order still permits interleaved primitives, temporary supports or repeated changes in the native graph. No disconnection follows.

## 5. Infinite unequal-floor control: the global count fails without losing repair

### 5.1 Fixed palette, roots and assignment class

Take an even integer m>=6 and the ordered palette

    P={x_1,y_1,...,x_m,y_m}, K_j={x_j,y_j},
    X={x_1,...,x_m}, Y={y_1,...,y_m}.

These names index actual subsets; they add no native geometry.

Declare 2^m BACKGROUND slots, each of ORIGINAL floor m, indexed by binary words epsilon in {0,1}^m. Its support B_epsilon chooses x_j or y_j according to epsilon_j. Hold these given supports fixed in the construction.

Declare 2m MODULE slots (b,x),(b,y), b=1,...,m, each of ORIGINAL floor m-1. For ANY bijection f from the labelled module blocks to {1,...,m}, specify

    E^f_(b,x)=X minus {x_f(b)},
    E^f_(b,y)=Y minus {y_f(b)}.

Together with the fixed background these are states on ONE fixed carrier. Both original grades are positive and unequal, indeed >=5. All supports equal their original floors. No root is added during repair.

Every E^f is exact FOUR. Any triple containing a full K_j has third label of some other pair and one orientation. The module at the unique block holding j in the OTHER orientation avoids the whole triple. A triple with no full K_j uses three distinct pairs; choose a background support opposite each of those three labels to miss it. Smaller sets extend to triples. Thus no at-most-three set hits all actual roots.

The four-label H=K_1 union K_2 hits every background root. Each module root contains its orientation's label from every pair except its ONE omitted pair, so it hits at least one of K_1,K_2. Hence H hits every root and tau(E^f)=4. It is an actual supplied minimum four-cover.

Background alone has tau2: any full K_j hits every background root, and for any single label there is a background root choosing its opposite. In particular the fixed background is NOT a three-guard.

### 5.2 Exact global and component counts

Take A=E^id and C=E^pi, where pi swaps (1,2),(3,4),...,(m-1,m). Source and destination have the SAME background, palette, labelled slots and original floors.

For a full pair K_j, exactly the two source module roots at block j avoid it. Every other module root contains its orientation's j label, and every background contains one label of K_j. Thus

    U_Kj={(j,x),(j,y)},
    V_Kj={(pi(j),x),(pi(j),y)}.

They are disjoint sets of size TWO. For every pair using labels from distinct K_j, an unchanged background root chooses the opposite labels at those two indices and misses it. Such pairs have ACTUAL common witnesses. These two cases exhaust all palette pairs.

Consequently the noncommon bad events are EXACTLY the m full pairs, each contributing1/binomial(4,2)=1/6:

    Psi_X34(A,C)=m/6>=1.

No two of these event records have identical ordered U,V sets. This failure is not an artifact of duplicating many identical pair patterns.

For each transposed block pair j,l, the interaction component consists of FOUR module indices, with just the two reciprocal events K_j,K_l. Its weight is

    Phi_J=2/6=1/3<1.

All background slots are isolated zero-event components. X35C applies for EVERY even m>=6, while the global sum grows without limit. This is a strict derived-bound improvement on actual feasible exact endpoints.

The full source/destination union tuple has tau2. For each swap j,l, same-orientation module unions equal X or Y respectively. A full K_s hits X,Y and all fixed backgrounds. No singleton hits the background. Therefore there is no static three-guard consisting of these union-compatible supports; even the entire union is only level two.

### 5.3 X33's actual simultaneous-good-label entry fails

The module grade has 2m roots and threshold floor(2m/2)=m. Any x_j is absent from all m y-oriented module roots and the ONE x-oriented root omitting j: m+1 absences. The same count holds for y_j. Thus EVERY label fails the module grade's actual good-label condition at both endpoints.

The background grade has exactly 2^(m-1) absences for each label, equal to its half-grade threshold; it cannot fix failure in the other grade. The module grade's scalar bad-count bound is already

    floor(2m*(m+1)/(m+1))=2m=k,

so the strict total grade bound also fails. This excludes precisely X33's entry mechanism. It does not exclude other guards or previously proved repair.

### 5.4 Explicit coupled handover and direct band safety

For the FIRST transposed block pair j=1,l=2, complete root replacements in this order:

    (j,x), (l,x), (j,y), (l,y).

Each replacement adds the ONE missing destination label and removes the ONE old-only label. For example

    X minus {x_j} -> X -> X minus {x_l}.

Its original floor m-1 holds; its temporary size is m. No incidence outside P or new root is used. Across these four roots the current support is always a source, union or destination at its SAME slot.

For K_j the first new witness (l,x) precedes the last old witness (j,y). For K_l the first new witness (j,x) precedes the last old witness (l,y). Every other full pair has its untouched module witnesses, and every cross-pair retains its actual fixed background witness. This accounts for ALL pairs through ALL primitive edits. Hence tau>=3.

The supplied H=K_1 union K_2 hits both endpoint supports in each root and therefore every intermediate support containing either its source or destination. It also hits the unchanged background and other module roots. Thus tau<=4 DIRECTLY in this symbolic construction. No upper-conversion theorem is needed for this control. It uses eight primitives per transposed module-block pair, hence 4m primitives for the disjoint-swap endpoints.

After the FIRST THREE roots have completed, their new supports are

    (j,x): X minus {x_l},
    (l,x): X minus {x_j},
    (j,y): Y minus {y_l}.

The fourth still has old support Y minus {y_l}. All other module blocks remain old.

The remaining OLD family, even including the fixed background, admits the pair K_j as a transversal: all its module roots omit other pair indices and hence meet K_j. The completed NEW family, also including the SAME fixed background, admits K_s for any s outside {j,l}: each completed module support includes its s label. Such s exists because m>=6. Thus neither side alone provides a three-guard; allowing the background in both sides does not change that conclusion.

The combined tuple still excludes every pair transversal by the actual witnesses above. Its ONLY missed root for K_j is the installed (l,x) root X minus {x_j}. Pick x_s from that support. Then K_j union {x_s} hits all roots, giving tau<=3. Therefore the combined state is EXACTLY THREE.

The next root (l,y) can still be repaired: while it changes, installed (l,x) protects K_j, installed (j,x)/(j,y) protect K_l, and every other pair retains the witnesses already described. This supplies a literal next primitive and full renewal, not an assumption that every safe prefix can finish.

The conditional count also certifies it. After the first local root, the only possible bad event has fraction1/binomial(3,1)=1/3. After the second root, both reciprocal events are impossible because a new witness has preceded a still-unprocessed old witness in each system; Phi_J(D)=0. The remaining roots can complete while preserving the certificate, including the critical level-three state.

### 5.5 Repeated handovers and arbitrary labelled module assignment

For arbitrary E^f,E^g in this stated family, if f!=g choose the least misplaced block b and find the UNIQUE block c with f(c)=g(b). It exists because f is a bijection. c!=b and c is misplaced too: if it were correct, injectivity of g would give c=b.

Swap the two assigned pair indices f(b),f(c), performing the same four-root alternating handover at their existing x/y module slots. The only noncommon pair events for this adjacent exact endpoint swap are the two swapped full pairs; all cross-pairs retain background witnesses and every untouched full pair has common module witnesses. Its component weight is1/3. The eight primitive sequence just proved is therefore eligible, including when its intermediate hitting number is three.

After the swap block b is correct, and no previously correct block was changed. The number of incorrect module assignments strictly decreases. Whenever positive, the unique holder supplies an eligible next swap. At most m-1 swaps suffice: a bijection cannot have just one incorrect position, so the nonzero count cannot stop at one.

Every completed swap is another exact-four E^f with original module/background supports and the same actual reserve structure. Continue finitely to E^g, restoring EVERY labelled module root and every already unchanged background root. H=K_1 union K_2 remains a four-cover throughout, so the entire repeated path is directly in {3,4}. Its count is at most8(m-1) primitives. No general efficiency or optimality claim is made.

This constructor is symbolic and finite for each m. The binary words index declared root supports, not an executed enumeration, an added probability law or an external design.

## 6. Scientific advance, comparisons and remaining obligation

X34 required a GLOBAL finite mean below one. X35 shows that ordering obligations should instead be grouped by the actual roots they share. Each connected interaction group can renew protection locally while the other groups retain old/new witnesses; the count need not remain small globally. Dependencies INSIDE each group are accounted for jointly by exact conditional averaging.

The symbolic family supplies arbitrarily large total failure weight, with all distinct events and uniformly bounded local weight. Its unchanged background is only level two. At the critical stage old and new collections individually admit two-label transversals, yet their combined actual relations enforce level three and a certified completion. This is a derived availability and repeated-handover explanation, not another passing-case count or assertion of schedule existence.

The family's endpoints are already related by permitted original-grade root permutations. Accepted M connects them, since all module tokens have the common original floor m-1 and are swapped only among those slots; background stays in its own slots. No arbitrary illegal mixed-floor permutation is inferred. The new result is NOT a new connectivity classification outside every accepted result. It is a stronger quantitative handover interface and strict improvement over X34's count, with explicit progress at the coupled stage.

Unrestricted mixed-floor root connectivity, broader destination-directed scheduling, higher-target and nested universality remain OPEN. Component failure is not disconnection. Interleaved/repeated temporary supports may succeed where no whole-root order exists, and their general renewable certificate remains the next deeper obligation. Stronger compatible grade bounds remain a parallel direction. No scientific execution, new numerical scope, implementation, benchmark, physical claim or numbered certificate is made.

## 7. Pinned dependencies for whole-argument review

At analytical parent a287ed73db909eaf254ceece2d3d0cbb736b105e:
- A11_X34_COUPLED_WITNESS_HANDOVER.md, blob b9b4fde21b3b830f99e158ad909d2ac440d8e469, and its fresh whole-argument review: inherited event fractions and conditional averaging.
- SEQUENTIAL_HANDOVER.md, blob b754237cf56ab4592eec82c81ebf00817f85ab43: exact whole-root order criterion.
- A11_X33_SIMULTANEOUS_GRADE_GUARDS.md, blob ef93c4010d7f22c1db18c349de06ad9f54a429a1: actual half-grade good-label condition.
- METHOD_COMPLETENESS_DECISION.md, blob 9fef91b043adc787b42d18f6c441d58f5de549af; UNBOUNDED_REPAIR_PARTICIPATION.md, blob bdab80fa21cf830f5ee012f616d075489ef93e57: method nonuniversality.
- GUARD_HANDOVER/CYCLE_BUFFER/ADAPTIVE_BUFFER_RENEWAL: older fixed/adaptive guard mechanisms remain unchanged.

At certified v16.54 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f:
- ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/GENERAL_PARENT_CONNECTIVITY.md, blob 922ae44713c6810c5a99716c52ecb37738a880a6: A, ONLY band conversion dependency.
- Same directory OVERLAPPING_CLIQUE_EXCHANGE.md, blob 865f0797892a2e5e869ec2180d3c842026889445: M, comparison explaining already-solved symmetry connectivity, not needed for new constructive proof.

No frozen source is modified or recertified. Analytical scope discloses prior reasoning. Fresh review must cover the full component decomposition, every actual pair, shared root capacities, next choices, complete restoration, repeated swaps and inherited domains.
