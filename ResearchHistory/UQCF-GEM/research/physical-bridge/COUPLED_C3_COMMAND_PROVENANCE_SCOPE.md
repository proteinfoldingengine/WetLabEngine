# C3 event-command provenance versus observation — frozen theorem-first scope

Date: 2026-10-08.
Status: PROSPECTIVE SCOPE; no independent acceptance.

Parent event-channel separation closeout COUPLED_C3_EVENT_CHANNEL_CLOSEOUT.md at e1bc1dae02e7647a00ff11c4b439851ee076f775.

Question: Does the native controller's knowledge of its own SIGNED edit commands suffice to update spectator capacity without a separate passive event-direction observer? Precisely distinguish exclusive control, unobserved concurrent changes, and accepted-versus-attempted edits.

Carrier: E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), finite spectator palette T, floor2, protected band 3<=tau<=4. Controller knows initial count q0 or has the closed partial-seed interval and receives a command log for spectator edits on r4. A command specifies (+ or -), root and spectator identity or at least spectator type; only successfully COMMITTED valid edits count. Commands may be rejected.

Required results:
1. Under EXCLUSIVE-WRITER (every spectator change on r4 is a committed controller command) and known q0, q_n=q0+sum committed signs exactly; no passive observation oracle is needed AFTER initialization. A rejected command does not change q. Distinguish command authorization from successful commitment and ensure acknowledgement is not assumed without declaration.
2. Under exclusive writer and unknown q0 but known N, apply previously closed prefix-feasibility interval to committed signs. Identify when b is forced and when ambiguous.
3. If hidden external spectator edits are permitted and not reported, exhibit two histories with identical controller command/acknowledgement transcripts but different final b. Even knowing signed OWN commands is insufficient for total state.
4. Distinguish a syntactically valid committed command (already requires edit validity mechanism) from an observer's passive ability to identify arbitrary hidden events. Existing prior theorem POST_A12_DYNAMIC_RESIDUAL_RESULT.md explicitly assumes a named active support for declared edits; AUTO_LOWER_WITNESS_RESULT.md defines signed endpoint events; neither by itself proves exclusive writer, commitment acknowledgement, initial count or hidden-event exclusion.
5. Do not derive physical observer access, energy, forces, geometry or fundamental time.

Publish source-grounded proof and author audit; request fresh adversarial review. No numerical campaign.
