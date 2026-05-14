# V498 Run Results

## Summary table

| family           |   n_nodes |   n_edges |   source_reserve_to_metric_R2 |   metric_to_curvature_R2 |   defect_localization_AUC |   leakage_path_AUC |   repair_path_AUC |   mean_C |   mean_C_surplus |   mean_eta_convert |
|:-----------------|----------:|----------:|------------------------------:|-------------------------:|--------------------------:|-------------------:|------------------:|---------:|-----------------:|-------------------:|
| lattice          |       169 |       312 |                      0.876377 |                 0.816349 |                  1        |           0.999299 |          0.996026 | 0.578413 |         0.436066 |          0.296933  |
| random_geometric |       180 |      1198 |                      0.75377  |                 0.479802 |                  0.999588 |           0.992785 |          0.991342 | 0.555338 |         0.448911 |          0.249502  |
| scale_free       |       180 |       531 |                      0.951965 |                 0.919741 |                  1        |           0.969903 |          0.989074 | 0.255663 |         0.120633 |          0.0630685 |
| small_world      |       180 |       540 |                      0.921192 |                 0.877872 |                  1        |           0.998763 |          0.996289 | 0.402387 |         0.265113 |          0.190066  |
| tree_with_loops  |       180 |       224 |                      0.971191 |                 0.939089 |                  1        |           0.95403  |          0.996083 | 0.26604  |         0.137781 |          0.0721989 |
| fragmented       |       180 |       480 |                      0.862955 |                 0.728294 |                  1        |           0.999588 |          0.998969 | 0.409113 |         0.304373 |          0.144143  |


## Main generated plots

- `v498_summary_bars.png`

- `aggregate_source_ratio_metric.png`

- `aggregate_metric_curvature.png`

- `geometry_<family>.png`

- `source_ratio_metric_<family>.png`

- `curvature_consistency_<family>.png`

- `defect_law_<family>.png`
