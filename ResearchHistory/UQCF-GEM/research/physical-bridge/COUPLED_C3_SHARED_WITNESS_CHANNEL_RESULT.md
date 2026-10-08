# C3 shared-witness channel — author-side analytical candidate

Date: 2026-10-08. Status: AUTHOR-SIDE PROOF CANDIDATE; independent verification/review/publication audit NOT completed.
Scope frozen at 6b38dddb62b34ced1098c88f214b0190b2ebec7c. This does not alter the closed core-history theorem.

## 1. Native relation and exact observation fibers

Use exactly the frozen four labelled roots and attempt/outcome relation. Let x and y indicate spectator w on roots 1 and 2. Core pairs A1,...,A4 are pairwise disjoint; w is outside their union. Floors are 2.

**Lemma.** tau(x,y)=4-x*y.

Roots 3 and 4 each require a hit from their own core pair, disjoint from all other supports. If x=y=1, w hits both first roots, so three labels suffice; at least one label for each of the three mutually disjoint groups (first-two-root union, A3, A4) is necessary. Thus tau=3. Otherwise S1 and S2 are disjoint: when at most one contains w they share no label. All four roots are then pairwise disjoint and nonempty, so four hits are necessary and sufficient. This proves tau=4. Every full root contains its two core labels, so all floors are valid. Every syntactically valid allowed toggle moves among these four admissible states and preserves the band.

Core projections, core-only miss counts and floor-validity are independent of (x,y). Therefore the exact observation fibers are

    tau=3: {(1,1)},
    tau=4: {(0,0),(1,0),(0,1)}.

This formula concerns the global minimum transversal size, not a selected cover or a new measurement variable.

## 2. Observable synchronization witness

An observed snapshot with tau=3 certifies x=y=1. Neither hidden root's support is read directly. The certificate follows from actual relational overlap and the already assumed tau observation.

Attempting +w on root 1 followed by +w on root 2 supplies a native route to the synchronization state if the required additions actually commit (an already-present incidence needs no addition). All states and committed moves preserve floors and band. This is a reachability statement, not a promise that two attempts succeed. A policy may repeat attempts but, from an unsynchronized initial state, an all-rejection execution stays unsynchronized indefinitely. No bounded or eventual synchronization is proved without a further progress premise.

No unknown initial bits are reconstructed from synchronization: the same final (1,1) can result from different initial states and actual additions.

## 3. Reusable observed-commit channel after synchronization

Let k be a prefix at which tau=3 has been observed. Thereafter freeze root 1 and issue only attempts to toggle w on root 2, with exactly the declared actual-toggle-or-NO-OP relation and no other writers.

**Theorem.** For every subsequent observed prefix n>=k,

    x_n=1,
    y_n=4-tau_n.

Consequently, every actual root-2 toggle is detectable from tau changing, and every unchanged tau certifies that no root-2 incidence change occurred in that attempt.

Proof. At k the observation-fiber lemma gives x_k=y_k=1. No permitted later action changes x, so x_n=1 inductively. Substituting into the proven formula gives tau_n=4-y_n. At each attempt, the outcome relation allows either no change or exactly the commanded root-2 toggle; with x fixed, these outcomes have distinct tau values. The relation contains no delayed or compensating writes, so equality/difference of consecutive observed tau values distinguishes these two outcomes exactly. This proves the statement for every prefix, including arbitrarily many rejections. A policy can choose the next command from this retained decoding without a hidden-support read.

The decoder uses the inherited global tau coordinate. There is no separately supplied success acknowledgement. The theorem does not claim tau is physically measurable or cheaply computable by an internal observer.

## 4. Observable payload cleanup and renewal

After synchronization, attempt -w on root 2. If tau changes from 3 to 4, then y=0 is certified while the reference incidence x=1 remains. If it stays 3, y remains 1; no cleanup is credited. Repeated rejected deletion attempts do not establish cleanup.

From the certified y=0 state, attempt +w on root 2. A change 4 to 3 certifies its actual addition. A NO-OP leaves tau=4 and y=0. Thus alternating observed successful deletion/addition renews the same decoding interface for any finite number of actual cycles. Finite completion of requested attempts is not guaranteed.

Only the payload incidence on root 2 is being cleaned up. The anchor on root 1 remains present and known. If root 1 is later deleted while y=0, tau stays 4, so this channel does not certify anchor removal. It also does not restore arbitrary unknown initial spectator configurations. Those restrictions are part of the result, not discarded overhead.

## 5. Refuting the overextensions

- Before synchronization, tau=4 allows both y=0 (state (1,0)) and y=1 (state (0,1)); applying y=4-tau there is false.
- If root 1 is allowed to change silently, a transition (1,1) to (0,1) yields tau=4 despite y still being 1. The fixed-anchor/no-other-writer premise is necessary for the decoder.
- An all-rejection run starting at (0,0) never produces tau=3. Native admissibility alone does not imply synchronization progress.
- With w confined to only one of the first two roots and no possible shared overlap, tau remains 4 through its toggles. The signal is generated by cross-root sharing, not by the mere existence of a spectator.
- If exact tau is removed from this frozen observation and only core projections, core miss counts and floor validity remain, all four states have identical observations. The channel has not derived tau access from those other coordinates.

## 6. Novelty and remaining obligation

The static two-root shared-spectator example was already a rejecting control in the prior core-history theorem. The present candidate uses that native overlap as an observable synchronization witness and proves a repeatable, transcript-decodable spectator-edit and payload-cleanup channel after synchronization. It removes the need for a separately initialized hidden-anchor bit in the synchronized phase: the tau=3 observation establishes the anchor's presence. It does not guarantee reaching that phase.

This is a conditional active information channel, not another blanket observer impossibility. Its unresolved prerequisite is access to the inherited exact-tau observation; its independent unresolved operational prerequisite is progress when attempts may reject. No new observer primitive, clock, energy, geometry or physical force is derived.

Before any scoped closeout, independently enumerate the frozen four-state/four-command outcome relation, require exact graph identity equality, exercise the false-decoder and corrupted-record controls in the scope, obtain a fresh mathematical review of this source, and perform a separate publication audit with immutable readback. Those obligations are still unfulfilled here. Broader C3 and C4-C6 remain OPEN.
