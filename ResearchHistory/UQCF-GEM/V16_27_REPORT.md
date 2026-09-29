# UQCF-GEM v16.27 — Increment-attribution closure

v16.27 asks whether v16.26's atomic 0/1 increments belong canonically to the removed event.

**Answer: no.**

An explicit two-child witness gives two legal pruning orders with identical endpoints and identical removed events. In one order child 1 carries delta h=1 and child 2 carries 0; reversing the order swaps those assignments. Both totals equal the same endpoint invariant h(final)-h(initial)=1.

Bounded exhaustive search through four vertices:
- 3,486 endpoint refinements
- 3,446 with multiple legal atomic paths
- 1,091 with path-dependent per-event attribution
- 56,498 legal paths checked

Therefore the endpoint total is canonical, while event-level attribution is generally state/order dependent.

Scientific GREEN: run **36618145414**.

See [findings](demos/v16.27-increment-attribution-closure/RESULTS.md) and [proof ledger](demos/v16.27-increment-attribution-closure/TYPE_AND_PROOF.md).

No fundamental time, response model, or geometry is introduced.
