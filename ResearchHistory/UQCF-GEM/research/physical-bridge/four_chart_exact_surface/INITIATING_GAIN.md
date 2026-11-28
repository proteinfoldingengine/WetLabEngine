# A unique source gain precedes a receiver write in the same v16.53 call

The source and all three candidate receivers begin with the same holdings in both experimental arms. Both marker labels, 0 and 1, are available at the source. The original normalizer generates a gain of label 3 at the source, then writes 3 into exactly one receiving branch and removes one marker there before completing the corresponding source withdrawal. The caller passes no gain, withdrawal, destination or replacement label. The construction supplies a tree, an exact starting state and an invocation. The passed hitting profile is computed from the starting holdings.

Only one remote evidence leaf differs between the arms. Its marker m is 0 or 1. The newly generated source gain is identical in both arms. The value that distinguishes the arms is which marker is cleared during the ensuing replacement. This is a prepared asymmetry and an executed interaction in a finite software model.

## How the operation is generated

Three ternary junctions use the original unique-pair overlap rule. At the outer junction the child continuing toward the receivers has labels 0–5, and its two siblings hold m and 6. At the middle junction the continuing child has 0–4, and its siblings hold 2 and 5. At the inner junction the continuing child has 0–3, and its siblings hold 3 and 4. At each junction the common label is promoted to the front of the continuing child's local order. Thus the local order at the four-child junction is (3, 2, m, u), with u the other marker. Every global ordering gives this same order when the evidence consists of one marker.

At the four-child junction the source branch holds {0,1,2}. Its three siblings each hold {0,1,2,3}. Below the source, A, B and C have the same ternary shape and identical initial root supports {0,1,2}. At precisely one candidate its three leaves hold distinct singletons 0, 1 and 2. Each leaf of each other candidate holds only 2. The original recursion therefore computes widths 3, 1 and 1. Moving the width-three condition changes only tip holdings in the preparation.

1. The four-child junction first normalizes its children. Inside the source the available local order is (2,m,u). The width-three candidate must retain all three. The narrow candidates each retain 2. Only the wide branch and one of its leaves still hold u below the source.
2. The four-child expansion finds precisely one missing incidence, label 3 at the source. Its original plan generates that gain. No traversal order can change this choice. The canonical target for the source has three labels, the set {3,2,m}. The same plan therefore schedules removal of u. Both candidates were available when the plan was built.
3. Before removing u, the writer scans its proper descendants. Their used labels are exactly {0,1,2}; the source now holds {0,1,2,3}. Label 3 is the unique available replacement. Nesting requires every descendant still holding u to release it by the time the parent does. The stock writer adds 3 to the wide root and the occupied tip, then removes u from the tip and wide root, and finally removes u from the source. Only this candidate receives 3 through completion of this source withdrawal. Which named tip holds u inside it can depend on order.

Consequently the six edits projected onto the source subtree are fixed up to the tip identity: source gains 3, wide root gains 3, tip gains 3, tip releases u, wide root releases u, source releases u. The first gain is an actual stored source edit and is required for subsequently introducing 3 at the receiver under nesting. The receiving edit precedes commitment of the source withdrawal. The upper overlap calculation and prospective source plan already determine which marker will be withdrawn.

## Measured trace

The table uses the default branch and palette order and places the width-three pattern at A. A frame is an index in the stored sequence. The two complete source subtrees were identical at preparation.

| Remote evidence | Source gains 3 | A gains 3 | Source completes withdrawal | A's root after the replacement |
| --- | ---: | ---: | --- | --- |
| 0 | 37 | 38 | Releases 1 at frame 42 | {0,2,3} |
| 1 | 33 | 34 | Releases 0 at frame 38 | {1,2,3} |

Both runs begin A's record with {0,1,2}, pass through {0,1,2,3}, and reach the indicated retained state. The final canonical endpoints of the whole runs agree. A local software frame measures the lifetime of a mathematical distinction without assigning any physical duration.

## Tests of necessity and provenance

- **Attempt the planned withdrawal before the source gain.** With the actual compact holdings and the same source withdrawal, the unmodified lift rejects the attempted first step because it would bring the parent below its required width of three. Both default marker arms give this outcome.
- **Fill the missing incidence before calling the program.** This changes only the initial source bit for label 3. The source plan still removes u, but now it has no gain at the source and invokes no clearance helper. The receiver gains 3 during the earlier normalization. For each marker and all six orders of the wide branch's leaves, the receiver root's *complete* sequence of distinct holdings equals that of the corresponding initially unfilled run. This directly limits what a root record can certify about the initiating event. The four-site histories of its root and leaves do differ at fixed order. Allowing a different leaf order even gives a matched four-site prefix through the first retained {2,3,m} root in each marker arm. The script reports the exact orders.
- **Give the remote evidence leaf both markers.** The local source still executes a gain; the earlier overlap selection now has two choices. Reversing the palette reverses the retained marker at A. This control retains the source and destination structure and locates where the evidence for a unique value ends.

We ran 612 matched pairs across 204 enumeration settings and three placements of the wide branch. All 1,224 full paths passed the independent historical verifier. The script captures the actual four-child plan and clearance arguments, verifies the unique spare, checks the ordered bit edits in the stored path, and verifies endpoint agreement in each pair. Enumeration included individual sibling permutations and every ordering of the four junction children crossed with every ordering of the three candidate receivers while varying the remaining traversal and palette. The structural claims use the width and incidence arguments above. The common-prior and prefilled controls are explicitly constructed comparisons.

[Original implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Runnable check and pins](initiating_gain.py) · [Results](initiating_gain.txt) · [Raw matched windows and site map](initiating_gain_trace.json) · [Previous receiver result](STRUCTURAL_RECEIVER.md)

```bash
set -euo pipefail
python -B initiating_gain.py "$DEMOS/v16.53-four-child-boundary" | diff - initiating_gain.txt
python -B initiating_gain.py "$DEMOS/v16.53-four-child-boundary" --example | diff - initiating_gain_trace.json
```
