# A11.X29 — pair redundancy permits unequal protection grades

Scope:b1dec959c6765ae5691c2bdc03e26e91e6c107ae.
Analytical parent:9f185dfeb69d646d671c549432108e3796502ad8.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument review. Analytical only.

## 1. Exact result

Fix ODD k>=7, a finite ordered k-label palette and labelled ORIGINAL slots. There are ell original low floors k-4 and f original high floors k-3. Assume integer counts satisfy

4ell+f=binomial(k,3), 0<=epsilon=3f-binomial(k,2)<k-3.

**X29G.** Every exact-four endpoint is forced compact and has ACTUAL three-guards in BOTH original grades. Every pair has at least one high missed-root witness and at least(k-3-epsilon)/2 low missed-root witnesses (an integer count may be rounded upward).

**X29R.** Every pair of exact-four endpoints on this carrier has a finite native one-incidence path with3<=tau<=4, restoring the FULL labelled destination. Exact balance epsilon0 from X28 is no longer required. Exact triple-capacity saturation, odd k and the stated excess bound remain hypotheses.

**X29F.** For every m>=3, k=2^m-1, and integer t>=0 with12t<k-3, a self-contained symbolic construction gives exact-four endpoints on the profile

ell=k(k-1)(k-3)/24-t, f=k(k-1)/6+4t,

with original floors k-4/k-3. ALL exact endpoint pairs on that profile repair by X29R. In particular m>=5 admits t1 and gives infinitely many genuinely UNBALANCED feasible classes. Construction coordinates specify supports only; no path is constrained by them.

Native palette/slots/floors stay fixed during repair. Each primitive changes ONE incidence in ONE original root; temporary larger supports/background/repeated changes remain permitted. No extra native label, slot, geometry or fundamental time.

## 2. Excess cannot consume the last low witness

At exact4 every triple lies in some ACTUAL complementary block. Low blocks have size at most4 and capacity at most4 triples; high blocks size at most3 and capacity at most1. Total capacity equals binomial(k,3). Thus every triple has EXACTLY ONE actual witness and every support attains its original floor. A smaller low/high complement would lose triple capacity, making coverage impossible. This is the inherited X28 saturation inference, unchanged.

For pair uv count its k-2 triple obligations in the SAME unique partition:

2p4(uv)+p3(uv)=k-2,

where p4/p3 count original low/high complements containing the pair. Odd k forces p3 odd>=1. Consequently

epsilon=3f-binomial(k,2)=sum_pairs(p3-1)>=0.

Each summand is NONNEGATIVE. Therefore for EVERY pair p3<=1+epsilon, and

p4=(k-2-p3)/2 >= (k-3-epsilon)/2>0.

This proves both actual grade guards. Smaller sets can be padded to pairs. Equivalently losing the last low witness at any pair would require p3=k-2 and consume at least k-3 of the total excess. The bound measures sharing in the SAME actual roots, not independent spare capacities.

The strict inequality is sufficient. Equality/outside it proves neither a missing guard nor native disconnection. No optimal threshold is claimed. If epsilon<0, exact-four is infeasible by the derived identity; infeasibility is not disconnected endpoints.

## 3. Complete native handover and repeated use

Given arbitrary original exact endpoints A,C, let L,F be the fixed original low/high index sets. Their actual guard property follows from Section2, not from a prescribed endpoint shape.

Hold A's HIGH roots fixed while repairing every LOW root to its actual C support. In each slot add every missing destination label first, then delete each old-only label, in fixed palette order. EVERY forbidden pair misses an unchanged actual source-high root. After all low slots equal C, the actual destination-low family is installed and supplies a three-guard.

Hold this installed LOW guard fixed while repairing every HIGH root in the same way. EVERY forbidden pair now misses an actual destination-low root. Source-high and destination-low indices are disjoint even when their label supports overlap. Replacement protection exists BEFORE the old protection changes.

