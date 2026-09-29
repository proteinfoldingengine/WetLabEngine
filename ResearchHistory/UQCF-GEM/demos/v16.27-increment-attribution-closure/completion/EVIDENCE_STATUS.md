# v16.27 completion ledger

Baseline `4a3eba5e36f49064515e4062b4cf18fcaeac5e9a`. Additive completion on research/v16.27-increment-attribution-closure. Original reports, implementations, tests and workflows are preserved.

- Ruling: the old coverage verifier is not independent; it calls the producer. Preserve its GREEN as execution evidence, not independent certification.
- Ruling: the old endpoint-mismatch test failure was a test-fixture problem (the assigned replacement could equal the existing endpoint), not automatically a discovered verifier defect. New strict-contract failures are recorded separately.
- Ruling: the historical path cap cannot truncate the admitted <=5-event universe (5!<=120); remove the cap in the new producer but do not fabricate a historical truncation.
- Ruling: h is a consistency-testing order, not an amount of retained information, elapsed time, or energy. Its telescoping total is an exact endpoint difference. No temporal or geometric no-go follows.
- Ruling: publish fresh complete path records and independently reconstruct their legality and coverage. Algorithms differ, but authorship/review remains self-review.

Completion status at preregistration: no new implementation or successful new adjudication yet.
