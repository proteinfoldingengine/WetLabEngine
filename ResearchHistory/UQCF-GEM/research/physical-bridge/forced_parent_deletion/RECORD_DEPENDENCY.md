# A recorded dependency that changes a later read

**Status:** Verified in the archived implementations. Native receiver delivery and the physical gravity signal remain open.

The [frozen protocol](RECORD_DEPENDENCY_PROTOCOL.md) preregistered controlled interventions in two original programs. Here “later” means later in the supplied event order. No clock, elapsed duration, detector, or additional response operator is used.

## V1472.3 — the named prior record is read

The original implementation is pinned to Git blob `797951f651014ce4b5bf753bb478dedfc0c0cabe`. `process_event` (lines 173–249) appends the dependency edge named by `prior_dependency` (lines 193–199) and stores the input `entropy_after` under the event ID (line 209). `_slice_coherence` (lines 148–171) reads those edges and stored values. In an admissible slice with \(m>0\) edges its result is

$$
C=\exp\left[-\frac{1}{m}\sum_{a\to b}(S_b-S_a)^2\right].
$$

With a single source and no edges, the result is 1. For a supplied source event the entropy validator accepts an absolute change up to `max(1e-9, abs(state_delta) + 1e-9)`. The trace provides both the number it stores and the predecessor label. `state_delta` is used for acceptance and does not enter the score.

**Source intervention.** Keep the original initial source’s reported before-value at \(1/10\). Change its reported after-value from \(1/10\) to \(1/5\) and its supplied `state_delta` from 0 to \(1/10\) to satisfy validation. Every downstream record is identical to baseline, including the next record’s own before-value \(1/10\), after-value \(3/4\), and named predecessor `e0_source`. Both source slices return the same score. The next slice has exactly one edge. The score changes from \(\exp(-169/400)=0.655406254327\) to \(\exp(-121/400)=0.738968488259\). Both traces are admissible. The difference comes from the previously stored source value.

**Prior intervention.** Reroute the first repair from `e2_loss` to `e1_disruption`, keeping all other fields fixed. The first three slices agree. At the repair, the three edge differences change from \(0.65,0.15,-0.35\) to \(0.65,0.15,-0.20\). The score changes from \(\exp(-227/1200)=0.827648553773\) to \(\exp(-97/600)=0.850724732194\). Both repair slices are admissible. The sole change is which stored record this edge names.

**Controls.** Missing prior and wrong provenance each produce their respective failure and suppress the score. In each case the event ID remains active and the archival caller still writes the supplied \(0.75\). The check therefore establishes an output gate, with a retained write even on these failed inputs. Reversing file order returns the same transcript because the original loader sorts by supplied ordinal.

## V1700.2 — chain fields may be broken without changing the result

The ZIP is pinned to Git blob `49742bac537ba7f7cbe61532c4bb959daed25d3a`. The checked Python member SHA-256 is `9ca0160105b7d2d2abece717723d8478acd6964d54519536bda90383ed722200`. Its original `charts` generator adds the literal `event` and `prior` fields (lines 78–85). Inspection of `current_node`, `integrity`, `J`, `B`, and the `eval_case` path (lines 87, 114–128, 142–160, 244–262) shows that the result depends on consumed chart and cell fields, including source and order witnesses. The literal chain fields are generated but have no downstream reads.

For each native size (9, 13, 17, 25, 33, 49, 65, 97), the checker changes only the generated rows in one of two ways: it swaps the first two event IDs, or changes the second record’s prior pointer to its own ID. Each intervention breaks that record’s predecessor relation. All eight gates still pass in both interventions. The entire return, including all 308 cell rows per intervention, serializes identically to baseline under the same canonical JSON serialization. Directly comparing edited charts with separate, unedited reference charts via original `integrity` also gives zero mismatches in all 16 checks. The original `order_shuffle` control changes a consumed order witness and changes \(q\) in all 308 cells. Every control gate fails. These facts apply to this audit’s read path.

## Consequence for Path A

The V1472.3 witness is an executed, identifier-addressed write followed by an actual numerical read. V1700.2 supplies a control for treating lineage metadata as evidence of causal use. V1472.3 takes the value and prior from a synthetic trace, and the reader is the shared software governor. The next missing link is an inherited event that produces its source-dependent state under the model’s own operation and delivers it to a mathematically identified receiver with an available read. Physical correspondence and pre-time gravity remain open.

Replays use [the trace checker](check_trace_dependency.py) and [the momentum checker](check_momentum_dependency.py). Their full deterministic receipts are [trace](evidence/record_dependency/trace.json) and [momentum](evidence/record_dependency/momentum.json).
