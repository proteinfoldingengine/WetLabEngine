# A11.X9 — exact endpoints force a strictly smaller actual guard

Scope commit: 7664ed65aac533f16f39740483dc5019055f217f.
Parent publication: 1fd30df860324402c5c5c6e11af2df3f10d3923f.
Integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Analytical candidate, frozen for fresh whole-argument review. No implementation or numerical execution.

## 1. Statements on the fixed native carrier

Fix a finite ordered palette P of size k, r labelled root slots and uniform ORIGINAL floor h>=2. Every root is a subset of P of size at least h. A primitive adds or deletes one incidence in one root, retaining its original floor. Consider feasible exact-q endpoints, q>=3, and set t=q-1 and

B=binomial(h+t-1,h)=binomial(h+q-2,h).

**Lemma X9G (strict actual-guard bound).** After legal exact minimum-cover-retaining compaction, every endpoint has an ACTUAL t-guard on at most B-1 existing slots.

**Theorem X9 (complete repair).** Put

G=min(floor(r*(k-h)/k), B-1).

If r>=2G-1, every such endpoint pair has a finite native primitive path with transversal in {q-1,q}, ending at the complete original labelled destination, including every initially noncompact incidence.

The endpoint-sensitive statement replaces the uniform G by the sizes m_A,m_C of any actual endpoint guards obtained after exact compaction: r>=m_A+m_C-1 suffices. One may choose the smaller guard supplied by X7G or X9G at EACH endpoint separately.

**Palette-independent corollary.** r>=2B-3 suffices, for every feasible palette size. In particular uniform floor three, target four needs only r>=17, improving the inherited sufficient threshold nineteen across ALL palettes. This is a sufficient bound, not a sharpness or necessity statement.

Combined with accepted X8, all seven-label uniform-floor-three exact-four endpoints are now covered except possibly carriers r=14,16, before excluding accepted endpoint subclasses. This arithmetic is a consequence of the general guard mechanism, not a new campaign at r=18. Larger-palette carriers at r=17,18 are also covered without an incidence-degree assumption.

## 2. Exact compaction and smallest actual guards

At an exact-q endpoint E choose a minimum hitting set H, |H|=q. In each actual root retain an h-subset containing a label of H. Delete all remaining incidences one by one. Each deletion meets the floor and retains H as a cover, so tau<=q. Shrinking roots cannot lower tau, so every primitive is exact q. Whenever excess remains, an incidence outside the retained subset is an eligible next deletion; total excess decreases. This finite path ends at an h-uniform exact-q tuple E*. Its reverse later restores the entire original support tuple.

Among all actual subfamilies of E* with transversal at least t, choose one C with MINIMUM CARDINALITY m. It exists because the full tuple has transversal q>t. This is a finite mathematical choice, not a claimed efficient executed search. No native edit is performed when selecting a subfamily.

Minimum cardinality implies inclusion minimality. Removing any edge E_i leaves transversal at most t-1. Adding one nonempty root raises transversal by at most one; therefore tau(C)=t and tau(C without E_i)=t-1. Choose a minimum cover T_i of C without E_i. Then

|E_i|=h, |T_i|=t-1,
E_i intersect T_i is empty,
E_j intersect T_i is nonempty for every j!=i.

The first disjointness is necessary because otherwise T_i would cover C. Repeated supports cannot occur in C: removing one duplicate would leave the same cover condition. Equal supports elsewhere in the full labelled endpoint cause no problem.

## 3. Explicit classical dependency and its boundary

Use the classical uniform Bollobas set-pairs theorem INCLUDING ITS EQUALITY CASE:

For finite pairs (U_i,V_i) with |U_i|=a, |V_i|=b, U_i intersect V_i empty and U_i intersect V_j nonempty for i!=j, their number is at most binomial(a+b,a). At equality the pairs are all a/b partitions of ONE (a+b)-element set.

Here a=h>=2 and b=t-1>=1. All cross-intersections are supplied in Section 2 on the same fixed palette. Thus m<=B, and if m=B there is a core S subset P, |S|=h+t-1, whose h-subsets are exactly the supports in C, with their complementary (t-1)-subsets as the T_i.

This equality input is classical and is not proved or claimed new here. Primary mathematical source checked: Gerbner, Lemons, Palmer, Patkos and Szecsi, *Almost intersecting families of sets*, April 7, 2010, Theorem 2.1, printed page 3 (PDF page 3), explicitly attributes the result to Bollobas and states the equality characterization.
https://www.renyi.hu/~gerbner/papers/glpps2.pdf
Original reference in that paper: Bollobas, *On generalized graphs*, Acta Math. Acad. Sci. Hungar. 16 (1965), 447–452. The publication relies on the stated classical equality theorem, not an unverified new equality proof or a numerical design property.

The inequality-only bound was already used in accepted baseline GUARD_BUFFER_CONNECTIVITY. The equality case is the new dependency disclosed in this scope. No originality assertion is made for the bound refinement or its reconfiguration application.

