# V1016 Information-Theoretic Reformulation

**Status:** theorem-boundary reformulation completed  
**Purpose:** Translate the recoverable-legitimacy result into information-loss language.

## Core Reframing

The failure mode is not mystical or merely philosophical.

It is an information problem.

Let:

```text
H = E × R
F(H) = (S(H), Ω(H))
```

where:

```text
E = event/order structure
R = provenance metadata
F = observable/geometry compression
```

If `F` maps multiple provenance variants into the same observable class, then `F` has lost provenance information.

## Key Quantity

```text
I_missing = log2(|R_equivalence_class|)
```

Where:

```text
R_equivalence_class = unresolved provenance variants sharing the same F(H)
```

If:

```text
I_missing > 0
```

then observable certification is underdetermined.

If:

```text
I_missing = 0
```

then provenance is already fully encoded in the observable.

## Theorem Form

```text
If H = E × R and F(H) = (S(H), Ω(H)) does not injectively encode R,
then legitimacy over R cannot be certified from F alone.

The missing certification information is at least:

I_missing = log2(|R_equivalence_class|)
```

## Results Table

The generated CSV sweeps provenance variant counts and leakage fractions.

Summary:

```text
If observable map F(H)=(S,Omega) collapses multiple provenance variants into the same equivalence class, then F lacks the bits needed to certify provenance legitimacy.
```

## Boundary Hardened

The theorem is not:

```text
observables can never certify legitimacy
```

The theorem is:

```text
compressed observables cannot certify legitimacy when they have discarded provenance bits
```

If `F` fully embeds provenance, then `F` is no longer merely a visible/geometry observable. It has become a provenance-bearing observable.

## Bridge Meaning

This sharpens the bridge:

```text
visible state
+ Ω-like geometry
```

fails when those observables collapse provenance distinctions.

Therefore the missing layer is not arbitrary. It is the missing information required to distinguish histories in the same observable equivalence class.

## Correct Scientific Claim

```text
Recoverable legitimacy requires enough information to distinguish legitimate
from illegitimate provenance variants inside an observable equivalence class.
```

Genesis Pin is one sufficient mechanism for supplying that missing information in the tested stack.

## Next Step

```text
V1017 — Entropy / Equivalence-Class Audit
```

Measure ambiguity as an entropy over observable equivalence classes and distinguish:

```text
observable entropy
provenance entropy
recoverability entropy
```
