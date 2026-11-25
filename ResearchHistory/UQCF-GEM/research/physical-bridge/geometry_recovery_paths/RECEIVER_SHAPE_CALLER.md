# An existing operation reads the source-dependent holder of a fixed leaf

With the receiver prior and initial geometry fixed, changing which equal-grade source leaf is pruned changes the holder that v16.39 reads for its first transfer. In the matched example it reads the source in one history and the receiver in the other. The transfer acts on the same leaf, goes to the same destination, and comes from the original implementation. Both histories end with the same chart records. This is a result about an invoked route constructor in a three-chart preparation. The original chart 12 experiment had a different preparation.

## The two histories

Let a nonroot fork p have tip children a, b, c. In the anchored preparation the root has another child d. All three charts hold the root and p. Source S holds a,b,c, helper H holds a and the separate leaf d, and receiver R holds b. Their initial sizes 5, 4, 3 identify the charts even if their numerical indices are hidden. The fine grades are 5 at the root, 3 at p, 2 at both a and b, 1 at c and 4 at d. In the original five-node control d is absent. Its two single-tip charts are interchangeable under a simultaneous exchange of their tips. The anchored experiment removes that ambiguity.

Use v16.26 to delete either a or b from S. Each event raises the local cover number at p from 1 to 2 and raises the source's retained atom at p from 3 to 5. R is identical immediately after either event. Supply the same target to both calls to v16.39: H holds a,b, S holds c, R holds none of the fork tips. Keep all other vertices as prepared. The profile at each endpoint is 1 at the root, 2 at p, and 0 at every tip.

| Inside the historical call | S deletes a | S deletes b |
|---|---|---|
| Unique minimum cover of the children of p | H and S | S and R |
| Holder of (a,b,c) after removing surplus copies | (H,S,S) | (S,R,S) |
| Receiver's retained P1 vector (root,p[,b]), anchored preparation | (9,8) | (9,6,2) |
| First transfer reads the old holder of b | S | R |
| Transfer materialized by the constructor | Add b to H, remove b from S | Add b to H, remove b from R |
| Receiver at the common endpoint | (9,8) | (9,8) |

Both calls make an actual receiver edit. In the first history R loses b while the surplus copies are being removed. In the second it loses b when the first transfer finishes. The receiver's grade at p differs at the existing entry to that transfer. The distinction has disappeared at the shared endpoint.

### Why the holder is forced within the call

After cutting a, H alone holds a and S alone holds c. They must both participate in every two-chart cover, and only S among them holds b. After cutting b, R alone holds b and S alone holds c. They must both participate, and only S among them holds a. Therefore the minimization and the choice of a keeper for each tip have unique answers in both histories. The private leaf d leaves that argument unchanged. Since p is active in the archived constructor (its cover number is 2), the three tips are the child blocks that its local operation processes. This also explains why a constructor that restored deep tips in the earlier two-chart case can take a different route here.

For the supplied target (H,H,S), the first singleton assignment (H,S,S) differs at b alone. The other assignment (S,R,S) must first replace the disappearing holder R by the newly used holder H, which also acts on b alone. The original `local_path` passes the very list returned by `shrink(initial)` into the closure `recolor`. That closure reads `current[i]`, appends the joint old/new holder mask, and then the new mask. The outer `build` materializes each one-bit change in its chart path. The trace records the old holder at function entry, checks list identity, and checks the three consecutive materialized states at that address for every transfer. No new callback selects the receiver, transfer, or stopping step.

This is a read of a joint holder mask in the route constructor. The materialized receiver vector is calculated separately with the archived P1 push. In v16.39's original campaign, `produce` selects endpoint representatives from the graph record and passes their chart masks and the cover profile to `build`. Neither that call, its shrink, nor its transfer receives the P1 numbers. Local access by the receiver and an event-driven invocation remain open.

## A fixed question about the receiver

For a prefix-closed retained view Y, let P push each fine grade to its nearest retained ancestor. A fixed linear question f on the fine grades can be computed from Pz for every z exactly when f is constant on every fiber of that ancestor map. Indeed a fiber-constant coefficient vector defines a linear functional on the retained coordinates. If two coefficients differ in one fiber, moving a unit between the two fine entries preserves Pz and changes f. Starting with all entries equal to two gives two strictly positive witnesses.

