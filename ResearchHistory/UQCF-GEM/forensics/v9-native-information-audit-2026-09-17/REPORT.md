# Protein P0 — Frozen v9 Native-Information / Source-Provenance Audit

**Audit date:** 2026-09-17  
**Audit base:** `f596583615a823a33170588dcbf998bf13f10453`  
**Branch:** `research/protein-p0-v9-native-information-audit`  
**Primary status:** `EXECUTABLE_V9_SOURCE_NOT_PINNED`

## Executive finding

The frozen v9 empirical result remains a bounded, documented protein result, but the current Git-tracked evidence does **not** pin the executable frozen-v9 implementation strongly enough to complete a source-level native-information audit.

The repository preserves:

- the v9 operator at equation / pseudocode level;
- 1UAO and 1L2Y summary/results/statistics/trajectory artifacts;
- trajectory columns for `compat_field`, `dihedral_preserve`, `productive_contact`, `sigma_bridge`, `closure_ready`, `false_closure`, `dir_pen`, `angle_var`, `dihed_smooth`, `soft_contacts`, `density_var`, `rg`, and `loop_compat`;
- the bridge-to-classical handoff packet;
- the final verification dossier and negative branch-family narrowing.

However, the accessible source record does not identify a pinned executable source file / commit implementing the frozen v9 definitions and data flow for the key observables and energy terms. In particular, the audit could not locate an executable definition for the v9 `bridge_observables` path or the internal construction of `compat_field`, `productive_contact`, `dihedral_preserve`, `loop_compat`, `false_closure`, and the exact v9 gating/energy wiring.

Therefore this audit **cannot certify** that frozen v9 is free of native-coordinate, native-RMSD, native-contact-map, or target-specific fitted information.

This is a **provenance failure**, not a falsification of the observed v9 effect.

## Adjudication

```text
formula-level operator documented              YES
cross-target empirical packet preserved        YES
trajectory-level bridge observables preserved  YES
bridge-to-classical handoff preserved           YES
exact executable frozen-v9 source pinned       NO
source-level native-information audit possible NO
native-information non-leakage certified       NO
P1 regularizer-reduction gate ready            NO
```

Primary result:

```text
EXECUTABLE_V9_SOURCE_NOT_PINNED
```

Next required object:

```text
PINNED_EXECUTABLE_FROZEN_V9_IMPLEMENTATION
```

## Why fail closed

The scientific question is not whether the published equations *look* native-free. The question is whether the executable implementation that generated the frozen v9 trajectories used only the documented current-conformation quantities.

A source-level certification requires tracing every path that contributes to at least:

- `compat_field`;
- `productive_contact`;
- `dihedral_preserve`;
- `loop_compat`;
- `soft_contacts`;
- `compactness` / `rg`;
- `false_closure`;
- `sigma_bridge`;
- `closure_ready`;
- the final v9 energy and optimizer / dynamics loop.

Without the exact implementation, the following questions are undecidable from the preserved CSVs and prose alone:

1. Did any term read native coordinates directly?
2. Did any term read native RMSD or an RMSD-derived quantity?
3. Did any term read a native contact map or target-specific contact list?
4. Were any masks, sequence-pair lists, cutoffs, weights, or target-specific constants derived from the native structure?
5. Were v9 parameters fitted using 1UAO, 1L2Y, or other target outcomes in a way that should change the model class?
6. Were the documented equations exactly the executable path used to produce the canonical packet?

The audit therefore refuses to infer `false` for any leakage flag from absence of evidence.

## Search and provenance work performed

The audit searched the connected GitHub evidence for distinctive executable v9 identifiers, including:

- `sigma_bridge`;
- `bridge_observables`;
- `closure_ready`;
- `false_closure`;
- `compat_field`;
- `productive_contact`;
- `dihed_smooth`;
- `uqcf_bridge_patch_v9`;
- the characteristic v9 coefficient structure around `closure` and `compat_field`.

Within `proteinfoldingengine/WetLabEngine`, results resolve to the bridge reports, pseudocode, trajectory packets, CSV artifacts, figures, and publication material rather than an executable frozen-v9 source implementation. The accessible `proteinfoldingengine/UQCF-GEM` code search likewise did not return a `sigma_bridge` implementation.

A commit-history search for v9 / bridge implementation provenance also did not identify a frozen implementation commit.

The strongest internal evidence that the source snapshot remained unfinished is the publication closeout plan itself. Its submission checklist still contains:

```text
[ ] freeze v9 and record commit hash / code snapshot
```

That is consistent with the present audit result: the result packet was preserved, but the exact generating implementation was not frozen into the currently audited source record.

## What remains valid

This P0 result does **not** invalidate the empirical artifacts.

The following bounded statements remain supported by their existing packets:

- frozen-v9-labelled runs on 1UAO and 1L2Y show the previously documented backbone/angle ordering and favorable RMSD movement;
- the final packet records a bridge-to-classical handoff advantage under its reported protocol;
- the v13–v16 contact/routing branch family did not earn promotion over v9;
- v9 remains the historical acceptance baseline for the reduced bridge research program.

What changes is the claim boundary:

> Until the exact generating source is recovered and pinned, v9 should be described as a **reproducible frozen empirical packet with a documented formula-level operator**, not as a source-audited native-free mechanism.

## Consequence for the unified thesis

The Multiscale Realizability Thesis remains a legitimate **hypothesis** because it explicitly separates empirical effect from mechanism distinctness and fundamental derivation.

But Gate P1 — regularizer reduction — should not begin from a reconstructed approximation of v9. A faithful reduction test requires the exact executable v9 implementation so that the controls differ only in the intended hierarchy/gating structure.

Starting P1 from a rewritten implementation would create a new model and would not answer whether the original frozen v9 hierarchy was irreducible.

## Required recovery package

To clear P0, recover and pin all of the following:

1. exact source file(s) that generated the canonical v9 1UAO and 1L2Y packets;
2. exact commit / archive hash or immutable blob identities;
3. exact configuration and parameter set;
4. target input files and sequence / geometry preprocessing;
5. seed protocol and optimizer / dynamics settings;
6. definitions of every bridge observable and every target-dependent mask/list;
7. analysis code used for summary/statistics outputs.

Then rerun this audit and assign explicit booleans to native coordinates, RMSD, native contacts, and target-specific fitting.

## Stop rule

Do not:

- infer non-leakage from the published equations alone;
- recreate v9 from the memo and call it the frozen implementation;
- begin mechanism novelty testing against a guessed implementation;
- use the observed transfer result to waive provenance requirements.

Do:

- preserve the existing v9 empirical evidence;
- recover the exact generator source;
- rerun P0 at source level;
- only then proceed to P1 reduction controls.

## Scientific conclusion

The immediate protein program has produced a useful negative result:

```text
v9 empirical signal:              PRESERVED_BOUNDED
v9 executable provenance:         INCOMPLETE
native-information non-leakage:   NOT_CERTIFIED
mechanism-reduction testability:  BLOCKED
```

The next protein task is no longer another folding run. It is source recovery:

```text
PINNED_EXECUTABLE_FROZEN_V9_IMPLEMENTATION
```

That is the minimum evidence needed to turn the existing v9 result into an auditable mechanistic object.