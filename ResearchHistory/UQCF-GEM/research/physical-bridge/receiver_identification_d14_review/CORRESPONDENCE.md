# Draft 12 continuation: match one existing receiver sector to the source transfer

Author: proteinfolding-gpt. Date: 2026-10-18 (America/Phoenix).
Original inspected immutable parent: `1383f49d4e1ecf399d4e968a3e688def8467c840`.
Status: analytical continuation and source correspondence. **Native receiver access NOT_DERIVED.** This note is not a new mechanism, a numbered stage, or independent acceptance.

Publication reconciled against `e1d8e0226a0299033341a4552ecafd8e89f92f66`. The original draft-12 freeze has since received Gemini ACCEPTED in run 39162569331. Its frozen text and receipt remain unchanged; that acceptance does not cover this revision. Its source trace independently records the same supplied-state/readout gap. The finite campaign used fixed origins for its independence claim, consistent with the clarified factorization scope.

## 1. What is carried forward

The user reports the arbitrary-probability-background strengthening and the coarse-record-sector test. This pass incorporates the former into section 18's written argument and continues the latter at its unresolved identification. It does not claim either as a new discovery.

The inspected parent still used finite-support arguments in Theorem 18.2 and Proposition 18.3(d). The revised section 18 gives the measure-level proof. For every Borel probability law nu on R and d>0,

    TV(nu, nu * delta_d) >= sup_t nu((t-d,t]) > 0.          (1)

The half-line probability difference proves the bound; countably many length-d intervals partition R, so some interval has positive mass. This removes support, density and moment assumptions. An atom-only bound cannot establish positivity for diffuse laws. The bound is distribution-dependent: broad backgrounds may make separation arbitrarily small. The occupancy-optimality proof is also extended to arbitrary nonnegative Borel laws through signed-measure domination; its equality case is still a nonincreasing law on g Z_{>=0}. Continuous laws are not claimed to be trace-class diagonal states on l²(R); the coherent-extension proposition is now explicitly finite-dimensional.

Sections 0-17 and the frozen earlier review packets are unchanged. The revised section 18 is unreviewed, and its historical scratch counts are preserved as historical claims, not fresh verification of this extension.

The same source check corrected three section-18 scope statements: sufficiency needs factorization across retained fibers (independent records with random origins do not guarantee it); sector intertwining is stronger than covariance; and logical irreversibility requires a non-singleton addition fiber. These qualifications preserve the positive transfer result and its open access premise.

The working target is narrower than full (H-J): identify one **already available receiver record** that distinguishes the two output preparations. Full initial receiver blindness is still required. A single separating output effect does not require universal ownership of the whole grade algebra.

## 2. The existing record is concrete

The v15.16 source extracts a basis from the already frozen v15.15 instrument; it does not choose it to fit the grade signal. Its complete branches and encoding have the form

    K_r = |r><b_r|,    V = sum_r |r>_R tensor K_r,           (2)
    F has rows <b_r|,  F†F = I.

For a fixed set S of record bits and an existing sector label s, define the inherited group C={r : r restricted to S=s}. In the source these are `groups(mask)`, `basis(schedule)`, and `projectors(mask,schedule)`. The corresponding output and input projectors are

    Q_C = (sum_{r in C} |r><r|_R) tensor I,
    P_C = sum_{r in C} |b_r><b_r| = F† D_C F.              (3)

If S is contained in A1,A2, Q_C is local to the demonstrator's A record factor. That factor ownership is part of the supplied v15.13-v15.16 model, not a derived Genesis-address assignment. A global collection of record labels need not be receiver-local.

The inherited identity is

    Q_C V = V P_C.                                         (4)

It gives an exact record-probability correspondence, for any input density matrix rho and any of the supplied record pinchings D_T:

    Tr[Q_C D_T(V rho V†)] = Tr[P_C rho].                   (5)

Proof: Q_C commutes with every record-basis pinching projector, hence D_T*(Q_C)=Q_C. Then use V†Q_C V=P_C and cyclicity of trace. No grade operator, zero-occupancy test, or new measurement channel is used. An already existing coarse sector suffices when Tr[P_C(rho_+-rho_-)] is nonzero.

For classical record accessibility after a particular mask T, require that C be a union of T-sectors (in particular S subset T). Then Q_C belongs to the retained central record algebra, and remains there under compatible later refinements. Probability preservation alone is weaker than this central-record condition. Readability within this supplied algebra is not proof of native availability.

## 3. A sharp sector needs less than an exact coordinate reader

A useful operator-level target is available without choosing an encoding. Let an already justified channel Phi have Kraus operators K_i. Let P be an input projection and Q an existing receiver-output projection. Then

    Phi*(Q)=P   iff   Q K_i = K_i P for every i.            (6)

This is elementary support mathematics, not a new physical law. To prove the forward direction, for v in range(P),

    sum_i ||(I-Q) K_i v||² = <v,(I-P)v> = 0.

For w in ker(P), sum_i ||Q K_i w||²=<w,Pw>=0. Positivity forces each term to vanish, yielding the intertwining. Conversely intertwining and trace preservation give sum_i K_i†Q K_i=P.

Thus exact transmission of one already identified binary sector does not require an exact numerical grade reader, a preferred full grade basis, or a unique microscopic channel. Equations (4)-(5) are an inherited realization of (6) inside the supplied record model. If an actual native event and its actual receiver effect satisfy the corresponding identity, unknown behavior within sectors does not weaken the sector conclusion.

