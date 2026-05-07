# COLAB_HEAT_NORMALIZATION_THEOREM_CAMPAIGN.md

# Colab Heat Normalization Theorem Campaign

## Files

```text
Heat_Normalization_Theorem_Campaign.ipynb
colab_heat_normalization_theorem_campaign.py
```

## Purpose

Run the heavy spatial heat-normalization audit in Colab/T4.

This tests:

1. Local heat diagonal normalization:
   \[
   H_i(t)= [e^{-tL}]_{ii}(4\pi t)^{3/2}
   \approx A_i+B_it
   \]

2. Candidate curvature estimators:
   \[
   \widehat R_i = \mathrm{sign}\cdot B_i/dx^p
   \]

3. Global heat-trace zero-mode coefficient:
   \[
   C_{\mathrm{trace}} = \frac{\int R\,dV}{B_{\mathrm{trace}}}
   \]

## How to run

In Colab:

1. Upload or open `Heat_Normalization_Theorem_Campaign.ipynb`.
2. Runtime → Change runtime type → T4 GPU.
3. Run with:

```python
QUICK_MODE = True
```

4. If successful, change to:

```python
QUICK_MODE = False
```

and rerun.

## Send back

```text
HEAT NORMALIZATION CAMPAIGN SUMMARY
LOCAL_CANDIDATE_SUMMARY
TRACE_SUMMARY
TRACE_ROWS
GPU or CPU used
```

## Expected output files

```text
heat_normalization_campaign_local_rows.csv
heat_normalization_campaign_local_summary.csv
heat_normalization_campaign_trace_rows.csv
heat_normalization_campaign_summary.json
```

**End of file.**
