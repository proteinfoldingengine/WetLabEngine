# P1 authoritative measurement archive

This directory mirrors the acceptance-grade outputs from GitHub Actions run `35288146185` on exact measurement head:

`f38cce040c98b78f4300ace06f28c350e4e4c313`

The run artifact was:

- artifact ID: `10525307040`
- name: `protein-p1-authoritative-measurement`
- archive SHA-256: `424a11c975ec7c7d662d027294f3034a5d42d93e2c2b8d17e416f4373d54a9d2`

The scientific decision is:

```text
NO_GO_HIERARCHICAL_ADVANTAGE
```

## Files mirrored here

- `p1_acceptance.json`
- `p1_run_manifest.json`
- `p1_primary_comparisons.csv`
- `p1_results.csv`
- `p1_summary.csv`
- `SHA256SUMS.txt`

`SHA256SUMS.txt` is copied from the workflow artifact and contains the hashes of the **original artifact bytes**.

The Python CSV writer emitted CRLF line endings in the workflow artifact. The GitHub text mirrors are stored with LF line endings. Therefore the CSV mirror byte hashes differ even though their parsed values are identical.

`MIRROR_SHA256SUMS.txt` records the LF-normalized repository mirror hashes. JSON hashes are unchanged because those files were already LF text.

The full trajectory table `p1_traces.csv` remains part of the authoritative workflow artifact and has original SHA-256:

`e069ad0bfae3a926df672b8c26ee906f1820db209b2f076a269e6be962a7ff44`

The trace table is not needed to recompute the frozen acceptance decision; `p1_results.csv` contains every matched target/seed/mode primary endpoint and secondary endpoint used by P1.

## Independent verification

After downloading the artifact, the acceptance logic was recomputed independently from `p1_results.csv`, including all 4096 sign assignments for each 12-pair exact test and the two-comparison Holm correction.

That independent calculation reproduced the runner's:

- pooled means;
- target-wise deltas;
- exact p-values;
- Holm-adjusted p-values;
- seven acceptance predicates;
- final NO-GO decision.

See `../P1_RESULT.md` for the scientific adjudication and bounded interpretation.
