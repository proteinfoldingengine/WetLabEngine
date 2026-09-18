# Protein GO/NO-GO Program — Continuation Decision

**Decision date:** 2026-09-17  
**Repository:** `proteinfoldingengine/WetLabEngine`  
**Historical evidence archive merge:** `fae90c62ea4edee9df1c552c170dc8261dda2bb2`  
**Current evidence baseline:** `ca3f0e062c5f28ff048fa01de5915f0990b16007`

## Program decision

```text
NO_GO_OPEN_ENDED_CUSTOM_PROTEIN_MECHANISM_DEVELOPMENT
RETAIN_VALIDATED_BACKBONE_INFRASTRUCTURE
```

The present protein-mechanism program has reached a stopping point on the evidence currently in hand.

This is not a claim that torsional information, backbone constraints, geometric regularization, or physics-based protein modeling are unimportant. It is a decision that the specific recovered custom mechanisms tested in this program have not earned additional open-ended development.

## Evidence chain

### P0 — provenance boundary

The exact historical April-2026 v9 generator remains provenance-unresolved.

The repository preserves the narrower conclusions:

- `CANONICAL_V9_GENERATOR_PROVENANCE_UNRESOLVED`
- `V9_REPRODUCTION_SOURCE_RECOVERED_AND_AUDITED`

P0 therefore prevented retrospective historical claims from being treated as prospectively certified source-level evidence.

### P1 — hierarchical-v9 mechanism discrimination

**Decision:** `NO_GO_HIERARCHICAL_ADVANTAGE`

- authoritative measurement head: `f38cce040c98b78f4300ace06f28c350e4e4c313`
- GitHub Actions run: `35288146185`

The recovered v9 construction did not establish a distinct advantage over simpler information-matched regularizers under the frozen prospective test. In particular, the live state-dependent hierarchy did not outperform the frozen-gate control strongly enough to justify v9-specific mechanism development.

### P4 — historical physical-backbone validity

**Decision:** `NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION`

- certified scientific head: `cd14868c6bb7865a4d6c13c0579a07b72581d60c`
- GitHub Actions run: `35292391335`
- artifact: `10526897177`

The recovered Patch-630 Cartesian representation did not maintain declared peptide connectivity. Therefore the historical low torsional-dispersion result cannot be promoted as evidence of physically valid backbone organization.

The historical numerical replay remains a valid computational reproduction within its original representation; the physical interpretation is what fails.

### P5 — constrained-backbone TPO survival

**Decision:** `NO_GO_TPO_ENTROPY_INCREMENT`

- pre-exposure contract certification head: `c65e7aa06fe06048dd8d5499539e51c0a5dd3b44`
- pre-exposure contract run: `35294941990`
- authoritative measurement head: `8adfdc161645c32a8ae7f2bcacbdb3fd78b32780`
- authoritative measurement run: `35295009294`
- result-record head: `889067f181f3bc770c77bdbe03afdb358df0ffeb`
- post-result contract certification run: `35295660706`
- authoritative artifact: `10528211747`
- artifact SHA-256: `cf64c0ea1e7356c72898b60c76e6910639bf6c70cb35ee041d5ded8951663e6b`

P5 replaced the invalid Cartesian historical representation with a covalently constrained kinematic peptide backbone and tested the recovered TPO entropy observable prospectively against preregistered conventional controls.

The constrained representation remained physically valid, but the TPO entropy candidate did not improve the frozen primary endpoint and failed the preregistered target-wise and statistical conditions.

This closes TPO-entropy-specific continuation on the present evidence.


### P6 — native-blind physical preorganization

**Decision:** `NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION`

- certified scientific head: `bc00fa3af135219fdf498ed0d271b6a8a649496a`
- authoritative launch head: `4866bee47ddecdf9e15daa71d2048854fcf24d80`
- authoritative measurement run: `35299722526`
- authoritative artifact: `10530595637`
- artifact SHA-256: `d0545fb6b70e28b2cfc26799ddc0b308febd69ebfafc0c05dd87e1013c2594ef`
- result-record head: `d1e159e226fb755e8d017564a9ca1f396eb8de9a`
- post-result certification run: `35303421027`
- archive merge: `ca3f0e062c5f28ff048fa01de5915f0990b16007`

