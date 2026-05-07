# Spectral-Content Normalization Analysis

This is the next step after the multi-geometry campaign.

## Why

The multi-geometry run showed:

```text
per-geometry q ≈ 2
per-geometry errors small
universal constant fails
```

So the next theorem target is:

```text
C_delta(dx, f) ≈ -F(f) dx²
```

not:

```text
C_delta(dx) ≈ -C0 dx²
```

## What this script does

It post-processes:

```text
multi_geometry_trace_dx_scaling_campaign_raw_rows.csv
```

and computes descriptors for each conformal field:

```text
E0 = <f²>
E1 = <|grad f|²>
E2 = <(Delta f)²>
k_eff² = E2/E1
IPR / participation
gradient anisotropy
```

Then it ranks simple candidate laws for the geometry factor F(f).

## Send back

```text
SPECTRAL CONTENT NORMALIZATION SUMMARY
MODEL_RANKINGS
BEST_MODEL_BY_GEOMETRY
LEAVE_ONE_GEOMETRY_OUT
```

**End of file.**
