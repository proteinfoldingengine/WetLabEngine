# A withdrawal can change what untouched charts can do together

Three charts hold one leaf. Before chart A releases it, B and C can both release it in either order, since A can retain the last copy. After A releases it, B and C each still have exactly the same holdings and the same individual possibilities as before. Either one can still release it. They can no longer both do so. One release by A has changed a relation between two other charts without sending either one a message. If withdrawals continue until none is legal, exactly one of B and C must release this leaf. The unchanged rule admits either outcome.

This case occurs on the original v16.29 example named ZERO. Its four saved states have identical cover profiles and height 1. They give the square for the releases by rows 0 and 1. The checker reproduces every archived state with the v16.26 atom and separately runs both possible resolutions by the remaining pair. The extra branch comes from the new replay. The archive stored a square built from supplied events. In its symmetric state after row 0's cut, exchanging rows 1 and 2 fixes the state, the source event, and the participant-neutral rule. A deterministic rule that respects this exchange cannot select just one of them on these inputs. Both endpoints are legal. Their indexed rows identify the surviving holder; exchanging the two participant labels exchanges the endpoints. [Original example data](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/EXAMPLES.json) · [Historical producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py#L53).

## Which groups are affected?

Work on the finite covered tree U. Each chart's row is an ancestor-closed set containing the root. A v16.26 withdrawal removes a nonroot local leaf from one row and must leave the union unchanged. Fix an accepted withdrawal by A at x. Let H be all other holders of x just before it. H is nonempty. For a set of other charts G, consider every finite sequence of successful withdrawals, keep the addressed withdrawals by members of G and erase the others. Include the empty sequence. This is a mathematical set of possibilities. The program need not record a group or observe this set.

**Theorem.** G's set of possible sequences shrinks exactly when x is a leaf of U and H is contained in G. If it shrinks, the missing sequences are precisely the old ones that withdraw x from every member of H. Every other old sequence is still possible. Thus for a leaf H is the unique smallest affected group. It is identified by the current holdings even when each member's entire individual action history remains possible. At an internal vertex every group of nonactors keeps its full set of possibilities.

**Proof.** Any projected sequence can be played in the same order with the other charts fixed at their original rows. Each participating chart has the same local leaves at its own moves. The frozen exterior contains everything that the interleaved exterior held at each point, so the union test still passes. The reverse implication follows by choosing just this sequence as the continuation. This equivalence concerns existential possibilities and imposes no scheduling choice on the model.

Before and after A's event, the initial rows of G agree. The frozen exterior changes only at x, and then only if H is contained in G. For any old sequence whose final group holdings still include x, every prefix retains x as well. All its original moves therefore still pass. When the exterior has lost x, an old sequence ending with no x in G must fail; under withdrawals x cannot return. If x is a leaf of U, all holders in H can relinquish it in any order in the old state with A retaining it, so the difference is real. If x has a covered child y, A could not have held y when it released its local leaf x. If H is contained in G, every holder of y was already in G. In every old continuation at least one member of G must still hold y and hence x. No old sequence can be lost. The argument uses the children of x in U, even when the ambient tree is larger.

For a leaf with h holders, the original same-union requirement forbids the joint removal of all h copies. A's withdrawal changes this to the prohibition on removing all h−1 remaining copies. At three holders this creates a pairwise conflict at that site. At two it makes the sole survivor's own release impossible. On a finite run continued to exhaustion, a leaf cannot end with two or more holders, since any of them could still release it. Either of the final two can release it immediately while the other must then keep it through every subsequent withdrawal. The choice to continue to exhaustion is explicit. The rule supplies no clock or probability law.

## The historical five-site census

| Smallest group with changed possibilities | Original source cuts |
| --- | ---: |
| No group of other charts changes | 1,472 |
| One chart | 10,310 |
| Two charts together, neither alone | 6,969 |
| Three charts together, no proper subset | 1,244 |

In 8,213 of 19,995 cuts the consequence first appears in the choices of more than one chart. These counts use the original campaign's distinct starting rows, at most four charts, and rooted shapes through five vertices. They count addressed cuts, not independent samples from nature. The one-chart figure reproduces the [earlier single-chart theorem](../receipt_remote_withdrawals/RESULT.md). A true cover trigger can coexist with no change at any group of nonactors. The new relation concerns legal sequences, independently of whether a cover number changes.

