# Atrium restoration: trace from a supplied update to an observed response

Date: 2026-11-13 America/Phoenix / 2026-11-14 UTC.
Status: bounded source assessment and direct algebra, pending independent review. Native receiver delivery **NOT_DERIVED**.

## 1. Why this specific source was inspected

After PR150 settled its fixed-resource charge-channel question, the next target returned to an actual event acting on an independently identified retained owner. The historical Atrium experiment is a concrete lead because it reports an active restoration distinction while passive measurements stay blind. Its existing updater and consumer could, in principle, provide an operation-to-observation trace without constructing another quantum receiver.

This pass inspected exactly three sources: the V725 observable-only report, its Python program, and the V737 reproduction program. It did not search all historical native models, execute either program, replay numerical results, or reopen metric-invariance/GR campaigns. The historical source labels such as "certified" are retained as quotations inside the source transcriptions, not newly endorsed statuses.

Full returned text and provenance are preserved in `source_transcriptions/` and `SOURCE_IDENTITIES.json`. All reads were complete; adding one terminal LF yielded the byte lengths reported by the source metadata. These are **text transcriptions, not authenticated original-byte downloads**. The V737 read reported that it parsed the backing file directly because full-text fetch was unavailable. Length agreement is not a substitute for an original-file checksum.

The source response is real within its specified mathematical construction: the chosen updater depends on k and can produce different visible paths from the same initial field. The question here is whether the source also derives that updater and its owner association from a native event. It does not do so in the inspected files.

## 2. Positive trace through the executable definitions

Line references below refer to the preserved text transcriptions. Neither Python file was imported or executed in this assessment.

| Link | V725 observable-only program | V737 reproduction program |
|---|---|---|
| Input field and target | `make_target` lines 73–82; `make_passive_equivalent_state` 85–92; `perturb_state` 95–102 | `make_target` 45–52; `perturbation` 55–79; initial field in `simulate` 82–90 |
| Capacity choice | `run_assay` 228–279 takes `k_high=0.90`, `k_low=0.25` and selects `(label,k)` arms | `build_dataset` 141–158 sets `high_k=0.82`, `low_k=max(0,high_k-k_gap)` |
| Operation that changes the field | `relax_response` 105–137 directly uses k in the restorative, Laplacian and nonlinear terms | `simulate` 82–90 directly uses k in the force and noise amplitude |
| Existing consumer | `compute_metrics` 140–178 reads target and trajectory; `finalize_metric` 195–225 combines metrics | `metrics_for_run` 93–138 reads target and trajectory and combines metrics |
| Calibration/read access | `zscore_from_admissible` 181–186 selects label-zero values; normalization uses the supplied dataset | No `adm_z`; target and trajectory remain explicit metric inputs |

The inputs and outputs are numerical arrays, scalar configuration parameters, random-draw schedules, trajectories, and computed metric records. The scripts do not supply a mapping from a same-Genesis pruning record to k or to the chosen evolution law. They do not identify the array with an independently named retained owner's state or grant that owner the program's read access to target and trajectory. The name "retained atlas field" in a docstring is not such a map.

An experimenter can legitimately choose a perturbation, know a target and measure a trajectory in a synthetic assay. Those permissions must not silently become native owner-available observations. An independently justified non-Hilbert owner and one local effect could suffice; a separate qubit receiver or this entire composite metric is not required.

## 3. V725: exactly where the active contrast enters

Let x be the common perturbed field, t the common target, eta the shared additive noise at one update, and L the discrete Laplacian implemented by `relax_response`, including its one-sided endpoint entries. In real arithmetic its update is

\[
 F_k(x;t,\eta)=x+k(t-x)+0.06kLx
       +0.015(1-k)\tanh(Lx)+\eta. \tag{1}
\]

Tanh acts componentwise. For a common input field and common target/noise, with `Delta k=k_high-k_low`, direct subtraction gives

\[
 F_{k_h}(x;t,\eta)-F_{k_l}(x;t,\eta)
 =\Delta k\big[(t-x)+0.06Lx-0.015\tanh(Lx)\big]. \tag{2}
\]

This is the exact first-update route by which a chosen capacity contrast can enter the visible field, without putting a direct k term inside the observable-only final score. The bracket can vanish; equation (2) is not a theorem of nonzero response for every input or of any AUC value. Later trajectory differences require propagating different states and are not given by this common-state identity alone.

`run_assay` makes x_pert, target and noise_schedule once for each pair and passes them to both k arms. `relax_response` copies its start. Therefore the complete visible starting field is identical between the paired runs, and the additive noise schedule is identical in V725. The program configuration still differs in k. Equality of the field, or of its passive summaries, is not equality of every hidden model parameter or a proved equality of a physical receiver's complete initial restriction.

The source report's statement "only k changes" refers to this controlled synthetic comparison. It does not derive k from retained order, P1, a native source event or an owned action. The first unsupported correspondence for the proposed native trace is the connection of an actual event and its native record to **this** F_k acting on **this** independently identified owner. Deriving a scalar k alone would not automatically justify the remainder of the update law or its access assumptions.

