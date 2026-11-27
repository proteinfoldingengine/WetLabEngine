# When do current holdings reproduce the receiver write?

The [previous release test](NESTED_HELPER.md) found 16 adjacent exact release/gain occurrences among the 72 successful two-label, root-target-two cases of v16.51. At each intermediate state, the original primitive could undo the source release or write the released label at one particular peer. Here we test whether the running normalizer's position was needed to recover its choice.

## One restart reproduces the full remaining path

Regenerate the original compressed certificate and check its Git blob. For each matched occurrence, call the original normalizer anew from the complete post-release holdings, with the same tree, label count, target profile and default palette order. Start with an empty diagnostic trace. Supply no event, receiver, phase or original path index. All 16 fresh calls return exactly the original sequence from that point through the endpoint. They represent four distinct post-release inputs across two tree shapes. Freshly starting just one edit earlier fails to reproduce the original release as the first step in all 16.

These post-release states have a simple structure. Each of the three top children has a single label. Nesting and nonempty supports then fix the label of every descendant in each branch. The live normalizer can reconstruct its local roles at such a state. The result is verified for the four input keys. It supplies no callback that makes the original program restart upon receipt of an event.

## Shortest exact completion resolves the forward-versus-undo choice

Use the original canonical endpoint and assign cost one per original primitive. The number of differing incidences between the post-release state and the target is a lower bound on every path length. Each archived continuation attains this bound with exact profile throughout. In each occurrence there are exactly two exact first edits anywhere in the tree. The inverse of the source release increases the number of differing incidences by one. The recorded receiver gain decreases it by one. Hence **every shortest exact completion starts with that receiver gain**. If the inverse is taken first, the sharp extra cost is two: after undoing, redo the release and take the original continuation.

| Tree | Post-release masks | Minimum exact edits to canonical target | Minimum with immediate undo |
| --- | --- | ---: | ---: |
| T | (127,897) | 12 | 14 |
| T | (15,1009) | 6 | 8 |
| U | (511,65025) | 24 | 26 |
| U | (15,65521) | 14 | 16 |

For the 12- and 24-edit cases, two entire branches differ from the target. Switching their order also achieves the incidence lower bound with a different first receiver gain and one unit of profile deviation. Both orders pass the historical path verifier. In the other two cases just one branch differs. The target and cost convention are supplied; this proof does not establish that the program derives its endpoint or generally minimizes path length.

## Restarting after every primitive

As a separate intervention, keep only the first edit from each fresh call, discard the remaining path, and repeat from its new holdings with the same parameters. Comparing complete masks detects recurrence exactly. Each of the four distinct inputs produces the receiver gain and later enters a two-state cycle away from the canonical endpoint. The first recurrent state occurs after three edits on T and five on U. This repeated restart policy was introduced for the test.

There is an implementation-independent obstruction to representing all original transitions by one deterministic rule on current holdings with fixed parameters. In the same original case 13, complete masks [911,127] occur at both frames 0 and 6. From the first visit the next masks are [907,127] (remove label 0 at site 2); from the second they are [911,119] (remove label 1 at site 3). Every frame in that run is exact. The same inputs cannot yield these two different deterministic outputs without some additional distinction. In the producer, recursive child normalization and later role transport occupy different parts of the same call. Across the 72-case bounded census, 11 of 323 distinct keys (tree, target profile, complete masks) have two observed successors when termination is counted as an outcome; case 13 witnesses the stronger move-versus-move ambiguity.

This locates where the stored informational state suffices for the observed continuation and where the software retains context outside it. A receiver-owned receipt, an endogenous invocation, and a physical interpretation remain open.

## Reproduction

[Script](restart_boundary.py) · [Frozen counts and cycle states](restart_boundary.txt) · [Historical producer and independent verifier](https://github.com/proteinfoldingengine/WetLabEngine/tree/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface). Historical compressed certificate Git blob: 571d38f08006b7023a65ec64cac77fe23e0db52a. The script was reproduced locally with two Python hash seeds. This extension has no separate independent model review.

```bash
set -euo pipefail
python -B restart_boundary.py "$DEMOS/v16.51-ternary-interface" | diff - restart_boundary.txt
```
