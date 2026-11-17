# V725 saved-score AUC audit

Scope: rescore the saved V725 main dataset and compare the saved V737 main dataset. No scientific generators, new simulations, parameter scans, ablation replays, source modifications or native-bridge claims.

## V725 main result

|Score|Saved V725 formula|Exact-tie AUC|Unequal close pairs|
|---|---:|---:|---:|
|restoration_distance|0.99991319444444449|0.99991319444444449|0|
|adm_z|0.99991319444444449|0.99991319444444449|0|
|g_atrium_observable_only|0.99805555555555558|0.99805555555555558|0|
|g_atrium_with_k_oracle|0.9992361111111111|0.9992361111111111|0|
|passive_mean|0.50012152777777774|0.5|14|
|passive_curvature|0.50001736111111106|0.5|2|

There are 480 saved rows, exactly 240 labels of each class and 240 matched pair IDs. Every saved main-summary AUC is exactly reproduced by the original formula. The four active/oracle scores have no approximate-tie pairs at all. The implementation defect therefore does not explain their high main-dataset AUCs. Both passive controls have exactly matching class score multisets and exact-tie AUC 1/2.

V725 computes (W + C/2)/N where C counts NumPy isclose, while ordinary exact-tie Mann–Whitney scoring computes (W + T/2)/N. All inspected scores are finite; thus the upward difference is (C−T)/(2N). For passive_mean C−T=14, giving 14/115200; for passive_curvature C−T=2, giving 2/115200. Counts include both close wins (double-counted to 1.5) and close losses (given spurious 0.5 versus exact-tie scoring). NumPy uses the negative score as the reference in its asymmetric tolerance.

## V737 comparison

The bundle contains original main and gap metrics CSVs, results JSON and code. The bundled code matches PR151's immutable V737 source blob. Its scorer uses strict greater-than plus exact equality, so cases are disjoint. Main CSV: 840 rows, 420 matched pairs. Exact ranks give atrium_scalar = 169348/176400 = 0.9600226757369614; the archived mean-of-row-means reports 0.9600226757369613 (one final floating summation rounding difference). Restoration residual is 1, passive controls 1/2. This is not the same dynamics or metric as V725, and it does not numerically authenticate V725 ablations.

## Evidence and limitations

- Current Library-downloaded V725 source bytes exactly match frozen Git blob cf8a1bd5937acde59586b6d42ae8979742fd4e89; bundled V737 source bytes exactly match 8b4f50b515603d978f8b2ca6e31c875314541c40. This authenticates the present downloaded source against PR151, not historical runtime provenance.
- V725 main CSV SHA256: 7a34ae50a613d3899c6ca2ce46457d6c91f57a170141badf43f5019bc2559f5b
- V737 bundle SHA256: edbe49efad09130ec81b6f1a772405887a8388c074a74f1b5fbd5d75a88bab7c
- V737 main CSV SHA256: a5de3faac83acff2da4c87c10351d69102f2931972bf3f76a3b53bba74e3f2e7
- The V725 JSON also records ablations and scans, but this CSV contains only the 240-pair main dataset. Their saved score rows were not found in this item; those AUCs were not rescored. The archived output schema writes only main CSV plus summarized scan results.
- No earlier V725 variant or unrelated archive was substituted for the exact observable-only dataset.
- Fixed-data audit under NumPy 2.3.5; independent rank/bisection and scalar-tolerance counts agree. Original source/data are preserved unchanged.
- These are local audit findings, not yet independently Gemini-reviewed or published. Prior PR151 acceptance covers the static caveat, not this new fixed-data rescore.
