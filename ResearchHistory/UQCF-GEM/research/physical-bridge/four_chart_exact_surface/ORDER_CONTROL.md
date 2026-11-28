# A choice of first receiver becomes forced after one subtree has switched

Original v16.51 cases 14 and 302 start with monochrome top subtrees (B,A,B) and finish at (A,B,A). The original producer visits the subtrees in the order left, middle, right. A second call with the two outer branches exchanged in its traversal visits them in the opposite order. We carry the complete subtrees and their holdings through the permutation and map every output back to the original chart addresses. The two complete physical starting states match, as do their two endpoints. The counterfactual uses the unchanged producer. Its reordered input is an explicit experimental choice.

| Original case (zero-based) | Sizes of the three subtrees | Original first site | Alternative first site after mapping back | Edits in each path |
| --- | --- | ---: | ---: | ---: |
| 14, template T | 3, 3, 3 | 1 | 7 | 18 |
| 302, template U | 3, 5, 7 | 1 | 9 | 30 |

Both paths for each case pass the original verifier with exact profile at every primitive. They have no common complete intermediate state. For each individual subtree, its entire sequence of retained states is identical between paths once consecutive repeats are removed. A reader with the three separate local histories but no relative order cannot recover which subtree acted first. The initial archived paths are reproduced from the original campaign; the reverse-order counterparts are constructed controls.

## Exact shortest choices without numerical case targets

We focus on a ternary root, two labels, and three nonempty initially monochrome subtrees. Both colors occur, so the measured root hitting number is two. Nesting forces all descendants of a singleton root to hold that same singleton; their internal hitting numbers are one. For each tested run we computed the profile with the original verifier on the current state and passed that vector to the producer. This eliminates lookup of the case's target-profile vector at these exact starts. Requiring that profile to persist and fixing the endpoint remain mathematical conditions. The stock routine generates a canonical endpoint using its convention for child and palette order.

Let m count how many subtree colors differ between the initial and desired monochrome triples. All mixed triples, initial and final, are allowed. For a differing subtree of size s, every vertex must acquire one label and release another. Its irreducible cost is 2s single-incidence edits. Summing those costs bounds the full route length. A shortest route attains this bound by expanding the new label from root to leaves and removing the old label from leaves to root, choosing the order of the subtrees as follows.

| m | Possible first receiver sites on shortest exact paths | Reason |
| ---: | ---: | --- |
| 0 | 0 | The target is present. |
| 1 | 1 | Only the differing subtree can make an edit directed towards the target. |
| 2 | 1 | The two differing subtrees have opposite colors. The one sharing its initial color with the fixed subtree moves first to keep both singleton types present. |
| 3 | 2 | Either member of the initial majority pair can move first. The original minority subtree must switch second, before the other majority subtree can switch. |

At an initially monochrome subtree only its root can gain the incoming label. While that root holds both labels, the other two top charts must be opposite singletons. Their descendants cannot change. A shortest route cannot spend an edit restoring a bit to its initial value. Hence the chosen subtree finishes switching before another begins. The combinatorial restriction determines the order of roots as above, even if descendants within a subtree admit several edit orders.

This identifies precisely when the earlier [unique shortest receiver](RESTART_BOUNDARY.md) appears. At the initial antipodal triple two choices exist. After one majority subtree finishes its switch, m falls to two and only the original minority branch can go next. After that switch, just one branch remains. For T, swapping the two equal-shaped majority branches preserves the initial state and target on the unordered tree. Neither of the two possible first edits is fixed by that symmetry. A deterministic rule invariant under these branch exchanges cannot select a single first edit there from those data alone. For U the branches have distinct shapes, so that symmetry argument is unavailable; the equal cost and the two exact routes still hold.

## Independent finite checks

The original normalizer was run on every mixed monochrome triple, all six traversal orders and both palette priorities on each tree: 144 primary calls in total. Every path was checked after mapping its coordinates, and its length compared with the differing-incidence lower bound in the common coordinates. A further color-renaming control in each call swapped both label identities and palette priority together. The complete paths then agreed after mapping labels back. Reordering traversal while keeping addresses attached to the same physical subtrees is a change to the producer's priority convention.

For all 36 ordered endpoint pairs on each tree, a separate recursion checked every potential first bit change towards the target and whether an exact completion from that change could attain the lower bound. The sets of possible first sites agree with the table and with the exact normalizer paths among the two traversal/priority combinations giving each endpoint. For the twelve pairs per tree at m=2, one of those combinations used a one-unit excursion. No new automatic traversal rule or receiver-owned event register was introduced.

The complete v16.51 certificate reproduced to historical Git blob 571d38f08006b7023a65ec64cac77fe23e0db52a. The theorem and the checker target finite monochrome interfaces under the original primitive and exact coverage. Independent external review of this extension remains outstanding.

[Replay](order_control.py) · [Frozen counts](order_control.txt) · [Original producer, verifier and certificate](https://github.com/proteinfoldingengine/WetLabEngine/tree/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface)

```bash
set -euo pipefail
python -B order_control.py "$DEMOS/v16.51-ternary-interface" | diff - order_control.txt
```
