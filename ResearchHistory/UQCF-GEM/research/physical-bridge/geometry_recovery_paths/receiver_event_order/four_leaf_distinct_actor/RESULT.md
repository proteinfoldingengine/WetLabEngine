# When the source cut determines which other chart can withdraw

**Author replay, 26 November 2026.** In a preparation reachable from the six-chart fixture, A can withdraw leaf 1 or leaf 2. In either case, if the next union-preserving withdrawal belongs to a different chart, the state determines both its actor and its leaf. C alone can withdraw, and it retains the leaf A released. If A acts twice, the two histories reconverge with C unchanged. This is a conditional statement about the original withdrawal relation.

## Construction on the original carrier

Use the [six-chart four-leaf star](https://github.com/proteinfoldingengine/WetLabEngine/blob/de5056da7a5071a9634a3d5018fd3ec7e9fdc8ca/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/RESULT.md). The common Pin remains in every chart. The supplied preparation first adds 1 at C, then withdraws 1 at X, 1 at Y, 2 at Z, 4 at C, and 3 at B. Addition uses the bare fixed-carrier rule. Every withdrawal below was executed by the unchanged v16.26 atom. These steps can all precede the source choice, so the histories have one identical prepared prior. [Bare addition rule](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b8/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_move_interface/RESULT.md) · [Original atom](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py)

| A's supplied cut | All possible next withdrawals | C's leaves if the other chart acts | C's leaves if A acts twice |
| --- | --- | --- | --- |
| 1 | A cuts 2 or C cuts 2 | {1} | {1,2} |
| 2 | A cuts 1 or C cuts 1 | {2} | {1,2} |

Immediately before A acts, both 1 and 2 are held by exactly A and C. Only A holds 3, and only B holds 4. Once A releases one shared leaf, C is its sole holder. Either A or C can release the other shared leaf. Both continuations are terminal under withdrawals because each leaf then has exactly one holder. The common endpoint when A acts twice supplies a control even if a maximal sequence of withdrawals is required. Allowing additions changes the terminality condition.

## What C can distinguish

A snapshot after the C cut contains one leaf in either history. Swapping leaves 1 and 2 fixes every chart in the prepared prior and exchanges the complete source arms, including their final snapshots. Thus the address distinguishes the arms if identities are available, while a single unlabelled terminal chart has the same rooted shape. If C can retain its own **original** pre-preparation view and track leaf identity across edits, it has a comparison invariant under any one consistent renaming. Its original leaves were {2,4}. Its final leaf belongs to that original set in the A-at-2 history only. The two intersection sizes are zero and one. This comparison requires access to both local records. The prepared prior {1,2} alone gives intersection size one in both.

## Exact characterization on a flat star

Fix distinct actors A and C and two distinct leaves x and y which A can individually withdraw from one prepared state. At a nonroot leaf of a flat star an actor may withdraw precisely when it holds that leaf and another chart holds a copy. Withdrawing at A changes the legality of C's cut only on the withdrawn leaf, and only when its full holder set was {A,C}. Every other withdrawal option at C stays the same.

Consequently C has nonempty, disjoint sets of possible withdrawals in the two arms exactly when **both x and y have holder set {A,C} and every other leaf held by C is held only by C**. For necessity, every nonempty disjoint menu must have a leaf that disappears in the opposite arm. Only the two candidate leaves can do that, one in each arm. Any other shared leaf at C would be a common option. These conditions also suffice, since in each arm only the uncut member of the pair is removable by C. In particular the exchange symmetry of the two source columns is necessary throughout this class of bare ungraded stars.

If in addition every non-A withdrawal must belong to C in each arm, **every other leaf on the star must have a single holder**. Any further shared leaf would allow a non-A withdrawal, either adding a common C option or admitting another actor. Singleton leaves add no option, giving sufficiency. This result determines the other actor conditional on such a withdrawal. The atom admits A as well. No selection of a first actor, requirement to switch actors, or physical access to a history follows here.

## Minimum preparation and replay

For the original six indexed charts, four leaves, fixed A and C, and source choices 1 and 2, count all bare prepared states allowing both cuts. Each source leaf must include A and at least one of five other charts (31 choices). Either other leaf has 63 nonempty holder sets. This gives 3,814,209 preparations. The replay groups the two background columns by their withdrawal eligibility and distance, with their exact multiplicity. For each pair of source columns it computes eligibility by removing A directly. The shortest distance from the original fixture is the number of changed incidences because all new memberships can be added before obsolete memberships are withdrawn.

| Requirement | Indexed preparations | Fewest common edits before A acts | Preparations at that minimum |
| --- | ---: | ---: | ---: |
| Both arms give disjoint nonempty C withdrawal options | 1,024 | 5 | 2 |
| In addition, C is the only possible next actor other than A in both arms | 36 | 6 | 4 |

The first five edits above attain the first minimum. B can still withdraw 3 after either A cut. The sixth edit removes that alternative. The classification predicts the totals directly. For the first row either remaining leaf may omit C and have any nonempty subset of the other five charts, or be held only by C (32 possibilities per leaf). In the second row either remaining leaf has six possible sole holders. All counts refer to labelled states, with no probability on them.

To reproduce both the original-engine check and the incidence census, run the following from a WetLabEngine checkout containing this note.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_distinct_actor/replay.py ResearchHistory/UQCF-GEM/demos
```

The author replay used the v16.26 module at revision `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`. The reviewed earlier normalization result has different premises. This extension has received no independent review.
