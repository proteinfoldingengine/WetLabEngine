# V1081 Independent Review Prompt for V1080

**Status:** external falsification prompt  
**Scope:** physics-only / retained geometry / time-as-pruning

## Target Claim

```text
Pi_pair certifies retained multiset geometry Omega_M, but does not certify ordered microhistory Omega_seq.
```

## Prompt

```text
You are an independent hostile reviewer. Review V1080 only.

Do not extend the model. Do not improve the model. Try to falsify the scoped claim.

Core frame:
- Do not assume physical spacetime.
- Do not assume physical clock time.
- tau is pruning / recoverability order.
- Omega_M is retained multiset / partition recoverability geometry.
- Omega_seq is ordered microhistory.
- Geometry-like structure is the invariant residue of admissible pruning.

Scoped claim:
Pi_pair certifies retained multiset geometry Omega_M, but does not certify ordered microhistory Omega_seq.

Definitions:
- E: finite retained event / partition structure.
- Omega_M(E): unordered retained multiset / partition geometry.
- Omega_seq(E): ordered microhistory geometry.
- Pi_pair(E): multiset({x_i} union {x_i + x_j : i < j}).

Falsification targets:
1. Find E1,E2 such that Pi_pair(E1)=Pi_pair(E2) but Omega_M(E1) != Omega_M(E2).
2. Confirm that Pi_pair fails for Omega_seq when raw order is retained.
3. Evaluate whether Omega_M is a legitimate retained-geometry quotient or merely a definition that hides the failure.
4. Try broader finite domains if definitions remain coherent.
5. Report the first counterexample, if found.

Pass condition:
No same-Pi_pair/different-Omega_M counterexample found in the tested domains, and ordered-history failure boundary is reproduced.

Failure condition:
Any same-Pi_pair/different-Omega_M pair.

Strict boundary:
Do not claim physical spacetime, clock time, General Relativity, Einstein equations, ADM recovery, quantum gravity, or universal theorem closure.

```

## Review Tasks

| ID | Task | Instruction |
|---|---|---|
| F1 | Falsify Ω_M claim | Find E1,E2 where Π_pair(E1)=Π_pair(E2) but Ω_M(E1)≠Ω_M(E2). |
| F2 | Verify ordered-history failure | Confirm Π_pair does not certify Ω_seq when raw order is retained. |
| F3 | Test quotient validity | Assess whether Ω_M is a legitimate retained-geometry quotient rather than an artifact. |
| F4 | Broaden finite domains | Try non-integer, signed, repeated, graph-like, or weighted retained structures if well-defined. |
| F5 | Report first counterexample | Any same-Π_pair/different-Ω_M collision is decisive. |
| F6 | Do not extend | Do not add new spectra or improve the model unless reporting a failure boundary. |
