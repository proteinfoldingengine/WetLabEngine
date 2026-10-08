# C3 command provenance theorem: exclusive-writer sufficiency and hidden-writer obstruction

Date: 2026-10-08.
Status: REVISED AUTHOR-SIDE MATHEMATICAL CANDIDATE after independent REVISE; fresh review required.
Frozen scope COUPLED_C3_COMMAND_PROVENANCE_SCOPE.md at 451844a800ef6146a72e47f0f44274b30c564ed7.

## 1. Native carrier and control/observation separation

Prepared roots E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), Z subseteq finite spectator palette T, floors2 and protected band 3<=tau<=4. Every valid spectator addition or deletion on r4 preserves tau=3 and floors2.

A controller may ISSUE signed commands +z(r4) or -z(r4). Only a successfully COMMITTED command changes Z. A rejected or uncommitted command changes nothing. A command log is NOT automatically a state-change log. Define a commit ledger as a record with authenticated success/failure acknowledgements and order, so that the controller can distinguish committed from rejected commands. This is a conditional interface, not a native observer theorem.

The earlier POST_A12_DYNAMIC_RESIDUAL_RESULT.md at d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7 assumes supplied/tracked support for a declared active edit; AUTO_LOWER_WITNESS_RESULT.md on this branch defines signed native endpoint events A(i,x),D(i,x). Neither source derives the existence of authenticated acknowledgements, exclusivity or seed genesis.

## 1A. Explicit semantic commit and validity contract

For any current Z subseteq T, a proposed +z(r4) is VALID iff z is absent; a proposed -z(r4) is VALID iff z is present. Every successful primitive changes exactly that one incidence and leaves all other spectator incidences unchanged. A committed command is a valid primitive whose state transition has ACTUALLY OCCURRED, not merely a signed request, delivery receipt, authorization, or attempted edit.

The conditional ledger contract guarantees: (i) an authenticated acknowledgement of actual semantic commitment or rejection for each attempted command, (ii) exactly-once correspondence between committed records and native changes, (iii) completeness and total order of the successful changes on r4, (iv) no duplicate/reordered records, and (v) no unreported changes by other actors (exclusive writer). A rejected, timed-out, or uncommitted request contributes zero to the count; absent an authoritative commitment outcome, its effect is UNKNOWN, not automatically zero.

None of these guarantees is derived from the native signed event notation or from UQCF-GEM's physical observer. They are hypotheses of this controller theorem.

## 2. Exclusive-writer sufficiency

Assume: (E1) the initial count q0=|Z0| is known; (E2) every actual spectator change on r4 is caused by one of the controller's own valid committed signed commands; (E3) the controller receives a complete ordered commit ledger including direction and root/spectator type, with rejected commands identified.

Let C_n be the sequence of committed spectator commands, and eps_j=+1 for a committed insertion, -1 for a committed deletion. Define
    q_n=q0+sum_{j in C_n} eps_j.

Induction on committed changes proves q_n=|Z_n|: an accepted insertion of an absent spectator increases occupancy by one; a committed deletion of a present spectator decreases occupancy by one. A rejected command is excluded and changes nothing. The exclusivity assumption excludes any other change to Z between commits.

Therefore b_n=1[q_n>0] is exact. After initialization, the controller does not require a separate PASSIVE observer to discover signs of its own committed commands. It still requires the declared commit acknowledgements and the guarantee that no unreported external edits occur. It also must have a mechanism ensuring/confirming command validity; this proof does not derive that mechanism.

## 3. Unknown seed: sign-only exactness versus identity-aware restrictions

Under the exclusive-writer and semantic-commit contract, suppose q0 is unknown but finite N is known. Let s_j be the cumulative signs of committed valid spectator edits.

For a SIGN-ONLY ledger, which hides identities and asserts only that some valid labelled history realizes those signs, the independently closed partial-seed theorem gives the EXACT integer feasible initial counts:
    L=max(0,-min_{0<=j<=n}s_j), U=min(N,N-max_{0<=j<=n}s_j).
If L>U the sign ledger is inconsistent. Otherwise current feasible counts are exactly [L+s_n,U+s_n], and the positivity bit is forced zero, forced positive, or ambiguous according to that interval.

For an IDENTITY-LABELLED commit ledger (+u,-v,...), the interval [L,U] is only a capacity-feasible OUTER BOUND. A particular sequence can impose extra membership constraints on the initial set, narrowing the seed possibilities or making the identity-labelled ledger inconsistent.

Concrete rejecting example: N=2, T={u,v}, ledger (+u,-u). The sign-only interval permits q0=0 or 1. But for the identity-labelled ledger, +u requires u initially absent; if q0=1 the only valid seed is {v}. Thus both cardinalities happen to remain feasible in this example, but not all q0-subsets are valid. A sharper example is (+u,-v), with u!=v: +u requires u absent and -v requires v present at the second event. With T={u,v}, the ONLY possible initial seed is {v}, so q0=1, while the sign-only interval permits q0=0 or 1. The latter q0=0 is impossible for this identity-labelled history. Hence exactness cannot be transferred from sign-only to identity-aware logs without a separate membership-consistency proof.

The known-seed signed-count induction remains exact for any ACTUALLY COMMITTED valid identity-labelled ledger. This section does not assume a passive full-state read.

## 4. Hidden-writer obstruction with identical controller transcript

Let T contain z, and let the known initial seed be empty. In both worlds the controller issues NO commands and receives the same empty command/commit transcript.

World A: no spectator change, final Z=empty, b=0.
World B: an external actor makes one valid unreported +z(r4) native change, final Z={z}, b=1.

Both prepared states preserve tau=3 and floors2. The controller transcript and known seed are identical, but final b differs. Hence a controller seeing only its own command/acknowledgement transcript cannot reconstruct global b when unreported external changes are allowed.

A less degenerate example: both worlds first commit controller +u(r4), then World A has no external edit while World B has an unreported +v(r4). The controller sees identical one-command success logs but q differs (1 vs2), which can affect subsequent deletion outcomes. The empty-transcript example already proves b non-identifiability.

Thus exclusive writing OR equivalent complete external-event reporting is sufficient for the simple signed-command ledger reconstruction guarantee. When unreported external edits are allowed, OWN-COMMAND-ONLY reconstruction is not guaranteed. This is an interface-relative counterexample, not a universal necessity of exclusive writing: an independently justified trusted observation channel could restore identifiability.

## 5. Command sign is not passive event observability

A native transition operator can be described with a sign (add/delete) in a mathematical proof or an action command. This is COMMAND METADATA. It does not imply a separate observer receives signs of ALL native updates. In particular, knowing the controller's intended command is insufficient if the edit is rejected or if an unreported actor changes the state.

The earlier C3 O_coarse separation theorem is not contradicted: O_coarse deliberately omitted signs, and did not assume exclusive writer. The command-provenance interface is strictly stronger and conditional.

## 6. Scientific boundary

This theorem distinguishes:
- mathematically available SIGNED NATIVE EVENT SYNTAX;
- conditionally available AUTHENTICATED COMMIT PROVENANCE;
- still-unproved GENERAL OBSERVER ACCESS to all relevant native updates.

No universal controller theorem, physics, force, geometry, energy, GR/ADM, continuum or fundamental time follows. Broader C3 and C4-C6 remain OPEN.
