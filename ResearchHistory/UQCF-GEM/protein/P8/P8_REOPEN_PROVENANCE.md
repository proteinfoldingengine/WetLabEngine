# Protein P8 — Patch 622/624 historical-mechanism reopen provenance

**Status:** bounded reopen authorized by the P7 reopen rule  
**Branch:** `research/protein-p8-patch622-624-reopen-certification`  
**Parent:** `research/protein-p7-early-backbone-controller-survival`

## P7 reference

- P7 closeout commit: `0e156790b961abdebcd288b333b44c2e6df05d61`
- certified source-audit head: `72c6d464cad50183fd17ac932b40745438576331`
- GitHub Actions run: `35298063514`
- artifact: `10528821674`
- artifact SHA-256: `c34e49c1ce9f23eae00afa2e0f15b25f15509acc275d4372d5e47726ad33f02d`

P7 certified the August-3 StableDAGPhysics source it had recovered. In that source the initial phase governed zero optimizer steps, the fractal term had no coordinate-gradient path, and the only later adaptive coordinate-force addition was contact springs.

P7 explicitly allowed reopening if an exact Patch622/624 raw runner/log showed additional active force switching that contradicted that reduction.

## Newly recovered Drive snapshots

### GlobularFoldQIS
Folder ID: `1kYk-we-NgI_Fbg_BG8IY1InFXnzEkxRU`

| File | Drive ID | SHA-256 | internal label |
|---|---|---|---|
| main.py | `1zibfebFh0-iQMkXZyDoBmdjLNYqUsbNG` | `7c461d6cb91531caf71b78c92e90244ba41b87323748e37c507670fb54ef94b3` | Patch 622.2 Contact Activation Fix |
| dag_engine.py | `1ojCa7wWaqzt9u3etrA8_YLkiVFbxpz8d` | `ee2d2f3148105815e0670b83d7dc62427e4637f732539343943506fe29b9b91e` | Patch 622.1 Configurable Topology |
| force_field.py | `1D82b07r8qjV923QsLpYP8CF-m1Pr10WP` | `69dde0b4a4de06798963c7bc489b13143cb2c5bf70b500fa1b420347f52230ce` | Patch 623.0 Torsional Incoherence Penalty |
| 1ubq_baseline.yaml | `18IgG-0Xci-kC3uTP-_bQTmV99pdA_qpr` | `2d1860bf586a5cb36d67f688aca032b2db262f8f77be4da92dc2aa45a2fe8638` | Patch 623.0 Torsional Incoherence Penalty |
| config_loader.py | `1lkuryf4fBe6q6rTuAOGapZLJuactYVcV` | `bb0abe0c79f6e68a64e0424b7cd0ae1eed412b027ab104ed2d09dc0f756eb100` | config loader |
| metrics_history.py | `1cdpUU8ZD-ZM0plQzjHna1DawkGRomKs9` | `bb5883f08721e2cf0394a3218fe890369eba47d3899ba8704010b886520b0bd6` | Patch 622.0 Betti-Driven Activation |

### StableGlobularQISBest
Folder ID: `1xW0FbrtXCR048VfdS7Hi01QvjTezDljk`

| File | Drive ID | SHA-256 | internal label |
|---|---|---|---|
| main.py | `1lvqWS0m2C2mJ7KhN5PKajurvNXLP6R7-` | `a78b3c638682e206178e6022748d75cab2937de3b737e3c53b3fa9be1dfb0760` | Patch 622.2 Contact Activation Fix; runtime PATCH_ID Patch_625 |
| dag_engine.py | `1soTZT-k6-xIw56JZ-e-guxzvT-Uwoo93` | `1eccbcdd4367db5ee63459e631657e634788387208d113eb7713880b2c08b43f` | Patch 624.1 Force Activation Fix |
| force_field.py | `1CEi0STjaoBYloTn58FfhMduZkm8rBtLg` | `1aa99c3e681c1c9a8c9e591e2c514e3762ed568b2fc5d2725313aa3b97578935` | Patch 624.1 Logging Fix |
| 1ubq_baseline.yaml | `1uvMq1A3YheUTJ1FNt8jDIGtDuqLssA01` | `57d3ff93e1762b54e3495bbd401f29bf9bb236e836af238f0d56544625d0da91` | Patch 625 Torsional Resolution |

## Provenance limitation

These are **mixed historical folder snapshots**, not byte-pure named releases. The internal patch labels differ inside each folder. P8 therefore does not call either folder an exact Patch-622 or Patch-624 release.

The admissible claim is narrower: the colocated runner/DAG/force/config snapshots are immutable historical source artifacts whose executable mechanism differs materially from the StableDAGPhysics source reduced by P7.

## Machine-checked source classification

Local RED was confirmed before the recovered source was supplied: 6/6 P8 tests failed because the required recovered source tree was absent.

After inserting the exact hashed snapshots, local GREEN was confirmed: 6/6 tests passed.

Measured predicates:

- Compaction does not transition at step 0 with Betti1 lifetime 1.
- It remains in Compaction at lifetime 99.
- It transitions to LockIn at lifetime 100.
- GlobularFoldQIS: LockIn - Compaction = contact springs + screened electrostatics.
- StableGlobularQISBest: LockIn - Compaction = contact springs + screened electrostatics + torsional incoherence penalty.
- fractal compaction has a nonzero coordinate gradient in both snapshots; test norm = `0.4999999403953552`.
- screened electrostatics has a nonzero coordinate gradient in both snapshots; test norm = `0.09621811658143997`.
- the later torsional incoherence penalty uses a detached metric scalar for phi_rms and is not promoted here as a coordinate force.
- the runner ordering records Betti history before DAG update, DAG update before force loss, and force loss before backward/optimizer stepping.

## Current classification

```text
P7_STABLEDAGPHYSICS_SOURCE_REDUCTION          REMAINS VALID FOR ITS EXACT SOURCE
P7_PROGRAM_LEVEL_CONTACT_ONLY_GENERALIZATION  REOPENED
DISTINCT HISTORICAL COLOCATED MECHANISM        SOURCE-SUPPORTED
EXACT NAMED PATCH-622/624 RELEASE              NOT ESTABLISHED
HISTORICAL EXECUTION TRACE                     NOT YET RECOVERED
USEFUL NATIVE-BLIND PREORGANIZATION            NOT YET ESTABLISHED
```

No folding GO is inherited from historical performance claims. The next scientific gate is a prospective constrained-backbone reproduction with matched ablations.
