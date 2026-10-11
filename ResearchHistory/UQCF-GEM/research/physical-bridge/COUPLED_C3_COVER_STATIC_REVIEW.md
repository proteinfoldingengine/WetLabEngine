# Cover-aware static reserve — implementation review

Status: independent code review ACCEPTED after one Important correction; scientific publication remains OPEN.
Reviewer: fresh separate agent /root/cover_static_code_review, review only, no implementation delegation. Prospective parent cf854dc082d82482f8d59b2fe122fdb059a9b5b7; source files reviewed locally before scientific publication.

The reviewer independently compared all 3,072 ordered source identities and six complete fixture reconstructions, accepted the complete count/cover/endpoint construction and exact protected-mask evaluation, and found no mathematical/domain omission or unsupported reachability claim. Full campaign execution was deliberately left to the independent verifier and fresh reproduction gates.

## Important finding and correction

Optimized Python removed assertion-based verification gates: a malformed six-record fixture returned True under python3 -O. This was independently reproduced before correction in optimized_runtime_red.log. Both producer and checker now reject optimized Python with an explicit non-removable top-level runtime guard. A subprocess regression was added; new scientific test count is35. The reviewer independently confirmed both modules reject -O, -OO and PYTHONOPTIMIZE=1 and accepted the correction with no remaining Critical or Important findings.

The reviewer's final inspection preceded complete final-test/readback evidence, and therefore did not attest those gates. The author separately verified tests_complete.log (35tests, exit0), independent_final.log (complete reconstruction PASS), all15 inherited suite logs (378tests, all exit0), and fresh_comparison.json (both files byteequal). The redirected tests_final.log and tests_final_attempt2.log lack terminal summaries and are retained as incomplete evidence; terminal outputs passed, and tests_complete.log captures the complete third run after subprocess exit. No scientific scope was changed.

## Retained boundaries

Endpoint-only theorem; all-positive integer profiles analytical; finite campaign exactly the frozen carrier/saturation families and binary profiles. First/last anchor conventions only, all protected one-hidden masks only; universal anchor/hidden validity analytical. No routes, reachability classification, edit-cost optimality, acquisition, access, native retained output, committed progress or broad C3/C4 closure.
