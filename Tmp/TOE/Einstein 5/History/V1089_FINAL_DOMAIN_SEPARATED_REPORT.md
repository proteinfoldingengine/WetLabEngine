# V1089 Final Domain-Separated Report

**Status:** final scoped report after signed-domain repair  
**Scope:** physics-only / recoverability / time-as-pruning

## Core Result

```text
The admissibility spectrum required to preserve retained geometry depends on the algebraic and chronological domain. Positive retained residues can be certified by Π_pair in tested finite domains; signed retained residues require sign_counts; ordered microhistory requires order-sensitive spectra.
```

## Time-as-Pruning Statement

```text
τ is pruning/recoverability order, not physical clock time. Geometry-like Ω is what pruning leaves invariant, but what must be preserved depends on what Ω retains.
```

## Domain-Separated Regimes

| Regime | Required Spectrum | Meaning |
|---|---|---|
| Positive / nonnegative retained geometry Ω_M | Π_pair | Local pairwise recoverability is sufficient in tested finite domains. |
| Signed retained geometry Ω_M | Π_pair + sign_counts | Sign/cancellation data is required in addition to pairwise recoverability. |
| Ordered microhistory Ω_seq | Order-sensitive spectrum | Raw chronology requires order-sensitive preservation. |

## Milestone Chain

| Version | Theme | Result |
|---|---|---|
| V1059 | Hostile review | Scalar invariants failed; spectral richness became central. |
| V1071 | Positive/multiset Π_pair stress | Π_pair remained collision-free through N=40. |
| V1075 | Non-partition falsification | Π_pair works for multiset Ω_M but fails for ordered Ω_seq. |
| V1079 | Geometry/chronology separation | Many ordered histories collapse into retained geometry; Π_pair certifies Ω_M. |
| V1083 | Signed-domain failure | Π_pair failed for signed retained values: (-2,1,1) vs (-1,-1,2). |
| V1085 | Signed-domain repair | Π_pair + sign_counts repaired bounded signed tests. |
| V1088 | Domain boundary packet | Positive, signed, and ordered regimes separated cleanly. |

## Claim Table

| Status | Claim |
|---|---|
| Supported | Geometry-like Ω_M is retained recoverability geometry after pruning quotients away raw order. |
| Supported | Π_pair certifies positive/multiset Ω_M in bounded tests. |
| Supported | Signed domains require sign/cancellation repair. |
| Supported | Ordered microhistory cannot be certified by unordered pairwise spectra. |
| Boundary | Admissibility spectra are domain-dependent. |
| Not claimed | Universal theorem, physical spacetime, GR, Einstein equations, ADM recovery, quantum gravity. |

## Final Scientific Framing

```text
Time is pruning.
Geometry is what pruning leaves invariant.
But the admissibility spectrum is domain-dependent.
```

This is the key mature result.

The model no longer claims one universal spectrum. It now has explicit domain boundaries:

```text
positive retained residues -> pairwise relational recoverability
signed retained residues -> pairwise recoverability + sign/cancellation information
ordered microhistory -> order-sensitive spectrum
```

## Falsification Conditions

```text
For positive Ω_M: find same Π_pair but different Ω_M. For signed Ω_M: find same (Π_pair, sign_counts) but different Ω_M. For Ω_seq: unordered spectra are insufficient by construction; use order-sensitive tests.
```

## Claim Boundary

This report does not claim:

```text
physical spacetime
physical clock time
General Relativity
Einstein equations
ADM recovery
quantum gravity
universal theorem closure
```

## Recommended Next Step

```text
Independent review of V1089 only.
Do not expand the model until the domain-separated claim is reviewed.
```
