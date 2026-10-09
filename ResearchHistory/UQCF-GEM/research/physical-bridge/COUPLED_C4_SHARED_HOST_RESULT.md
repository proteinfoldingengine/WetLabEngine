# Shared-host multi-block completion by native cover substitution
Status: frozen analytical argument; independent verification/review pending.
Scope commit: 0da4cab896c7f60d4aa244372e5bd104cddca097.

## 1. Carrier and exact task
Let k>=1. Pool L has k+2 distinct labels; B,C,w and the finite spectator palette T are disjoint from L and one another.
Block i consists of labelled roots R_i0={A_i,B} union Z_i0 and R_i1={A_i,C} union Z_i1, with distinct pool labels A_i.
There is one shared base root R_b={B,C} union Z_b, and one shared host R_h={D,E} union Z_h, where {D,E}=L minus {A_i}.
All Z are arbitrary subsets of T, held fixed and unknown to the controller. The source satisfies 3<=tau<=4 and positive immutable floors f_r<=2+|Z_r|. Since {B,C,E} covers the source, its hitting number is exactly3.

A goal is any injection i->G_i from the labelled blocks into L. Each block must replace its apex by G_i, the host must contain the remaining two pool labels, all Z must remain in their original roots, and w must be absent at completion.

## 2. Cover-substitution lemma
For two families S=(S_r) and U=(U_r) on the same labelled roots, suppose a label map phi satisfies phi(U_r) subseteq S_r for every r.
Every hitting set H of U gives a hitting set phi(H) of S: for each root choose x in H intersect U_r, then phi(x) belongs to phi(H) intersect S_r. Its cardinality is at most |H|. Consequently tau(S)<=tau(U).

The map need not be injective. It is a proof device on actual label incidences, not an identification of unrelated physical carriers or an observer measurement. Both families and the same root slots are specified natively.

## 3. One shared-host exchange
Choose block i, its current apex A, one host label D and the other host label E. Execute:
+w(h), -D(h), +D(i0), -A(i0), +D(i1), -A(i1), +A(h), -w(h).

Every command is syntactically determined from the known core phase; no spectator shares a named core/marker label. The host/root sizes never fall below their macro-source sizes: add-before-delete preserves the block sizes and w provides the host's replacement incidence. Other roots do not change. Thus every original admissible floor is preserved, including saturated unequal floors.

For each of the nine slices, define phi relative to this macro's source. Fix all spectators, B,C,E and every other block's apex. Always send w to E.
- Slices0,1,2: fix A,D.
- Slices3,4,5,6: send D to A and fix A.
- Slices7,8: send D to A and A to D.
Here slice0 is the source and slice j follows j actual edits.

At slices0-2, D has not entered the block; the only new incidence is w in the host, whose source contains E.
At slices3-6, D occurs only in a subset of the two selected block roots, both of which originally contained A. Any remaining A is still in its original block roots; neither A nor D is on the host.
At slices7-8, A occurs only on the host, whose source contained D, while D is on the selected block's two roots, whose source contained A.
All other core and spectator incidences are unchanged. Therefore phi(U_r) subseteq S_r at EVERY root and slice, regardless of the hidden spectator pattern.

The lemma gives tau(U)>=tau(S)=3. The fixed set {B,C,E} is a three-cover throughout: B,C cover every block and the shared base, while E remains on the host. Thus tau(U)=3 exactly after every primitive.

At the endpoint the selected apex and D have exchanged roles, the host again contains two pool labels, all spectator incidences are unchanged, and w is absent. Root sizes equal their macro-source sizes.

## 4. Why genuinely coupled spectators are covered
No separation of Z_h from block spectators is assumed or derived here. For k=2, take exactly one spectator z on R_00 and the host, with all other Z empty. The isolated four-root subfamily consisting of block0, base and host has a two-cover {C,z}. But the full six-root carrier is protected: no two core labels cover the core skeleton, and no core label covers all roots not hit by z (R_01,R_10,R_11,R_b). These latter four supports have empty common intersection. A spectator/core two-cover is therefore impossible, and there is only one spectator. The explicit three-cover proves tau=3.

The second block thus supplies protection absent from the isolated first block. Applying the earlier one-block separation theorem independently would reject this legitimate source. Section3 instead uses the global source's cover obstruction and preserves it by substitution. It applies to any number of spectator labels, including ones shared among many roots, provided the full source is protected.

## 5. Exact completion for arbitrary target injections
The controller retains current core apex allocation, requested goal allocation, fixed block order and phase; it never acquires Z or a count field.

Process blocks i=1,...,k:
- If A_i=G_i, leave it fixed.
- If G_i is in the host, exchange block i with host label G_i.
- Otherwise G_i is the current apex of a different block j. That block is not already fixed: distinct goal labels prevent a fixed earlier block from holding G_i. Choose a host label using the supplied label order, exchange block j with it, then exchange block i with the now-hosted G_i.

Each stage fixes block i and changes no previously fixed block. At most two exchanges are used per stage. Hence the integer count of still-unprocessed block positions decreases, and the finite constructed schedule uses at most2k exchanges and16k actual incidence edits. This bound is not claimed optimal.

Section3 applies inductively after every exchange because the same carrier form, protection, root sizes, floors and spectator data are restored, with w absent. On completion all block apexes equal their goals. Since pool labels are exchanged rather than created/deleted at boundaries, the host contains precisely the complementary pair. Every labelled target support is exact, including its untouched hidden spectator set.

## 6. Operational and physical boundaries
This is a uniformly legal committed-edit construction. Phase bookkeeping does not prove that attempted requests commit, that their resolution is observable, or that the controller is physically realized. Arbitrary NOOP semantics may prevent completion, exactly as in the prior checkpoints.
Initial native admissibility, known core roles and a reserved fresh w are premises. The proof removes any need to inspect spectators for the stated repair; it does not derive general observation/access or native enforcement.
No unrestricted core skeleton, additional pool incidence, moving spectator, arbitrary root identification, shortest-path result, physical force, spacetime, dark matter or fundamental time is inferred.

## 7. Verification contract
The frozen bounded domain checks all two-spectator masks at k=2 in the canonical source, all four single exchanges there, and all source/goal apex injections with one spectator. Production uses actual bit toggles and subset transversal enumeration. Independent reconstruction uses closed-form phase states, exact root-representative unions and independent goal planning. All source/path/goal identities and values are compared.
The source-to-slice containment maps, explicit three-cover, size minima, exact boundary renewal and target allocations are checked directly. The arbitrary-k and arbitrary-palette statements rest on sections2-5, not finite test counts.
Historical one-block closeout and all observer-origin failures remain unchanged. This is a new bounded C4 repair checkpoint, not closure of broader C3 observer origin or a numbered v16 certification.
