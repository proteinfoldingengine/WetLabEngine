# C3 event-channel separation: indistinguishable coarse traces with different capacity

Date: 2026-10-08.
Status: AUTHOR-SIDE ANALYTICAL CANDIDATE; independent review pending.
Frozen scope COUPLED_C3_EVENT_CHANNEL_SCOPE.md at 5f11d4ee5d9911b717e2eac68fcd945c65a8720a.

## 1. Prepared native carrier and observation channel

Let core P0={a,b,c,d,e}, spectator palette T contain distinct u,v, and fresh w outside T and P0. Prepared four-root states:
E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), Z subseteq T.
All original floors f_i=2; native spectator event +z(r4) adds z not already present and -z(r4) deletes z currently present.

Define O_coarse at each slice to contain the labelled core projections E_i intersect P0, every core-only miss count M_core(H) for H subseteq P0 with 1<=|H|<=4, exact hitting number tau, all four floor-validity Booleans, and the ordered occurrence/root address of each native edit. It does NOT report the edit sign, spectator identity, |Z|, full support, or hypothetical legality. The observer knows Z0=empty.

## 2. Two actual native histories

World A:
  E(empty) -- +u(r4) --> E({u}) -- -u(r4) --> E(empty).

World B:
  E(empty) -- +u(r4) --> E({u}) -- +v(r4) --> E({u,v}).

All four events are syntactically legal at their respective sources: the first +u inserts an absent u; -u removes present u; +v inserts absent v. Every fourth root contains d,e and any spectators, hence cardinality at least2 and floor2 always holds. The three fixed triangle roots have hitting number2; r4 is disjoint from their union {a,b,c} and nonempty, so full tau=3 at every slice in both worlds. Both histories have exactly two edits addressed to r4.

## 3. Exact transcript equality

At all three slices in both worlds:
- labelled core root projections are ({a,b},{b,c},{a,c},{d,e});
- core-only M_core(H) is identical for every H subseteq P0 because Z contains no core labels;
- exact tau=3;
- all four floor-validity flags are true.

The ordered occurrence record is (r4,r4) in both worlds, with the same length and addresses. At slice1 the FULL states are also identical E({u}); at slice2 the hidden full states differ, but every field in O_coarse is identical.

Thus O_coarse(World A)=O_coarse(World B) as complete observed histories.

Nevertheless final capacity bits differ:
  b_A=1[Z_A nonempty]=0,
  b_B=1[Z_B nonempty]=1.

Therefore no deterministic estimator g(O_coarse) can equal the true final b for both worlds. Equality of input transcripts would require equal outputs, contradicting b_A!=b_B.

This is a concrete observability obstruction for the SPECIFIED coarse channel even with known empty seed, complete edit occurrence counting, labelled root address, exact tau and core-only miss counts. It is not a universal impossibility theorem for every retained observer.

## 4. Minimal local separation and stronger available channels

For this PAIR of histories, the sign of the second spectator event separates them: World A's second event is a deletion, World B's is an addition. With known empty seed and complete valid spectator event signs, the prior closed event theorem reconstructs q and b by q_n=sum eps_j. This does not prove that the native observer is actually supplied those signs.

A direct current r4 cardinality or floor slack also separates the final states: |r4|=2 in World A and 4 in World B. These are NOT part of O_coarse.

If a full-palette residual miss-count field for residual family {r4} is legitimately initialized, M_R({u}) and M_R({v}) identify occupancy. At final slice World A has M_R({u})=M_R({v})=1, whereas World B has both zero. But those spectator coordinates are absent from the core-only M_core field.

The single sign bit of the second event suffices to distinguish this pair. This does NOT assert that one bit is always sufficient for arbitrary event histories, nor does it imply a general observer-access law.

## 5. Consequence for exact protected repair

The previously independently closed C3 hidden-spectator theorem gives shortest repair length8 for final Z empty and length6 for final Z nonempty, while a fresh-w eight-edit route is legal in both.

Thus the identical O_coarse transcript cannot select a shortest repair uniformly across Worlds A and B, although the safe eight-edit policy works for both. This conclusion uses the prior bounded carrier result and does not claim any physical force or observer mechanism.

## 6. Native event-channel gate

A successful first-principles bridge must derive a channel that distinguishes the two histories, or prove a different native observable with the same distinguishing power, from ordered-update structure rather than assuming it.

Simply knowing event OCCURRENCES, core retained certificates, global tau and floor-validity is insufficient in this carrier. The origin of a sign-complete channel, full-palette miss-count initialization, or retained root cardinality remains open.

No physical geometry, energy, GR/ADM, continuum, fundamental time, or general observer-access result follows.
