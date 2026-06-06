# V1664 — BPIC 2013 Alternative Branch Mapping Audit

## Status

```text
prepared_and_preview_audited
```

## Purpose

Test whether the V1662 empirical candidate signal survives alternative branch definitions.

## Full Normalized Baseline

```json
{
  "candidate_count": 173,
  "mean_delta": 0.10684879346729056,
  "max_delta": 0.5,
  "count_delta_gt_0_025": 165,
  "count_delta_gt_0_05": 126,
  "count_delta_gt_0_10": 66,
  "mapping": "v1662_branch_id_baseline_full_normalized",
  "row_count": 65533,
  "trace_count": 7554,
  "data_scope": "full_normalized_csv"
}
```

## Raw Preview Branch Columns Detected

```json
[
  "org:group",
  "resource country",
  "organization country",
  "org:resource",
  "organization involved",
  "org:role",
  "product"
]
```

## Limitation

The uploaded raw event file is a preview subset, not necessarily the full XES-derived event table.

Therefore this package includes a full Colab runner:

```text
v1664_bpic2013_alternative_branch_mapping_colab.py
```

It re-downloads/re-parses the XES file and tests branch mappings:

```text
org:group
org:resource
org:role
organization involved
product
impact
activity bucket
```

## Boundary

This does not close L3.
This does not prove empirical geometry.
This does not claim physical geometry, GR, ADM, or Einstein equations.
