# v16.26 — Atomic consistency-increment law

## Result

For one lawful atomic same-union pruning—removing one leaf from exactly one indexed retained view—the local consistency number at the affected parent and the global consistency order can each increase by **at most one**.

If c is the removed child of v:

- all tau_u for u != v are unchanged;
- tau_v(after)-tau_v(before) is 0 or 1;
- h(after)-h(before) is 0 or 1.

The exact local trigger is combinatorial: tau_v rises iff **every old minimum cover of the children of v is destroyed by deleting that incidence**. The global h rises only when the resulting local value exceeds the previous global maximum.

## Complete bounded audit

All atomic same-union deletions from every legal cover of at most four views were independently enumerated on all 17 rooted unordered trees through five vertices:

- atomic deletions: **19,995**
- local trigger events: **4,111**
- global h increments: **4,090**
- jumps larger than one: **0**

The 21 trigger events that did not raise global h are important: a local information bottleneck can become stricter while another vertex already determines the same global maximum. Therefore the local trigger and global increment are not interchangeable.

## Factorization law

Every same-union componentwise pruning can be factored into legal leaf deletions that preserve the union at every step. Along any such factorization,

**h(final)-h(initial) = sum of atomic delta h**, with every summand in {0,1}.

This is ordinary telescoping of the already-defined endpoint invariant h, not a new fundamental time variable. Different lawful pruning orders may place the unit increments at different steps; only the total endpoint difference is canonical.

## Evidence

Wiring RED: run **36614097664** failed with implementation absent.

The preregistered strict witness was corrected before adjudication because the first candidate still had a surviving two-view cover. The corrected minimal witness is child sets {1,2}, {2}, {3} -> {1}, {2}, {3}, giving h:2->3.

An intermediate full campaign run completed the v16.26 science but failed inherited regressions solely because SymPy was not installed. That run is not called GREEN.

Final scientific GREEN: run **36614522299**, execution SHA `28bbd88f6b3c5da48540d400c45485ccda3d4452`. It passed the complete v16.26 campaign and inherited v16.25/v16.24 regressions.

## Scope

This is a theorem about the retained-view consistency order under actual atomic pruning. It introduces no response law, geometry, physical source postulate, or fundamental time.

**Time is pruning / ordered recoverability update.**
