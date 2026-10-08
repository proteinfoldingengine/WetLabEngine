# C3 command provenance theorem: exclusive-writer sufficiency and hidden-writer obstruction

Date: 2026-10-08.
Status: AUTHOR-SIDE MATHEMATICAL CANDIDATE; independent review pending.
Frozen scope COUPLED_C3_COMMAND_PROVENANCE_SCOPE.md at 451844a800ef6146a72e47f0f44274b30c564ed7.

## 1. Native carrier and control/observation separation

Prepared roots E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), Z subseteq finite spectator palette T, floors2 and protected band 3<=tau<=4. Every valid spectator addition or deletion on r4 preserves tau=3 and floors2.

A controller may ISSUE signed commands +z(r4) or -z(r4). Only a successfully COMMITTED command changes Z. A rejected or uncommitted command changes nothing. A command log is NOT automatically a state-change log. Define a commit ledger as a record with authenticated success/failure acknowledgements and order, so that the controller can distinguish committed from rejected commands. This is a conditional interface, not a native observer theorem.

The earlier POST_A12_DYNAMIC_RESIDUAL_RESULT.md at d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7 assumes supplied/tracked support for a declared active edit; AUTO_LOWER_WITNESS_RESULT.md on this branch defines signed native endpoint events A(i,x),D(i,x). Neither source derives the existence of authenticated acknowledgements, exclusivity or seed genesis.

## 2. Exclusive-writer sufficiency

Assume: (E1) the initial count q0=|Z0| is known; (E2) every actual spectator change on r4 is caused by one of the controller's own valid committed signed commands; (E3) the controller receives a complete ordered commit ledger including direction and root/spectator type, with rejected commands identified.

Let C_n be the sequence of committed spectator commands, and eps_j=+1 for a committed insertion, -1 for a committed deletion. Define
    q_n=q0+sum_{j in C_n} eps_j.

Induction on committed changes proves q_n=|Z_n|: an accepted insertion of an absent spectator increases occupancy by one; a committed deletion of a present spectator decreases occupancy by one. A rejected command is excluded and changes nothing. The exclusivity assumption excludes any other change to Z between commits.

Therefore b_n=1[q_n>0] is exact. After initialization, the controller does not require a separate PASSIVE observer to discover signs of its own committed commands. It still requires the declared commit acknowledgements and the guarantee that no unreported external edits occur. It also must have a mechanism ensuring/confirming command validity; this proof does not derive that mechanism.

## 3. Unknown seed under exclusive writer

Assume E2,E3 and known finite palette size N but unknown q0. Let s_j be cumulative committed signs, with s_0=0. The exact feasible seed interval is
    L=max(0,-min_j s_j), U=min(N,N-max_j s_j).
For consistent ledgers the exact current occupancy interval is [L+s_n,U+s_n], by the independently closed partial-seed theorem. b is forced zero if the upper bound is zero, forced positive if the lower bound is >=1, and otherwise ambiguous.

Thus exclusive writer plus a complete signed commit log need not reveal the exact seed in every history; the finite-capacity native validity constraints sometimes resolve it. No unconditional initialization claim is made.

## 4. Hidden-writer obstruction with identical controller transcript

Let T contain z, and let the known initial seed be empty. In both worlds the controller issues NO commands and receives the same empty command/commit transcript.

World A: no spectator change, final Z=empty, b=0.
World B: an external actor makes one valid unreported +z(r4) native change, final Z={z}, b=1.

Both prepared states preserve tau=3 and floors2. The controller transcript and known seed are identical, but final b differs. Hence a controller seeing only its own command/acknowledgement transcript cannot reconstruct global b when unreported external changes are allowed.

A less degenerate example: both worlds first commit controller +u(r4), then World A has no external edit while World B has an unreported +v(r4). The controller sees identical one-command success logs but q differs (1 vs2), which can affect subsequent deletion outcomes. The empty-transcript example already proves b non-identifiability.

Thus EXCLUSIVE WRITER or equivalent complete external-event reporting is necessary for the simple signed-command ledger reconstruction guarantee in this domain. This is a necessity relative to the declared controller interface, not proof that all possible alternative observation channels fail.

## 5. Command sign is not passive event observability

A native transition operator can be described with a sign (add/delete) in a mathematical proof or an action command. This is COMMAND METADATA. It does not imply a separate observer receives signs of ALL native updates. In particular, knowing the controller's intended command is insufficient if the edit is rejected or if an unreported actor changes the state.

The earlier C3 O_coarse separation theorem is not contradicted: O_coarse deliberately omitted signs, and did not assume exclusive writer. The command-provenance interface is strictly stronger and conditional.

## 6. Scientific boundary

This theorem distinguishes:
- mathematically available SIGNED NATIVE EVENT SYNTAX;
- conditionally available AUTHENTICATED COMMIT PROVENANCE;
- still-unproved GENERAL OBSERVER ACCESS to all relevant native updates.

No universal controller theorem, physics, force, geometry, energy, GR/ADM, continuum or fundamental time follows. Broader C3 and C4-C6 remain OPEN.
