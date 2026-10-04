# A11.X31 — actual witness redundancy protects multiple-overlap renewal

Scope:e9af8d829a166b9881486d0aea8b7098d9d65e87.
Analytical parent:2b1bcbc4f1f36d137636f8588c1351720febb59d.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument review. Analytical only.

## 1. Exact statements and native rules

Fix a finite ordered palette, labelled ORIGINAL slots and positive original floors. Primitive moves add/remove ONE incidence in ONE root. Temporary larger supports, background and repeated edits are permitted. Exact endpoints have transversal FOUR.

**X31M — multiple actual patches.** Partition original slots into L,F. Let A,C be exact-four endpoints and J be a specified subset of L, with p=|J|. Suppose EVERY palette pair misses at least p+1 DISTINCT actual source roots in L, and the ACTUAL destination roots in F union J form a three-guard. Then A,C have complete finite native{3,4} repair with FULL original labelled destination restoration. Supports may be noncompact and floors arbitrary positive.

**X31R — derived completion at arbitrary excess.** Let ODD k>=7 and original low/high floors k-4/k-3 with ell/f slots. Define

delta=4ell+f-binomial(k,3)>=0,
epsilon=3f-binomial(k,2).

If epsilon+5delta<k-3, EVERY original exact-four endpoint pair has complete native3/4 repair restoring EVERY original labelled/noncompact destination support. At exact original-floor compaction every pair has at leastdelta+1 actual LOW witnesses. The destination HIGH roots plus at mostdelta existing LOW patches form a replacement guard. All patches and redundancy are derived, not assumed.

For delta0 this overlaps X29. For delta1 this bound is MORE CONSERVATIVE than X30; preserve X30's stronger one-excess class. No universal sharpness or disconnection claim.

**X31F — infinite multi-excess feasibility.** For k=2^m-1,m>=3, integers t,d>=0 satisfying12t+8d<k-3, exact endpoints exist on

ell=k(k-1)(k-3)/24-t,
f=k(k-1)/6+4t+d,

with original floors k-4/k-3. Every exact endpoint pair on that fixed profile repairs by X31R. For every m>=5, d2,t0 qualifies, proving infinitely many genuinely MULTI-excess carriers. No existence classification for all other odd profiles is inferred.

Native labels, slots and floors remain fixed during repair. No extra native reserve, simultaneous primitive, geometry or fundamental time. The patch budget is DERIVED from actual excess and can grow; no universal fixed buffer count is assumed.

## 2. General multiple-overlap handover: witnesses and progress

For X31M HOLD ALL source L roots fixed while repairing each F slot to its FULL actual C support. Add missing destination labels in palette order, then delete old-only labels. Every forbidden pair has an unchanged actual L witness (indeed p+1). The installed F roots then remain FIXED.

Now repair ALL patch slots in J to their actual C supports by the same individual add-before-delete process. HOLD every L root OUTSIDE J unchanged. For any pair K, at least p+1 DISTINCT original L roots missed K. At most p of their indices can belong to J. Therefore at least ONE actual source-L witness lies OUTSIDE J and stays unchanged through EVERY patch edit, even if the pair loses all witnesses inside J. This proves all-pair protection during shared patch installation. It does not assign different fictitious reserves to different pairs; the SAME unchanged roots may witness many pairs.

After all patch supports equal C, the installed ACTUAL destination family F union J is a three-guard by hypothesis. HOLD that renewed family fixed while repairing every remaining L slot to its full C support. Every pair now has an actual installed missed-root witness. Replacement protection is completed BEFORE the last old unedited supports change.

All additions use labels of C_i subset P and retain the current original floor. All deletions retain the already complete C_i at that SAME original floor. An unfinished scheduled root supplies a missing destination label, or after additions an old-only label. Its symmetric difference decreases by one per primitive. A finite phase/slot list terminates at FULL labelled C; previously completed supports stay correct.

This gives a complete finite LOWER path with tau>=3. Apply maximum-layer A ONLY after the actual exact-ended original-carrier path is complete. Positive floors and arbitrary union/addition closure hold, so A yields a finite{3,4} path with identical labelled endpoints. Preliminary length/scheduling/efficiency are not transferred. Smaller sets inherit missed witnesses by padding to pairs, since exact4 implies at least four labels.

This proves X31M. It handles p shared slots without imposing compactness/destination-monotonicity on the native graph. Reuse is guaranteed whenever its ACTUAL witness conditions hold; next-move existence and termination are supplied, not inferred from any safe prefix.

