# V771 Peer Review Packet / Falsification Checklist

## One-line claim

```text
A compact recoverability-source law generates stable GR-like conformal/curvature structure across ordered recoverability updates.
```

## Guardrail

```text
Simulation index t is not physical time.
Ordering is primitive.
```

All claims are over ordered recoverability updates, not physical spacetime time.

## What is claimed

```text
1. Ω-based Atrium geometry exists operationally.
2. G_proxy = -2Δφ is Laplacian-dominant.
3. R_conf = exp(-2φ)G_proxy is conformal-weighted.
4. Dual-branch source closure is stable under geometry variation and scaling.
5. Lower-order source classes fail for G-side.
6. Conformal weighting is necessary for R-side.
```

## What is not claimed

```text
physical GR
physical spacetime curvature
physical time
Einstein equations in nature
coordinate-covariant tensor theory
coefficient-free theorem
formal continuum proof
```

## Frozen laws

### G-side

```text
log_mu
lap_repair
lap_C
repair_phi
```

Necessary core:

```text
lap_repair
lap_C
```

### R-side

```text
log_mu
lap_repair
lap_C
repair_phi
exp_phi_lap_C
exp_phi_lap_repair
grad_phi_energy
phi_lap_C
C_grad_phi
boundary_proxy
```

## Key evidence

### Structural closure

V759.1:

```text
mean G R² ≈ 0.996
min G R²  ≈ 0.991

mean R R² ≈ 1.000
min R R²  ≈ 0.999
```

### G-side falsification

V765:

```text
zero-order R² ≈ 0.241
first-derivative R² ≈ 0.514
lap repair/surplus R² ≈ 0.993
```

### R-side conformal necessity

V766:

```text
unweighted G_proxy → R_conf R² ≈ -0.188
conformal-weighted G R² ≈ 1.000
```

### Coefficients

V769:

```text
G-side coefficient scaling partially collapses under dx/Laplacian normalization.
R-side remains stable but not coefficient-free.
```

## Falsification checklist

The result should be considered weakened or failed if any of the following occur:

```text
1. Dual-branch closure fails on independent geometries.
2. Closure only works under one arbitrary update-order schedule.
3. Zero-order or first-derivative source classes close G_proxy as well as Laplacian classes.
4. R_conf closes without conformal weighting.
5. Coefficients fail to transfer after intrinsic normalization.
6. Grid refinement drives R² toward chance.
7. A simpler non-recoverability source explains the same closure.
8. The Ω field depends on hidden k/oracle labels.
9. The result requires interpreting simulation index as physical time.
```

## Reviewer questions

```text
1. Are the source terms genuinely observable-only?
2. Are there hidden labels, k, or oracle capacity terms?
3. Does closure survive held-out geometries?
4. Does closure survive ordered-update reparameterization?
5. Are G_proxy and R_conf properly distinguished?
6. Is the R-side conformal factor inserted or derived from Ω?
7. Does the proof rely on physical-time assumptions?
8. Can lower-order source classes falsify the Laplacian necessity claim?
9. Are coefficients universal, normalized, or empirical?
10. What would count as a failed replication?
```

## Recommended replication order

```text
1. Reproduce Ω extraction.
2. Reproduce V747.1 order audit.
3. Reproduce V753 minimal source pruning.
4. Reproduce V755 coefficient transfer.
5. Reproduce V759.1 dual-branch scaling.
6. Reproduce V765 lower-order falsification.
7. Reproduce V766 conformal correction test.
8. Reproduce V769 coefficient-collapse audit.
```

## Final reviewer-facing status

```text
Step 4 structural closure: supported
Theorem: incomplete
Physical GR: not claimed
Best next research step: coefficient-free variational/action derivation
```
