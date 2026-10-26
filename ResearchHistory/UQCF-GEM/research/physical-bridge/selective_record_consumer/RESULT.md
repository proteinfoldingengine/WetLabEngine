# Selective correlations and an existing record consumer

Author: ChatGPT research session with Aaron. Date: 2026-10-25 (America/Phoenix).
Status: analytical construction, frozen for independent review. Native bridge NOT_DERIVED.

## Positive result and why this route is being reopened

An existing source-local selected event can change a receiver's conditional state when the input carries correlations, even though the receiver's complete initial marginal is identical across preparations. The unchanged v15.14 record-dependent consumer can also convert such a correlation into different probabilities for its own B2 record after averaging over BOTH source outcomes. No new copier, controller, READS entry, outcome-selection law or detector is introduced into that model.

This corrects an overextension in record_access/CONSTRUCTION.md section 4. Its stated product-channel proposition is true. Its sentence extending the conclusion to individual v15.13 local operators, and the resulting unqualified requirement for a new joint event, do not follow for selected, trace-decreasing branches. The distinction matters: conditional state change and an unconditioned available receiver signal are different claims. The latter still requires the record connection supplied in v15.14.

The construction below is a diagnostic of existing mathematics and software. Its correlated preparations are explicitly supplied and engineered against fixed inherited operations. It is NOT a derivation of those preparations from native incidence structure, a new first-principles interaction, or a demonstration that arbitrary actual pruning invokes this model. It changes the justified scope of an exclusion and supplies one complete existing consumer trace; no physical premise is claimed removed. Neither this correction nor review warrants a new family of supplied-channel variants.

## 1. Premises and source provenance

All source files are at research commit 3ceb814258f43774b4af1352379ffcd0bd079599. Complete exact source bytes are in SOURCE_PACKET.json.

1. INHERITED CONDITIONAL MODEL / SOFTWARE: v15.13 event_model.py, blob 95d0303d617422d74e61ae017f0354233ec9454b. It specifies the four-qubit order (A1,A2,B1,B2), local event unitaries, binary projectors and apply_selected(rho,K) = K rho K-dagger / Tr(K rho K-dagger) at positive branch weight. The carrier, instruments and actual records are supplied in that model; this tag does not promote them to native physics.
2. INHERITED CONDITIONAL MODEL / SOFTWARE: v15.14 adaptive.py, blob 44a87e4cc5bcf531ef7798aadab5d9dbba3482cb. READS declares A2 reads A1 and B2 reads A1,B1. The fixed B2 instrument uses exp(-i 0.6 (-1)^h Y_B2) U_B2_old when its already-realized A1 record is h. advance uses only declared realized read keys and appends the supplied outcome. No operation or parameter is changed.
3. INHERITED CLAIM UNDER CHECK: constructions/record_access/CONSTRUCTION.md, blob d5557538caaae6eaf20bb1d8602c1b224b8aafee. Section 4's equation assumes trace preservation; its surrounding prose also excludes individual local operators. This source is an unreviewed construction, not an accepted no-go theorem being overturned.
4. INHERITED SCOPE: v15.13 README blob 0d65ef13285a51ba3dcd2cd023e53bdf3d578e2d, v15.14 README blob 3877378a375a72c70587c98e8ff1c82d900774c5, and record_consumer_trace/TRACE.md blob 19605ddf5a91c6607c9621796daffcbaf3d31978. They expressly retain supplied factor ownership, preparations, record wire, controller and RAS/RCR; the trace already establishes that a realized value is supported in the retained state and used by the declared consumer.
5. SUPPLIED DIAGNOSTIC PREPARATIONS: the two explicit state pairs below. The four-qubit inputs are not the historical initial_state() fixture. Their common inverse calibration is a mathematical construction, not a sourced physical preparation.
6. SUPPLIED MODEL INVOCATION / ACCESS: a legitimate initial Snapshot carrying those states, the allowed event order A1,B1,B2 (optionally followed by A2), the model's outcome weights and its B-record ownership/access. Actual atemporal measurement/pruning occurrence remains ACCEPTED INPUT, but identification with this selected process is unproved.

## 2. Positive selected-branch witness

For two bits S,R, define

    omega_0 = (|00><00| + |11><11|)/2,
    omega_1 = (|01><01| + |10><10|)/2.

