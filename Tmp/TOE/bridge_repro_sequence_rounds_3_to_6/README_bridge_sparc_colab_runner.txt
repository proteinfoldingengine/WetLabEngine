
# Bridge SPARC Colab Runner

## Quick start in Colab

Upload `bridge_sparc_colab_runner.py` and run:

```python
!python bridge_sparc_colab_runner.py
```

It will:

1. `wget` the official SPARC Newtonian mass-model archive:
   - `https://astroweb.case.edu/SPARC/Rotmod_LTG.zip`
2. unzip it
3. run the shared Bridge family across all `*_rotmod.dat` files
4. write outputs into:
   - `bridge_sparc_full_sample_results/`

## Main outputs

- `sparc_full_sample_summary.csv`
- `sparc_full_sample_aggregate.csv`
- `top20_rmse_improvement.csv`
- `bottom20_rmse_improvement.csv`
- `rmse_improvement_histogram.png`

## Current shared Bridge family

- beta = 1.1
- L = 3.5 kpc
- gamma_curv = 1.0
- eta_signed = 0.35
- zeta_disk = 0.5

## Notes

This is a pressure-test scaffold.
It does not claim a solved physical theory.
It tests whether one shared retained-memory response family can improve the baryonic baseline across the public SPARC mass-model sample.
