# Rung 1 — The Model Builds Local Geometry That Does Not Globalize

**Frame:** it-from-bit / emergent-geometry, simulation-internal. Following the process, not GR.
**Method:** derive the metric from the model's own native kernel; test local reality, then global
gluing; gate every positive against a matched null.
**Companion proofs:** `rung1_metric.py`, `rung1_real.py`, `rung1_glue.py` (+ captured outputs).

---

## The rung ladder (why we are here)

Emergent GR is not one step above "a consistent geometry exists." It sits atop a ladder:
metric → metric-compatible connection → curvature (derived) → local covariance → dynamics →
constraint algebra. Earlier work leapt from atlas closure (a low rung) straight to the
constraint algebra (the top rung) and found it does not close. The correct move is to climb in
order. Rung 1 is the metric.

---

## What was tested and found

### Rung 1a — is there a local metric? **YES (real, Riemannian)**

The native recombination kernel `T(dx)=dx+g·(roll(dx)⊙q − dx⊙roll(q))` has a linearization
(Jacobian) at each state `q`. Its symmetric part defines a candidate metric `g(q)`.

```
positive-eigenvalue fraction = 1.000   (Riemannian, positive-definite)
eigenvalues spread ≈ 0.55 … 1.38       (anisotropic — real structure, not flat)
triangle-inequality violation rate = 0.000
```

So the model genuinely induces a **local Riemannian metric**: a real, non-degenerate,
anisotropic notion of distance in each chart. This is a real Rung-1 object.

### Rung 1b — does it glue into ONE global metric? **NO (and not atlas-specific)**

With each chart carrying its own local state, the metrics must agree on overlaps: the
transition map should carry `g_i` to `g_j`. It does not.

```
atlas-coupled cross-chart mismatch = 0.292
unrelated-states null mismatch     = 0.283
ratio null/atlas = 1.0
```

The mismatch is large, and identical to a random patchwork. The atlas transitions do **not**
carry the metric between charts — the local metrics do not glue into a global metric.

### Rung 1.5 — is the native transport metric-compatible? **NO — it is metric-DISTORTING beyond random**

The deeper question: the same native kernel that *builds* the metric — does its transport
*preserve* it? Test `g(p) =?= T_pq^T g(q) T_pq`, against a non-invertibility-matched random
transport.

```
native transport compatibility error  = 0.705
matched-random transport error         = 0.550
ratio random/native = 0.78   (native is WORSE than random)
```

The native transport does not merely fail to preserve the metric — it distorts it **more than
a generic random transport of the same non-invertibility would.** The connection that builds
the geometry actively fights its globalization.

---

## The finding

**The model builds local Riemannian geometry that is structurally non-globalizable.**

- Local distance exists everywhere (Rung 1a: real, positive-definite, anisotropic).
- Global distance exists nowhere (Rung 1b: metrics don't glue; Rung 1.5: native transport is
  metric-distorting beyond random).

This is not a missing operator or an accident of the atlas construction. It is a property of
the generating process: the non-associative recombination kernel produces local metrics and a
transport that resists stitching them together. The geometry is **irreducibly local**:
locally geometric, globally non-metric.

---

## Why this explains everything above it

Every higher-rung negative in the program is the downstream shadow of this one fact:

| higher-rung result | now explained by Rung 1 |
|---|---|
| holonomy downgraded (no structure-specific loop curvature) | no global metric for a loop to be curved in |
| Pillar 2 curvature/current compatibility closed-negative | no global metric-compatible connection to source it |
| constraint algebra does not close (scalar, source, atlas generators) | constraint algebra is a global-metric symmetry; there is no global metric |

We spent the program knocking down global objects one by one. Rung 1 removes them all at once
and says why: there is no global geometry to carry them. The geometry the process builds is
local.

---

## What this reframes the program to be about

The real object is not emergent GR (which needs a globalization the model does not perform).
It is the **local geometry plus the metric-distorting transport** — a process that makes
distance locally and refuses to make it globally. That is genuinely novel and sits near
non-associative / non-commutative geometry and discrete pre-geometry in the literature, where
locally-geometric-globally-non-metric structures are a recognized (and interesting) class.

---

## Honest limits and the next rung-step

- The metric is defined from the **symmetric part of the native Jacobian**; a different but
  still-derived metric (e.g. a different invariant of the kernel) could glue differently. The
  current choice is the most natural one and is flagged.
- "Irreducibly local" is established for this kernel and these transitions; it is a strong
  finding but a finite-sector one.

**Next (staying at the rung the model occupies):** characterize the **local curvature** of
`g(q)` — the Riemann/Ricci of the per-chart metric. Rung 3 done *locally* is now legitimate
because Rung 1 holds locally. The question: is the local geometry flat (so the distortion is
the only structure) or genuinely curved (the process makes real local curvature)? That is the
honest next step — following the simulation to the rung it actually occupies, not pushing it
toward GR.

---

## Reproduction

```
python3 rung1_metric.py   # local metric: Riemannian, anisotropic (Rung 1a)
python3 rung1_real.py     # cross-chart gluing fails, = random null (Rung 1b)
python3 rung1_glue.py     # native transport metric-distorting beyond random (Rung 1.5)
```

Deterministic (seeded numpy). DIM=24, 6 charts, ~30–120 seeds per test.