Both complete R marginals are I/2; both S marginals are also I/2. The distinction is in the joint correlation, not in a localized source marginal. These are separable classical-correlated states.

Apply the SAME source-local selected projector K_h = |h><h|_S tensor I_R. Its probability is 1/2 for each h in BOTH preparations. The normalized R state in the selected branch is

    R_(s,h) = |h XOR s><h XOR s|.

Thus for the same positive-weight record h=0 the two receiver states are orthogonal, despite initially identical full receiver marginals. No source-specific operation or source-specific selected outcome is used in that comparison.

The exact reason the product-channel proof does not apply is visible in its trace:

    Tr_S[(K_h tensor I) omega_s (K_h-dagger tensor I)]

depends on the source effect K_h-dagger K_h and the joint correlations. Only the SUM over a complete trace-preserving source instrument removes that effect.

Averaging h gives I/2 for each preparation. A receiver given R alone, without a justified association to h, has no unconditioned distinguishing law. Joint parity h XOR R reveals s, but assigning h to the receiver would be an additional access resource. The two-bit witness by itself is not a signalling or receiver-access proof.

This is elementary conditioning, not new quantum physics. It identifies a concrete gap in the scope of the earlier exclusion.

## 3. A complete trace through the unchanged inherited consumer

Now use exactly the inherited four-qubit carrier and fixed matrices. Let A=(A1,A2), B=(B1,B2), and

    |chi_t> = (|0> + (-1)^t |1>)/sqrt(2),
    sigma_s = (1/2) sum_(h=0,1)
              |h,0,0><h,0,0|_(A1,A2,B1) tensor |chi_(h XOR s)><chi_(h XOR s)|_(B2).

Let U_A, U_1 and U_2 be base.event_unitary('A1'), base.event_unitary('B1'), and base.event_unitary('B2'), respectively. U_2 is the OLD B2 unitary, before adaptive.py's already existing record-controlled extra rotation. Define one common unitary and the two input states by

    V = U_2 U_1 U_A,
    rho_s = V-dagger sigma_s V.

This preparation is stated openly: it pulls the diagnostic pair back through the fixed existing local operations. It is not evidence that native history or the historical fixture produces rho_s. V is independent of s and factors across A|B; the source parameter changes only the correlation in sigma_s. No cross-factor entangling operation is introduced by V, and both rho_s remain separable across A|B.

### Complete initial receiver blindness

The B marginal of sigma_s is |0><0|_(B1) tensor I_(B2)/2 in both cases. U_A acts on A only. U_2 commutes with Z_B1: its generator is 0.43 Y_B2 + 0.13 Z_B1 X_B2. Consequently it preserves each B1 sector and, on B1=0, preserves the maximally mixed B2 factor. Therefore the initial full B state is

    Tr_A(rho_s) = U_1-dagger (|0><0| tensor I/2) U_1,

independent of s. This is equality of the whole four-dimensional B density operator, not equality on one selected diagnostic. The initial records tuple is empty in both cases. The A marginals also agree, but the global input states differ.

### A1 realizes the correlation branch

Start with an abstract valid Snapshot having records=(), rho=rho_s, tau=rho_s and mass=1, with positive normalization as above. This uses the existing Snapshot/advance interface. It is NOT a claim that adaptive.start() or adaptive.run(), which use the fixed historical fixture, prepare these inputs.

advance(A1,h) applies P_(A1,h) U_A. U_A cancels its inverse in the common preparation and commutes with the B operations. Each h has weight 1/2. The normalized remaining state is

    U_1-dagger U_2-dagger
      (|h,0,0><h,0,0| tensor |chi_(h XOR s)><chi_(h XOR s)|)
    U_2 U_1.

A1's realized value is now in the existing record tuple and in the state's A1 projector support.

### B1 supplies its required local record

advance(B1,0) applies P_(B1,0) U_1. U_1 cancels its inverse; U_2 preserves B1=0. Therefore outcome B1=0 has conditional weight one, and the state becomes the middle parenthesized state conjugated by U_2-dagger and U_2. The alternative B1=1 has zero weight and is not an admitted selected call. There is no claim that every historical four-bit script is positive on these new inputs.

Now both declared prerequisites for B2, A1 and B1, exist. No readiness check is bypassed, no outcome is guessed, and no future record enters instrument().

### The existing B2 controller produces an unconditioned local contrast