P6 was deliberately independent of the failed historical mechanisms. It tested a target-independent canonical peptide backbone with ordinary native-blind sterics, local Ramachandran preference, directional backbone hydrogen bonding, sequence-dependent hydropathy and screened electrostatics against a composition-preserving shuffled-sequence control and a gradient-matched generic-collapse null.

The result contains a bounded partial signal:

- the real-sequence arm had the highest pooled fixed-budget native-contact precision;
- the real sequence beat generic collapse in the pooled matched comparison after Holm correction;
- 1UAO showed a strong favorable real-sequence effect.

But the preregistered transfer claim failed because:

- 1VII did not beat generic collapse;
- the real sequence did not beat the shuffled-sequence control on every target;
- the real-versus-shuffle comparison was not statistically significant;
- 1VII and 1L2Y failed the anti-collapse Rg gate.

The larger targets also lost native-contact precision relative to their matched randomized starting ensembles, whereas 1UAO improved. This is not transferable physical preorganization.

P6 therefore closes the tested minimal conventional-physics model. The result does not justify post-exposure coefficient tuning or adding familiar force-field terms merely to rescue the endpoint.

## What is closed

Do not continue, on the current evidence, with:

- v9 live-gate coefficient tuning or hierarchy refinements;
- attempts to rescue the Patch-630 Cartesian backbone as physically meaningful;
- post-exposure retuning of the recovered TPO entropy term;
- seed removal, target substitution, alternate-endpoint rescue, or coefficient search intended to reverse a frozen NO-GO;
- broad force-field expansion whose purpose is primarily to keep one of the failed custom mechanisms alive;
- another historical replay whose only purpose is to restate an already-bounded historical result;
- post-exposure tuning or endpoint rescue of the P6 minimal conventional-physics model;
- open-ended addition of standard solvation, side-chain packing, or many-body terms merely to convert P6 into an existing-style coarse-grained force field.

## What survives

The following remain useful scientific and engineering assets:

1. provenance-first historical reconstruction;
2. deterministic matched-control experiment design;
3. corrected Kabsch C-alpha RMSD evaluation;
4. exact paired sign-flip tests and frozen multiplicity handling;
5. source- and artifact-hash certification;
6. physically constrained differentiable peptide-backbone kinematics;
7. native-blind optimization/evaluation separation;
8. CI-backed RED/GREEN and authoritative-measurement workflow patterns;
9. target-independent canonical peptide geometry;
10. composition-preserving sequence-shuffle and gradient-matched collapse controls;
11. fixed-budget topology metrics designed to resist over-collapse artifacts.

These assets can support future protein work, but they do not themselves establish a novel folding mechanism.

## Reopening rule

The custom-mechanism line should be reopened only for a materially new scientific reason, not because a previous gate was unfavorable.

Examples of sufficient reopening evidence would include:

- recovery of an immutable historical source artifact that materially changes the mechanism actually being tested;
- an independently motivated mechanism not reducible to the failed v9 or TPO observables;
- an external dataset or experiment that makes a new falsifiable prediction available before tuning;
- a prospectively specified physical term with a clear baseline/control family and held-out transfer test;
- independent experimental evidence that specifically distinguishes the proposed mechanism from conventional geometry or statistical regularization.

Any reopened program should begin with a fresh preregistration and should not inherit a GO from historical performance claims.

## Decision-path consequence

The protein GO/NO-GO program has done what it was designed to do: distinguish preserved historical observations from mechanisms that survive controlled prospective testing. P6 extended that discipline beyond the historical mechanisms and showed that the retained backbone infrastructure can support a clean native-blind physics benchmark, but the tested minimal model still did not earn a transferable sequence-specific preorganization claim.

The current decision is therefore:

```text
STOP mechanism-specific open-ended development.
PRESERVE the evidence.
RETAIN the validated constrained-backbone and measurement infrastructure.
REOPEN only on materially new, prospectively testable evidence.
Do not launch P7 merely to tune P6 or recreate an established coarse-grained force field.
```
