# CONTINUUM_LIMIT_CLOSURE_STATUS.md

# Continuum Limit Closure Status
## Seam-by-seam audit of the affine GEM Bridge continuum-limit program

## Status
**Audit document. Not a proof.**

This file summarizes the current proof-chain status for the continuum-limit seam.

It does **not** claim that the GR continuum limit is closed.

Its purpose is to classify each seam as:

- **Closed**
- **Verifier-backed**
- **Conditional**
- **Open**
- **Failure-prone**

and to state exactly what evidence exists, what remains missing, and what public claim is supportable.

---

# 1. Current proof-chain

The current continuum-limit chain is:

```text
MICROSCOPIC_LAW.md
        ↓
OPERATOR_THEOREM.md
        ↓
CHI_FIXED_POINT.md
        ↓
MICRO_TO_BLOCK_ACTION.md
        ↓
DISCRETE_MEMORY_ACTION.md
        ↓
COEFFICIENT_DERIVATION.md
        ↓
COARSE_GRAINING_MAP.md
        ↓
EMERGENT_METRIC_MAP.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
        ↓
FIELD_EQUATION_VARIATION.md
        ↓
CONTINUUM_LIMIT.md
```

The chain is now substantially less vague than the original `CONTINUUM_LIMIT.md`, but it remains a derivation program rather than a completed proof.

---

# 2. Status key

## Closed
A seam is closed only if the mathematical object is explicitly derived from upstream assumptions, the derivation is not merely an ansatz, and no essential bridge step remains open.

## Verifier-backed
A seam is verifier-backed if an explicit candidate object exists and a runnable verifier supports structural consistency, but the object is not yet fully derived or uniquely forced.

## Conditional
A seam is conditional if the result follows only assuming another open seam, or if the proof is standard once a missing input is granted.

## Open
A seam is open if the key mathematical object is still only stated as a target and no verifier or derivation exists.

## Failure-prone
A seam is failure-prone if the existing verifier shows high sensitivity or the construction depends on a strong assumption likely to fail without deeper work.

---

# 3. Seam audit table

| Seam | File | Current status | Evidence | Main remaining gap |
|---|---|---:|---|---|
| Microscopic pruning law | `MICROSCOPIC_LAW.md` | Open / upstream | Assumed as source law | Needs final explicit law and invariant statement |
| Bridge operator form | `OPERATOR_THEOREM.md` | Conditional | Prior theorem-shaped affine bridge structure | Needs full closure from microscopic law |
| Bridge coefficient χ | `CHI_FIXED_POINT.md` | Verifier-backed | Fixed-point/loading reduction + sweep evidence | Still not first-principles microscopic uniqueness |
| Micro-to-block constants | `MICRO_TO_BLOCK_ACTION.md` | Verifier-backed candidate | `micro_to_block_action_verifier.py` | Constants not uniquely derived |
| Block memory action | `DISCRETE_MEMORY_ACTION.md` | Verifier-backed candidate | `discrete_memory_action_verifier.py` | Block action not proven unique or covariant |
| Continuum coefficients | `COEFFICIENT_DERIVATION.md` | Verifier-backed candidate | `continuum_limit_verifier_v2.py` | Scale constants remain open |
| Scalar coarse-graining | `COARSE_GRAINING_MAP.md` | Verifier-backed candidate | `coarse_graining_map_verifier.py` | Metric-compatible/covariant block map open |
| Local metric reconstruction | `EMERGENT_METRIC_MAP.md` | Verifier-backed candidate | `emergent_metric_map_verifier.py` | Riemannian/local only |
| Lorentzian signature | `LORENTZIAN_SIGNATURE_MAP.md` | Verifier-backed candidate | `lorentzian_signature_map_verifier.py` | Causal/time label not derived |
| Curvature estimation | `CURVATURE_ESTIMATION.md` | Failure-prone / verifier-backed toy | Controlled refinement test works; noisy sweep soft-fails | Full 4D Lorentzian curvature not implemented |
| Einstein-Hilbert action limit | `EINSTEIN_HILBERT_LIMIT.md` | Failure-prone / verifier-backed toy | Smooth 2D conformal convergence works | 4D Lorentzian EH / Regge convergence open |
| Field-equation variation | `FIELD_EQUATION_VARIATION.md` | Conditional / verifier-backed proxy | Stress-energy scaling verifier works | Full EH variation and exact Qν open |
| Full continuum GR limit | `CONTINUUM_LIMIT.md` | Not closed | Organized action + coefficients + verifiers | Requires all seams closed together |

---

# 4. Verifier results summary

## 4.1 Scalar-density weak-memory verifier

File:

```text
continuum_limit_verifier.py
```

Result:

