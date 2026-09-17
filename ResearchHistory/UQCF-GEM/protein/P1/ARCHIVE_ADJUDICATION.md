> **P1 status correction (2026-09-17): ARCHIVE EVIDENCE ONLY.** The recovered CSVs below are retained as historical context, not as the prospective P1 acceptance measurement. Their exact historical generator is not source-certified, so any GO/NO-GO wording below is restricted to that archive packet and must not be promoted to the current P1 result. The prospective P1 result requires the frozen source identity, deterministic implementation, matched seven-control matrix, and bound inputs in this branch.\n\n# Protein P1 — Regularizer-Reduction Adjudication

**Date:** 2026-09-17  
**Branch:** `research/protein-p1-v9-regularizer-reduction`  
**Prospective core GREEN head:** `35a9d99e7530a263e296dcd80b4854dea438d93b`  
**GREEN GitHub Actions run:** `35278659190`  

## Executive result

The recovered archive contains stronger completed controls than were visible when P1 was opened. Those controls are sufficient to split the original P1 question into two parts:

```text
P1-A: Are live sigma_bridge / closure_ready gates necessary?
Result: NO-GO.

P1-B: Does frozen v9 outperform simpler preconditioning controls on a harder topology?
Result: NO-GO for distinct v9 superiority on the archived 1VII discriminator.
```

This does **not** mean the protein-side preconditioning effect is empty. The same packets show a large, repeatable advantage over the minimal classical baseline. The narrower conclusion is that the evidence does not require the special live compressed bridge state to explain that advantage.

## P1-A — live-gate necessity

The archived 1VII fixed-gate ablation used constants estimated from prior frozen-v9 traces on 1UAO and 1L2Y:

```text
sigma_const   = 0.1956
closure_const = 0.0393
```

Six matched seeds compared classical-only, live-v9 preconditioning, and fixed-gate preconditioning followed by the same classical relaxer.

### v9 versus classical-only

| Metric | v9 - control | paired p |
|---|---:|---:|
| best RMSD | -2.1740 Å | 0.025439 |
| angle RMS | +0.0454 | 0.048286 |
| dihedral RMS | +0.0547 | 0.287835 |
| contact recovery | +0.4032 | 0.002012 |

The preconditioning effect is real relative to this baseline.

### v9 versus fixed-gate preconditioning

| Metric | v9 - fixed gate | paired p |
|---|---:|---:|
| best RMSD | +0.0202 Å | 0.693795 |
| angle RMS | -0.0009 | 0.946963 |
| dihedral RMS | +0.0729 | 0.013337 |
| contact recovery | +0.0158 | 0.109867 |

There is no v9 advantage in RMSD, angle RMS, or contact recovery; fixed-gate is significantly better on dihedral RMS.

Therefore:

```text
LIVE_COMPRESSED_GATE_NECESSITY = NO_GO
```

The archived result is inconsistent with the proposition that live `sigma_bridge` / `closure_ready` compression is required for the observed preconditioning benefit.

## P1-B — harder-topology bridge discriminator

A separate 1VII discriminator compared:

- classical-only;
- v9 preconditioning;
- dihedral-only preconditioning;
- static-combo preconditioning.

Mean outcomes over six seeds were:

| Protocol | best RMSD | angle RMS | dihedral RMS | contact recovery |
|---|---:|---:|---:|---:|
| classical-only | 9.2515 | 0.7520 | 1.8245 | 0.3671 |
| dihedral-only | 6.7753 | 0.8212 | 1.7836 | 0.7185 |
| static-combo | 6.7919 | 0.7810 | 1.7974 | 0.7162 |
| v9 | 6.8609 | 0.8058 | 1.8461 | 0.7230 |

The archived paired statistics report:

### v9 versus dihedral-only

| Metric | v9 - control | paired p |
|---|---:|---:|
| best RMSD | +0.0856 Å | 0.188543 |
| angle RMS | -0.0153 | 0.572890 |
| dihedral RMS | +0.0625 | 0.417212 |
| contact recovery | +0.0045 | 0.771111 |

### v9 versus static-combo

| Metric | v9 - control | paired p |
|---|---:|---:|
| best RMSD | +0.0690 Å | 0.029610 |
| angle RMS | +0.0248 | 0.252655 |
| dihedral RMS | +0.0487 | 0.562102 |
| contact recovery | +0.0068 | 0.562313 |

Positive RMSD differences are worse. Thus v9 is significantly worse than the static-combo control on best RMSD in this packet and has no compensating significant advantage on the other endpoints. It also has no significant advantage over the dihedral-only preconditioner.

Therefore:

```text
DISTINCT_V9_SUPERIORITY_ON_1VII = NO_GO
```

## What survives

The result does **not** support saying “v9 does nothing.” It supports a more specific interpretation:

1. A geometry-based preconditioning effect exists relative to the minimal classical baseline.
2. That effect transfers to 1VII in the archived experiments.
3. The evidence does not isolate the live compressed bridge state as the causal ingredient.
4. Simpler coarse-grained/static biases reproduce the main downstream benefit and can equal or outperform v9.

The scientifically defensible surviving object is therefore closer to:

> a generic coarse-grained geometric preconditioning effect

than to:

> a uniquely demonstrated live multiscale bridge-state mechanism.

## Consequence for the Multiscale Realizability Thesis

The broad hypothesis that geometric preorganization can change accessible downstream structure remains viable. The stronger v9-specific thesis is narrowed:

```text
geometry-based preorganization effect        SUPPORTED_BOUNDED
live sigma/closure compression necessary     NOT_SUPPORTED / NO_GO
v9 superior to simple biases on 1VII         NO_GO
protein-specific folding law                  NOT_ESTABLISHED
fundamental UQCF derivation                   NOT_ESTABLISHED
```

This is scientifically useful negative narrowing. It prevents the program from mistaking one implementation detail for the underlying phenomenon.

## Provenance boundary

The four archived CSV files copied into this directory were recovered from the connected file Library. Their bytes are preserved here with SHA-256 identities:

- `archive/uqcf_1vii_bridge_discriminator_results.csv` — `639051f168ccd6ccaed478c33c92670a988ed39b994ef3fa0909ddcfa986a4a2`
- `archive/uqcf_1vii_bridge_discriminator_stats.csv` — `05fdb722521d1bd93ee3b0057a2c8dbe29162415354cc4b08d4c6b756dc5488f`
- `archive/uqcf_1vii_fixed_gate_ablation_results.csv` — `ec85d4ab7658492d71d7f7f3e0c04da99b6ec3cad0a8c1b40e6b501aa7e73aa6`
- `archive/uqcf_1vii_fixed_gate_ablation_stats.csv` — `34f1a9bc0d42e69fb4646591b4d2b43baee77410000e510e88a1e08e3b4656a0`

The exact historical generator source for these packets is not yet pinned. Therefore this adjudication treats them as recovered executed-result artifacts, not as a source-certified rerun.

The prospective P1 deterministic core remains useful as a clean future reproduction harness, but the archive already answers the mechanism-necessity question strongly enough that another immediate run would be redundant.

## Stop / proceed decision

**Stop:** further v9 coefficient tuning, live-gate refinements, and attempts to establish novelty from `sigma_bridge` / `closure_ready` themselves.

**Proceed only if the scientific question changes.** The two high-value directions are:

1. characterize whether the surviving generic geometric preconditioning effect adds anything beyond established coarse-grained/polymer regularizers; or
2. return to the independent older full-backbone/TPO lineage, whose torsional/backbone hypotheses are not tested by this P1 result.

For advancing protein-folding science rather than preserving v9 as an implementation, the second direction now has the higher upside.
