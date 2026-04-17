# Direct Calibration Runner

## Files
- `run_restricted_affine_calibration.py`
- `baseline_anchor.json`
- `screened_family_vectors.jsonl`

## Command
```bash
python run_restricted_affine_calibration.py   --baseline baseline_anchor.json   --screened screened_family_vectors.jsonl   --outdir calibration_output
```

## What it produces
- `anchor_constants.csv`
- `screened_family_calibration.csv`
- `affine_overlay.png`
- `remainder_vs_bound.png`

## Note
This runner uses any provided `M_theta` values from the screened JSONL file.
If you do not provide them, it defaults `M_theta = 0.0`, which is fine for a first pass but not a final curvature-calibrated run.

