# V1688 Holonomy Proof Visualizer V4

Colab one-cell runnable proof visualization. Generates static PNG, GIF, and MP4.

## Core equations

```text
T_pq(dx) = dx + gamma_pq [roll(dx) ⊙ q − dx ⊙ roll(q)]
c_pq = <Z_q, T_pq Z_p> / (||T_pq Z_p|| ||Z_q||)
H_cycle^dir = Π_loop c_pq
native_directional_cycle_defect = |1 − H_cycle^dir| · mean(|C_corr|)
```

## Metrics

```json
{
  "source_mode": "loaded_uploaded_or_prior_proof_object",
  "H_cycle_dir": 0.0001932756421973766,
  "native_directional_cycle_defect": 0.5413093198510933,
  "mean_abs_C_corr": 0.5414139619822901,
  "reverse_H_cycle_dir": 0.0003622947565895673,
  "reverse_directional_cycle_defect": 0.5412178105427196,
  "orientation_asymmetry_abs": 9.150930837376059e-05,
  "edge_count": 8,
  "node_count": 8,
  "max_abs_continuity_residual": 0.12160044468422859,
  "interpretation": "Directed native holonomy is generated edge-by-edge by native recombination transport acting on retained correction mode Z over an explicit provenance cycle.",
  "gif_created": true,
  "mp4_created": true
}
```

## Boundary

The displayed curve is only a visualization of the discrete provenance cycle.
The proof object is the ordered edge product Π_loop c_pq.

This is a finite retained-flow proof object, not a GR/Einstein derivation.
