# V1701.15 — Post-Frame-Repair H-H Obstruction Decomposition

**Verdict:** `POST_FRAME_HH_OBSTRUCTION_DECOMPOSED`

## Purpose

V1701.14 showed that Ω_W scalar-frame repair made H-H meaningful but did not close it.

V1701.15 decomposes the true remaining obstruction:

```text
O_HH_new = [X_H_new(N), X_H_new(M)] - X_M(c)
```

and compares it against:

```text
O_HH_old = [X_H_old(N), X_H_old(M)] - X_M(c)
```

## Metrics

```json
{
  "version": "V1701.15",
  "dynamic_mean_old_total_norm": 2.7627251856205626,
  "dynamic_mean_new_total_norm": 2.3218979435427474,
  "dynamic_mean_improvement": 0.1636126717804455,
  "dynamic_mean_g_block_improvement": 0.33842826181360663,
  "dynamic_mean_K_block_improvement": -0.33178956710442653,
  "remaining_dominant_block": "new_K_block",
  "remaining_dominant_sector": "near2",
  "remaining_sector_means": {
    "diag": 0.06733788008020612,
    "symmetric": 0.07978173252992041,
    "antisymmetric": 0.9956819407382744,
    "offdiag": 0.9969423291703066,
    "local": 0.7527506625265507,
    "near2": 0.9999999999993314,
    "far": 0.0,
    "density_projection": 0.0028426156865730664
  },
  "diagnosis": "After \u03a9_W frame repair, the remaining H-H obstruction is dominated by new_K_block with strongest sector signature 'near2'. The repair reduced total obstruction by 0.164 but did not remove it.",
  "verdict": "POST_FRAME_HH_OBSTRUCTION_DECOMPOSED",
  "pillar_status": {
    "Pillar 1 - Global Atlas Closure": "COMPLETE",
    "Pillar 2 - Retained Curvature / Source-Current Compatibility": "NONTRIVIAL FINITE-SECTOR ACTION PASS",
    "Pillar 3 - GR / ADM Correspondence and Continuum Identification": "POST-FRAME HH OBSTRUCTION LOCALIZED; CLOSURE OPEN"
  }
}
```

## Diagnosis

After Ω_W frame repair, the remaining H-H obstruction is dominated by new_K_block with strongest sector signature 'near2'. The repair reduced total obstruction by 0.164 but did not remove it.

## Boundary

This does not close H-H.

It localizes the post-frame algebraic obstruction that remains after both scalar and momentum generators are Hamiltonian under Ω_W.
