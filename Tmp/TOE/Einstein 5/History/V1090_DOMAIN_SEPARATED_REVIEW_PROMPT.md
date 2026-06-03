# V1090 Domain-Separated Independent Review Prompt

**Status:** external hostile review prompt  
**Scope:** physics-only / recoverability / time-as-pruning

## Target Claim

```text
Admissibility spectra are domain-dependent: positive Ω_M uses Π_pair; signed Ω_M uses Π_pair + sign_counts; ordered Ω_seq requires order-sensitive spectra.
```

## Prompt

```text
You are an independent hostile reviewer. Review V1089 only.

Do not extend the model. Do not improve the model. Try to falsify the domain-separated claim.

Core frame:
- Do not assume physical spacetime.
- Do not assume physical clock time.
- tau is pruning / recoverability order.
- Geometry-like Omega is what pruning leaves invariant.
- The admissibility spectrum is domain-dependent.

V1089 domain-separated claim:
1. Positive/nonnegative retained geometry Omega_M: Pi_pair is the certificate candidate.
2. Signed retained geometry Omega_M: Pi_signed = (Pi_pair, sign_counts) is the repair candidate.
3. Ordered microhistory Omega_seq: order-sensitive spectra are required.

Definitions:
- Pi_pair(E) = multiset({x_i} union {x_i+x_j : i<j})
- sign_counts(E) = (#negative, #zero, #positive)
- Omega_M(E) = unordered retained multiset / partition recoverability geometry
- Omega_seq(E) = ordered microhistory geometry

Falsification targets:
1. Positive Ω_M failure:
   Find E1,E2 with Pi_pair(E1)=Pi_pair(E2) but Omega_M(E1)!=Omega_M(E2).

2. Signed Ω_M failure:
   Find E1,E2 with Pi_pair(E1)=Pi_pair(E2) and sign_counts(E1)=sign_counts(E2), but Omega_M(E1)!=Omega_M(E2).

3. Ordered-boundary verification:
   Confirm unordered spectra do not certify Omega_seq.

4. Regime-boundary audit:
   Determine whether the split between positive, signed, and ordered regimes is mathematically legitimate.

Pass condition:
No counterexample in the tested domains for the positive and signed scoped claims, and ordered-history failure boundary is reproduced.

Failure condition:
Any same-spectrum/different-Omega_M pair inside the claimed regime.

Strict boundary:
Do not claim physical spacetime, clock time, General Relativity, Einstein equations, ADM recovery, quantum gravity, or universal theorem closure.

```

## Review Tasks

| ID | Task | Instruction |
|---|---|---|
| F1 | Positive Ω_M attack | Find E1,E2 with same Π_pair but different positive/nonnegative Ω_M. |
| F2 | Signed Ω_M attack | Find E1,E2 with same (Π_pair, sign_counts) but different signed Ω_M. |
| F3 | Ordered Ω_seq boundary | Confirm unordered spectra fail when raw order is retained. |
| F4 | Domain legitimacy | Assess whether the positive/signed/ordered regime split is mathematically legitimate. |
| F5 | Smallest counterexample | If failure exists, report the smallest domain, alphabet, length, and exact E1,E2. |
| F6 | No expansion | Do not add new spectra unless reporting a failure boundary. |
