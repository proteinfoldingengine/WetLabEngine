# A first response by the remaining holder, and what a current work measurement reveals

On the five-chart fixture, B's withdrawal at tip 5 identifies a second chart, F. F is the only remaining holder of that tip. After the same two subsequent deletions in both source histories, every successful first edit by F writes a persistent record of which source history produced B's tip-5 increment. The identity of F's edit follows from ordinary last-copy preservation. The P1 vector at F distinguishes its blank state from either written state. Reading the written bit uses the retained tip addresses.

There is a separate result about the withdrawal at tip 6. With unrestricted ordering, a particular combination of B's retained grade and two work measurements incident on B certifies a completed A withdrawal and its positive cover increment. B's own P1 data alone can stay unchanged. The two results concern different events.

## Native response at the remaining holder of tip 5

The [supplied unit-grade star](../../../FIXTURE.json) has charts B, A, E, F and X. The two historical source choices are A deleting (1,2) or (3,4), followed in both cases by B deleting 5. The historical joint increment at this B event is respectively 0 or 1. Before that event the holders of 5 are exactly B and F. Afterward 5 is private to F. F's own row is the Pin with tips 2, 4 and 5 in both histories. Its P1 root is 5 and its ordinary deletion menu at this point is {2,4} in both arms.

Now let E release 2 and X release 4. Both ordinary edits succeed in both source histories, in either order. No receipt value selects them. Their effect on the remaining holders is decisive.

| Old B-at-5 increment | Holders of 2 | Holders of 4 | Holders of 5 | Only possible first F deletion | F's surviving tips |
|---:|---|---|---|---|---|
| 0 | F | A and F | F | 4 | 2 and 5 |
| 1 | A and F | F | F | 2 | 4 and 5 |

In either arm F's root rises from 5 to 6 when F acts. Its two surviving tips are private, so no later ordinary deletion can undo the record. Its root alone marks that an F edit occurred; the retained address 2 versus 4 gives the value. Prior to its response F has identical complete addressed P1 and identical incident work in the two arms. Its *legal menu* now differs. Full holder identities for all F sites are not matched inputs. After the common preparation any intervening edits preserve this conclusion for a successful F event, since they can only remove its remaining opportunity.

**Why those edits.** Enumerate common successful non-F preparatory commands from both states immediately after B drops 5. At 2 the possible common non-F deletion is E's; F can give up 2 in the old-0 arm until E does so. At 4 the analogous editor is X in the old-1 arm. A's other tip holdings are disjoint across source arms, so common A commands cannot replace these steps. Commands at 6 change neither F comparison. The resulting paired graph has 12 states and 20 edges. Precisely the three states in which both E-at-2 and X-at-4 have occurred have two nonempty, disjoint F menus. The third independent choice is whether and how 6 has resolved. Thus those two edits are jointly necessary and sufficient in this class. They are the unique shortest set, with two possible orders.

**Role of the earlier event.** If B's withdrawal is omitted and the same E and X cuts occur, F can release 5 in both source arms. That successful edit leaves exactly the same F row, with tips 2 and 4. The earlier B withdrawal is therefore necessary for the guarantee that *every* possible first F edit separates these histories under this preparation. The source choices had already selected different incidences at 2 and 4. No calculation in F takes the old numeric certificate as input.

**Occurrence.** From either prepared state there are 27 states, 54 edges and eight terminal states. In four terminals F has written the record. In four F still has all three tips. If A makes no further cut after preparation, its copy of the one shared F tip remains available and every maximal continuation contains F's unique edit. If A can act freely, it can remove its remaining non-6 tips in each arm, leaving F unable to edit and bringing both arms to the *same full atlas*. The preparation and the opportunity for F to respond are genuine conditions. Outside the prepared family, the archive includes a wrong-arm terminal with the same complete F state and all ten work readings as a written old-1 terminal.

## What B can certify about a remote withdrawal without a preparation phase

Start immediately after B's tip-5 probe in either source history. All later ordinary cuts by all five charts are now permitted. With seven unit tips, the P1 root at B is 8 minus the number of its retained tips. Pair work is the number of tips in the symmetric difference of the two rows. The following three current readings suffice:

| B root | Work between B and A | Work between B and E | Necessary earlier event |
|---:|---:|---:|---|
| 7 | 3 | 1 | A released tip 6 and increased the minimum cover from 3 to 4 |

B then retains just 6. E never holds 6, so B–E work 1 means E has no remaining tip. Only the old-0 source arm permits this because E alone owns 3 in the old-1 arm. A starts that old-0 continuation with tips 3, 4 and 6. Work B–A equal to 3 forces A to have given up 6 while retaining 3 and 4. F holds 2 now, because E has relinquished it, and consequently held it at A's withdrawal. At that withdrawal F and X were compulsory via private tips 5 and 7. Together with A they covered all tips. Replacing A by B would miss 3. A withdrawing from 6 therefore destroys every triple cover and adding B gives a four-chart cover.