## 3. Shared multiplicity bounds derive the needed redundancy

At each original exact endpoint E choose a minimum four-cover H_E. Retain an original-floor subset meeting H_E in every root and delete excess incidences one at a time. Deletion cannot lower tau and retained H_E keeps tau<=4. Floors hold; an excess incidence supplies the next deletion and finite total excess decreases. Save the FULL reverse.

At compact E*, low/high complements have sizes4/3. Every triple has at least one actual complementary witness. Define mu(T)=its witness multiplicity minus1, so mu>=0. Counting all triple incidences gives

sum_T mu(T)=4ell+f-binomial(k,3)=delta.

For each pair K let e_K=sum_(T containing K)mu(T). Then sum_pairs e_K=3delta and the SAME actual blocks give

2p4(K)+p3(K)=k-2+e_K.

Let O be the number of pairs with ODD e_K. Since odd positive excess is at least1, O<=3delta. On every other pair, odd k makes p3 odd>=1; on the O exceptional pairs p3 may be even and zero.

For any specified pair K the other pairs contribute at least binomial(k,2)-1-O to the sum of high pair multiplicities. This relaxed bound is valid even if K itself is exceptional. Therefore

p3(K)<=3f-[binomial(k,2)-1-O]
=epsilon+1+O
<=epsilon+1+3delta.

Using e_K>=0,

p4(K)>=(k-3-epsilon-3delta)/2>delta

under epsilon+5delta<k-3. Since p4 is an integer ACTUAL ROOT COUNT, every pair has at leastdelta+1 distinct LOW missed-root witnesses. Distinct means ORIGINAL slot indices; equal supports in different slots are already separate actual roots, not cloned capacities introduced by the proof.

Feasibility also forces epsilon>=-O>=-3delta, but the theorem need not independently assume this: it follows for any existing exact endpoint. Necessary counting bounds do not assert feasible endpoints exist.

Source and destination multiplicity functions may differ. The redundant source witnesses and destination patch choices are derived separately in the SAME declared carrier, not by identifying their excess triples.

## 4. Actual destination patches are available and complete the guard

At compact exact destination C*, list the DISTINCT triples T with mu_C(T)>0. Their number is at mostdelta, because each contributes at least1 to sum mu=delta.

For each such T, exact FOUR supplies an ACTUAL C*_s disjoint from T; otherwise T would hit every root. Choose the first such original slot in fixed order. If it is HIGH, it is already in the background family F. If it is LOW, include its index in J. Deduplicate repeated LOW choices. Hence p=|J|<=delta. The full support used at each patch is its ACTUAL destination support at that SAME original slot, so its floor fit is automatic.

The destination family F union J protects EVERY pair:
- If e_C(K) is EVEN, odd k makes p3(K) odd>=1, so an actual HIGH root misses K.
- If e_C(K) is ODD, then e_C(K)>0. Some excess triple T contains K. Its chosen actual avoiding root misses T and therefore K, and belongs to F or J.

Thus F union J is an ACTUAL three-guard. One patch may cover several excess triples; sharing reduces p, never invents capacity. No single support avoiding the UNION of all excess triples is assumed.

By Section3 every source pair has at leastdelta+1>=p+1 actual LOW witnesses. This supplies ALL X31M inputs. Compact A*,C* admit a complete finite lower path: LOW protects HIGH installation, unchanged LOW outside J protects all patch installation, and renewed HIGH-plus-J protects remaining LOW repair.

Prepend original source exact preparation and append the FULL reversed actual destination preparation. Every join is its actual saved tuple. This is a complete lower path between ORIGINAL exact FOUR endpoints A,C. Apply A to this full path to obtain native{3,4} repair with every labelled/noncompact support restored. No conversion is applied prematurely at an inexact patch boundary.

At a next original exact endpoint, preparation again derives redundant LOW witnesses, destination excess triples and actual patch choices; phases and decreasing measures are available again. Renewal during each preliminary handover occurs BEFORE old protection changes and need not restore exact4 after each patch. This proves complete repeatable X31R.

## 5. Infinite symbolic feasible profiles and a single-union method limit

Inherit X29F's self-contained binary-vector constructor. On the nonzero m-bit labels, k=2^m-1, t replacements yield compact counts

ell=ell0-t, f_base=f0+4t,
ell0=k(k-1)(k-3)/24, f0=k(k-1)/6.

The proof there establishes unique triple coverage and an ACTUAL minimum four-cover H={e1,e2,e3,e1+e2}. Our inequality12t+8d<k-3 implies12t<k-3, so all its constructor hypotheses hold.

