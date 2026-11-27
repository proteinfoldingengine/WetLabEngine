# Why all fifty original paths left the exact surface

Use the same two labels, four named leaf charts, single-incidence moves and exact hitting number two as in [the surface result](RESULT.md). The v16.53 normalizer first adds every missing label in chart order and then removes labels outside the canonical target. The midpoint of that construction has both labels everywhere, with hitting number one. All fifty calls from exact starts pass through this one full state and take the same four remaining edits. From that midpoint the later retained states carry no distinction among the fifty starts when aligned at the midpoint. Earlier path frames are still in the returned trace. [Original construction](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py#L234-L251)

For every one of the fifty starts, the canonical target (A,A,A,B) can instead be reached with exact coverage throughout, using exactly one edit per differing incidence. This is a lower bound even in the relaxed model because a primitive changes one bit. The stock path uses more edits for 43 starts and ties this minimum for seven, while leaving the surface for all fifty. Starting at the target itself gives the largest difference: zero edits suffice and the stock path uses eight. Minimizing edit count alone cannot select exact coverage on the seven ties. The comparison paths are computed mathematical witnesses, with no claim that the original dispatcher selects them.

## Finite distance classification

Across all 2,500 ordered pairs including equal endpoints, breadth-first search and an original-verifier replay of a shortest exact path for each pair give the following classification. The unrestricted distance is the number of differing incidences; at an individual chart, changing singleton A to singleton B passes through the double support.

| Endpoints | Ordered pairs | Shortest exact length |
| --- | ---: | --- |
| Two opposite singletons swap addresses, the other two charts double at both endpoints | 12 | 6 edits versus 4 unrestricted |
| All other endpoints | 2,488 | Unrestricted distance |

The extra two edits in the swap have a specific role. Releasing either original singleton's exclusivity as a first step removes the only witness for one label. A spare double chart must become a singleton first. For example, begin with (A,D,D,B) where D denotes both. Change the second chart to A, change the first from A through D to B, change the fourth from B through D to A, then restore the second chart to D. Both singleton types exist throughout. A shortest unrestricted swap has only four moves, all at the exchanging charts; exactness precludes that first move. Restoring a spare chart costs at least two extra moves. Exhaustive enumeration establishes that this is the only excess-distance class in the four-leaf model.

The result separates the geometry of possible paths from the dynamics that selected the historical paths. The prepared target and the unit cost per primitive are supplied. An endogenous rule maintaining exactness, a receiver-owned log and a physical interpretation remain open. PR 179 separately reports an actual local size-word contrast for another operation.

[Replay script](exact_routes.py) · [Frozen counts and common suffix](route_counts.txt). Run on Python 3 with the same pinned historical demos directory as the parent result.

```bash
set -euo pipefail
python -B exact_routes.py "$DEMOS/v16.53-four-child-boundary" | diff - route_counts.txt
```
