# A surviving view changes its geometry on its second local edit

On the original ordered four-leaf star, one deletion by the same source index at one of two sites determines whether a surviving view adds or removes a leaf on its second own edit during the v16.53 normalization. The view can be identified from the shared preparation. Its root degree follows 2 → 3 → 4 or 2 → 3 → 2. The observation uses the order of that view's own changes. Neither elapsed time nor a global completion signal is an input to the mathematical read.

## Same receiver, one source edit in each history

Write S for the source index, R for the receiver index and T for the third index. On a star with a fixed root and four leaves, give the four leaves the following supports in any order.

| Leaf role | Labels present |
|---|---|
| Shared by everyone | S, R, T |
| Shared by the source and receiver | S, R |
| Private to the source | S |
| Private to the third index | T |

All three indices contain the root. The unique index without a private leaf identifies R before either event. R retains both possible source sites before and immediately after the source edit. Delete S either at the three-label leaf or at the two-label leaf. Both are legal v16.26 atoms preserving the same union. R's own view is unchanged by either source edit.

Let τ be the fewest indices needed to cover all four leaves. The two private leaves force S and T into a cover in the preparation. Deleting S at the three-label leaf keeps {S,T} a cover and gives τ=2. Deleting S at the two-label leaf gives R its own private leaf. All three labels are then necessary, so τ=3. The target t stored by the v16.53 controller is its *initial* post-source τ, measured from the supplied state. It remains fixed as the incidence state evolves.

This exhausts the eligible cases in the archived R family. For at most three labels, changing which of two sites S deletes cannot change whether a universal one-label cover exists, because other labels are unchanged and S now misses a site in both arms. Unequal outputs of the cover-number calculation therefore require 2 versus 3 and three labels. With three labels τ=3 requires, and suffices for, a private singleton leaf for each label. At the raising deletion, its previously shared site must become the R singleton. The other compared site must carry all three labels, since a second {S,R} site would also become an R singleton under its own alternative deletion. The remaining two sites must be the S and T singletons. There are exactly 3! ordered label roles times 4! assignments to leaves, or 144 comparisons. The four-label part of this particular archive contains only singleton-owner permutations with no union-preserving deletion. This classification is for the stated star and archive domain.

## Why the second write has opposite signs

The historical R caller computes t with `coordinate` and calls `normalize` on that row. Define an R edit as a primitive that actually changes R's membership, ignoring all other indices' edits. Initially R has two leaves.

1. For t=2 the original `normalize_four` expands every child support to the full palette before contracting. R lacks precisely two leaves. Its first two edits add them, so its root degree becomes 3 and then 4.
2. For t=3 the implementation operates on the four *complements* of the supports. R initially occurs in two complements. The first phase assigns each label one bin and removes its duplicate copies. For R this removes one complement copy, which adds one leaf to R. The remaining complement copy cannot be deleted until another exists. The target single-owner supports use all three labels, so R finishes on at most two leaves and must change again. Its second edit adds a complement copy, which removes one leaf from R. More generally, any path staying within one of t=3 forbids an R view containing all four leaves, since that would make τ=1. After reaching three leaves, a second positive edit would violate this bound.

Thus the original controller produces a signed change of +1 versus −1 on the receiver's second actual edit. This statement survives all placements of the four leaves and all assignments of the three labels to the ordered palette. It does not require a named output leaf or R to be the first palette label. The rule producing the edits remains essential.

## A fixed remote cell and a matched no-deletion run

Use the original palette A,B,C. Set S=B, R=A, T=C, with supports (ABC, B, C, AB) at leaves v1 through v4. A starts on v1 and v4. Its full root-inclusive mask is 19, using bit v for site v. The common full state in A,B,C order is [19,23,11].

| Input to the original R caller | Archived row, zero based | t | A's successive own masks, initial included | A leaf counts |
|---|---:|---:|---|---|
| No deletion | 2468 | 2 | 19, 23, 31, 15 | 2, 3, 4, 3 |
| B deletes at v1 | 1782 | 2 | 19, 23, 31, 15 | 2, 3, 4, 3 |
| B deletes at v4 | 2466 | 3 | 19, 27, 19, 23, 7 | 2, 3, 2, 3, 2 |

On its second change A adds **v3** in the v1 history and removes **v3** in the v4 history. That remote bit remains 1 and 0, respectively, to the ends of these paths. Both paths contain 14 primitive normalization moves. Both displayed writes also happen to be the fourth global move. The comparison is already defined by the second local move. A's first edit adds a leaf in both arms but its address differs. Immediately before its second edit its leaf count is equal in both arms and its full masks differ.

If one granted A a legal-move oracle, it could distinguish these preparations sooner. After B deletes at v4, only A covers v4. After deletion at v1, another index still covers every leaf. Both arguments above concern A's actual own membership history. The two histories are matched in A's own mask and counting marginal immediately after the source deletion. They are not matched in the full hypothetical command oracle. The separate same-site control below matches that interface too.

