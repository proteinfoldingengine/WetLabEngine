# UQCF-GEM v16.27 — Increment-attribution closure

## Completion and corrected evidence status

**The finding is confirmed by a replacement independent full-path verifier.** See the [completed v16.27 report](V16_27_COMPLETION_REPORT.md), [complete findings](demos/v16.27-increment-attribution-closure/completion/RESULTS.md), [proofs and types C1–C7](demos/v16.27-increment-attribution-closure/completion/PROOFS.md), and [publication evidence](demos/v16.27-increment-attribution-closure/completion/PUBLICATION_EVIDENCE.json).

The original verifier called the producer for enumeration. The completion contract exposed seven accepting-invalid-certificate failures. The new verifier imports no producer, reconstructs ALL legal event permutations and rejects those corruptions. Corrected scientific run **36625099103**, execution **a89f4cabc484612ed2924247245a0a8a2adab6d2**, passed **170 tests** and verified all original 3,486 endpoints/56,498 paths plus the actual relabeled copies. Complete raw path/state certificates are durably published, not just aggregate digests. The separate publication receipt records its actual execution.

This completes **16.27**, not a new stage. The canonical endpoint quantity here is a difference in consistency-testing order h, not an amount of information loss or physical time. No physical-time or geometry conclusion follows. Review is self-review with an algorithmically independent verifier, not a separate reviewer.

## Initial report (preserved below)

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
