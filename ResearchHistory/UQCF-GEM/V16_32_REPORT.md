# UQCF-GEM v16.32 — Retained-state reconstruction closure

## Result

[
oxed{	ext{The v16.31 value-level closure is NONINJECTIVE on retained cover states.}}
]

A three-vertex, two-view counterexample is sufficient.

Tree: root 0 with children 1,2.

Two legal states in the same endpoint interval:

- L = ({0},{0,1,2})
- R = ({0,1},{0,1,2})

They are different indexed retained covers, but both have

[
	au=(1,0,0),qquad h=1
]

and identical normalized component-value signature. The extra occurrence of child 1 in the first view is redundant for every minimum-cover count.

The bounded four-vertex audit searched **4,397 endpoint intervals** and **36,178 legal state occurrences**. It found **28,937 excess occurrences in collision classes** for both tau and the complete frozen value-level signature.

The exact information not represented by the closure is **redundant labeled retained-incidence identity**. Adding the full incidence relation would reconstruct the state but would simply reinsert the object being reconstructed, so v16.32 does not call that a new invariant.

Scientific search/GREEN: run **36651291089**, SHA `fbe644e31ab92713b5449e788a435c97936a8241`.

See [findings](demos/v16.32-retained-state-reconstruction/RESULTS.md), [proofs](demos/v16.32-retained-state-reconstruction/PROOFS.md), and [preregistration](demos/v16.32-retained-state-reconstruction/PREREGISTRATION.md).

No physical information-loss, geometry, or temporal claim is inferred.
