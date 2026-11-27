# Two empty remote charts distinguish the earlier path, even when their names are discarded

Start from the matched four-chart star in [the path/triangle result](../joint_withdrawal_constraint_loops/RESULT.md). Given that A released exactly one of the two candidate tips first, two other charts can end with just their roots after the release that leaves a path. That outcome is impossible after the release that closes a triangle. In the old v16.29 archive we found the actual two-write square ending at these two bare roots. The older archive starts at the square's own initial state. We verified its connection to the longer preparation separately.

There is a causal limit. The other charts can reach the identical record *before A makes any release*. Their own holdings and their full sequences of local P1 grade vectors are identical in the source-first and source-last replays. This is a persistent distributed record that distinguishes two specified source-first histories. Taken on its own, it cannot tell the participants that a source event has occurred.

## From possible actions to actual retained records

The common source A owns tips 1 and 2. B owns 1, 3 and 4; C owns 1, 2 and 3; D owns 2 and 4. Every chart also holds the root. The input holdings and the two source alternatives are supplied. The only subsequent operation is the original union-preserving withdrawal. It edits one chart's retained row. Other charts may act in any order, and the run may stop at any prefix.

| First source cut | What two actual remote records can establish using site identities | What survives removal of all remote chart and tip names |
| --- | --- | --- |
| A releases 1, leaving the path | If C and D both lose tip 2, A had to retain it. Their two rows exclude the other source choice. | Two bare roots can occur. The other remote chart has three tips. |
| A releases 2, closing the triangle | If B and C both lose tip 1, A had to retain it. Their two rows exclude the other source choice. | Every multiset of remote tip counts reached in this arm can also occur in the path arm. |

The triangle has an incompatibility edge between every remote pair: every pair is the entire set of holders of at least one covered leaf. Two of those charts can never both become bare. In the path arm C and D have no such edge, and A together with B can keep the union even if C and D both empty. Both bare rows persist through every subsequent withdrawal. In the original P1 calculation with grade 1 at each of the five vertices, a chart keeping k tips has root grade 5−k and grade 1 at each retained tip. The two bare roots therefore each contain the numerical record (5). The address-free conclusion uses only the individual unlabelled shapes of the remote rows: their sorted tip counts are (0,0,3). Their shared-site incidence and their names are discarded. The boundary excluding the specified source is still supplied. Sorting the tip counts of *all four* charts with no source marker gives no exclusive signature in the named example.

Both hypotheses can be identified using a pair of addressed records, with only two post-source withdrawals in the appropriate pair. No single remote row or its own successful action history identifies either arm. The previous single-chart theorem covers those action histories, and the complete snapshot comparison here covers every remote subset. The unlabelled two-root outcome requires five post-source withdrawals from the common remote prior.

## General criterion for a distributed record

Let A have two distinct legal cuts x and y in the same starting family of ancestor-closed rows on a finite rooted tree. Fix a set G excluding A. Suppose A−x happens first. Let H(y) be all non-A charts initially holding y. For an *attainable* snapshot of G after A−x, the following statements are equivalent:

1. The snapshot cannot occur after A−y.
2. G includes H(y), and every member of H(y) has lost y.

The matching statement with x and y interchanged also holds. Such a positive record exists precisely when y is a leaf of the covered union and G includes H(y). Its minimum cost is one actual release at y by every member of H(y). Further withdrawals preserve the resulting exclusion. The hypotheses include the known common preparation and the two specified source alternatives. The record does not encode unrestricted event provenance.

**Derivation.** To realize a group's snapshot, freeze the exterior after the initial source cut. The intended remote rows must be componentwise retained subviews. Together with the frozen exterior they must cover the original union. These conditions suffice: remove unwanted local leaves, descendants first. Every intermediate family still contains the final covered family. Equivalently, any actual remotely observed sequence can be executed with the exterior frozen, preserving all local leaf tests and coverage.

Switching the source hypothesis from x to y *restores* x to the exterior. Only y can lose exterior coverage. The proposed rows thus fail in the other history precisely when H(y) is contained in G and every such holder has lost y. For a covered leaf, each holder in H(y) can relinquish it in the true history with A retaining its copy. Each such chart must make at least one edit. If y has a covered child, A cannot hold the child because y was locally withdrawable there. When G contains H(y), at least one group member must retain the child, hence y, throughout. The argument yields an exact criterion without introducing a reader or assigning a new storage field.

On the matched star, after the first cut there are three possible situations. While A and at least one remote still hold the uncut tip, both outcomes remain possible. If all its remote holders release it, the corresponding two-row certificate is permanent. If A releases that tip instead, it has released both alternatives and the full state is compatible with either first cut. In this example the entire common continuation graph begins at the double cut. The term "erased" in the data refers to this ambiguity of the full retained holdings and the projected remote words, not loss from a separate central event log.

## Every continuation, including stopping early