Define a completed NEW FIXED carrier by retaining all those roots and specifying d further ORIGINAL high-floor slots with duplicates of selected existing HIGH supports. Repetitions of the chosen support are allowed; at least one exists since f0>0. This is a mathematical endpoint specification BEFORE repair, not adding native slots, altering floors or proving a cloning/path equivalence.

The duplicated supports already meet H, so the new family remains exact FOUR. Counts give

delta=d, epsilon=12t+3d,
epsilon+5delta=12t+8d<k-3.

X31R connects ALL exact endpoints on that fixed profile, whether or not they follow the constructor pattern. This proves X31F.

For every m>=5,k>=31, choose t0,d2. Then16<k-3 and infinitely many MULTI-excess carriers are feasible. To check the single-union strategy, select TWO DISTINCT original high supports for the duplicates. Before duplication their high complements form the binary triple pair partition: distinct such triples share at most ONE label. Their two excess triples therefore have union of size at least FIVE. Every actual low/high root has complementary capacity at most4, so NO actual root can avoid the entire union.

This rigorously obstructs the proposal to supply ONE root avoiding BOTH whole excess triples. It does NOT say the constructor itself lacks a high guard, that actual missing-pair gaps must fill that union, that X30L fails at every endpoint, or that native repair is disconnected. The multiple actual-patch construction needs only individual avoiding witnesses plus derived source redundancy, and completes all endpoints in the class.

The k31,t0,d2 feasible control has ell1085,f157,r1242,floors27/28,S33691 and every compact maximum degree M>=ceil(33691/31)=1087. X14's cap would require r>=2*1087+2=2176>1242. X15N requires D<=1242-1087-1=154, inconsistent with33691<=31D<=4774. Thus their whole-cap/degree domains cannot explain this completion. No blanket failure of all conditional older bridges is asserted.

## 6. Discovery, inherited domains and remaining obligation

X30 localized gaps in ONE triple and supplied one actual patch. X31 handles arbitrarily many excess triples within a derived bound: enough source witnesses survive OUTSIDE the complete patch set, so every needed patch can be installed before the old protection is relinquished. The required patch budget grows with ACTUAL excess; no universal fixed-buffer assumption is introduced.

For arbitrary positive floors X31M is conditional on actual source redundancy and actual destination patch guard. For the odd two-grade class X31R DERIVES both, including actual next patch availability at every excess triple. Completion, not only local safety, follows from finite progress and full exact restoration.

Atdelta0 X29 is recovered; atdelta1 preserve X30's STRONGER bound epsilon<k-6 rather than replacing it with this conservative epsilon<k-8. Several excess triples are genuinely new relative to the zero/one-excess hypotheses. The sufficient inequality is not claimed sharp; its failure is not disconnection.

Sources read at analytical parent2b1bcbc4f1f36d137636f8588c1351720febb59d: live status/obligation, X30 full localized patch, X29 full constructor. Baseline GENERAL_PARENT_CONNECTIVITY A at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f applies to the FULL completed lower path in the original positive-floor union-closed carrier. X14/X15 cap requirements are checked only for the stated control; all frozen proofs/failure classifications remain unchanged.

Fresh whole-argument review must check odd-excess parity, all-other-pair count even when the chosen pair is exceptional, actual distinct-slot redundancy, patch set cardinality/sharing and actual avoiding roots, all-pair witnesses through simultaneous obligations but INDIVIDUAL primitive edits, eligible moves/termination/reuse, supplied minimum-cover compaction, exact FULL ends before A, noncompact labelled restoration, constructor parameters/fixed carrier, honest single-union method obstruction and inherited domains.

Remaining mathematical direction: improve the redundancy bound, exploit ACTUAL smaller patch sets or coupled witnesses when source redundancy is insufficient, or extend beyond odd two-grade complementary sizes4/3. None is reduced to an isolated root-count campaign. Original A11 directed/unrestricted mixed/higher-target/nested/physical closure remains OPEN; conditional lifting retains exact-child/fixed-root-clearance interfaces. Ordered repair/retained recoverability; no native geometry or fundamental time.

No scientific enumeration/numerical test/workflow/run ID, implementation/benchmark or certified integration merge. Numbered v16.55 stays OPEN pending prospective execution scope, independent full reconstruction, substantive rejecting controls, inherited replay/logs, deterministic reproduced durable evidence, exact merge review and actual post-merge audit. Certified v16.54 and efficiency design unchanged; runner execution/measured speedup unstarted.
