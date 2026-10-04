# A11.X32 — deterministic placement preserves actual witnesses during patch renewal

Scope:3c1a9a24d652847e3fcc9594243bbc3307ab0e10.
Analytical parent:331480e780945633cd170db307745d915cb64d06.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument review. Analytical only.

## 1. Exact statements

Fix a finite ordered palette P of k>=4 labels and labelled ORIGINAL slots with positive floors. A primitive changes ONE incidence in ONE slot. Larger supports and temporary, repeated and background changes remain permitted.

**X32P — actual witness-preserving placement.** Partition slots into L,F with ell=|L|>0. All ORIGINAL L floors equal the same positive h; F floors can differ. Let A,C be exact-four endpoints. For each pair K let W(K)={i in L:A_i avoids K}, and assume w_K=|W(K)|>=1. Suppose p distinct destination L support TOKENS, indexed by U subset L, together with the actual destination F roots form a three-guard. Equal supports at different indices are distinct existing tokens. Set

Phi(empty)=sum_(pairs K) binomial(ell-w_K,p-w_K)/binomial(ell,p),

with binomial(n,j)=0 for j<0 or j>n. If Phi(empty)<1, there is a deterministic finite native{3,4} path from A to the FULL original labelled C. No endpoint compaction is required for this statement.

**X32B — scalar sufficient bound.** If every w_K>=rho>=1 and N(p/ell)^rho<1, where N=binomial(k,2), X32P applies. It does not require rho>p.

**X32R — derived odd two-grade completion.** Let ODD k>=7 and ORIGINAL floors k-4/k-3 with ell>0 low slots and f high slots. Put

delta=4ell+f-binomial(k,3)>=0,
epsilon=3f-binomial(k,2),
rho=ceil((k-3-epsilon-3delta)/2).

If epsilon+3delta<k-3 and

binomial(k,2)*delta^rho < ell^rho,

EVERY exact-four endpoint pair on the fixed carrier admits complete finite native{3,4} repair restoring its FULL labelled, possibly noncompact destination supports.

**X32F — infinite new feasible profiles.** For every m>=5, put k=2^m-1, d=floor((k-7)/6),

ell=k(k-1)(k-3)/24, f=k(k-1)/6+d.

Exact-four endpoints exist with ORIGINAL floors k-4/k-3. All exact endpoint pairs repair by X32R. These profiles FAIL the X31 sufficient inequality epsilon+5delta<k-3. This is a genuine extension of that bound, not a claim that every earlier conditional bridge fails.

No native labels or slots are added during repair; no weakened floors, simultaneous primitive, geometry or fundamental time. Counting below is an exact finite mathematical proof, not a randomized campaign, heuristic or reachability enumeration.

## 2. Select patch slots without exhausting any actual witness family

For a p-element subset J of L, a bad pair K means W(K) subset J. There are binomial(ell-w_K,p-w_K) such J, among binomial(ell,p) total. Thus Phi(empty) is the exact average NUMBER of bad pairs. Phi<1 implies some J has zero bad pairs. The following supplies an eligible deterministic next selection and termination, rather than merely invoking existence.

At partial D subset L, |D|=s<=p, let a_K=|W(K) minus D| and define

Phi(D)=sum_K binomial(ell-s-a_K,p-s-a_K)/binomial(ell-s,p-s).

This is the average bad-pair count over all p-element completions of D. When s<p,

average_(j in L minus D) Phi(D union {j}) = Phi(D).

Indeed choosing one remaining j uniformly and then a uniform completion containing it gives each completion the same multiplicity p-s. This is a finite counting identity; no random choice is executed or required.

Therefore at least one eligible remaining j has Phi(D union {j})<=Phi(D). Select the first such j in the ORIGINAL slot order, evaluating exact rational binomial counts. The measure p-|D| decreases. After p selections, J=D and Phi(J) is the INTEGER number of bad pairs. It is <=Phi(empty)<1, hence zero. For EVERY K, an ACTUAL source root in L minus J avoids K. The same roots may witness many pairs; capacities are not split into independent fictional systems. For p=0 the empty J already works because every W(K) is nonempty.

For X32B, if w<=p<ell the fraction for a particular W equals

(p)_w/(ell)_w = product_(j=0 to w-1) (p-j)/(ell-j) <= (p/ell)^w <= (p/ell)^rho.

If w>p its bad fraction is zero. If p=0 all fractions are zero. A passing bound forces p<ell (since N>=6 and rho>=1). Summing gives Phi(empty)<=N(p/ell)^rho<1. This proves X32B.

The witness-preserving J is selected BEFORE any native incidence edits. No computation of a full native graph, empirical failure rate or bounded-length search is involved. No runtime efficiency claim is made for exact rational selection.

## 3. Place FULL tokens legally and compose full repair

Map the p specified actual C tokens in U bijectively onto J, in index order; extend this to a bijection of ALL actual C L tokens onto L, again in index order for the remainder. Leave F fixed. Call the resulting FULL destination C'. Every L token has size>=h and every L ORIGINAL floor is h, so all placements, including noncompact tokens, fit. No F token moves. C' has tau4 because permutation preserves the family of supports.