Every addition is in P and retains its current floor. Each deletion retains the full destination support C_i, which meets the same original floor. Every unfinished scheduled root supplies a missing incidence, or after all additions an old-only incidence. Each primitive decreases its symmetric difference from C_i by one; finite slot and phase lists terminate at the EXACT full labelled C. Thus a complete finite LOWER path maintaining tau>=3 exists, with no assumed spare residual capacity, independent outside-slot degree, common hub or slot permutation.

The preliminary path can exceed4. Invoke accepted maximum-layer A ONLY after this complete lower path between actual original exact-four endpoints exists. The positive-floor native carrier is union-closed and admits all additions, so A supplies a finite{3,4} path with the SAME labelled endpoints. No efficiency/destination-directed schedule property is inferred from conversion.

At every exact endpoint both grade guards are forced again. Each next endpoint leg therefore has the same eligible two-phase construction. Intermediate renewal occurs when the destination-low guard is installed; exact4 resetting after each handover is unnecessary. Full original restoration is supplied. Saturation forces exact endpoints compact in this class, so no noncompact exact endpoint is presumed; converted intermediate supports remain unrestricted.

This proves X29R using X28's full direct composition in its actual native domain.

## 4. Infinite self-contained feasible families

Let V be the set of m-bit binary vectors, with addition coordinatewise modulo2, m>=3. Let0 be its zero vector and P=V minus{0}, so k=2^m-1. Order P lexicographically. All native labels are in P.

Define an AUXILIARY collection of four-subsets of V:

B={ {a,b,c,a+b+c}: a,b,c distinct in V }.

The fourth vector differs from each of the first three: equality with a, for example, would give b=c. Each block has four distinct vectors with sum0. Every three-subset of V lies in its UNIQUE such block, since its fourth vector is forced to be the sum of its three elements. Conversely any three elements of a zero-sum four-block complete to its remaining fourth. Thus distinct blocks do not share a triple. This proves unique triple coverage algebraically, not by enumeration or an external classification.

Every block containing0 reduces on P to a triple{a,b,a+b}. These high complements cover EVERY pair of P exactly once: for distinct nonzero a,b, a+b is nonzero and differs from a,b, and the unique block through0,a,b supplies that triple. Hence their number is

f0=binomial(k,2)/3=k(k-1)/6.

Retain every block avoiding0 as a size4 LOW complement on P. Every triple of P is contained in exactly one retained low complement or equals one of the high complements. If ell0 counts the low complements, unique triple incidence gives4ell0+f0=binomial(k,3), so

ell0=k(k-1)(k-3)/24.

The counts are integers by their proved combinatorial interpretation. The auxiliary zero symbol is NOT a native label or incidence; it has been removed before defining any actual root. There are ell0+f0 EXISTING slots in this specified carrier. Root supports are the complements in P, of sizes k-4/k-3.

Let e1,e2,e3 be the first three unit vectors and set

H={e1,e2,e3,e1+e2}.

These are four distinct NONZERO native labels. Their sum is e3!=0, so H is NOT a zero-sum four-block. It cannot lie in a size3 complement. A size4 complement containing H would equal H, contradicting its nonzero sum. Thus H meets EVERY actual root. Unique triple coverage gives tau>=4; H gives tau<=4. This is a supplied actual minimum four-cover.

Now choose t DISTINCT retained low four-complements, by their lexicographic order. Replace each, in the completed mathematical support specification, by its FOUR triple subsets as high complements. The former four-block's four triple obligations are then covered exactly once by those four triples. Unique triple coverage in the original partition ensures no new triple duplicates a preexisting high complement or a triple supplied by another selected block. Therefore the new complement family still partitions ALL triple obligations.

The new counts are ell=ell0-t and f=f0+4t. It has original low/high floors k-4/k-3 and r=ell0+f0+3t slots. This is a definition of a NEW FIXED carrier and its endpoint, not a primitive transformation between carriers that changes floors or adds slots. Once chosen, all subsequent native repair fixes this carrier permanently.

