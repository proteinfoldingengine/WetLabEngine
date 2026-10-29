# A physical counterpart, with a different event law

Author: proteinfolding-gpt. Date: 2026-10-29 America/Phoenix.
Research baseline: c5cefae1b1dd8d877d1a919c27f4196eb150e353.
Status: bounded primary-source assessment; Class C; UNREVIEWED. Native bridge NOT_DERIVED.

## Concrete finding

Linpeng et al. measured a transmon–cavity system with dispersive Z readout and a driven X Hamiltonian. Output-field I/Q records yielded spectra separating the two X-eigenstate preparations. The resolved-shift regime is explicitly nonideal. Reflected photons are inaccessible, and exact total energy balance is obtained in an idealized simulation. Drive-off photon-number calibration uses Ramsey coherence and an assumed exponential relation.

Source: Xiayu Linpeng et al., *Quantum energetics of a noncommuting measurement*, Physical Review Research 6, 033045 (2024), [DOI](https://doi.org/10.1103/PhysRevResearch.6.033045), sections II–V, Appendices A–B, Figures 2–4. These are the paper's reported results; no raw-data reproduction is claimed.

This locates an existing physical carrier, state-sensitive output field, and recorded observation. It does not identify that experiment with the exact source-pruning instrument in our note.

## Comparison with the archived construction

The [source-generator construction](https://github.com/proteinfoldingengine/WetLabEngine/blob/e317784d620e5409194d20bc0737a09f84f9917f/ResearchHistory/UQCF-GEM/research/physical-bridge/source_generator_composition/NOTE.md) assumes a specific source operation. On its rank-one initial generator eigenspace it derives

    L = (1 - q^2)/2,
    L_z = (1 - z q)/2.

Those are exact consequences of that operation, not universal consequences of obtaining a source-outcome label. The equal-effects control in [6488925960](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6488925960) remains decisive: for K = X, Q = Z, psi = |+>, the Kraus families A_z = |z><z| and B_z = |+><z| have the same effects and source probabilities, but produce leakage 1/2 and 0 respectively. Direct multiplication verifies both claims.

Our comparison therefore has three separate conclusions:

1. **Physical accessibility example:** a measurement's consequence can reach a specific existing field record. This is established physics reported by the external source, not a UQCF-GEM discovery.
2. **Exact event correspondence not established:** matching the symbols X and Z does not identify an actual instrument with A_z, transfer the exact leakage law, or establish repeatability. The cited experimental regime cannot be silently replaced by the ideal operation.
3. **Native correspondence not established:** the actual apparatus, coupling, drive, preparation, and receiver are external empirical structure. No producing operation in the inherited Genesis/P1 stack has been identified with them. Laboratory pulse durations supply no fundamental time variable to UQCF-GEM.

The spectral distinction above compares two physical source preparations. It is not the event/no-event comparison on one input used in our archived note. Neither comparison may be substituted for the other without a new derivation.

## Receiver check for the exact ideal candidate

Here is that check, under an explicit conditional system–apparatus model. Let the same isometry V implement the exact one-qubit channel Delta_Z for every input, with an apparatus initially in a fixed state independent of the preparation. Purify that apparatus state if necessary; an actually accessible receiver is a subsystem of the resulting environment E. These are SUPPLIED quantum implementation assumptions, not a native construction.

Because Delta_Z fixes each pure state |z><z|, purity of the reduced output forces

    V|0> = |0>|e_0>,  V|1> = |1>|e_1>.

Since Delta_Z(|0><1|) = 0, tracing V|0><1|V^dagger over E gives <e_1|e_0> = 0. Tracing the same joint output over the source instead gives, for every input rho,

    sigma_E(rho) = rho_00 |e_0><e_0| + rho_11 |e_1><e_1|.

Thus |+x> and |-x> give exactly the same complete environment state, and hence the same state on every receiver subsystem of it. No environment-only observation distinguishes this pair under these assumptions. This covers every fixed isometric implementation of the exact channel, not just a chosen copying circuit.

The equality already follows from fixing both source basis states; environment orthogonality is unnecessary for it. The same pair therefore remains environment-blind for partial Z dephasing with nonorthogonal pointer states. Merely reducing measurement strength cannot provide this missing contrast.

The control is essential: for exact Delta_Z, inputs |0> and |1> do give orthogonal environment states. The result does not say that ideal pruning never transfers a distinction. It says that this particular equal-Z-population pair does not transfer its X distinction to the environment alone. Their joint source–environment states can still differ.

Consequently, using the observed field contrast as the receiver for our exact Delta_Z calculation would require an additional, justified part of the implemented operation. That is a concrete mismatch, not merely a missing name for the receiver. The archived leakage identities remain valid; they never asserted this environment contrast. This elementary argument is author-checked and unreviewed, with no mathematical novelty claim.

## Disposition and bot handoff

Preserve this as one external physical comparison; do not turn it into a detector-design, calibration-fitting, or simulation campaign. It supplies a concrete example of what a complete physical record chain looks like. It removes no currently supplied native premise.

T-213/T-214's v15.12 carrier remains parked. I independently inspected simulation.py lines 43–51 (blob 19798d70e13361d1e9879c118b66b31e60fcdeef) and README line 36 (blob f15c64f13e05582061b408cfe19ce6839bf703c8): their explicit supplied-input status stands. Those are different sources from the external experiment and must not be combined as one derived carrier.

Further work on this route requires an inherited producer identifying the actual operation and owned record, or independently characterized instrument evidence that supports a clearly scoped empirical correspondence. A further commutant calculation cannot provide either. No historical numerical replay, Gemini verdict, merge, or milestone is claimed. P1 and PR123 are unchanged.
