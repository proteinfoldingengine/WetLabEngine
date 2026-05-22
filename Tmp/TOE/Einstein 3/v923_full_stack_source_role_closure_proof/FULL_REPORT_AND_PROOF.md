# Full Scientific Report and Python Proof: Minimal Source-Role Closure

**Document ID:** V923_FULL_STACK_SOURCE_ROLE_CLOSURE_PROOF  
**Status:** Report-out bundle after V921/V922 stop condition  
**Scope:** Recoverability Accessibility / UQCF-GEM source-legitimacy closure branch  

## 1. Executive finding

The current branch reaches a clean report-out point:

```text
E_OSC closes basin geometry.
Endpoint/path observables define a quotient taxonomy.
Observable-only closure fails.
Binary source-role collapse fails.
A ternary source-role primitive closes exact source legitimacy.
The older four-state source-origin label is over-complete.
```

The minimal exact primitive is:

```text
source_active_role
source_basin_eligible_nonactive_role
source_rejected_or_broken_role
```

The resulting closure is not a 1/f ledger claim, not a physical-time claim, and not a GR/continuum claim. It is a finite, reproducible, source-legitimacy result inside the tested ordered-recoverability simulation branch.

## 2. Why this mattered

Earlier audits showed that a signed-coherence basin can be reached by more than one route. That creates a governance/legitimacy problem:

```text
same endpoint basin
same observable quotient
possibly different source legitimacy
```

The model therefore needed something beyond static basin geometry. The question became whether that missing information could be derived from ordinary ordered-update observables, or whether an additional source-origin primitive was irreducible.

V919 showed ordinary non-label ordered-update observables did not derive the source-origin bit. V920 then proved the full four-state source-origin label was over-complete: exact closure only required a three-state source-role primitive. V921 verified that primitive on a fresh blind regeneration. V922 ablated and stressed it, meeting the stop-and-report condition.

## 3. Formal objects

### 3.1 Basin functional

The basin law remains the signed-coherence energy:

```text
E_OSC = 1/2 D_AC^2 + 1/2(m_AC - c*)^2
```

where:

```text
q = n_psi · n_phi
D_AC = std_J(q)
m_AC = <q>_J
c* ≈ -0.999786375236
```

This functional determines whether the system is in the signed-coherence basin. It does not, by itself, certify how the system got there.

### 3.2 Observable quotient

Endpoint/path observables induce an observable quotient. In the proof data this is represented by:

```text
v921_observable_quotient
```

The quotient compresses observable endpoint/path behavior, but it is source-degenerate.

### 3.3 Source-role primitive

The former four source families were:

```text
active_source
passive_source
structured_source
rejected_or_broken_source
```

The minimal exact source-role primitive reduces them to three roles:

```text
active_source             -> source_active_role
passive_source            -> source_basin_eligible_nonactive_role
structured_source         -> source_basin_eligible_nonactive_role
rejected_or_broken_source -> source_rejected_or_broken_role
```

This is the minimum lift found by exhaustive partition search.

## 4. Dataset and proof input

The full-stack proof script uses the frozen V921 blind cohort:

```text
input file: /mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/v921_ternary_endpoint_scores.csv
rows: 840
source families: active_source, passive_source, rejected_or_broken_source, structured_source
true classes: 7
```

The proof requires only three input columns:

```text
source_family
true_class
v921_observable_quotient
```

All closure, ablation, and partition claims are recomputed from those columns.

## 5. Proof method

The proof script performs five operations:

1. Load the frozen blind endpoint cohort.
2. Evaluate observable-only closure using the observable quotient alone.
3. Exhaustively enumerate all canonical partitions of the four source families into 1, 2, 3, and 4 symbols.
4. For each partition, build a deterministic lookup from `(observable_quotient, source_symbol)` to the majority true class, then measure false cases and collision rows.
5. Stress the certified ternary primitive using random role corruption and targeted role flips.

The exhaustive partition search proves minimality inside this branch because every possible 1-, 2-, 3-, and 4-symbol compression of the four source families is tested.

## 6. Main result: lift ladder