## 4. V737: common seed is not common additive noise

V737 uses the same target and perturbation within a pair, starts each arm at `x=t+0.55*pert`, and initializes a new RNG from the same pair_seed for each arm. Let L_0 denote its `second_diff`, whose two endpoint entries are zero. Its real-arithmetic one-step stochastic model can be written

\[
 G_k(x;t,z)=x-0.20k(x-t)-0.030kL_0x-0.010x
             +(0.012-0.005k)z, \tag{3}
\]

where z is the common standardized Gaussian draw. This expression interprets the code's normal draw through its location/scale parameterization; it is not a new bit-for-bit replay claim about any software version.

At a common x,t,z,

\[
 G_{k_h}(x;t,z)-G_{k_l}(x;t,z)
 =\Delta k\big[-0.20(x-t)-0.030L_0x-0.005z\big]. \tag{4}
\]

Thus the changed k affects both deterministic restoration and the additive-noise amplitude. Same pair_seed shares the underlying standardized draws in the model; it does **not** make the added noise vectors equal when the amplitudes differ. A k-dependent stochastic amplitude is not direct k leakage into the scalar formula, and is not inherently an invalid experiment. It is part of the supplied response law and must be disclosed when comparing mechanisms or interpreting the signal.

The V737 program uses different force coefficients and Laplacian sign/boundary convention, noise law, target/perturbation construction and scalar from the inspected V725 program. It describes its purpose as synthetic reproducibility. It is not an exact replay of those V725 trajectory bytes. This observation does not refute an intended qualitative robustness demonstration; no such numerical claim is reproduced or recertified here.

## 5. What the observer formula does and does not establish

V725 separates its `g_atrium_observable_only` from an explicitly marked `g_atrium_with_k_oracle`. Direct k is absent from the former formula and present in the latter control. However, its `adm_z` is computed relative to the label-zero/high-capacity arm, and its min/max normalizations use the supplied metric dataset. Its raw restoration quantities also use target and trajectory arrays. The normalization therefore includes a specified reference/calibration procedure. That can be legitimate calibration; its existence is not a proof that an independently identified native owner can perform it.

V737 removes `adm_z` and omits direct k and labels from the expression for `atrium_scalar`. It still reads the known target and the generated trajectory. This is a meaningful distinction between the two metric implementations, but neither program derives native readout permission or the production of a receiver-owned record by an actual event.

Both programs make the initial visible field the same within each pair. Their respective passive metrics are deterministic functions of shared initial inputs, so the paired values are identical by construction. This is a useful controlled baseline for testing a hidden dynamical parameter. It is not evidence of an earned native source-to-owner correspondence, and it must not be promoted into an independent complete-initial-blindness theorem for a physical receiver.

No source-to-W_R/W_E map is supplied by these programs, so this assessment assigns no W_R/W_E pass/fail score. Nor does it replace the operational receiver by the whole array or by a program that has unrestricted access to all simulation variables.

## 6. Separate static AUC implementation caveat

V725's `auc_score`, lines 51–63, sums `p > neg` and `0.5*np.isclose(p, neg)` for each positive score p. These predicates need not be disjoint. Whenever p is strictly greater than a negative score and also considered close, that comparison contributes `1+0.5=1.5`. This is not a consistent Mann–Whitney win/tie contribution for that case. V737's `roc_auc`, lines 27–34, uses strict greater-than plus exact equality, whose cases are disjoint for finite scores.

This is a bounded source-code caveat, not a numerical finding about the published dataset. No comparison records were replayed to determine whether the overlap occurred, how often it occurred, or whether any reported AUC would change. It does not by itself invalidate the supplied k-dependent update or establish that the active/passive separation disappears. Historical source code is preserved unchanged; no correction or re-certification is claimed. Any future use of the affected V725 routine needs a separately verified comparator before relying on newly calculated AUCs.

## 7. Disposition and next admissible input

The positive conditional mechanism is now explicit: a supplied k selects a supplied array update, and an existing software consumer reads the resulting path. Equations (2) and (4) locate the first-update dependence, including the V737 noise channel. None of this requires a new decoder or a newly invented receiver register.

The inspected source does not derive the desired native operation-to-owner binding. No native premise moves from SUPPLIED to DERIVED. Actual atemporal measurement/pruning occurrence remains ACCEPTED INPUT; this assessment adds no demand to explain why events occur. The missing correspondence is which actual event implements an inherited operation that changes one identified owner's available source-dependent effect.

Re-entry on this lead requires a specific inherited construction that derives an appropriate operation and binds its affected field/local effect to a retained owner before response outputs are selected. A justified alternate operation or carrier remains eligible. Complete field tomography, this scalar, a unique generator, global synchronization, physical time or a full theory of gravity are not necessary new hurdles.

The source trace stops here. Do not launch another k sweep, tune coefficients, create an owner label, call a metric read a native observation by definition, or repeat these source readings without new relevant evidence. Historical active-restoration mathematics remains scoped to its supplied synthetic law; it is not converted into a physical signal or an archive-wide impossibility result.
