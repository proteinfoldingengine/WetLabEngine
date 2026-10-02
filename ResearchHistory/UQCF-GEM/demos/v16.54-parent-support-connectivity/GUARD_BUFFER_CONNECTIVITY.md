# Connectivity by preserving and replacing a small hitting guard

Status: candidate analytical proof for independent review. Parent head: 59f708231dd0e57548fc5931a8b0c98156ed8aa0. No implementation, enumeration or numerical execution.

## 1. Native carrier and results

The carrier is the existing one: r labelled nonempty roots on one fixed palette P of k labels, root i having fixed positive floor a_i. A primitive move toggles one root incidence and respects all floors. No temporary root slot or extra label is allowed. Fix exact-q endpoints with q>=3, and write t=q-1.

A t-guard is a subfamily of root slots whose supports have hitting number at least t. It protects the lower guard regardless of what happens in the other slots. This terminology denotes actual roots, not extra constraints or proof-only native supports.

**Theorem AB (two-guard criterion, arbitrary floors).** Let A and B be exact-q endpoints. If A has a t-guard on indices I, B has a t-guard on indices J, and I and J are disjoint, then A and B are connected by a native root path with tau in {q-1,q}.

**Theorem AC (uniform-floor slot bound).** If every floor equals h>=1 and

    r >= 2*C(h+q-2,h),

then every pair of feasible exact-q endpoints is connected with tau in {q-1,q}. There is no restriction on their overlap pattern. The bound is sufficient, not claimed necessary or sharp. It counts existing root slots and does not authorize adding slots.

An endpoint-sensitive version replaces the displayed bound with r>=m_A+m_B, where m_A and m_B are sizes of t-guards selected after exact compaction. The proof below explains how equal floors let us place them on disjoint indices by a safe endpoint root permutation.

## 2. Exchanging guards without losing the lower bound

For Theorem AB, first replace every root A_j with B_j for j in J, using A_j -> A_j union B_j -> B_j and single incidences. Indices I are untouched, so their t-guard remains fixed. Both supports meet the same slot's floor; the union path also meets it.

Once J agrees with B, hold J fixed and replace every remaining root by its B support, again through unions. The B guard on J protects every step. This gives a finite path from A to B with tau>=t throughout. Upper values may exceed q; no direct full-band claim is made for this preliminary path.

Apply the independently accepted maximum-layer removal theorem (Theorem A of GENERAL_PARENT_CONNECTIVITY.md) to these exact-q endpoints and their lower-guard path. It supplies a finite path with tau in {q-1,q}, preserving all floors and using only primitive incidences. This proves AB. The intermediate complete coexistence of two guards may have a high hitting number, and is precisely why the prior upper-excursion removal theorem is needed.

## 3. A small guard exists after uniform exact compaction

Fix a minimum hitting set H of an exact-q endpoint. For each root select one label from its intersection with H and shrink it to exactly h labels, retaining that selected label. All deletions respect floor h. H still hits every root, so tau<=q, while deletion cannot decrease tau. Hence compaction is exact-q.

From this h-uniform tuple choose an inclusion-minimal subfamily C with hitting number at least t. Such a subfamily exists because the full tuple has hitting number q>t. Minimality means removal of any edge E leaves hitting number at most t-1. Adding one nonempty edge increases hitting number by at most one, so tau(C)=t and tau(C without E)=t-1 for every E. In particular C has no repeated edges.

For each E in C, choose a minimum hitting set T_E of C without E. It has size t-1, is disjoint from E (otherwise it would hit C), and meets every other edge F. Thus the pairs (E,T_E) satisfy

    E intersect T_E is empty;
    E intersect T_F is nonempty whenever E!=F.

The classical Bollobas set-pairs argument gives |C|<=C(h+t-1,h). For completeness, consider a uniformly random linear order of P, and let event Q_E say that all labels of E precede all labels of T_E. Its probability is 1/C(h+t-1,h). For two distinct edges E,F choose x in E intersect T_F and y in F intersect T_E. They are different, because E and T_E are disjoint. Event Q_E forces x before y, while Q_F forces y before x. The events are therefore disjoint. Summing their probabilities gives

    |C| / C(h+t-1,h) <= 1.

Only a finite counting argument is used; no random procedure is run. With t=q-1 put N=C(h+q-2,h). Every compact endpoint has an actual t-guard on at most N slots.

This guard-size bound is classical, not claimed as new. See Bucic, Korandi and Sudakov, *Covering graphs by monochromatic trees and Helly-type results for hypergraphs*, Corollary 2.9 (attributed there to Bollobas): https://korandi.org/docs/monotreecover_final.pdf. The native two-guard reconfiguration application is proved here independently of any implementation.

## 4. Slot assignment and endpoint restoration

Compact the two endpoints to A' and B', remaining exact-q. Select guards on I_A and I_B of sizes m_A,m_B<=N. If r>=m_A+m_B, there are at least m_B slots outside I_A. Permute the root supports of B' so that its chosen guard occupies such a set J. This is a permutation of the existing r supports, not an insertion of new supports.

All floors equal h, so every root permutation is admissible at its completed endpoint. The previously accepted safe root-permutation theorem supplies a unit-band path between the exact-q tuples B' and the permuted tuple B''. In particular, this permutation is carried out as an endpoint operation at level q, not as an unproved permutation of a bare t-guard at level t.

Now A' has a guard on I_A, B'' has a guard on disjoint J, and Theorem AB applies. Concatenate the exact compaction of A, the resulting unit-band path to B'', the reversed safe endpoint permutation to B', and reversed exact compaction to B. This proves the endpoint-sensitive criterion and AC, since r>=2N implies r>=m_A+m_B.

Every phase joins at an exact-q state. Slots are labelled and retained throughout, and no relocation of a guard is assumed possible at level q-1 without protection. For nonuniform floors, arbitrary root permutations need not be admissible; only AB with its actual compatible index sets is asserted universally.

## 5. What this closes and what it leaves open

The theorem handles arbitrary hyperedge overlap once the original slot budget is large enough. It does not require a complete-module exact-q terminal form, a disjoint-root packing, a pair-root clone guard or a positive-slack proxy. It extends the analytical sufficient conditions to every uniform rank, not one branching number at a time.

It does not settle all uniform-floor endpoints below the bound, nor general mixed-floor endpoints without a compatible disjoint pair of guards. Failure of the numerical inequality is not a disconnection result: it only makes this sufficient proof unavailable. Likewise a failed choice of guards does not prove that no other guards or safe exchange exists.

For the equal-part cyclic example k=3a, h=3, q=3a-3, a>=2, the generic sufficient threshold is 2*C(3a-2,3). The actual slot count is r=a(a-1)(2a-1), and

    2*C(3a-2,3)-r = (a-1)(7a^2-17a+8) > 0.

Indeed the quadratic is 2 at a=2 and its increment from a to a+1 is 14a-10>0. Thus this coarse guard bound does not imply connectivity for that family. CYCLIC_TRIPLE_CONNECTIVITY.md supplies a separate structural route for it. Neither proof makes the other redundant.

The remaining global task is to reconfigure compatible guards when they cannot coexist in disjoint slots, or find a genuine exact-endpoint obstruction. Earlier native lifting is conditional on its child-interface assumptions. No universal arbitrary-floor result, native barrier, implementation certification, efficiency guarantee or physical implication is asserted here.
