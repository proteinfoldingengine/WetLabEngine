# Independent operation check: V725 and V737

This is a bounded, read-only source and algebra review of the three supplied text transcriptions. Neither Python source was imported or executed. No model call, numerical assay, metric reproduction, external lookup, or GitHub write was performed. The reviewed files are Library-read text transcriptions with a final LF, not authenticated downloads of original bytes. All line references below refer to these local transcriptions in `package/ResearchHistory/UQCF-GEM/research/physical-bridge/atrium_owner_trace/source_transcriptions/`.

## Finding

The visible programs supply an active parameter-response mechanism: paired runs have the same entire initial visible field and target, while an explicitly selected parameter `k` changes the update. The supplied metric code can read the ensuing trajectory and the target, so the scalar need not contain a direct numerical `k` term to respond to the selected dynamics.

This is a useful positive result, but it does not supply the requested native chain from an actual event, through an independently identified retained owner, to an available source-dependent effect. Neither source reads an actual pruning/event record, identifies a retained owner independently of the arm designation, or derives `k` from that record or owner. Their data path starts with a synthetic preparation and a chosen high/low `k`. The missing native input-to-parameter link is upstream of a real, explicitly coded parameter-to-response link.

The exact one-step identities below establish the parameter dependence of the update, subject to the displayed vectors being nonzero. They do not establish nonzero scalar separation for every preparation, numerical reproducibility, an AUC, or a physical receiver/reader.

## Parameter origin and native event/owner boundary

| Source | Exact entry point and parameter origin | Consequence |
|---|---|---|
| V725 | `run_assay`, lines 228–235: caller parameters default to `k_high = 0.90`, `k_low = 0.25`. Lines 251–253 assign `(label, k)` as `(0, k_high)` and `(1, k_low)` and pass `k` directly to `relax_response` and `compute_metrics`. | `k` is an experimental/model input. The label is assigned with the selected arm, not inferred from an independently observed owner. |
| V725 | `k_gap_ablation`, lines 282–287, fixes the high value and calculates the low value from a chosen gap. `monotonic_by_k_scan`, lines 300–304, supplies a list of low values to `run_assay`. | The scans vary selected parameter values; they do not implement an event-to-`k` derivation. |
| V737 | `build_dataset`, lines 141–145, receives `k_gap`, sets `high_k = 0.82`, and sets `low_k = max(0.0, high_k - k_gap)`. Lines 154–156 assign labels and pass each `k` directly to `simulate` and `metrics_for_run`. | Again, the capacity designation and parameter are selected together. |
| V737 | `main`, lines 174–185, chooses the main gap and the gap-scan list. | No preceding owner/event computation supplies these choices. |

V725's imports (lines 20–27), preparation and assay (lines 73–137, 228–255), and main/output path (lines 315–329, 458–480) contain no upstream model import, event-data read, pruning transition, owner map, or event-derived `k`. V737's imports and setup (lines 16–24), preparation and assay (lines 45–90, 141–158), and main/output path (lines 174–223) likewise contain none. These are findings about the reviewed complete text bodies, not a claim that no other source could contain such a map.

The phrases “retained atlas field” in V725 `curvature_like` (lines 66–70) and “retained restorative capacity” in `relax_response` (lines 112–117) name an interpretation. They do not add an executable retained-owner identity or an actual event record. No sourced `P1 → k` map or owner-held record is present in these files.

## Same preparation and exact updates

### V725

`run_assay` generates `target`, `x0`, `mask`, `direction`, `amplitude`, and `x_pert` once per pair (lines 239–246). It also generates the complete additive `noise_schedule` once per pair (lines 248–249). Both arms receive those same objects (lines 251–253). `relax_response` copies `x_start` before evolution (lines 119–120), so the updater does not alter the shared starting array.

Consequently the two arms have the same complete pre-probe field `x0` and the same complete perturbed initial field `x_pert`, not just equal means or curvatures. The pair still differs in its model parameter `k`; full state/configuration equality including `k` is not established or intended.