Equation (6) is a sufficient exact target, not an extra universal requirement for the milestone. A justified nonzero probability contrast on an admissible pair can qualify without all-input projection intertwining. A noisy effect can also suffice under its own justified error contract.

## 4. The remaining source-to-record identification

The native field supplies, under the declared P1 event, the formal output y_p=x_p+x_l. The actual record stack supplies (3)-(5). These are different typed objects; the bridge is still to establish their correspondence.

For a coarse sector C already fixed by the receiver's existing record structure, let h_C be the proposed source predicate represented by that sector. If native input states sigma_x associated with grade configurations x are independently specified, the exact sufficient match is

    Tr[P_C sigma_x] = h_C(x_p+x_l)                         (7)

for the admissible inputs of the event, together with identification of the actual event and receiver sector used in (5). For a binary predicate h_C, this is sector support, not a numerical occupancy reader. For a random background one integrates (7) against the preparation law; only a nonzero difference between the two sector probabilities is needed.

Equation (7) is **an outstanding proof obligation**. No sigma_x, h_C, basis rotation, record partition, or native channel is chosen in this note to make it true. In particular, taking sigma_x=|b_r><b_r| after assigning r from the desired field answer would supply the missing encoding and would not derive it. Identity of two binary label sets, or matching their dimensions, is insufficient.

The complete pre-event state on the actual receiver algebra must also agree for the two preparations. Equality on Q_C alone cannot establish initial blindness. Native preparability remains an independent obligation. No global information is created by locating an already existing distinction in a receiver.

## 5. What the inspected implementations actually accept

| Inherited object | Actual input / operation | Correspondence available now |
| --- | --- | --- |
| v15.56 source binding | Genesis id, provenance root, source event, full lineage address | Types source origin; supplies no receiver projector or density matrix |
| v15.56 retained amplitude / pushforward | Relative source grade; sum over nearest-retained-ancestor fibers | Determines J and r_*J; supplies no map into v15.16's input states |
| v15.11 select_record | A density matrix, a supplied projector family and an explicit positive-weight record index | Conditions on an already supplied record; does not take a Genesis address or J as input |
| v15.14 instrument / advance | Declared READS keys and supplied outcome; explicit A1-dependent B2 controller | Demonstrates consumption within its supplied record interface; not a native source-field reader |
| v15.15 encoding | Supplied controller and copy gates | Establishes V in that model; cannot be installed as a newly derived native write |
| v15.16 projectors / pinch_joint | Frozen V, extracted basis, record-mask sectors | Gives (3)-(5) exactly; no inherited grade-to-sector association is implemented |

This source trace answers draft 12's proposed `select_record` type-match question at the inspected versions: neither that function nor the subsequent pinching consumes the source field at a Genesis address. The positive reusable object is the existing record sector and its exact input pullback P_C. The next construction should start with that object, not add an occupancy query.

Pinching preserves the already written record probabilities. It must not be counted as the event that first transfers the distinction. The source record's origin certificate is also not automatically delivered to the receiver when its retained representative changes.

## 6. Disposition and continuation

The present advance is a concrete source-to-existing-sector target and integration of the user's background correction. It does not establish that any previously missing native-access assumption is now derived. The elementary identities in this note do not justify another large numerical campaign.

Continue the same source-to-receiver construction by finding, in an inherited actual state/event definition, the association in (7), receiver ownership of Q_C, and whole-state initial blindness. The exact sector, state association and event must come from that source. If those are earned, submit the whole argument and its original sources to Gemini through the repository's established review pipeline; acceptance of the earlier frozen sections, including original section 18, does not cover this revision.

No scientific module was imported or executed in this pass. Source hashes and publication readback establish identity only. No new reader, outcome rule, physical grading axiom, clock, geometry, or default-branch merge was introduced.

## 7. Progress review against draft 13

Publication parent: `0f1c43bf8541df55d649d35480f2efb691ba5d51`; draft 13 section 19 is preserved verbatim, and remains unreviewed. Theorem 19.4 characterizes the effects invariant across coherent extensions of the declared classical map. This is useful conditional mathematics, but does not by itself establish physical access.

**Corollary 19.5 needs an availability qualification.** As written, (A2) says an effect is available *only if* it belongs to Det(f). If A_av denotes the receiver's available algebra, this establishes A_av ⊆ D_p, not A_av = D_p. For example, on the owned register take A_av = C·I. Every available effect is event-determined, so this obeys (A2) and is compatible with the register ownership in (A1), yet every normalized input gives the same accessible state. It does not give access to the full grade law or any nonconstant separating sector. If “register ownership” instead means access to every register effect, then (A1) and (A2) conflict on a nontrivial register unless the intended restriction of accessibility is stated. Either reading requires clarification.

To infer the full (H-J) identification, one would need the converse availability inclusion, or an explicit completeness assumption saying that every event-determined local effect is available. That would remain an assumption until sourced. The narrower constructive target in this note needs less: one independently identified available Q_C with unequal output probabilities, together with full initial receiver blindness and preparability. The constant-only counterexample is an analytical logical check, not independent Gemini review.

The section-19 proposed uniqueness-of-changing-subsystem check also cannot alone identify availability: formal change of a coordinate does not imply a receiver can read a nonconstant effect of that coordinate. Any follow-up should keep that distinction explicit. No additional physical mechanism is introduced here.
