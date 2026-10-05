# A11.X47 source-integrity erratum closeout

Status: ACCEPTED SOURCE-INTEGRITY CORRECTION when the distinct reporting review and final immutable readback are published. No new mathematical result, numerical execution or numbered certification.

Historical accepted head: 6414a606bba86712faa89222ef5f7d5203085acd.
Erratum scope commit: 541b1894e5462d20ebee59ab12aebee48d21b10d.
Corrected candidate: 4372e9fc280ed0fd7f4b9c21c796bcc84d96dff4.
Corrected candidate tree: 82f74f55179a2683e90047c8e905c1406fb4c5be.
Corrected proof blob: 29d5a612862d84c85a47a56ee47409f029e96719.

Authoritative readable proof: A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION_CORRECTED.md.
Fresh whole/source-integrity review: INDEPENDENT_A11_X47_ERRATUM_WHOLE_REVIEW.md, ACCEPTED without correction.

## Incident and root cause

Ordinary JavaScript template-literal escaping corrupted LaTeX-bearing Markdown before upload. Live scans reproduced 39 forbidden controls in the historical proof, 19 in the historical whole review, 4 in the historical closeout and 5 in each of the three X47 report blocks. The proof and whole review retained zero literal backslashes.

The earlier readback tested equality with the already-corrupted in-memory string. It proved transport identity, not readable-source integrity.

## Correction

The corrected proof uses ASCII mathematics and a new filename. It contains zero forbidden C0 controls, zero replacement characters and all required literal theorem tokens. The old source and reviews remain at their immutable commit as incident evidence.

Fresh review verified exact equivalence of the beta theorem, sharpness family, exact four-cover proof, empty X45 intersection, beta/Gamma/rho formulas, X40L-before-Theorem-A dependency, every method separation/control and every nonclaim.

## Boundary

X47 remains an accepted analytical theorem. This erratum changes only its authoritative readable rendering and reporting. It does not reopen or recertify v16.55/v16.54, authorize numerical work, start efficiency work, merge integration or add a theorem.

The next mathematical obligation remains a joint condition coupling actual lower witnesses to transitions among actual four-covers.

## Publication gate

Publish the exact corrected proof and whole review, reconcile the four reports, obtain a distinct exact reporting review, append only that review, then perform immutable readback, full-tree comparison and non-force live-reference verification.