```text
Weak-memory decoupling only:
PASS: 94.24%
HARD_FAIL: 5.76%

With stronger stationary-vacuum condition V'(0)=0:
SOFT_FAIL: 94.24%
HARD_FAIL: 5.76%
```

Interpretation:

- `V(0)=0` is the key weak-memory decoupling condition.
- `V'(0)=0` is stronger than required for GR decoupling.
- The scalar-density class is structurally viable but not microscopically derived.

Status:

```text
Verifier-backed candidate
```

---

## 4.2 CL-2 coefficient bridge verifier

File:

```text
continuum_limit_verifier_v2.py
```

Result:

```text
PASS: 99.191%
HARD_FAIL: 0.809%
```

Key symbolic checks:

```text
V(0)=0
V'(R_*)=0
V''(R_*)=mu_R^2(1-a)
```

Interpretation:

The coefficient bridge from seam-2 loading fixed point to scalar-density coefficients is structurally safe for stable loading parameters.

Status:

```text
Verifier-backed candidate
```

---

## 4.3 Discrete memory action verifier

File:

```text
discrete_memory_action_verifier.py
```

Result:

```text
PASS: 98.988%
SOFT_FAIL: 0.193%
HARD_FAIL: 0.819%
```

Interpretation:

The block action gives a structurally stable map:

```text
mu_R^2 = K_U / K_t
Z0 = (K_x / K_t)(dx/dt)^2
lambda0 = K_int / K_t
```

Status:

```text
Verifier-backed candidate
```

---

## 4.4 Micro-to-block action verifier

File:

```text
micro_to_block_action_verifier.py
```

Result:

```text
PASS: 96.479%
SOFT_FAIL: 0.197%
HARD_FAIL: 3.324%
```

Interpretation:

Plausible microscopic recursion parameters can produce positive block-action constants, but the map is not uniquely derived.

Status:

```text
Verifier-backed candidate
```

---

## 4.5 Coarse-graining map verifier

File:

```text
coarse_graining_map_verifier.py
```

Result:

```text
PASS: 99.48%
SOFT_FAIL: 0.01%
HARD_FAIL: 0.51%
```

Median scalar stability:

```text
Lambda_cv_median: 0.0817
R_eff_std_median: 0.0410
```

Interpretation:

The scalar identification `R_eff ~ Lambda` is structurally viable in sampled local regimes.

Status:

```text
Verifier-backed candidate
```

---

## 4.6 Emergent metric map verifier

File:

```text
emergent_metric_map_verifier.py
```

Result:

```text
PASS: 86.67%
HARD_FAIL: 13.33%
```

Median stability:

```text
valid_fraction_median: 0.9833
cond_median: 1.63
metric_variation_median: 0.628
```

Interpretation:

Positive geometry weights and adjacency can support a local nondegenerate metric estimate in a Riemannian/local setting.

Status:

```text
Verifier-backed candidate
```

Major limitation:

```text
Not Lorentzian.
```

---

## 4.7 Lorentzian signature verifier

File:

```text
lorentzian_signature_map_verifier.py
```

Result:

```text
PASS: 94.0%
HARD_FAIL: 6.0%
```

Median signature stability:

```text
valid_fraction_median: 1.0
signature_fraction_median: 1.0
cond_median: 1.56
metric_variation_median: 0.522
```

Interpretation:

If causal/time-orientation data is supplied, a local metric fit can structurally produce one negative and three positive eigenvalue directions.

Status:

```text
Verifier-backed candidate
```

Major limitation:

```text
The causal/time label is not derived.
```

---

## 4.8 Curvature estimation verifier

File:

```text
curvature_estimation_verifier.py
```

Refinement result:

```text
rel_rmse_n24: 0.0418
rel_rmse_n64: 0.0060
rel_rmse_n128: 0.0015
```

Sweep result:

```text
PASS: 14.67%
SOFT_FAIL: 85.33%
HARD_FAIL: 0.0%
```

Interpretation:

Curvature estimation works cleanly in smooth/refined settings but is highly sensitive to noise and under-resolution.

Status:

```text
Failure-prone / verifier-backed toy
```

Major limitation:

```text
Not full 4D Lorentzian curvature.
```

---

## 4.9 Einstein-Hilbert limit verifier

File:

```text
einstein_hilbert_limit_verifier.py
```

Refinement result:

```text
abs_rel_err_n24: 0.0418
abs_rel_err_n64: 0.0060
abs_rel_err_n128: 0.0015
abs_rel_err_n192: 0.00067
```

Sweep result:

```text
PASS: 32.0%
SOFT_FAIL: 68.0%
HARD_FAIL: 0.0%
```

Interpretation:

Discrete curvature-density action convergence works in smooth/refined settings, but action estimates are sensitive to noise and resolution.

Status:

```text
Failure-prone / verifier-backed toy
```

