# C3++ retained-information state starter pack

## Files
- `c3_retained_information_state_experiment_plan.md`
- `c3_retained_information_state_analysis.py`
- `c3_retained_information_state_sample_telemetry.csv`

## Purpose
This sample CSV shows the expected schema for the retained-information-state experiment.

## Run
Example command:

```bash
python c3_retained_information_state_analysis.py \
  --input c3_retained_information_state_sample_telemetry.csv \
  --target fail_within_32 \
  --outdir c3_retained_state_results
```

## Expected result
The script will compare:
- `G_t` only
- `G_t + R_t`

and output:
- `predictor_comparison.csv`
- `matched_pair_analysis.csv`
- `matched_pair_summary.csv` (if enough pairs are found)

## Replace with real data
Swap the sample CSV for a real C3++ export that includes the same columns.