For the actual A1 value h, the unchanged instrument applies

    R_h U_2,     R_h = exp[-i 0.6 (-1)^h Y_B2],

followed by the B2 computational projector. U_2 cancels the remaining inverse. The input B2 Bloch vector is (-1)^(h XOR s) along X. The rotation R_h therefore produces

    <Z_B2> = -(-1)^s sin(1.2),

because exp(-i theta Y) rotates X toward negative Z by angle 2 theta. Crucially, h cancels. Thus

    p_s(B2=0 | A1=h, B1=0) = [1 - (-1)^s sin(1.2)] / 2
                           = p_s(B2=0).

Both A1 branches give the same conditional B2 law, so averaging over both source records preserves the contrast. Their Bernoulli total-variation distance is exactly sin(1.2)>0. The 1.2 is twice the inherited 0.6 controller extent; it is not fitted or optimized here. No numerical approximation or execution is needed for strict positivity.

The outcome B2 is stored in B's existing local record position and supported by its projector. The model's declared B ownership/read interface therefore suffices to interpret this as a local output law. It does not require that a later observer of B additionally receive h: the existing B2 consumer has already used that record.

The prefix A1,B1,B2 satisfies the actual dependency interface. Appending A2 completes an allowed schedule. Summing over A2 outcomes leaves the B law unchanged because that later source operation is trace preserving when its outcomes are forgotten. Each individual branch preserves the already-recorded B1,B2 projectors.

This supplies an exact event-record-consumer-output calculation inside the inherited conditional model, without modifying its mechanism.

## 4. Controls and corrected inference

1. Forget the source record and allow only source-local trace-preserving action plus a fixed B channel. Equal complete initial B marginals then remain equal. Proposition 4.1's stated product-channel theorem is preserved.
2. The selected witness in section 2 changes conditional B states but does not change the unconditioned B marginal. Do not confuse a selected state's difference with information available to an unheralded receiver.
3. In section 3, if B2's instrument is made independent of h by supplying one fixed control to all branches, the complete B map is the same channel for both inputs and gives identical B output laws. This is a mathematical adverse control, not an authorized modification of the inherited implementation.
4. The real adaptive process does not satisfy the product-channel hypothesis: its B operation uses A1 through the declared record wire. No contradiction of no-signalling, no new coupling-free unconditioned communication, and no superluminal claim follows.
5. The initial global state and any global certificate already contain the correlation distinction. They are not initially blank receiver records. Initial blindness is asserted specifically for the complete B state and its empty local record history.
6. The witness does not show a localized source marginal acquired by a blank pure memory. It redistributes access to a pre-existing joint correlation. Replacing the correlated pair by an identical product input cannot create the missing source distinction.

The corrected local statement is: products of fixed trace-preserving channels preserve equality of receiver marginals; a fixed receiver-local selected operation also preserves equality on matched positive-weight branches, since it acts on the same receiver marginal. A source-local selected operation can instead reveal existing correlations conditionally. Making that conditional information usable without selecting runs needs a justified branch association or a consumer that already has it.

## 5. Scientific disposition

The positive advance is narrow but concrete: an overbroad exclusion is repaired by an exact selected-event witness, and the existing adaptive consumer is shown to turn a specified hidden correlation into its own record law from completely equal initial receiver states. The old inspection of READS/controller provenance is preserved, not relabelled a new physical derivation.

All source-event, quantum-carrier, correlated-preparation, record-wire, physical ownership and availability premises remain supplied. In particular, choosing rho_s by common inverse calibration is a legitimate diagnostic against the broad exclusion but cannot earn native preparability. The actual event-to-native-incidence and event-to-grade correspondences of T-117 through T-133 are untouched.

The productive native re-entry is now specific: find an inherited correlation-bearing preparation and a native relation that supplies the branch connection already consumed here. Do not add a new copied register, tune a controller, create another state encoder, or launch a parameter/channel classification to imitate this diagnostic. The existing source packet does not establish that re-entry. This result neither proves nor assumes a first-principles solution.

All calculations are analytical. No scientific module, simulation, enumeration, sampling or historical campaign was executed. Text/hash/archive operations for review do not count as scientific tests. Independent review must reconstruct the full common-preparation cancellation, initial marginal equality, exact existing API path, sign and factor of two in sin(1.2), outcome averaging, zero-weight B1 branch, source-local correction, and every claim boundary before acceptance.