Accepted endpoint permutation M supplies a finite{3,4} path C to C' on this ORIGINAL carrier. Only L slots are swapped; their floors are equal. Its union expansions/contractions are legal ONE-incidence moves, and each completed token swap fixes an additional misplaced token without moving correctly assigned ones. Duplicate supports cause no obstruction; tokens retain indices. Save the full reverse C' to C. This is NOT an arbitrary mixed-floor permutation.

Now construct a complete lower path A to C':
1. Hold ALL source L fixed while repairing every F slot to its actual C'_i=C_i.
2. Hold every L root outside J fixed while repairing every J slot to its placed actual C'_i. The old source witness outside ALL J for EVERY pair was supplied by Section2, so every patch edit is protected.
3. The installed actual C'_F plus C'_J family is the destination three-guard, transported from F plus U. Hold this renewed family fixed while repairing all remaining L roots to C'.

In every scheduled root, add its missing destination labels in palette order, then delete old-only labels. Additions retain floors; every deletion retains its FULL destination support at that ORIGINAL floor. An unfinished root has an eligible missing label or, after additions, an old-only label. Symmetric difference decreases by one per primitive. The finite phase and slot list terminates at EXACT full C'.

All forbidden pairs are witnessed in every phase: source L in phase1, unchanged source L outside J in phase2, installed F plus J in phase3. Smaller hitting sets are excluded by padding them to pairs. Thus tau>=3 everywhere. The preliminary path may exceed4.

Invoke maximum-layer theorem A on this COMPLETE lower path between actual exact-four endpoints A,C'. Native positive-floor unions/additions satisfy its hypotheses, so it gives a finite{3,4} path with those SAME full labelled endpoints. Append the saved native{3,4} reverse M path C' to C. The join is the actual exact C', and EVERY original labelled destination support is restored. No conversion is applied at an inexact handover boundary.

This proves X32P. At each subsequent exact endpoint leg satisfying its actual witness/patch conditions the same selection, legal placement and finite three-phase construction are available again. Renewal means a replacement actual guard is installed before old protection changes; it does not require returning to exact4 after each patch. Safe prefixes alone do not supply this guarantee.

## 4. Derive all conditions from actual odd two-grade multiplicities

At an original exact-four endpoint E choose an actual minimum four-cover H_E. In every root retain an ORIGINAL-floor subset containing a label of H_E, and delete the other incidences singly. Deletion cannot lower tau, while retained H_E bounds it by4, so preparation stays EXACT4. Each excess incidence is an eligible deletion and total excess strictly decreases. Save the full reverse, preserving all original noncompact supports.

At compact E*, low/high complementary blocks have sizes4/3. Exact4 requires every triple T to lie in an ACTUAL complementary block. Let mu_E(T) be its total witness multiplicity minus1. Then mu>=0 and

sum_T mu(T)=4ell+f-binomial(k,3)=delta.

For a pair K define e_K=sum_(T containing K)mu(T). Then sum_K e_K=3delta, and counting the SAME actual blocks yields

2p4(K)+p3(K)=k-2+e_K,

where p4 and p3 count actual low and high missed-root indices.

The number O of pairs with ODD e_K is <=3delta. At all other pairs odd k forces p3 odd>=1. For any specified K, the other pairs contribute at least N-1-O to sum p3=3f. This bound remains valid if K itself is exceptional. Consequently

p3(K)<=epsilon+1+O<=epsilon+1+3delta,
p4(K)>=(k-3-epsilon-3delta)/2.

The positive bound and integrality give at least rho DISTINCT actual source LOW witnesses for EVERY pair. No independent capacities or cloning are assumed.

At compact destination C*, there are at most delta DISTINCT triples with mu_C(T)>0. For each choose the first actual root avoiding T; existence follows from exact4, since otherwise T would hit every root. High choices are already in F; deduplicate low choices into U. Then p=|U|<=delta. The ACTUAL destination F plus U family protects every pair:
- For EVEN e_C(K), p3(K) is odd>=1, giving an actual high witness.
- For ODD e_C(K)>0, some excess T contains K. Its chosen actual avoiding root misses K and belongs to F or U.

One root may protect several obligations; no root avoiding the UNION of all excess triples is required. Source and destination multiplicity functions need not agree.

X32R's inequality implies delta<ell. Since p<=delta,

N(p/ell)^rho <= N(delta/ell)^rho<1.

X32B applies to compact A*,C* with the same common original low floor k-4 and positive original high floors k-3. It supplies full native{3,4} repair A* to C*, including legal within-L token placement and reverse restoration. Prepend source exact preparation and append the saved full reverse destination preparation. These exact4 paths meet at their actual saved tuples and restore original noncompact C. This proves X32R.

At every next original exact endpoint, the same multiplicity bound rederives source witnesses and destination patch availability. Selection, token swaps and all primitive progress are supplied again. This is guaranteed complete repair in the stated class, not merely repeated local safety.

