# When a leaf deletion forces the next deletion to its parent

A conditional result on the native nested-support grammar. From one common state, the first of two consecutive incidence deletions can remove either label A or B. In either case, the rules determine the vertex and label of the second deletion. The two parent supports then differ at one fixed membership question. A single intervening addition gives a pair of histories that erase the distinction before it reaches the parent.

## Premises and provenance

- **INHERITED mathematical operation.** A finite rooted tree has fixed root support equal to the palette. Every vertex support is nonempty and lies inside its parent's support. A primitive toggles one incidence at one nonroot vertex and leaves a valid state. See `demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md`, “Carrier and extension,” blob `ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2`. The independent implementation is `verifier.py`, functions `profile_check` and `path_check`, blob `54e23706c170d0bb82c1b78161290145b6b99af7`. Integrated research source `e7e01bab68ba5171dacd91333f98d208d810dac3`. The two internal vertices of our binary example fall within the stated carrier.
- **SUPPLIED preparation.** The root o has children p and d. In turn p has children l and w. The palette is {A,B,C}. Initially o and p carry ABC, l carries AB, and w and d each carry C. The fixture and the fixed question “is A present at p?” are chosen once, before either source alternative. The source distinction is which label the first event removes. No two different initial preparations are required.
- **SUPPLIED event class.** The episode consists of two consecutive actual primitives in the support grammar, both deletions. Equivalently the result applies to every two-edge descending path starting from this state. The mathematical hypothesis contains no actor, location or label for either edit. We specify neither a probability for either source alternative nor a rule that produces two actual deletions. A path edge expresses order and requires no physical clock.
- **Open physical premises.** The project still needs independent evidence that a physical event or composite realizes this class, and that a surviving physical system holds and can interrogate the specific p-membership effect. The formal vertex state is preserved as a carrier through the episode. Its physical ownership and read access are unproved.

## Derivation

1. At a nonroot internal vertex v, the deletable labels are exactly the members of its support absent from the union of its children's supports. Necessity follows from nesting. For sufficiency, each child is nonempty, so after the proposed deletion at least one child label still keeps v nonempty. At a nonroot leaf all members can be removed individually when its support has size at least two. A singleton leaf permits no deletion. The root is fixed.
2. Every label at p initially occurs in a child, so p permits no deletion. The only movable leaf for a deletion is l. The first global deletion must remove A or B there. It leaves p at ABC.
3. Write x for the removed label. Now all leaves are singletons. At p the union of child supports is exactly ABC minus x. Hence there is precisely one deletion anywhere in the tree. It removes x at p. All leaves retain their supports and p remains nonempty. There is then no legal further deletion. These are the only two maximal paths made entirely of deletions from the preparation. A physically realized path could stop earlier.
4. The fixed function that returns one if A belongs to p, and zero otherwise, starts at one and stays at one after the first event on both branches. Its final values are zero after deletion of A at l, and one after deletion of B. Thus only the parent readout and its two mathematical values are needed to distinguish the alternatives after the second deletion. No instrument, access map, clock or probability law follows from this implication.

| First global deletion | Only next global deletion | Parent after the second edit | A present at p? |
| --- | --- | --- | --- |
| Remove A from l | Remove A from p | {B,C} | 0 |
| Remove B from l | Remove B from p | {A,C} | 1 |

The child supports at o always share C through p and d. At p, l and w have disjoint supports along both descending paths. The two internal hitting numbers therefore stay (1,2) in root-first order. Both complete paths have zero excursion for that exact target. The primary argument uses bare admissibility.

## Adverse continuations

**Stop after the first edit.** The parent and the selected parent effect are identical in the two branches. Occurrence of the second event matters.

**Allow a common addition.** After the first leaf deletion, add C at l in both branches. In each branch delete the remaining original label at l. The complete states now coincide, with l carrying C and p still carrying ABC. Remove A and then B at p in both histories. The common final state has p,l,w,d all at C and permits no further deletion. Across the two histories the successive parent supports are identical at every matched step, even though each history contains several deletions. The comparison uses bare admissibility. It does not require exact target (1,2) along the mixed histories.

**Fixed-profile control.** Even with an exact (1,2) profile at every step, the first event can be undone by adding its label back at l. Both branches return to the common initial state with the parent unchanged. At that state any common legal continuation can follow.

**Indexed ownership.** The complete column for label C, consisting of the vertices o,p,w,d, stays the same on both purely descending histories. The column for A already differs at l immediately after the first edit. The p effect stays blind at that point. The result concerns a fixed region p and a fixed membership effect. It establishes neither a write to a separate label owner nor a new bit learned by an otherwise entirely blind A-index between the first and second edits.

## Relation to prior work and what to test

`source_withdrawal_completion/WORKING_CONSTRUCTION.md` §§2–4 (blob `cc74a6d511439106a703c863c512cb0d3badeb13`) derives a child endpoint from a specified committed parent withdrawal. `first_pruning_own_view_review/RESULT.md` §§4–5 (blob `5f4a3758cfc59b9a7d023d541a8765801254943b`) restricts the response to one specified index. Here the direction is child to parent and every vertex and every label remains eligible for both deletions. The destination follows from ruling out all alternatives in this fixture. We make no general priority claim.

This reduces what must be supplied for the second mathematical edit. Its occurrence and polarity are still assumed, but its site and label are derived. The present example uses the same label at two addresses. It does not identify a separate receiver register, physical accessibility, the P1 address-contraction channel, a gravitational force or a measurable signature. A challenge that advances the physical question would locate an independent event/writer in the original implementation that enforces descent on this incidence carrier and supplies p's own read. A global verifier's ability to inspect p proves neither premise.

## Status of the computation

This is an unnumbered mathematical note. The five-state descending diagram and the controls were explored before the written freeze. An exploratory assertion that protecting the parent with additions at w eliminated all global deletions failed. Those additions can protect p while leaving deletions at w legal. No argument above uses that assertion. The submitted verifier checks the exact signed transitions against the historical implementation throughout the finite binary-tree, three-label state space, then follows every descending continuation from the declared fixture and tests both erasure controls. The dated run and review record are separate from the frozen argument.
