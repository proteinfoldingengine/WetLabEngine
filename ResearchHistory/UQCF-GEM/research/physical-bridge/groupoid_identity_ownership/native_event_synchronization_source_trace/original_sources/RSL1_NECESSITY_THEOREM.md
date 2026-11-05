# RSL-1 Necessity Theorem — Minimal Retained Action Ledger

## Setup

Inside RAG-0, the finite-capacity conserved-current law family is:

```text
d f_n = b_n
f_n = c_n ⊙ sigma((a_n ⊙ d*phi_n)/c_n)
```

Let:

```text
x_n = (a_n ⊙ d*phi_n)/c_n
A_sigma(x) = integral_0^x sigma(u) du
L_sigma(x) = x sigma(x) - A_sigma(x)
ell_n = c_n ⊙ L_sigma(x_n)
```

## Claim

If a retained state `rho_n` is:

```text
compact
target-blind
generated from current-slice admissible finite-capacity action residuals
closed under ordered-slice composition
not a full history replay
not a learned latent/lookup table
```

then its update must be a monoid homomorphism from slice increments into retained state:

```text
rho_{n+1} = rho_n ⊕ P_G(ell_n)
```

In the minimal vector gauge:

```text
rho_{n+1} = rho_n + P_G(ell_n)
```

## Reason

Composition of ordered slices requires:

```text
Update(Update(rho, ell_1), ell_2)
  ~ Update(rho, Compose(ell_1, ell_2))
```

Associativity plus compactness forbids dependence on the full ledger ordering except through a retained increment. Under the minimal vector representation, every admissible commutative retained-increment monoid embeds as addition up to gauge/equivalence.

## What is forced

```text
additive / monoid retained update form
current-slice finite-capacity action increment
target-blind compact state
```

## What is not forced

```text
specific sigma choice inside Sigma
projection gauge P_G
repair rule
future capacity/conductance/operator coupling
simulation proto-gravity certification
```
