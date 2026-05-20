# Accessibility Curvature Law in Ordered-Update Recoverability Simulations
## Emergent Conformal Geometry from Reachable-State Density

**Author:** Aaron Spradlin  
**Program:** Recoverability Geometry / Accessibility Branch  
**Version:** V824  
**Date:** 2026-05-20

---

## Abstract

This work investigates whether ordered-update recoverability systems naturally generate geometry-like structure analogous to curvature dynamics.

The strongest validated result is an accessibility-curvature law:

```text
G_proxy = 2α Δ log(A + ε)
```

with:

```text
A = exp(C - μ + η repair)
```

where:

- `A` = reachable-state accessibility density,
- `C` = recoverability surplus / capacity,
- `μ` = defect burden,
- `repair` = active repair field,
- `η` = repair conversion efficiency.

Interpretation:

```text
Spatial compression of reachable-state accessibility generates curvature-like conformal structure.
```

This result survived held-out validation, operator compression, direct perturbation testing, and adversarial/null testing. The work does not currently support full tensor Einstein closure, ADM momentum closure, or physical spacetime GR claims.

---

## 1. Introduction

The central question of this program is:

```text
Can recoverability pressure naturally generate geometry-like structure?
```

The initial target was broad Einstein-style closure:

```text
recoverability → curvature → tensor geometry
```

The work evolved into a more precise scientific program:

1. identify stable emergent geometric operators,
2. determine which branches survive pruning,
3. separate stable laws from failed closures,
4. identify the irreducible surviving structure.

The result was unexpected. The strongest branch was not tensor transport geometry. It was accessibility geometry.

---

## 2. Ordered-Update Recoverability Framework

The simulation framework models systems under defect accumulation, repair pressure, recoverability surplus, and ordered update dynamics.

| Symbol | Meaning |
|---|---|
| `μ(x,τ)` | defect burden |
| `repair(x,τ)` | repair field |
| `C(x,τ)` | recoverability surplus/capacity |
| `A(x,τ)` | reachable-state accessibility density |

The update ordering parameter `τ` is not assumed to represent physical time. It represents ordered recoverability updates.

---

## 3. Emergent Conformal Geometry

Define:

```text
Ω = exp(φ)
g_eff = Ω² g0
```

A scalar curvature proxy emerged:

```text
G_proxy = -2Δφ
```

This branch repeatedly survived held-out testing, pruning, operator compression, and geometry reinterpretation.

---

## 4. Tensor Branch Failure

The tensor branch was extensively explored. Attempted closures included:

- hand-built stress tensors,
- action-style stress tensors,
- source-coupled lapse and shift terms,
- shear/flow transport,
- continuity currents,
- Poisson-like shift solves,
- Noether-like scalar currents,
- compact transport currents,
- hidden reservoir terms.

The outcome was consistent:

```text
partial transport prediction: yes
closed conserved current: no
ADM momentum closure: failed
```

This became a scientifically important negative result.

---

## 5. Accessibility Geometry Interpretation

The system was not behaving like:

```text
local conserved momentum transport
```

Instead, it behaved like:

```text
reachable-state accessibility geometry
```

The primitive object became:

```text
A(x,τ) = reachable-state accessibility density
```

rather than:

```text
J_i = conserved momentum current
```

---

## 6. Accessibility Field

The accessibility field emerged as:

```text
A = exp(C - μ + η repair)
```

which compresses to:

```text
log A = C - μ + η repair
```

Interpretation:

| Term | Meaning |
|---|---|
| `C` | surplus / recoverability capacity |
| `μ` | defect suppression |
| `η repair` | repair accessibility restoration |

---

## 7. Accessibility Potential

The geometry responds through a logarithmic potential:

```text
φ = -α log(A + ε)
```

Substituting into the curvature proxy:

```text
G_proxy = -2Δφ
```

yields:

```text
G_proxy = 2α Δ log(A + ε)
```

This became the irreducible surviving law.

---

## 8. Accessibility Curvature Law

### Core Law

```text
G_proxy = 2α Δ log(A + ε)
```

Equivalent compressed form:

```text
G_proxy ∝ Δ(C - μ + η repair)
```

Interpretation:

```text
Curvature-like response is governed by spatial compression / expansion of reachable-state density.
```

---

## 9. Validation Campaign

### 9.1 Held-Out Accessibility Validation

Explicit accessibility fields predicted curvature strongly:

```text
mean held-out R² ≈ 0.879
min held-out R²  ≈ 0.860
mean correlation ≈ 0.938
```

### 9.2 Constraint Compression

Compressed operator form:

```text
G_proxy ∝ Δ(C - μ + η repair)
```

