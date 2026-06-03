# V1058 External Review and Falsification Packet

**Status:** external pressure-testing handoff  
**Scope:** physics-only / it-from-bit / recoverability / time-as-pruning

## Primary Instruction to Reviewer

```text
Do not extend the model. Do not improve the law. Attempt to falsify the refined law.
```

## Refined Law Under Review

```text
T ~Ω identity iff [Π_sum(T(E)) = Π_sum(E)] and [Π_moment(T(E)) = Π_moment(E)].
```

## Core Physics Frame

```text
Time is pruning. τ is recoverability order, not physical clock time. Geometry-like Ω is the invariant residue of admissible pruning.
```

## Included Artifacts

| Version | Artifact | Purpose |
|---|---|---|
| V1056 | Final scientific report-out packet | Main physics summary and claim boundaries. |
| V1054 | Minimal theorem draft | Definitions, theorem candidate, proof sketch, caveats. |
| V1055 | Symbolic exhaustion report | Tiny complete transform-family support. |
| V1057 | Independent reimplementation audit packet | Clean reimplementation protocol. |

## Review Tasks

| ID | Task | Instruction |
|---|---|---|
| R1 | Reimplement from clean definitions only | Do not inspect prior code. Use only V1057 definitions and theorem statement. |
| R2 | Attempt to falsify refined law | Search for T where prediction disagrees with Ω-gauge equivalence. |
| R3 | Verify old-law failure | Confirm partition-sum-only law can fail under adversarial transforms. |
| R4 | Verify refined repair | Confirm adding partition-moment spectrum repairs the failure. |
| R5 | Run scale variations | Test across k, L, and transform families. |
| R6 | Run tiny exhaustive case | Exhaust at least one small complete transform family. |
| R7 | Report every counterexample | Any FP/FN must be treated as a law failure or boundary condition. |

## Pass Condition

```text
Independent reviewer reproduces old-law failure, refined-law repair, randomized/scale closure, and tiny exhaustive support without using prior implementation code.
```

## Failure Condition

```text
Any independently generated transformation T where the refined law prediction disagrees with Ω-gauge equivalence.
```

## Strict Claim Boundary

This review packet does not claim:

```text
physical spacetime
physical clock time
General Relativity
Einstein equations
full ADM recovery
quantum gravity
universal theorem over all maps
```

## Correct Review Posture

```text
Try to break the law.
Treat every mismatch as meaningful.
Do not assume the prior implementation is correct.
Do not reuse prior helper functions.
```

## Scientific Meaning If It Survives

```text
If an independent implementation reproduces the refined law from clean definitions,
the result becomes much less likely to be an implementation artifact and much more
likely to be intrinsic to the finite recoverability model.
```