| Lift | Symbol count | Accuracy | False cases | Collision groups | Collision rows |
|---|---:|---:|---:|---:|---:|
| observable_quotient_only | 1 | 0.628571 | 312 | 3 | 662 |
| best_binary_source_role_lift | 2 | 0.916667 | 70 | 2 | 306 |
| ternary_source_role_primitive | 3 | 1.000000 | 0 | 0 | 0 |
| full_four_family_source_lift | 4 | 1.000000 | 0 | 0 | 0 |


Best partition by symbol count:

| Symbol count | Best accuracy | False cases | Collision rows | Mapping |
|---:|---:|---:|---:|---|
| 1 | 0.628571 | 312 | 662 | `{"active_source": "symbol_0", "passive_source": "symbol_0", "rejected_or_broken_source": "symbol_0", "structured_source": "symbol_0"}` |
| 2 | 0.916667 | 70 | 306 | `{"active_source": "symbol_0", "passive_source": "symbol_1", "rejected_or_broken_source": "symbol_0", "structured_source": "symbol_1"}` |
| 3 | 1.000000 | 0 | 0 | `{"active_source": "symbol_0", "passive_source": "symbol_1", "rejected_or_broken_source": "symbol_2", "structured_source": "symbol_1"}` |
| 4 | 1.000000 | 0 | 0 | `{"active_source": "symbol_0", "passive_source": "symbol_1", "rejected_or_broken_source": "symbol_2", "structured_source": "symbol_3"}` |


The first exact closure appears at three symbols:

```text
minimal exact source-symbol count: 3
```

## 7. Stress result

Random role corruption degrades exact classification smoothly, confirming the ternary source-role is information-bearing rather than decorative.

| Noise probability | Mean accuracy | Min accuracy | Mean false cases |
|---:|---:|---:|---:|
| 0.001 | 0.999101 | 0.995238 | 0.755 |
| 0.005 | 0.995339 | 0.988095 | 3.915 |
| 0.010 | 0.991137 | 0.978571 | 7.445 |
| 0.020 | 0.982440 | 0.971429 | 14.750 |
| 0.050 | 0.954107 | 0.933333 | 38.550 |
| 0.100 | 0.909083 | 0.884524 | 76.370 |
| 0.200 | 0.820381 | 0.790476 | 150.880 |


Worst targeted flip:

```text
source_basin_eligible_nonactive_role -> source_active_role
affected rows: 360
accuracy: 0.571429
false cases: 360
```

## 8. What is proven in this branch

```text
1. E_OSC is sufficient to identify signed-coherence basin membership.
2. E_OSC and endpoint/path observables are not sufficient to certify source legitimacy.
3. Observable-only quotient closure fails.
4. Every binary source-role collapse fails.
5. A ternary source-role primitive succeeds with zero false cases and zero collision rows.
6. The full four-state source-family/source-origin label is not required for exact closure.
```

## 9. What is not proven

```text
1. This does not prove a 1/f temporal ledger.
2. This does not use physical time.
3. This does not prove a CMB, black-hole, or cosmological memory claim.
4. This does not prove a unique repair-channel law.
5. This does not prove General Relativity, Einstein equations, physical spacetime curvature, or continuum closure.
```

## 10. Scientific conclusion

The irreducible structure of this branch is:

```text
E_OSC basin law
+ observable quotient
+ ternary source-role primitive
```

This is the cleanest current closure. It avoids the 1/f rabbit hole, avoids overclaiming physical time or GR-like ontology, and gives a concrete minimal information primitive for exact source legitimacy.

## 11. Reproduction instructions

Run the full-stack proof script:

```bash
python /mnt/data/v923_full_stack_source_role_closure_proof/v923_full_stack_source_role_closure_proof.py
```

It writes reproduced artifacts to:

```text
/mnt/data/v923_full_stack_source_role_closure_proof_run/
```

The script can also be run with custom input and output paths:

```bash
python v923_full_stack_source_role_closure_proof.py   --input path/to/v921_ternary_endpoint_scores.csv   --out path/to/output_dir
```

## 12. Files in this bundle

```text
v923_full_stack_source_role_closure_proof.py        full-stack Python proof
FULL_REPORT_AND_PROOF.md                            this report
outputs/                                             reproduced CSV, JSON, and figures
v923_full_stack_source_role_closure_proof.zip        zipped handoff bundle
```