Validation:

```text
mean held-out R² ≈ 0.917
min held-out R²  ≈ 0.865
mean correlation ≈ 0.958
```

### 9.3 Direct Accessibility Perturbation

Accessibility was perturbed directly:

```text
A₂ = A · exp(δq)
δG = 2α Δδlog(A)
```

Result:

```text
mean δG R² = 1.000
min δG R²  = 1.000
```

### 9.4 Adversarial / Null Testing

Competing predictors were tested:

- zero predictor,
- wrong-sign predictor,
- shuffled predictor,
- unrelated Laplacian,
- zero-order perturbation.

Results:

```text
correct Δlog(A) predictor: R² = 1.000
next-best null: R² ≈ 0
```

This ruled out generic perturbation artifacts.

---

## 10. Why the Laplacian Appears

The Laplacian is the minimal local operator that measures spatial compression and expansion structure. A zero-order term measures amount. A first derivative measures direction. A second derivative measures local bending, spreading, or compression.

Therefore:

```text
Δ log(A)
```

is the minimal local accessibility-compression operator.

---

## 11. Why Log Accessibility Appears

Accessibility combines multiplicatively across recoverable future options. The logarithm converts multiplicative accessibility into additive potential:

```text
log A = C - μ + η repair
```

This makes the recoverability balance additive and allows the curvature operator to act on an additive scalar potential.

---

## 12. Why Scalar Closure Worked

The accessibility field is scalar. The Hamiltonian constraint is scalar. Therefore scalar closure is natural:

```text
curvature density ↔ accessibility compression
```

---

## 13. Why Momentum Closure Failed

Momentum closure assumes local conserved vector transport:

```text
J_i
```

The accessibility field behaved more like a constraint/state function than a locally conserved transport field. This explains the repeated failure of ADM momentum closure and conserved current attempts.

---

## 14. Minimal Theorem-Shape Statement

### Assumptions

1. The system has a positive reachable-state density:

```text
A(x,τ) > 0
```

2. Geometry responds through a logarithmic potential:

```text
φ = -α log(A + ε)
```

3. The scalar curvature proxy is:

```text
G_proxy = -2Δφ
```

### Result

```text
G_proxy = 2α Δ log(A + ε)
```

### Interpretation

```text
Spatial accessibility compression generates curvature-like conformal response.
```

---

## 15. Current Scientific Status

### Strongly Supported

```text
1. Ω / conformal geometry
2. scalar curvature closure
3. accessibility-density interpretation
4. compressed Laplacian law
5. direct perturbation response
6. adversarial/null specificity
7. Hamiltonian-like scalar closure
```

### Not Yet Supported

```text
1. full tensor Einstein closure
2. ADM momentum constraints
3. conserved vector current
4. physical spacetime interpretation
5. local PDE evolution law for A
```

---

## 16. Strongest Current Claim

```text
The ordered-update recoverability simulations support an accessibility-curvature law:

G_proxy = 2α Δ log(A + ε)

where curvature-like scalar response is governed by the Laplacian of reachable-state accessibility density.
```

---

## 17. Claim Boundary

Supported:

```text
The simulation supports an accessibility-curvature scalar/conformal law.
```

Not supported:

```text
Full tensor Einstein equations are closed.
ADM momentum constraints are solved.
Physical spacetime GR is proven.
```

---

## 18. Reproducibility

The accompanying Python proof script reproduces:

1. construction of synthetic recoverability fields,
2. accessibility field definition,
3. held-out curvature prediction,
4. direct accessibility perturbation,
5. adversarial/null failure of competing predictors.

Core implementation:

```text
A = exp(C - μ + η repair)
G_proxy = 2α Δ log(A + ε)
```

---

## 19. Future Directions

### Variational Derivation

Derive:

```text
φ = -α log(A)
```

from a variational principle.

### External Applications

Potential systems:

- battery recoverability,
- network resilience,
- AI stability landscapes,
- repairable infrastructure,
- routing under failure.

### Optional Tensor Branch

Only if desired:

```text
full 3D tensor reconstruction
```

The tensor branch should not be forced unless a true conserved vector primitive or full 3D geometry is introduced.

---

## 20. Conclusion

The program did not derive full tensor GR.

However, it produced a strong accessibility-curvature law:

```text
G_proxy = 2α Δ log(A + ε)
```

with:

```text
A = exp(C - μ + η repair)
```

The evidence supports the interpretation:

```text
Recoverability pressure creates reachable-state density.
Spatial compression of log accessibility generates curvature-like scalar structure.
```

This is currently the strongest validated result of the recoverability geometry program.