There are enough low complements to choose t. Since12t<k-3, t<(k-3)/12, while ell0=k(k-1)(k-3)/24 is larger than that for k>=7. All new size3 complements cannot contain H, and remaining low complements are old zero-sum four-blocks that cannot equal H. Hence H still meets every actual root. Triple coverage gives exact FOUR after the replacement.

Capacity remains saturated:4ell+f=binomial(k,3). The high-pair excess is epsilon=3f-binomial(k,2)=12t<k-3. X29G/R apply to EVERY exact endpoint pair on this profile, regardless of whether the endpoints have binary-vector structure. This proves X29F.

For m3,4 the bound permits only t0 and those instances remain balanced. For every m>=5, k>=31 so t1 is permitted and epsilon12>0. Hence infinitely many UNBALANCED feasible carriers lie outside X28's exact balance hypothesis. Arbitrary qualifying odd palettes outside this specified constructor family are not asserted feasible.

## 5. New statement versus inherited methods

X28 requires epsilon0; X29 supplies full completion at POSITIVE epsilon<k-3. The advance is a quantitative actual redundancy bound: excess high protection can be distributed unevenly, but cannot eliminate the last low witness before the shared excess budget reaches k-3. Both grade guards remain available to renew actual endpoint repair.

The m5,t1 feasible control has k31,ell1084,f159,r1243, original floors27/28 and total original incidence S33720. Every exact endpoint maximum degree M>=ceil(S/k)=1088. X14 cap repair requires D>=1088 and r>=2D+2>=2178, exceeding1243. X15's leveling requirement r>=D+M+1 forces D<=154, while S<=Dk would require33720<=4774, impossible. No choice of those cap/degree parameters applies.

This genuinely mixed high-floor carrier is outside uniform3/4 closure, has no floor1/2 or automatic floor>=k-2=29, and fails palette-room k>=S. No blanket failure of every older CONDITIONAL guard bridge is asserted. X28 itself already supplies direct repair at balanced profiles; that overlap t0 is disclosed. The unbalanced infinite class is a proof, not a collection of passing numerical campaigns.

## 6. Dependencies, review and limits

Read live status/next obligation and X28 at parent9f185dfeb69d646d671c549432108e3796502ad8. Baseline GENERAL_PARENT_CONNECTIVITY A at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f supplies only upper removal after the complete lower leg. X14/X15 cap domains are inherited as stated in X28 and checked for the control. No M/O1/canonical access, classification theorem, scientific enumeration or newly inserted geometric rule is used.

Fresh whole-argument review must check strict excess inequality/odd parity, original compaction and unique shared witnesses, actual all-pair guards, fixed original grade indices, eligible primitive/floors/palette/progress/renewal/exact endpoint restoration and legitimate upper conversion. Also check binary-vector unique fourth, counts, auxiliary symbol removal, supplied H, no triple duplication on replacement, t availability, fixed NEW carrier versus illegal cross-carrier moves, positive-excess novelty and arithmetic. Frozen prior sources and failed construction classifications remain unchanged.

Exact saturation and oddness remain unresolved restrictions to relax; multiple-overlap mechanisms remain another direction. Failure of this sufficient bound is not disconnection. No arbitrary safe-prefix completion, no optimal threshold, and no native equivalence for cloning or coordinate-preserving paths is claimed.

Original destination-directed A11, unrestricted mixed/higher-target/nested and physical interpretation remain OPEN; conditional child lifting retains exact-child/fixed-root-clearance hypotheses. Ordered repair/retained recoverability; no fundamental time or native geometry.

No numerical scientific execution/test/workflow/run ID, implementation/benchmark or certified integration merge. v16.55 remains OPEN pending prospective execution scope, independent full reconstruction, substantive rejecting controls, inherited replay/logs, reproduced durable evidence, exact merge review and actual post-merge audit. Certified v16.54 and accepted efficiency design remain unchanged; runner execution/measured speedup unstarted.
