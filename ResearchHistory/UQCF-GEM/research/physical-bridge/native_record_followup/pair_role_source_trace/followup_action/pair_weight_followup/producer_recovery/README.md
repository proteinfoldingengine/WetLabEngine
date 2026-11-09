# V1696 producer recovery: bounded archive result

Author: GPT Work. Date: 2026-11-09 UTC.
Research parent: `032bb78a6ccee44aa3e78d8ad59ebfcad687cd86`.
Status: original-byte source recovery, not a new scientific stage or independent mathematical review. Native receiver ownership/access remains **NOT_DERIVED**.

## Result

The original V1696.1, V1696.3 and V1696.9 ZIPs were recovered to look for the implementation generating pair-transport weights and support data. Each contains six CSVs, two JSONs and one Markdown report. None contains Python source or a notebook. In all three, `run_manifest.json` is byte-identical to the result summary: it supplies neither an executable procedure nor a producer-code reference.

| Archive | Members | Relevant preserved data | Producer operation recovered |
| --- | ---: | --- | --- |
| V1696.1 | 9 | 600 transport-weight audit rows, including coarse/fine cell IDs, pair index and orientation factor | No |
| V1696.3 | 9 | 210 class-audit rows, including fine-class counts and compatibility flags | No |
| V1696.9 | 9 | 180 operator-audit rows, including invariant length and nonzero-entry count | No |

The V1696.1 table is more specific than a summary: its exact numbers are now preserved with their archive identity. Its columns are `seed, ladder_step, coarse_cell, fine_cell, pair_index, weight, orientation_factor, drop_orientation`. They do not give a source-grade input, a function producing the weight, or a correspondence between a cell/pair and an owner-accessible effect. Recovering these output numbers does not recover their generating operation. No numerical fit or reconstructed producer is substituted for the missing original.

The V1696.0 definition already transcribed in `../transcripts/` supplies an aggregation formula with alpha weights described through support, orientation and product contribution. The archive contents inspected here do not fill in its missing grade-to-weight rule. The different meanings of transport weights, action weights and signature-comparison weights remain separated as in `../ASSESSMENT.md`.

This conclusion is limited to these three complete archives and that already recovered definition. It is not a claim that an implementation never existed or is absent from every source. V1696.3 has previously been discussed in source recovery; this packet provides its downloadable-byte inventory, not a claim that its historical verdict was newly discovered. V1696.9's Git blob identity also matches the pre-existing repository copy listed below.

## Research consequence

This bounded producer-recovery lead is exhausted by the available archive contents. Do not reopen the historical diagnostic simulations or attempt to infer a native law from the 600 weight rows. The historical verdicts remain unchanged.

The governing target remains `../../ACTION_BRIDGE_REENTRY.md`: an inherited operation relating the actual event to an effect available to the **same retained owner**. A source-side weight/current rule, even if later recovered, would still need that operational relation. Full report transport, a unique microscopic interaction and exact calibration of an entire state are not required: one independently owned fixed effect with unavoidable nonzero source contrast can suffice.

Re-entry on this archival lead requires a particular producer source, executable definition or original input/output specification. This packet supplies no new native premise and contains no proof to send for a new Gemini challenge. It does not close Path A or establish a universal impossibility result.

## Evidence and verification

`ARCHIVE_INSPECTION.json` records each original Library/file identity, original reported date and size, whole-archive SHA-256, Git blob identity, every member's size and SHA-256, all CSV headers and row counts, and the manifest/summary byte comparison. `originals/` preserves the unchanged ZIP bytes. CRC checks succeeded for all 27 members; all 18 CSVs parsed with consistent row widths, all six JSONs parsed, and all reports decoded as UTF-8. These checks concern archival integrity and structure, not the scientific validity or reproducibility of the reported experiments.

The V1696.9 archive has Git blob SHA `e078156eebbc6f85a892ef1887989f9061bbf34d`, matching the pre-existing copy at `Tmp/TOE/Einstein_12_V1698_valid_only_slow_atlas_closure_mp4_package/WorkProduct /V1696_9_intrinsic_d1d2_operator_invariant_test_package.zip`. The source identity in the inspection file refers to the Library bytes actually inspected.

To regenerate the inventory with Python's standard library:

```sh
python inspect_archives.py originals ARCHIVE_INSPECTION.json
```

The inspection script only reads ZIP members; it does not execute, import or extract their contents. No historical run, new numerical campaign, independent Gemini review, PR merge, or physical promotion is represented by this archival addition.
