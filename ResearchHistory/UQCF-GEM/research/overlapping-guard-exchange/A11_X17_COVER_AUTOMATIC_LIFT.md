# A11.X17 — cover-automatic root lifting and complete mixed-floor repair

Scope:a68e6f04191c70a12f12c7317aaec6a45faca43e.
Parent publication:53f434a4f86cbdeed4517a9784cdadb18470ccec.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for independent WHOLE-ARGUMENT review. Analytical only.

## 1. General sufficient lifting theorem

Fix a finite ordered palette P of k labels, r labelled original root slots, positive original floors a_i<=k, and exact target q>=2. A primitive adds or removes ONE incidence in ONE original root, preserving its floor. Exact-q feasibility implies k>=q.

Select a set B of existing slots whose ORIGINAL floors satisfy

a_i>=k-q+2.

Write J for the remaining labelled slots. A root in B meets EVERY(q-1)-label subset of P because its complement has at most q-2 labels. Call these roots cover-automatic at this declared level. This is a support fact, not a new native constraint or an invented root.

**Theorem X17L (cover-automatic sufficient lift).** Suppose every exact-q endpoint pair on the retained J-subcarrier, with the SAME palette and the retained original floors, has finite native repair with tau in {q-1,q}. Then EVERY exact-q pair on the FULL original carrier has such repair, restoring the complete original labelled/noncompact destination.

At full exact-q endpoints the retained subfamily is itself exact q. Its complete band path lifts while the B supports stay fixed. After the retained destination is reached, repair each B root through its own union with its original destination, using individual incidences. The full tuple is exact q throughout that final restoration.

No native slot is deleted, introduced or permuted. J is an auxiliary mathematical subfamily; its primitives operate in the corresponding EXISTING full-carrier slots. The theorem is a sufficient positive lift. It is NOT an equivalence of unrestricted band graphs and does not justify projecting a full safe path to a retained safe path.

## 2. Universal mixed-profile consequence at target four

**Theorem X17F.** On EVERY finite ordered palette and fixed labelled carrier, EVERY exact-four endpoint pair has complete native{3,4} repair if each original floor satisfies

a_i<=3 OR a_i>=k-2.

There is no restriction on how many large-floor slots occur. Every original destination support is restored. This extends X15's original uniform-floor-three theorem to a broad mixed class WITHOUT a whole-carrier sum-of-floors budget.

Retain only floors below k-2. The displayed hypothesis makes each retained floor belong to{1,2,3}. If any retained floor is1, accepted X3 supplies arbitrary-positive-floor exact-four repair; if a retained floor is2, accepted X4 does; otherwise the retained profile is uniform floor3 and X15 applies. The exact projection theorem supplies actual exact retained endpoints, rather than assuming a convenient core exists or is reachable.

This is a transparent structural lift of accepted COMPLETE mechanisms, not a newly claimed independent incidence handover or a numerical campaign.

**Corollary X17P.** EVERY original positive-floor target-four profile on a palette of at most SIX labels has complete repair whenever exact endpoints exist. At k<4 exact four is infeasible. At4<=k<=6, floors below k-2 are at most3, so the condition in X17F holds automatically. This asserts connectivity, not feasibility of every profile.

Unrestricted mixed-floor target-four on larger palettes, original destination-directed universality and unrestricted nested universality remain open.

## 3. Exact retained endpoints are forced

Let E be a FULL exact-q endpoint. Any hitting set of E hits every retained root, so tau(E_J)<=q.

Suppose E_J had a hitting set of size at most q-1. Extend it, if needed, to a(q-1)-set K in the SAME palette; this is possible since k>=q. K hits every retained root and, by the ORIGINAL floor threshold, every B root. Thus K hits the full tuple, contradicting exact q.

Therefore tau(E_J)=q. In particular J cannot be empty and must have enough actual slots for exact q. If all full slots are cover-automatic, exact-q endpoints are impossible; this is infeasibility, not disconnection.

This proves exactness BEFORE any retained exact-endpoint theorem is invoked. Larger original endpoint supports and unequal B floors do not affect the argument.

## 4. Every lower and upper witness during the lift

Take a supplied COMPLETE retained primitive path E_J->C_J in{q-1,q}. Hold every B support at its original E_i and enact the retained edits in their existing full-carrier slots.

At any intermediate retained tuple A_J, choose a minimum retained hitting set H. Its size is q-1 or q. Every B root meets it: if |H|=q-1 this is the defining floor fact; if |H|=q, it contains a(q-1)-subset already meeting that root. Therefore H hits the FULL tuple. Conversely any full hitting set also hits the retained family. Hence

tau(A_FULL)=tau(A_J)

at EVERY lifted primitive. Both lower and upper bounds are direct; no new upper conversion is required for the lift of an already-converted retained path.

For an explicit lower witness, every palette K of size at most q-2 misses an ACTUAL retained root because tau(A_J)>=q-1. That same existing root misses K in the full tuple. This covers ALL forbidden small sets, including labels appearing only in large roots. The large slots do not provide fictitious independent reserve capacities; the retained actual roots supply all required witnesses.

The retained theorem supplies the next edits, floor legality, progress and finite termination. Enacting its edits changes no B incidence and preserves each retained slot's ORIGINAL floor. Any temporary incidences/repeated edits in that theorem remain native.

## 5. Complete large-root restoration and renewed use

After the retained path ends, its tuple is EXACTLY C_J with transversal q. Process each B slot i in its fixed label order:

1. Add every incidence in C_i missing from its current support E_i.
2. Delete every old-only incidence after C_i is fully present.

This is the finite individual-primitive path E_i->E_i union C_i->C_i. Additions retain the original E_i floor; deletions retain the complete original C_i. No floor is compacted below a_i, including high floors. Only original palette labels are used.

