# v15.45 Scientific Visualization

This directory provides a presentation layer for the exact published v15.45 scalar operator

`A = (I+X)(I+Y) Delta / 8`

on the periodic-square formula domain.

The plotting code reconstructs the operator using exact rational arithmetic, verifies the certified rank/nullity and exact kernel basis before rendering, and only then converts to floating point for eigendecomposition and graphics.

## Scientific representation

- The mathematical domain is the periodic square `Z_L x Z_L`.
- The 3D torus is a **visualization embedding only**; it is not an inferred physical geometry.
- Normal surface displacement is a **visual encoding of scalar amplitude only**.
- The animated field is the largest-absolute-eigenvalue eigenmode of the finite operator; it is not labeled as a source-selected physical response.
- Nullity/kernel statements are exact rational checks, not floating threshold classifications.
- L=6 and L=8 are formula-extension controls.
- Finite conditioning is reported only on the nonzero/centered spectral sector for odd L.

Run:

```bash
python visualize_v1545.py
```

The script writes PNG figures, MP4 animations when ffmpeg is available (GIF fallback), and `artifacts/verification.json`.

This visualization is intended to accurately communicate the mathematical foundation established in v15.45 while keeping visual embedding choices distinct from the certified operator.
