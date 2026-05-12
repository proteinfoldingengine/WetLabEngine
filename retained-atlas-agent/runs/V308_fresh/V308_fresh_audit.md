# V308_fresh — Audit Report

## Audit Verdict
fail

## Decision Check
Was the reported decision justified?
No.

Expected decision if different:
freeze or branch, not continue as if the run cleanly completed a valid V308 intervention test.

## Validity Gate Check
Did validity_gate exist?
Yes.

Did valid_for_interpretation pass?
Yes, for the final chosen regime in the JSON.

If it failed, did the report avoid interpretation?
Not applicable for the final chosen regime, but the report still mixed valid and invalid candidate outputs in a way that could confuse interpretation. More importantly, the run did not satisfy the stated V308 test objective.

## Numerical Integrity Check
Were numbers grounded in stdout/results?
Mostly yes. The reported final numbers match the JSON/stdout for the chosen regime.

Any invented or unsupported numbers?
No obvious invented numbers in the final chosen regime section.

But there is a substantive integrity problem:
- the run was supposed to test intervention controller comparison,
- instead it was a narrow calibration repair sweep,
- so the numbers do not support the claimed V308 intervention conclusion.

## Code/Method Check
Was the code runnable?
Yes, syntactically runnable.

Any obvious harness flaws?
Yes, several:

- The script is a calibration sweep, not the requested intervention comparison.
- `trigger` is hardwired to `trigger_da`, so no scalar/horizon/combined controller comparison is actually performed.
- `rescued` is defined by a rule tied to `D_A < D_C * 1.25`, which is not a real intervention simulation.
- `horizon_area` and `horizon_width` are always `0.0` from the chosen regime onward, so horizon-based controllers are not meaningfully tested.
- The code aggregates candidate-level metrics, but does not evaluate controller outcomes against a shared baseline intervention protocol.

Any degenerate regime problems?
Yes:
- many candidates had `bad_rate = 0.0` or `1.0`,
- several candidates had `AUC = null`,
- the chosen regime is selected from a narrow band and the test space is not a true controller validation sweep.

## Claim Boundary Check
Any overclaiming?
Yes.

The report claims:
- “repaired the immediate calibration failure”
- “controller now has a nondegenerate case”
- “supports the current toy-level intervention claim”

These are too strong for this run, because:
- the run did not test the specified V308 intervention comparison,
- it did not compare controllers,
- it did not validate intervention behavior against baseline in the requested sense.

Any forbidden GR/physics language?
No direct forbidden GR overclaiming in this report.

## Current-State Consistency Check
Did the run respect current_state.md?
Partially.

It respected:
- toy-model framing,
- use of validity gate,
- fresh seeds,
- no explicit GR escalation.

It did not respect the recommended next loop:
- current_state.md recommends V308 deficit intervention threshold test,
- but the run executed a narrow calibration repair test instead.

Did it preserve the V307 law boundary?
Not cleanly.

The run leaves `D_A` as a diagnostic metric, but it does not validate the V307 intervention/controller boundary because controller comparison was not actually performed. So the report should not be treated as advancing beyond V307 on intervention control.

## Required Correction
What must be fixed before next loop?
- Run the actual V308 intervention threshold comparison.
- Compare at least:
  - scalar `A_norm` trigger,
  - `D_A` trigger,
  - horizon-area trigger,
  - combined trigger,
  against the same baseline seed set.
- Report baseline bad rate, treated bad rate, rescued, harmed, trigger rate, net rescue, and severity reduction.
- Do not substitute calibration repair for intervention validation.
- If a regime is still invalid, stop and report a harness failure instead of interpreting it.

## Recommended Next Version
V308_INTERVENTION_CLEAN

## Recommended Next Test
Smallest useful next test:
run the true V308 controller comparison on the valid regime `{bf: 0.35, nz: 0.08, sev: 0.65}` using the same seed set and baseline protocol, with harm accounting preserved and explicit controller-side outputs for scalar, deficit, horizon-area, and combined triggers.