# UQCF-GEM v13.22 — Quantum Refinement Naturality / Nested-State Law Gate

**Date:** 2026-09-12

## Adjudication

The current ontology does **not** derive a unique quantum refinement law.

There is an exact infinite family of admissible refinements:

`R_tau(rho) = rho tensor tau`

with coarse map

`C = Tr_anc`.

For every fixed faithful ancilla state `tau`, this lift satisfies all presently frozen requirements:
- positivity;
- normalization;
- CPTP refinement/coarse maps;
- exact coarse recovery `C o R_tau = id`;
- retained-observable naturality;
- ETL/PGRL source naturality under `P -> P tensor I`;
- exact two-step compositionality.

Therefore those requirements are insufficient to select one fine completion.

## Exact ETL/PGRL naturality

Because

`log(rho tensor tau)=log rho tensor I + I tensor log tau`

and the two terms commute,

`tilt_s(rho tensor tau, P tensor I)`

factorizes exactly as

`tilt_s(rho,P) tensor tau`.

Fresh executed maximum naturality error:

`5.426e-16`.

So source naturality does **not** break the ambiguity.

## Low-order data do not break it either

Use two full-rank three-qubit ancilla states:

`tau_0 = I/8`

and

`tau_eps=(I+eps Z tensor Z tensor Z)/8`

with `eps=0.4`.

They have identical one- and two-body marginals to numerical precision:

`0.000e+00`.

Yet their hidden three-body information differs.

`CMI(tau_0) = 0.000e+00`

while

`CMI(tau_eps) = 0.0822828785051`.

The corresponding refined global states have trace distance

`0.2`

while both coarse-grain exactly back to the same `rho`.

Thus even demanding the same low-order retained data does not select the refinement.

## RATS anti-circularity theorem

The ambiguity directly affects the sealed continuum experiment.

Choose

`tau_h=(I+epsilon(h) ZZZ)/8`

with

`epsilon(h)=h^r`.

For small `h`,

`CMI(tau_h)=Theta(epsilon(h)^2)=Theta(h^(2r))`.

Executed synthetic controls:

`[{'chosen_hidden_amplitude_exponent_r': 0.5, 'measured_CMI_exponent': 1.0070444141163044, 'asymptotic_expected': 1.0}, {'chosen_hidden_amplitude_exponent_r': 1, 'measured_CMI_exponent': 2.0008403864501925, 'asymptotic_expected': 2}, {'chosen_hidden_amplitude_exponent_r': 2, 'measured_CMI_exponent': 4.000012177281737, 'asymptotic_expected': 4}, {'chosen_hidden_amplitude_exponent_r': 3, 'measured_CMI_exponent': 6.000000183403315, 'asymptotic_expected': 6}]`.

So an unconstrained refinement selector can manufacture different CMI refinement exponents while preserving:
- the same coarse state;
- exact restriction;
- the same retained observables;
- exact ETL source naturality.

Therefore the v13.21 RATS exponent cannot be scientifically interpreted until the hidden refinement completion is selected independently of the desired continuum outcome.

## Executed controls

- coarse restriction error: `1.129e-16`
- retained observable naturality error: `2.220e-16`
- ETL/PGRL naturality error: `5.426e-16`
- two-step composition error: `3.291e-17`
- fine-state distance between admissible lifts: `0.2`
- low-order marginal mismatch: `0.000e+00`

All exact structural controls pass.

## Missing object

This isolates a new typed object:

**QRSL — Quantum Refinement Selection Law**

QRSL must select the hidden fine completion independently of:
- CMI/RATS exponent;
- polar conditioning;
- desired continuum smoothness;
- Einstein/GR target.

Without QRSL, refinement naturality is satisfiable but nonunique.

## Status

- quantum refinement naturality: **SATISFIABLE**
- unique refinement selection: **NO**
- low-order marginal selection: **NO**
- ETL source-naturality selection: **NO**
- compositionality selection: **NO**
- QRSL: **MISSING**
- RATS: **REMAINS SEALED**
- continuum recoverability atlas: **NOT CERTIFIED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major refinement non-uniqueness theorem and anti-circularity result**.

## Next — v13.23

### QRSL Origin / Canonical Refinement Selector Gate

Test only ontology-native candidates:
- Genesis Pin provenance;
- recoverability order;
- retained incidence/filling data already frozen upstream.

Ask whether any of them distinguishes `tau_0` from `tau_eps` without referencing RATS or continuum targets.

If every frozen candidate factors through the coarse state and is therefore blind to the `tau` family, QRSL becomes irreducible relative to the current ontology and this refinement branch should stop until one explicit new axiom is introduced.
