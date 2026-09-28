# v16.06 sixth-edge domain audit

Parent publication: 95f76672e379c05438b592d73e1bfd3ebf9c5835. The user approved the sixth-edge admissibility audit on 2026-09-28. This is an audit of the frozen baseline, not a new loop-response experiment.

Question: can edge (2,3) enter the inherited polar readout without changing its domain or choosing a null-space alignment?

Before new computation: reconstruct the exact connected baseline C23 from all archived binary-rational Pauli coefficients, including excluded-sector residues. Archive its symbolic polynomial in attenuation a for both preparations, determinants and minors; evaluate exact ranks at archived binary a=1,1/3,1/6. The ideal mixture has no raw 23 pair moment, so C23=-n2 n3^T has rank at most one. Do not assume the archived binary matrix shares the ideal support exactly.

Use all 12 candidates, both preparations, both frames and 50/80-digit archived origin matrices (288 frame cases). Compare exact native evaluations to archived matrices and their frame transforms with 1e-35 absolute Frobenius tolerance. Compare precisions with 1e-30. Evaluate the existing edge-domain code with the inherited unprepared connected baseline as reference: plane requires a second singular value >1e-9 reference and third <=1e-11 reference; isotropic requires all three >1e-9 reference and proper polar determinant. Never repair, regularize or select null axes. Record every spectrum, relative spectrum, exact rank and rejection reason.

Validity requires parent hashes, exact source reconstruction, full candidate/configuration coverage, matrix agreement, precision agreement, and identical domain decisions in both frames/precisions. Domain rejection is a scientific result, not INVALID. All rejected gives SIXTH_EDGE_OUTSIDE_FROZEN_DOMAIN; all admitted gives SIXTH_EDGE_ADMISSIBLE; otherwise MIXED_DOMAIN. Invalid evidence takes precedence.

No loop response is evaluated. Rank one leaves a rotational freedom in the two-dimensional null complement, even with proper orientation; the support partial isometry alone does not provide the inherited full link. Isotropic exact rank two, if caused by binary residues, must not be promoted into the frozen full-rank domain. At a=0 geometry remains excluded. Time is pruning / ordered recoverability update. No source-law or gravity claim.

Run absent-implementation RED, then unit and inherited tests; execute the audit in a targeted GitHub workflow. Publish complete results, logs, hashes and final report permanently.
