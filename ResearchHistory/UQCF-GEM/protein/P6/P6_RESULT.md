# Protein P6 — Authoritative Native-Blind Physical Preorganization Result

**Decision:** `NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION`

**Certified scientific head:** `bc00fa3af135219fdf498ed0d271b6a8a649496a`  
**Designated authoritative launch head:** `4866bee47ddecdf9e15daa71d2048854fcf24d80`  
**GitHub Actions authoritative run:** `35299722526` — SUCCESS  
**Authoritative artifact:** `10530595637`, `protein-p6-authoritative-measurement`  
**Artifact SHA-256:** `d0545fb6b70e28b2cfc26799ddc0b308febd69ebfafc0c05dd87e1013c2594ef`

A second frozen-copy run also completed successfully:

- run: `35299731968`;
- launch head: `356f1d6b854570b4efa7485dc7b3c01157299ff6`;
- artifact: `10530735137`;
- artifact SHA-256: `772e697b8e9328a2ee49f092aac939e4e0621d7d090b9f1c0277091c8718c6ab`.

All scientific output files from the two completed runs are byte-identical. Only `p6_run_manifest.json` and the enclosing `SHA256SUMS.txt` differ because the two workflow-only launch commits have different Git SHAs.

## Question tested

P6 prospectively asked whether a covalently exact torsion-space peptide backbone driven only by transparent conventional native-blind physics could produce **sequence-specific native-topology enrichment beyond generic polymer collapse**.

This was a new benchmark, not a rescue of v9, Patch-630, or the P5 TPO entropy mechanism.

The frozen comparison was:

1. real-sequence conventional physics;
2. composition-preserving shuffled side-chain labels;
3. a sequence-independent generic-collapse null matched to the real-sequence nonlocal initial torsional-gradient norm.

Targets were 1VII, 1L2Y and 1UAO, with six deterministic matched seeds per target and three arms, for 54 trajectories total.

Native geometry was evaluation-only.

## Primary pooled result

Mean final fixed-budget top-K long-range native-contact precision:

| arm | pooled mean precision |
|---|---:|
| physical real sequence | **0.2456790123** |
| physical shuffled sequence | 0.1845679012 |
| generic collapse | 0.1074074074 |

The real-sequence arm therefore had the highest pooled primary score.

## Real sequence versus generic collapse

Across the 18 matched target/seed pairs:

- mean precision delta: **+0.1382716049**;
- median delta: **+0.0277777778**;
- wins: **9/18**;
- ties: **6/18**;
- exact two-sided sign-flip p: **0.0166015625**;
- Holm-adjusted p: **0.033203125**.

Target-wise mean precision deltas:

- 1VII: **-0.0185185185**;
- 1L2Y: **+0.0333333333**;
- 1UAO: **+0.4000000000**.

Thus the pooled comparison is statistically favorable to the real-sequence model, but the frozen requirement that the real sequence beat generic collapse on **every target** fails because 1VII moves in the wrong direction.

## Real sequence versus shuffled sequence

Across the same 18 matched pairs:

- mean precision delta: **+0.0611111111**;
- median delta: **0.0**;
- wins: **6/18**;
- ties: **10/18**;
- exact two-sided sign-flip p: **0.1015625**;
- Holm-adjusted p: **0.1015625**.

Target-wise mean precision deltas:

- 1VII: **0.0**;
- 1L2Y: **+0.0166666667**;
- 1UAO: **+0.1666666667**.

Therefore the real-sequence arm does not establish a statistically reliable sequence-order-specific advantage over the composition-preserving shuffle, and the frozen every-target direction requirement also fails because 1VII is tied.

## Anti-collapse gate

Median final real-sequence Rg/native-Rg:

- 1VII: **0.7092399056** — FAIL;
- 1L2Y: **0.6458198689** — FAIL;
- 1UAO: **0.9155532030** — PASS.

The frozen admissible interval was `[0.75, 1.25]`.

Thus the minimal model still over-collapses 1VII and 1L2Y. The primary top-K precision metric prevents that collapse from automatically earning a high contact score, but the physical-sanity gate independently rejects the model.

## Frozen acceptance predicates

| condition | result |
|---|---|
| real sequence highest pooled mean primary precision | PASS |
| real sequence beats generic collapse on every target | **FAIL** |
| real sequence beats shuffled sequence on every target | **FAIL** |
| real vs generic Holm p < 0.05 | PASS |
| real vs shuffle Holm p < 0.05 | **FAIL** |
| real-sequence Rg ratio gate on every target | **FAIL** |
| canonical covalent geometry preserved | PASS |
| all runs numerically healthy | PASS |
| native-information firewall passed | PASS |

Therefore the preregistered decision is necessarily:

```text
NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION
```

## Physical and numerical controls

All 54 runs completed without numerical failure.

Maximum observed covalent reconstruction drift across all runs:

- bond length: approximately `2.0e-15 A`;
- bond angle: approximately `1.33e-15 rad`.

The native-information firewall passed on the exact measurement implementation.

The canonical peptide representation therefore worked as intended; the scientific NO-GO is not caused by backbone-geometry failure.

## Independent verification

The authoritative downloaded ZIP independently hashes to:

`d0545fb6b70e28b2cfc26799ddc0b308febd69ebfafc0c05dd87e1013c2594ef`

which exactly matches the GitHub Actions artifact digest.

Every file hash in the authoritative `SHA256SUMS.txt` independently matches its corresponding archive member.

The following were independently recomputed from raw `p6_results.csv` rather than trusted from `p6_acceptance.json`:

- pooled primary means;
- all target-wise paired deltas;
- both exact `2^18` sign-flip p-values;
- Holm correction;
- target-wise Rg medians;
- geometry and numerical-health predicates;
- the final NO-GO decision.

The independent calculations reproduce the machine-generated acceptance packet.

The second completed workflow copy produces byte-identical scientific data and acceptance output, providing an additional deterministic reproducibility check.

## What is scientifically interesting

The NO-GO is not equivalent to “no signal.”

The real-sequence model:

- has the best pooled primary precision;
- significantly outperforms the generic-collapse null in the pooled matched comparison;
- moves favorably versus generic collapse on 1L2Y and strongly on 1UAO;
- preserves physically exact peptide covalent geometry throughout.

However, those observations do **not** meet the stronger P6 question.

The effect is not robust across targets, is not statistically distinguishable from the composition-preserving shuffled-sequence control, and still produces excessive compaction on two of the three proteins.

The strongest bounded conclusion is:

> The frozen minimal conventional-physics model contains evidence of sequence-dependent behavior beyond a simple matched collapse null, but it does not establish transferable sequence-order-specific native preorganization under the preregistered P6 criteria.

## Decision-path consequence

P6 closes this **minimal model**.

Do not respond to this result by:

- tuning its coefficients after exposure;
- changing the target set;
- replacing the shuffle;
- selecting a favorable checkpoint;
- switching to RMSD or contact recall as a rescue endpoint;
- relaxing the Rg sanity gate.

A future protein-physics gate would require a materially new, independently motivated model or physical ingredient with a new preregistration. It must not be framed as parameter rescue of P6.

The validated scientific assets that remain include:

- target-independent canonical torsion-space peptide geometry;
- native-information firewall;
- matched generic-collapse and sequence-shuffle controls;
- fixed-budget top-K topology endpoint;
- exact matched randomization statistics;
- deterministic CI-backed measurement and artifact verification.