The replay exhausts all 24 indexed path/triangle comparisons identified in the original census. On each of the 48 arms it obtains 189 states, 621 directed edits and 2,880 complete ordered paths. Across all 24 comparisons the only remote shape signature exclusive to the path is (0,0,3). There is no triangle-exclusive anonymous remote signature, even when comparing only terminal shapes. No completion or stop signal is needed to recognize the path-exclusive pair of bare roots when it occurs. Each source choice also admits outcomes compatible with both histories.

For the named case, each arm has 27 states whose three addressed remote rows exclude the alternate arm, 81 states also reachable as full states in the other arm, and 81 earlier states from which either outcome remains possible. At exhaustion, eight of 24 full terminal states in each arm carry an exclusive addressed remote record. The other 16 terminals are shared by both arms. In each arm 960 complete event words finish with the exclusive addressed record and 1,920 finish at a common state. These are counts of unweighted words. Only one terminal in the named path arm has the anonymous signature (0,0,3). The full graph certificate covers arbitrary prefixes, terminal states and all directed edges. [Counts and named case](results.json) · [Complete graphs and projection counts](records.json.xz).

## Historical square and source-last control

The old five-site star group, code (()()()()), original variant, contains the predicted square at **zero-based entry 14,633**, starting at byte 20,039,362 of the decompressed archive. In archive order A,C,D,B its initial masks are (5,9,17,27). Its two events remove C's last tip 3 and D's last tip 4. Both orders reach (5,1,1,27). The entire archived certificate matches a fresh v16.29 certification, and all four edges agree with original v16.26 returns. The archived verifier accepts it and rejects a substituted final C row. The certificate's canonical SHA-256 is 41185f12aeb464930ffdd4dd54ba4e54d947c0cd75d4fb652f38fc3de693f04d. The archive's ZERO classification concerns the cover-profile/height response of this square. [Original archive](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/FULL_CERTIFICATES.json.xz) · [Historical verifier](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/verifier.py#L55) · [Extracted certificate and order controls](archive_order.json).

From the original matched preparation, take remote events C−1, C−2, D−2, C−3, D−4. With A−1 first, the last two moves reproduce the archived square. With A−1 last, C and D already have their bare roots before the source event. Without any A event, they have the same bare roots and the same local P1 histories. Now A can still release 1, while A−2 would discard the only remaining copy and the historical atom rejects it. Thus the same record can anticipate which source release remains possible.

Every one of the 720 orderings of those six distinct withdrawals reaches the identical full endpoint; A occurs in each position 120 times. For every accepted step in every ordering, parent cover and height stay 2, trigger stays false and the height increment is zero. The original complete receipts do contain global before/after states; equality of the scalar fields does not imply equality of full receipts. Equality of entire individual participant histories was tested on the matched source-first, source-last and no-source runs with the remote order fixed.

More generally, fix any successful withdrawal-only run. Preserve the internal sequence of each chart's actions and interleave the charts in any other order. Each chart's local leaf tests are unchanged. Every intermediate atlas contains the fixed final atlas componentwise, so it preserves the union. In particular, all remote subsequences can run before the source chart's subsequence, even when individual charts contain nontrivial ancestry. This argument concerns holdings and local P1 push on a common fixed grade; it need not preserve cover-trigger or height fields in other examples. It applies the inherited endpoint factorization and ancestry results to the causal interpretation of the new witness. [Original factorization proof](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md) · [Inherited within-chart predecessor structure](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.31-global-component-factorization/PROOFS.md).

## Reproduction and scope

The original-atom replay enumerates the 24 cases and invokes the historical per-atom verifier and P1 push. The separate checker enumerates all endpoint subviews by Cartesian product and reconstructs every graph edge, exact projection and terminal path count. The four-site comparison checks 942 same-actor pairs among 1,198 reachable indexed states, 6,966 group comparisons and 52,221 projected snapshots across the two arm directions. [Independent verification](verification.json) · [Scope before enumeration](SCOPE.md) · [Archive lookup scope](ARCHIVE_SCOPE.md) · [Source-order control scope](ORDER_SCOPE.md).

With DEMOS set to the demos directory at historical SHA e61d5b0e827f7b412824ad46021e2ad6cc6f7875 and PRIOR pointing to the pinned joint_withdrawal_constraint_loops directory of PR #174, run on Python 3.11 with SymPy 1.13.3 and mpmath 1.3.0:

```bash
set -euo pipefail
python -B replay.py "$DEMOS" "$PRIOR" fresh.xz | cmp - results.json
python -B verify.py fresh.xz "$PRIOR" | cmp - verification.json
python -B archive_order.py "$DEMOS" | cmp - archive_order.json
```

These records reside in two actual retained rows. Access to both by one participant, a source-triggered dispatch and transport around a loop remain open. The native constraint affects which joint futures survive. The source-last control excludes a requirement that the source act before these particular locally retained records are formed.
