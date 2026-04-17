# Restricted Affine Coupling Calibration Data Contract
## Minimal inputs needed to run the calibration scaffold

## Purpose
This document defines the exact input structure needed to execute the calibration phase without ambiguity.

Use this contract to assemble one baseline example plus a screened family of corrected points.

---

## 1. Minimal required objects

The calibration scaffold needs:

### A. One fixed baseline
For a single baseline instance:
- `q` : latent target probability vector
- `p_b` : baseline score vector

### B. One reference corrected point
For one screened reference point:
- `p_c_ref` : corrected score vector at the chosen reference setting
- reference parameters: `alpha_0`, `beta_0`, `nu_0`

### C. Screened family of corrected points
For each screened point \(\theta\):
- label
- `q`
- `p_b`
- `p_c`
- optional metadata: `alpha`, `beta`, `nu`

---

## 2. Shape requirements

For every point:
- `q`, `p_b`, and `p_c` must all have the same length
- all vectors must refer to the same sample ordering
- values should be numeric
- no missing values

---

## 3. File-level recommendation

Recommended organization:

### `baseline_anchor.json`
Contains:
- `label`
- `q`
- `p_b`
- `p_c_ref`
- `alpha_0`
- `beta_0`
- `nu_0`

### `screened_family.csv`
One row per screened parameter point with columns:
- `label`
- `alpha`
- `beta`
- `nu`
- `q_path`
- `p_b_path`
- `p_c_path`

### vector files
For each point, store vectors in simple CSV or NPY files.

---

## 4. Simplest working option

If you do not want multiple files yet, the simplest usable structure is:

### `baseline_anchor.json`
with embedded arrays for:
- `q`
- `p_b`
- `p_c_ref`

and

### `screened_family_vectors.jsonl`
one JSON object per screened point containing:
- `label`
- `alpha`
- `beta`
- `nu`
- `q`
- `p_b`
- `p_c`

This is the easiest route for the first pass.

---

## 5. Notes on consistency

- `q` and `p_b` should be identical across the screened family if the baseline is truly fixed
- if they differ across points, document why
- the calibration logic assumes a fixed baseline family unless explicitly modified

---

## 6. Required outputs after calibration

The calibration run should produce:

- anchor constants table: \(C_0, V_0, \lambda_0, a_0, b_0\)
- empirical cloud: \((\Delta \mathrm{Var}, \Delta \mathrm{Cov})\)
- control diagnostics: \(|\lambda_\theta-\lambda_0|, M_\theta, \eta_{\nu,\theta}|\)
- observed remainder \(\epsilon_\theta\)
- theorem-bound comparison

---

## 7. Immediate next action

The next concrete step is:

1. build `baseline_anchor.json`
2. build `screened_family.csv` or `screened_family_vectors.jsonl`
3. load into the calibration scaffold
4. run the anchor computation

