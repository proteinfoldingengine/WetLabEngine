# V823 Reproducibility Packet

## Claim tested

```text
G_proxy = 2α Δ log(A + ε)
A = exp(C - μ + η repair)
```

## What this packet reproduces

1. Builds synthetic recoverability fields:
   - `C` = surplus / recoverability capacity
   - `μ` = defect burden
   - `repair` = active repair field

2. Constructs accessibility:

```text
A = exp(C - μ + η repair)
```

3. Tests held-out curvature prediction:

```text
G_proxy ≈ k Δ log(A)
```

4. Perturbs A directly and verifies:

```text
δG = 2α Δδlog(A)
```

5. Runs adversarial/null comparisons.

## How to run

```bash
python v823_repro_accessibility_curvature.py
```

Outputs are written to:

```text
v823_results/
```

## Expected result

The exact numbers will vary slightly by environment, but the key pattern should hold:

```text
held-out accessibility curvature: strong
direct A perturbation: ~perfect
adversarial/null predictors: fail
```

## Claim boundary

Supported:

```text
The synthetic ordered-update model supports an accessibility-curvature law.
```

Not supported:

```text
Full tensor GR closure.
ADM momentum closure.
Physical spacetime GR.
```