Let `t` denote the shared target, `x` the common initial perturbed field, `eta` the shared additive noise at the first step, and `L` the operator implemented at lines 125–128:

- Interior: `(Lx)_i = x_(i-1) - 2 x_i + x_(i+1)`.
- First endpoint: `(Lx)_0 = x_1 - x_0`.
- Last endpoint: `(Lx)_(n-1) = x_(n-2) - x_(n-1)`.

The code at lines 123–135 gives

```text
x_k^+ = x + k(t - x) + 0.06 k Lx + eta
          + 0.015(1 - k) tanh(Lx).
```

With `Delta k = k_high - k_low`, subtraction at the common initial field yields exactly

```text
x_high^+ - x_low^+
  = Delta k [(t - x) + 0.06 Lx - 0.015 tanh(Lx)].
```

The parent's provisional identity is correct. Common additive noise cancels. This is a same-state one-step identity; it must not be reapplied unchanged at later times after the two states diverge.

### V737

`build_dataset` creates the target and perturbation once per pair (lines 148–151) and passes them to both arms (lines 154–156). `simulate` starts each arm from `state = target + 0.55 * pert` (lines 82–84), so the entire initial visible field is the same. The returned `perturbed` field at line 90 is the same expression. Neither input is modified by `simulate`.

The pair also uses the same `pair_seed` for a fresh generator in each arm (lines 152–155). However, `simulate` sets the noise standard deviation to

```text
0.007 + 0.005 (1 - k) = 0.012 - 0.005 k
```

at line 87. Thus the common-seed coupling gives the same underlying standardized Gaussian sequence, with a different scale in the two arms. Same seed does not mean the same additive noise when `k` differs. Both drift and stochastic amplitude vary with the selected capacity parameter.

Let `L0` be `second_diff` at lines 41–42: ordinary second differences on the interior and zero output at both endpoints. Under the code's common-standardized-draw coupling, write the first Gaussian vector as `z`. Lines 85–89 then give

```text
x_k^+ = x - 0.20 k (x - t) - 0.030 k L0 x - 0.010 x
          + (0.012 - 0.005 k) z.
```

For the same initial field and target,

```text
x_high^+ - x_low^+
  = Delta k [-0.20 (x - t) - 0.030 L0 x - 0.005 z].
```

The parent's provisional identity is correct. The `-0.010 x` term cancels; the scaled noise does not. Preserve the negative sign on the `L0` term when describing this implementation. These equations interpret the programmed stochastic coupling; they are not a floating-point reproduction or a certification of a particular NumPy execution.

## What the passive comparison establishes

V725 calculates passive statistics from `x0 - target`: mean absolute residual and mean absolute second difference (lines 176–177, with `curvature_like` at 66–70). V737 calculates them from the complete initial `perturbed` field: its mean and mean squared second difference (lines 136–137, with `second_var` at 37–38). These are different definitions across the two programs.

Within each respective pair, equality of the input fields makes the corresponding passive statistics identical by construction. More strongly, any deterministic function restricted to the same initial visible array and shared target would return the same value in the pair. This does not show that every permitted observation is identical once `k`, arm metadata, evolution, or calibration information is included. It also does not itself reproduce a reported passive AUC.

For equal high and low `k`, the update arguments coincide in V725, and both the drift and noise scale also coincide in V737. Source inspection therefore gives a structural reason for identical paired response paths in that limiting case under the same deterministic execution conditions. No reported null-gap number is recertified here.

## Observation access and calibration

