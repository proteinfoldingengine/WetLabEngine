# v15.14 — Record-dependent simulation extension

Continue the integrated simulator without changing the earlier files or ontology.
Base: 3fd5aa06ddc2970aa5662dfc57afbfcbe4b3c7e5, v15.13.

Reuse the exact earlier initial state and local instruments. Add ONE explicitly
supplied illustrative record-read rule: B2 uses the realized A1 bit to select a
finite rotation on B's second qubit, in addition to its previous local operation.
A1=0 uses extent +0.6, A1=1 uses -0.6. Neither value is fitted or a physical law.
Local chain dependencies remain A1<A2 and B1<B2. The extra read requires A1<B2.

1. Tests first: actual-record availability, no reading future outcome scripts,
   immutable input records, five permissible schedules, all 16 supplied records,
   state validity, record retention, Kraus completeness, common-ideal confluence,
   mass normalization and rejection of premature execution.
2. Implement a record-store scheduler and adaptive instrument. The instrument
   selector sees only realized declared read keys, not the complete outcome script.
3. Negative controls: bypass the missing record by guessing 0 or 1. Compare full
   joint outcome weights as well as final normalized states. Do not adopt a guess.
4. Produce an interactive readiness/blocked-event replay and short video from
   computed states. Graph layout/playback are not geometry or physical time.
5. Run new tests and prior 77 tests, retain logs, inspect HTML/video, publish a
   stacked draft branch. Do not claim new collapse physics or metric time.