## 5. Infinite feasible class beyond X31's bound

Use the self-contained X29 binary constructor at t=0. On k=2^m-1 nonzero m-bit labels it supplies ell0=k(k-1)(k-3)/24 low roots and f0=k(k-1)/6 high roots with unique triple coverage. Its actual four-cover H={e1,e2,e3,e1+e2} is retained.

Specify d=floor((k-7)/6) further ORIGINAL high slots with duplicates of an existing high support. This defines a NEW FIXED carrier BEFORE repair. It is not a primitive adding slots, or a claim that cloning preserves paths. The original roots force tau>=4; the duplicated supports already meet H, so tau<=4. The specified endpoint is exact4. All native paths thereafter fix these declared labels, slots and floors.

Counts give delta=d and epsilon=3d. For m>=5, k>=31 and d>=4. Since6d<=k-7,

epsilon+3delta=6d<k-3, rho=ceil((k-3-6d)/2)>=2.

Also ell=ell0>d and d<=k/6. Therefore

N(d/ell)^rho <= N(d/ell)^2
<= 8k/[(k-1)(k-3)^2] <1

for k>=31. The middle bound follows by substituting N=k(k-1)/2 and ell=k(k-1)(k-3)/24; the last strict bound follows from k-1>k/2 and (k-3)^2>=28^2>16. Thus X32R connects EVERY exact endpoint pair on each such fixed profile, including endpoints without binary structure.

These profiles fail X31's epsilon+5delta<k-3, since that would require8d<k-3. At k31, d4 gives32>=28. For binary k>=63, d>= (k-12)/6, hence8d>=4(k-12)/3>=k-3 (the latter holds for k>=39). They are also outside zero-excess X29 and one-excess X30 structural hypotheses. No blanket failure of all their conditional bridges is asserted.

The first control has k31,ell1085,f159,r1244, original floors27/28 and total original incidence S33747. Compact maximum degree M>=ceil(S/31)=1089. X14 whole-cap repair would require r>=2M+2>=2180>1244. X15N's r>=D+M+1 forces D<=154, inconsistent with S<=31D<=4774. The explicit placement inequality is465*4^2=7440<1085^2=1177225. These are symbolic/arithmetic checks, not scientific enumeration.

## 6. Discovery, dependencies and precise remaining obligations

X31 protected patches at their original indices using p+1 witnesses per pair. X32 removes that requirement in a common ORIGINAL floor grade: exact finite witness counts select a placement leaving one old actual witness outside ALL patches. Complete FULL token assignment and a legal saved permutation path restore the original labelled destination. The new infinite profiles satisfy the placement bound while failing X31's redundancy bound.

This does not replace stronger inherited zero/one-excess or other accepted classes. If the count bound fails, it proves neither that a suitable placement is absent nor that repair is disconnected. Exact Phi can improve the scalar bound; even Phi>=1 does not prove every placement bad. Uniform low-floor placement is an openly stated new hypothesis of the general lemma, not native admissibility. Arbitrary unequal low floors would require a compatible assignment proof.

Read at analytical parent331480e780945633cd170db307745d915cb64d06: X31 complete multiple-patch argument and shared multiplicity identities; X29 self-contained constructor; live status/next obligation. Baseline OVERLAPPING_CLIQUE_EXCHANGE M and GENERAL_PARENT_CONNECTIVITY A at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f were read in their full endpoint permutation/upper-removal domains. M is applied only to a complete legal same-grade full-token assignment with exact endpoints. A is applied only to a complete lower path with actual exact ends. X14/X15 bounds are used only to exclude their cap domains in the stated control. Frozen sources are unchanged.

Fresh independent whole-argument review must check finite bad-pair counts, conditional-average identity, eligible selection and termination, p0/p=ell/zero binomial cases, ALL pair witnesses, shared capacities, full same-grade assignment/M reversal, original floor fit of noncompact tokens, phase primitives/progress/renewal, actual exact C' before A and full labelled C restoration, compaction retaining H, parity/excess derivation, actual patch availability, infinite fixed carrier/H/counts and novel inequality, and inherited domains.

Remaining direction: sharpen actual pair multiplicity bounds and compatible witness-preserving placements, or supply coupled handovers when no all-patch outside witness survives. Extend beyond odd two-grade complementary sizes4/3 without replacing the native graph by restricted supports. Failure of this sufficient route is not disconnection. No universal native connectivity, unrestricted mixed/higher-target/nested/physical closure, or stricter destination-directed scheduling is claimed. Conditional child lifting retains inherited exact-child/fixed-root-clearance interfaces.

No scientific numerical execution/test/workflow/run ID, implementation/benchmark or certified integration merge. v16.55 remains OPEN pending prospective execution scope, independent full reconstruction, substantive rejecting controls, inherited GitHub execution/logs, reproduced durable evidence, exact merge-head review and actual post-merge audit. Certified v16.54 and accepted efficiency baseline/A2 proposal/tiny validation DESIGN remain unchanged; runner implementation/execution/measured speedup unstarted.
