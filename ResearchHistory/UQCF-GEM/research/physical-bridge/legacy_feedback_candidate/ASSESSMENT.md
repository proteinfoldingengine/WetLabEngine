# V1153: an implemented ensemble write and feedback, with native typing still missing

Date: 2026-11-11 America/Phoenix. Author: GPT Work.
Inspected scientific snapshot: `b65060486618662ed1a57ffddc110a33df1edfe9`.
Status: **IMPLEMENTED ENSEMBLE WRITE LOCATED; NATIVE EVENT / OWNER BINDING OPEN.**
This source-specific investigation identifies an existing update rather than constructing a new consumer. No legacy program was executed and no new physical law was adopted.

## 1. Exact source and provenance

[Original V1153 engine](https://github.com/proteinfoldingengine/WetLabEngine/blob/b65060486618662ed1a57ffddc110a33df1edfe9/Tmp/TOE/Einstein%206/v1153_first_principles_recoverable_pruning/v1153_first_principles_recoverable_pruning_engine.py):

- Git blob: `c473e6f750577a5e63d2481c1d702031edfb99b6`.
- SHA-256: `f44dbada0b812551ad4e79c8df3aea73e3113dea54bfab5999cccac693850a0a`.
- UTF-8 bytes: 15,979.
- The original path at the inspected commit returns this same blob.

The blob agrees with the V1153 identity frozen by `ResearchHistory/UQCF-GEM/v15/v15.10/pruning_order_emergent_time_audit.py`. I fetched the complete blob, hashed its UTF-8 bytes, verified Git's blob-header hash, and parsed the source without importing it. Parsing identifies syntax; the interpretation below follows the actual function bodies.

The original V1153 report, blob `1fe4248b71fd9e6628b7aee52eacbab96830bfde`, describes histories competing under an informational potential and preserves its toy-assay claim boundary.

## 2. The actual write, not merely a proposed readout

| Step | Source location | Actual operation |
|---|---|---|
| Candidate data | Candidate, lines 81-89 | Stores idx, mode, source, order_memory, geometry, flow, accessibility and weight |
| Per-history potential | primitive_potential, lines 191-230 | Reads that candidate's fields and returns U_info |
| Shared weight update | run_engine, lines 280-289 | Computes all U values, normalizes their weighted exponentials, then assigns each c.weight |
| Feedback into fields | update_candidate, lines 247-252 | Uses the newly assigned c.weight in the source update |
| Software record | run_engine, lines 291-298 | Stores the new weight and existing potential diagnostics in history_rows |
| Accessibility array | update_candidate, lines 268-269 | Recomputes a numerical array from the source, geometry and order_memory |

The first inter-history coupling in one iteration is the shared weight denominator. The field feedback is explicit: line 250 includes

    0.015 * c.weight * (expected_geometry - c.geometry).

Thus it would be incorrect to say this inspected engine has no implemented field-sensitive write or only a passive plotting routine. It updates stored weights and subsequently uses them in the candidate dynamics.

This is a source-dataflow result. A source-array perturbation need not change U_info for every pair. No new preparation pair has been asserted to be realized by the native P1 event.

## 3. Exact sensitivity of the existing weight writer

Fix old positive candidate weights and all potentials except U_A. Choose A away from the minimum and vary U_A in an interval where the minimum U_* remains unchanged. This is a conditional examination of the implemented update, not an adopted event law. Put

    a_i = w_i exp[-beta(U_i-U_*)],
    Z = EPS + sum_i a_i,
    w_i^+ = a_i/Z.

For B != A, direct differentiation gives

    partial w_B^+ / partial U_A = beta a_A a_B / Z^2
                               = beta w_A^+ w_B^+ > 0.

This includes the literal EPS in the denominator; it does not silently replace the implementation by a perfectly normalized simplex map. For a finite change delta in U_A, set t=exp(-beta delta). Then

    w_B^{+,new} - w_B^{+,old}
       = a_B a_A (1-t) / [Z (Z+a_A(t-1))].

These are identities of the real-arithmetic update formula. Strict positivity is not asserted after arbitrary floating-point underflow. No such numerical behavior was tested here.

The stored weight therefore changes when delta is nonzero under the stated real-arithmetic assumptions. However, for B,C != A,

    w_B^+ / w_C^+ = a_B/a_C,

so their relative weights are unchanged. A global probability-weight change is not, by itself, proof of a locally readable state change in an independently existing receiver.

The later feedback is a separate code operation. Hold B's input arrays, update position and random draws fixed. Its geometry update does not use c.weight, so it is identical in the two comparisons. Let d_B be expected_geometry minus that newly updated geometry. Before source normalization, the difference contributed by the weight change is exactly

    0.015 * (w_B^{+,new}-w_B^{+,old}) * d_B.

The actual source output then passes through normalize_unit. A nonzero field difference is not guaranteed: d_B=0, or a constant d_B removed by centering, defeats it. The displayed sensitivity is an analytical code consequence, not a numerical separation claim for the original seven histories or the fixed Path-A pair.

## 4. Why this is not yet the native receiver construction

The source identifies these objects as seven candidate histories/modes on a fixed 128-coordinate grid. The inspected functions do not identify Candidate.idx with a Genesis-pinned retained address or type the iteration as the P1 deletion u->p. The source arrays are repeatedly centered and standardized; they are not identified there with the extensive positive grade on a changing prefix tree.

A direct identification of history weights with P1 grades also fails without extra input. With the same old weights and the same declared P1 pruning held fixed, P1 has a fixed output. The legacy weight rule can produce different outputs when U_A changes. A representation that includes that additional state or changes the event might be possible, but it requires an explicit typed map; renaming the quantities does not supply one.

Within the software, the potential formula, beta=2.2, the normalization and the 0.015 feedback term are explicit implemented rules. They are inherited as **legacy model specifications**, not thereby derived from the Path-A native event axioms. The inspected original report gives their computational interpretation but no derivation of this feedback term as an owner-bound P1 operation.

The numerical field named accessibility is likewise not an operational proof that a retained owner can perform a read. The visible record consumer is software telemetry/output. Distinguishing a field variable, a stored ensemble weight and an owner's available effect remains necessary.

The first missing link for this candidate is therefore the event/state correspondence:

    native P1 preparation and event -> the specified Candidate state and update.

An independently justified retained-owner association and available effect remain separate. This investigation does not replace the frozen four-address source pair with the seven-history ensemble or claim that the ensemble distinguishes that pair.

## 5. Continuity and disposition

The v15.10 CONTINUITY_NOTICE is respected: its fixed-known-potential inverse does not prove reversibility of the full coupled engine, and an execution loop does not disqualify pre-time computation. This candidate is not rejected merely for having a loop or a reversible weight substep.

The earlier `native_record_writer_trace/ASSESSMENT.md` located V1172's diagnostic writer and separated it from a precomputed provenance ledger. Here the distinct object inspected is V1153's automatic ensemble-weight write and its explicit feedback into the field. No archive-wide novelty or absence claim is made.

**Result:** a concrete producer exists at the software-model level, with an explicit coupling formula. No native ownership/access premise has moved from SUPPLIED to DERIVED. This does not yet admit a physical-delivery campaign.

Re-entry should supply the exact already-justified event/state map and owner trace for this code path, if one exists. Do not add a fresh copying channel, reinterpret ensemble weights as receiver records by fiat, or launch parameter sweeps to make the output resemble delivery.

Verification: complete-source identity and syntax inspection only; hand-derived algebra; no simulation, historical replay, finite campaign, model API request, independent acceptance, new research branch or merge. Native delivery remains NOT_DERIVED.

## 6. Correction dated 2026-11-12: prior producer screen and review credited

This append-only correction supersedes any reading of the opening status or section 5 as a newly discovered V1153 producer. The November 11 text above is preserved so the correction remains auditable. PR111 comment [6812282128](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6812282128) identified the prior screen; Grok accepted that correction in T-420. I have now read the prior result, status and final readback at research commit `1abc8246283f3f37e7794e900fa302f289313bc4`.

The same engine blob `c473e6f750577a5e63d2481c1d702031edfb99b6` was already examined on October 17. The existing screen traced source -> primitive_potential -> stored-weight update -> host log, constructed an initially weight-blind input pair, derived the exact-real first-step relative-weight factor exp(-4 beta c), and stopped native promotion at the supplied carrier/reference, then update/access/retention premises. That producer, its source dependence, and its host retention are not new November findings.

| Prior evidence | Exact Git blob | What it establishes |
|---|---|---|
| [v1153_record_screen/RESULT.md](../v1153_record_screen/RESULT.md) | `7728ca6da85c00a992f10ee7dac511a4f81f4976` | Frozen October 17 conditional derivation and candidate-specific stop |
| [v1153_record_screen/STATUS.md](../v1153_record_screen/STATUS.md) | `60f8283d28ef4af9dbb9caf68320974e88b4488f` | Records Gemini ACCEPTED, run 38996098467 attempt 1, and separate publication audit PASS |
| [v1153_record_screen/FINAL_READBACK.md](../v1153_record_screen/FINAL_READBACK.md) | `c7d6304e4b32640afd0140bdac9b1bcef3874a48` | Records immutable source, argument and review-evidence readback after publication |

The bounded additive detail here is the downstream edge in update_candidate: the newly assigned weight multiplies 0.015 * (expected_geometry - updated_geometry) in the source update. Section 3 traces its conditional sensitivity and explains why subsequent normalization can erase a field difference. This is a source/dataflow clarification, not a new producer, a new preparation witness, or native delivery progress.

The October acceptance applies to its frozen argument and stop. It does not independently accept the November feedback calculation. For this correction I read the preserved status and final readback; I did not rerun Gemini or repeat their raw-artifact audit.

**Corrected disposition:** the existing V1153 native-record stop remains in force. No event/state/owner correspondence or owner-available effect was derived here. Re-entry still requires a cited derivation of the missing native obligations for this exact code path. No new V1153 campaign or duplicate review is requested.
