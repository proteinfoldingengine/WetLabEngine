# Atrium follow-up: saved-main AUC correction and source-byte match

Date: 2026-11-14 UTC. This additive integration updates the current interpretation of PR151 using the independently reviewed PR152 result. It introduces no new calculation campaign, native theorem, scientific generator run or review call. The original PR151 argument, source transcriptions and review record remain frozen unchanged.

## What the later evidence resolves

PR151 at `571c647615f9ea2e77ce4705febf5e1b497cbba9` identified the V725 comparator overlap but had not inspected saved score rows. Its section 6 therefore made no numerical-impact claim. [PR152](https://github.com/proteinfoldingengine/WetLabEngine/pull/152), frozen here at `c6ec5c2e2a3539cf51786b4b353b73d3abb5a898`, supplies the separately reviewed answer for the saved main datasets:

| V725 main score | Saved formula AUC | Ordinary exact-tie AUC | Unequal-close comparisons |
|---|---:|---:|---:|
| restoration_distance | 0.9999131944444445 | unchanged | 0 |
| adm_z | 0.9999131944444445 | unchanged | 0 |
| g_atrium_observable_only | 0.9980555555555556 | unchanged | 0 |
| g_atrium_with_k_oracle | 0.9992361111111111 | unchanged | 0 |
| passive_mean | 0.5001215277777777 | **0.5** | 14 |
| passive_curvature | 0.5000173611111111 | **0.5** | 2 |

There are 480 saved rows, 240 complete pairs and 57,600 cross-label comparisons per score. With W strict wins, T exact ties and C approximate ties, the original formula is `(W+C/2)/N`; ordinary exact-tie AUC is `(W+T/2)/N`. On these finite values the excess is `(C-T)/(2N)`. Unequal-close losses as well as wins contribute to that excess. Both passive score multisets match across classes, and both exact-tie AUCs are exactly one half.

The active/oracle scores contain no approximate ties. Consequently this comparator defect does not explain their high AUC on the saved main rows. This statement does not validate their calibration, dynamics, physical interpretation or owner/access assumptions. The historical report rounded both passive values to .500, so its rounded main active/passive pattern does not change.

V737's actual comparator uses disjoint strict-greater and exact-equality cases and reproduces its saved main summaries. Its atrium fraction is `42337/44100`; the actual mean-of-row-means result is `0.9600226757369613`, whereas direct rational-to-float conversion gives `0.9600226757369614`. This is the documented aggregation-rounding difference, not a scoring mismatch. V737 still uses different dynamics and a different metric; it is not an exact V725 replay.

## What the later source recovery authenticates

PR152 reports original source downloads and a byte-for-byte extraction of the V737 source from its original ZIP. Its source-identity ledger matches the following two PR151 transcription blobs:

| Code source | Matching Git blob |
|---|---|
| V725 observable-only program | `cf8a1bd5937acde59586b6d42ae8979742fd4e89` |
| V737 reproduction program | `8b4f50b515603d978f8b2ca6e31c875314541c40` |

This improves the provenance of those two code transcriptions to a match against the current downloaded source bytes. It does not authenticate historical execution, software environment, generation order or creation-chain provenance. PR152's original-download identity ledger does not include the V725 Markdown report; this note does not extend the code-byte authentication to that report.

## Review attribution and this integration's checks

PR152's new numerical result received one independent `gemini-3.1-pro-preview` ACCEPTED verdict in [run 43583237420](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/43583237420), attempt 1, finish STOP. The preserved answer contains seven substantive checks and four limitations, with empty findings, missing-assumptions and counterexample arrays. Its separate publication receipt is PASS. PR151's earlier review is not retroactively credited with this numerical result, and PR152's review does not cover this later integration note as a new reviewed argument.

For this integration I inspected the pinned PR152 argument, adjudication, source identities, exploratory results, complete raw model response, ordinary review, fixed-verification output, publication receipt and final-readback receipt. The ordinary review text exactly matches the response's sole candidate text. All six V725 W/T/C/N count sets agree between the exploratory result and fixed-verification output; both AUC formulas agree with those counts. These are evidence-consistency checks, not a new independent rescore of the original rows or a repeat of the artifact publication audit.

The PR152 final-readback receipt records 56 initial additions checked at `11622e92bf7127777c89ac822b91b8cc1639f73e`. Its PR description reports four subsequent archival additions checked separately at the pinned final head. The numerical claims here rest on the pinned reviewed evidence, not solely on a successful workflow status.

## Limits and disposition

Saved main rows only: no V725 scan/ablation correction and no V737 gap-data rescore is inferred. The historical programs, saved results and original PR151 scientific/review evidence are not repaired or rewritten. If other historical scores are later reused, their exact original row-level outputs must be recovered before extrapolating this correction.

Actual atemporal measurement/pruning occurrence remains **ACCEPTED INPUT**, including the explicit scope correction already recorded in PR151's adjudication. The remaining obligation is a source-backed event-to-operation identification, independently identified retained-owner action, and a fixed effect available to that same owner. The high synthetic AUCs and corrected passive controls do not supply those links. Native bridge: **NOT_DERIVED**. Native premises moved from SUPPLIED to DERIVED: **none**.

This incorporates the bot result and closes PR151's previously unquantified comparator question for these saved main rows. It does not request another Atrium parameter sweep, repeated review of unchanged material, new receiver label, merge, hold release or new native assignment.

## Immutable evidence

- [PR152 argument](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/ARGUMENT.md)
- [Source identities](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/SOURCE_IDENTITIES.json)
- [Fixed verification](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/evidence/43583237420/publication/fixed_verification.json)
- [Raw model response](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/evidence/43583237420/review/response.json)
- [Publication receipt](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/evidence/43583237420/publication/receipt.json)
- [Final-readback receipt](https://github.com/proteinfoldingengine/WetLabEngine/blob/c6ec5c2e2a3539cf51786b4b353b73d3abb5a898/ResearchHistory/UQCF-GEM/research/physical-bridge/saved_auc_audit/final_readback/receipt.json)
