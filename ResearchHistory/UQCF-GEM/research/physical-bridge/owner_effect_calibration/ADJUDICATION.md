# Fixed-effect calibration adjudication

The exact signed-response interval for a fixed effect in the stated benchmark is
`[(a_min - b_max)/5, (a_max - b_min)/5]`.
A uniform nonzero response is equivalent to strict separation of its two retained-sector calibration intervals. The hidden factor can have any fixed finite dimension at least two. The proof realizes both extrema and every intermediate value using a hidden qubit. Availability of the effect, its association with retained source states, the preparation and actual-event correspondence remain supplied.

The two constructed effects exercise the criterion directly. The overlapping effect has response 1/50 for every realization with an entire two-dimensional complement. Extending the same available effect by an identity on a hidden qubit admits response zero, with exactly the same source channel and input pair. The separated effect guarantees response at least 2/25 throughout the enlarged class. The former uses the previously established T249 qubit exception. The latter illustrates the fixed-effect criterion with nonconstant calibration within each sector. These are chosen analytical controls. [Frozen assessment](https://github.com/proteinfoldingengine/WetLabEngine/blob/270128b05eb5910a79759692d5c8342fa650282f/ResearchHistory/UQCF-GEM/research/physical-bridge/owner_effect_calibration/ASSESSMENT.md) · [Exact matrix replay](https://github.com/proteinfoldingengine/WetLabEngine/blob/4896395feb2b19485b63db2c3866b224cc664210/ResearchHistory/UQCF-GEM/research/physical-bridge/owner_effect_calibration/verification.json)

Gemini 3.1 Pro Preview returned **ACCEPTED**, with empty findings, missing assumptions and counterexamples. Its native-bridge verdict is **NOT_DERIVED**. The proof, original boundary sources, exact control code and raw results were included in the prompt. [Full raw verdict](evidence/review_verdict.json) · [Complete request and response archive](evidence/owner-calibration-whole-argument-review.zip)

## Corrections to two reviewer scope statements

The review says the bounds depend on a hidden factor that can be arbitrarily large. That is stronger than the actual condition. A fixed hidden dimension of two already gives the entire exact interval, by the explicit orthogonal flags construction. No larger-dimension limit is taken.

The review also says the full interface is initially informative. The manuscript specifies an available effect and leaves the owner's complete interface unspecified. The algebra of all operators on the full ambient space can distinguish the input pair. It need not be the owner's available interface. The proved statement is initial equality for the tested effect, with full-interface blindness unclaimed. In fact the algebra generated solely by either constructed block-diagonal effect is initially blind on this pair, because its u and v blocks agree for every function of that effect. This elementary observation corrects the reviewer’s blanket sentence and establishes no physical availability.

These corrections concern the reviewer commentary. They leave the frozen argument, equations, code, inputs, raw response and finite outputs intact. No additional model generation was requested.

## Execution and publication evidence

[Run 44373775973](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44373775973) completed the replay, whole-argument review and publication audit on attempt one at checkout and workflow SHA `4896395feb2b19485b63db2c3866b224cc664210`. The replay and a fresh replay in the publication job both matched the committed exact result byte for byte. Each tested isometry was checked on the complete 16 source matrix units, preserving retained coherences as well as the selected pair.

The three downloaded archives matched GitHub's SHA-256 digests and byte counts, and their member CRC checks passed. The raw response and publication receipt also matched their exact log readbacks. [Archive manifest](evidence/archive_checks.json) · [Review receipt](evidence/receipt.json) · [Replay archive](evidence/owner-calibration-source-replay.zip) · [Publication receipt archive](evidence/owner-calibration-publication-readback.zip)

This is supporting mathematics within the existing conditional event model. It supplies an exact calibration requirement for future owner-effect proposals. No native ownership, event correspondence, gravity signal, new physical postulate or numbered-stage closure follows. The source task remains finding an inherited operation that establishes the available owner effect and the relevant physical association.