## 4. Exactness provides the actual replacement root

Suppose for contradiction the smallest guard has m=B. Choose ANY t-subset H_0 of S. It hits every h-subset of S because S minus H_0 has only h-1 labels, so H_0 covers C.

The full compact endpoint E* is exact q=t+1. Consequently H_0 does NOT hit E*: an ACTUAL root F at a slot outside C misses H_0. Such a root exists by exactness, not by spare capacity or a hypothetical auxiliary support. Put D=F intersect S. Then D subset S minus H_0 and |D|<=h-1.

Choose two DISTINCT h-subsets U,V of S that contain D. They exist: extend D to an (h-1)-subset L of S; at least |S|-(h-1)=t>=2 labels lie outside L, so L plus either of two such labels supplies U and V. Both occur as actual supports in C at distinct labelled slots. F is not either root because it misses H_0 whereas every core h-subset meets H_0.

Select the actual family

C'=(C without the two roots U,V) plus the actual root F.

Its cardinality is B-1. This is selection among already existing roots, not a simultaneous primitive replacement or a new support/slot. The full endpoint has not changed.

## 5. All forbidden small covers remain excluded

We prove tau(C')>=t. Let K be any label set with |K|<=t-1 that hits C without U,V. Only K intersect S matters for those remaining core supports.

If |K intersect S|<=t-2, then |S minus K|>=h+1. There are at least h+1 distinct h-subsets of S minus K. Every one misses K; only TWO core h-subsets were removed. Since h>=2, h+1>=3, so at least one remaining actual core root misses K. This contradicts that K hits C without U,V.

Hence any putative small cover of those roots must have |K intersect S|=t-1. Because |K|<=t-1, K is wholly contained in S and has exactly t-1 labels. The unique core h-subset disjoint from K is S minus K. To hit every retained core root this subset must be U or V. Thus K is S minus U or S minus V.

Both U and V contain D=F intersect S, so either such K misses F. No putative small cover can hit C'. This covers EVERY small K, including labels outside the core, rather than only a supplied minimum cover. Therefore C' is a t-guard on B-1 actual slots, contradicting minimum cardinality of C. We conclude m<=B-1, proving X9G.

At target four this argument excludes all label pairs: a pair meeting at most one core label misses at least four core triples, and a core pair covering retained triples must complement U or V and therefore miss F. Pair witness protection is actual; no coverage-count proxy substitutes for it.

The use of MINIMUM cardinality is material. A merely inclusion-minimal guard of size B may coexist with F inside the endpoint; that guard need not itself be altered by deletion alone. We construct a smaller different actual guard and contradict global minimal size, not inclusion minimality alone.

The hypotheses h>=2 and t>=2 are material. For h=1, deleting two supports need not leave another missed root; exact higher-target singleton endpoints may require exactly t guard roots. No B-1 assertion is made there.

## 6. Derived guards at both exact endpoints and safe placement

Compact the original endpoints A,C exactly to A*,C*. At each choose the smaller of:
- the actual guard of size at most B-1 supplied by X9G;
- the actual roots avoiding a maximum-incidence label, supplied by X7G on at most floor(r*(k-h)/k) slots.

For completeness the X7G premise follows by counting hr compact incidences. Some label has degree at least ceil(hr/k). The roots avoiding that label require at least q-1 hitting labels: a smaller cover together with the omitted label would hit the full exact-q tuple with at most q-1 labels. They occupy at most r-ceil(hr/k)=floor(r*(k-h)/k) existing slots. This independently spells out the availability logic, not a relabelled X7 theorem.

Write I,J_0 for the chosen actual guards, of sizes m_A,m_C<=G. Under r>=2G-1, or the endpoint-sensitive assumption r>=m_A+m_C-1, at least m_C-1 existing slots lie outside I. Place the destination guard on a set J with overlap at most one with I: use outside slots first and, if needed, one source slot. A t-guard is nonempty because t>=2.

Permute the ENTIRE compact destination support tuple so its selected guard occupies J, completing the token assignment on the remaining existing slots; equal supports may be treated as distinct tokens. Uniform original floor h makes the completed permutation admissible and exact q. Accepted baseline Lemma M gives a finite native {q-1,q} path from C* to the permuted tuple C**. Save its reverse. This is not an assumed permutation of an unprotected level-t guard. It supplies exact-q entry states; arbitrary mixed-floor placement is not licensed.

Lemma M's eligible swap and termination apply: at an unfixed destination slot its desired token is in an unfixed slot, the swap fits both uniform floors, and fixes at least that destination without moving previously fixed slots.

## 7. Primitive handover, all witnesses and renewed progress

On I union J define D_i=A*_i for source-exclusive i, D_j=C**_j for destination-exclusive j, and D_s=A*_s union C**_s if the shared index exists.

If I,J are disjoint this family contains the source t-guard. If they share s, any K of size at most t-1 meeting all exclusive supports must miss BOTH A*_s and C**_s, by the two actual guard inequalities. It consequently misses their union. Thus tau(D)>=t in both cases. This is accepted O1, with its exact hypotheses furnished. At q=4 it supplies an actual missing-root witness against every pair of palette labels.

Construct the following finite LOWER path:
1. Replace destination-exclusive roots individually by C**_j, adding destination-only incidences then deleting old-only incidences. I is untouched and protects every primitive.
2. If s exists, expand A*_s to its union with C**_s and contract to C**_s, by one incidence per move. All supports on I union J are contained in D throughout. Any small K missed by an actual support of D is still missed by its current subset; hence tau>=t throughout this phase.
3. Hold the now-installed destination guard J fixed. Repair EVERY remaining root to C** by its individual union bridge. J protects all these subsequent edits.

Floors hold in each root replacement: additions contain the old h-support; deletions begin only after all destination labels are present and contain the destination h-support. All labels lie in P, all slots are existing, and each primitive toggles exactly one incidence.

The integer sum_i |current_i symmetric-difference C**_i| decreases by one at every middle primitive. Each unfinished root supplies a missing destination incidence, or, when none is missing, an old-only incidence eligible for deletion. The phase order never requires an unavailable edit: finish the current phase before beginning the next, and previously finished destination roots stay fixed. This proves next-move existence and finite termination at exactly C**.

Renewal means the actual completed destination guard replaces the old one before edits to remaining old-guard roots. It supports the entire remaining repair without being modified. The tuple can stay at level t at that handover; exact q need not reset. No arbitrary safe-prefix completion or universal multiple-overlap rule is inferred.

## 8. Upper conversion and exact labelled restoration

The supplied middle path maintains tau>=t. It is not asserted to have tau<=q. At uniform floor h every k-h+1 labels hit every root, so the finite preliminary upper bound is k-h+1.

Invoke accepted maximum-layer Theorem A on THIS actual lower path between exact-q endpoints A*,C**. The fixed native carrier is closed under support additions/unions, roots remain nonempty at their original floors, and both endpoints are exact q. Theorem A replaces successive maximum levels with finite primitive segments whose lower values stay at least q-1, until maximum q. Its termination is by decreasing maximum layer; it does not assert a short path or preserve the preliminary schedule.

Concatenate source exact compaction, the converted middle path, reversed Lemma M destination permutation, and reversed destination exact compaction. Each join is exact q; every primitive stays in {q-1,q}. This reaches the ORIGINAL labelled tuple C and every originally larger support. Thus Theorem X9 is complete endpoint repair.

This is root-level repair. Conditional native lifting uses baseline Section 7's six-clause child interfaces, fixed-root clearance and exact child interiors. It is not a new unconditional nested theorem.

## 9. General coverage, boundaries and consolidated obligation

The palette-independent criterion r>=2B-3 follows because G<=B-1. For h=3,q=4, B=10 and threshold seventeen follows for every feasible k. This genuinely extends old O1's threshold nineteen on larger palettes, not merely previously covered seven-label carriers.

At k=7,h=3,q=4, min(floor(4r/7),9) plus X8 and the seventeen threshold leave only r=14,16 as possible universal carrier obligations; endpoint-sensitive guards, X5, cyclic and other accepted classes still exclude further pairs. This is no instruction to enumerate them and no claim they are disconnected.

The general question remains whether smaller actual guards can always be derived below this threshold, or whether guards with genuinely necessary multiple overlaps admit a reusable handover. The strict-bound proof improves availability without proving such a handover. A failed bound, target class or chosen bridge is a limitation of that method, not a native barrier.

Original destination-directed scheduling remains OPEN: endpoint permutation, compaction and upper conversion may use temporary incidences/repeated toggles relative to the original endpoints. No universal native/nested closure, sharp guard bound, efficient guard-selection algorithm, measured runtime, physical law or originality claim.

## 10. Whole-argument dependency gate

Fresh review must inspect X9G and the entire composition, not just the one-unit arithmetic improvement. Dependencies:
- Classical uniform set-pairs theorem AND equality case: exact ranks h,t-1 and complete cross-intersections; Section 3, external primary citation above.
- Exact compaction: retained minimum q-cover plus monotonicity and eligible deletions.
- X7G: actual omitted-label family, exact uniform compact endpoint; Section 6 restates availability proof.
- O1: actual t-guards, at most one shared labelled index; Section 7 restates witness proof and primitives.
- M: permutation of full exact-q endpoints with destination-compatible floors; uniform h, reversed before noncompact restoration.
- A: constructed finite lower path between exact-q endpoints on original union-closed width-floor carrier, Section 8.

Inherited implementations/proofs/certificates remain unchanged. No scientific execution, test run, workflow, new numbered version or merge into certified integration. A fresh attributable exact-source whole-argument receipt and immutable publication readback are required before acceptance is reported.
