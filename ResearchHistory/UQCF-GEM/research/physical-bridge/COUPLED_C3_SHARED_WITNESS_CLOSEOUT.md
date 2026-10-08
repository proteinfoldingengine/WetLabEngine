# C3 shared-witness channel — final scoped closeout
Status: CLOSED within the declared finite native transition/observation model.
Broader C3, native observer access/progress and C4-C6: OPEN.
No numbered v16 certification, full inherited-stack post-merge replay or physical derivation is claimed.

## Exact result

For four disjoint core-pair roots and one spectator w permitted on the first two roots, let x,y indicate its two incidences. The global minimum hitting number satisfies tau=4-xy; every declared toggle preserves floor 2 and band [3,4].

An observed tau=3 certifies x=y=1. After this synchronization witness, freezing the first incidence gives y=4-tau at every later ordered slice. Under the exactly-once actual-toggle-or-NOOP relation with no other writers, a change of tau is equivalent to an actual root-2 toggle. Observed deletion/addition permits payload cleanup and renewal for arbitrary finite sequences. The universal finite-prefix statement follows by induction, not by treating four-state enumeration as a physical theorem.

The contribution beyond the earlier static overlap counterexample is a reusable synchronized conditional information channel. It does not recover unknown initial bits, certify anchor cleanup, guarantee synchronization/progress under arbitrary rejection, or derive access to exact tau.

## Immutable chain and reproducible evidence

- Scope: 6b38dddb62b34ced1098c88f214b0190b2ebec7c.
- Proof: 1c5d58a857a633854ab7485e9a0d0cf409f333c5, unchanged.
- Prospective verification contract, tests and preserved local RED: a9c833a178343e73c08ddd701c4a00d200a48c1b.
- Independent code and scientific execution snapshot: 159c1b119e3bc0707837aecf3a3d01c04b52e2f6.
- Verification/review run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37856079404.
- Verification/review workflow: 1224e2cf3daf89f71e55818f6fd97240e5f46a0b.
- Accepted raw review, reconciliation and durable originals: fd5103473926d12553240c275b3d4fe3cb50154b.
- Separate publication audit: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37856637045.
- Audit workflow: 2b9399b1896d4240a76a052e059c59c0e0e0e2fb.
- Audit ACCEPTED with zero issues; see COUPLED_C3_SHARED_WITNESS_PUBLICATION_AUDIT.md for exact reconciliation.

Actual checks: 8 new contract tests, 28 inherited tests, complete 4-state/24-outcome reconstruction, 6 fixed-anchor outcomes, byte-identical second-process production, and unchanged inherited A12 bounded baseline (35792 primary states, 508 families, 33 fixtures, 11 rejecting controls). Producer uses full-carrier subset enumeration; verifier independently minimizes unions of one chosen representative per root. Full canonical identity comparison rejects missing/duplicate/substituted rows, wrong values/types, forged claims/provenance and corrupted counterexamples. Initial local failures remain preserved; no GitHub RED run is claimed.

Reproduce at the scientific snapshot:
    ROOT=ResearchHistory/UQCF-GEM/research/physical-bridge
    python3 -m unittest discover -s "$ROOT/shared_witness" -p test_shared_witness.py -v
    python3 "$ROOT/shared_witness/shared_witness_producer.py" > graph.json
    python3 "$ROOT/shared_witness/shared_witness_independent.py" graph.json

The original three ZIPs, all scientific members, full job logs, source digests and exact audit submission are preserved under evidence/c3-shared-witness-37856079404/. Prior review history and prior rejecting controls are unchanged. The publication audit does not grant automatic authority to certify a theorem; the primary author separately reconciled the proof, controls and provenance before this closeout.

## Remaining first-principles obligation

The unresolved input is an accessible initialized native record sufficient to distinguish the synchronized channel states. Deriving a coordinate from a full hidden-support read, or supplying actual-event success as an acknowledgement, would assume the missing information. The inherited full-palette miss-count update theorem explicitly assumes correct initialization and active-root support. Its algebraic update law alone does not close observer access.

Next work must trace a sufficient record's initialization and update inputs to an already available path-A native interface, separate record access from progress, and reject circular access arguments. No force, geometry, fundamental time, continuum or GR result follows here.
