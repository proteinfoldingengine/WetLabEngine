# Nested coverage selects one helper and identifies its next eligible peer

[The four-leaf exchange](EXACT_ROUTES.md) needs one of two spare charts. In original v16.53 template C the four top children consist of a binary branch and three leaves. Keep two labels A and B and the original target (2,2), meaning hitting number two at both internal vertices. A double is a support containing both labels. This analysis first restricts every intermediate state to the exact target. The historical verifier separately admits a total deviation of one.

## Which chart can act?

Exactness inside the binary branch forces its two children to be opposite singletons. Nesting forces the branch itself to be double. A single edit cannot reverse the two children's assignments while preserving the inner profile. Thus the two possible internal assignments give two disconnected components. In each component the remaining three leaves must collectively contain an A-only and a B-only support. Their graph under primitive edits is precisely the earlier 12-cycle. The exact four-chart surface has been reduced to its equator by an inherited constraint inside one participant. No chart was manually frozen to derive this result.

Consider any prior where the three leaves hold A, B and a double. Call the double leaf H. Neither singleton leaf can gain a label because that would erase its sole singleton type. Neither can lose its only label. The binary branch has no exact primitive. Therefore, if any exact primitive happens, H must act first. There are two choices, retaining A or retaining B. Suppose H keeps A. There are now two A-only leaves and one B-only leaf. The possible next edits are for H to regain B (the inverse), or for the original A-only leaf to gain B. Retaining B gives the exchanged statement. The known state selects the first actor, and its actual release selects the only next actor and label other than undoing that release. Exactness alone permits stopping, undoing or later backtracking. No forward scheduler is derived.

## Exchange controls

Swap the two singleton leaves, restore H to double and retain the same internal state. Breadth-first search over all six non-root supports, classified by the independent historical verifier, gave these distances at every one of the 12 indexed priors.

| Constraint throughout the path | Minimum primitive edits |
| --- | ---: |
| Both profiles exact | 6 |
| Both exact, H held fixed | Unreachable |
| Outer exact, inner may deviate by one, H held fixed | 10 |
| Inner exact, outer may deviate by one, H held fixed | 4 |

The ten-edit alternative explains the role of the inner constraint. To use the binary branch as the spare, change one child from its initial singleton to match its sibling, withdraw the newly unused label at the branch, perform the four edits of the swap, and reverse the three setup edits. At the time when the branch is a singleton one of its children must have changed labels. The lower bound counts two edits there before and two after, two at the branch, and four at the exchanging leaves. Relaxing the outer constraint instead permits the direct swap by temporarily losing the last witness of a singleton type.

These are legal constructions. All six stock template-C campaign calls for these parameters took a permitted excursion. The three inflated starting specifications put H at double initially; each stock path left exactness at its first move. Those calls do not demonstrate execution of the exact-helper construction.

## Actual receiver write with the same successor criterion

In the historical v16.51 ternary archive, case 14 frames 5, 6 and 7 give masks [127,899], [127,897] and [127,913]. Before the release, the top children at sites 1, 4 and 7 hold double, A and B respectively. Both descendants of site 1 hold A. The unique exact primitive changing any top row is for site 1 to release B; two possible edits at its descendants are also exact. Holding site 1 at double, even while permitting arbitrary exact edits elsewhere, leaves site 4's support invariant in all seven reachable full states. The opposite singleton witnesses at sites 4 and 7 cannot change one at a time while site 1 stays double.

After the recorded release, exactly two primitive changes anywhere in the tree preserve all exact coordinates. They are the inverse gain at site 1 and a gain of B at site 4. The original producer executes the latter. Among 72 successful original cases with two labels and root hitting target two, we found 16 adjacent exact release/gain segments at distinct top sites sharing this behavior. The scan required the same label, all three frames exact, and the premature receiver gain alone lowering the root hitting number to one. For every hit we separately enumerated all single-bit edits at **every** non-root site and checked both the pre-release top choice and post-release pair of options. These are indexed occurrences; they need not be independent examples.

The input state determines the only possible forward continuation *conditional on an immediate exact edit other than reversal*. The original code made that continuation inside its prepared call. It still had a supplied target and ordering. A local observer's later double support cannot by itself distinguish every route to that state or prove receipt of the release record.

## Reproduction and sources

The numerical tests were run locally. The v16.51 code regenerated the complete historical gzip certificate to Git blob 571d38f08006b7023a65ec64cac77fe23e0db52a. The v16.53 test enumerated all 729 nonempty assignments before admission and replayed each reported shortest witness against the historical path checker. No independent model review of this extension has been obtained.

* [v16.51 original certificate](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/evidence/reproduction/scientific/CERTIFICATE.json.gz)
* [v16.53 template and producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py#L258)
* [Nested test](nested_helper.py) and [results](nested_helper.txt)
* [Original-path scan](archived_successor.py) and [results](archived_successor.txt)

With the corresponding historical demo directories available, rerun:

```bash
set -euo pipefail
python -B nested_helper.py "$DEMOS/v16.53-four-child-boundary" | diff - nested_helper.txt
python -B archived_successor.py "$DEMOS/v16.51-ternary-interface" | diff - archived_successor.txt
```
