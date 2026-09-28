# UQCF-GEM 16.12 — final loop report

Completed 2026-09-28. **CONTINUOUS_SIGNED_NORMAL_RESPONSE_CERTIFIED.** The targeted GitHub audit passed all five new tests, six parent tests, and all scientific validity controls. Complete results and execution evidence are published with the [full report](demos/v15.56-response-selector-obstruction/continuous-response/RESULTS.md).

The signed source response survives when singular-value magnitude is retained. Across all 144 frozen physical families, the sixth-edge connected matrix approaches its baseline continuously, uniformly over the whole allowed coherence interval. Its projected normal derivative remains λN+, with N+ nonzero in every case.

All 48 nonidentity order pairs retain a nonzero normal contrast coefficient; the actual first-order contrast vanishes at zero coherence. All 24 identity-middle pairs have zero ordering contrast. The equal polar boundary limits found in 16.09 therefore did not imply that the underlying matrix had lost its ordering information.

The Gram derivative CᵀV+VᵀC is blind to the normal component. The leading normal energy λ²N+ᵀN+ loses the source sign; the full higher-order polynomial is archived and need not be even in coherence. This is a specific information-loss result, not a claim that all Gram response disappears.

| Evidence | Result |
|---|---|
| Exact physical families | 144 |
| Order pairs | 48 nonidentity + 24 identity |
| Numerical records | 3,456; 80/120 digits; two frames |
| Maximum weighted reconstruction error | 3.0102e-84 |
| Maximum cross-precision discrepancy | 1.2941e-66 |
| Uniform-bound violations | 0 |
| Independent publication checks | All projector, polynomial, bound, contrast and record-completeness checks passed |

The observable U|C| equals C by standard matrix algebra. The contribution of this loop is the audited response and information-loss classification in the frozen model, not a novel identity or a newly derived transport. The original polar boundary obstruction and the original five-edge null remain intact. Sources remain specified; no source-selection, clock or gravity law has been derived. Time is pruning / ordered recoverability update.

- [Full scientific report](demos/v15.56-response-selector-obstruction/continuous-response/RESULTS.md)
- [Complete raw results](demos/v15.56-response-selector-obstruction/continuous-response/result.json.xz): 19,446,793 bytes compressed losslessly to 1,907,732 bytes.
- [Execution and artifact provenance](demos/v15.56-response-selector-obstruction/continuous-response/EVIDENCE.json)
- [Successful run 36496955303](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36496955303), executed head `88109eeb3e7f60f73f433f5e0ed33938c943e205`.
- [Prior 16.09–16.11 final report at its publication commit](https://github.com/proteinfoldingengine/WetLabEngine/blob/75a9a64223880a2c39e1f54e5e544688e28f92c8/ResearchHistory/UQCF-GEM/V16_09-11_REPORT.md). Its aggregate publication checksums apply to that historical commit; scientific source and raw-result checksums remain unchanged.

The next concrete question is whether a frame-invariant closed-loop observable formed from continuous edge matrices retains the signed ordering response. This loop does not assume such a quantity is already geometric transport. No 16.13 measurement is included here.
