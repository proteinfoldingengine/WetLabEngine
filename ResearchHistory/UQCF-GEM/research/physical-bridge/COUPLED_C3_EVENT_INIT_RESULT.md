# C3 ordered-event initialization: conditional count reconstruction and seed obstruction

Date: 2026-10-07.
Status: AUTHOR-SIDE ANALYTICAL PROOF CANDIDATE; independent review pending.
Frozen scope COUPLED_C3_EVENT_INIT_SCOPE.md at a7e2b8f66844286ea129b6c2c210f9fc41f2989a.

## 1. Native carrier and prepared-event domain

Let T be a finite spectator palette disjoint from {a,b,c,d,e,w}. Four labelled roots have supports
 E(Z)=({a,b},{b,c},{a,c},{d,e} union Z)
for Z subseteq T, original floors2, and band 3<=tau<=4.

A spectator-only prepared prehistory changes Z by one legal native +z(r4) or -z(r4) at a time; core supports remain unchanged. An addition is valid only for z notin Z, and a deletion only for z in Z.

For every Z, the first three roots form a triangle with hitting number2 and the fourth is nonempty and disjoint from their labels. Hence tau(E(Z))=3. The fourth root has size2+|Z|>=2. Every declared legal spectator toggle therefore stays within the protected band and respects original floors.

This is an ORDERED native update sequence, not an assumption of primitive physical time.

## 2. Reconstruction with a known seed and complete event directions

Assume the controller is legitimately supplied a seed q0=|Z0| and a complete ordered record of directions eps_j in {+1,-1} for every spectator incidence change on labelled r4. Events are guaranteed to be syntactically valid in the underlying carrier.

Define q_n=q0+sum_{j=1}^n eps_j.

Induction: at a valid +z event, the spectator cardinality increases by exactly one; at a valid -z event it decreases by exactly one. Therefore q_n=|Z_n| for every prefix. The retained bit is b_n=1[q_n>0].

If the seed is known to be empty, q0=0. This permits reconstruction of b from the event-direction ledger without inspecting the hidden Z at decision time. The ledger must be complete, address r4, distinguish spectator events from core events, and preserve add/delete direction. None of those observation capabilities is derived here.

If the full event labels z are also retained and the exact initial Z0 is known, the controller can reconstruct Z_n itself by native set additions and deletions. Cardinality reconstruction does not need the label identities.

## 3. Exact indistinguishability without seed or complete event access

A. Unknown seed. Let T contain z. Compare initial worlds Z0=empty and Z0={z}. If no subsequent event is observed, both produce the same empty event transcript but b0=0 versus b0=1. Thus no function of the transcript alone determines b without seed information.

B. Core-only channel. Start from the SAME known empty baseline in both worlds. World A performs no spectator events; world B performs one valid +z(r4). A channel that omits all spectator events produces the same core-only transcript in both, yet b differs. Thus knowing the baseline is not enough if event visibility is incomplete.

C. Unknown offset after a shared nonempty transcript. If an event-direction transcript is consistent with two distinct nonnegative initial counts, q_n differs by the initial offset. The formula does not magically remove the seed dependency.

These are information-access obstructions for the specified channels, not a universal impossibility theorem for every conceivable observer.

## 4. One bit is insufficient for update under arbitrary spectator deletions

Assume T contains distinct u,v. Compare Z={u} and Z'={u,v}. Both have b=1. Apply the SAME valid native deletion -u(r4) to both:
 Z becomes empty, hence b'=0;
 Z' becomes {v}, hence b'=1.

Even if the root address, deletion direction and deleted label u are supplied, b alone cannot determine the updated b. Therefore b is sufficient for a ONE-TIME optimal path choice at the prepared source, but not update-closed under arbitrary ongoing spectator deletions.

By contrast q=|Z| updates exactly by +/-1 for every valid spectator event, so it is a sufficient update statistic for b over this event domain. This does not establish q as minimal for every restricted event grammar; if deletions are forbidden, b alone is update-closed.

## 5. Relationship to existing full-palette miss counts

The earlier published dynamic residual field M_R(H), with residual family {r4}, gives M_R({z})=1-1[z in Z]. Therefore q=sum_{z in T}(1-M_R({z})).

The event-derived q is a coarser statistic than the full vector of singleton spectator miss counts. It suffices to decide whether r4 has spectator floor slack and to choose the six-versus-eight-edit policy in the previously closed hidden-Z family. It does NOT replace full M_R(H) for arbitrary cover/legality queries or spectator-addressed edit syntax.

If initialized M_R is already available, q can be computed from it. If instead a complete event-direction ledger with known q0 is available, q can be updated without storing spectator identities. Neither route proves native observer access to the initial counts or the complete ledger.

## 6. Conditional optimal repair controller

At any prepared E(Z), IF the event-derived q is legitimate and accurate, choose:
 q=0: the closed eight-edit +w(r4),-d(r4),+d(r1),-a(r1),+d(r3),-a(r3),+a(r4),-w(r4) route;
 q>0: the closed six-edit -d(r4),+d(r1),-a(r1),+d(r3),-a(r3),+a(r4) route.

The previous independently closed theorem proves each is shortest and protected in its respective fiber. The event theorem supplies only the conditional ability to select the branch. It does not derive the origin of the known seed or of the event visibility.

## 7. Scientific boundary

This proof separates three gates:
- Representation: the full-palette miss-count certificate mathematically contains b.
- Update: a known seed plus complete valid ordered spectator event directions yields q and b without repeated hidden-state reads.
- Initialization/access: a native reason why the seed and event channel are actually available remains UNPROVED.

No physical force, geometry, continuum, GR/ADM, energy, observer field or fundamental time follows. Broader C3 retained host-selection and C4-C6 remain OPEN.
