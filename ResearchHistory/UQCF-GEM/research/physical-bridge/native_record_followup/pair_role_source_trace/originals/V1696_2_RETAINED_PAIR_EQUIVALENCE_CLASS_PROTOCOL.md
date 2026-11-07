# V1696.2 — Retained Pair Equivalence Class Protocol

**Verdict:** `RETAINED_PAIR_EQUIVALENCE_CLASS_PROTOCOL_FROZEN_NO_EXECUTION`

## Why this reset is needed

V1696.1 showed that cross-scale pair transport failed even after replacing nearest-cell matching with aggregation-derived `R_pair`.

That means the problem is likely not:

```text
find a better vector transport
```

The better question is:

```text
what does it mean for retained pair identity to survive coarse-graining?
```

---

## New object

Define:

```text
[p]_R
```

as a retained pair equivalence class.

Two product pairs `p` and `q` are equivalent if they preserve the same retained product role under:

```text
Phi_oplus response
orientation
support/provenance admissibility
D1/D2 action profile
signed pair-Gram context
retained-order dependency class
```

This is not a vector and not a nearest coarse/fine cell match.

It is a quotient object.

---

## Equivalence requirements

```text
E1 product role
E2 orientation
E3 D1/D2 derivative-response profile
E4 signed pair-Gram relation
E5 support/provenance admissibility
E6 retained-order dependency class
```

A pair identity survives only if these structures survive up to declared role-preserving morphism.

---

## Coarse-graining rule

A coarse retained pair class is:

```text
[P_A^C]_R
=
quotient-aggregate({[p_a^F]_R : a ∈ block(A)})
```

A coarse class exists only if the fine classes form a compatible role-preserving family.

If not, coarse pair identity is undefined.

Do not force it.

---

## Class signature

Define:

```text
Sig([p]_R)
=
(role, orientation, D1D2_profile, signed_Gram_context, support_class, order_class)
```

Coarse preservation means:

```text
Sig([P_A^C]_R)
≈
quotient-aggregate Sig({[p_a^F]_R})
```

better than class-breaking nulls.

---

## Killer nulls

```text
N_role_preserved_vector_scrambled
N_D1D2_profile_scramble
N_orientation_flip
N_support_class_shuffle
N_local_signature_preserved_class_broken
```

These preserve local pair vector statistics where possible while breaking the equivalence-class identity.

---

## Promotion boundary

Allowed:

```text
retained pair equivalence-class diagnostic
```

Not allowed:

```text
cross-scale vector transport law
D = rho + Q compatibility
global generated-algebra law
```

## Next

```text
V1696.3 — Retained Pair Equivalence Class Python Test
```