At every intermediate B support, its floor is at least k-q+2, so it meets every(q-1)-set. A retained minimum q-cover continues to hit every B root, while the exact retained family supplies the lower q bound. Thus the FULL hitting number stays EXACT q throughout these restoration edits.

Every unfinished B root has a missing destination incidence to add, or an old-only incidence to delete once its destination is present. Its symmetric difference decreases by one at every such primitive. A finite ordered slot list and finite differences therefore terminate at EVERY ORIGINAL labelled destination support, including excess incidences and repeated support tokens.

The entire full path has two supplied complete phases: retained repair and exact full restoration. At the end all roots equal C, not merely their hitting number. For any finite sequence of full exact-q endpoints satisfying the same carrier hypotheses, repeat the construction. Each leg restores its full exact endpoint; deficits do not accumulate across joins.

The theorem uses no arbitrary mixed-floor token permutation. If the retained proof uses a permutation, it is valid only within that proof's original retained-floor domain and is implemented through its native edits. The B roots stay fixed during those edits and their automatic cover property preserves the full band.

## 6. Why projection is NOT a converse safety theorem

A full level-(q-1) tuple can project to level q-2 or lower, because the B roots may add a hitting obligation when the retained cover is too small. The equality in Section4 assumes the supplied retained path already has tau>=q-1.

A concrete same-carrier control at target4 uses palette1..6, four retained slots of original floor1 and one B slot of original floor4=k-2.

The full tuple
{1},{2},{1},{2},{3,4,5,6}
has hitting number THREE, while its retained projection has hitting number TWO. The full carrier also admits exact-four endpoints.

Indeed start at the exact-four tuple
{1},{2},{3},{4},{3,4,5,6}.
Replace the third singleton3 by1 using add1 then delete3, and then replace the fourth singleton4 by2 using add2 then delete4. The first replacement keeps full level three after leaving the exact endpoint; the second retains full level three because the large root still requires a label outside{1,2}. Every primitive respects its original floor and full tau remains in{3,4}. Its retained projection reaches level two.

Thus projection of a FULL safe prefix need not preserve retained safety even on a carrier with exact-four endpoints. This control is NOT a disconnected endpoint pair or a necessary higher barrier. X17L deliberately supplies a positive lift only; no negative retained obstruction can be promoted to a full native obstruction by this argument.

## 7. Actual mixed class beyond whole-carrier degree budgets

A feasible family illustrates why active protection and ambient floors must be distinguished.

Take k9 and eight retained ORIGINAL floor-three slots: all four triples of{1,2,3,4} and all four triples of{5,6,7,8}. Each complete core requires two labels, so their disjoint union is exact four with supplied minimum cover{1,2,5,6}.

Append ANY m existing large slots with ORIGINAL floor7 and support{1,2,3,4,5,6,9}. These slots satisfy the cover-automatic threshold7=k-2, and every full tuple is still exact four. No additional slot is introduced along a path; this specifies a fixed mixed carrier at the outset.

The class is MUCH larger than this control: X17F connects arbitrary exact-four endpoints with eight floor-three slots and m floor-seven slots, regardless of the retained incidence/core shape or B supports.

For the displayed control with m>=2, every root is already at its original floor, so its only floor-size compaction is itself. Its total original incidence is S=24+7m and maximum label degree is m+3. Any whole-carrier X15N application would need a bound M>=m+3 and, at q4,

r=m+8>=D+M+1,

forcing D<=4. But S>=38>4*9=36, contradicting its required S<=Dk. Thus NO choice of whole-carrier degree parameters supplies that theorem on this control. X17F proves complete repair without weakening those large original floors.

This demonstrates a meaningful removal of the whole-carrier capacity-budget assumption. It does not claim no other inherited guard argument could connect a particular control. The new statement is universal over the full mixed profile, by actual exact projection and retained complete repair.

## 8. Inherited domains and remaining scientific boundary

At q4 the retained original floors are in{1,2,3}. Accepted X3 applies if there is an original floor-one slot, with all other retained floors arbitrary positive; X4 applies for an original floor-two slot; otherwise X15 gives UNIVERSAL uniform-original-floor-three target-four ROOT repair on the same finite ordered palette. All are COMPLETE original labelled/noncompact endpoint results, not merely local moves. Section3 supplies their exact endpoint inputs.

Relevant sources at parent53f434a4f86cbdeed4517a9784cdadb18470ccec:
A11_RESIDUAL_THREE_ANCHOR_LIFT.md(X3), A11_PAIR_ANCHOR_CONNECTIVITY.md(X4), A11_X15_UNIVERSAL_FLOOR_THREE_REPAIR.md. Their immutable accepted review/closeout receipts govern acceptance. Native floor/nonempty rules and conditional child interfaces remain baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.

X15 uniform-floor-three universal closure remains unchanged. X16 density bounds and mixed-floor budget classes remain accepted. X17 adds a sufficient lift for cover-automatic high-floor coordinates and a broad universal mixed profile; it makes no unrestricted mixed-floor, higher-target or nested universality claim.

Original A11 destination-directed scheduling remains OPEN. A retained proof may use temporary/repeated edits and upper conversion; the lifted path inherits that freedom, not a stricter schedule. Conditional child lifting keeps baseline interfaces.

No native slots are erased, no floor is weakened and no new label/slot/geometry is introduced. Unit repair is an upper bound, not a positive minimum for every pair. No physical energy/metric/gravity/fundamental-time or originality claim.

No numerical enumeration, scientific test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. Certified v16.54, frozen prior sources/failed-method classifications and separate accepted efficiency design remain unchanged.