Major limitation:

```text
Not 4D Lorentzian Einstein-Hilbert convergence.
```

---

## 4.10 Field-equation variation verifier

File:

```text
field_equation_variation_verifier.py
```

Result:

```text
PASS: 95.1%
HARD_FAIL: 4.9%
```

Symbolic proxy:

```text
Tmem_general:
eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1) + v0

Tmem_with_V0_zero:
eta**2*(ZR*dr2/2 + r**2*v2/2) + eta*(Tmat*lam*r + r*v1)

Q_exchange_proxy:
eta*(Tmat*lam + divT*lam*r)
```

Interpretation:

The memory stress-energy decoupling and controlled exchange-current scaling are structurally safe when `V(0)=0` and coefficients are finite.

Status:

```text
Conditional / verifier-backed proxy
```

Major limitation:

```text
Does not prove full EH variation from the discrete action.
```

---

# 5. What is now legitimately supportable

The following public claim is supportable:

> The continuum-limit seam has been turned into a falsifiable, verifier-backed derivation program. The package now contains explicit candidate maps for memory coefficients, block action constants, scalar coarse-graining, local metric reconstruction, Lorentzian-signature fitting, curvature estimation, action convergence, and field-equation variation. These are not a completed derivation of GR, but they sharply reduce the open seams and make the failure conditions testable.

The following stronger claim is **not** supportable:

> The framework derives general relativity from first principles.

That is not yet true.

---

# 6. What remains open

## 6.1 Microscopic law closure
The chain still depends on an upstream microscopic pruning / retained-memory law.

Open target:

```text
microscopic law -> alpha_s, alpha_f, beta_s, beta_f, c_s, c_f, mu_G, I_s, I_f
```

## 6.2 Causal-order derivation
The Lorentzian-signature verifier assumes time-orientation / signed intervals.

Open target:

```text
microscopic update order -> tau_i or causal order
```

## 6.3 Full 4D curvature
Curvature is currently tested in a 2D conformal setting.

Open target:

```text
g_mu_nu^(i) -> R_mu_nu, R
```

in four-dimensional Lorentzian geometry.

## 6.4 Einstein-Hilbert convergence
The action-convergence verifier is a controlled 2D proxy.

Open target:

```text
sum_h A_h delta_h -> integral d^4x sqrt(-g) R
```

## 6.5 Matter operator
The memory coupling still contains:

```text
O_mat
```

Open target:

```text
O_mat = ?
```

## 6.6 Exchange current
The field-equation file contains schematic:

```text
Q_nu
```

Open target:

```text
Q_nu = explicit covariant expression
```

## 6.7 Newton constant normalization
The emergence or calibration of:

```text
G_N
```

is not derived.

---

# 7. High-risk seams

The highest-risk seams are:

1. **Causal-order derivation**
   - because Lorentzian signature currently assumes time data.

2. **4D curvature convergence**
   - because curvature estimation is noise-sensitive.

3. **Einstein-Hilbert action convergence**
   - because the current verifier is only a 2D conformal proxy.

4. **Microscopic origin of block constants**
   - because several coefficients remain candidate maps rather than forced outputs.

5. **Matter coupling and Q_nu**
   - because the exact matter operator is unspecified.

---

# 8. Recommended next work

The next file should be:

```text
CAUSAL_ORDER_DERIVATION.md
```

Purpose:

```text
microscopic update/pruning order -> causal order / time orientation
```

This is the most important next seam because it supports:

```text
Lorentzian signature -> 4D curvature -> Einstein-Hilbert limit
```

A second strong option is:

```text
MATTER_OPERATOR_AND_QNU.md
```

Purpose:

```text
O_mat -> T_mem,int -> Q_nu
```

But the causal-order seam is more fundamental.

---

# 9. Bottom-line status

## What has improved

The original continuum-limit file asked:

> can the bridge framework recover a controlled GR continuum limit?

The current package now decomposes that question into explicit, testable seams:

1. coefficient bridge,
2. block action,
3. micro-to-block constants,
4. scalar coarse-graining,
5. local metric reconstruction,
6. Lorentzian signature,
7. curvature estimation,
8. action convergence,
9. field-equation variation.

Each seam now has either:
- a candidate derivation,
- a verifier,
- a failure mode,
- or all three.

## What has not been proven

The package still does not prove:

```text
S_disc -> S_EH + S_mat + S_mem
```

from first principles.

It also does not prove:

```text
G_mu_nu = 8pi(T_mat + T_mem)
```

as a fully derived microscopic consequence.

## Honest final status

> Seam 3 is now theorem-shaped, verifier-backed, and sharply decomposed. It is not closed. The next decisive bottleneck is deriving causal/time order from the microscopic law.

**End of file.**