| Source/function | Actual inputs used by the metric | Boundary for an operational reader |
|---|---|---|
| V725 `compute_metrics`, lines 140–178 | `x_pert`, `target`, and the trajectory determine initial/final target distances, contraction, path length and deviation, temporal second variation, final-window boundary, and strain. `x0` and `target` determine passive statistics. | The target, initial data, and trajectory are supplied directly. The code does not derive a physical observation permission or show that a separate receiver owns these records. |
| V725 `zscore_from_admissible`, lines 181–186; `finalize_metric`, lines 195–225 | The high-capacity cohort is selected using `labels == 0`. Its mean and standard deviation calibrate restoration distances. Other terms use `normalize01` (189–192) over the supplied metric collection. | The composite has a high-arm-labelled calibration dependency and a cohort normalization dependency, despite no direct numerical `k` addend in `g_observable`. A proposed reader must have this reference/calibration information as well as the raw observations. |
| V737 `metrics_for_run`, lines 93–138 | The initial/full trajectory and target determine restoration residual, path deviation, curvature residual, observation-window ratio, and strain. `atrium_scalar` at 117–123 combines those values. `label` and `k` are included only in returned metadata at 126–129. | The scalar removes V725's `adm_z` and its high-arm calibration. Its shown formula does not use labels or direct `k`, but it still presumes access to target and trajectory. |

V725 explicitly separates the direct-`k` oracle: `retained_capacity_deficit` at line 204 enters only `g_oracle` at line 219. `g_observable` at lines 209–216 contains no direct `m.k` term. Its `adm_z` input nonetheless depends on the labelled high-capacity reference cohort (lines 196, 206). The precise wording is therefore “no direct numerical `k` term in the final candidate, with high-arm calibration,” rather than an unrestricted claim that no capacity-side metadata enters the metric construction.

That calibration dependence alone is not a finding that an AUC or metric is invalid. It identifies what the implemented calculation is allowed to know. V737 eliminates this particular calibration path but does not supply the missing event/owner-to-`k` path. Neither program contains an independently specified physical receiver, target-estimation channel, or owner-held record readout.

## Bounded AUC implementation caveat

V725 `auc_score` adds `np.sum(p > neg)` and `0.5 * np.sum(np.isclose(p, neg))` at line 62, then divides by the pair-comparison count at line 63. These predicates can overlap: a strictly greater positive score that is also `np.isclose` to a negative score contributes `1 + 0.5 = 1.5` to that comparison. V737 `roc_auc` uses strict `>` and exact `==` at line 34; those predicates are disjoint.

This is a static observation about the implementations. It does not establish that any reported V725 comparison enters the overlap, that any published AUC would change, or that a narrow reported finding is invalid. No historical code was edited and no metric was recalculated. It supplies an additional reason to keep source-reported numbers distinct from recertified numerical results; it is independent of the missing native event/owner link and of the calibration-access caveat.

## Source-bound result and scope cautions

The sharper warranted result is:

> For paired synthetic preparations with the same entire initial visible field and shared target, these chosen update laws allow an externally selected restoration parameter to affect later observable trajectories. The supplied trajectory/target computations form scalars without a direct numerical `k` addend; V725 additionally uses high-arm-labelled calibration. This establishes an implemented parameter-to-response mechanism and identifies its information requirements. The reviewed sources do not identify an actual native event, an independent retained owner, or an event/owner-derived value of `k`.

The following statements would exceed the inspected source:

- “Same total initial state”: the displayed field is identical, while `k` and its induced update law differ.
- “Identical additive relaxation noise in V737”: only the underlying standardized draw sequence is coupled; the scale depends on `k`.
- “V725 finalization uses observations alone with no arm information”: its calibration selects `label == 0`.
- “V737 exactly repeats V725's operator and scalar”: the target, update, boundary operator, noise treatment, passive statistics, and metric formula visibly differ. The V737 header's reproduction description is a source claim, not identity of the two programs or certification by this review.
- “Observed parameter sensitivity earns the actual-event/owner link”: this skips the missing upstream identification and sourcing step.
- “The algebra certifies every scalar separation or the published numbers”: update sensitivity is not an injectivity proof for the composite, and no numerical execution was performed.

The V725 Markdown itself limits its claims to an operational scalar, disclaims GR/tensor/real-world conclusions (lines 5–7 and 108–118), and reports numerical tables (lines 59–100). Those numbers and interpretive claims are source-reported material, not newly verified results. This operation check neither reopens the closed charge-diagnostics series nor extends it into quantum, gravitational, or other physical claims.