For the question “what is the fine grade at b?”, recoverability holds exactly when b belongs to Y. With b absent, the fork and b lie in the same fiber. At the first transfer the same fine question consequently fails in the first history and succeeds in the second. In both histories the fine answer itself is 2. The same rank test on the archived v16.23 projection and the two positive inputs verify the distinction. This is mathematical recoverability from the receiver vector. The executed constructor uses the ownership mask.

Grok's common-address objection in PR 111 holds in this example. The subtree sum at p is 8 on both sides. In the root-balanced source coordinates of v16.22, both the flat and depth-weighted responses at every retained address coincide with the restriction of the full response. At p both choices give 8 in both histories. In this convention subtracting the fine total at the root represents the nonroot coordinates on the zero-sum space. The receiver's P1 atom at p can still be 8 or 6 because it excludes the separate b atom when b survives. With both edited tip grades set to zero the ownership transfers persist, recoverability for arbitrary inputs still differs, and both fork atoms and both tested responses at p are 4. These controls distinguish change of view, change of a numerical atom, and common-address response.

## Exactly how much depends on the target

Write a target as the three singleton holders of a,b,c in that order. There are 18 assignments using exactly two of the three charts. In all 18, the first singleton assignment is determined by the initial post-source masks alone. For an actual first transfer to read b in both arms, the target palette must be H,S. If it is S,R, the first history starts by replacing H on a. If it is H,R, the second history starts by replacing S on a or c. In the H,S case the second history must first transfer b from R to H. In the first, the archive takes the first differing tip in index order. Consequently only three targets ever give a first read of b in both arms.

| Target (a,b,c) | Matched pairs reading b first in both arms | Reason |
|---|---:|---|
| (H,H,S) | 144 of 144 | Only b differs in the first arm |
| (S,H,H) | 48 of 144 | b must precede both other differing tips |
| (S,H,S) | 72 of 144 | b must precede a |
| Other 15 | 0 of 2,160 | At least one arm starts elsewhere or makes no transfer |

For the two targets equal to an initial singleton assignment, (H,S,S) and (S,R,S), one arm has no transfer beyond surplus removal. These cases account for 288 matched pairs. Counts include both geometries, two grade preparations, all six chart index orders and all six sibling index orders. Each arm of the 2,592 matched pairs was independently reconstructed, including every materialized state, profile, live read value, fixed fine test and endpoint. The verifier rejects twelve corruptions of identity, path, coverage, numerical result and provenance. These exhaustive counts apply to this stated finite family.

## Source-only counterexample and status

Under unrestricted v16.26 pruning S may delete both a and b in either order. The same terminal state results in both arms: S holds c, H holds a, R still holds b, and H alone holds d when present. Every remaining tip has exactly one holder. Removing an internal ancestor would violate prefix closure, so there is no further legal deletion. Thus the source alone admits complete indistinguishable receiver histories. A supplied two-endpoint route gives an existing consumer of a source-dependent chart distinction. A native rule requiring that route, or an equivalent receiver-accessible operation, is still missing. No physical gravity observable follows from this finite construction.

### Provenance and reproduction

The intervention and fixed target were registered in 1b138d7c0cefde8e613179050fb7752c6b32447f; the anchored preparation and all-target controls in 5b266b4d34515ed12787cbac0594274f8056cec2, both before scientific execution. Historical source is e61d5b0e827f7b412824ad46021e2ad6cc6f7875. Premises: the P1 projection and historical operations are inherited; the preparation, invocation and common target are supplied experimental inputs; the matched read, target classification and scope of the comparison are derived. A local source-pin check initially caught a transcribed v16.39 checker identifier before any scientific execution. It was corrected against the archived Git tree. The publication evidence includes the diagnostic.

From the repository root, with the historical checkout at review_sources and SymPy installed, run:

```sh
SCI=ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths
python "$SCI/check_receiver_shape.py" review_sources replay
python "$SCI/verify_receiver_shape.py" replay
```

[Original constructor](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/construct.py#L21-L83) · [Original campaign entry](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/campaign.py#L31-L42) · [Grok's shape question](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7149694094) · [Earlier fork adjudication](https://github.com/proteinfoldingengine/WetLabEngine/pull/156#issuecomment-7147247291)
