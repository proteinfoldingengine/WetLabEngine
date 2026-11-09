# Phase 57.3D6 — ARC-1 Admissibility / Repair Compatibility Law

## Verdict

`ARC1_MINIMAL_SOURCE_CURRENT_COMPATIBILITY_PROJECTION_CLOSED__PREQUENTIAL_OPERATOR_RETEST_OPEN`

## Diagnosis

`ARC1_DERIVES_REPAIR_AS_MINIMAL_ADDED_ACCESSIBLE_CAPACITY_REQUIRED_FOR_BOUNDED_SOURCE_CURRENT_FEASIBILITY`

## Why ARC-1 was needed

ROC-1P failed because unrepaired ROC-1 can make the finite-capacity source-current problem infeasible:

```text
d f = b
|f_e| <= c_eff_e
```

The measure-twice audit showed retained accessibility collapse, not numerical noise.

## ARC-1 law

Given the ROC-1 multiplier:

```text
m0 = exp(-r_n)
```

ARC-1 defines the repaired multiplier by constrained projection:

```text
m_arc = argmin_m Σ_e c_e (m_e - m0_e)
```

subject to:

```text
exists f:
  d f = b
  |f_e| <= c_e m_e

m0_e <= m_e <= 1
```

Equivalently, with repair variable:

```text
u_e = m_e - m0_e >= 0
```

ARC-1 solves:

```text
minimize Σ_e c_e u_e

subject to:
  d f = b
  |f_e| <= c_e(m0_e+u_e)
  0 <= u_e <= 1-m0_e
```

## What this means

Repair is not a free healing knob.

It is the least accessibility restoration forced by source-current compatibility.

If the ROC-1 state is already feasible, repair is zero.

## Test result

```text
normal slices:
  64

normal slices infeasible before ARC-1 by local source-cut check:
  60

normal slices infeasible after ARC-1 by local source-cut check:
  0

max divergence residual after ARC-1:
  3.735601e-16

max capacity violation after ARC-1:
  1.387779e-17

median repair cost / full reset cost:
  0.055282

median repaired edge fraction:
  0.090000

high-capacity median repair cost:
  0.000000e+00
```

## What is closed

```text
ARC-1:
  minimal source-current compatibility projection
```

## What remains open

```text
ARC-1P / ROC-1P rerun with ARC-1:
  open

simulation proto-gravity:
  open

ADM / Einstein:
  open
```

## Next

Rerun the prequential retained-operator challenge with ARC-1 projection included.

The new predictor must use:

```text
m_arc
a_eff = m_arc ⊙ a
c_eff = m_arc ⊙ c
```

computed before future target scoring.
