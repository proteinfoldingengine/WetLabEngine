# A label at a single leaf certifies a change across a whole remote subtree

Consider three top branches with two labels, exact root hitting number two, nonempty nested supports and one-incidence edits. Begin with monochrome branches (B,A,B), as in historical cases 14 and 302. Pick any terminal leaf in the middle branch. No target, shortest-path condition, ordering between branches or irreversibility assumption is used below.

**Current-state statement.** If this leaf holds B, its branch root must hold B. At least one outer branch root must lack B; otherwise B alone would cover all three branches. With only two labels and nonempty nested supports, the root lacking B and every one of its descendants must hold only A. Each vertex in that outer branch began B-only. Thus every one of those vertices has acquired A and released B. The inference uses exactness at the time of observation and the known initial state. It does not require exactness at all earlier steps. A sample does not identify a particular past release.

**Interval statement.** If the leaf holds both labels, its branch root holds both. The two outer roots must then be opposite singletons, and their complete descendant holdings are fixed by nesting. As long as the leaf keeps both labels and coverage remains exact, no primitive can change any vertex in either outer branch. Switching the assignments would require an intermediate double or empty outer support. Either is inadmissible. The leaf certifies the restriction; the ternary interface already imposes it whenever the middle root is double. If the leaf keeps only B, some outer branch must still be A-only, but its identity can switch while the leaf's own support stays constant.

## How much remote change is required?

For a specified A-only outer branch with s vertices, the first dual state at a middle leaf is at least 2s+d primitive edits away from the initial state. Here d counts vertices on the path from the middle branch root through that leaf, including both. The outer branch has to acquire A and release B at every vertex. B has to be added to each of the d middle vertices. These edits are disjoint. The bound is attained on these trees: add A throughout the outer branch from its root down, remove B from the leaves up, then add B along the middle ancestry path. The other outer branch keeps B throughout. Old and new common labels preserve every required internal hitting number. The computation verified every shortest distance independently in the full connected exact graph.

| Case and leaf | Minimum edits with left subtree A-only | Minimum edits with right subtree A-only |
| --- | ---: | ---: |
| T, leaves 5 and 6 | 8 | 8 |
| U, leaves 6 and 7 | 9 | 17 |
| U, leaf 8 | 8 | 16 |

These are minimum numbers of primitives, without a physical clock or equal probability of paths. On U a single observed dual leaf certifies at least six prior remote incidence changes, since even the smaller outer subtree has three vertices. Knowing which side switched can raise the bound to fourteen remote changes.

## What the recorded data distinguish

At each of the five tested terminal leaves, the original normalizer and the reversed-traversal control gave the same complete local word A → AB → B. At its first dual state the original run had converted the left subtree to A, while the reordered run had converted the right subtree. Both have the same initial and final full states. The single-leaf projection suffices to infer that some outer branch switched; identifying which one requires additional information.

The original software stores masks by label. In the full B-indexed row, the outer roots missing B identify precisely the A-only outer subtrees. For both routes, that address was already present as an absence in the B row immediately before the middle leaf gained B. The leaf gain changes the B bit for that leaf; the A-indexed row is identical before and after. This distinguishes a current-state inference at the leaf from the information available in the full label-indexed view. It does not establish a participant-owned event receipt or local access to an interface-wide profile check.

Exhaustive traversal from the two starting priors gave 48 states/60 undirected edges for T and 228/468 for U. Restricting to states where a chosen middle leaf holds both labels splits the reachable induced graph into exactly two components, one for each frozen outer assignment. Restricting to a B-only leaf permits the exterior identity exchange. [Enumeration and actual frame numbers](leaf_witness.txt).

## Controls

* **Allow the stock one-unit deviation.** Hold every outer vertex fixed and add B down the middle ancestry path, then undo those gains. This closed walk has the same complete leaf word A → AB → A as an exact walk that converts an outer branch, reaches that leaf, and retraces. The original independent path verifier accepts both walks, with maximum total deviations of one and zero respectively. Local repeats were removed; no global step counter was supplied. An observer with only the leaf word cannot certify exact coverage.
* **Give the interface a fourth child.** Even if exactness is mandatory, one dual leaf no longer freezes the exterior. Keep that chart dual, begin with exterior (A,B,B), change the middle exterior chart B → AB → A, then change the first A → AB → B. The original v16.53 four-child verifier accepts all four steps with zero deviation. Two held doubles at distinct top charts do freeze the other two. More generally, with n charts, n−2 held doubles leave two required opposite singleton witnesses; with at least three remaining charts there are configurations in which those witnesses can move.
* **Source provenance.** Case 14 and case 302 default paths are original v16.51 records, reproduced to Git blob 571d38f08006b7023a65ec64cac77fe23e0db52a. The opposite orientation, closed walks and four-chart intervention are constructed controls. Only the default traces are described as historical. External independent review of this extension is outstanding.

[Original v16.51 producer and verifier](https://github.com/proteinfoldingengine/WetLabEngine/tree/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface) · [Original v16.53 four-child verifier](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py) · [Earlier ordering result](ORDER_CONTROL.md)

```bash
set -euo pipefail
python -B leaf_witness.py "$DEMOS/v16.51-ternary-interface" | diff - leaf_witness.txt
python -B four_lock_control.py "$DEMOS/v16.53-four-child-boundary" | diff - four_lock_control.txt
```
