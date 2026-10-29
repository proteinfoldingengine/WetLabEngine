# Source pruning and the existing generator-sector law

Author: proteinfolding-gpt. Date: 2026-10-28 America/Phoenix.
Baseline: c5cefae1b1dd8d877d1a919c27f4196eb150e353.
Status: author-side analytical derivation, UNREVIEWED. Native bridge NOT_DERIVED.
Admission: **Class C for the present physical target**. The operations below already occur in the archived conditional model; their actual enactment and receiver ownership are still supplied. This is a brief composition check, not a new verification campaign or a claim of native progress.

## Positive construction

The archived v9.33 generator pinching fixes the starting generator eigenstate. That does not make its spectral record uninformative after the different, source-derived pruning in v9.34. Compose those two existing structures before inventing another observable.

The resulting calculation gives an exact possible observation law, including for each selected source outcome. It does not identify a physical detector or show that an existing receiver writes the outcome.

## Premises and provenance

1. A finite-dimensional carrier, a Hermitian generator K with distinct eigenvalues mu and spectral projectors Pi_mu, and a normalized state psi with K psi = lambda psi — INHERITED WITHIN THE ARCHIVED CONDITIONAL MODEL, v9.33 section 5. The archived ensemble uses generator eigenstates. Their realization by native Genesis/grade preparations is not earned here.
2. A distinguished qubit source observable Q, extended by the identity on the exterior, with Q = Q^dagger and Q^2 = I — INHERITED WITHIN THAT MODEL, v9.34, Exact source-reduction theorem. Put q = <psi|Q|psi>.
3. The source projectors P_z = (I + z Q)/2, z = +/-1, and the mathematical source reduction Delta_Q(A) = sum_z P_z A P_z = (A + Q A Q)/2 — the existing v9.34 operation. Identification with the actual pruning event remains SUPPLIED, not derived from occurrence alone.
4. The existing generator pinching E_K(A) = sum_mu Pi_mu A Pi_mu — v9.33 section 5. Its spectral probabilities are the usual conditional-model law Tr(Pi_mu A). Physical availability of that spectral observation, its outcome instrument, and receiver ownership are NOT established.
5. Rank(Pi_lambda) = 1 — EXPLICIT ADDITIONAL CONDITION for the scalar formulas below, not a theorem about every native generator. The general formula does not need it.
6. Actual measurement occurrence — ACCEPTED INPUT under DIRECTION_UPDATE_2026_10_21 section 2. No trigger, clock, universal completion, or privileged ordering is being derived.

K and Q are fixed before evaluating the consequence. No spectral projector is fitted to a desired separation. Mathematical specification still does not establish measurement availability.

## Exact deduction

Write rho = |psi><psi|. Before source pruning the generator-sector law is concentrated at lambda. After the nonselective source operation,

    p_mu = Tr(Pi_mu Delta_Q(rho))
         = (delta_(mu,lambda) + ||Pi_mu Q psi||^2)/2.        (1)

This follows by substituting Delta_Q(rho) = (rho + Q rho Q)/2. The probabilities sum to one because the Pi_mu resolve the identity and ||Q psi|| = 1. Applying E_K afterward preserves these same probabilities.

The probability outside the initial generator eigenspace is therefore

    L = 1 - p_lambda
      = ||(I - Pi_lambda) Q psi||^2/2.                    (2)

For the nondegenerate case in premise 5, Pi_lambda Q psi = q psi, so

    p_lambda = (1 + q^2)/2,
    L = (1 - q^2)/2.                                      (3)

Thus |q| < 1 forces a different generator-sector probability law under the stated correspondence. Its total-variation distance from the original point mass at lambda is L. This is an outcome-probability calculation for a fixed pre-existing spectral family, not merely a norm difference between two density matrices.

### One selected source outcome

This distinction need not be inferred only from a nonselective average. A source outcome z has weight

    w_z = <psi|P_z|psi> = (1 + z q)/2.

For w_z > 0 its normalized branch state is rho_z = P_z rho P_z / w_z. Under premise 5,

    Tr(Pi_lambda rho_z)
      = |<psi|P_z|psi>|^2 / w_z
      = w_z,
    L_z = 1 - w_z = (1 - z q)/2.                          (4)

When |q| < 1, every positive-weight source outcome has L_z > 0. No favorable source outcome is selected to manufacture the consequence. Averaging gives sum_z w_z L_z = (1 - q^2)/2, as in (3). Equation (4) remains conditional on the actual event being this selective instrument; it does not derive actual-outcome selection. There is no uniform positive lower bound over all |q| < 1.

## Analytical controls

- **Positive control, and no extra nonselective change required:** K = X and Q = Z for the Pauli matrices, psi = |+>, lambda = 1. Source pruning gives I/2 and a subsequent K-sector law (1/2, 1/2). E_K(I/2) = I/2: the possible outcome distinction does not require E_K itself to change this post-state. A possible outcome law is not an already written classical record.
- **Degeneracy matters:** K = Z tensor Z, Q = Z tensor I, psi = (|00> + |11>)/sqrt(2), lambda = 1. Here q = 0, but both source branches remain in the same two-dimensional lambda eigenspace. Equation (2) gives L = 0. Using (3) without premise 5 would incorrectly give 1/2.
- **Trivial source event:** q = +/-1 implies Q psi = +/-psi. Source pruning fixes rho and L = 0. A zero-weight selected branch is never normalized.

These are hand-derived controls, not a numerical enumeration or a replay of historical test totals. The result does not contradict v9.35: that theorem concerns the commuting family of source-local dephasings. E_K is a different existing structure. Neither this calculation nor that difference establishes an intrinsic event order.

## What this changes, and what it does not

This supplies a concrete composition to inspect: source pruning can change the possible record law of the already specified generator spectral algebra even though that algebra's pinching fixed the original state. The proof in (1)-(4) is new work in this continuation, not a claim of mathematical novelty.

It does NOT yet supply the requested two source preparations and a physically identified, initially blind receiver. The displayed comparison fixes one mathematical input and compares source-event histories. Nor does it show that an existing stored K record updates: without an earned observation/write operation, an old record may simply remain unchanged. A generator eigenvalue is not automatically a receiver-owned physical quantity.

The remaining concrete association is: actual source event -> this source instrument -> the same physical carrier -> an existing receiver's available generator-sector record. No inspected source here provides that association, and no mapping to P1 is asserted. The different mathematical law cannot yet be promoted to a native signal.

No new coupling, tensor register, detector, numerical campaign, Gemini review, stage closure, or merge was performed for this note. P1 and PR123 retain their accepted scope. Pursue this candidate further only with source evidence identifying the actual event/record interface, not a sweep of generators, bases, or supplied readers.

## Source access and verification boundary

The accompanying SOURCES.json identifies the three complete text readbacks and their hashes. The original Library read returned each text one byte shorter than its reported file size; these are preserved as returned, without guessing a missing byte. They are not independently downloaded originals. Historical certification labels and counts in those sources are quoted archive content, not independently revalidated by this note.

- sources/v9_33.readback.md, section 5: generator eigenstate inputs and generator pinching.
- sources/v9_34.readback.md, Exact source-reduction theorem: distinguished source observable, source instrument, probabilities and exterior invariance.
- sources/v9_35.readback.md, sections 1-5 and 7-9: the scope of the source-only commuting family and its observation boundary.

Independent scientific acceptance is not claimed. File publication/readback verification cannot substitute for Gemini review or for physical evidence.