The rooted unweighted star on n leaves has root degree n and reduced Laplacian and Green inverse equal to the n-dimensional identity in the root-zero gauge. Consequently A has four versus two independent formal response directions at its second change. On the common sites (o,v1,v4) a fixed unit balanced drive from o to v1 still has the same potential (0,1,0). Nearest-ancestor projection of the same unit-ambient grade to the common A carrier also coalesces. Thus the observed quantity here is a change of A's retained geometry and a stored membership bit. A dimensionful force or a changed common-port gravitational response would require further physics.

**Rejecting path.** From the v1-deletion input [19,21,11] the following alternative reaches exactly the same t=2 canonical endpoint while retaining τ=2 on every step.

    [19,21,11] → [27,21,11] → [11,21,11] → [15,21,11]
                → [15,17,11] → [15,17,9] → [15,17,1].

Its A leaf counts at its first two changes are 3 and 2. The historical verifier accepts all six moves with zero profile excursion. Thus bare admissibility, even with the correct target and exact profile throughout, permits the opposite sign in the low branch. The actual low-branch expansion selects the reported signature. The high-branch prohibition against full coverage follows from the band constraint.

## Same-site control for passive loss and controller memory

A separate common start [19,3,31] has supports (ABC,C,C,AC). Compare deleting C or B at the very same leaf v1. A retains v1 throughout both paths. Its initial own mask, its counting grade (3,1,1), and the set of leaves covered by indices other than A are identical after either deletion. The full bare A-command interface is therefore identical under the earlier `receiver_move_interface` theorem. With unit counting, each deleted incidence has the same formal lost source vector `δ_v1−δ_o`. A does not need that grade for the normalization result.

The two resulting original R rows 1196 and 1882 compute t=2 and t=1. Both have 14 moves. Their full incidence states coincide at each position 1 through 12, starting at the restored common preparation and ending at [31,17,17]. At position 13 the t=2 row deletes A at v4, while the t=1 row deletes B there. A ends with three versus four leaves. Restarting the unchanged R caller on the restored common incidence state computes t=1 and yields the same no-deletion path in both restarts. Its global saved target and route carried the distinction while the incidence states agreed. The t=1 A-only trace is a prefix of the t=2 trace, so this pair alone lacks the two-sided local stopping criterion proved above. Giving both B and C universal coverage makes either source deletion give t=1 and the same A endpoint. Later common P1 transport of the unit counting grade on (o,v1,v2,v3) gives (2,1,1,1) in both arms.

## Evidence, earlier work and boundaries

For the default ordered R star the canonical compact supports give four singleton leaves across the first t labels. The first label occupies the initial 5−t leaves and each remaining used label occupies one. A legal deletion either preserves τ or raises it by one. If all old minimum covers fail, a surviving label at the edited leaf can be added to any old minimum cover, proving the upper bound. Otherwise an old cover survives. Hence the first label's terminal degree in the canonical output N obeys

    degree_first(N(after)) − degree_first(N(before)) = −1[the v16.26 root trigger fires].

The unmodified zero-argument producer recreated all 2,507 archived R rows including their complete paths. The replay separately applied the original path verifier and checked all 12,564 legal one-incidence deletions in this archive. The trigger fired for 2,708. It verified the complete two-site class of 144 and the same-remote-leaf second write in 40. These counts enumerate a fixed catalogue and imply no physical frequencies. [Replay program](check_active_holder_write.py) and [exact output](active_holder_write_results.json).

The October `profile_receiver_signal/RESULT.md` had already recovered the stateful R writer, terminal signal following a three-deletion preparation, retained target and restart control. The present comparison gives a structurally identifiable holder, one authentic source atom in each arm, two-sided discrimination before termination, and a legal same-endpoint path that falsifies the sign under weaker assumptions. It also controls for identical single-site loss and bare local commands in a different pair. The preceding five-site [loss-support proof](LOSS_SUPPORT.md) continues to describe the passive operation.

**INHERITED in software.** v16.26 `atomic` and its verifier, together with v16.53 `produce` R, the ordered state representation, `coordinate`, `normalize_four`, `cover.reconfigure` and `lift_root_path`. The last function writes the actual indexed bit then rereads the new state to enforce the global band. The receiver is an indexed view, which differs from an individual child leaf. At a canonical leaf endpoint `child_call` strips global label identities before calling the leaf normalizer and passes the singleton raw state [1] in either arm. The parent retains the index association. No physical child receipt is implied.

**SUPPLIED.** Preparation, choice and occurrence of the source atom, and passage of its returned incidence state to the original R normalization. The equality with historical R inputs is exact. v16.26's production loop tallies atoms. The v16.53 campaign starts from enumerated inputs. These entry points do not subscribe R to real pruning events. A physical observer's access to its membership, degree or own-edit occurrence is also supplied. **OPEN.** Identify an actual event law that enforces the distinguishing route or its sufficient local conditions, and identify a physical system that retains and can use the resulting change. The finite model supplies a controlled signal candidate before any physical time coordinate is introduced.
