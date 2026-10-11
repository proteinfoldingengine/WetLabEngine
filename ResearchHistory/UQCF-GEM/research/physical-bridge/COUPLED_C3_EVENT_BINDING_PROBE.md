# Event-to-request binding probe: archived ledger producer

Date: 2026-10-11 UTC. Status: source-scoped candidate assessment; no new theorem, numerical campaign or native mechanism. Candidate C1 is direct use of the archived V1172 Genesis ledger to supply the event binding required by the target-blind C3 gate. Source parent: `ba999041ae68e3d4bde4b88164d962c7ae41d49b`. Thirteen complete immutable sources and their hashes are retained in evidence/event-binding-probe/source_readbacks.json.

## Concrete producer inspected

The file `Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py` is the archived producer named by the v15.56 ledger/address audit. This probe follows that citation into its actual code rather than inferring an event channel from the word "ledger". No whole-archive coverage claim is made.

`HistoryLedger` contains mode, registry, root, events, witnesses and roots. `make_ledger(mode)` constructs seven literal strings:

    genesis_source_key
    source_origin_identity
    retained_sequence_identity
    label_transport
    geometry_commit
    source_flow_commit
    closure_commit

Its ordinary branch supplies the fixed registry, fixed Genesis root and the same three witness names for every event. Two mode branches substitute an attacker registry/root/witness list; another reverses the event names. These are explicit fixture controls. The function receives no C3 request, root address, incidence label, edit direction, actual successor or support state.

`chain_transition` hashes the previous root, registry, ordinal index, event string and witness strings. `build_chain` applies it to those supplied strings. `append_chain_valid_partial` recomputes the same chain; the pin check also checks the declared registry/root and membership-based witness quorum. The hash helper truncates SHA-256 to twelve hexadecimal characters. This assessment does not claim collision resistance, authenticated physical witnesses, or a security theorem. The relevant distinction is payload: verification of these strings does not verify an incidence event absent from the payload.

## Connection to the update loop

`run_pruning_for_mode` calls `make_ledger(mode)` before constructing and iterating the candidate fields. The update loop evolves a six-dimensional numerical field ensemble, weights candidates using declared divergence/source/sequence scores, and selects a diagnostic winner using `torch.argmax(weights)`. It appends numerical diagnostics to `log_rows`.

Those real simulation diagnostics must not be described as nonexistent. However, the loop does not append its actual field updates or winning-state payloads to `ledger.events` or `ledger.roots`. The ledger fixture and numerical log are different objects. Neither is a C3 incidence-edit record in this file.

After the loop, `certify_field` receives the winner and ledger separately. It evaluates the ledger pin and field closure/alignment conditions, then conjoins their booleans. It does not add a source-event/request/successor payload to the hash chain or establish that the seven literal names encode those numerical updates. A conjunction of a valid fixture-ledger check and a field check is not itself an event-to-field binding.

This is direct code/data-flow inspection, not execution of the historical simulation, a reconstructed C3 counterexample, or an allegation that its declared fixture tests were computed incorrectly. No existing historical verdict is rerun or recertified here. The supplied argmax rule and score coefficients are not adopted as native C3 successor selection.

## Comparison with the actual C3 consumer

The closed event-initialization theorem requires a legitimately known initial count and a COMPLETE valid ordered record of actual spectator changes, with root association and add/delete direction. Its count recurrence then follows. The native-interface closeout separately explains why a mathematically defined miss-count field does not supply its own initialization. The event-channel closeout proves that even ordered occurrence/root data can be insufficient if the distinguishing event signs are omitted.

The V1172 fixture has no such seed, spectator event grammar, root/label association, or add/delete payload. Assigning `label_transport` to a chosen C3 edit after the fact would add the very dictionary the new gate requires us to derive. The generic `event` string parameter could certainly hold a richer serialization if one were supplied; that engineering possibility does not derive the physical coupling, the completeness of capture or observer access. This assessment does not assert that hash-ledger architectures are incapable of recording actual events.

The later v15.56 product identity and source-binding schema do not remove this gap. They correctly state that localization is typed IF a certified source record explicitly binds a full structural lineage address. That conditional statement is preserved. This particular V1172 producer does not furnish the required C3 binding merely by naming source identity and transport in its event list.

## Candidate decision and next live obligation

**C1: CANDIDATE_STOPPED_MISSING_CONNECTION.** Directly treating this archived ledger as an already produced complete C3 event channel fails at its payload producer. C0's abstract missing map has now been checked against this concrete proposed producer; no new universal obstruction is inferred.

The next eligible candidate must identify where a justified incidence interaction produces its record—not merely where supplied records are hashed or decoded. It must derive the relation between the actual update and retained payload, including relevant identities, direction/resolution, capture completeness, seed provenance and accessibility. Requirements depend on the chosen consumer; they are not a claim that every observer must store a full C3 state or every event label.

A software wrapper that reads the whole hidden support and writes a rich event object would be an external verifier, not a solution. A declaration that every legal request commits would add a selection/progress assumption. Neither is implemented here. With no admitted native construction, another numerical campaign is not justified by this probe.

Native input/action/accessible retained output, enforcement, actual successor selection and progress remain OPEN, as do broad C3/C4-C6. The historical source-to-GR branch stops are unchanged. No geometry, physical energy, fundamental clock, dark-matter variable or new axiom is introduced. Ordered-slice provenance remains distinct from a derivation of physical duration.