The native checker tries to withdraw the subtree rooted at x from each chosen group, children first, before and after each cut. Its whole per-shape event and receipt digests reproduce the original. The independent implementation rebuilds ordered event and group identities, both challenge outcomes, the cover increment and global height change. Both produce the same 1,929,509 uncompressed certificate bytes for 144,874 comparisons. Of these, 50,465 groups lose at least one word. Through four sites it additionally enumerates the entire global reachability graph, including intermediate repeated rows, and compares all projected endpoint sets for 28,524 event/group pairs on 1,198 states. An endpoint specifies which addressed withdrawals occurred. Since the local leaf checks are the same in both histories, filtering old words by this endpoint requires no extra assumption on the order. Full words were proved above; the bounded traversal compares endpoints.

## Does the receiver actually respond in the earlier handoff?

In [PR #162's original five-chart preparation](https://github.com/proteinfoldingengine/WetLabEngine/blob/b6d53c9b1c6f793697d0d43e4289e42e21e39992/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/compact_control/last_copy/cover_memory/snapshots/RESULT.md), both histories contain B's release at tip 5 and the same two background cuts E−2 and X−4. The two earlier source withdrawals by A differ between histories. We replay the exact saved fixture. The two common background cuts have different effects depending on the earlier history.

| Earlier B-at-5 trigger | Effect of E releasing 2 | Effect of X releasing 4 | What every complete continuation contains |
| --- | --- | --- | --- |
| 0 | Leaves F alone at 2 | Leaves A and F at 4 | Exactly one of A and F releases 4 |
| 1 | Leaves A and F at 2 | Leaves F alone at 4 | Exactly one of A and F releases 2 |

All 48 maximal paths in each arm include this site-specific release. In 24 F releases it, leaving a record in F's holdings, as previously found. In the other 24 A releases it and F keeps its entire prepared row. The two arms have two complete terminal states in common. Equal path counts describe the enumerated paths; the model supplies no weights. This calculation identifies which actual withdrawal is forced somewhere on a completed path, while allowing the source to preempt the receiver. The source arms already differed at sites 2 and 4; B's withdrawal at 5 alone does not transfer its numeric trigger there.

A further caller test was chosen after these path counts were known. The historical v16.26 factor procedure operates on a supplied initial state and a supplied final state. For each arm we gave it two complete endpoints differing only in whether A or F holds the compulsory site. Every other site's final owner was fixed across the pair. The same original procedure produced and verified a full path to each. Changing only this endpoint made the original actor at that site switch between A and F. This locates the choice in a real automatic caller. In the bare atom, the index and site are direct arguments; in the factorizer, the supplied endpoint already decides which of those two participants must give up the site. The five-chart replay enumerates the possibilities. None of these callers binds the write to F from the committed source event alone. [Historical atom and factorizer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py#L25).

The separate [PR #166 source-repeat control](https://github.com/proteinfoldingengine/WetLabEngine/blob/81903f31243144a82e2c3f478f100a86a3fad998/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_distinct_actor/RESULT.md) still reconverges under A's two releases with C unchanged. On the distinct-actor branch C's release retains A's first site. These conclusions coexist with the exact group constraint.

## Reproduce and interpret

Starting from the historical demos directory at e61d5b0e827f7b412824ad46021e2ad6cc6f7875, run

```bash
set -euo pipefail
python -B replay.py "$DEMOS" fresh.xz | cmp - results.json
python -B verify.py fresh.xz | cmp - verification.json
xz -dc fresh.xz | sha256sum
```

The uncompressed certificate SHA-256 is 53416324ebcf44251b019013cd19bec3accc1bc2b85338f734e4936bb4c0662f. [Scope frozen before execution](SCOPE.md) · [Complete compressed certificate](records.json.xz) · [Both fixture replays](results.json) · [Independent checks](verification.json).

The existing operation creates a constraint among a particular set of other participants from their original shared holdings. It supplies neither a participant-side receipt nor an operation making F act in preference to A. The shift from a shared constraint to a pairwise one takes place on the original leaf. Generating new shared sites, propagation between sites, scale dependence, and spacetime curvature remain separate open problems.
