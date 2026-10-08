# C3 semantic-commit observability gate — frozen theorem-first scope

Date: 2026-10-08.
Status: PROSPECTIVE SCOPE / NO INDEPENDENT ACCEPTANCE.

Parent closed command-provenance theorem: COUPLED_C3_COMMAND_PROVENANCE_CLOSEOUT.md at 62f012a48c1a6abd25637179eac39214f58a2e25.
Parent closed coarse-event separation theorem: COUPLED_C3_EVENT_CHANNEL_CLOSEOUT.md at e1bc1dae02e7647a00ff11c4b439851ee076f775.

## Objective

Can the controller infer that its attempted native incidence command ACTUALLY committed from the existing core-only retained fields, without a new acknowledgement primitive? Freeze the exact observable and construct a pair of legal executions with the same observations but different commitment outcomes.

## Declared model

Four-root prepared carrier E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), floors2, tau=3; spectator palette T contains z, and initially Z=empty. Controller knows the initial full prepared state and issues exactly one attempted command +z(r4). The attempt is either (C) successfully committed as a valid native transition or (R) rejected before changing any incidence. Rejection is a NO-OP, not itself a native edit. A command-attempt channel logs the same issued signed command and root/label address in both cases, but does NOT include authoritative commit/reject acknowledgement. After the attempt, observer receives the exact core-only retained channel: core projections, all core-only miss-count coordinates for |H|<=4, global tau, and floor-validity Booleans. It does not receive root4 cardinality, spectator occupancy, full-palette miss counts, or a state-difference oracle.

## Required theorem and controls

1. Prove both possible executions are consistent with the declared attempt interface; C is a legal native transition, R is an allowed rejected attempt (no native change). Both preserve floor2 and tau3.
2. Show entire visible transcripts (known seed, issued signed command, post-attempt core projections, all core-only miss counts, tau and floors) are identical.
3. Prove actual semantic commitment bit c differs (1 versus 0), as does final spectator capacity b. Thus no deterministic estimator from this channel can certify actual commitment, nor update q exactly for both.
4. Explain why an attempted-command SIGN alone is not a committed-event SIGN; why a guaranteed always-successful validity/commit mechanism would eliminate this particular ambiguity; and why adding root cardinality, full-palette spectator miss counts, or authoritative acknowledgement is a stronger channel.
5. Distinguish this obstruction from prior +u,-u versus +u,+v histories, which both consisted entirely of committed events.
6. Do not claim rejection is a native transition, a universal observer impossibility, or physical geometry/force/time.

No numerical campaign. Freeze proof, author audit, fresh independent adversarial review and separate publication audit before scoped closeout.
