# C3 ordered-event capacity initialization — frozen theorem-first scope

Date: 2026-10-07.
Status: PROSPECTIVE ANALYTICAL SCOPE; not independently accepted.

Parent native retained-interface closeout COUPLED_C3_NATIVE_INTERFACE_CLOSEOUT.md at 59c330c4ba455bd7e12ff3aa157cebbf0baa1878.

## Scientific question

Can the capacity bit b=1[Z nonempty] be reconstructed from an ORDERED EVENT HISTORY without inspecting the hidden spectator supports at decision time? Distinguish known genesis/seed, unknown initial occupancy, and events not visible to the retained controller.

## Declared carrier and native prehistory

Four roots E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), floor2, 3<=tau<=4. Finite spectator palette T disjoint from a,b,c,d,e,w.

A prepared baseline B=E(empty) is KNOWN as an initial condition. A prehistory consists only of admissible native spectator toggles +z(r4), -z(r4), z in T, while the three triangle roots and core r4={d,e} remain unchanged. Each toggle is valid only when adding absent z or deleting present z. All prepared states have tau=3 and floor2.

Event channel E_full supplies ordered spectator-toggle direction (+/-), labelled root r4, and optionally label z. A coarser channel E_count supplies only root r4 and direction of a valid spectator toggle; it does not supply spectator identities. E_core omits all spectator toggles.

## Required theorem and rejecting controls

1. From a known empty seed Z0=empty and full valid spectator event stream, derive exact Z by native set toggles; from direction-only E_count derive q=|Z| by q'=q+1 on addition and q'=q-1 on deletion; prove b=1[q>0] and no hidden support read is needed after seed.
2. For arbitrary known seed cardinality q0, show q=q0+sum event signs; identity reconstruction may require more information, but b does not.
3. Without an initial count/seed and with identical observed event stream, prove b is not generally determined: empty versus singleton spectator states with no observed events are indistinguishable. Also show E_core with identical baseline and hidden spectator additions cannot determine b.
4. Prove q cannot in general be updated from b alone: states with |Z|=1 and |Z|=2 have same b=1, but a single legal spectator deletion yields b'=0 versus b'=1. This identifies count as a sufficient update state and b as insufficient for arbitrary ongoing spectator deletions.
5. A known empty baseline plus all spectator event directions is a CONDITIONAL information interface, not a derivation that UQCF-GEM's observer already possesses the baseline, event completeness, or spectator root addressability.
6. Compare with existing full-palette M_R singleton coordinates and core-only retained R. Show q is a smaller retained statistic for this capacity query but not a replacement for M_R's general legality functions.
7. Do not infer geometry, force, energy, observer-accessibility or fundamental time.

No numerical campaign. Freeze proof, author audit, fresh independent mathematical review, then publication audit and immutable closeout if accepted.