The three edits A-at-6, E-at-2 and E-at-3 can occur in any of their six orders. The readings and the positive A increment hold in all six. In particular, both exterior edits can follow A's withdrawal. No single incident work coordinate together with B's unchanged root of 7 certifies an A-at-6 increment of one on this two-arm domain. These two readings are sufficient where their specified values occur; some later edits can change them. Releasing 4 from F and X after this example gives an all-private terminal where B retains root 7 and its entire incident work row is permanently (3,1,3,3), in A,E,F,X order.

There are also persistent, sometimes inconclusive, indications of the *earlier source*. E and X are each disjoint from B outside the Pin. Subtracting B's own tip count from B–E or B–X work gives E's or X's tip count. E reaching zero certifies the old-0 source, since E's private 3 forbids zero in the other arm. X reaching one certifies the old-1 source, since X retains both 1 and 7 in the old-0 arm and always retains 7. Once reached, either count persists. Both indications remain possible if B's tip-5 event is omitted, so they establish source information and cannot independently establish that the earlier receipt was delivered. With only A held fixed, every maximal branch in the old-0 arm makes E relinquish 3, and every maximal branch in the old-1 arm makes X relinquish 1. Those address-level indications also survive. A common schedule allowing B,E,X to exhaust their moves while A,F wait gives the two exclusive count tests in both arms. No such priority is required for their soundness when observed.

## Entire current geometry and historical attribution

Reconstruct every ordinary continuation after the old B event. Each source arm has 189 states and 621 directed single-edit edges. Their union has 351 distinct indexed states and 291 distinct labelled pair-work tables. A work table always determines whether tip 6 is pending, A has withdrawn, or B has withdrawn. It can leave the amount of the past cover increment ambiguous.

| What histories are consistent with one current work table | Number of distinct tables |
|---|---:|
| Tip 6 pending | 97 |
| B withdrew, increment 0 | 97 |
| A withdrew, increment definitely 0 | 18 |
| A withdrew, increment definitely 1 | 27 |
| A withdrew, increment could be 0 or 1 | 52 |

An explicit common-endpoint control exchanges A-at-6 and X-at-1 immediately after the old-1 probe. A receives increment 0 if it acts first and 1 if it acts second. The final indexed states coincide. Thus knowing the current atlas can establish both completion and actor while losing the original increment.

Across the union of the two arms, the unique smallest fixed set of pair measurements determining pending/A/B for *every* state contains nine of the ten labelled entries, all except B–F. If B's own P1 root is also supplied, the unique smallest fixed set is B–A, A–E, A–F, A–X, E–F, F–X. The checker examines all 1,024 coordinate subsets under each information assumption. These are finite exact results for this fixture. They measure the number of fixed raw pair entries, without assuming adaptive queries, physical availability, or independent scalar degrees of freedom. As a local counterexample, in the old-0 arm compare the state immediately after the B probe with A subsequently deleting 6 and 4. All B P1 entries and all four B-incident works coincide, while completion differs.

## Provenance and replay

- **Inherited.** [P1](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py), [union-preserving atom and verifier](https://github.com/proteinfoldingengine/WetLabEngine/tree/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law), the [pair-work function](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py), and the [pinned last-copy checker](../../check.py). Source bytes are verified by Git blob ID.
- **Supplied.** The five-chart fixture and the original source and B events. The F result assumes its common preparation. The geometry search allows every subsequent ordinary deletion from either post-B state and uses current, labelled work. A B-owned operation that physically accesses these pair values remains open. P1 ownership of an indexed row is mathematical. Neither a degree-four carrier nor physical geometry is established here.
- **Verification.** The unrestricted geometry observations and planned exhaustive checks were [disclosed before verification](https://github.com/proteinfoldingengine/WetLabEngine/pull/161#issuecomment-7175798157). The analytic local certificates and remaining-holder response were subsequent exploratory discoveries. The independent state universe is the product of nonempty holder subsets; every state and edge agrees with native generation. A separate incidence calculation reconstructs cover sizes and propagates all possible prior records through the acyclic graph. An independent symmetric-difference sum checks every historical work calculation. Raw bytes and the summary were identical across two Python hash seeds. These are history and state counts, without a sampling law.

Use Python 3.11+ and SymPy. From this directory, pass the historical checkout at `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`.

```bash
python3 -B check_snapshots.py /path/to/WetLabEngine --raw actual_raw.json > actual.json
cmp actual.json result.json
xz -dc raw.json.xz | cmp - actual_raw.json
```

[Replay](check_snapshots.py) · [Exact results](result.json) · [All native edges, current observations and controls](raw.json.xz)
