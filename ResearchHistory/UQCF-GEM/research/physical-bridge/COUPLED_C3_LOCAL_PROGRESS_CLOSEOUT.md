# Safe local progress with inaccessible reserve — scoped closeout

Status: **CLOSED for the declared theorem and bounded verification contract.** Broad C3/general C4, native observer-record origin, source admission, actual outcome selection, and guaranteed progress remain OPEN. This is not a numbered-v16 or full-stack certification.

## Result

For arbitrary `n>=2`, take roots `L_i={a,c_i}`, `R_i={b,c_i}`, `T={f,g,h}`, and `U={f}` with saturated floors two on `L/R`, three on `T`, and one on `U`. Hidden labels range over all original protected completions and are never read or changed.

The exact static active-label minimum is `kappa=7`. The source is not isolated: safe changing edits exist at `U`. Nevertheless, its entire uniformly safe single-toggle component contains exactly seven cores—`L/R` and `T` never change while `U` ranges over nonempty subsets of `{f,g,h}`. Every palette label remains active throughout this component.

For `n>=3`, a universally safe seven-label target exists with `c_3,...,c_n` absent, so the static spare capacity `n-2` grows without bound while no reserve is reachable from the source. At `n=2`, the target is still outside the component but no absent-label surplus is claimed. Thus `kappa<|P|` plus genuine safe local motion is insufficient for transferable reserve capacity.

This is a family-specific obstruction, not a general impossibility theorem. It does not rule out a stronger criterion requiring motion in a repair-relevant component or a restoring path to the actual destination.

## Verification and review

The analytical construction and prospective contract were frozen at `4426bd04f91913d09d9f939ad2e9119f858473e4`. The original execution at `f36a2d8ad65149aab7fc444c79523c46002f2e7c` and internal evidence report at `9b0449fce503fd7582c4e6cdc41c71b13d4c018b` remain preserved.

The exact-commit Gemini campaign ran on immutable event commit `afbbb19cb11a578d3d8a5ad43f6c2490d03dd35a` in [Actions run 38021164402](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/38021164402):

- 135 tests passed: 17 new plus 118 inherited.
- Independent complete reconstruction covered four families (`n=2..5`), 28 reachable states, 72 directed edges, 5,298 original protected one-hidden completions, 42,384 state/target checks, and 2,140 rejecting toggles.
- The certificate was independently rebuilt byte-for-byte with SHA-256 `7deae40ee68d1671f973a77a7054ce6dec3ec208ad31aaa3fd8cf8aaa3e54d5e`.
- Gemini 3.1 Pro adversarial mathematical review: `ACCEPTED`, zero missing assumptions, zero counterexamples.
- Separate Gemini 3.1 Pro publication audit: `ACCEPTED`, zero missing assumptions, zero counterexamples.
- The publication gate verified 22 mathematical-review inputs, exact event-commit provenance, response hashes, byte-identical reproduction, and independent full reconstruction.

All three original workflow artifact ZIPs, all three complete job logs, raw review responses, manifests, the publication gate, archive hashes, and member hashes are preserved under `evidence/local-progress/external-review/`. The mathematical review's isolated/non-isolated wording slip is preserved and adjudicated in `COUPLED_C3_LOCAL_PROGRESS_GEMINI_RECONCILIATION.md`.

## Boundaries and next obligation

The theorem assumes the original protected fiber, fixed core palette, original floors, supplied current-core access, single-incidence toggles, and actual committed progress. Optional NOOPs can still stall. No admissibility relation is promoted into an implementation or outcome-selection oracle.

Next seek a reusable positive condition for releasing a prescribed occupied label with an actual restoring route to the exact repair destination. Donor-footprint containment, floor replacement/slack, and an upper-four cover must be maintained jointly; static capacity and unrelated local motion are insufficient.

