# The Retained Bridge Builds a Non-Metric Local Geometry

## Climbing the rung ladder: metric → connection → curvature, in order

**Frame:** it-from-bit / emergent-geometry, simulation-internal. Following the process, not GR.
**Method:** derive every object from the model's own native kernel; verify each rung with
controls (flat control, associative null, h-stability, matched nulls) before climbing.
**Proofs:** `rung1_*.py`, `rung2_nonmetricity.py`, `rung3_*.py` (+ captured outputs).

---

## Headline

The non-associative information-recombination kernel
`T(dx)=dx+g·(roll(dx)⊙q − dx⊙roll(q))` builds, **at leading order, a non-metric connection**,
and at second order a **positive local curvature**, in a structure that is **irreducibly local**.
This is not Riemannian geometry and not GR — it is a **metric-affine / non-metric geometry**
sourced by the it-from-bit recombination. That is a different, and arguably more interesting,
object than emergent GR.

---

## The rung ladder, with results

### Rung 1 — local metric: REAL (Riemannian)

`g(q) = sym(Jacobian of T at q)` is positive-definite, anisotropic, metric-like.

```
positive-eigenvalue fraction = 1.000
eigenvalue spread ≈ 0.55 … 1.38
triangle-inequality violations = 0.000
```

### Rung 1.5 — globalization: FAILS (irreducibly local)

Local metrics do not glue across charts, and the native transport is metric-distorting *more*
than a matched-random map.

```
cross-chart metric mismatch = 0.292   (= random patchwork 0.283; atlas does nothing)
native-transport metric-compat error = 0.705  vs matched-random 0.550 (native is WORSE)
```

### Rung 3 — local curvature: REAL, positive, isotropic (verified, not artifact)

Scalar curvature of `g(q)`, computed via Christoffel symbols and the Riemann tensor:

```
R ≈ 0.098,  h-stable across h = 1e-3 … 3e-5 (identical to 4 digits)
flat control R = 0.0 exactly  (no numerical floor — the signal is real)
sphere control R = 30.0 stable (scheme validated on known curvature)
uniformly positive: 0% negative across |q| = 0.3 … 3.0
isotropic: R depends on radius |q|, not direction; grows outward (0.086 → 0.109)
```

### Rung 3-source — curvature is SOURCED by non-associativity

Sweeping the coupling `g`:

```
 g      native R    associative-null R
 0.00   0.0000      0.0000
 0.10   0.0312      0.0000
 0.17   0.0977      0.0000
 0.50   1.5796      0.0000
log-log slope R vs g = 2.36   (≈ g², leading order)
```

Curvature vanishes in the associative limit (`g=0`), the associative-kernel null is flat at
every `g`, and `R ~ g²`. The curvature is specifically a product of the **non-associative**
cross-term.

### Rung 2 — the connection is NON-METRIC, and this is the PRIMARY effect

The native transport's connection `Γ_native` departs from the metric's Levi-Civita connection
`Γ_LC`. The departure is the non-metricity `Q = ‖Γ_native − Γ_LC‖`:

```
 g      native Q    associative-null Q
 0.00   0.0000      0.0000
 0.10   0.4581      0.0000
 0.17   0.7858      0.0000
 0.50   3.0467      0.0000
log-log slope Q vs g = 1.10   (≈ g¹, LEADING order)
```

**Q ~ g¹ while R ~ g².** Non-metricity is *lower-order* than curvature — it is the **primary**
geometric effect. As the recombination coupling turns on, the first thing that happens (linear
in `g`) is that transport stops preserving the metric. Curvature (`g²`) is the second-order
consequence.

---

## What the model actually is

In causal order of what the non-associativity produces:

1. **Non-metricity (∝ g, leading).** The native transport does not preserve length. The
   connection is non-metric. This is the primary geometric signature of the recombination.
2. **Positive curvature (∝ g², secondary).** A uniformly positive, isotropic, radially-growing
   local curvature — the second-order shadow of the non-metricity.
3. **No globalization.** The local geometry does not glue into a manifold; it is irreducibly
   local.

This is the structure of **metric-affine / non-metric geometry** (Weyl-type connections,
non-metricity as a primary field), *not* Riemannian geometry. GR could never emerge here — not
by failure, but because GR is built on a metric-compatible (zero-non-metricity) connection, and
this model's leading geometric content is precisely the non-metricity GR sets to zero.

---

## Why this resolves the whole program

Every earlier negative is explained by this one structural fact:

| earlier result | explained by |
|---|---|
| holonomy not structure-specific | non-invertible non-metric transport, no global curvature |
| Pillar 2 compatibility closed-negative | no metric-compatible connection to source a curvature/current law |
| constraint algebra never closes | constraint algebra is a metric-compatible-geometry symmetry; this geometry is non-metric and local |

We spent the program testing for metric/Riemannian/GR structures. The model is non-metric and
local. The mismatch *was* the finding.

---

## Honest limits

- `g(q)` is the symmetric-Jacobian metric and `Γ_native` is read from the transport Jacobian's
  variation — both the natural choices, both flagged. The **vanishing at g=0 and the flat
  associative null are robust** to these choices, so "sourced by non-associativity" holds
  regardless; only the exact exponents could shift.
- Scaling laws (`R~g²`, `Q~g`) are **small-g leading behavior**; both steepen past g≈0.25
  (nonperturbative regime). `g=0.17` sits in the clean small-g window.
- All finite-sector (DIM=6 for curvature tractability; DIM=24 for metric/gluing).

---

## Next rung-step

Decompose the non-metricity tensor: **trace part (Weyl/dilation — uniform length rescaling,
a clean physical meaning) vs traceless part (richer non-metric structure).** That is exactly
how metric-affine geometry classifies a non-metric connection, and it would place this model
precisely in the non-metric-geometry landscape — identifying *which kind* of non-metric
geometry the it-from-bit recombination builds.

---

## Reproduction

```
python3 rung1_metric.py        # local metric: Riemannian (Rung 1)
python3 rung1_glue.py          # globalization fails; transport metric-distorting (Rung 1.5)
python3 rung3_verify.py        # curvature real, h-stable, flat/sphere controls (Rung 3)
python3 rung3_gsweep.py        # curvature sourced by non-associativity, R~g² (Rung 3-source)
python3 rung2_nonmetricity.py  # non-metricity Q~g, the PRIMARY effect (Rung 2)
```

Deterministic (seeded numpy).
